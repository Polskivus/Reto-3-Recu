import pygame

pygame.init()
pantalla = pygame.display.set_mode((1280, 720))
reloj = pygame.time.Clock()
ejecutando = True

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
    
    pantalla.fill("blue")

    pygame.display.flip()

    reloj.tick(60)

pygame.quit()