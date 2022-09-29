import pymem
import MainGUI as mainGui

# 偏移寻址
# offsets为空时，会把base视为指针并进入一次
def read_int64(pm, base, offsets):
    try :
        value = pm.read_longlong(base)
        for offset in offsets:
            value = pm.read_longlong(value + offset)
        return value
    except :
        print("reset")
        mainGui.restart_program()

# 没有偏移,如果传入则不会进入指针
def read_memory_bytes(pm,base,count):
    try :
        value = pm.read_bytes(base,count)
        result=""
        for item in value:
            result = str(hex(item))[2:].zfill(2).upper() +result
        return int(result,16)
    except :
        print("reset")
        mainGui.restart_program()

def read_multi_bytes(pm, base, offsets,count):
    try :
        value = pm.read_longlong(base)
        for offset in offsets:
            if offsets.index(offset) == len(offsets)-1:
                value = pm.read_bytes(value + offset,count)
                result=""
                for item in value:
                    result = str(hex(item))[2:].zfill(2).upper() +result
                return int(result,16)
            value = pm.read_longlong(value + offset)
        # return value
    except :
        print("reset")
        mainGui.restart_program()

# 获取到对象的类型名
# address 需要转换的对象,ascii的上一级指针地址
# return 函数类型
def read_Type_Name(pm,address):
    asciiHeadAdd = read_int64(pm,address+0x10,[])
    print(hex(asciiHeadAdd))
    result_name = ""
    count = 0
    while True:
        temp_add = read_memory_bytes(pm,asciiHeadAdd+count,0x1)
        if temp_add == 0:
            return result_name
        result_name+=chr(temp_add)
        count += 1
        if count >= 99:
            print("Read_Type_Name函数超过{}次,请检查地址是否合法!本次操作已经正长返回".format(count))
            return result_name

