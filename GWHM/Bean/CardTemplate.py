class CardTemplate(object):

    def __init__(self):
            self._id = 0x10
            self._debugName = 0x18
            self._availability = 0x20
            self._rarity = 0x21 
            self._artId = 0x24
            self._audioId = 0x28
            self._abilityIds = 0x30
            self._linkedTemplateId = 0x38
            self._linkedTemplateOrder = 0x3c
            self._factionId = 0x40
            self._secondaryFactionId = 0x44
            self._tier = 0x48
            self._type = 0x49
            self._tokens = 0x4c
            self._maxRange = 0x50
            self._power = 0x54
            self._armor = 0x58
            self._provision = 0x5c
            self._initialTimer = 0x60
            self._overrideTimerIcon = 0x65
            self._initialTapCharges = 0x68
            self._tapActive = 0x6c
            self._summoningSickness = 0x6d
            self._visibleTapCharges = 0x6e
            self._madness = 0x6f
            self._placement = 0x70
            self._primaryCategory = 0x78
            self._categories = 0x80
            self._semanticTags = 0x88
            self._initialCardPosition = 0x90
            self._energy = 0x94
            self._card = 0x95
            # self._baseAddress = 0x99
    

    @property
    def id(self):
        return self._id
    @id.setter
    def set(self, id):
        self._id = id

    @property
    def debugName(self):
        return self._debugName
    @debugName.setter
    def set(self, debugName):
        self._debugName = debugName

    @property
    def availability(self):
        return self._availability
    @availability.setter
    def set(self, availability):
        self._availability = availability
    
    @property
    def rarity(self):
        return self._rarity
    @rarity.setter
    def set(self, rarity):
        self._rarity = rarity
    
    @property
    def artId(self):
        return self._rarity
    @rarity.setter
    def set(self, rarity):
        self._rarity = rarity
    
    @property
    def audioId(self):
        return self._audioId
    @audioId.setter
    def set(self, audioId):
        self._audioId = audioId
            
    @property
    def abilityIds(self):
        return self._abilityIds
    @abilityIds.setter
    def set(self, abilityIds):
        self._abilityIds = abilityIds
        
    @property
    def linkedTemplateId(self):
        return self._linkedTemplateId
    @linkedTemplateId.setter
    def set(self, linkedTemplateId):
        self._linkedTemplateId = linkedTemplateId
    
    @property
    def linkedTemplateOrder(self):
        return self._linkedTemplateOrder
    @linkedTemplateOrder.setter
    def set(self, linkedTemplateOrder):
        self._linkedTemplateOrder = linkedTemplateOrder

    @property
    def factionId(self):
        return self._factionId
    @factionId.setter
    def set(self, factionId):
        self._factionId = factionId

    @property
    def secondaryFactionId(self):
        return self._secondaryFactionId
    @secondaryFactionId.setter
    def set(self, secondaryFactionId):
        self._secondaryFactionId = secondaryFactionId

    @property
    def tier(self):
        return self._tier
    @tier.setter
    def set(self, tier):
        self._tier = tier
    
    @property
    def type(self):
        return self._type
    @type.setter
    def set(self, type):
        self._type = type
    
    @property
    def tokens(self):
        return self._tokens
    @tokens.setter
    def set(self, tokens):
        self._tokens = tokens
    
    @property
    def maxRange(self):
        return self._maxRange
    @maxRange.setter
    def set(self, maxRange):
        self._maxRange = maxRange
    
    @property
    def power(self):
        return self._power
    @power.setter
    def set(self, power):
        self._power = power
    
    @property
    def armor(self):
        return self._armor
    @armor.setter
    def set(self, armor):
        self._armor = armor
    
    @property
    def provision(self):
        return self._provision
    @provision.setter
    def set(self, provision):
        self._provision = provision
    
    @property
    def initialTimer(self):
        return self._initialTimer
    @initialTimer.setter
    def set(self, initialTimer):
        self._initialTimer = initialTimer
    
    @property
    def resetInInactive(self):
        return self._resetInInactive
    @resetInInactive.setter
    def set(self, resetInInactive):
        self._resetInInactive = resetInInactive
    
    @property
    def overrideTimerIcon(self):
        return self._overrideTimerIcon
    @overrideTimerIcon.setter
    def set(self, overrideTimerIcon):
        self._overrideTimerIcon = overrideTimerIcon
    
    @property
    def initialTapCharges(self):
        return self._initialTapCharges
    @initialTapCharges.setter
    def set(self, initialTapCharges):
        self._initialTapCharges = initialTapCharges
    
    @property
    def tapActive(self):
        return self._tapActive
    @tapActive.setter
    def set(self, tapActive):
        self._tapActive = tapActive
    
    @property
    def summoningSickness(self):
        return self._summoningSickness
    @summoningSickness.setter
    def set(self, summoningSickness):
        self._summoningSickness = summoningSickness
    
    @property
    def visibleTapCharges(self):
        return self._visibleTapCharges
    @visibleTapCharges.setter
    def set(self, visibleTapCharges):
        self._visibleTapCharges = visibleTapCharges
    
    @property
    def madness(self):
        return self._madness
    @madness.setter
    def set(self, madness):
        self._madness = madness
    
    @property
    def placement(self):
        return self._placement
    @placement.setter
    def set(self, placement):
        self._placement = placement
    
    @property
    def primaryCategory(self):
        return self._primaryCategory
    @primaryCategory.setter
    def set(self, primaryCategory):
        self._primaryCategory = primaryCategory
    
    @property
    def categories(self):
        return self._categories
    @categories.setter
    def set(self, categories):
        self._categories = categories
    
    @property
    def semanticTags(self):
        return self._semanticTags
    @semanticTags.setter
    def set(self, semanticTags):
        self._semanticTags = semanticTags
    
    @property
    def initialCardPosition(self):
        return self._initialCardPosition
    @initialCardPosition.setter
    def set(self, initialCardPosition):
        self._initialCardPosition = initialCardPosition
    
    @property
    def energy(self):
        return self._energy
    @energy.setter
    def set(self, energy):
        self._energy = energy
    
    @property
    def card(self):
        return self._card
    @card.setter
    def set(self, card):
        self._card = card

    def toString(self):
        print("id:",self._id,"\n","debugName:",self._debugName,'\n',"availability:",self._availability,'\n',"rarity:",self._rarity,'\n',"artId:",self._artId,'\n',"audioId:",self._audioId,'\n',"abilityIds:",self._abilityIds,'\n'
        ,"linkedTemplateId:",self._linkedTemplateId,'\n',"linkedTemplateOrder:",self._linkedTemplateOrder,'\n',"secondaryFactionId:",self._secondaryFactionId,'\n',"tier:",self._tier,'\n',"type:",self._type,'\n',"tokens:",self._tokens,'\n'
        ,"maxRange:",self._maxRange,'\n',"power:",self._power,'\n',"armor:",self._armor,'\n',"provision:",self._provision,'\n',"initialTimer:",self._initialTimer,'\n',"overrideTimerIcon:",self._overrideTimerIcon,'\n',"initialTapCharges:",self._initialTapCharges,'\n'
        ,"tapActive:",self._tapActive,'\n',"summoningSickness:",self._summoningSickness,'\n',"visibleTapCharges:",self._visibleTapCharges,'\n',"madness:",self._madness,'\n',"placement:",self._placement,'\n',"primaryCategory:",self._primaryCategory,'\n'
        ,"categories:",self._categories,'\n',"semanticTags:",self._semanticTags,'\n',"initialCardPosition:",self._initialCardPosition,'\n',self.energy,'\n')