import pygame
from input import InputVal


pygame.init()


# функция для вывода ошибки
def error_message(screen, font):
    string_rendered = font.render('ОШИБКА. НЕВЕРНЫЙ ВВОД', 1, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    screen.blit(string_rendered, intro_rect)


# функция для вывода значений энергий тела
def print_text(screen, text, y, font):
    string_rendered = font.render(text, 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top += y
    screen.blit(string_rendered, intro_rect)


# основная функция
def falling_simulation():
    # параметры pygame
    size = width, height = 1000, 1000
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    FPS = 60
    font = pygame.font.Font(None, 50)
    run = True
    draw = False
    error = False
    input_flag = True
    height_pix = 680    # высота падения в пикселях
    t = 0               # счетчик времени (в кадрах)

    # поля для ввода данных
    input_h = InputVal(100, 100, 170, 30, 3, default="высота падения")
    input_m = InputVal(100, 150, 170, 30, 3, default="масса тела")
    inputs = [input_h, input_m]

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    if bool(input_h.get_text()) and bool(input_m.get_text()):
                        if input_h.get_text().isdigit() and input_m.get_text().isdigit():
                            input_flag = False
                            draw = True
                        else:
                            error = True
                    else:
                        error = True

            for i in inputs:
                i.event_handler(event)

        if input_flag:
            screen.fill('white')
            for i in inputs:
                i.render_input(screen)
            if error:
                error_message(screen, font)

        elif draw:
            # запись введенных данных в переменные
            h = float(input_h.get_text())   # высота падения в метрах
            m = float(input_m.get_text())   # масса тела

            total_t = (2 * h / 10) ** 0.5   # общее время падения
            scale = h / height_pix          # кол-во метров в 1 пикселе
            max_potential_e = m * 10 * h    # максимальная потенциальная энергия

            screen.fill(pygame.Color('white'))
            if t - 1 < total_t * 60:
                s = 10 * ((t / 60) ** 2) / 2  # преодаленное расстояние в метрах
                s_pix = int(s / scale)        # преодаленное расстояние в пикселях
                v = t / 60 * 10               # скорость
                if t % 30 == 0:
                    kinetic_e = m * (v ** 2) / 2    # кинетическая энергия
                    potential_e = m * 10 * (h - s)  # потенциальная энергия

                # вывод значений энергии объекта
                print_text(screen, 'кинетическая энергия ' + str(int(kinetic_e)), 0, font)
                print_text(screen, 'потенциальная энергия ' + str(int(potential_e)), 50, font)
                print_text(screen, 'максимальная потенциальная энергия ' + str(int(max_potential_e)), 100, font)

                pygame.draw.rect(screen, 'red', (425, 150 + s_pix, 150, 150))
                t += 1
            else:
                max_kinetic_e = m * (v ** 2) / 2  # максимальная кинетическая энергия

                # вывод значений энергии объекта
                print_text(screen, 'кинетическая энергия ' + '0', 0, font)
                print_text(screen, 'потенциальная энергия ' + '0', 50, font)
                print_text(screen, 'максимальная потенциальная энергия ' + str(int(max_potential_e)), 100, font)
                print_text(screen, 'максимальная кинетическая энергия ' + str(int(max_kinetic_e)), 150, font)

                pygame.draw.rect(screen, 'red', (425, 850, 150, 150))
                draw = False

        clock.tick(FPS)
        pygame.display.update()