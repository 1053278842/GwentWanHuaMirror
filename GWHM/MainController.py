from email.charset import add_charset
from email.utils import getaddresses
from pickle import GLOBAL
import pymem
from Banner import *
from time import sleep
import threading
from FileTool import *
from CardDao import *
from CardService import *


def main():
    banner()
    try:
        get_baseAddress()
    except Exception:
        print("启动失败，请检查启动游戏是否启动!")
        return 0
    # -----------------测试用行----------------- 
   
    # CardDataFileToJson()
    # Cpp2liTransBean(r"C:\Users\Administrator\Desktop\cpp2il_out\types\Assembly-CSharp\Card_metadata.txt","Card","Card")
    # return 0

    thread_getGameInstanceAdd = threading.Thread(target=SearchingGameInstance)
    thread_getGameInstanceAdd.start()
    thread_getGameInstanceAdd.join()
    print("Get GameInstance Success! Address is:",hex(GI))
    return 1
    # -----------------测试用行-----------------
    
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



