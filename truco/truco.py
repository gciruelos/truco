## Truco
# Version 0.0.1beta
#
#
# Esta es una implementacion del juego de cartas truco hecha en Python.
#
# Todo lo que esta dicho despues de una flecha ("--->") es porque lo dice la computadora
# el resto debe ser interpretado como pies a inputs del jugador.
#
# Cuando se deba ingresar una carta se debe hacer de la siguiente manera:
# "numero arabigo" de "palo en singular y con mayuscula". Por ejemplo: "2 de Basto",
# "4 de Espada" o "5 de Copa" son cartas validas, mientras que "dos de Basto", 
# "4 de espada" o "5 de Copas" no lo son. (Proximamente lo seran).
#
#
# Si desea irse al mazo, cuando le pregunte que carta quiere ingresar,
# ingrese "Mazo" sin comillas o presione la combinacion de teclas EOF 
# (En Unix-like es Ctrl+D)
#
# 
# Author: Gonzalo Ciruelos <comp.gonzalo@gmail.com>
# License: GPLv3



from cartaymano import Mano, Carta, cartas_tiradas_MIA, cartas_tiradas_CPU

import random

SI = ('s','S','si','Si')		#Tambien podria ir con expresiones regulares, pero es mas facil asi. ('[sS][iI]?')

manos = [None, None, None]

tiene_el_quiero = None			#True lo tiene la pc, False el jugador

ManoCPU = Mano()
ManoMIA = Mano()

Mano_Quien = bool(random.randint(0,1))			#Si va la pc True, si va el jugador False

envido_CPU = 0
envido_JUG = 0

carta_del_otro = []
#tanto_del_otro = 0

envido_hecho = 0
truco_hecho = 0

pJUG = 0
pCPU = 0

Palos =	['Oro', 'Espada', 'Copa', 'Basto'] 
Numeros = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]	
Mazo = []
for palo in Palos:
	for numero in Numeros:
		Mazo.append([numero,palo])


#################------JUEGO


def primera_mano(tanto, mano):

	global manos, mis_cartas_tiradas, cartas, cartas_tiradas_CPU, cartas_tiradas_MIA


	if mano == False:			#Va el jugador
		envido(False, tanto, mano) 
		cartita = Carta(carta_del_oponente())
		envido(True, tanto, mano)
		quejugar(mano, cartita)

	else:						#Va la pc
		envido(True, tanto, mano)
		quejugar(mano)
		envido(False, tanto, mano)
		carta_del_oponente()

	if Carta(cartas_tiradas_MIA[0]).jerarquizar() > Carta(cartas_tiradas_CPU[0]).jerarquizar():
		manos[0] = 0
		segunda_mano('jugador')
	elif Carta(cartas_tiradas_MIA[0]).jerarquizar() < Carta(cartas_tiradas_CPU[0]).jerarquizar():
		manos[0] = 1
		segunda_mano('cpu')
	elif Carta(cartas_tiradas_MIA[0]).jerarquizar() == Carta(cartas_tiradas_CPU[0]).jerarquizar():
		manos[0] = 2
		segunda_mano('parda')

		
def segunda_mano(quienva):
	
	global manos, mis_cartas_tiradas, cartas, cartas_tiradas_CPU, cartas_tiradas_MIA

	if quienva == 'jugador':
		truco('el')
		cartita = Carta(carta_del_oponente())
		truco('yo')
		quejugar(False, cartita)		
	elif quienva == 'cpu':
		truco('yo')
		quejugar(True)
		truco('el')
		carta_del_oponente()
	else:
		truco('yo')
		quejugar(None)
		truco('el')
		carta_del_oponente()
	
	if Carta(cartas_tiradas_MIA[1]).jerarquizar() > Carta(cartas_tiradas_CPU[1]).jerarquizar():
		manos[1] = 0
		if manos[0] == 0:
			print '---> Perdi la mano.'
			exit()
		tercera_mano('jugador')
	elif Carta(cartas_tiradas_MIA[1]).jerarquizar() < Carta(cartas_tiradas_CPU[1]).jerarquizar():
		manos[1] = 1
		if manos[0] == 1:
			print '---> Gane la mano.'
			exit()
		tercera_mano('cpu')
	elif Carta(cartas_tiradas_MIA[1]).jerarquizar() == Carta(cartas_tiradas_CPU[1]).jerarquizar():
		manos[1] = 2
		tercera_mano('parda')
		

