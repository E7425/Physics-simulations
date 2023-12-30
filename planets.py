import pygame
import math
from input import InputVal

pygame.init()

WIDTH, HEIGHT = 1040, 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 120


def init_planets():
    sun = Planet(0, 0, 20, "yellow", 1.9891 * 10 ** 30)
    sun.vx = 0 * 10 ** 3
    sun.vy = 0 * 10 ** 3
    sun.is_sun = True

    earth = Planet(Planet.au, 0, 6, (17, 188, 240), 5.976 * 10 ** 24)
    earth.vy = -29.78 * 10 ** 3

    mercury = Planet(Planet.au * 0.387, 0, 3, (247, 215, 182), 3.33 * 10 ** 23)
    mercury.vy = -47.4 * 10 ** 3

    venus = Planet(-Planet.au * 0.723, 0, 6, (252, 133, 48), 4.87 * 10 ** 24)
    venus.vy = 35.02 * 10 ** 3

    mars = Planet(Planet.au * 1.52, 0, 5, (255, 77, 0), 6.42 * 10 ** 23)
    mars.vy = -24.08 * 10 ** 3

    jupiter = Planet(Planet.au * 5.2, 0, 13, (255, 170, 0), 1.8986 * 10 ** 27)
    jupiter.vy = -13.1 * 10 ** 3

    objects = [sun, mercury, venus, earth, mars, jupiter]
    return objects


class Planet:
    step = 86400
    # Гравитационная постоянная
    G = 6.67 * 10 ** (-11)
    # Астрономическая единица (в метрах)
    au = 1496 * 10 ** 8
    scaling = 65 / au

    def __init__(self, x, y, r, color, m):
        self.vx = 0
        self.vy = 0
        self.orbit = []

        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.m = m

        self.is_sun = False

    def render(self, screen):
        x = self.x * self.scaling + WIDTH / 2
        y = self.y * self.scaling + HEIGHT / 2
        pygame.draw.circle(screen, self.color, (x, y), self.r)

    def get_force(self, target):
        dx = target.x - self.x
        dy = target.y - self.y
        d = (dx ** 2 + dy ** 2) ** 0.5

        angle = math.atan2(dy, dx)

        force = (self.G * self.m * target.m) / (d ** 2)
        force_x = force * math.cos(angle)
        force_y = force * math.sin(angle)

        return force_x, force_y

    def move(self, planets):
        sigma_fx = 0
        sigma_fy = 0
        for p in planets:
            if p == self:
                continue

            force_x, force_y = self.get_force(p)
            sigma_fx += force_x
            sigma_fy += force_y

        ax = sigma_fx / self.m
        ay = sigma_fy / self.m
        self.vx += ax * self.step
        self.vy += ay * self.step

        self.x += self.vx * self.step
        self.y += self.vy * self.step

        self.orbit.append((self.x, self.y))


def planet_moving():
    run = True
    clock = pygame.time.Clock()

    # Создание планет (Реальные характеристики)
    objects = init_planets()

    inp_xv = InputVal(100, 100, 220, 30, 8, default="Гор. скор. солнца(км/с))")
    sun_xv = 0
    sun_yv = 0
    inp_yv = InputVal(100, 150, 220, 30, 8, default="Верт. скор. солнца(км/с)")

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                objects = init_planets()

                try:
                    objects[0].vx = float(sun_xv) * 1000
                except ValueError as e:
                    print(e)

                try:
                    objects[0].vy = float(sun_yv) * 1000
                except ValueError as e:
                    print(e)

            for inp in (inp_xv, inp_yv):
                res = inp.event_handler(event)

                if res is not None:
                    if inp == inp_xv:
                        sun_xv = res
                    elif inp == inp_yv:
                        sun_yv = res


        clock.tick(FPS)
        screen.fill("black")

        # Отрисовка планет
        for p in objects:
            for j in p.orbit:
                pygame.draw.circle(screen, p.color, (j[0] * Planet.scaling + WIDTH / 2, j[1] * Planet.scaling + HEIGHT / 2), 1)
            p.render(screen)
            p.move(objects)
        inp_yv.render_input(screen)
        inp_xv.render_input(screen)
        pygame.display.update()
