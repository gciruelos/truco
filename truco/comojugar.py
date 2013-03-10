
#		PRIMERA MANO ---> VA EL JUGADOR
#
#		for carta in ManoCPU.decir_cartas():
#			carta = Carta(carta)							#Se fija si alguna carta esta entre x y x+3
#			if carta.jerarquizar() > carta_del_jugador.jerarquizar() and carta.jerarquizar() < (carta_del_jugador.jerarquizar()+3):
#				posibles.append(carta)
#				for carta in posibles:					#Elije la menor de esas cartas
#					if carta.jerarquizar() < maximo:
#						maximo = carta.jerarquizar()
#				for carta2 in ManoCPU.decir_cartas():					#Busca esa carta en la lista 'cartas', la imprime y la borra
#					if Carta(carta2).jerarquizar() == maximo:
#						ManoCPU.tirar_carta(carta2)
#		if posibles == []:
#			carta = Carta(carta)
#			for carta in ManoCPU.decir_cartas():					#Elije la menor de todas las cartas
#				if carta.jerarquizar() < maximo:
#					maximo = carta.jerarquizar()
#			for carta2 in ManoCPU.decir_cartas():					#Busca esa carta en la lista 'cartas', la imprime y la borra
#				if carta2.jerarquizar() == maximo:
#					ManoCPU.tirar_carta(carta2)
