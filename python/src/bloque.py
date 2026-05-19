import pygame

def crearBloque(ancho, alto, color):
    plataforma = pygame.Surface((ancho,alto))
    plataforma.fill(color)
    return plataforma.convert_alpha()


class Bloque(pygame.sprite.Sprite):

    def __init__(self, posicion_central, ancho, alto, color):

        super().__init__()

        bloque_normal = crearBloque(
            ancho=ancho, alto=alto, color=color
        )

        self.imagen = bloque_normal
        self.rect = bloque_normal.get_rect(center=posicion_central)

    def draw(self, surface):
        surface.blit(self.imagen, self.rect)
    
    def mostrar_hitbox(self, surface):
        pygame.draw.rect(surface, (0,0,0), self.rect, 2)

"""
    self.esta_encima = False
    self.image = pygame.Surface((ancho, alto))
    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y)
"""