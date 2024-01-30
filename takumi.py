from random import randint
import pygame, math
import sys
import neat

pygame.init()

W, H = 1920, 1080

screen = pygame.display.set_mode((W, H))

trackArr = [
    "./assets/tracks/track1.png"
    "./assets/tracks/track2.png"
    "./assets/tracks/track3.png"
    "./assets/tracks/track4.png"
    "./assets/tracks/track5.png"
    "./assets/tracks/track6.png"
]

pygame.display.set_caption("tAkumI")
pygame.display.update()


class Car:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pygame.image.load("./assets/cars/ae86.png").convert()
        self.rect = pygame.Rect(x, y, h, w)
        self.surface = pygame.Surface((h, w), pygame.SRCALPHA)
        self.surface.blit(self.image, (0, 0))
        self.angle = -90
        self.speed = 0
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self):
        self.rect.topleft = (self.x, self.y)
        rotated = pygame.transform.rotate(self.surface, self.angle)
        surface_rect = self.surface.get_rect(topleft=self.rect.topleft)
        new_rect = rotated.get_rect(center=surface_rect.center)
        screen.blit(rotated, new_rect.topleft)
        
    def move(self):
        key_press = pygame.key.get_pressed()
        self.speed *= 0.9
        
        if key_press[pygame.K_UP]:
            self.speed += 0.8
        if key_press[pygame.K_DOWN]:
            self.speed -= 0.4

        if key_press[pygame.K_LEFT]:
            car.angle += self.speed / 0.75
        if key_press[pygame.K_RIGHT]:
            car.angle -= self.speed / 0.75
        
        car.x -= self.speed * math.sin(math.radians(car.angle))
        car.y -= self.speed * math.cos(math.radians(-car.angle))


class FinishLine:
    def __init__(self):
        self.image = pygame.image.load("./assets/finish.png").convert()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(810, 890))
        
    def update(self):
        screen.blit(self.image, self.rect)


class Track:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pygame.image.load(trackArr[randint(0, len(trackArr) - 1)]).convert_alpha()
        self.rect = self.image.get_rect()
        self.surface = pygame.Surface((h, w))
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())

    def update(self):
        center_x = round(self.x)
        center_y = round(self.y)
        self.rect = self.image.get_rect(topleft=(center_x, center_y))
        screen.blit(self.image, self.rect)

finish = FinishLine()
track = Track(0, 0, W, H)
car = Car(800, 900, 36, 19)   
clock = pygame.time.Clock()

# test code to display background mask
mask_overlay_surface = pygame.Surface((W, H), pygame.SRCALPHA)
mask_overlay_surface.fill((0, 255, 0, 255))  # Transparent background for overlay

# Set the alpha value for the masked area
mask_overlay_surface.fill((0, 255, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)



running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    screen.fill((255, 255, 255)) 
    track.update()
    finish.update()
    car.draw()
    car.move()
    # Blit the mask overlay onto the screen
    screen.blit(mask_overlay_surface, (0, 0))
    pygame.display.flip()
    clock.tick(60)


