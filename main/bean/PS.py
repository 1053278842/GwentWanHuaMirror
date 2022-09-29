class Ps(object):

	def __init__(self):		self._LeaderEnabled = 0x10
		self._StartingCrowns = 0x14
		self._ShuffleDeck = 0x18
		self._DisableActions = 0x1C
		self._InitialDraw = 0x20
		self._Mulligan = 0x28
		self._Info = 0x30
		self._Deck = 0x38
		self._BasePowerBonus = 0x40
		self._Power = 0x44
		self._Armor = 0x48
		self._StartingMoney = 0x4C
		self._MoneyLimit = 0x50
		self._ShouldHalveAtRoundEnd = 0x54
		self._AllowIdling = 0x55

	@property
	def LeaderEnabled(self):
		return self._LeaderEnabled
	@LeaderEnabled.setter
	def set(self,LeaderEnabled):
		self._LeaderEnabled=LeaderEnabled

	@property
	def StartingCrowns(self):
		return self._StartingCrowns
	@StartingCrowns.setter
	def set(self,StartingCrowns):
		self._StartingCrowns=StartingCrowns

	@property
	def ShuffleDeck(self):
		return self._ShuffleDeck
	@ShuffleDeck.setter
	def set(self,ShuffleDeck):
		self._ShuffleDeck=ShuffleDeck

	@property
	def DisableActions(self):
		return self._DisableActions
	@DisableActions.setter
	def set(self,DisableActions):
		self._DisableActions=DisableActions

	@property
	def InitialDraw(self):
		return self._InitialDraw
	@InitialDraw.setter
	def set(self,InitialDraw):
		self._InitialDraw=InitialDraw

	@property
	def Mulligan(self):
		return self._Mulligan
	@Mulligan.setter
	def set(self,Mulligan):
		self._Mulligan=Mulligan

	@property
	def Info(self):
		return self._Info
	@Info.setter
	def set(self,Info):
		self._Info=Info

	@property
	def Deck(self):
		return self._Deck
	@Deck.setter
	def set(self,Deck):
		self._Deck=Deck

	@property
	def BasePowerBonus(self):
		return self._BasePowerBonus
	@BasePowerBonus.setter
	def set(self,BasePowerBonus):
		self._BasePowerBonus=BasePowerBonus

	@property
	def Power(self):
		return self._Power
	@Power.setter
	def set(self,Power):
		self._Power=Power

	@property
	def Armor(self):
		return self._Armor
	@Armor.setter
	def set(self,Armor):
		self._Armor=Armor

	@property
	def StartingMoney(self):
		return self._StartingMoney
	@StartingMoney.setter
	def set(self,StartingMoney):
		self._StartingMoney=StartingMoney

	@property
	def MoneyLimit(self):
		return self._MoneyLimit
	@MoneyLimit.setter
	def set(self,MoneyLimit):
		self._MoneyLimit=MoneyLimit

	@property
	def ShouldHalveAtRoundEnd(self):
		return self._ShouldHalveAtRoundEnd
	@ShouldHalveAtRoundEnd.setter
	def set(self,ShouldHalveAtRoundEnd):
		self._ShouldHalveAtRoundEnd=ShouldHalveAtRoundEnd

	@property
	def AllowIdling(self):
		return self._AllowIdling
	@AllowIdling.setter
	def set(self,AllowIdling):
		self._AllowIdling=AllowIdling

	def toString(self):
		print("LeaderEnabled:",hex(self._LeaderEnabled),"\n","LeaderEnabled:",hex(self._LeaderEnabled),"\n","StartingCrowns:",hex(self._StartingCrowns),"\n","ShuffleDeck:",hex(self._ShuffleDeck),"\n","DisableActions:",hex(self._DisableActions),"\n","InitialDraw:",hex(self._InitialDraw),"\n","Mulligan:",hex(self._Mulligan),"\n","Info:",hex(self._Info),"\n","Deck:",hex(self._Deck),"\n","BasePowerBonus:",hex(self._BasePowerBonus),"\n","Power:",hex(self._Power),"\n","Armor:",hex(self._Armor),"\n","StartingMoney:",hex(self._StartingMoney),"\n","MoneyLimit:",hex(self._MoneyLimit),"\n","ShouldHalveAtRoundEnd:",hex(self._ShouldHalveAtRoundEnd),"\n","AllowIdling:",hex(self._AllowIdling),"\n")