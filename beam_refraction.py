import pygame
import math
from input import InputVal

pygame.init()


# функция для получения конечной координаты по градусной мере угла
def get_coords(x, y, alpha, length):
    x += length * math.sin(alpha)
    y += length * math.cos(alpha)
    return x, y


# функция для рисования 1 угла
def draw_alpha(screen, alpha):
    screen.fill('white')
    pygame.draw.rect(screen, 'grey', (0, 500, 1000, 1000))
    pygame.draw.line(screen, 'black', (0, 500), (1000, 500), 5)
    x, y = get_coords(500, 500, math.radians(alpha), 1000)
    pygame.draw.line(screen, 'red', (500, 500), (1000 - x, 1000 - y), 4)
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(str(alpha), 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    screen.blit(string_rendered, intro_rect)


# функция для рисования 2 угла
def draw_gamma(screen, gamma, x, y):
    pygame.draw.line(screen, 'orange', (500, 500), (x, y), 4)
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(str(round(math.degrees(gamma), 2)), 1, pygame.Color('black'), pygame.Color('grey'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top += 980
    screen.blit(string_rendered, intro_rect)


# функция для вывода сообщения об ошибке
def error_message(screen):
    font = pygame.font.Font(None, 50)
    string_rendered = font.render('ОШИБКА. НЕВЕРНЫЙ ВВОД', 1, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    screen.blit(string_rendered, intro_rect)


# основная функция
def beam_ref_sim():
    # параметры pygame
    size = width, height = 1000, 1000
    screen = pygame.display.set_mode(size)
    run = True
    draw = False
    draw2 = False
    error = False
    input_flag = True
    # поля для ввода данных
    input_n1 = InputVal(100, 100, 400, 30, 3, default="показатель преломления 1 поверхности")
    input_n2 = InputVal(100, 150, 400, 30, 3, default="показатель преломления 2 поверхности")
    input_alpha = InputVal(100, 200, 400, 30, 3, default="угол падения луча")
    inputs = [input_n1, input_n2, input_alpha]

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:  # старт симуляции
                    try:
                        alpha = float(input_alpha.get_text())  # угол падения луча
                        n1 = float(input_n1.get_text())  # показатель преломления 1 поверхности
                        n2 = float(input_n2.get_text())  # показатель преломления 2 поверхности
                        if (not (0 < alpha <= 180)) or n1 == 0 or n2 == 0:
                            raise ValueError
                        if input_flag:
                            draw = True
                            input_flag = False
                        else:
                            draw2 = True
                    except (ValueError, TypeError):
                        error = True

            for i in inputs:
                i.event_handler(event)

        if input_flag:
            screen.fill('white')
            for i in inputs:
                i.render_input(screen)
            if error:
                error_message(screen)

        elif draw:
            # запись введенных данных в переменные
            draw_alpha(screen, alpha)
            if draw2:
                gamma = math.asin((n1 * abs(math.sin(math.radians(alpha)))) / n2)
                x, y = get_coords(500, 500, gamma, 1000)
                draw_gamma(screen, gamma, x, y)
                draw = False

        pygame.display.flip()
