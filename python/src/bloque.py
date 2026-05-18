import pygame

class Bloque(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto):
        super().__init__()
        self.image = pygame.Surface((ancho, alto))
        self.image.fill((139, 69, 19))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)