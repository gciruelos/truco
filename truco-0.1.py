##Truco
#Por Gonzalo Ciruelos
#Version 0.1 alpha

import random

manos = [2, 2, 2]

mis_cartas_tiradas = [0, 0, 0]

carta_del_otro = []
#tanto_del_otro = 0

cartas = [[], [], []]

envido_hecho = 0
truco_hecho = 0


#################------JUEGO


def jugar(tanto, mano):

  global manos, mis_cartas_tiradas, cartas

	posibles = []
	maximo = 15


	if mano == False:
		envido(mano, tanto)
		carta_del_oponente()
		for carta in cartas:							#Se fija si alguna carta esta entre x y x+3
			if carta[2] > carta_del_otro[2] and carta[2] < (carta_del_otro[2]+3):
				posibles.append(carta)
				for carta in posibles:					#Elije la menor de esas cartas
					if carta[2] < maximo:
						maximo = carta[2]
				for carta2 in cartas:					#Busca esa carta en la lista 'cartas', la imprime y la borra
					if carta2[2] == maximo:
						print 'Tira ', carta2
						mis_cartas_tiradas[0] = carta2
						cartas.remove(carta2)
		if posibles == []:
			for carta in cartas:					#Elije la menor de todas las cartas
				if carta[2] < maximo:
					maximo = carta[2]
			for carta2 in cartas:					#Busca esa carta en la lista 'cartas', la imprime y la borra
				if carta2[2] == maximo:
					print 'Tira ', carta2
					mis_cartas_tiradas[0] = carta2
					cartas.remove(carta2)
	else:
		envido(mano, tanto)
		if cartas[2][2] > 10:													#Si la mayor carta es mas grande que un 3, 
			if cartas[1][2] >= 10:											#y la segunda mayor carta tambien, tira la segunda mayor
				print 'Tira ', cartas[1]
				mis_cartas_tiradas[0] = cartas[1]
				cartas.remove(cartas[1])
			else:															#si no, tira la mas baja
				print 'Tira ', cartas[0]
				mis_cartas_tiradas[0] = cartas[0]
				cartas.remove(cartas[0])
		elif cartas[2][2] == 10:												#Si la carta mas alta es un 3
			if cartas[0][2] + cartas[1][2] >= (cartas[2][2]-2):					#y si las otras dos son masomenos buenas, tira el 3
				print 'Tira ', cartas[2]
				mis_cartas_tiradas[0] = cartas[2]
				cartas.remove(cartas[2])
			elif cartas[0][2]+cartas[1][2] < (cartas[2][2]-2):				#si no tira la mas baja
				print 'Tira ', cartas[0]
				mis_cartas_tiradas[0] = cartas[0]
				cartas.remove(cartas[0])
		elif cartas[2][2] < 10:													#Si todas son mas chicas que 3 tira una al azar
			#r=random.randint(1,3)
			print 'Tira ', cartas[0]
			mis_cartas_tiradas[0] = cartas[0]
			cartas.remove(cartas[0])
		envido(False, tanto)
		carta_del_oponente()
	
	manos[0] = 1
	
	if mis_cartas_tiradas[0][2] > carta_del_otro[2]:
		segunda_mano('yo')
	elif mis_cartas_tiradas[0][2] < carta_del_otro[2]:
		segunda_mano('el')
	elif mis_cartas_tiradas[0][2] == carta_del_otro[2]:
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
				print 'Canta real envido'
				envido_hecho = 1
			else:
				if cantar_envido(tanto, 100) == True:
					print 'Canta envido'
					envido_hecho = 1
				else:
					print 'No cantes nada'
		else:
			canto_envido = raw_input('Canto evido el otro? (S/n) ')
			
			if canto_envido == 'S' or canto_envido == 's':
				if cantar_envido(tanto, tanto) == True:
					print 'Canta envido'
					envido_hecho = 1
				else:
					if cantar_envido(tanto, 100) == True:
						print 'Quere'
						envido_hecho = 1
					else:
						print 'No quieras'
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
	cartadelotro = raw_input('Que carta tiro el otro? ')
	otro = cartadelotro.split(' ')
	otro.append(0)
	otro[2] = jerarquizacion_de_las_cartas(otro)
	global carta_del_otro
	carta_del_otro = otro


#################------UTILIDADES


def randomizacion_de_eventos(probabilidad):
	azar=random.randint(1, 100)
	if azar <= probabilidad:
		return True
	else: 
		return False


def jerarquizacion_de_las_cartas(carta):
	if int(carta[0]) == 1:
		if carta[1] == 'O' or carta[1] == 'C':
			return 8
		elif carta[1] == 'B':
			return 13
		elif carta[1] == 'E':
			return 14
	elif int(carta[0]) == 2:
		return 9
	elif int(carta[0]) == 3:
		return 10
	elif int(carta[0]) == 4:
		return 1
	elif int(carta[0]) == 5:
		return 2
	elif int(carta[0]) == 6:
		return 3
	elif int(carta[0]) == 7:
		if carta[1] == 'B' or carta[1] == 'C':
			return 4
		elif carta[1] == 'O':
			return 11
		elif carta[1] == 'E':
			return 12
	elif int(carta[0]) == 10:
		return 5
	elif int(carta[0]) == 11:
		return 6
	elif int(carta[0]) == 12:
		return 7
	else:
		print 'Hubo un error al ingresar las cartas, por favor hacelo de nuevo\n'
		ingresar_mano()


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
	

def suma_envido(n,m):
	if n>=10:
		n = 0
	if m>=10:
		m = 0
	return 20+n+m


def tengo_envido(cartas):
	
	palos = [cartas[0][1],cartas[1][1],cartas[2][1]]
	numeros = [int(cartas[0][0]),int(cartas[1][0]),int(cartas[2][0])]
	
	if palos[0]==palos[1]:
		return suma_envido(numeros[0], numeros[1])
	elif palos[1]==palos[2]:
		return suma_envido(numeros[1], numeros[2])
	elif palos[0]==palos[2]:
		return suma_envido(numeros[0], numeros[2])
	else:
		return 0



#################------INGRESAR MANO


def ingresar_mano():
	#Palos:		O(ro) E(spada) C(opa) B(asto) 
	#Numeros:	1 2 3 4 5 6 7 10 11 12
	print 'Escribir el numero, seguido de un espacio, seguido del palo.\nPor ejemplo 12 O, es el rey de oro; 1 E es el ancho de espadas.\nIngresarlas en orden creciente de valor \n'
	carta1 = raw_input('Ingresa una carta: ')
	carta2 = raw_input('Ingresa una carta: ')
	carta3 = raw_input('Ingresa una carta: ')
	mano = raw_input('Sos mano? (S/n): ')
	
	c1 = carta1.split(' ')
	c2 = carta2.split(' ')
	c3 = carta3.split(' ')
	
	envido=tengo_envido([c1, c2, c3])
	
	#Reasignacion del valor de las cartas, segun su valor
	c1.append(0)
	c2.append(0) 
	c3.append(0)
	
	c1[2] = jerarquizacion_de_las_cartas(c1)
	c2[2] = jerarquizacion_de_las_cartas(c2) 
	c3[2] = jerarquizacion_de_las_cartas(c3)
	
	#Traduzco la input de mano a true/false
	if mano == 'S' or mano == 's':
		man = True
	else: man = False
	
	print c1, c2, c3
	
	global cartas
	cartas[0] = c1
	cartas[1] = c2
	cartas[2] = c3
	
	jugar(envido, man)


ingresar_mano()
