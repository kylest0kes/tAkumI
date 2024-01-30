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
    "./assets/tracks/track6.png",
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
        self.alive = True
        self.distance = 0
        self.time = 0
        self.rect = pygame.Rect(x, y, h, w)
        self.image = pygame.image.load("./assets/cars/ae86.png").convert_alpha()
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

    def update_corners(self):
        self.corners = [
            (self.x, self.y),
            (self.x + self.w, self.y),
            (self.x, self.y + self.h),
            (self.x + self.w, self.y + self.h),
        ]

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
        self.image = pygame.image.load(
            trackArr[randint(0, len(trackArr) - 1)]
        ).convert_alpha()
        self.rect = self.image.get_rect()
        self.surface = pygame.Surface((h, w))
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())

    def update(self):
        center_x = round(self.x)
        center_y = round(self.y)
        self.rect = self.image.get_rect(topleft=(center_x, center_y))
        screen.blit(self.image, self.rect)

def check_collision_with_background(surface, rect, bg_color):
    # Get the four edges of the rectangle
    left_edge = rect.left
    right_edge = rect.right
    top_edge = rect.top
    bottom_edge = rect.bottom

    # Check collision for each edge
    left_collision = any(surface.get_at((left_edge, y))[:3] == bg_color for y in range(top_edge, bottom_edge))
    right_collision = any(surface.get_at((right_edge, y))[:3] == bg_color for y in range(top_edge, bottom_edge))
    top_collision = any(surface.get_at((x, top_edge))[:3] == bg_color for x in range(left_edge, right_edge))
    bottom_collision = any(surface.get_at((x, bottom_edge))[:3] == bg_color for x in range(left_edge, right_edge))

    return left_collision or right_collision or top_collision or bottom_collision


finish = FinishLine()
track = Track(0, 0, W, H)
car = Car(800, 870, 36, 19)
target_color = (255, 255, 255)
clock = pygame.time.Clock()

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
    
    if check_collision_with_background(track.image, car.rect, target_color):
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
