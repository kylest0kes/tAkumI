import pygame

from pygame.math import Vector2

from math import radians, tan, degrees, copysign

pygame.init()

width = 1920
height = 900
hWidth = width/2
hHeight = height/2

SURFACE = pygame.HWSURFACE | pygame.DOUBLEBUF
global screen
screen = pygame.display.set_mode((width, height), SURFACE)

time = pygame.time.Clock()
clock = pygame.time.Clock()

white = (255,255,255)
grey = (105,105,105)

class Race_car(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        x = 32.6
        y = 26.3
        self.pos = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = 0.0
        self.length = 4
        self.maxAcceleration = 10
        self.maxSteering = 50
        self.maxVelocity = 17
        self.brakeDeceleration = 20
        self.freeDeceleration = 6
        self.acceleration = 0.0
        self.steering = 0.0
        self.dt = clock.get_time() / 1000
        self.image = pygame.image.load('F1 Car1.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rotated = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.rotated.get_rect()

    def update(self):
        self.dt = clock.get_time() / 1000

        self.velocity += (self.acceleration * self.dt, 0)
        self.velocity.x = max(-self.maxVelocity, min(self.velocity.x, self.maxVelocity))

        if self.steering:
            turningRadius = self.length / tan(radians(self.steering))
            angular_velocity = self.velocity.x / turningRadius
        else:
            angular_velocity = 0

        self.pos += self.velocity.rotate(-self.angle) * self.dt
        self.angle += degrees(angular_velocity) * self.dt

        center_x = round(self.pos.x)
        center_y = round(self.pos.y)
        self.rotated = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.rotated.get_rect(center=(center_x, center_y))

        screen.blit(self.rotated, self.pos * 32 - (self.rect.width / 2, self.rect.height / 2))

    def controls(self):

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            if self.velocity.x < 0:
                self.acceleration = +self.brakeDeceleration
            self.acceleration += 400 * self.dt
        elif pressed[pygame.KEYDOWN]:
            if self.velocity.x < 0:
                self.acceleration = -self.brakeDeceleration
            else:
                self.acceleration -= 5 * self.dt
        elif pressed[pygame.K_SPACE]:
            if abs(self.velocity.x) > self.dt * self.brakeDeceleration:
                self.acceleration = -copysign(self.brakeDeceleration, self.velocity.x)
            else:
                self.acceleration = -self.velocity.x / self.dt
        else:
            if abs(self.velocity.x) > self.dt * self.freeDeceleration:
                self.acceleration = -copysign(self.freeDeceleration, self.velocity.x)
            else:
                if self.dt != 0:
                    self.acceleration = -self.velocity.x / self.dt
        self.acceleration = max(-self.maxAcceleration, min(self.acceleration, self.maxAcceleration))

        if pressed[pygame.K_RIGHT]:
            self.steering -= 400 * self.dt
        elif pressed[pygame.K_LEFT]:
            self.steering += 400 * self.dt
        else:
            self.steering = 0
        self.steering = max(-self.maxSteering, min(self.steering, self.maxSteering))


class Finish_Line(pygame.sprite.Sprite):
    def __init__(self, finish_image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(finish_image).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(1190, 803))

    def update(self):
        screen.blit(self.image, self.rect)

class Racetrack(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pygame.image.load('pixil mask.png')
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())
        self.rect = self.image.get_rect()

    def update(self):
        center_x = round(self.x)
        center_y = round(self.y)
        self.rect = self.image.get_rect(topleft=(center_x, center_y))
        screen.blit(self.image, self.rect)


finish = Finish_Line('FinishSt.jpg')
car = Race_car()
track = Racetrack(0,0,1920,1080)

track_image = pygame.image.load('pixil mask.png').convert_alpha()
track_mask = pygame.mask.from_surface(track_image)
track_rect = track_image.get_rect()

markings = pygame.image.load('markings (1).png')


def check_for_collisions():
    offset = (int(car.rect.x), int(car.rect.y))
    collide = track.mask.overlap(car.mask, offset)
    print(offset, collide)
    return collide

class Game:    # initialize game class
    def __init__(self):

        pygame.display.set_caption("2D Racer")

        self.running = True

    def run(self):

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            check_for_collisions()

            screen.fill(grey)
            track.update()
            finish.update()
            screen.blit(markings, (974, 812))
            car.update()
            car.controls()
            pygame.display.update()
            clock.tick(60)

        pygame.quit()


g = Game()

if __name__ == '__main__':
    game = Game()
    g.run()