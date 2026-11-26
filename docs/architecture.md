# 原理与结构

## 数据是怎么来的

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

四条要点：

* **附加进程**：`pymem.Pymem("Gwent.exe")` + `GameAssembly.dll` 基址；
* **版本偏移**：`version.json` 里是 `address / addressGOG / addressGY` 三个基址偏移，
  客户端会向 `/version/api/getId` 拉最新版本记录来决定是否切基址；
* **卡牌数据表**：`resources/config/card_json_local.json`（1427 张卡的名称/人口/战力/类型/势力），
  `resources/data/decks.json`（3488 副官网卡组，用于「预测卡组/差异对比」），
  `resources/data/LeaderCardData.json`（领袖）；
* **卡图**：`resources/images/GwentImg_preview/<cardId>.jpg`（1369 张缩略图），
  UI 切图在 `resources/images/deck_preview/`，字体在 `resources/fonts/`。

## 目录

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

## 悬浮窗是怎么拼出来的

`GwentGUI` 创建一张无边框窗口，然后依次放五个 `Frame` 里的 `Canvas`：

| 画布 | 高度来源 | 画什么 |
| --- | --- | --- |
| `bg_img` | `WIN_HEIGHT` | 上/中/下三段背景图拼接 |
| `title_board` | `TOP_HEIGHT * 0.40` | 当前页签名 + 左右切换箭头 |
| `module_board` | `TOP_HEIGHT * 0.55` | 6 个页签按钮，当前页签高亮 |
| `status_board` | `TOP_HEIGHT * 0.20 + offset` | 剩余张数 / 单位数 / 总人口 |
| `card_preview_list_board` | `MID_HEIGHT + 4%` | 卡牌列表（逐张 `create_image`） |

`TOP_HEIGHT / MID_HEIGHT / BOTTOM_HEIGHT` 由 `bg_img` 按图片实际尺寸算出来，
其余四个画布都依赖它，所以初始化顺序不能变。

窗口透明靠 Win32 API：给每个 Frame 加 `WS_EX_LAYERED`，把 `0x222222` 设为 colorkey 色，
该颜色在窗口里变成完全透明，看起来就是浮在游戏画面上。

## 数据流的三段

**读**：`CardDao` 里全是硬编码偏移（`gi+0x20`、`[0x60,0x18,0x20+i*0x8,...]` 这种），
每个方法读一类东西：玩家 id、牌表、每张牌的位置/战力/人口、对局状态、回合信息。

**算**：`CardService` 把读到的原始结构转成 `{Id, PlayId, Location, Index, Provision, BasePower, ...}`，
再按当前页签过滤（牌库/手牌/墓场/放逐/场地），按人口或索引排序；
「预测卡组」会用 `decks.json` 里 3488 副官网卡组做匹配与差异对比。

**画**：`card_preview_list_board.updateData()` 每 400ms 轮询一次，比对上一帧，
新增的牌做白框动画；`CardView` 的等价逻辑在 `FileTool.get_deck_preview_img()`
（把卡图与人口/战力/稀有度合成一张图）。

## 主控制窗

`GwentMirror.py` 的 `create_page()` 用 ttkbootstrap 的 darkly 主题搭 5 个页签：

| 页签 | 内容 |
| --- | --- |
| 启动 | 我方/对方记牌窗开关、分辨率（宽/高） |
| 更新 | 版本拉取（Steam / GOG / GY 三个平台基址） |
| 高级 | 差异对比、真实牌组顺序、共享对局卡组 |
| 日志 | 更新日志文本 |
| 其他 | 官网/下载/卡组站三个按钮 |

⚠️ 原始 `geometry` 是 `250x280`，启动页内容比它高，「分辨率」第二行会被裁掉；
`gui_demo.py` 截图时宽度保持 250、高度按内容自适应。