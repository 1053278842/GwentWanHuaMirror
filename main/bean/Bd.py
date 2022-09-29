class Bd(object):

	def __init__(self):		self._FactionId = 0x10
		self._LeaderAbility = 0x14
		self._Stratagem = 0x1C
		self._Cards = 0x28
		self._CardBackVanityId = 0x30
		self._Name = 0x38
		self._AbilityId = 0x40
		self._LeaderSetup = 0x48

	@property
	def FactionId(self):
		return self._FactionId
	@FactionId.setter
	def set(self,FactionId):
		self._FactionId=FactionId

	@property
	def LeaderAbility(self):
		return self._LeaderAbility
	@LeaderAbility.setter
	def set(self,LeaderAbility):
		self._LeaderAbility=LeaderAbility

	@property
	def Stratagem(self):
		return self._Stratagem
	@Stratagem.setter
	def set(self,Stratagem):
		self._Stratagem=Stratagem

	@property
	def Cards(self):
		return self._Cards
	@Cards.setter
	def set(self,Cards):
		self._Cards=Cards

	@property
	def CardBackVanityId(self):
		return self._CardBackVanityId
	@CardBackVanityId.setter
	def set(self,CardBackVanityId):
		self._CardBackVanityId=CardBackVanityId

	@property
	def Name(self):
		return self._Name
	@Name.setter
	def set(self,Name):
		self._Name=Name

	@property
	def AbilityId(self):
		return self._AbilityId
	@AbilityId.setter
	def set(self,AbilityId):
		self._AbilityId=AbilityId

	@property
	def LeaderSetup(self):
		return self._LeaderSetup
	@LeaderSetup.setter
	def set(self,LeaderSetup):
		self._LeaderSetup=LeaderSetup

	def toString(self):
		print("FactionId:",hex(self._FactionId),"\n","FactionId:",hex(self._FactionId),"\n","LeaderAbility:",hex(self._LeaderAbility),"\n","Stratagem:",hex(self._Stratagem),"\n","Cards:",hex(self._Cards),"\n","CardBackVanityId:",hex(self._CardBackVanityId),"\n","Name:",hex(self._Name),"\n","AbilityId:",hex(self._AbilityId),"\n","LeaderSetup:",hex(self._LeaderSetup),"\n")