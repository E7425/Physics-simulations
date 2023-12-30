import pygame
import math
from input1 import InputVal


pygame.init()


def beam_ref_sim():
    def get_coords(x, y, alpha, length):
        x += length * math.sin(alpha)
        y += length * math.cos(alpha)
        return x, y

    size = width, height = 1000, 1000
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    run = True
    draw = False
    draw2 = False
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
                    if not draw:
                        draw = True
                    else:
                        draw2 = True
                        gamma = math.asin((n1 * abs(math.sin(math.radians(alpha)))) / n2)

            if draw:
                n1 = float(input_n1.get_text())
                n2 = float(input_n2.get_text())
                alpha = float(input_alpha.get_text())
                screen.fill('white')
                pygame.draw.rect(screen, 'grey', (0, 500, 1000, 1000))
                pygame.draw.line(screen, 'black', (0, 500), (1000, 500), 5)
                x, y = get_coords(500, 500, math.radians(alpha), 1000)
                pygame.draw.line(screen, 'red', (500, 500), (1000 - x, 1000 - y), 4)
                font = pygame.font.Font(None, 30)
                string_rendered = font.render(str(alpha), 1, pygame.Color('black'))
                intro_rect = string_rendered.get_rect()
                screen.blit(string_rendered, intro_rect)
                if draw2:
                    x, y = get_coords(500, 500, gamma, 1000)
                    pygame.draw.line(screen, 'orange', (500, 500), (x, y), 4)
                    string_rendered = font.render(str(round(math.degrees(gamma), 2)), 1, pygame.Color('black'))
                    intro_rect = string_rendered.get_rect()
                    intro_rect.top += 980
                    screen.blit(string_rendered, intro_rect)
            else:
                screen.fill('black')
                for i in inputs:
                    i.render_input(screen)

            for i in inputs:
                res = i.event_handler(event)

        clock.tick(100)
        pygame.display.flip()
    pygame.quit()

beam_ref_sim()