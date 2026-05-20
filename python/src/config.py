#Imports para la config
import os
from enum import Enum

#Pantalla
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 750

#Atributos del mundo
VELOCIDAD = 200
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
#ruta_imagen_PJ = os.path.abspath(os.path.join(ruta_actual, '..', 'assets', 'img','Stick_man.png'))
#ruta_imagen_PJ_salto = os.path.abspath(os.path.join(ruta_actual, '..', 'assets', 'img','Saltando.png'))
ruta_assets_robot = os.path.abspath(os.path.join(ruta_actual, '..', 'assets', 'img'))
ruta_andar = os.path.abspath(os.path.join(ruta_assets_robot, "walk"))
ruta_saltar = os.path.abspath(os.path.join(ruta_assets_robot, "jump"))
ruta_quieto = os.path.abspath(os.path.join(ruta_assets_robot, "idle"))

#Posibles estados de juego
class estadoJuego(Enum):
    SALIR = -1
    PRINCIPAL = 0
    NUEVO_JUEGO = 1