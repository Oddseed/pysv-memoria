"""
Juego de memoria - Jacob Cornejo jacob@oddseed.com
"""

MODO_DEBUG = True

def print_debug(mensaje,tag='INFO'):
	if tag != '':
		print '[{}] {}'.format(tag,mensaje)
	else:
		print mensaje

def rgb(r,g,b):
	try:
		assert r >= 0 and g >= 0 and b >= 0
		assert r <= 255 and g <= 255 and b <= 255
		return [r/255.,g/255.,b/255.,1]
	except AssertionError:
		return [1,1,1,1]


COLORES = [
	rgb(255, 0, 0),
	rgb(255, 128, 0),
	rgb(255, 255, 0),
	rgb(128, 255, 0),
	rgb(0, 255, 255),
	rgb(0, 128, 255),
	rgb(0, 0, 255),
	rgb(128, 0, 255),
	rgb(255, 0, 255),
	rgb(255, 0, 128),
]

class Carta:
	def __init__(self,valor):
		self.id = valor
		self.estaBocaAbajo = True
		self.seEncotroPareja = False

	def __str__(self):
		#if not self.estaBocaAbajo:
		return 'Carta('+str(self.id)+')'
		#else:
		#	return 'Carta(?)'

	def __repr__(self):
		#if not self.estaBocaAbajo:
		return 'Carta('+str(self.id)+')'
		#else:
		#	return 'Carta(?)'

class Game:
	def __init__(self,cant_de_parejas):
		self.cant_de_parejas = cant_de_parejas
		self.deck = []
		self.seleccion = []
		self.n_turno = 0
		self.game_over = False

	def __str__(self):
		return 'Juego('+str(self.deck)+')'

	def __repr__(self):
		return 'Juego('+str(self.deck)+')'

	def contarCartasBocaArriba(self):
		cantidad = 0
		index = 0
		for carta in self.deck:
			if not carta.estaBocaAbajo:
				cantidad += 1
				if not carta.seEncotroPareja:
					if len(self.seleccion) >= 2:
						if self.deck[self.seleccion[0]].id == self.deck[self.seleccion[1]].id:
							if MODO_DEBUG:
								print_debug('Se encontro pareja!') 
							self.deck[self.seleccion[0]].seEncotroPareja = True
							self.deck[self.seleccion[1]].seEncotroPareja = True
			index+=1
		return cantidad

	def voltearCarta(self,n):
		if MODO_DEBUG:
			print_debug('Se eligio: {}'.format(n))
		if len(self.seleccion) < 2:
			if n not in self.seleccion:
				self.seleccion.append(n)
		else:
			self.seleccion = [n]
		if self.deck[n].estaBocaAbajo:
			self.deck[n].estaBocaAbajo = False
			self.n_turno += 1
			self.turno()
			return True
		else:
			if MODO_DEBUG:
				print_debug('Ya estaba boca arriba: {}'.format(n),'WARNING')
			return False

	def prepararJuego(self):
		self.generarCartas()
		self.barajearCartas()
		self.generarPatrones()

	def generarCartas(self):
		for numero in range(1,self.cant_de_parejas+1):
			for x in range(2):
				self.deck.append(Carta(numero))

	def voltearBocaAbajoTodasLasCartas(self):
		for carta in self.deck:
			if not carta.seEncotroPareja:
				carta.estaBocaAbajo = True


	def turno(self):
		self.n_turno += 1
		cartas_boca_arriba = self.contarCartasBocaArriba()
		if cartas_boca_arriba == len(self.deck):
			self.game_over = True
			if MODO_DEBUG:
				print_debug('GAME OVER')
		else:
			if MODO_DEBUG:
				print_debug('Cartas boca arriba: {}'.format(cartas_boca_arriba))
				print_debug('Turno: {}'.format(self.n_turno))
				print_debug(self.deck,tag='')
			
			if len(self.seleccion) >= 2:
				self.seleccion = []
				self.voltearBocaAbajoTodasLasCartas()

	def generarPatrones(self):
		from random import choice
		posibles_caracteres = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
		posibles_colores = range(10)
		posibles_figuras = range(10)
		self.patrones = []
		while len(self.patrones) < self.cant_de_parejas:
			self.patrones.append((choice(posibles_colores),   #Color de fondo
								  choice(posibles_colores),   #Color de figura
								  choice(posibles_colores),   #Color de fuente
								  choice(posibles_figuras),   #Figura
								  choice(posibles_caracteres) #Caracter
								))
			self.patrones = list(set(self.patrones))

	def barajearCartas(self):
		from random import shuffle
		shuffle(self.deck)

if __name__ == '__main__':
	from kivy.app import App
	from kivy.uix.button import Button
	from kivy.uix.gridlayout import GridLayout
	class MemoriaApp(App):
		def build(self):
			g = Game(10)
			g.prepararJuego()
			layout = GridLayout(cols=5)
			for carta in g.deck:
				color_bg = g.patrones[carta.id-1][0]
				color_fg = g.patrones[carta.id-1][1]
				color_fn = g.patrones[carta.id-1][2]
				figura = g.patrones[carta.id-1][3]
				caracter = g.patrones[carta.id-1][4]
				layout.add_widget(Button(text=caracter,
										 background_color=COLORES[color_bg:color_bg+1][0],
										 color=COLORES[color_fn:color_fn+1][0],

				))

			return layout

	MemoriaApp().run()