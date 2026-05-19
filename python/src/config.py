#Imports para la config
import os
from enum import Enum

#Pantalla
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 750

#Atributos del mundo
VELOCIDAD = 300
GRAVEDAD = 200

#Colores basicos
ROJO = (255,0,0)
VERDE = (0,255,0)
AZUL = (0,0,255)
BLANCO = (255,255,255)
CASIMARRON = (225, 193, 110)

#Opcion debug
DEBUG = True

#Fotogramas por segundo
FPS = 60

#Rutas para las imagenes
ruta_actual = os.path.dirname(__file__)
ruta_imagen_PJ = os.path.abspath(os.path.join(ruta_actual, '..', 'assets', 'img','Stick_man.png'))
ruta_imagen_PJ_salto = os.path.abspath(os.path.join(ruta_actual, '..', 'assets', 'img','Saltando.png'))

#Posibles estados de juego
class estadoJuego(Enum):
    SALIR = -1
    PRINCIPAL = 0
    NUEVO_JUEGO = 1