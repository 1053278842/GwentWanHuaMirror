from email.charset import add_charset
from email.utils import getaddresses
from pickle import GLOBAL
import pymem
from others.Banner import *
from tools.FileTool import *
from dao.CardDao import *
from services.CardService import *
from time import sleep


def main():
    try:
        get_baseAddress()
    except Exception:
        print("启动失败，请检查启动游戏是否启动!")
        return 0
    # -----------------测试用行----------------- 
    SearchingGameInstance()
    banner()
    print("Get GameInstance Success! Address is:",hex(GI))
    return 1
    # -----------------测试用行-----------------

def SearchingGameInstance():
    global GI
    print("正在等待玩家进入游戏,检测GameInstance中...")
    cardDao = CardDao(pm,baseAddress)
    while True:
        try:
            gameInstanceAdd = cardDao.getGameInstance()
            obj_type_name = cardDao.getAddTypeName(gameInstanceAdd,2)
            # AddressToString(gameInstanceAdd)
        except Exception:
            print("[线程]获取GameInstance地址发生错误,重试中...")
            sleep(2)
            continue
        
        if("GameInstance" in obj_type_name):
            GI = gameInstanceAdd
            break
        sleep(2)


# 根据地址打印其基本信息
def AddressToString(address,nameLen=2):
    print("地址:",hex(address)," 指向对象类型:",cardDao.getAddTypeName(address,nameLen))


# 获取程式模块基址
def get_baseAddress():
    global pm
    global baseAddress
    pm = pymem.Pymem("Gwent.exe")
    baseAddress = pymem.process.module_from_name(
        pm.process_handle,"GameAssembly.dll"
    ).lpBaseOfDll


if __name__ == "__main__":
    main()



