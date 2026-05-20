import pygame
from pygame.locals import *
from config import *
import glob, os

def cargar_frames(ruta_carpeta, factor=1.0):
    rutas = sorted(glob.glob(os.path.join(ruta_carpeta, "*.png")))

    frames = []
    for ruta in rutas:
        img = pygame.image.load(ruta).convert_alpha()
        if factor != 1.0:
            w, h = img.get_size()
            img = pygame.transform.scale(img, (int(w * factor), int(h * factor)))
        frames.append(img)
    return frames

class PJ(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            #self.imagen_normal = pygame.image.load(ruta_imagen_PJ).convert_alpha()
            #self.imagen_salto = pygame.image.load(ruta_imagen_PJ_salto).convert_alpha()
            #self.imagen = self.imagen_normal
            self.animaciones = {
                "idle": cargar_frames(ruta_quieto, factor=0.5),
                "caminar": cargar_frames(ruta_andar, factor=0.5),
                "saltar": cargar_frames(ruta_saltar, factor=0.5)
            }
        except pygame.error as e:
            print("No se pudo cargar las animaciones")
            raise SystemExit(e)
        #Este sera el estado inicial
        self.estado_anima = "idle"
        self.frame_actual = 0
        self.tiempo_acumulado = 0.0
        self.velocidad_anim = 0.1 

        self.imagen = self.animaciones["idle"][0]
        self.mask = pygame.mask.from_surface(self.imagen)

        #Estos dos atributos comprueban si esta saltando y si esta en el suelo
        self.saltando = False
        self.en_suelo = True
        #Velocidad en el eje Y
        self.velocidad_y = 0
        #Direccion a la que esta mirando 0 izq y 1 derecha
        self.direccion = 1
        self.moviendose = False

        self.rect = pygame.Rect(0, 0, ANCHO_HITBOX, ALTO_HITBOX)
        self.rect.midbottom = (SCREEN_WIDTH / 2, SCREEN_HEIGHT)

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def draw(self,surface):
        contenido_no_transparente = self.imagen.get_bounding_rect()
        img_rect = self.imagen.get_rect(midbottom=self.rect.midbottom)
        img_rect.y += img_rect.height - contenido_no_transparente.bottom
        surface.blit(self.imagen, img_rect)

    def update(self, dt, bloques):
        self.control_input(dt)
        self.aplicar_gravedad(dt)
        self.actualizar_img(dt)
        self.check_colisiones(bloques)

    def control_input(self, dt):
        tecla_pulsada = pygame.key.get_pressed()
        self.moviendose = False

        if self.rect.left > 0 and tecla_pulsada[K_a]:
            self.x -= VELOCIDAD * dt
            self.direccion = 0
            self.moviendose = True
        if self.rect.right < SCREEN_WIDTH and tecla_pulsada[K_d]:
            self.x += VELOCIDAD * dt
            self.direccion = 1
            self.moviendose = True
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
        rect_cabeza = pygame.Rect(self.rect.x, self.rect.top, self.rect.width, 4)
        self.en_suelo = rect_pies.bottom >= SCREEN_HEIGHT

        for bloque in bloques:
            if rect_pies.colliderect(bloque.rect) and self.velocidad_y >= 0:
                self.rect.bottom = bloque.rect.top
                self.y = float(self.rect.y)
                self.saltando = False
                self.velocidad_y = 0
                self.en_suelo = True
            elif rect_cabeza.colliderect(bloque.rect) and self.velocidad_y < 0:
                self.rect.top = bloque.rect.bottom
                self.y = float(self.rect.y)
                self.velocidad_y = 0

    def actualizar_img(self, dt):
        """
        img_base = self.imagen_salto if self.saltando else self.imagen_normal
        self.imagen = pygame.transform.flip(img_base, self.direccion == 0, False)
        self.mask = pygame.mask.from_surface(self.imagen)
        """
        if not self.en_suelo:
            nuevo_estado = "saltar"
        elif self.moviendose:
            nuevo_estado = "caminar"
        else:
            nuevo_estado = "idle"
        
        if nuevo_estado != self.estado_anima:
            self.estado_anima = nuevo_estado
            self.frame_actual = 0
            self.tiempo_acumulado = 0.0
        
        self.tiempo_acumulado += dt
        if self.tiempo_acumulado >= self.velocidad_anim:
            self.tiempo_acumulado -= self.velocidad_anim
            frames = self.animaciones[self.estado_anima]

            if self.estado_anima == "saltar":
                self.frame_actual = min(self.frame_actual + 1, len(frames) - 1)
            else:
                self.frame_actual = (self.frame_actual + 1) % len(frames)
        
        frame = self.animaciones[self.estado_anima][self.frame_actual]
        self.imagen = pygame.transform.flip(frame, self.direccion == 1, False)
        self.mask = pygame.mask.from_surface(self.imagen)

    def mostrar_hitbox(self, surface):
        pygame.draw.rect(surface, (0,0,0), self.rect, 2)
    """
        rect_cabeza = pygame.Rect(self.rect.x, self.rect.top, self.rect.width, 4)
        pygame.draw.rect(surface, (0,0,0), rect_cabeza, 2)

        rect_pies = pygame.Rect(self.rect.x, self.rect.bottom - 2, self.rect.width, 4)
        pygame.draw.rect(surface, (0,0,0), rect_pies, 2)
    """


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
