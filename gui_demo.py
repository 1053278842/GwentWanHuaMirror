#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GwentWanHuaMirror 桌面端 GUI 离线复现 / 截图工具
================================================

记牌器本体是「读 Gwent.exe 进程内存 + tkinter 悬浮窗」的 Windows 程序，
没有游戏进程就无法启动（PanelManager 会直接弹「检测到游戏未启动」并退出）。

本脚本用**替身数据源**替换掉内存读取层（只替换 dao 层的读数函数），
其余界面代码（GwentGUI / bg_img / title_board / module_board /
status_board / card_preview_list_board）全部使用仓库原始实现，
因此渲染出来的就是真实界面：

  python gui_demo.py --target overlay   # 对局内悬浮记牌窗
  python gui_demo.py --target main      # 主控制窗（启动/更新/高级/日志/其他）
  python gui_demo.py --target both      # 两张都截

截图默认写到 ../docs/screenshots/ 。
"""
import argparse
import json
import os
import sys
import time
import types

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)                                   # 代码里大量 'main/resources/...' 相对路径
sys.path.insert(0, os.path.join(HERE, "main"))


# --------------------------------------------------------------------------
# 1) 假 pymem：让 dao 层的内存读取全部返回 0，而不是抛异常
# --------------------------------------------------------------------------
class _FakeModule:
    lpBaseOfDll = 0x7FF600000000


class _FakePymem:
    def __init__(self, name=None):
        self.process_handle = 0xDEAD

    def read_longlong(self, address):
        return 0

    def read_bytes(self, address, length):
        return b"\x00" * length


pymem_stub = types.ModuleType("pymem")
pymem_stub.Pymem = _FakePymem
pymem_stub.process = types.SimpleNamespace(module_from_name=lambda h, n: _FakeModule())
sys.modules["pymem"] = pymem_stub

import bean.global_var as global_var          # noqa: E402
import services.CardService as cs            # noqa: E402
from enums.GameEnum import EGameStatus        # noqa: E402
from enums.GwentEnum import CardType, Location, Rarity  # noqa: E402

global_var._init()

CARD_JSON = json.load(open("main/resources/config/card_json_local.json", encoding="utf-8"))
DECKS = json.loads(open("main/resources/data/decks.json", "rb").read().decode("utf-16"))

PREVIEW_DIR = "main/resources/images/GwentImg_preview"


def _has_preview(cid):
    return os.path.exists(os.path.join(PREVIEW_DIR, "{0}.jpg".format(cid)))


def pick_deck():
    """挑一副「所有卡都有预览图」的整套卡组，保证界面能完整渲染。"""
    for deck in DECKS:
        ids = [deck["leaderCtId"], deck["stratagemCtId"]] + list(deck["sortedCtIds"])
        ids = [i for i in ids if i]
        if len(ids) < 20:
            continue
        if all(_has_preview(i) for i in ids):
            return deck
    raise SystemExit("没有找到素材完整的卡组")


def build_card_templates(deck):
    """把一副卡组摊平成 dao.initCtData() 的等价结构（内存里那套字段）。"""
    cards = []
    ins_id = 1000

    def add(cid, ctype, location, power=0, provision=0, rarity=1):
        nonlocal ins_id
        info = CARD_JSON.get(str(cid), {})
        cards.append({
            "Id": cid,
            "FactionId": int(info.get("factionId", deck.get("factionId") or 1)),
            "Rarity": int(info.get("rarity", rarity)) or rarity,
            "Provision": int(info.get("provision", provision)) or provision,
            "Type": ctype,
            "PlayId": 1,                 # 我方玩家 id
            "Location": location,
            "Index": ins_id,
            "Address": 0x1000 + ins_id,
            "CardId": ins_id,
            "FromPlayerId": 1,
            "BasePower": int(info.get("power", power) or power),
            "CurrPower": int(info.get("power", power) or power),
        })
        ins_id += 1

    # 领袖 / 战略卡本来就在导出的牌表里（官网 API 的 sortedCtIds 含领袖），
    # 不再额外插一条，否则界面上会重复出现两行领袖。
    # 牌库页按人口降序，领袖（人口 15）自然排在最前，看起来就是标题行。

    # 牌库 N 张（留 2 张在手牌、1 张在墓地，方便切换页签时也有内容）
    ids = list(deck["sortedCtIds"])
    for i, cid in enumerate(ids):
        info = CARD_JSON.get(str(cid), {})
        ctype = int(info.get("cardType", CardType.UNIT.value)) or CardType.UNIT.value
        if i >= len(ids) - 3:
            loc = Location.HAND.value if i < len(ids) - 1 else Location.GRAVEYARD.value
        else:
            loc = Location.DECK.value
        add(cid, ctype, loc)
    return cards


def install_data_source(deck):
    """把 CardService 里「读内存」的几个入口换成替身。"""
    templates = build_card_templates(deck)
    ins_ids = [c["CardId"] for c in templates]

    # 先跑一次原始 main()：它会加载卡牌表/领袖表/卡组表到 global_var
    # （pymem 已被替换成假实现，所以这里不会真的去读游戏进程）
    try:
        cs.main()
    except Exception as exc:      # noqa: BLE001
        print("[warn] cs.main() 失败，手工注入卡牌表:", exc)
        global_var.set_value("AllCardDict", CARD_JSON)
        global_var.set_value("LeaderCardDict", {})
        global_var.set_value("decks", {})

    cs.get_all_cardTemplates = lambda: templates

    class _BattleInfo:
        currPlayerId = 1
        bottomPlayerId = 1
        topPlayerId = 2
        localPlayerId = 1

    cs.getCurrBattleInfo = lambda: _BattleInfo()
    cs.getViewingCards = lambda: {}
    cs.getPlayerEnableActionsStatus = lambda pid: 0
    cs.getPlayerCarriedCarInsIds = lambda pid: ins_ids
    cs.getGameStatus = lambda: EGameStatus.RUNNING
    cs.isExistGameInstance = lambda: True
    cs.getDeckInfo = lambda pid: {"totalCardNums": len(templates), "isDefensive": False, "leaderIndex": 0}
    cs.refreshGI = lambda: None
    return templates


# --------------------------------------------------------------------------
# 2) 截图辅助
# --------------------------------------------------------------------------
def grab(bbox, out_path):
    from PIL import ImageGrab
    img = ImageGrab.grab(bbox=bbox, all_screens=True)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path)
    print("[shot] {0}  {1}".format(out_path, img.size))
    return img


def make_backdrop(width, height, color="#0d1117", title=""):
    """给悬浮窗垫一层深色底，模拟游戏画面（悬浮窗本身是透明置顶的）。"""
    import tkinter as tk
    from PIL import Image, ImageDraw, ImageTk

    win = tk.Toplevel()
    win.overrideredirect(True)
    win.geometry("{0}x{1}+0+0".format(width, height))
    win.configure(bg=color)

    img = Image.new("RGB", (width, height), color)
    draw = ImageDraw.Draw(img)
    # 一点点渐变，别让背景死黑
    for y in range(height):
        k = y / max(height - 1, 1)
        draw.line([(0, y), (width, y)], fill=(int(13 + 14 * k), int(17 + 16 * k), int(23 + 20 * k)))
    photo = ImageTk.PhotoImage(img)
    lbl = tk.Label(win, image=photo, bd=0, highlightthickness=0)
    lbl.image = photo
    lbl.pack(fill="both", expand=True)
    win.lower()
    return win


# --------------------------------------------------------------------------
# 3) 两种界面
# --------------------------------------------------------------------------
def render_overlay(out_path, size=(338, 1000), is_enemy=False, tab=None):
    import tkinter as tk
    from ttkbootstrap import Style
    from GwentGUI import GwentGUI

    deck = pick_deck()
    install_data_source(deck)

    root = tk.Tk()
    Style(theme="darkly")
    root.title("Gwent Card View")
    global_var.set_value("panel_root", root)

    backdrop = make_backdrop(size[0] + 40, size[1] + 40)

    gui = GwentGUI(root, size, isEnemy=is_enemy)
    root.update_idletasks()
    root.update()

    # 等待渲染稳定（updateData 是 400ms 轮询，卡牌入场动画 2.5s）
    deadline = time.time() + 2.6
    while time.time() < deadline:
        root.update()
        time.sleep(0.05)

    if tab:
        ok = _switch_tab(root, tab)
        print("[tab] {0} -> {1}".format(tab, ok))
        t2 = time.time() + 2.0
        while time.time() < t2:
            root.update()
            time.sleep(0.05)

    root.update()
    time.sleep(0.3)
    img = grab((0, 0, size[0], size[1]), out_path)
    img = _crop_to_full_row(root, img, out_path)
    try:
        root.destroy()
    except Exception:      # noqa: BLE001
        pass
    try:
        backdrop.destroy()
    except Exception:      # noqa: BLE001
        pass


def _crop_to_full_row(root, img, out_path):
    """把截图裁到最后一张「完整显示」的卡牌下方，避免出现半截卡。"""
    try:
        canvas = root.card_list_board.can_bg
        row = float(root.card_list_board.canvas_row_padding)
        boxes = [canvas.bbox(i) for i in canvas.find_withtag("UICard")]
        boxes = [b for b in boxes if b]
        if not boxes or row <= 1:
            return img
        top = min(b[1] for b in boxes)
        rows = int((img.size[1] - top) // row)
        bottom = int(top + rows * row) + 2
        if 200 < bottom < img.size[1]:
            from PIL import Image
            img = img.crop((0, 0, img.size[0], bottom))
            img.save(out_path)
            print("[shot] 裁剪到 {0}（{1} 行 × {2:.1f}px）".format(img.size, rows, row))
    except Exception as exc:                      # noqa: BLE001
        print("[warn] 裁剪失败:", exc)
    return img


def _switch_tab(root, button_name):
    """切换悬浮窗顶部的模块页签（卡组 / 牌库 / 墓场 / 手牌 …）。"""
    rm = root.responseManager
    for cdi in rm.CARD_DECK_INFO:
        if cdi.buttonName == button_name:
            rm.cardList.resetType(cdi)
            rm.title.updateText(cdi)
            rm.cardList.updateData()
            return True
    return False


def render_main(out_path, size=(250, 280)):
    import tkinter as tk
    from ttkbootstrap import Style
    import GwentMirror as GM

    deck = pick_deck()
    install_data_source(deck)

    # 主窗里的 PanelManager 会检测 Gwent.exe，这里换成空壳
    class _DummyPanelManager:
        def __init__(self, root):
            self.root = root

        def openOurPanel(self, *a, **k):
            pass

        def closeOurPanel(self, *a, **k):
            pass

        def openOpponentPanel(self, *a, **k):
            pass

        def closeOpponentPanel(self, *a, **k):
            pass

    GM.PM = types.SimpleNamespace(PanelManager=_DummyPanelManager)

    root = tk.Tk()
    Style(theme="darkly")
    root.title("Gwent Mirror")
    x = 200
    y = 120
    root.geometry("{0}x{1}+{2}+{3}".format(size[0], size[1], x, y))
    root.resizable(0, 0)
    global_var.set_value("panel_root", root)
    # GwentMirror.py 里的若干回调直接引用模块级 root（正常流程由 __main__ 赋值）
    GM.root = root

    GM.create_page(root)
    root.update_idletasks()
    root.lift()
    root.attributes("-topmost", True)
    root.focus_force()

    end = time.time() + 1.0
    while time.time() < end:
        root.update()
        time.sleep(0.05)

    # 宽度保持原样（250），高度取「当前页签实际用到的最大 Y」，
    # 避免把其它页签（日志页很高）的空白也算进来。
    w = size[0]
    root.update_idletasks()
    origin_y = root.winfo_rooty()
    bottom = 0
    stack = [root]
    while stack:
        widget = stack.pop()
        for child in widget.winfo_children():
            if not child.winfo_ismapped():
                continue
            bottom = max(bottom, child.winfo_rooty() - origin_y + child.winfo_height())
            stack.append(child)
    h = max(size[1], bottom + 12)
    root.geometry("{0}x{1}+{2}+{3}".format(w, h, x, y))
    root.update_idletasks()

    end = time.time() + 1.2
    while time.time() < end:
        root.update()
        time.sleep(0.05)

    root.update_idletasks()
    rx, ry = root.winfo_rootx(), root.winfo_rooty()      # 客户区左上角（屏幕坐标）
    # 连标题栏/边框一起截进来
    grab((rx - 8, ry - 34, rx + w + 8, ry + h + 8), out_path)
    root.destroy()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default="both", choices=["overlay", "main", "both"])
    ap.add_argument("--out-dir", default=os.path.join(HERE, "..", "docs", "screenshots"))
    ap.add_argument("--enemy", action="store_true", help="渲染敌方视角的记牌窗")
    ap.add_argument("--tab", default=None, help="渲染指定页签：卡组/牌库/墓场/放逐/手牌/场地")
    ap.add_argument("--out", default=None, help="覆写输出文件名")
    args = ap.parse_args()

    out_dir = os.path.abspath(args.out_dir)
    os.makedirs(out_dir, exist_ok=True)

    if args.target in ("overlay", "both"):
        name = args.out or ("06-desktop-overlay.png" if not args.enemy else "07-desktop-overlay-enemy.png")
        render_overlay(os.path.join(out_dir, name), is_enemy=args.enemy, tab=args.tab)

    if args.target in ("main", "both"):
        name = args.out or "05-desktop-main.png"
        render_main(os.path.join(out_dir, name))


if __name__ == "__main__":
    main()