def tercera_mano(quienva):
	
	global manos, mis_cartas_tiradas, cartas, cartas_tiradas_CPU, cartas_tiradas_MIA
	
	if quienva == 'jugador':
		truco('el')
		cartita = Carta(carta_del_oponente())
		truco('yo')
		quejugar(False, cartita)
	elif quienva == 'cpu':
		truco('yo')
		quejugar(True)
		truco('el')
		carta_del_oponente()
	else:
		truco('yo')
		quejugar(None)
		truco('el')
		carta_del_oponente()
	
	if Carta(cartas_tiradas_CPU[2]).jerarquizar() > Carta(cartas_tiradas_MIA[2]).jerarquizar():
		print '---> Gane'
	else:
		print '---> Perdi'
	exit()
	
	

def truco(quienlocanta, pasar = 0):
	
	global truco_hecho, tiene_el_quiero
	
	vaqueriendo = True
	
	
	if quienlocanta == 'el' and tiene_el_quiero is not True:
		if pasar == 0:
			if truco_hecho == 0:
				cantar = raw_input('Queres cantar truco? (S/n) ' )
			elif truco_hecho == 1:
				cantar = raw_input('Queres cantar retruco? (S/n) ' )
			elif truco_hecho == 2:
				cantar = raw_input('Queres cantar vale cuatro? (S/n) ' )
			else:
				pass
		else:
			cantar = 'S'
		
		if cantar in SI:
			if truco_utilidad()==True:
				print '---> Quiero'
				truco_hecho += 1
				tiene_el_quiero = False
			else:
				print '---> No quiero'
				vaqueriendo = False
		else:
			pass
	elif quienlocanta == 'cpu' and tiene_el_quiero is not False:
		if truco_utilidad()==True:
			if truco_hecho == 0:
				cantar = raw_input('---> Truco\n---> Queres? (S/n/R) ')
			elif truco_hecho == 1:
				cantar = raw_input('---> Re truco\n---> Queres? (S/n/R) ')
			elif truco_hecho == 2:
				cantar = raw_input('---> Vale cuatro\n---> Queres? (S/n/R) ')
			else:
				pass
			if cantar in SI:
				truco_hecho += 1
				tiene_el_quiero = True
			elif cantar == 'R':
				truco_hecho += 1
				truco('el',1)
			else:
				vaqueriendo = False
		else:
			pass
	else:
		pass
			
	if vaqueriendo == False:
		exit()


def envido(soymano, tanto, mano):
	
	global envido_hecho, envido_CPU, envido_JUG
	
	if envido_hecho == 0:
		
		if soymano == True:
			if cantar_envido(tanto, tanto) == True:
				env = raw_input('---> Real envido\n---> Queres? (S/n) ')
				if env in SI:
					hablar_envido(mano)
				envido_hecho = 1
			else:
				if cantar_envido(tanto, 100) == True:
					env = raw_input('---> Envido\n---> Queres? (S/n) ')
					if env in SI:
						hablar_envido(mano)
					envido_hecho = 1
				#else:
				#	print 'No cantes nada'
		else:
			canto_envido = raw_input('Queres cantar envido? (S/n) ')
			
			if canto_envido in SI:
				envido_hecho = 1
				if cantar_envido(tanto, tanto) == True:
					env = raw_input('---> Envido\n---> Queres? (S/n) ')
					if env in SI:
						hablar_envido(mano)
						
				else:
					if cantar_envido(tanto, 100) == True:
						print '---> Quiero'
						hablar_envido(mano)
					else:
						print '---> No quiero'
						
			else:
				pass

	else:
		pass
		

#################------CARTAS


def carta_del_oponente():
	while True:
		try:
			cartadeljugador = raw_input('Que carta queres tirar? ')
			if cartadeljugador == 'Mazo':
				exit()
		except EOFError:
			seguro = raw_input('Seguro queres irte al mazo? (S/n) ')
			if seguro in SI:
				exit()
			else:
				continue
		lacarta = cartadeljugador.split(' de ')
		lacarta[0] = int(lacarta[0])
		global ManoMIA
		if lacarta in ManoMIA.decir_cartas():
			ManoMIA.tirar_carta(lacarta, 'jugador')
		elif lacarta == ManoMIA.decir_cartas():
			ManoMIA.tirar_carta(lacarta, 'jugador')
		else:
			print 'Ingresa una carta que tengas'
			continue
		return lacarta
		break


#################------UTILIDADES


