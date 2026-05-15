import pygame
from pygame.locals import *
import os

pygame.init()

#informacion de pantalla
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

VELOCIDAD = 300
GRAVEDAD = 200

pantalla = pygame.display.set_mode((1400, 800), pygame.DOUBLEBUF)
reloj = pygame.time.Clock()
ejecutando = True
dt = 0

pantalla.fill("white")

ruta_actual = os.path.dirname(__file__)
ruta_imagen_PJ = os.path.abspath(os.path.join(ruta_actual, '..', 'assets', 'img','Stick_man.png'))

class PJ(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.imagen = pygame.image.load(ruta_imagen_PJ).convert_alpha()
        except pygame.error as e:
            print(f"No se pudo cargar la imagen: {ruta_imagen_PJ}")
            raise SystemExit(e)
        
        self.saltando = False
        self.velocidad_y = 0

        self.rect = self.imagen.get_rect()
        self.rect.midbottom = (pantalla.get_width() / 2, SCREEN_HEIGHT)

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self, dt):
        tecla_pulsada = pygame.key.get_pressed()

        if tecla_pulsada[pygame.K_SPACE] and not self.saltando:
            self.saltando = True
            self.velocidad_y = -400

        if self.velocidad_y > 0:
            self.velocidad_y += GRAVEDAD *2 * dt
        else:
            self.velocidad_y += GRAVEDAD * dt

        if self.velocidad_y < 0 and not tecla_pulsada[pygame.K_SPACE]:
            self.velocidad_y *= 0.5

        self.y += self.velocidad_y * dt

        if self.y + self.rect.height >= SCREEN_HEIGHT:
            self.y = float(SCREEN_HEIGHT - self.rect.height)
            self.saltando = False
            self.velocidad_y = 0

        if self.rect.left > 0:
            if tecla_pulsada[pygame.K_a]:
                self.x -= VELOCIDAD * dt
        if self.rect.right < SCREEN_WIDTH:
            if tecla_pulsada[pygame.K_d]:
                self.x += VELOCIDAD * dt

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