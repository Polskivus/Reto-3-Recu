import pygame
import pygame.freetype
from pygame.sprite import Sprite

def crearSuperficieConTexto(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont("comicsansms", font_size, bold=True)
    #La _ hace referencia a que el "segundo resultado" se ignore
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

class ElementoUI(Sprite):

    def __init__(self, posicion_central, text, font_size, bg_rgb, text_rgb, action=None):

        self.mouse_over = False

        default_image = crearSuperficieConTexto(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        imagen_resaltada = crearSuperficieConTexto(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        self.imagenes = [default_image, imagen_resaltada]
        self.rects = [
            default_image.get_rect(center=posicion_central),
            imagen_resaltada.get_rect(center=posicion_central)
        ]

        self.action = action

        super().__init__()
    
    @property
    def image(self):
        return self.imagenes[1] if self.mouse_over else self.imagenes[0]
    
    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]
    
    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over=True
            if mouse_up:
                return self.action
        else:
            self.mouse_over=False

    def draw(self, surface):
        surface.blit(self.image, self.rect)