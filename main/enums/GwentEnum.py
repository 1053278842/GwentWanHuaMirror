from enum import Enum


# 卡牌位置类型
class Location(Enum):
    INVALID  = 0                # 无效          0x0
    MELEE  = 1                  # 混乱          0x1
    RANGED   = 2                # 场上          0x2
    EVENT_EXECUTING = 4         # 事件中        0x4
    HAND    = 8                 # 手牌          0x8
    DECK    = 16                # 卡组          0x10
    GRAVEYARD     = 32          # 墓地          0x20
    LEADER        = 64          # 领队          0x40
    SPAWNING_POOL = 128         # 孵化          0x80
    PAY_STACK      = 256        # 待打出        0x100
    VOID          = 512         # 放逐          0x200
    MULLIGAN_STACK = 1024       # 调度替换栈    0x400

# 卡片提示动画类型
class TipsType(Enum):
    ADD     = 0 
    REMOVE  = 2 
    MOVE    = 4 
    WHITE   = 8  

# 卡牌稀有度
class Rarity(Enum):
    ALL         = 0     # 全部
    COMMON      = 1     # 普通
    RARE        = 2     # 稀有
    EPIC        = 4     # 史诗
    LEGENDARY   = 8     # 传说

# 卡牌种类
class CardType(Enum):
    ALL         = 0     # 全部
    LEADER      = 1     # 领袖卡    0x 01
    SPECIAL     = 2     # 特殊卡    0x 02
    UNIT        = 4     # 单位卡    0x 04
    ARTIFACT    = 8     # 神器卡    0x 08
    STRATAGEM   = 16    # 战略卡    0x 10

class Faction(Enum):
    NEUTRAL = 1
    MONSTER = 2
    NILFGAARD = 4
    NORTHERN_REALMS = 8
    SCOIATAEL = 16
    SKELLIGE = 32
    SVNDICATE = 64

