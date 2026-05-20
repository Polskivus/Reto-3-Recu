from pygame.sprite import RenderUpdates
from botones import ElementoUI
from bloque import Bloque
from config import *

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
    return botones_inicio


def nivel_1(pantalla, jugador):
    bloque1 = Bloque(
        posicion_central=(600,400),
        ancho=150,
        alto=25,
        color=ROJO
    )

    bloque2 = Bloque(
        posicion_central=(200,200),
        ancho=50,
        alto=7,
        color=AZUL
    )

    boton_sal2 = ElementoUI(
        posicion_central=(1200, 50),
        font_size=30,
        bg_rgb=ROJO,
        text_rgb=AZUL,
        text="X",
        action=estadoJuego.SALIR,
    )

    bloques_nivel = RenderUpdates(bloque1,bloque2)
    boton = RenderUpdates(boton_sal2)
    return bloques_nivel, boton
