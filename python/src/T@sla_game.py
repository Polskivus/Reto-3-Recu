import pygame
from pygame.locals import *
import os

pygame.init()

#informacion de pantalla
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

VELOCIDAD = 300
GRAVEDAD = 120

pantalla = pygame.display.set_mode((1400, 800), pygame.DOUBLEBUF)
reloj = pygame.time.Clock()
ejecutando = True
dt = 0

pantalla.fill("white")

ruta_actual = os.path.dirname(__file__)

print(ruta_actual)

ruta_imagen_PJ = os.path.abspath(os.path.join(ruta_actual, '..', 'assets', 'img','Stick_man.png'))

print(ruta_imagen_PJ)

class PJ(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.imagen = pygame.image.load(ruta_imagen_PJ).convert_alpha()
            print(self.imagen.get_size())
        except pygame.error as e:
            print(f"No se pudo cargar la imagen: {ruta_imagen_PJ}")
            raise SystemExit(e)
        self.rect = self.imagen.get_rect()
        self.rect.midbottom = (pantalla.get_width() / 2, SCREEN_HEIGHT)
        print(self.rect)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self, dt):
        tecla_pulsada = pygame.key.get_pressed()

        if self.rect.top > 0:
            if tecla_pulsada[pygame.K_w]:
                self.y -= VELOCIDAD * dt
        if self.rect.bottom < SCREEN_HEIGHT:
            if tecla_pulsada[pygame.K_s]:
                self.y += VELOCIDAD * dt
        if self.rect.left > 0:
            if tecla_pulsada[pygame.K_a]:
                self.x -= VELOCIDAD * dt
        if self.rect.right < SCREEN_WIDTH:
            if tecla_pulsada[pygame.K_d]:
                self.x += VELOCIDAD * dt

        if self.rect.bottom < SCREEN_HEIGHT:
            self.y += GRAVEDAD * dt

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
    
    def draw(self,surface):
        surface.blit(self.imagen, self.rect)

P1 = PJ()

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
    
    dt = reloj.tick(60) / 1000
    
    pantalla.fill("white")
    P1.update(dt)
    P1.draw(pantalla)
    pygame.display.flip()

pygame.quit()