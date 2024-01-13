import pygame as pg
from planets import planet_moving
from collision import elasticity_true, elasticity_false
from friction import friction_simulation
from beam_refraction import beam_ref_sim
from archimedes import archimedes_simulation
from energy import falling_simulation

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
    buttons = [MenuButton(165, 130, 310, 50, elasticity_true, "Упругое столкновение"),
               MenuButton(505, 130, 340, 50, elasticity_false, "Неупругое столкновение"),
               MenuButton(165, 240, 310, 50, beam_ref_sim, "  Преломление луча"),
               MenuButton(505, 240, 340, 50, archimedes_simulation, "      Сила Архимеда"),
               MenuButton(505, 350, 340, 50, planet_moving, "      Движение планет"),
               MenuButton(165, 350, 310, 50, friction_simulation, "       Сила трения"),
               MenuButton(165, 450, 310, 50, falling_simulation, "  Падение тела")
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
