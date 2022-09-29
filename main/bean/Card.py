class Card(object):

    __slots__ = ['instanceId', 'templateId', 'name','factionId','rarity','provision','cardType','playerId','location','index','address','basePower','currPower']
    def __init__(self,instanceId,templateId,name,factionId,rarity,provision,cardType,playerId,location,index,address,basePower,currPower):
        self.instanceId = instanceId
        self.templateId = templateId
        self.name = name
        self.factionId = factionId
        self.rarity = rarity
        self.provision = provision
        self.cardType = cardType
        self.playerId = playerId
        self.location = location
        self.index = index
        self.address = address
        self.basePower = basePower
        self.currPower = currPower
    
    # def reset(self,instanceId,templateId,name,factionId,rarity,provision,cardType,playerId,location,index,address,basePower,currPower):
    #     self.instanceId = instanceId
    #     self.templateId = templateId
    #     self.name = name
    #     self.factionId = factionId
    #     self.rarity = rarity
    #     self.cardType = cardType
    #     self.playerId = playerId
    #     self.location = location
    #     self.basePower = basePower
    #     self.currPower = currPower
    #     self.provision = provision
    #     self.index = index
    #     self.address = address
    