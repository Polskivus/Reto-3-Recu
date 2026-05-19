import pygame
from pygame.locals import *
from pygame.sprite import RenderUpdates
from personaje import PJ
from bloque import Bloque
from botones import ElementoUI
from config import *


def main():
    pygame.init()

    pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF)
    estado = estadoJuego.PRINCIPAL

    while True:

        if estado == estadoJuego.PRINCIPAL:
            estado = pantalla_principal(pantalla)

        if estado == estadoJuego.NUEVO_JUEGO:
            jugador = PJ()
            estado = nivel_1(pantalla, jugador)

        if estado == estadoJuego.SALIR:
            pygame.quit()
            return
        
def pantalla_principal(pantalla):
    boton_ini = ElementoUI(
        posicion_central=(400, 400),
        font_size=30,
        bg_rgb=AZUL,
        text_rgb=ROJO,
        text="Start",
        action=estadoJuego.NUEVO_JUEGO,
    )

    boton_sal = ElementoUI(
        posicion_central=(400, 500),
        font_size=30,
        bg_rgb=ROJO,
        text_rgb=AZUL,
        text="Quit",
        action=estadoJuego.SALIR,
    )

    botones_inicio = RenderUpdates(boton_ini, boton_sal)
    return loop_principal(pantalla, botones_inicio, None, None)

def nivel_1(pantalla, jugador):
    bloque1 = Bloque(
        posicion_central=(600,600),
        ancho=50,
        alto=7,
        color=ROJO
    )

    bloque2 = Bloque(
        posicion_central=(200,200),
        ancho=50,
        alto=7,
        color=AZUL
    )

    boton_sal2 = ElementoUI(
        posicion_central=(900, 100),
        font_size=30,
        bg_rgb=ROJO,
        text_rgb=AZUL,
        text="Quit",
        action=estadoJuego.SALIR,
    )

    bloques_nivel = RenderUpdates(bloque1,bloque2)
    boton = RenderUpdates(boton_sal2)
    return loop_principal(pantalla, boton, bloques_nivel, jugador)



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