class Bss(object):

	def __init__(self):		self._PlayerId = 0x10
		self._Hand = 0x18
		self._Graveyard = 0x20
		self._Melee = 0x28
		self._Ranged = 0x30

	@property
	def PlayerId(self):
		return self._PlayerId
	@PlayerId.setter
	def set(self,PlayerId):
		self._PlayerId=PlayerId

	@property
	def Hand(self):
		return self._Hand
	@Hand.setter
	def set(self,Hand):
		self._Hand=Hand

	@property
	def Graveyard(self):
		return self._Graveyard
	@Graveyard.setter
	def set(self,Graveyard):
		self._Graveyard=Graveyard

	@property
	def Melee(self):
		return self._Melee
	@Melee.setter
	def set(self,Melee):
		self._Melee=Melee

	@property
	def Ranged(self):
		return self._Ranged
	@Ranged.setter
	def set(self,Ranged):
		self._Ranged=Ranged

	def toString(self):
		print("PlayerId:",hex(self._PlayerId),"\n","PlayerId:",hex(self._PlayerId),"\n","Hand:",hex(self._Hand),"\n","Graveyard:",hex(self._Graveyard),"\n","Melee:",hex(self._Melee),"\n","Ranged:",hex(self._Ranged),"\n")