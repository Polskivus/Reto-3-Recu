import pygame
from pygame.locals import *
import os
from config import *

class PJ(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.imagen_normal = pygame.image.load(ruta_imagen_PJ).convert_alpha()
            self.imagen_salto = pygame.image.load(ruta_imagen_PJ_salto).convert_alpha()
            self.imagen = self.imagen_normal
        except pygame.error as e:
            print(f"No se pudo cargar la imagen: {ruta_imagen_PJ}")
            raise SystemExit(e)
        
        self.saltando = False
        self.velocidad_y = 0
        self.en_suelo = True

        self.direccion = 1

        self.rect = self.imagen.get_rect()
        self.rect.midbottom = (SCREEN_WIDTH / 2, SCREEN_HEIGHT)

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self, dt, bloques):
        tecla_pulsada = pygame.key.get_pressed()
        
        rect_pies = pygame.Rect(self.rect.x, self.rect.bottom, self.rect.width, 2)
        self.en_suelo = rect_pies.bottom >= SCREEN_HEIGHT or any(
            rect_pies.colliderect(b.rect) for b in bloques
        )

        if tecla_pulsada[K_SPACE] and not self.saltando:
            self.saltando = True
            self.velocidad_y = -400

        if not self.en_suelo:
            if self.velocidad_y > 0:
                self.velocidad_y += GRAVEDAD *2 * dt
            else:
                self.velocidad_y += GRAVEDAD * dt

        if self.velocidad_y < 0 and not tecla_pulsada[K_SPACE]:
            self.velocidad_y *= 0.5

        self.y += self.velocidad_y * dt

        if self.y + self.rect.height >= SCREEN_HEIGHT:
            self.y = float(SCREEN_HEIGHT - self.rect.height)
            self.saltando = False
            self.velocidad_y = 0
            self.en_suelo = True

        if self.rect.left > 0:
            if tecla_pulsada[K_a]:
                self.x -= VELOCIDAD * dt
                self.direccion = 0
        if self.rect.right < SCREEN_WIDTH:
            if tecla_pulsada[K_d]:
                self.x += VELOCIDAD * dt
                self.direccion = 1

        imagen_base = self.imagen_salto if self.saltando else self.imagen_normal
        self.imagen = pygame.transform.flip(imagen_base, self.direccion == 0, False)
        
        self.rect.x = int(self.x)

        colisiones = pygame.sprite.spritecollide(self, bloques, False)
        for bloque in colisiones:
            if self.x < bloque.rect.left:
                self.rect.right = bloque.rect.left
                self.x = float(self.rect.x)
            elif self.x > bloque.rect.left:
                self.rect.left = bloque.rect.right
                self.x = float(self.rect.x)

        self.rect.y = int(self.y)

        colisiones = pygame.sprite.spritecollide(self, bloques, False)
        for bloque in colisiones:
            if self.velocidad_y >= 0:
                self.rect.bottom = bloque.rect.top
                self.y = float(self.rect.y)
                self.saltando = False
                self.velocidad_y = 0

    def draw(self,surface):
        surface.blit(self.imagen, self.rect)
