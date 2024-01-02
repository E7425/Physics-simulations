import pygame
import math
from input1 import InputVal

pygame.init()


def get_coords(x, y, alpha, length):
    x += length * math.sin(alpha)
    y += length * math.cos(alpha)
    return x, y


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


def draw_gamma(screen, gamma, x, y):
    pygame.draw.line(screen, 'orange', (500, 500), (x, y), 4)
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(str(round(math.degrees(gamma), 2)), 1, pygame.Color('black'), pygame.Color('grey'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top += 980
    screen.blit(string_rendered, intro_rect)


def error_message(screen):
    font = pygame.font.Font(None, 50)
    string_rendered = font.render('ОШИБКА. НЕВЕРНЫЙ ВВОД', 1, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    screen.blit(string_rendered, intro_rect)


def beam_ref_sim():
    size = width, height = 1000, 1000
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    FPS = 60
    run = True
    draw1 = False
    draw2 = False
    error = False
    input_n1 = InputVal(100, 100, 120, 30, 3, default="n1")
    input_n2 = InputVal(100, 150, 120, 30, 3, default="n2")
    input_alpha = InputVal(100, 200, 120, 30, 3, default="alpha")
    inputs = [input_n1, input_n2, input_alpha]

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    alpha = str(input_alpha.get_text())
                    n1 = str(input_n1.get_text())
                    n2 = str(input_n2.get_text())
                    if alpha.isdigit() and n1.isdigit() and n2.isdigit():
                        if 0 <= float(alpha) <= 180:
                            if not draw1:
                                error = False
                                draw1 = True
                            else:
                                error = False
                                draw2 = True
                        else:
                            error = True
                    else:
                        error = True

            if draw1:
                n1 = float(input_n1.get_text())
                n2 = float(input_n2.get_text())
                alpha = float(input_alpha.get_text())
                draw_alpha(screen, alpha)

                if draw2:
                    gamma = math.asin((n1 * abs(math.sin(math.radians(alpha)))) / n2)
                    x, y = get_coords(500, 500, gamma, 1000)
                    draw_gamma(screen, gamma, x, y)
            else:
                screen.fill('black')
                for i in inputs:
                    i.render_input(screen)
                if error:
                    error_message(screen)

            for i in inputs:
                i.event_handler(event)

        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


beam_ref_sim()
