import pygame
from pygame.locals import *
from niveles import pantalla_principal, nivel_1
from personaje import PJ
from config import *


def main():
    pygame.init()

    pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF)
    estado = estadoJuego.PRINCIPAL

    while True:

        if estado == estadoJuego.PRINCIPAL:
            botones = pantalla_principal(pantalla)
            estado = loop_principal(pantalla, botones, None, None)
            

        elif estado == estadoJuego.NUEVO_JUEGO:
            jugador = PJ()
            bloques, boton = nivel_1(pantalla, jugador)
            estado = loop_principal(pantalla, boton, bloques, jugador)

        elif estado == estadoJuego.SALIR:
            pygame.quit()
            return

def loop_principal(pantalla, botones_inicio, bloques, jugador):
    reloj = pygame.time.Clock()
    while True:
        mouse_up = False
        dt = reloj.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        pantalla.fill(CASIMARRON)

        if botones_inicio:
            for boton in botones_inicio:
                accion_ui = boton.update(pygame.mouse.get_pos(), mouse_up)
                if accion_ui is not None:
                    return accion_ui
            botones_inicio.draw(pantalla)
        
        if bloques:
            for bloque in bloques:
                bloque.draw(pantalla)
        
        if jugador:
            jugador.update(dt, bloques)
            jugador.draw(pantalla)

        pygame.display.flip()

if __name__ == "__main__":
    main()

'''
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
'''