##Truco
#Por Gonzalo Ciruelos
#Version 0.1 beta

from cartaymano import Mano, Carta, cartas_tiradas_MIA, cartas_tiradas_CPU

import random

manos = [2, 2, 2]

Mano_Quien = bool(random.randint(0,1))			#Si va la pc True, si va el jugador False



carta_del_otro = []
#tanto_del_otro = 0

envido_hecho = 0
truco_hecho = 0

ManoCPU = Mano()
ManoMIA = Mano()

Palos =	['Oro', 'Espada', 'Copa', 'Basto'] 
Numeros = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]	
Mazo = []
for palo in Palos:
	for numero in Numeros:
		Mazo.append([numero,palo])


#################------JUEGO


def jugar(tanto, mano):

	global manos, mis_cartas_tiradas, cartas

	posibles = []
	maximo = 15


	if mano==False:			#Va el jugador
		envido(mano, tanto) ###Ahora tendria que preguntar si quiere cantar envido
		carta_del_jugador = Carta(carta_del_oponente())
		for carta in ManoCPU.decir_cartas():
			carta = Carta(carta)							#Se fija si alguna carta esta entre x y x+3
			if carta.jerarquizar() > carta_del_jugador.jerarquizar() and carta.jerarquizar() < (carta_del_jugador.jerarquizar()+3):
				posibles.append(carta)
				for carta in posibles:					#Elije la menor de esas cartas
					if carta.jerarquizar() < maximo:
						maximo = carta.jerarquizar()
				for carta2 in ManoCPU.decir_cartas():					#Busca esa carta en la lista 'cartas', la imprime y la borra
					if Carta(carta2).jerarquizar() == maximo:
						ManoCPU.tirar_carta(carta2)
		if posibles == []:
			for carta in ManoCPU.decir_cartas():					#Elije la menor de todas las cartas
				if carta.jerarquizar() < maximo:
					maximo = carta.jerarquizar()
			for carta2 in ManoCPU.decir_cartas():					#Busca esa carta en la lista 'cartas', la imprime y la borra
				if carta2.jerarquizar() == maximo:
					ManoCPU.tirar_carta(carta2)
	else:			#Va la pc
		envido(mano, tanto)
		valor_mayor_carta = Carta(ManoCPU.mayor_carta()).jerarquizar()
		valor_media_carta = Carta(ManoCPU.media_carta()).jerarquizar()
		valor_menor_carta = Carta(ManoCPU.menor_carta()).jerarquizar()
		
		if valor_mayor_carta > 10:													#Si la mayor carta es mas grande que un 3, 
			if valor_media_carta >= 10:											#y la segunda mayor carta tambien, tira la segunda mayor
				ManoCPU.tirar_carta(ManoCPU.media_carta())
			else:															#si no, tira la mas baja
				ManoCPU.tirar_carta(ManoCPU.menor_carta())
		elif valor_mayor_carta == 10:												#Si la carta mas alta es un 3
			if valor_menor_carta+valor_media_carta >= (valor_mayor_carta-2):					#y si las otras dos son masomenos buenas, tira el 3
				ManoCPU.tirar_carta(ManoCPU.mayor_carta())
			elif cvalor_menor_carta+valor_media_carta < (valor_mayor_carta-2):				#si no tira la mas baja !!!CAMBIAR POR UN ELSE
				ManoCPU.tirar_carta(ManoCPU.menor_carta())
		elif valor_mayor_carta < 10:													#Si todas son mas chicas que 3 tira una al azar
			#r=random.randint(1,3)
			ManoCPU.tirar_carta(ManoCPU.menor_carta())
		envido(False, tanto)
		carta_del_oponente()
	
	manos[0] = 1
	
	if Carta(cartas_tiradas_MIA[0]).jerarquizar() > Carta(cartas_tiradas_CPU[0]).jerarquizar():
		segunda_mano('jugador')
	elif Carta(cartas_tiradas_MIA[0]).jerarquizar() < Carta(cartas_tiradas_CPU[0]).jerarquizar():
		segunda_mano('cpu')
	elif Carta(cartas_tiradas_MIA[0]).jerarquizar() == Carta(cartas_tiradas_CPU[0]).jerarquizar():
		segunda_mano('parda')


def truco(quienlocanta, pasar = 0):
	
	global truco_hecho
	
	if quienlocanta == 'yo':
		if truco_utilidad() == True:
			if truco_hecho == 0:
				print 'Canta truco'
				truco_hecho += 1
			elif truco_hecho == 1:
				print 'Canta retruco'
				truco_hecho += 1
			elif truco_hecho == 3:
				print 'Canta vale cuatro'
				truco_hecho += 1
			respuesta = raw_input('Quiso, no quiso o retruco? (S/n/R) ')
			if respuesta == 'S':
				pass
			elif respuesta == 'n':
				exit()
			else:
				truco('el', 1)
		else:
			pass
				
	elif quienlocanta == 'el':
		if pasar == 0:
			if raw_input('Canto truco? (S/n) ') == 'S':
				if truco_utilidad == True:
					print 'Quere'
				else:
					print 'No quieras'
					exit()
		elif pasar == 1:
			if truco_utilidad() == True:
				print 'Quere'
			else:
				print 'No quieras'
				exit()