def una_carta_mas():
	#EL JUGADOR tiene una carta mas devuelve True, si CPU tiene una carta mas False y si tienen iguales None.
	global ManoMIA, ManoCPU
	
	try:
		if type(ManoCPU.decir_cartas()[1]) == list:			#Si al CPU le queda mas de una carta
			try:
				if len(ManoCPU.decir_cartas())<len(ManoMIA.decir_cartas()):			
					return True
				elif len(ManoCPU.decir_cartas())>len(ManoMIA.decir_cartas()):
					return False
				else:
					return None
			except TypeError:
				if ManoCPU.decir_cartas() == []:
					return True
				else:
					return False
		elif type(ManoCPU.decir_cartas()[1]) == (str or int):
			if type(ManoMIA.decir_cartas()[1]) == (str or int):
				return None
			elif type(ManoMIA.decir_cartas()[1]) == list:
				return True
			else:
				return False
	except TypeError:
		return True
		

def quejugar(mano, carta_del_jugador = None):
	global manos
	global ManoCPU, ManoMIA
	
	maximo = 15
	minimo = 0
	posibles = []
	if carta_del_jugador != None:
		valor_carta_jugador = carta_del_jugador.jerarquizar()

	
	if manos[0] == None:	
		if mano == False:
			for carta in ManoCPU.decir_cartas():
				carta = Carta(carta)									#Se fija si alguna carta esta entre x y x+3
				if carta.jerarquizar() > valor_carta_jugador and carta.jerarquizar() < (valor_carta_jugador+3):
					posibles.append(carta)
			if posibles == []:
				ManoCPU.tirar_carta(ManoCPU.menor_carta())				#Si no hay ninguna que cumpla esa condicion, tira la menor
			else:
				for carta in posibles:									#Si hay, elije la menor
					if Carta(carta).jerarquizar() < maximo:
						maximo = Carta(carta).jerarquizar()
				for carta2 in ManoCPU.decir_cartas():					#Busca esa carta y la tira
					if Carta(carta2).jerarquizar() == maximo:
						ManoCPU.tirar_carta(carta2)
		elif mano == True:
			valor_mayor_carta = Carta(ManoCPU.mayor_carta()).jerarquizar()
			valor_menor_carta = Carta(ManoCPU.menor_carta()).jerarquizar()
			valor_media_carta = Carta(ManoCPU.media_carta()).jerarquizar()		
			if valor_mayor_carta > 10:									#Si la mayor carta es mas grande que un 3, 
				if valor_media_carta >= 10:								#y la segunda mayor carta tambien, tira la segunda mayor
					ManoCPU.tirar_carta(ManoCPU.media_carta())
				else:													#si no, tira la mas baja
					ManoCPU.tirar_carta(ManoCPU.menor_carta())
			elif valor_mayor_carta == 10:								#Si la carta mas alta es un 3
				if valor_menor_carta+valor_media_carta >= (valor_mayor_carta-2):	#y si las otras dos son masomenos buenas, tira el 3
					ManoCPU.tirar_carta(ManoCPU.mayor_carta())
				elif valor_menor_carta+valor_media_carta < (valor_mayor_carta-2):	#si no, tira la mas baja
					ManoCPU.tirar_carta(ManoCPU.menor_carta())
			elif valor_mayor_carta < 10:								#Si todas son mas chicas que 3 tira la mas chica
				#r=random.randint(1,3)									#en un futuro, una al azar
				ManoCPU.tirar_carta(ManoCPU.menor_carta())
		else:
			pass

	elif manos[1] == None:	
		if mano == False:
			if Carta(ManoCPU.menor_carta()).jerarquizar() > carta_del_jugador.jerarquizar():		#Se fija si alguna carta es mayor que x
				ManoCPU.tirar_carta(ManoCPU.menor_carta())					
			elif Carta(ManoCPU.mayor_carta()).jerarquizar() > carta_del_jugador.jerarquizar():
				ManoCPU.tirar_carta(ManoCPU.mayor_carta())
			else: 
				print '---> Ganaste la mano, bien jugado.'
				exit()
		elif mano == True:
			if Carta(ManoCPU.mayor_carta()).jerarquizar() >= 10:
				ManoCPU.tirar_carta(ManoCPU.mayor_carta())
			else:
				ManoCPU.tirar_carta(ManoCPU.menor_carta())	
		else:
			ManoCPU.tirar_carta(ManoCPU.mayor_carta())
	
	elif manos[2] == None:
		if mano == False:
			valor_mayor_carta = Carta(ManoCPU.mayor_carta()).jerarquizar()
			if valor_mayor_carta > valor_carta_jugador:
				ManoCPU.tirar_carta(ManoCPU.mayor_carta())				
			else: 
				print '---> Me voy al mazo.'
				exit()	
		elif mano == True:
			ManoCPU.tirar_carta(ManoCPU.mayor_carta())
		else:
			ManoCPU.tirar_carta(ManoCPU.mayor_carta())


