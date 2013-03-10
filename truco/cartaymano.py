cartas_tiradas_MIA = []
cartas_tiradas_CPU = []

def suma_envido(n,m):
	if n>=10:
		n = 0
	if m>=10:
		m = 0
	return 20+n+m

class Carta:
	def __init__(self, carta):
		self.numero = carta[0]
		self.palo = carta[1]
	def decir(self):
		return [self.numero, self.palo]
	def jerarquizar(self):
		if int(self.numero) == 1:
			if self.palo == 'Oro' or self.palo == 'Copa':
				return 8
			elif self.palo == 'Basto':
				return 13
			elif self.palo == 'Espada':
				return 14
		elif int(self.numero) == 2:
			return 9
		elif int(self.numero) == 3:
			return 10
		elif int(self.numero) == 4:
			return 1
		elif int(self.numero) == 5:
			return 2
		elif int(self.numero) == 6:
			return 3
		elif int(self.numero) == 7:
			if self.palo == 'Basto' or self.palo == 'Copa':
				return 4
			elif self.palo == 'Oro':
				return 11
			elif self.palo == 'Espada':
				return 12
		elif int(self.numero) == 10:
			return 5
		elif int(self.numero) == 11:
			return 6
		elif int(self.numero) == 12:
			return 7
		else:
			print 'Hubo un error al ingresar las cartas, por favor hacelo de nuevo\n'
			ingresar_mano()

	def __str__(self):
		return str(self.numero), 'de', (self.palo+'.')


class Mano:
	def __init__(self, *args):
		self.cartas = []
		for carta in args:
			self.cartas.append(carta)
		if len(self.cartas)==1:
			self.c1 = Carta(self.cartas[0])
		if len(self.cartas)==2:
			self.c1 = Carta(self.cartas[0])
			self.c2 = Carta(self.cartas[1])
		if len(self.cartas)==3:
			self.c1 = Carta(self.cartas[0])
			self.c2 = Carta(self.cartas[1])
			self.c3 = Carta(self.cartas[2])
	def tengo_envido(self):		
		if self.c2.palo == self.c1.palo:
			return suma_envido(self.c2.numero, self.c1.numero)
		elif self.c2.palo == self.c3.palo:
			return suma_envido(self.c2.numero, self.c3.numero)
		elif self.c3.palo == self.c1.palo:
			return suma_envido(self.c3.numero, self.c1.numero)
		else:
			return 0
	def decir_cartas(self):
		if len(self.cartas)==1:
			return Carta(self.cartas[0]).decir()
		if len(self.cartas)==2:
			return [Carta(self.cartas[0]).decir(), Carta(self.cartas[1]).decir()]
		if len(self.cartas)==3:
			return [Carta(self.cartas[0]).decir(), Carta(self.cartas[1]).decir(), Carta(self.cartas[2]).decir()]
	def tirar_carta(self, carta, quien='CPU'):
		global cartas_tiradas_CPU, cartas_tiradas_MIA
		global cartas_tiradas_CPU, cartas_tiradas_MIA
		if quien=='CPU':
			self.cartas.remove(carta)
			print '---> Tiro el', Carta(carta).numero, 'de', Carta(carta).palo
			cartas_tiradas_CPU.append(carta)
		else:
			self.cartas.remove(carta)
			print 'Las cartas que te quedan son', self
			cartas_tiradas_MIA.append(carta)
	def mayor_carta(self):
		maximo=0
		mayorcarta=[]
		for carta in self.cartas:
			Carta(carta).jerarquizar()<maximo
			mayorcarta=carta
		return mayorcarta
	def media_carta(self):
		cartas = Mano(self.decir_cartas())
		cartas.cartas.remove(cartas.mayor_carta())
		cartas.cartas.remove(cartas.menor_carta())
		return cartas.decir_cartas()		
	def menor_carta(self):
		minimo=15
		menorcarta=[]
		for carta in self.cartas:
			Carta(carta).jerarquizar()<minimo
			menorcarta=carta
		return menorcarta
	def __str__(self):
		cartas_que_tengo = []
		for carta in self.cartas:
			if carta != 0:
				cartas_que_tengo.append(carta)
		cartas_returnear = []
		for carta in cartas_que_tengo:
			cartas_returnear.append(str(Carta(carta).numero)+' de '+str(Carta(carta).palo))
		return ', '.join(cartas_returnear)
