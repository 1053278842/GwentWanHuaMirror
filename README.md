# GwentWanHuaMirror · 昆特记牌器（桌面端）

Windows 桌面小工具：以**透明置顶悬浮窗**的形式，实时显示自己和对手的牌库/手牌/墓场，
对局结束后把整场战报上报给服务端，顺便充当官网卡组库的抓取端。

> 本目录是 [gwent-mirror-all](https://github.com/1053278842/GwentMirrorAllInOne) 一体化项目的桌面层。
> 它无法跑进 Linux 容器（要附加 `Gwent.exe` 读内存），所以镜像里只放了服务端与前端；
> 这里的代码给 Windows 侧用，界面的离线复现在 `gui_demo.py`。

![记牌器悬浮窗](docs/screenshots/06-desktop-overlay.png)

---

## 1. 它是怎么工作的

```text
Gwent.exe ──┐
            │  pymem 附加进程
            ▼
  GameAssembly.dll 基址 + 版本偏移表（resources/config/version.json 的 address）
            ▼
      GameInstance ──► Players / Cards / RoundInfos
            ▼
   dao/CardDao.py  initCtData()  ──►  {Id, PlayId, Location, Index, Provision, BasePower, ...}
            ▼
   services/CardService.py         ──►  按位置/玩家/类型过滤、按人口或索引排序
            ▼
   views/* （tkinter Canvas 成帧）  ──►  悬浮窗逐张画卡
            ▼
   RequestManager.sendBattleInfo() ──►  POST {server}/battle/api/save
```

* **附加进程**：`pymem.Pymem("Gwent.exe")` + `GameAssembly.dll` 基址；
* **版本偏移**：`version.json` 里是 `address / addressGOG / addressGY` 三个基址偏移，
  客户端会向 `/version/api/getId` 拉最新版本记录来决定是否切基址；
* **卡牌数据表**：`resources/config/card_json_local.json`（1427 张卡的名称/人口/战力/类型/势力），
  `resources/data/decks.json`（3488 副官网卡组，用于「预测卡组/差异对比」），
  `resources/data/LeaderCardData.json`（领袖）；
* **卡图**：`resources/images/GwentImg_preview/<cardId>.jpg`（1369 张缩略图），
  UI 切图在 `resources/images/deck_preview/`，字体在 `resources/fonts/`。

## 2. 目录

```text
desktop/
├─ gui_demo.py                  # 离线复现 GUI 并截图（不开游戏也能出图）
├─ GwentMirror.spec             # PyInstaller 打包脚本（原作者的）
└─ main/
   ├─ GwentMirror.py            # 主控制窗：启动/更新/高级/日志/其他 5 个页签
   ├─ GwentGUI.py               # 对局内悬浮窗：透明、置顶、可拖动、双击关闭
   ├─ PanelManager.py           # 检测进程、开关我方/敌方面板、对局状态轮询
   ├─ ResponseManager.py        # 把内存数据分发给 5 个画布
   ├─ RequestManager.py         # 与服务端通信（getDecks / getId / battle save）
   ├─ views/
   │  ├─ bg_img.py              # 背景板（上/中/下三段拼接）
   │  ├─ title_board.py         # 标题栏（页签名 + 左右箭头）
   │  ├─ module_board.py        # 6 个页签按钮：卡组/牌库/墓场/放逐/手牌/场地
   │  ├─ status_board.py        # 统计行：剩余张数 / 单位数 / 总人口
   │  └─ card_preview_list_board.py  # 卡牌列表（43 KB，整张牌一张一张画）
   ├─ dao/CardDao.py            # 全部内存偏移都写在这里
   ├─ services/CardService.py   # 卡牌数据装配与过滤排序
   ├─ tools/{FileTool,MemoryTool,DataUtils}.py
   └─ resources/{config,data,fonts,images}/
```

## 3. 在 Windows 上真正跑起来

```bash
cd desktop/main
pip install pymem pillow ttkbootstrap pywin32
# 先起服务端（容器或本地后端），把 resources/config/global_config.json 的 url 指过去
python GwentMirror.py
```

前置条件：

1. 游戏在运行（否则 `PanelManager` 直接弹「检测到游戏未启动」并退出）；
2. `resources/config/version.json` 的 `address` 与当前游戏版本匹配
   （不匹配就点主窗「更新」页去服务器拉新的版本记录）；
3. 服务端 URL 在 `global_config.json` 的 `url`，默认是作者的线上库。

## 4. 离线复现界面（不用游戏）

`gui_demo.py` 把「读内存」这层换掉，界面代码和素材保持原样，用于截图/演示：

```bash
cd desktop
pip install pillow ttkbootstrap pywin32
python gui_demo.py --target both                  # 主窗 + 悬浮窗
python gui_demo.py --target overlay --tab 手牌     # 指定页签
python gui_demo.py --target overlay --enemy       # 敌方视角
```

替换了哪些东西：

| 原始实现 | demo 里的替身 |
| --- | --- |
| `pymem.Pymem("Gwent.exe")` | 注入假 `pymem` 模块，`read_longlong/read_bytes` 返回 0 |
| `CardService.get_all_cardTemplates()` | 从 `resources/data/decks.json` 取一副素材齐全的卡组，摊平成 `initCtData()` 的字段结构 |
| 当前玩家 / 双方 id / 牌库实例 id 区间 | 固定值（`getCurrBattleInfo` / `getPlayerCarriedCarInsIds` 等几个函数打桩） |
| `GwentGUI` 与 `views/*` | **原样调用** |
| 卡图、UI 切图、字体 | **原文件** |

截图前会垫一层深色窗口再抓屏，因为悬浮窗本身是
`overrideredirect + WS_EX_LAYERED（colorkey 0x222222）` 的透明置顶窗口，
直接抓屏会把桌面/浏览器一起拍进去。

主控制窗（原始 geometry 250×280，内容比它高，截图时按内容自适应高度）：

![记牌器主窗口](docs/screenshots/05-desktop-main.png)

## 5. 上报协议

对局结束（`GameStatus == ENDED`）且不是单人/观战/友谊赛/竞技场时，
`RequestManager.sendBattleInfo()` 会 POST 到 `{url}/battle/api/save`：

```jsonc
{
  "GameStatus": 3, "GameMode": 1, "GameId": 1732..., "BattleType": 2,
  "roundInfos": [{ "index": 0, "left_score": 12, "right_score": 8,
                   "starting_playerId": 1, "winner_playId": 1, "turn_index": 11 }, ...],
  "curr_round_index": 2, "winner_playId": 1, "end_game_reason": 0,
  "players": [
    { "player_name": "...", "service_id": 900000000000000001, "paragon_level": 0,
      "MMR": 9600, "rank": 0, "leader_id": 200087, "stratagem_id": 0, "faction_id": 4,
      "decks": [200087, 0, 202115, 201779, ...],   // leader + stratagem + 牌表
      "deckId": 1234567890123456789 }              // hash(frozenset(decks))
  ]
}
```

字段与 `dao/CardDao.py:getBattleInfo()` 一一对应。
**没有游戏的机器**可以用仓库根目录的 [`scripts/simulate_battle.py`](https://github.com/1053278842/GwentMirrorAllInOne/blob/main/scripts/simulate_battle.py) 按同样的结构回放对局，
把「客户端上报 → 后端入库 → 前端可见」这条链路跑通。

另外两个接口：

* `GET {url}/deck/api/getDecks` → 本地卡组库（写 `resources/data/decks.json`），用于预测卡组；
* `POST {url}/version/api/getId` → 版本记录（写 `resources/config/version.json`）。

## 6. 桌面包（可选）

```bash
cd desktop
pyinstaller GwentMirror.spec      # 产出 dist/GwentMirror.exe，单文件、无控制台
```

## 7. 已知限制

* 只支持 Windows（`pymem` / `win32gui` / `win32api` 都是 Windows 专用）；
* 内存偏移与游戏版本强绑定，游戏一更新就要重新校对（`CardDao.py` 里全是硬编码偏移）；
* 这个目录只带了界面必需的素材（`deck_preview` 57 张 + `GwentImg_preview` 1369 张），
  没有 `GwentImg原图`（约 300 MB 高清原画），需要时用
  `main/othersFile/从gwent获取图片.py` 重新抓；
* `main/othersFile/` 里是作者抓卡图/卡表/卡组的一次性脚本（含 `chromedriver.exe`），
  其中 `抓取卡组-官网.py` 已整理成仓库根目录的 `scripts/fetch_decks.py`（去 GUI 依赖、加线程池）。