def randomizacion_de_eventos(probabilidad):
	azar = random.randint(1, 100)
	if azar <= probabilidad:
		return True
	else: 
		return False


#################------TRUCO


def truco_utilidad():
	
	global manos
	
	jugador_cartademas = una_carta_mas()
	
	if manos[1] == None:
		if jugador_cartademas == True:
			if manos[0] == True and ((Carta(cartas_tiradas_CPU[1]).jerarquizar() or (Carta(ManoCPU.decir_cartas()[0]).jerarquizar())) >= 9):
				return True
			elif manos[0] == False:
				if (cartas_tiradas_CPU[1].jerarquizar() + Carta(ManoCPU.decir_cartas()[0]).jerarquizar()) >= 18:
					return True
				else:
					return False
			else:
				if Carta(cartas_tiradas_CPU[1]).jerarquizar() >= 9:
					return True
				else:
					return False
		elif jugador_cartademas == None or False:
			if manos[0] == True and ((Carta(ManoCPU.decir_cartas()[0]).jerarquizar() or (Carta(ManoCPU.decir_cartas()[1]).jerarquizar())) >= 9):
				return True
			elif manos[0] == False:
				if (Carta(ManoCPU.decir_cartas()[0]).jerarquizar() + Carta(ManoCPU.decir_cartas()[0]).jerarquizar()) >= 18:
					return True
				else:
					return False
			else:
				if Carta(ManoCPU.mayor_carta()).jerarquizar() >= 9:
					return True
				else:
					return False

	elif manos[2] == None:
		if jugador_cartademas == True:
			if Carta(cartas_tiradas_CPU[2]).jerarquizar() >= 9:
				return True
			else:
				return False
		elif jugador_cartademas == None or False:
			if (Carta(ManoCPU.mayor_carta()).jerarquizar() >= 9):
				return True
			else:
				return False
	

#################------ENVIDO


def cantar_envido(tanto, modificador):
	#20--> 5 porciento de probabilidades, 27--> 80 porciento de probabilidades
	#33--> 100 porciento de probabilidades, curve fit con el graphmatica
	#y = -0.3463x^2 + 25.6468x - 366.2554 ' curve-fit for Data plot 1; r=0.9942, chi^2=57.793 after 24999 iterations
	
	
	#Modificador modifica las probabilidades
	probabilidad = -0.3463*(tanto**2) + 25.6468*tanto - 366.2554
	probabilidades = int(probabilidad*modificador/100)
	cantar = randomizacion_de_eventos(probabilidades)
	return cantar


def hablar_envido(mano):
	if mano == True:
		if envido_CPU >= envido_JUG:
			print '---> Tengo '+str(envido_CPU)+' y vos decis \"son buenas\". Gane.'
		else:
			print '---> Tengo '+str(envido_CPU)+' y vos '+str(envido_JUG)+'. Perdi.'
	elif mano == False:
		if envido_CPU >= envido_JUG:
			print '---> Tenes '+str(envido_JUG)+' y las mias son mejores: '+str(envido_CPU)+'. Gane.'
		else:
			print '---> Tenes '+str(envido_JUG)+' y digo \"son buenas\". Perdi.'


#################------INGRESAR MANO


def ingresar_mano():

	global ManoMIA, ManoCPU, envido_CPU, envido_JUG
	
	#Mezclo el mazo
	mazo_mezclado = Mazo
	random.shuffle(mazo_mezclado)
	
	#Reparto las cartas una y una
	cartaj1 = mazo_mezclado[0]
	cartaj2 = mazo_mezclado[2]
	cartaj3 = mazo_mezclado[4]
	
	cartacpu1 = mazo_mezclado[1]
	cartacpu2 = mazo_mezclado[3]
	cartacpu3 = mazo_mezclado[5]
	
	
	
	#Creo dos objetos, Mano
	ManoMIA = Mano(cartaj1, cartaj2, cartaj3)
	ManoCPU = Mano(cartacpu1, cartacpu2, cartacpu3)
	
	#Me fijo cuanto tiene la pc de envido
	envido_CPU = ManoCPU.tengo_envido()
	envido_JUG = ManoMIA.tengo_envido()

	print ManoMIA
	
	global Mano_Quien
	primera_mano(envido_CPU, Mano_Quien)
	
	#Cambia quien es mano
	Mano_Quien = not Mano_Quien
	##Hacer un while para las manos

ingresar_mano()
