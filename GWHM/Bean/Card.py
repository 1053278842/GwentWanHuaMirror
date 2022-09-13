class Card(object):

	def __init__(self):
		self._cardManager = 0x10
		self._AbilityData = 0x18
		self._AEntityId = 0x38
		self._CardAbilities = 0x40
		self._Template = 0x48
		self._cardDefinition = 0x50
		self._id = 0x58
		# self._m_Position = 0x5C
		self._position_playerId = 0x5C
		self._position_location = 0x60
		self._position_index = 0x64
		self._EFactionId = 0x68
		self._CardBackVanityId = 0x6C
		self._DeckFactionId = 0x70
		self._IsBeingPlayedBy = 0x74
		self._FromPosition = 0x78
		self._PlayedFrom = 0x84
		self._LastActivePosition = 0x90
		self._Data = 0xA0
		self._m_OnStartedToMove = 0xA8
		self._m_OnMoved = 0xB8
		self._m_OnVisibilityChanged = 0xC8
		self._m_OnPowerChanged = 0xD8
		self._m_OnStatusChanged = 0xE8
		self._m_OnActiveKeywordsChanged = 0xF8
		self._m_OnDefinitionChanged = 0x108
		self._m_OnTimerChanged = 0x118
		self._m_OnOverrideTimerIconChanged = 0x128
		self._m_OnTapChargesChanged = 0x138
		self._m_OnTapStateChanged = 0x148
		self._m_OnTapChargesActiveChanged = 0x158
		self._m_OnSummoningSicknessChanged = 0x168
		self._m_OnRecommendedLocationsChanged = 0x178
		self._m_OnMadnessChanged = 0x188
		self._m_OnPayActiveChanged = 0x198
		self._m_OnPlayedByChanged = 0x1A8
		self._m_OnEnergyChanged = 0x1B8
		self._m_OnBecameVisuallyDirty = 0x1C8
		self._PlayedBy = 0x1D8
		self._IsWaitingToDie = 0x1D9
		self._IsWaitingForBanish = 0x1DA
		self._IsWaitingForDestroy = 0x1DB
		self._DeathType = 0x1DC
		self._ECardVisibility = 0x1DD
		self._cardTemplate = 0x1DF
		self._baseAddress = 0x1FF

	@property
	def cardManager(self):
		return self._cardManager
	@cardManager.setter
	def set(self,cardManager):
		self._cardManager=cardManager

	@property
	def AbilityData(self):
		return self._AbilityData
	@AbilityData.setter
	def set(self,AbilityData):
		self._AbilityData=AbilityData

	@property
	def AEntityId(self):
		return self._AEntityId
	@AEntityId.setter
	def set(self,AEntityId):
		self._AEntityId=AEntityId

	@property
	def CardAbilities(self):
		return self._CardAbilities
	@CardAbilities.setter
	def set(self,CardAbilities):
		self._CardAbilities=CardAbilities

	@property
	def Template(self):
		return self._Template
	@Template.setter
	def set(self,Template):
		self._Template=Template

	@property
	def cardDefinition(self):
		return self._cardDefinition
	@cardDefinition.setter
	def set(self,cardDefinition):
		self._cardDefinition=cardDefinition

	@property
	def id(self):
		return self._id
	@id.setter
	def set(self,id):
		self._id=id

	@property
	def position_playerId(self):
		return self._position_playerId
	@position_playerId.setter
	def set(self,position_playerId):
		self._position_playerId=position_playerId

	@property
	def position_location(self):
		return self._position_location
	@position_location.setter
	def set(self,position_location):
		self._position_location=position_location

	@property
	def position_index(self):
		return self._position_index
	@position_index.setter
	def set(self,position_index):
		self._position_index=position_index

	@property
	def EFactionId(self):
		return self._EFactionId
	@EFactionId.setter
	def set(self,EFactionId):
		self._EFactionId=EFactionId

	@property
	def CardBackVanityId(self):
		return self._CardBackVanityId
	@CardBackVanityId.setter
	def set(self,CardBackVanityId):
		self._CardBackVanityId=CardBackVanityId

	@property
	def DeckFactionId(self):
		return self._DeckFactionId
	@DeckFactionId.setter
	def set(self,DeckFactionId):
		self._DeckFactionId=DeckFactionId

	@property
	def IsBeingPlayedBy(self):
		return self._IsBeingPlayedBy
	@IsBeingPlayedBy.setter
	def set(self,IsBeingPlayedBy):
		self._IsBeingPlayedBy=IsBeingPlayedBy

	@property
	def FromPosition(self):
		return self._FromPosition
	@FromPosition.setter
	def set(self,FromPosition):
		self._FromPosition=FromPosition

	@property
	def PlayedFrom(self):
		return self._PlayedFrom
	@PlayedFrom.setter
	def set(self,PlayedFrom):
		self._PlayedFrom=PlayedFrom

	@property
	def LastActivePosition(self):
		return self._LastActivePosition
	@LastActivePosition.setter
	def set(self,LastActivePosition):
		self._LastActivePosition=LastActivePosition

	@property
	def Data(self):
		return self._Data
	@Data.setter
	def set(self,Data):
		self._Data=Data

	@property
	def m_OnStartedToMove(self):
		return self._m_OnStartedToMove
	@m_OnStartedToMove.setter
	def set(self,m_OnStartedToMove):
		self._m_OnStartedToMove=m_OnStartedToMove

	@property
	def m_OnMoved(self):
		return self._m_OnMoved
	@m_OnMoved.setter
	def set(self,m_OnMoved):
		self._m_OnMoved=m_OnMoved

	@property
	def m_OnVisibilityChanged(self):
		return self._m_OnVisibilityChanged
	@m_OnVisibilityChanged.setter
	def set(self,m_OnVisibilityChanged):
		self._m_OnVisibilityChanged=m_OnVisibilityChanged

	@property
	def m_OnPowerChanged(self):
		return self._m_OnPowerChanged
	@m_OnPowerChanged.setter
	def set(self,m_OnPowerChanged):
		self._m_OnPowerChanged=m_OnPowerChanged

	@property
	def m_OnStatusChanged(self):
		return self._m_OnStatusChanged
	@m_OnStatusChanged.setter
	def set(self,m_OnStatusChanged):
		self._m_OnStatusChanged=m_OnStatusChanged

	@property
	def m_OnActiveKeywordsChanged(self):
		return self._m_OnActiveKeywordsChanged
	@m_OnActiveKeywordsChanged.setter
	def set(self,m_OnActiveKeywordsChanged):
		self._m_OnActiveKeywordsChanged=m_OnActiveKeywordsChanged

	@property
	def m_OnDefinitionChanged(self):
		return self._m_OnDefinitionChanged
	@m_OnDefinitionChanged.setter
	def set(self,m_OnDefinitionChanged):
		self._m_OnDefinitionChanged=m_OnDefinitionChanged

	@property
	def m_OnTimerChanged(self):
		return self._m_OnTimerChanged
	@m_OnTimerChanged.setter
	def set(self,m_OnTimerChanged):
		self._m_OnTimerChanged=m_OnTimerChanged

	@property
	def m_OnOverrideTimerIconChanged(self):
		return self._m_OnOverrideTimerIconChanged
	@m_OnOverrideTimerIconChanged.setter
	def set(self,m_OnOverrideTimerIconChanged):
		self._m_OnOverrideTimerIconChanged=m_OnOverrideTimerIconChanged

	@property
	def m_OnTapChargesChanged(self):
		return self._m_OnTapChargesChanged
	@m_OnTapChargesChanged.setter
	def set(self,m_OnTapChargesChanged):
		self._m_OnTapChargesChanged=m_OnTapChargesChanged

	@property
	def m_OnTapStateChanged(self):
		return self._m_OnTapStateChanged
	@m_OnTapStateChanged.setter
	def set(self,m_OnTapStateChanged):
		self._m_OnTapStateChanged=m_OnTapStateChanged

	@property
	def m_OnTapChargesActiveChanged(self):
		return self._m_OnTapChargesActiveChanged
	@m_OnTapChargesActiveChanged.setter
	def set(self,m_OnTapChargesActiveChanged):
		self._m_OnTapChargesActiveChanged=m_OnTapChargesActiveChanged

	@property
	def m_OnSummoningSicknessChanged(self):
		return self._m_OnSummoningSicknessChanged
	@m_OnSummoningSicknessChanged.setter
	def set(self,m_OnSummoningSicknessChanged):
		self._m_OnSummoningSicknessChanged=m_OnSummoningSicknessChanged

	@property
	def m_OnRecommendedLocationsChanged(self):
		return self._m_OnRecommendedLocationsChanged
	@m_OnRecommendedLocationsChanged.setter
	def set(self,m_OnRecommendedLocationsChanged):
		self._m_OnRecommendedLocationsChanged=m_OnRecommendedLocationsChanged

	@property
	def m_OnMadnessChanged(self):
		return self._m_OnMadnessChanged
	@m_OnMadnessChanged.setter
	def set(self,m_OnMadnessChanged):
		self._m_OnMadnessChanged=m_OnMadnessChanged

	@property
	def m_OnPayActiveChanged(self):
		return self._m_OnPayActiveChanged
	@m_OnPayActiveChanged.setter
	def set(self,m_OnPayActiveChanged):
		self._m_OnPayActiveChanged=m_OnPayActiveChanged

	@property
	def m_OnPlayedByChanged(self):
		return self._m_OnPlayedByChanged
	@m_OnPlayedByChanged.setter
	def set(self,m_OnPlayedByChanged):
		self._m_OnPlayedByChanged=m_OnPlayedByChanged

	@property
	def m_OnEnergyChanged(self):
		return self._m_OnEnergyChanged
	@m_OnEnergyChanged.setter
	def set(self,m_OnEnergyChanged):
		self._m_OnEnergyChanged=m_OnEnergyChanged

	@property
	def m_OnBecameVisuallyDirty(self):
		return self._m_OnBecameVisuallyDirty
	@m_OnBecameVisuallyDirty.setter
	def set(self,m_OnBecameVisuallyDirty):
		self._m_OnBecameVisuallyDirty=m_OnBecameVisuallyDirty

	@property
	def PlayedBy(self):
		return self._PlayedBy
	@PlayedBy.setter
	def set(self,PlayedBy):
		self._PlayedBy=PlayedBy

	@property
	def IsWaitingToDie(self):
		return self._IsWaitingToDie
	@IsWaitingToDie.setter
	def set(self,IsWaitingToDie):
		self._IsWaitingToDie=IsWaitingToDie

	@property
	def IsWaitingForBanish(self):
		return self._IsWaitingForBanish
	@IsWaitingForBanish.setter
	def set(self,IsWaitingForBanish):
		self._IsWaitingForBanish=IsWaitingForBanish

	@property
	def IsWaitingForDestroy(self):
		return self._IsWaitingForDestroy
	@IsWaitingForDestroy.setter
	def set(self,IsWaitingForDestroy):
		self._IsWaitingForDestroy=IsWaitingForDestroy

	@property
	def DeathType(self):
		return self._DeathType
	@DeathType.setter
	def set(self,DeathType):
		self._DeathType=DeathType

	@property
	def ECardVisibility(self):
		return self._ECardVisibility
	@ECardVisibility.setter
	def set(self,ECardVisibility):
		self._ECardVisibility=ECardVisibility

	def toString(self):
		print("cardManager:",hex(self._cardManager),"\n","cardManager:",hex(self._cardManager),"\n","AbilityData:",hex(self._AbilityData),"\n"
,"AEntityId:",hex(self._AEntityId),"\n","CardAbilities:",hex(self._CardAbilities),"\n"
,"Template:",hex(self._Template),"\n","cardDefinition:",hex(self._cardDefinition),"\n"
,"id:",hex(self._id),"\n","m_Position:",hex(self._m_Position),"\n"
,"EFactionId:",hex(self._EFactionId),"\n","CardBackVanityId:",hex(self._CardBackVanityId),"\n"
,"DeckFactionId:",hex(self._DeckFactionId),"\n","IsBeingPlayedBy:",hex(self._IsBeingPlayedBy),"\n"
,"FromPosition:",hex(self._FromPosition),"\n","PlayedFrom:",hex(self._PlayedFrom),"\n"
,"LastActivePosition:",hex(self._LastActivePosition),"\n","Data:",hex(self._Data),"\n"
,"m_OnStartedToMove:",hex(self._m_OnStartedToMove),"\n","m_OnMoved:",hex(self._m_OnMoved),"\n"
,"m_OnVisibilityChanged:",hex(self._m_OnVisibilityChanged),"\n","m_OnPowerChanged:",hex(self._m_OnPowerChanged),"\n"
,"m_OnStatusChanged:",hex(self._m_OnStatusChanged),"\n","m_OnActiveKeywordsChanged:",hex(self._m_OnActiveKeywordsChanged),"\n"
,"m_OnDefinitionChanged:",hex(self._m_OnDefinitionChanged),"\n","m_OnTimerChanged:",hex(self._m_OnTimerChanged),"\n"
,"m_OnOverrideTimerIconChanged:",hex(self._m_OnOverrideTimerIconChanged),"\n","m_OnTapChargesChanged:",hex(self._m_OnTapChargesChanged),"\n"
,"m_OnTapStateChanged:",hex(self._m_OnTapStateChanged),"\n","m_OnTapChargesActiveChanged:",hex(self._m_OnTapChargesActiveChanged),"\n"
,"m_OnSummoningSicknessChanged:",hex(self._m_OnSummoningSicknessChanged),"\n","m_OnRecommendedLocationsChanged:",hex(self._m_OnRecommendedLocationsChanged),"\n"
,"m_OnMadnessChanged:",hex(self._m_OnMadnessChanged),"\n","m_OnPayActiveChanged:",hex(self._m_OnPayActiveChanged),"\n"
,"m_OnPlayedByChanged:",hex(self._m_OnPlayedByChanged),"\n","m_OnEnergyChanged:",hex(self._m_OnEnergyChanged),"\n"
,"m_OnBecameVisuallyDirty:",hex(self._m_OnBecameVisuallyDirty),"\n","PlayedBy:",hex(self._PlayedBy),"\n"
,"IsWaitingToDie:",hex(self._IsWaitingToDie),"\n","IsWaitingForBanish:",hex(self._IsWaitingForBanish),"\n"
,"IsWaitingForDestroy:",hex(self._IsWaitingForDestroy),"\n","DeathType:",hex(self._DeathType),"\n"
,"ECardVisibility:",hex(self._ECardVisibility),"\n")