import pygame
import random


pygame.init()
sizes = pygame.display.get_desktop_sizes()
X, Y = sizes[0][0], sizes[0][1]
mw = pygame.display.set_mode((X, Y), pygame.SRCALPHA)
pygame.display.set_caption('race')
clock = pygame.time.Clock()

w_background = pygame.Surface((X, Y))
w_hills = pygame.Surface((X, Y * 0.5))
w_cars = pygame.Surface((X, Y * 0.4))

w_cars.set_colorkey((255, 255, 255), pygame.RLEACCEL)

running_game = True
FPS = 60

for i in range(1, 7):
    exec(f'a{i} = pygame.transform.scale(pygame.image.load("a{i}.png").convert_alpha(), (X, Y))')

sprite_background = pygame.image.load('background.png').convert_alpha()
sprite_background = pygame.transform.scale(sprite_background, (X, Y))

x_background, y_background = 0, 0

sprite_ground = pygame.image.load('ground.png').convert_alpha()
sprite_ground = pygame.transform.scale(sprite_ground, (X, Y * 0.5))

sprite_road = pygame.image.load('road5.png').convert_alpha()
sprite_road = pygame.transform.scale(sprite_road, (X * 0.5, Y * 0.5))

sprite_car11 = pygame.image.load('car11.png').convert_alpha()
sprite_car11 = pygame.transform.scale(sprite_car11, (X * 0.2, Y * 0.3))
sprite_car12 = pygame.image.load('car12.png').convert_alpha()
sprite_car12 = pygame.transform.scale(sprite_car12, (X * 0.2, Y * 0.3))
sprite_car13 = pygame.image.load('car13.png').convert_alpha()
sprite_car13 = pygame.transform.scale(sprite_car13, (X * 0.2, Y * 0.3))

TEXTURES = {
    'car1': [sprite_car11, sprite_car12, sprite_car13]
}

CARS = []


class Car:
    def __init__(self, x, y, sprite, speed=2, max_speed=100, way=1, time=1):
        self.x, self.y = x, y
        self.sprite, self.speed, self.max_speed, self.way, self.time = sprite, speed, max_speed, way, time

    def move(self, x, y):
        if self.x >= X * 0.7:
            self.set_speed(-5)
            if x < 0:
                self.x += x
                turn(-2)
        elif self.x <= X * 0.1:
            self.set_speed(-5)
            if x > 0:
                self.x += x
                turn(2)
        else:
            if x > 0: turn(-2)
            else: turn(2)
            self.x += x
            self.y += y

        w_hills.blit(sprite_ground, (0, 0))
        # w_hills.blit(sprite_road, (X * 0.25, 0))

        w_cars.fill((255, 255, 255))
        w_cars.blit(player.sprite[player.way], (player.x, player.y))

        mw.blit(w_hills, (0, Y * 0.5))
        mw.blit(w_cars, (0, Y * 0.6))
        pygame.display.flip()

    def set_speed(self, speed):
        if self.speed + speed <= self.max_speed:
            self.speed += speed
        else:
            self.speed = self.max_speed
        if self.speed + speed < 1:
            self.speed = 0
        print(speed, self.speed)

    def set_max_speed(self, max_speed):
        self.max_speed = max_speed

    def set_way(self, way):
        self.way = way


class Player:
    def __init__(self):
        pass


class Animation(pygame.sprite.Sprite):
    def __init__(self, images, time_interval, index=0):
        super(Animation, self).__init__()
        self.images = images
        self.image = self.images[0]
        self.time_interval = time_interval
        self.index = index
        self.timer = 0

    def update(self, seconds, reverse=False):
        self.timer += seconds
        if self.timer >= self.time_interval:
            self.image = self.images[self.index]
            if reverse:
                self.image = pygame.transform.flip(self.image, True, False)
            self.index = (self.index + 1) % len(self.images)
            self.timer = 0


def game():
    global running_game

    mw.blit(sprite_background, (0, 0))
    mw.blit(sprite_road, (X * 0.3, Y * 0.5))
    mw.blit(player.sprite[0], (X * 0.4, Y * 0.6))

    while running_game:
        #print(clock.get_fps())
        if random.randint(0, 100) == 1:
            CARS.append(Car(random.randint(int(X * 0.4), int(X * 0.6)), random.randint(0, int(Y * 0.2)), TEXTURES['car1']))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()
            if event.type == pygame.QUIT:
                running_game = False

        keys = pygame.key.get_pressed()

        if keys:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player.set_speed(player.speed / player.time / 10)
                player.set_way(1)
                player.move(0, 0)

            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player.set_speed(-player.speed / player.time / 10)
                player.set_way(1)
                player.move(0, 0)

            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player.set_speed(-player.speed / player.time / 2 / 10)
                player.set_way(0)
                player.move(-10, 0)

            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player.set_speed(-player.speed / player.time / 2 / 10)
                player.set_way(2)
                player.move(10, 0)

        else:
            player.set_speed(-player.speed / player.time / 50)
            player.time = 1

        '''for car in CARS:
            w_cars.blit(car.sprite[car.way], (car.x, car.y))
        mw.blit(w_cars, (0, Y * 0.6))'''

        pygame.display.flip()
        clock.tick(FPS)


def pause():
    global running_game, running_game

    running_pause = True
    pause_menu = pygame.Rect((X * 0.3, Y * 0.2), (X * 0.4,  Y * 0.6))
    pause_resume = pygame.Rect((X * 0.35, Y * 0.25), (X * 0.3, Y * 0.1))
    pause_settings = pygame.Rect((X * 0.35, Y * 0.4), (X * 0.3, Y * 0.1))
    pause_exit = pygame.Rect((X * 0.35, Y * 0.55), (X * 0.3, Y * 0.1))

    while running_pause:
        pygame.draw.rect(mw, (100, 100, 100), pause_menu)
        pygame.draw.rect(mw, (200, 200, 200), pause_resume)
        pygame.draw.rect(mw, (200, 200, 200), pause_settings)
        pygame.draw.rect(mw, (200, 200, 200), pause_exit)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                xx, yy = event.pos

                if pause_resume.collidepoint(xx, yy):
                    running_pause = False

                elif pause_settings.collidepoint(xx, yy):
                    pass

                elif pause_exit.collidepoint(xx, yy):
                    running_pause = False

            if event.type == pygame.QUIT:
                running_pause = False
                running_game = False

        pygame.display.flip()
        clock.tick(FPS)

    mw.blit(w_background, (x_background, y_background))
    mw.blit(w_hills, (0, Y * 0.5))
    mw.blit(w_cars, (0, Y * 0.6))


def ride():
    w_hills.blit(road.image, (0, 0))
    w_hills.blit(sprite_road, (X * 0.25, 0))
    road.update(player.speed)


def turn(x):
    pass
    '''global x_background, y_background
    x_background += x / 2
    w_background.blit(sprite_background, (0, 0))
    mw.blit(w_background, (x_background, y_background))
    mw.blit(w_hills, (0, Y * 0.5))
    mw.blit(w_cars, (0, Y * 0.6))'''


player = Car(X * 0.4, Y * 0.1, TEXTURES['car1'], 5, 150)
road = Animation([a1, a2, a3, a4, a5, a6], 2000)
game()
