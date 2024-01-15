import pygame
from input import InputVal

pygame.init()


# функция для получения архимедовой силы
def get_archimedes(v_parallelepiped, ro_water):
    return ro_water * 10 * v_parallelepiped


# функция для получения силы тяжести
def get_gravity(v_parallelepiped, ro_cube):
    return ro_cube * 10 * v_parallelepiped


# функция для отрисовки тела в воде
def render_object(screen, y):
    pygame.draw.rect(screen, 'red', (425, y, 200, 250))


# функция для вывода ошибки
def error_message(screen, font):
    string_rendered = font.render('ОШИБКА. НЕВЕРНЫЙ ВВОД', 1, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    screen.blit(string_rendered, intro_rect)


# функция для рисования сосуда с водой
def render_vessel(screen):
    pygame.draw.rect(screen, 'black', (290, 400, 470, 410))
    pygame.draw.rect(screen, (0, 190, 255), (300, 400, 450, 400))


# координаты тела
def get_pos(ro_parallelepiped, v_parallelepiped, ro_water):
    v_parallelepiped_in_water = (ro_parallelepiped * v_parallelepiped) / ro_water
    return 200 * (v_parallelepiped_in_water / v_parallelepiped) + 200


# основная функция
def archimedes_simulation():
    # параметры pygame
    size = width, height = 1000, 1000
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    FPS = 60
    font = pygame.font.Font(None, 50)
    run = True
    draw = True
    error = False
    input_flag = True

    # поля для ввода данных
    input_ro_water = InputVal(100, 100, 300, 30, 10, default="плотность воды")
    input_ro_parallelepiped = InputVal(100, 150, 300, 30, 10, default="плотность тела")
    input_height_parallelepiped = InputVal(100, 200, 300, 30, 10, default="высота тела")
    input_s_plunge_face = InputVal(100, 250, 300, 30, 10, default="площадь погружаемой грани")
    inputs = [input_ro_water, input_ro_parallelepiped, input_height_parallelepiped, input_s_plunge_face]

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:  # старт симуляции и проверки на правильность введенных данных
                    input_flag = False
            for i in inputs:
                i.event_handler(event)

        if input_flag:
            screen.fill('black')
            for i in inputs:
                i.render_input(screen)
            if error:
                error_message(screen, font)

        elif draw:
            try:
                # запись введенных данных в переменные
                ro_water = int(input_ro_water.get_text())  # плотность воды
                ro_parallelepiped = int(input_ro_parallelepiped.get_text())  # плотность тела
                hight_parallelepiped = int(input_height_parallelepiped.get_text())  # высота тела
                s_plunge_face = int(input_s_plunge_face.get_text())  # площадь погруж. грани

                v_parallelepiped = hight_parallelepiped * s_plunge_face  # объем тела
                f_archimedes = get_archimedes(v_parallelepiped, ro_water)  # архимедова сила
                f_gravity = get_gravity(v_parallelepiped, ro_parallelepiped)  # сила тяжести

                screen.fill('white')
                render_vessel(screen)

                if f_archimedes < f_gravity:
                    render_object(screen, 550)
                elif f_archimedes > f_gravity:
                    render_object(screen, (get_pos(ro_parallelepiped, v_parallelepiped, ro_water)))
                else:
                    render_object(screen, 475)

                draw = False
            except Exception:
                input_flag = True
                error = True

        clock.tick(FPS)
        pygame.display.update()
    pygame.quit()
