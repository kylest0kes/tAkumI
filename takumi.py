import pygame, math
import sys
import neat

W, H = 1920, 1080
RADAR_COLOR = (57, 255, 20)
COLLISION_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)
GEN = 0
TRACK_INDEX = 0
CARS = []

pygame.init()
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

##########################################################################################  

class Car:
    radars_on_global = False
    
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.center = [800 + self.w / 2, self.y + self.h / 2]
        self.alive = True
        self.distance = 0
        self.time = 0
        self.radars = []
        self.radars_on = False
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.image.load("./assets/cars/ae86.png").convert()
        self.surface = pygame.Surface((w, h), pygame.SRCALPHA)
        self.surface.blit(self.image, (0, 0))
        self.angle = -90
        self.speed = 0.9
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self):
        self.rect.topleft = (self.x, self.y)
        rotated = pygame.transform.rotate(self.surface, self.angle)
        surface_rect = self.surface.get_rect(topleft=self.rect.topleft)
        new_rect = rotated.get_rect(center=surface_rect.center)
        screen.blit(rotated, new_rect.topleft)

    def move(self):
        speed = 5.0

        self.x -= speed * math.sin(math.radians(self.angle))
        self.y -= speed * math.cos(math.radians(self.angle))

        self.center = [self.x + self.w / 2, self.y + self.h / 2]

        self.time += 1

    def check_radar(self, deg, track):
        length = 0
        max_len = 95

        while length <= max_len:
            x = int(
                self.rect.center[0]
                + math.cos(math.radians(self.angle + deg)) * length  # Adjust angle calculation
            )
            y = int(
                self.rect.center[1]
                - math.sin(math.radians(self.angle + deg)) * length  # Adjust angle calculation
            )

            if (
                0 <= x < track.surface.get_width()
                and 0 <= y < track.surface.get_height()
            ):
                pixel_color = track.surface.get_at((x, y))[:3]
                if pixel_color == COLLISION_COLOR:
                    break

            length += 1

        dist = int(
            math.sqrt(
                math.pow(x - self.rect.center[0], 2)
                + math.pow(y - self.rect.center[1], 2)
            )
        )
        self.radars.append(((x, y), dist))

    @classmethod
    def toggle_draw_radars(cls):
        cls.radars_on_global = not cls.radars_on_global
    
    def draw_radars(self, screen, track):
        if self.radars_on_global:
            pygame.draw.circle(screen, RADAR_COLOR, self.rect.center, 5)
        self.radars = []
        for deg in range(0, 181, 45):
            self.check_radar(deg, track)
            if self.radars_on_global:
                pygame.draw.line(
                    screen, RADAR_COLOR, self.rect.center, self.radars[-1][0], 2
                )

    def is_alive(self):
        return self.alive

    def eval_reward(self):
        if self.distance < 0:
            return 0  
        else:
            return self.distance / (19 / 2)

    def get_radar_data(self):
        radars = self.radars
        radar_values = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            # not entirely sure what the 30 in this correlates to. may need to look further
            radar_values[i] = int(radar[1] / 30)
        return radar_values

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
            trackArr[TRACK_INDEX]
        ).convert()
        self.rect = self.image.get_rect()
        self.surface = pygame.Surface((w, h))
        self.mask = pygame.mask.from_surface(self.image.convert())

    def update(self):
        center_x = round(self.x)
        center_y = round(self.y)
        self.rect = self.image.get_rect(topleft=(center_x, center_y))
        self.surface.blit(self.image, (0, 0))
        screen.blit(self.surface, self.rect)

class Button:
    def __init__(self, x, y, radius, text, cb, color, hover_color):
        self.x = x
        self.y = y
        self.radius = radius 
        self.text = text
        self.cb = cb 
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.hovered = False
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.current_color, (self.x, self.y), self.radius)
        font = pygame.font.Font(None, 32)
        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)

    def check_hover(self, mouse_pos):
        distance = math.sqrt((self.x - mouse_pos[0])**2 + (self.y - mouse_pos[1])**2)
        self.hovered = distance < self.radius
        return self.hovered
    
class Text:
    def __init__(self, text, font_size, position, color=(0, 0, 0), font=None):
        self.text = text
        self.font_size = font_size
        self.position = position
        self.color = color
        self.font = font or pygame.font.Font(None, self.font_size)
        self.update_surface()

    def update_surface(self):
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(topleft=self.position)

    def set_text(self, text):
        self.text = text
        self.update_surface()

    def set_position(self, position):
        self.position = position
        self.update_surface()

    def set_color(self, color):
        self.color = color
        self.update_surface()

    def draw(self, screen):
        screen.blit(self.surface, self.rect.topleft)

##########################################################################################  

