import pygame as pg


pg.init()


class InputVal:
    def __init__(self, x, y, width, height, mx_sym, text='', font=pg.font.Font(None, 28), default=""):
        self.rect = pg.Rect(x, y, width, height)
        self.mx_sym = mx_sym
        self.color = "blue"
        self.text = text
        self.font = font
        self.default = default
        self.text_surface = self.font.render(text, True, self.color)
        self.active = False

    def render_input(self, surface):
        if self.text:
            surface.blit(self.text_surface, (self.rect.x+4, self.rect.y+5))
        else:
            surface.blit(self.font.render(self.default, True, self.color), (self.rect.x+4, self.rect.y+5))
        pg.draw.rect(surface, self.color, self.rect, 1)

    def event_handler(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
                return self.get_text()
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN or event.key == pg.K_k:
                    self.active = False
                    return self.get_text()
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) != self.mx_sym:
                    self.text += event.unicode
                self.text_surface = self.font.render(self.text, True, self.color)

    def get_text(self):
        if self.text:
            return self.text
        return None