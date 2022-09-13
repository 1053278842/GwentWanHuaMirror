from enum import Enum
 
# 继承枚举类
class Location(Enum):
    INVALID  = 0 # 无效
    RANGED   = 2 # 场上
    EVENT_EXECUTING = 4 # 事件中
    HAND    = 8  # 手牌
    DECK    = 16 # 卡组
    GRAVEYARD     = 32  # 墓地
    VOID          = 512 # 放逐
    MULLIGAN_STACK = 1024# 调度替换栈