def check_collision_with_background(surface, rect, bg_color):
    left_edge = rect.left
    right_edge = rect.right
    top_edge = rect.top
    bottom_edge = rect.bottom

    left_collision = any(
        surface.get_at((left_edge, y))[:3] == bg_color
        for y in range(top_edge, bottom_edge)
    )
    right_collision = any(
        surface.get_at((right_edge, y))[:3] == bg_color
        for y in range(top_edge, bottom_edge)
    )
    top_collision = any(
        surface.get_at((x, top_edge))[:3] == bg_color
        for x in range(left_edge, right_edge)
    )
    bottom_collision = any(
        surface.get_at((x, bottom_edge))[:3] == bg_color
        for x in range(left_edge, right_edge)
    )

    return left_collision or right_collision or top_collision or bottom_collision

def cycle_to_next_track():
    global TRACK_INDEX, GEN 
    TRACK_INDEX = (TRACK_INDEX + 1) % len(trackArr)
    GEN = 0
    start()

def cycle_to_prev_track():
    global TRACK_INDEX, GEN 
    TRACK_INDEX = (TRACK_INDEX - 1) % len(trackArr)
    GEN = 0
    start()
    
def toggle_car_radars(buttons):
    for car in CARS:
        car.toggle_draw_radars()
        
    toggle_btn_index = 2
    
    # Toggle the color of the third button based on the global state of car radars
    buttons[toggle_btn_index].current_color = (0, 255, 0) if Car.radars_on_global else (255, 0, 0)
    # Update the hover_color attribute based on the current state of car radars
    buttons[toggle_btn_index].hover_color = (0, 255, 20) if Car.radars_on_global else (255, 0, 20)
    
def intro_screen():
    screen.fill((255, 255, 255))
    # start_btn = Button(300, 300, 30, "start", start, (150, 150, 150), (200, 200, 200))
    # start_btn.draw(screen)
    
def main():
    intro = True
    game = False
    
    start_btn = Button(300, 300, 30, "start", start, (150, 150, 150), (200, 200, 200))

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if start_btn.check_hover((mouse_x, mouse_y)):
                    start_btn.cb()
                
                
        if intro:
            intro_screen()
            start_btn.draw(screen)
        elif game:
            start()

        pygame.display.update()

        if __name__ == "__main__":
            main()
    
def start():
    def run_sim(genomes, config):

        nn = []
        global CARS
        CARS  = []

        # create a new nn for each genome that are passed in
        for _, g in genomes:
            n = neat.nn.FeedForwardNetwork.create(g, config)
            nn.append(n)
            g.fitness = 0
            CARS.append(Car(875, 870, 19, 36))
        
        finish = FinishLine()
        track = Track(0, 0, W, H)
        clock = pygame.time.Clock()

        # track generations
        global GEN 
        GEN += 1

        # keep track of time passed
        time = 0
        
        texts = [
            Text("Cycle Between Tracks", 30, (600, 1010), TEXT_COLOR),
            Text("Toggle Radar", 30, (880, 1010), TEXT_COLOR),
            Text("Generation: ", 30, (1065, 1010), TEXT_COLOR),
            Text(str(GEN), 30, (1190, 1010), TEXT_COLOR),
            Text("Alive Total: ", 30, (1220, 1010), TEXT_COLOR)  
        ]
        
        buttons = [
            Button(570, 1020, 20, "<", cycle_to_prev_track, (150, 150, 150), (200, 200, 200)),
            Button(845, 1020, 20, ">", cycle_to_next_track, (150, 150, 150), (200, 200, 200)), 
            Button(1035, 1020, 15, "", Car.toggle_draw_radars, (255, 20, 0), (255, 20, 50))
        ]

        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for button in buttons:
                        if button.check_hover((mouse_x, mouse_y)):
                            button.cb()

            # get each cars actions
            for i, car in enumerate(CARS):
                data = nn[i].activate(car.get_radar_data())
                action = data.index(max(data))
                if action == 0:
                    car.angle += 10
                elif action == 1:
                    car.angle -= 10
                elif action == 2:
                    if car.speed >= 6:
                        car.speed -= 1
                else:
                    car.speed += 1

            alive = 0
            for i, car in enumerate(CARS):
                car.move()
                if check_collision_with_background(track.image, car.rect, COLLISION_COLOR):
                    car.alive = False
                if car.is_alive():
                    alive += 1
                    car.draw()
                    genomes[i][1].fitness += car.eval_reward()
                    g.fitness = car.eval_reward() / (time + 1)

            if alive == 0:
                break
            
            time += 1
            if time == 3200:
                break

            screen.fill((0, 0, 0))
            track.update()
            finish.update()

            for car in CARS:
                if car.is_alive():
                    car.draw()
                    car.draw_radars(screen, track)

            for button in buttons:
                if button.check_hover(pygame.mouse.get_pos()):
                    button.color = tuple(c - 20 for c in button.hover_color)
                else:
                    button.color = button.hover_color
                button.draw(screen)
                
            toggle_car_radars(buttons)
            
            for text in texts:
                text.draw(screen)
                
            alive_value = Text(str(alive), 30, (1335, 1010), TEXT_COLOR) 
            alive_value.draw(screen)
            
            pygame.display.flip()
            clock.tick(60)

    ##########################################################################################  

    if __name__ == "__main__":

        config_path = "./config.txt"
        config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path,
        )

        population = neat.Population(config)
        population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)
        
        population.run(run_sim, 1000)
        
main()