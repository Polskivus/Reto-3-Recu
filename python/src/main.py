import pygame
from pygame.locals import *
from personaje import PJ
from bloque import Bloque
from config import *

pygame.init()

pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF)
reloj = pygame.time.Clock()
ejecutando = True

P1 = PJ()
bloques = pygame.sprite.Group()
bloques.add(Bloque(400,500, 300, 20))
bloques.add(Bloque(100, 500, 300, 20))

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == QUIT:
            ejecutando = False
    
    dt = reloj.tick(FPS) / 1000
    
    pantalla.fill("white")
    bloques.draw(pantalla)
    P1.update(dt, bloques)
    P1.draw(pantalla)
    pygame.display.flip()

pygame.quit()