def envido(soymano, tanto):
	
	global envido_hecho
	
	if envido_hecho == 0:
		
		if soymano == True:
			if cantar_envido(tanto, tanto) == True:
				print '---> Real envido\n---> Queres? (S/n)'
				envido_hecho = 1
			else:
				if cantar_envido(tanto, 100) == True:
					print '---> Envido\n---> Queres? (S/n)'
					envido_hecho = 1
				#else:
				#	print 'No cantes nada'
		else:
			canto_envido = raw_input('Queres cantar envido? (S/n) ')
			
			if canto_envido == 'S' or canto_envido == 's':
				if cantar_envido(tanto, tanto) == True:
					print '---> Envido'
					envido_hecho = 1
				else:
					if cantar_envido(tanto, 100) == True:
						print '---> Quiero'
						envido_hecho = 1
					else:
						print '---> No quiero'
			else:
				pass

	else:
		pass
		
		
def segunda_mano(quienva):
	maximo = 15
	
	global manos, mis_cartas_tiradas, cartas

	if quienva == 'el':
		truco('el')

		carta_del_oponente()
		if cartas[0][2] > carta_del_otro[2]:				#Se fija si alguna carta es mayor que x
			print 'Tira ', cartas[0]
			mis_cartas_tiradas[1] = cartas[0]
			cartas.remove(cartas[0])						
		elif cartas[1][2] > carta_del_otro[2]:
			print 'Tira ', cartas[1]
			mis_cartas_tiradas[1] = cartas[1]
			cartas.remove(cartas[1])
		else: print 'Perdiste'		
		
	elif quienva == 'yo':
		truco('yo')
		if cartas[1][2] >= 10:
			print 'Tira ', cartas[0]
			mis_cartas_tiradas[1] = cartas[0]
			cartas.remove(cartas[0])
		else:
			print 'Tira ', cartas[0]
			mis_cartas_tiradas[1] = cartas[0]
			cartas.remove(cartas[0])
		truco('el')
		carta_del_oponente()
	else:
		print 'Tira ', cartas[1]
		mis_cartas_tiradas[1] = cartas[1]
		cartas.remove(cartas[1])
		truco('el')
		carta_del_oponente()
	
	manos[1] = 1
	
	if mis_cartas_tiradas[1][2] > carta_del_otro[2]:
		manos[1] = True
		tercera_mano('yo')
	elif mis_cartas_tiradas[1][2] < carta_del_otro[2]:
		manos[1] = False
		tercera_mano('el')
	elif mis_cartas_tiradas[1][2] == carta_del_otro[2]:
		manos[1] = None
		tercera_mano('parda')
		

def tercera_mano(quienva):
	
	if quienva == 'el':
		truco('el')
		carta_del_oponente()
					
		if cartas[0][2] > carta_del_otro[2]:
			print 'Tira ', cartas[0]
			mis_cartas_tiradas[1] = cartas[0]
			cartas.remove(cartas[0])				
		else: 
			print 'Perdiste'
			exit()		
		
	elif quienva == 'yo':
		truco('yo')
			
		if cartas[0][2] >= 10:
			print 'Tira ', cartas[0]
			mis_cartas_tiradas[2] = cartas[0]
			cartas.remove(cartas[0])
			truco('el')
			carta_del_oponente()
	
	else:
		print 'Tira ', cartas[0]
		mis_cartas_tiradas[2] = cartas[0]
		cartas.remove(cartas[0])
		truco('el')
		carta_del_oponente()


#################------CARTAS


def carta_del_oponente():
	cartadeljugador = raw_input('Que carta queres tirar? ')
	lacarta = cartadeljugador.split(' de ')
	lacarta[0] = int(lacarta[0])
	global ManoMIA
	if lacarta in ManoMIA.decir_cartas():
		ManoMIA.tirar_carta(lacarta, 'jugador')
	else:
		print ' Ingresa una carta que tengas'
	return lacarta


#################------UTILIDADES


def randomizacion_de_eventos(probabilidad):
	azar = random.randint(1, 100)
	if azar <= probabilidad:
		return True
	else: 
		return False


#################------TRUCO


def truco_utilidad():
	
	if manos[1] == 0:
		if manos[0] == True and cartas[1][2] >= (9+truco_hecho):
			return True
		elif manos[0] == False:
			if cartas[1][2]+cartas[0][2] >= 18:
				return True
		else:
			return False

	elif manos[2] == 0:
		if cartas[0][2] >= (9+truco_hecho):
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


#################------INGRSAR MANO


def ingresar_mano():

	global ManoMIA, ManoCPU
	
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
	envido = ManoCPU.tengo_envido()

	print ManoMIA
	
	global Mano_Quien
	jugar(envido, Mano_Quien)
	
	#Cambia quien es mano
	Mano_Quien = not Mano_Quien
	##Hacer un while para las manos


ingresar_mano()
