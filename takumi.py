import pygame, math
import neat

pygame.init()

size = (1920, 1080)  # Width, Height

screen = pygame.display.set_mode(size)

car_img = pygame.image.load('./assets/ae86.png')

track = pygame.image.load('./assets/map.png')
track = pygame.transform.scale(track, (1920, 980))
pygame.display.set_caption("tAkumI")

pygame.display.update()


class Car:
        def __init__(self, x, y, w, h):
                self.x = x
                self.y = y
                self.w = w
                self.h = h
                self.rect = pygame.Rect(x, y, h, w)
                self.surface = pygame.Surface((h, w), pygame.SRCALPHA)
                self.surface.blit(car_img, (0, 0))
                self.angle = -90
                self.speed = 0               

        def draw(self):
                self.rect.topleft = (self.x, self.y)
                rotated = pygame.transform.rotate(self.surface, self.angle)
                surface_rect = self.surface.get_rect(topleft = self.rect.topleft)
                new_rect = rotated.get_rect(center = surface_rect.center)
                screen.blit(rotated, new_rect.topleft)

car1 = Car(800, 800, 46, 19)
clock = pygame.time.Clock()

running = True
while running:
        for e in pygame.event.get():
                    if e.type == pygame.QUIT:   
                            running = False
        
        screen.fill((255, 255, 255))
        screen.blit(track, (0, 0))
        key_press = pygame.key.get_pressed()
        car1.speed *= 0.9

        if key_press[pygame.K_UP]: car1.speed += 0.5 
        if key_press[pygame.K_DOWN]: car1.speed -= 0.5 

        if key_press[pygame.K_LEFT]: car1.angle += car1.speed / 2 
        if key_press[pygame.K_RIGHT]: car1.angle -= car1.speed / 2 
        car1.x -= car1.speed * math.sin(math.radians(car1.angle)) 
        car1.y -= car1.speed * math.cos(math.radians(-car1.angle)) 
        
        car1.draw()
        pygame.display.flip()
        clock.tick(60) 

pygame.quit()        
