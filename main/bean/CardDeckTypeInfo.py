
from enums.GwentEnum import CardType, Rarity


class CardDeckTypeInfo():
    def __init__(self,titleName,location,playerId = 1,isSortByIndex=True,isActive = False,isMain = False,buttonName = "NONE",secLocation = None,isEnemy=False) -> None:
        self.titleName = titleName
        self.location = location
        self.isActive = isActive
        self.playerId = playerId
        self.isSortByIndex = isSortByIndex
        self.isMain = isMain    # 是不是卡表
        self.anim_type = None   # 不同类型的动画有一定区别
        self.isDefensive = None # 先手
        self.buttonName = buttonName

        # 敌我
        self.isEnemy = isEnemy

        # filter
        self.rarity = Rarity.ALL
        self.cardType = CardType.ALL
        
        if secLocation == None:
            self.secLocation = location
        else:
            self.secLocation = secLocation
        
    def toString(self):
        print(self.titleName,self.location,self.isActive,self.playerId,self.isSortByIndex,self.isMain,self.isDefensive,self.isEnemy)