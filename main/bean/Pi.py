class Pi(object):

	def __init__(self):		self._Name = 0x10
		self._ServiceId = 0x18
		self._Title = 0x20
		self._Personality = 0x28
		self._Level = 0x30
		self._ParagonLevel = 0x34
		self._MMR = 0x38
		self._Rank = 0x3C
		self._Vanity = 0x40

	@property
	def Name(self):
		return self._Name
	@Name.setter
	def set(self,Name):
		self._Name=Name

	@property
	def ServiceId(self):
		return self._ServiceId
	@ServiceId.setter
	def set(self,ServiceId):
		self._ServiceId=ServiceId

	@property
	def Title(self):
		return self._Title
	@Title.setter
	def set(self,Title):
		self._Title=Title

	@property
	def Personality(self):
		return self._Personality
	@Personality.setter
	def set(self,Personality):
		self._Personality=Personality

	@property
	def Level(self):
		return self._Level
	@Level.setter
	def set(self,Level):
		self._Level=Level

	@property
	def ParagonLevel(self):
		return self._ParagonLevel
	@ParagonLevel.setter
	def set(self,ParagonLevel):
		self._ParagonLevel=ParagonLevel

	@property
	def MMR(self):
		return self._MMR
	@MMR.setter
	def set(self,MMR):
		self._MMR=MMR

	@property
	def Rank(self):
		return self._Rank
	@Rank.setter
	def set(self,Rank):
		self._Rank=Rank

	@property
	def Vanity(self):
		return self._Vanity
	@Vanity.setter
	def set(self,Vanity):
		self._Vanity=Vanity

	def toString(self):
		print("Name:",hex(self._Name),"\n","Name:",hex(self._Name),"\n","ServiceId:",hex(self._ServiceId),"\n","Title:",hex(self._Title),"\n","Personality:",hex(self._Personality),"\n","Level:",hex(self._Level),"\n","ParagonLevel:",hex(self._ParagonLevel),"\n","MMR:",hex(self._MMR),"\n","Rank:",hex(self._Rank),"\n","Vanity:",hex(self._Vanity),"\n")