import pygame as pg
import pymunk.pygame_util
from random import randrange
from collision import Status_bar
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
segment_shape = pymunk.Segment(space.static_body, (2, HEIGHT), (100 * WIDTH, HEIGHT), 26)
space.add(segment_shape)


def render_inputs(inputs):
    for i in inputs:
        i.render_input(surface)


def create_square(space, pos, mass, speed, friction):
    global segment_shape
    square_mass, square_size = mass, (60, 60)
    square_moment = pymunk.moment_for_box(square_mass, square_size)
    # Создается тело объекта
    square_body = pymunk.Body(square_mass, square_moment, pymunk.Body.DYNAMIC)
    square_body.position = pos

    # Создаем и настраиваем "фигуру" объекта
    segment_shape.friction = friction
    square_shape = pymunk.Poly.create_box(square_body, square_size)
    square_shape.body.apply_impulse_at_local_point((mass * speed, 0), (0, 0))
    square_shape.elasticity = 0
    square_shape.friction = 1
    square_shape.color = [randrange(256) for i in range(4)]

    space.add(square_body, square_shape)
    return square_shape


def friction_simulation():
    global space, draw_options
    # Нужные значения
    obj = None

    spd_cur = Status_bar(380, 100, 120, 30)
    accel_cur = Status_bar(380, 150, 120, 30)
    distance_cur = Status_bar(380, 200, 120, 30)
    spd, m, friction = None, None, None
    values = [spd, m, friction]
    # Создаем платформу
    segment_shape.elasticity = 0
    segment_shape.friction = 0.0

    status = Status_bar(100, 200, 270, 40)
    status.set_text("Нажмите 'k', чтобы начать")
    # Поля для ввода
    input_speed = InputVal(100, 100, 120, 30, 8, default="Скорость")
    input_friction = InputVal(100, 150, 120, 30, 8, default="Коэфициент трения")
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
                            obj = create_square(space, (60, HEIGHT - 70), m, spd, friction)
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
            distance_cur.set_text(str(round(obj.body.position[0] - 60, 2)))
            accel_cur.set_text("-" + str(friction * m * 10))

        surface.fill("white")
        render_inputs(inputs)
        status.render_bar(surface)
        for cur in (spd_cur, distance_cur, accel_cur):
            cur.render_bar(surface)
        if not pause:
            space.step(1 / FPS)
        space.debug_draw(draw_options)

        pg.display.flip()
        clock.tick(FPS)
    space = pymunk.Space()
    space.gravity = 0, 8000
    draw_options = pymunk.pygame_util.DrawOptions(surface)
friction_simulation()