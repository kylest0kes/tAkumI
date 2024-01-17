from random import randint
import pygame, math
import neat
import os
# import sys

pygame.init()

win_size = (1920, 1080)  # Width, Height
screen = pygame.display.set_mode(win_size)

track_size = (1920, 980)

trackArr = [pygame.transform.scale(pygame.image.load(os.path.join("assets", "map.png")), track_size), pygame.transform.scale(pygame.image.load(os.path.join("assets", "map2.png")), track_size), pygame.transform.scale(pygame.image.load(os.path.join("assets", "map3.png")), track_size), pygame.transform.scale(pygame.image.load(os.path.join("assets", "map4.png")), track_size), pygame.transform.scale(pygame.image.load(os.path.join("assets", "map5.png")), track_size)]

# trackArr = ['./assets/map.png', './assets/map2.png', './assets/map3.png', './assets/map4.png', './assets/map5.png']
# track = pygame.image.load(trackArr[randint(0, len(trackArr) - 1)])
# track = pygame.transform.scale(track, (1920, 980))

track = trackArr[randint(0, len(trackArr)-1)]

pygame.display.set_caption("tAkumI")
pygame.display.update()

class Car:
        def __init__(self, x, y, w, h):
                self.x = x
                self.y = y
                self.w = w
                self.h = h
                self.image = pygame.image.load('./assets/ae86.png')
                self.rect = pygame.Rect(x, y, h, w)
                self.surface = pygame.Surface((h, w), pygame.SRCALPHA)
                self.surface.blit(self.image, (0, 0))
                self.angle = -90
                self.speed = 0   
                self.mask = pygame.mask.from_surface(self.image)            

        def draw(self):
                self.rect.topleft = (self.x, self.y)
                rotated = pygame.transform.rotate(self.surface, self.angle)
                surface_rect = self.surface.get_rect(topleft = self.rect.topleft)
                new_rect = rotated.get_rect(center = surface_rect.center)
                screen.blit(rotated, new_rect.topleft)

car1 = Car(800, 800, 36, 19)
clock = pygame.time.Clock()

running = True
while running:
        for e in pygame.event.get():
                    if e.type == pygame.QUIT:   
                            running = False
        
        # screen.fill((255, 255, 255))
        screen.blit(track, (0, 0))
        key_press = pygame.key.get_pressed()
        car1.speed *= 0.9

        if key_press[pygame.K_UP]: car1.speed += 0.8 
        if key_press[pygame.K_DOWN]: car1.speed -= 0.4 

        if key_press[pygame.K_LEFT]: car1.angle += car1.speed / .75
        if key_press[pygame.K_RIGHT]: car1.angle -= car1.speed / .75 
        car1.x -= car1.speed * math.sin(math.radians(car1.angle)) 
        car1.y -= car1.speed * math.cos(math.radians(-car1.angle)) 
        
        car1.draw()
        pygame.display.flip()
        clock.tick(60) 

pygame.quit()        
