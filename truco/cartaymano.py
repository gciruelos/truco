#
# Clases Carta y Mano con los metodos en los que esta basado casi todo 
# el programa
# Author: Gonzalo Ciruelos <comp.gonzalo@gmail.com>
# License: GPLv3
#


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
		num = int(self.numero)
		if num == 1:
			if self.palo == 'Oro' or self.palo == 'Copa':
				return 8
			elif self.palo == 'Basto':
				return 13
			elif self.palo == 'Espada':
				return 14
		elif num == 2:
			return 9
		elif num == 3:
			return 10
		elif num == 4:
			return 1
		elif num == 5:
			return 2
		elif num == 6:
			return 3
		elif num == 7:
			if self.palo == 'Basto' or self.palo == 'Copa':
				return 4
			elif self.palo == 'Oro':
				return 11
			elif self.palo == 'Espada':
				return 12
		elif num == 10:
			return 5
		elif num == 11:
			return 6
		elif num == 12:
			return 7
		else:
			print 'Hubo un error al ingresar las cartas, por favor hacelo de nuevo\n'
			ingresar_mano()
	def __getitem__(self, indice):
		if indice == 0:
			return self.numero
		elif indice == 1:
			return self.palo
	def __str__(self):
		return str(self.numero)+' de '+str(self.palo)+'.'


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
		if quien=='CPU':
			self.cartas.remove(carta)
			print '---> Tiro el', Carta(carta).numero, 'de', Carta(carta).palo
			cartas_tiradas_CPU.append(carta)
		else:
			self.cartas.remove(carta)
			print 'Las cartas que te quedan son', self
			cartas_tiradas_MIA.append(carta)
	def mayor_carta(self):
		if len(self.cartas) != 1:
			maximo=0
			mayorcarta=[]
			for carta in self.cartas:
				if Carta(carta).jerarquizar()>maximo:
					maximo = Carta(carta).jerarquizar()
					mayorcarta = carta
		else:
			mayorcarta = self.cartas[0]
		return mayorcarta
	def media_carta(self):
		try:
			media_carta = self.decir_cartas()
			media_carta.remove(self.mayor_carta())
			media_carta.remove(self.menor_carta())
			media_carta = media_carta[0]
		except ValueError:
			media_carta = None
		return media_carta		
	def menor_carta(self):
		minimo=15
		menorcarta=[]
		for carta in self.cartas:
			if Carta(carta).jerarquizar()<minimo:
				minimo = Carta(carta).jerarquizar()
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

