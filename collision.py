import pygame as pg
import pymunk.pygame_util
from random import randrange
from input import InputVal

pymunk.pygame_util.positive_y_is_up = False

# параметры PyGame
RES = WIDTH, HEIGHT = 1040, 680
FPS = 60

pg.init()
font = pg.font.SysFont("arial", 25)
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)

# настройки Pymunk
space = pymunk.Space()
space.gravity = 0, 8000


class Status_bar:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text_ren = font.render("", True, "black")

    def render_bar(self, screen):
        pg.draw.rect(screen, "blue", (self.x, self.y, self.width, self.height), width=1)
        screen.blit(self.text_ren, (self.x + 7, self.y))

    def set_text(self, text):
        self.text_ren = font.render(text, True, "blue")


def elasticity_true():
    collision_simulation(1)


def elasticity_false():
    collision_simulation(0)


def render_inputs(inputs):
    for i in inputs:
        i.render_input(surface)


def create_square(space, pos, mass, speed, elastic=1):
    square_mass, square_size = mass, (60, 60)
    square_moment = pymunk.moment_for_box(square_mass, square_size)
    # Создается тело объекта
    square_body = pymunk.Body(square_mass, square_moment, pymunk.Body.DYNAMIC)
    square_body.position = pos

    # Создаем и настраиваем "фигуру" объекта
    square_shape = pymunk.Poly.create_box(square_body, square_size)
    square_shape.body.apply_impulse_at_local_point((mass * speed, 0), (0, 0))
    square_shape.elasticity = elastic
    square_shape.friction = 1.0
    square_shape.color = [randrange(256) for i in range(4)]

    space.add(square_body, square_shape)
    return square_shape


def collision_simulation(elastic=1):
    global space, draw_options
    # Нужные значения
    obj1, obj2 = None, None
    spd1, spd2 = None, None
    spd_cur1 = Status_bar(380, 100, 120, 30)
    spd_cur2 = Status_bar(380, 150, 120, 30)
    m1, m2 = None, None
    values = [spd1, spd2,  m1, m2]
    # Создаем платформу
    segment_shape = pymunk.Segment(space.static_body, (-2000, HEIGHT), (WIDTH * 10, HEIGHT), 26)
    space.add(segment_shape)
    segment_shape.elasticity = 0
    segment_shape.friction = 0.0

    status = Status_bar(100, 200, 270, 40)
    status.set_text("Нажмите 'k', чтобы начать")
    # Поля для ввода
    input_speed1 = InputVal(100, 100, 120, 30, 8, default="Скорость 1")
    input_speed2 = InputVal(100, 150, 120, 30, 8, default="Скорость 2")
    input_mass1 = InputVal(250, 100, 120, 30, 8, default="Масса 1")
    input_mass2 = InputVal(250, 150, 120, 30, 8, default="Масса 2")
    inputs = [input_speed1, input_speed2, input_mass2, input_mass1]
    run = True
    pause = False
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_p:
                    pause = not pause
                    status.set_text("Симуляция на паузе" if pause else "Симуляция продолжается")

                if event.key == pg.K_k:  # Старт симуляции
                    if obj1 is not None:
                        space.remove(obj1)
                        space.remove(obj2)
                        obj1 = None
                        obj2 = None

                    if any(i is None for i in values):
                        status.set_text("Не все поля заполнены")
                    else:
                        try:
                            spd1, spd2, m1, m2 = (float(i) for i in values)
                            obj1 = create_square(space, (60, HEIGHT - 70), m1, spd1, elastic)
                            obj2 = create_square(space, (WIDTH - 60, HEIGHT - 70), m2, -spd2, elastic)
                        except ValueError:
                            status.set_text("Некорректные данные")

            for i in inputs:
                res = i.event_handler(event)

                if res is not None:
                    if i == input_speed1:
                        values[0] = res
                    elif i == input_speed2:
                        values[1] = res
                    elif i == input_mass1:
                        values[2] = res
                    elif i == input_mass2:
                        values[3] = res

        if obj1 is not None:
            spd_cur1.set_text(str(round(obj1.body.velocity[0], 2)))
            spd_cur2.set_text(str(round(obj2.body.velocity[0], 2)))

        surface.fill("white")
        render_inputs(inputs)
        status.render_bar(surface)
        spd_cur1.render_bar(surface)
        spd_cur2.render_bar(surface)
        if not pause:
            space.step(1 / FPS)
        space.debug_draw(draw_options)

        pg.display.flip()
        clock.tick(FPS)
    space = pymunk.Space()
    space.gravity = 0, 8000
    draw_options = pymunk.pygame_util.DrawOptions(surface)
