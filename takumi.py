import pygame

pygame.init()
size = (1000, 800)  # Width, Height
screen = pygame.display.set_mode(size)
pygame.display.set_caption("tAkumI")

running = True

while running:
        for e in pygame.event.get():
                    if e.type == pygame.QUIT:   
                            running = False

pygame.quit()