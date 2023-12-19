import pygame as pg


class InputVal:
    def __init__(self, x, y, width, height, mx_sym, text='', font=pg.font.Font(None, 28)):
        self.rect = pg.Rect(x, y, width, height)
        self.mx_sym = mx_sym
        self.color = "white"
        self.text = text
        self.font = font
        self.text_surface = self.font.render(text, True, self.color)
        self.active = False

    def render_input(self, surface):
        surface.blit(self.text_surface, (self.rect.x+4, self.rect.y+5))
        pg.draw.rect(surface, self.color, self.rect, 1)

    def event_handler(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    return self.text
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) != self.mx_sym:
                    self.text += event.unicode
                self.text_surface = self.font.render(self.text, True, self.color)

    def get_text(self):
        if self.text:
            return self.text
        return None
