from pygame import draw, mouse

class Button(object):
    def __init__(self, (x, y), color, font, actual_text, colors, antial=False):
        self.x = x
        self.y = y
        self.color = color
        self.font = font
        self.actual_text = actual_text
        self.antial = antial
        self.colors = colors
        self.highlight = False
        self.width = font.size(actual_text)[0] + 10
        self.height = font.size(actual_text)[1]

    def show(self, surface):
        draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        text = self.font.render(self.actual_text, self.antial, self.colors[0 if not self.highlight else 1])
        surface.blit(text, (self.x + 5, self.y + 2))

    def pressed(self):
        mouse_pos = mouse.get_pos()
        if self.x + self.width > mouse_pos[0] > self.x:
            if self.y + self.height > mouse_pos[1] > self.y:
                self.highlight = True
                if mouse.get_pressed()[0]:
                    return True
            else:
                self.highlight = False
        else:
            self.highlight = False
            return False
