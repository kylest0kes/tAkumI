import pygame
import neat

pygame.init()
size = (1920, 1080)  # Width, Height
screen = pygame.display.set_mode(size)
track = pygame.image.load('./assets/map.png')
track = pygame.transform.scale(track, size)
pygame.display.set_caption("tAkumI")
screen.blit(track, (0, 0))
pygame.display.update()

running = True

while running:
        for e in pygame.event.get():
                    if e.type == pygame.QUIT:   
                            running = False

pygame.quit()