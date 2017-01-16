"""
Juego de memoria - Jacob Cornejo jacob@oddseed.com
"""
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

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

class Carta(Button):
    def __init__(self,valor, *args, **kwargs):
        super(Carta, self).__init__(*args, **kwargs)
        self.id = valor
        self.estaBocaAbajo = True
        self.seEncotroPareja = False
        self.indice_widget = None

    def ver(self):
        g =self.parent.GAME
        n = int(self.id)
        if self.estaBocaAbajo:
            self.text='?'
            self.background_color, self.color = [1, 1, 1, 1],[1, 1, 1, 1]

        else:
            color_bg = g.patrones[n-1][0]
            color_fn = g.patrones[n-1][1]
            caracter = g.patrones[n-1][2]
            background_color=COLORES[color_bg:color_bg+1][0]
            color=COLORES[color_fn:color_fn+1][0]
            self.text=caracter
            self.background_color=COLORES[color_bg:color_bg+1][0]
            self.color=COLORES[color_fn:color_fn+1][0]

    def press(self,carta):
        g =self.parent.GAME
        g.voltearCarta(self.indice_widget)
        self.ver()



class Game:
    def __init__(self,cant_de_parejas):
        self.cant_de_parejas = cant_de_parejas
        self.deck = []
        self.seleccion = []
        self.n_turno = 0
        self.game_over = False

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
                carta_ins = Carta(valor=str(numero),text='?',font_size=200,bold=True)
                carta_ins.bind(on_press=carta_ins.press)
                self.deck.append(carta_ins)

    def voltearBocaAbajoTodasLasCartas(self,test):
        print test
        for carta in self.deck:
            if not carta.seEncotroPareja:
                carta.estaBocaAbajo = True
                carta.ver()


    def turno(self):
        from kivy.clock import Clock
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
                Clock.schedule_once(self.voltearBocaAbajoTodasLasCartas, 5)

    def generarPatrones(self):
        from random import choice
        posibles_caracteres = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        posibles_colores = range(10)
        posibles_figuras = range(10)
        self.patrones = []
        while len(self.patrones) < self.cant_de_parejas:
            self.patrones.append((choice(posibles_colores),   #Color de fondo
                                  choice(posibles_colores),   #Color de fuente
                                  choice(posibles_caracteres) #Caracter
                                ))
            self.patrones = list(set(self.patrones))

    def barajearCartas(self):
        from random import shuffle
        shuffle(self.deck)

if __name__ == '__main__':
    class MemoriaApp(App):
        def build(self):
            layout = GridLayout(cols=5)
            layout.GAME = Game(10)
            layout.GAME.prepararJuego()
            i = 0
            for carta in layout.GAME.deck:
                carta.indice_widget = i
                layout.add_widget(carta)
                i +=1
            return layout

    MemoriaApp().run()