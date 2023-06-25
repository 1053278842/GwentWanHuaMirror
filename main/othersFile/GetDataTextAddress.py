import os
import sys
import threading
import time

os.path.join(os.path.dirname(__file__), '../')
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
import pymem
from tools.MemoryTool import *


# 本脚本用于获取游戏的GameInstance组件的偏移地址
# ps:前置条件-游戏在battle界面
# 1c8是中文偏移
def getGameInstanceValue(pm,base,add):
    gameInstanceAdd = read_int64(pm,base+add,[0x30,0xf0,0x0])
    return gameInstanceAdd

class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

def search_range(start_add, end_add, pm, base_address, check_name, result_lock, result_list, stop_event):
    for i in range(start_add, end_add):
        if stop_event.is_set():
            return
        try:
            gi_value = getGameInstanceValue(pm, base_address, i)
            type_name = read_Type_Name(pm, gi_value)
            print(pm,type_name)
        except Exception:
            continue
        if type_name == check_name:
            with result_lock:
                result_list.append(i)
            stop_event.set()
            return


if __name__=='__main__':
    pm = pymem.Pymem("Gwent.exe")
    base_address = pymem.process.module_from_name(
        pm.process_handle,"GameAssembly.dll"
    ).lpBaseOfDll

    # 62974112
    start_add = 62974112
    end_add = start_add+5000000
    check_name = 'String'

    num_threads = 12  # 设置线程数
    sub_ranges = [(i, i + (end_add - start_add) // num_threads) for i in range(start_add, end_add, (end_add - start_add) // num_threads)]
    sub_ranges[-1] = (sub_ranges[-1][0], end_add)  # 确保最后一个子范围包含剩余的所有地址
    
    result_list = []
    result_lock = threading.Lock()
    stop_event = threading.Event()

    start_time = time.time()
    print("搜索中，请耐心等待......")
    threads = []
    for sub_range in sub_ranges:
        t = StoppableThread(target=search_range, args=(sub_range[0], sub_range[1], pm, base_address, check_name, result_lock, result_list, stop_event))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    if result_list:
        print("搜索完成，寻找到指针：",result_list[0]," (",check_name,")")
    else:
        print("抱歉,未找到适合地址,请尝试扩大范围(start_add,end_add)!")
    end_time = time.time()
    print("搜索用时：", end_time - start_time, "秒")


