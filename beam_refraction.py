import pygame
import math


pygame.init()


def beam_ref_sim():
    def get_coords(x, y, alpha, length):
        x += length * math.sin(alpha)
        y += length * math.cos(alpha)
        return x, y

    n1, n2, alpha = float(input('n1: ')), float(input('n2: ')), int(input('a: '))

    size = width, height = 1000, 1000
    screen = pygame.display.set_mode(size)
    run = True
    clock = pygame.time.Clock()
    draw = False
    screen.fill('white')
    pygame.draw.rect(screen, 'grey', (0, 500, 1000, 1000))
    pygame.draw.line(screen, 'black', (0, 500), (1000, 500), 5)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0 <= alpha <= 180 and (n1 and n2) >= 0:
                    gamma = math.asin((n1 * abs(math.sin(math.radians(alpha)))) / n2)
                    draw = True

            x, y = get_coords(500, 500, math.radians(alpha), 1000)
            pygame.draw.line(screen, 'red', (500, 500), (1000 - x, 1000 - y), 4)
            if draw:
                x, y = get_coords(500, 500, gamma, 1000)
                pygame.draw.line(screen, 'orange', (500, 500), (x, y), 4)

        clock.tick(100)
        pygame.display.flip()
    pygame.quit()
