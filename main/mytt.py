import pymem
import services.CardService
from dao.CardDao import *
from tools.FileTool import *



if __name__ == "__main__":
    global pm
    global baseAddress
    pm = pymem.Pymem("Gwent.exe")
    baseAddress = pymem.process.module_from_name(
        pm.process_handle,"GameAssembly.dll"
    ).lpBaseOfDll
  
    print("ga:",hex(baseAddress))
    app = read_int64(pm,baseAddress+0x36f7260,[])
    
    print("gc:",hex(app))

    
