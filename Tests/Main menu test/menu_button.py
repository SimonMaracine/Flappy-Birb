import pygame

class Button(object):
    def __init__(self, text, y, x_offset, font, actual_text):
        self.text = text
        self.width = font.size(actual_text)[0] + 10
        self.height = font.size(actual_text)[1] + 1
        self.color = (250, 100, 160)
        self.x = 800 / 2 - self.width / 2 + x_offset
        self.y = y









    def show(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        surface.blit(self.text, (self.x + 5, self.y + 5))

    def pressed(self, mouse_click):
        if self.x + self.width > pygame.mouse.get_pos()[0] > self.x and mouse_click and pygame.mouse.get_pressed()[0]:
            if self.y + self.height > pygame.mouse.get_pos()[1] > self.y and mouse_click and pygame.mouse.get_pressed()[0]:
                return True
        else:
            return False
