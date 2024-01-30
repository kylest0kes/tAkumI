from random import randint
import pygame, math
import sys
import neat

pygame.init()

W, H = 1920, 1080

screen = pygame.display.set_mode((W, H))

trackArr = [
    "./assets/tracks/track1.png",
    "./assets/tracks/track2.png",
    "./assets/tracks/track3.png",
    "./assets/tracks/track4.png",
    "./assets/tracks/track5.png",
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
        self.center = [800 + self.w / 2, 900 + self.y / 2]
        self.radars = [] 
        self.drawing_radars = [] 
        self.alive = True 
        self.distance = 0 
        self.time = 0 
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
            self.speed += 0.55
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
        self.rect = self.image.get_rect(topleft=(800, 833))
        
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
target_color = (255, 255, 255)
clock = pygame.time.Clock()

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    
    collision_point = (int(car.rect.x), int(car.rect.y))
    background_color_at_collision = track.image.get_at(collision_point)
    
    if background_color_at_collision == target_color:
        print("Collision detected!")
        running = False
        pygame.quit()
        sys.exit()
    
    screen.fill((255, 255, 255)) 
    track.update()
    finish.update()
    car.draw()
    car.move()
    pygame.display.flip()
    clock.tick(60)


