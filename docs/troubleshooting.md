# 已知问题与排查

## 启动

**一启动就弹「检测到游戏未启动」**

`PanelManager.__init__` 会先 `pymem.Pymem("Gwent.exe")` + 取 `GameAssembly.dll` 基址，失败就
`tips_show("警告","检测到游戏未启动!")` 然后 `destroy()`。先开游戏，再开记牌器。

没有游戏只想看界面，用 `python gui_demo.py`。

**界面出来了但一直空白 / 没有牌**

说明附加成功但读到的牌表为空。检查：

1. `resources/config/version.json` 的 `address` 是否与当前游戏版本匹配（点主窗「更新」页）；
2. 是否在观战/单人模式（这两类局本来就没有双方牌表）；
3. 主窗「日志」页看有没有读取异常。

**主窗「分辨率」第二行被裁掉**

原始 `geometry` 是 `250x280`，内容比它高。这是上游布局问题，功能不受影响；
`gui_demo.py` 截图时按内容自适应高度。

## 数据

**游戏更新后读不到牌**

内存偏移与游戏版本强绑定（`CardDao.py` 里全是硬编码偏移）。点主窗「更新」页，
从 `/version/api/getId` 拉新的 `address` 再重开。

**卡组预测不出现**

`global_config.comparative` 要打开，且 `resources/data/decks.json` 要有内容
（由 `GET /deck/api/getDecks` 同步，或从别处拷一份）。

**战报没上去**

`RequestManager.postBattleInfo()` 里是 `try/except` 吞异常的，只在控制台打印「发送对局信息失败!」。
检查 `global_config.url` 是否能从本机访问，以及服务端 `/battle/api/save` 是否返回 200。

## 素材

**卡图位置空白**

`resources/images/GwentImg_preview/` 里缺这个 cardId 的 jpg。仓库只带了 1369 张缩略图，
新增卡可能没有；用 `main/resources/images/GwentImg_preview/` 补同名文件即可。

**没有高清原画**

这个目录只带了界面必需的素材（`deck_preview` 57 张 + `GwentImg_preview` 1369 张），
没有 `GwentImg原图`（约 300 MB），需要时用
`main/othersFile/从gwent获取图片.py` 重新抓。

**字体缺失导致中文变方块**

`resources/fonts/` 里有 `YSHaoShenTi-2.ttf`（界面标题）、`JZJDCYJF.ttf`、`NEOESPORT-2.ttf`，
`FileTool.getTextImg()` 直接按相对路径加载，缺文件会抛异常。

## 离线复现脚本

**`gui_demo.py` 报 `ModuleNotFoundError: ttkbootstrap`**

```bash
pip install pillow ttkbootstrap pywin32
```

**截图里是浏览器/桌面而不是窗口**

悬浮窗是 `overrideredirect + WS_EX_LAYERED` 的透明窗，脚本会先垫一层深色背景并置顶。
如果有多显示器或缩放比例异常，`ImageGrab` 的坐标可能对不上，用 `--out` 换输出路径后重跑，
或临时关掉其它置顶窗口。

**`--tab 手牌` 截图很矮**

手牌只有几张时列表就那几行，这是正常的；脚本会按内容裁掉多余空白。

## 打包

**`pyinstaller GwentMirror.spec` 打出来的 exe 起不来**

spec 里的路径是作者机器上的绝对路径（`G:\GwentWanHuaMirror\...`），
改成本机路径再打包；同时确认 `main/resources` 整个目录随包分发（程序用相对路径读配置与图片）。

## 平台

只支持 Windows——`pymem`、`win32gui`、`win32api` 都是 Windows 专用，
所以它也不能放进 Linux 容器。服务端与前端在
[GwentMirrorAllInOne](https://github.com/1053278842/GwentMirrorAllInOne) 的镜像里。