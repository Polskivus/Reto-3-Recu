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
        #Estos dos atributos comprueban si esta saltando y si esta en el suelo
        self.saltando = False
        self.en_suelo = True
        #Velocidad en el eje Y
        self.velocidad_y = 0
        #Direccion a la que esta mirando 0 izq y 1 derecha
        self.direccion = 1

        self.rect = self.imagen.get_rect()
        self.rect.midbottom = (SCREEN_WIDTH / 2, SCREEN_HEIGHT)

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def draw(self,surface):
        surface.blit(self.imagen, self.rect)

    def update(self, dt, bloques):
        self.control_input(dt)
        self.aplicar_gravedad(dt)
        self.check_colisiones(bloques)
        self.actualizar_img()
    
    def control_input(self, dt):
        tecla_pulsada = pygame.key.get_pressed()

        if self.rect.left > 0 and tecla_pulsada[K_a]:
            self.x -= VELOCIDAD * dt
            self.direccion = 0
        if self.rect.right < SCREEN_WIDTH and tecla_pulsada[K_d]:
            self.x += VELOCIDAD * dt
            self.direccion = 1
        if tecla_pulsada[K_SPACE] and not self.saltando and self.en_suelo:
            self.saltando = True
            self.velocidad_y = -400
    
    def aplicar_gravedad(self, dt):
        if not self.en_suelo:
            tecla_pulsada = pygame.key.get_pressed()
            if self.velocidad_y > 0:
                self.velocidad_y += GRAVEDAD * 2 * dt
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

    def check_colisiones(self, bloques):
        self.rect.x = int(self.x)
        for bloque in pygame.sprite.spritecollide(self, bloques, False):
            if self.rect.centerx < bloque.rect.centerx:
                self.rect.right = bloque.rect.left
            else:
                self.rect.left = bloque.rect.right
            self.x = float(self.rect.x)
        
        self.rect.y = int(self.y)
        rect_pies = pygame.Rect(self.rect.x, self.rect.bottom - 2, self.rect.width, 4)
        self.en_suelo = rect_pies.bottom >= SCREEN_HEIGHT

        for bloque in bloques:
            if rect_pies.colliderect(bloque.rect) and self.velocidad_y >= 0:
                self.rect.bottom = bloque.rect.top
                self.y = float(self.rect.y)
                self.saltando = False
                self.velocidad_y = 0
                self.en_suelo = True
            elif self.rect.colliderect(bloque.rect) and self.velocidad_y < 0:
                self.rect.top = bloque.rect.bottom
                self.y = float(self.rect.y)
                self.velocidad_y = 0

    def actualizar_img(self):
        img_base = self.imagen_salto if self.saltando else self.imagen_normal
        self.imagen = pygame.transform.flip(img_base, self.direccion == 0, False)

    def mostrar_hitbox(self, surface):
        pygame.draw.rect(surface, (0,0,0), self.rect, 2)

        rect_pies = pygame.Rect(self.rect.x, self.rect.bottom - 2, self.rect.width, 4)
        pygame.draw.rect(surface, (0,0,0), rect_pies, 2)


"""

PRIMERA VERSION ESTA TO-DO METIDO EN UPDATE ME PARECIA FEO ASI QUE HE CAMBIADO PARA QUE 
CADA COSA VAYA INDIVIDUALMENTE Y EL UPDATE LAS RECOGA PARA EJECUTAR

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

"""