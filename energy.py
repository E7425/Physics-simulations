import pygame
from input1 import InputVal


pygame.init()


def error_message(screen, font):
    string_rendered = font.render('ОШИБКА. НЕВЕРНЫЙ ВВОД', 1, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    screen.blit(string_rendered, intro_rect)


def print_text(screen, text, y, font):
    string_rendered = font.render(text, 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top += y
    screen.blit(string_rendered, intro_rect)


def falling_simulation():
    size = width, height = 1000, 1000
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    FPS = 60
    font = pygame.font.Font(None, 50)
    run = True
    draw = False
    error = False
    height_pix = 680
    t = 0
    input_h = InputVal(100, 100, 120, 30, 3, default="h")
    input_m = InputVal(100, 150, 120, 30, 3, default="m")
    inputs = [input_h, input_m]

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    if bool(input_h.get_text()) and bool(input_m.get_text()):
                        if input_h.get_text().isdigit() and input_m.get_text().isdigit():
                            h = float(input_h.get_text())
                            m = float(input_m.get_text())

                            total_t = (2 * h / 10) ** 0.5
                            scale = h / height_pix
                            max_potential_e = m * 10 * h
                            draw = True
                        else:
                            error = True
                    else:
                        error = True

            for i in inputs:
                i.event_handler(event)

        if draw:
            screen.fill(pygame.Color('white'))
            if t - 1 < total_t * 60:
                s = 10 * ((t / 60) ** 2) / 2
                s_pix = int(s / scale)
                v = t / 60 * 10
                if t % 30 == 0:
                    kinetic_e = m * (v ** 2) / 2
                    potential_e = m * 10 * (h - s)
                print_text(screen, 'кинетическая энергия ' + str(int(kinetic_e)), 0, font)
                print_text(screen, 'потенциальная энергия ' + str(int(potential_e)), 50, font)
                print_text(screen, 'максимальная потенциальная энергия ' + str(int(max_potential_e)), 100, font)
                pygame.draw.rect(screen, 'red', (425, 150 + s_pix, 150, 150))
                t += 1
            else:
                max_kinetic_e = m * (v ** 2) / 2
                print_text(screen, 'кинетическая энергия ' + str(int(kinetic_e)), 0, font)
                print_text(screen, 'потенциальная энергия ' + str(int(potential_e)), 50, font)
                print_text(screen, 'максимальная потенциальная энергия ' + str(int(max_potential_e)), 100, font)
                print_text(screen, 'максимальная кинетическая энергия ' + str(int(max_kinetic_e)), 150, font)
                kinetic_e = 0
                potential_e = 0
                pygame.draw.rect(screen, 'red', (425, 850, 150, 150))
        else:
            screen.fill('black')
            for i in inputs:
                i.render_input(screen)
            if error:
                error_message(screen, font)

        clock.tick(FPS)
        pygame.display.update()
    pygame.quit()
