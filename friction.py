import pygame as pg
import pymunk.pygame_util
from random import randrange
from collision import StatusBar
from input import InputVal

pymunk.pygame_util.positive_y_is_up = False


# параметры PyGame
RES = WIDTH, HEIGHT = 1040, 680
FPS = 60

pg.init()
font = pg.font.SysFont("arial", 25)
clock = pg.time.Clock()


def render_inputs(inputs, screen):
    for i in inputs:
        i.render_input(screen)


def create_square(space, pos, mass, speed):
    square_mass, square_size = mass, (60, 60)
    square_moment = pymunk.moment_for_box(square_mass, square_size)
    # Создается тело объекта
    square_body = pymunk.Body(square_mass, square_moment, pymunk.Body.DYNAMIC)
    square_body.position = pos

    # Создаем и настраиваем "фигуру" объекта
    square_shape = pymunk.Poly.create_box(square_body, square_size)
    square_shape.body.apply_impulse_at_local_point((mass * speed, 0), (0, 0))
    square_shape.elasticity = 0
    square_shape.friction = 0
    square_shape.color = [randrange(256) for i in range(4)]

    space.add(square_body, square_shape)
    return square_shape


def friction_simulation():
    # Нужные значения
    obj = None
    surface = pg.display.set_mode(RES)
    draw_options = pymunk.pygame_util.DrawOptions(surface)

    # настройки Pymunk
    space = pymunk.Space()
    space.gravity = 0, 8000

    spd_cur = StatusBar(380, 100, 120, 30)
    accel_cur = StatusBar(380, 150, 120, 30)
    distance_cur = StatusBar(380, 200, 120, 30)
    spd, m, friction = None, None, None
    values = [spd, m, friction]
    # Создаем платформу
    segment_shape = pymunk.Segment(space.static_body, (2, HEIGHT), (100 * WIDTH, HEIGHT), 26)
    space.add(segment_shape)
    segment_shape.elasticity = 0
    segment_shape.friction = 0.0

    status = StatusBar(100, 200, 270, 40)
    status.set_text("Нажмите 'k', чтобы начать")
    # Поля для ввода
    input_speed = InputVal(100, 100, 120, 30, 8, default="Скорость")
    input_friction = InputVal(100, 150, 220, 30, 8, default="Коэфициент трения")
    input_mass = InputVal(250, 100, 120, 30, 8, default="Масса")
    inputs = [input_speed, input_friction, input_mass]
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
                    if obj is not None:
                        space.remove(obj)
                        obj = None

                    if any(i is None for i in values):
                        status.set_text("Не все поля заполнены")
                    else:
                        try:
                            spd, friction, m = (float(i) for i in values)
                            if m <= 0:
                                raise ValueError
                            obj = create_square(space, (60, HEIGHT - 58), m, spd)
                        except ValueError:
                            status.set_text("Некорректные данные")

            for i in inputs:
                res = i.event_handler(event)

                if res is not None:
                    if i == input_speed:
                        values[0] = res
                    elif i == input_friction:
                        values[1] = res
                    elif i == input_mass:
                        values[2] = res

        if obj is not None:
            spd_cur.set_text(str(round(obj.body.velocity[0], 2)))
            distance_cur.set_text(str(round((obj.body.position[0] - 60), 2)))
            accel_cur.set_text("-" + str(round(friction * m * 10, 2)))

        surface.fill("white")
        render_inputs(inputs, surface)
        status.render_bar(surface)
        for cur in (spd_cur, distance_cur, accel_cur):
            cur.render_bar(surface)
        if not pause:
            if values.count(None) == 0 and obj is not None:
                obj.body.velocity = (obj.body.velocity[0] - friction * m * 10 / FPS, 0)
                if obj.body.velocity[0] <= 0:
                    obj.body.velocity = (0, 0)
            space.step(1 / FPS)
        space.debug_draw(draw_options)
        pg.display.flip()
        clock.tick(FPS)