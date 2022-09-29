class Cd(object):

	def __init__(self):
		self._GwentGameplay_Card_1 = 0x10
		self._GwentGameplay_ECardTier_2 = 0x18
		self._GwentGameplay_CardPower_3 = 0x20
		self._GwentGameplay_CardStatuses_4 = 0x28
		self._GwentGameplay_CardKeywords_5 = 0x30
		self._GwentGameplay_TapCardCharges_6 = 0x38
		self._GwentGameplay_CardCategory_7 = 0x40
		self._GwentGameplay_CardCategory_8 = 0x48
		self._GwentGameplay_CardSemanticTag_9 = 0x50
		self._GwentGameplay_CardRange_10 = 0x58
		self._GwentGameplay_CardRecommendedLocations_11 = 0x60
		self._GwentGameplay_CardWallet_12 = 0x68
		self._GwentGameplay_CardEnergy_13 = 0x70

	@property
	def GwentGameplay_Card_1(self):
		return self._GwentGameplay_Card_1
	@GwentGameplay_Card_1.setter
	def set(self,GwentGameplay_Card_1):
		self._GwentGameplay_Card_1=GwentGameplay_Card_1

	@property
	def GwentGameplay_ECardTier_2(self):
		return self._GwentGameplay_ECardTier_2
	@GwentGameplay_ECardTier_2.setter
	def set(self,GwentGameplay_ECardTier_2):
		self._GwentGameplay_ECardTier_2=GwentGameplay_ECardTier_2

	@property
	def GwentGameplay_CardPower_3(self):
		return self._GwentGameplay_CardPower_3
	@GwentGameplay_CardPower_3.setter
	def set(self,GwentGameplay_CardPower_3):
		self._GwentGameplay_CardPower_3=GwentGameplay_CardPower_3

	@property
	def GwentGameplay_CardStatuses_4(self):
		return self._GwentGameplay_CardStatuses_4
	@GwentGameplay_CardStatuses_4.setter
	def set(self,GwentGameplay_CardStatuses_4):
		self._GwentGameplay_CardStatuses_4=GwentGameplay_CardStatuses_4

	@property
	def GwentGameplay_CardKeywords_5(self):
		return self._GwentGameplay_CardKeywords_5
	@GwentGameplay_CardKeywords_5.setter
	def set(self,GwentGameplay_CardKeywords_5):
		self._GwentGameplay_CardKeywords_5=GwentGameplay_CardKeywords_5

	@property
	def GwentGameplay_TapCardCharges_6(self):
		return self._GwentGameplay_TapCardCharges_6
	@GwentGameplay_TapCardCharges_6.setter
	def set(self,GwentGameplay_TapCardCharges_6):
		self._GwentGameplay_TapCardCharges_6=GwentGameplay_TapCardCharges_6

	@property
	def GwentGameplay_CardCategory_7(self):
		return self._GwentGameplay_CardCategory_7
	@GwentGameplay_CardCategory_7.setter
	def set(self,GwentGameplay_CardCategory_7):
		self._GwentGameplay_CardCategory_7=GwentGameplay_CardCategory_7

	@property
	def GwentGameplay_CardCategory_8(self):
		return self._GwentGameplay_CardCategory_8
	@GwentGameplay_CardCategory_8.setter
	def set(self,GwentGameplay_CardCategory_8):
		self._GwentGameplay_CardCategory_8=GwentGameplay_CardCategory_8

	@property
	def GwentGameplay_CardSemanticTag_9(self):
		return self._GwentGameplay_CardSemanticTag_9
	@GwentGameplay_CardSemanticTag_9.setter
	def set(self,GwentGameplay_CardSemanticTag_9):
		self._GwentGameplay_CardSemanticTag_9=GwentGameplay_CardSemanticTag_9

	@property
	def GwentGameplay_CardRange_10(self):
		return self._GwentGameplay_CardRange_10
	@GwentGameplay_CardRange_10.setter
	def set(self,GwentGameplay_CardRange_10):
		self._GwentGameplay_CardRange_10=GwentGameplay_CardRange_10

	@property
	def GwentGameplay_CardRecommendedLocations_11(self):
		return self._GwentGameplay_CardRecommendedLocations_11
	@GwentGameplay_CardRecommendedLocations_11.setter
	def set(self,GwentGameplay_CardRecommendedLocations_11):
		self._GwentGameplay_CardRecommendedLocations_11=GwentGameplay_CardRecommendedLocations_11

	@property
	def GwentGameplay_CardWallet_12(self):
		return self._GwentGameplay_CardWallet_12
	@GwentGameplay_CardWallet_12.setter
	def set(self,GwentGameplay_CardWallet_12):
		self._GwentGameplay_CardWallet_12=GwentGameplay_CardWallet_12

	@property
	def GwentGameplay_CardEnergy_13(self):
		return self._GwentGameplay_CardEnergy_13
	@GwentGameplay_CardEnergy_13.setter
	def set(self,GwentGameplay_CardEnergy_13):
		self._GwentGameplay_CardEnergy_13=GwentGameplay_CardEnergy_13

	def toString(self):
		print("GwentGameplay_Card_1:",hex(self._GwentGameplay_Card_1),"\n","GwentGameplay_Card_1:",hex(self._GwentGameplay_Card_1),"\n","GwentGameplay_ECardTier_2:",hex(self._GwentGameplay_ECardTier_2),"\n"
,"GwentGameplay_CardPower_3:",hex(self._GwentGameplay_CardPower_3),"\n","GwentGameplay_CardStatuses_4:",hex(self._GwentGameplay_CardStatuses_4),"\n"
,"GwentGameplay_CardKeywords_5:",hex(self._GwentGameplay_CardKeywords_5),"\n","GwentGameplay_TapCardCharges_6:",hex(self._GwentGameplay_TapCardCharges_6),"\n"
,"GwentGameplay_CardCategory_7:",hex(self._GwentGameplay_CardCategory_7),"\n","GwentGameplay_CardCategory_8:",hex(self._GwentGameplay_CardCategory_8),"\n"
,"GwentGameplay_CardSemanticTag_9:",hex(self._GwentGameplay_CardSemanticTag_9),"\n","GwentGameplay_CardRange_10:",hex(self._GwentGameplay_CardRange_10),"\n"
,"GwentGameplay_CardRecommendedLocations_11:",hex(self._GwentGameplay_CardRecommendedLocations_11),"\n","GwentGameplay_CardWallet_12:",hex(self._GwentGameplay_CardWallet_12),"\n"
,"GwentGameplay_CardEnergy_13:",hex(self._GwentGameplay_CardEnergy_13),"\n")