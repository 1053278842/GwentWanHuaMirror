from enum import Enum


# 卡牌位置类型
class ChoiceType(Enum):
    CHOOSE_CARD                 = 0 # 选择              
    CARD_TO_PLAY                = 1                  
    CARD_TO_MOVE                = 2             
    CARD_TO_DISCARD             = 3         
    CARD_TO_PUT_BACK_IN_DECK    = 4 # 洗回卡组       
    CARD_TO_DRAW                = 5 # 进入手牌        
    CARD_TO_SPAWN               = 6         
    CARD_TO_COPY                = 7         
    CARD_TO_REVEAL              = 8 # reveal:揭示        

class ActionName(Enum):
    REQUEST_MULLIGAN_ACTION = "RequestMulliganAction"
    REQUEST_CARD_CHOICES_ACTION = "RequestCardChoicesAction"    # 卡牌选择时触发