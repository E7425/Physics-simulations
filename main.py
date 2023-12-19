import pygame as pg
import pymunk.pygame_util
from collision import collision_simulation

pg.init()
font = pg.font.SysFont("arial", 35)
screen = pg.display.set_mode((1040, 680))


class MenuButton:
    def __init__(self, x, y, width, height, func, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.func = func
        self.text = font.render(text, True, "black")

    def render_button(self):
        pg.draw.rect(screen, "blue", (self.x, self.y, self.width, self.height), width=1)
        screen.blit(self.text, (self.x + 7, self.y))

    def check_clicked(self, pos):
        if self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height:
            self.func()


def main(): # Основная функция
    buttons = [MenuButton(165, 130, 310, 50, collision_simulation, "Упругое столкновение"),
               MenuButton(505, 130, 340, 50, collision_simulation, "Неупругое столкновение"),
               MenuButton(165, 240, 310, 50, collision_simulation, "  Преломление луча"),
               MenuButton(505, 240, 340, 50, collision_simulation, "      Сила Архимеда"),
               MenuButton(505, 350, 340, 50, collision_simulation, "      Движение планет"),
               MenuButton(165, 350, 310, 50, collision_simulation, "       Сила трения")
               ]

    clock = pg.time.Clock()
    run = True
    while run:
        screen.fill("white")
        for btn in buttons:
            btn.render_button()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for btn in buttons:
                    btn.check_clicked(event.pos)
        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
    pg.quit()
