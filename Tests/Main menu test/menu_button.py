import pygame as pg

class Button(object):
    def __init__(self, text, x, y):
        self.x = x
        self.y = y
        self.text = text
        self.width = 150
        self.height = 60
        self.color = (250, 100, 160)





    def show(self, surface):
        pg.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        surface.blit(self.text, (self.x + 10, self.y + 5))

    def pressed(self, mouse_click):
        if self.x + self.width > pg.mouse.get_pos()[0] > self.x and mouse_click and pg.mouse.get_pressed()[0]:
            if self.y + self.height > pg.mouse.get_pos()[1] > self.y and mouse_click and pg.mouse.get_pressed()[0]:
                return True
        else:
            return False
