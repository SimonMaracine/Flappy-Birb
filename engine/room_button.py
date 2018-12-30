import pygame

class Button(object):
    def __init__(self, text, (x, y), color, font, actual_text):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = font.size(actual_text)[0]
        self.height = font.size(actual_text)[1]

    def show(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        surface.blit(self.text, (self.x, self.y))

    def pressed(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.x + self.width > mouse_pos[0] > self.x:
            if self.y + self.height > mouse_pos[1] > self.y and pygame.mouse.get_pressed()[0]:
                return True
        else:
            return False
