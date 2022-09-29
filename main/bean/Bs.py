class Bs(object):

	def __init__(self):
		self._StartingPlayer = 0x10
		self._ShowIntro = 0x11
		self._BattleAbilities = 0x18
		self._P2 = 0x20
		self._P1 = 0x28
		self._TopSide = 0x30
		self._BottomSide = 0x38
		self._AllowInspectDeck = 0x40
		self._ShowDeckInOrder = 0x41
		self._SpawnTacticalAdvantage = 0x42
		self._GameID = 0x48
		self._VisualSeed = 0x50
		self._LogicSeed = 0x57
		self._BattleType = 0x58
		self._EnableTimers = 0x59
		self._Timers = 0x60
		self._EnableTimeout = 0x68
		self._ForceTimersOnSinglePlayer = 0x69
		self._CombatDifficulty = 0x6C
		self._IsRunningBattleFlowchart = 0x70
		self._SkipBattleResults = 0x71

	@property
	def StartingPlayer(self):
		return self._StartingPlayer
	@StartingPlayer.setter
	def set(self,StartingPlayer):
		self._StartingPlayer=StartingPlayer

	@property
	def ShowIntro(self):
		return self._ShowIntro
	@ShowIntro.setter
	def set(self,ShowIntro):
		self._ShowIntro=ShowIntro

	@property
	def BattleAbilities(self):
		return self._BattleAbilities
	@BattleAbilities.setter
	def set(self,BattleAbilities):
		self._BattleAbilities=BattleAbilities

	@property
	def P2(self):
		return self._P2
	@P2.setter
	def set(self,P2):
		self._P2=P2

	@property
	def P1(self):
		return self._P1
	@P1.setter
	def set(self,P1):
		self._P1=P1

	@property
	def TopSide(self):
		return self._TopSide
	@TopSide.setter
	def set(self,TopSide):
		self._TopSide=TopSide

	@property
	def BottomSide(self):
		return self._BottomSide
	@BottomSide.setter
	def set(self,BottomSide):
		self._BottomSide=BottomSide

	@property
	def AllowInspectDeck(self):
		return self._AllowInspectDeck
	@AllowInspectDeck.setter
	def set(self,AllowInspectDeck):
		self._AllowInspectDeck=AllowInspectDeck

	@property
	def ShowDeckInOrder(self):
		return self._ShowDeckInOrder
	@ShowDeckInOrder.setter
	def set(self,ShowDeckInOrder):
		self._ShowDeckInOrder=ShowDeckInOrder

	@property
	def SpawnTacticalAdvantage(self):
		return self._SpawnTacticalAdvantage
	@SpawnTacticalAdvantage.setter
	def set(self,SpawnTacticalAdvantage):
		self._SpawnTacticalAdvantage=SpawnTacticalAdvantage

	@property
	def GameID(self):
		return self._GameID
	@GameID.setter
	def set(self,GameID):
		self._GameID=GameID

	@property
	def VisualSeed(self):
		return self._VisualSeed
	@VisualSeed.setter
	def set(self,VisualSeed):
		self._VisualSeed=VisualSeed

	@property
	def LogicSeed(self):
		return self._LogicSeed
	@LogicSeed.setter
	def set(self,LogicSeed):
		self._LogicSeed=LogicSeed

	@property
	def BattleType(self):
		return self._BattleType
	@BattleType.setter
	def set(self,BattleType):
		self._BattleType=BattleType

	@property
	def EnableTimers(self):
		return self._EnableTimers
	@EnableTimers.setter
	def set(self,EnableTimers):
		self._EnableTimers=EnableTimers

	@property
	def Timers(self):
		return self._Timers
	@Timers.setter
	def set(self,Timers):
		self._Timers=Timers

	@property
	def EnableTimeout(self):
		return self._EnableTimeout
	@EnableTimeout.setter
	def set(self,EnableTimeout):
		self._EnableTimeout=EnableTimeout

	@property
	def ForceTimersOnSinglePlayer(self):
		return self._ForceTimersOnSinglePlayer
	@ForceTimersOnSinglePlayer.setter
	def set(self,ForceTimersOnSinglePlayer):
		self._ForceTimersOnSinglePlayer=ForceTimersOnSinglePlayer

	@property
	def CombatDifficulty(self):
		return self._CombatDifficulty
	@CombatDifficulty.setter
	def set(self,CombatDifficulty):
		self._CombatDifficulty=CombatDifficulty

	@property
	def IsRunningBattleFlowchart(self):
		return self._IsRunningBattleFlowchart
	@IsRunningBattleFlowchart.setter
	def set(self,IsRunningBattleFlowchart):
		self._IsRunningBattleFlowchart=IsRunningBattleFlowchart

	@property
	def SkipBattleResults(self):
		return self._SkipBattleResults
	@SkipBattleResults.setter
	def set(self,SkipBattleResults):
		self._SkipBattleResults=SkipBattleResults

	def toString(self):
		print("StartingPlayer:",hex(self._StartingPlayer),"\n","StartingPlayer:",hex(self._StartingPlayer),"\n","ShowIntro:",hex(self._ShowIntro),"\n"
,"BattleAbilities:",hex(self._BattleAbilities),"\n","P2:",hex(self._P2),"\n"
,"P1:",hex(self._P1),"\n","TopSide:",hex(self._TopSide),"\n"
,"BottomSide:",hex(self._BottomSide),"\n","AllowInspectDeck:",hex(self._AllowInspectDeck),"\n"
,"ShowDeckInOrder:",hex(self._ShowDeckInOrder),"\n","SpawnTacticalAdvantage:",hex(self._SpawnTacticalAdvantage),"\n"
,"GameID:",hex(self._GameID),"\n","VisualSeed:",hex(self._VisualSeed),"\n"
,"LogicSeed:",hex(self._LogicSeed),"\n","BattleType:",hex(self._BattleType),"\n"
,"EnableTimers:",hex(self._EnableTimers),"\n","Timers:",hex(self._Timers),"\n"
,"EnableTimeout:",hex(self._EnableTimeout),"\n","ForceTimersOnSinglePlayer:",hex(self._ForceTimersOnSinglePlayer),"\n"
,"CombatDifficulty:",hex(self._CombatDifficulty),"\n","IsRunningBattleFlowchart:",hex(self._IsRunningBattleFlowchart),"\n"
,"SkipBattleResults:",hex(self._SkipBattleResults),"\n")