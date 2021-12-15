import pygame
import random


pygame.init()
sizes = pygame.display.get_desktop_sizes()
X, Y = sizes[0][0], sizes[0][1]
mw = pygame.display.set_mode((X, Y))
pygame.display.set_caption('race')
clock = pygame.time.Clock()

w_background = pygame.Surface((X, Y))
w_hills = pygame.Surface((X, Y))
w_cars = pygame.Surface((X, Y))

running = True
FPS = 60


sprite_background = pygame.image.load('background.png').convert_alpha()
sprite_background = pygame.transform.scale(sprite_background, (X, Y))

sprite_road = pygame.image.load('road2.png').convert_alpha()
sprite_road = pygame.transform.scale(sprite_road, (X * 0.5, Y * 0.5))

sprite_car11 = pygame.image.load('car.png').convert_alpha()
sprite_car11 = pygame.transform.scale(sprite_car11, (X * 0.2, Y * 0.1))
sprite_car12 = pygame.image.load('car.png').convert_alpha()
sprite_car12 = pygame.transform.scale(sprite_car12, (X * 0.2, Y * 0.1))
sprite_car13 = pygame.image.load('car.png').convert_alpha()
sprite_car13 = pygame.transform.scale(sprite_car13, (X * 0.2, Y * 0.1))

FORMS = {
    'car1': [sprite_car11, sprite_car12, sprite_car13]
}

CARS = []


class Car:
    def __init__(self, x, y, sprite, speed=0, max_speed=100, way=2, time=1):
        self.x, self.y = x, y
        self.sprite, self.speed, self.max_speed, self.way, self.time = sprite, speed, max_speed, way, time

    def move(self, x, y):
        self.x += x
        self.y += y

    def set_speed(self, speed):
        self.speed += speed

    def set_max_speed(self, max_speed):
        self.max_speed = max_speed

    def set_way(self, way):
        self.way = way


class Player:
    def __init__(self):
        pass


def game():
    global running

    mw.blit(sprite_background, (0, 0))
    mw.blit(sprite_road, (X * 0.3, Y * 0.5))
    mw.blit(player.sprite[0], (X * 0.4, Y * 0.6))

    while running:
        if random.randint(0, 100) == 1:
            CARS.append(Car(random.randint(0, X), random.randint(Y * 0.5, Y), random.randint(0, len(FORMS))))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.set_speed(player.speed / player.time)

                elif event.key == pygame.K_s:
                    player.set_speed(-player.speed / player.time)

                elif event.key == pygame.K_a:
                    player.set_speed(-player.speed / player.time / 2)
                    player.set_way(1)
                    player.move(0, -10)

                elif event.key == pygame.K_d:
                    player.set_speed(-player.speed / player.time / 2)
                    player.set_way(3)
                    player.move(0, 10)

                else:
                    player.set_speed(-player.speed / player.time / 5)

            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(FPS)


player = Car(X * 0.4, Y * 0.6, FORMS['car1'], 0, 150)
game()
