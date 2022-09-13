import json
import pymem
# 偏移寻址
def read_int64(pm, base, offsets):
    value = pm.read_longlong(base)
    for offset in offsets:
        value = pm.read_longlong(value + offset)
    return value

def read_memory_bytes(pm,base,count):
    value = pm.read_bytes(base,count)
    result=""
    for item in value:
        result = str(hex(item))[2:].zfill(2).upper() +result
    return int(result,16)



