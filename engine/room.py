import pygame

class Room(object):
    def __init__(self):
        self.run = True

    def exit(self):
        self.run = False


class MainMenu(Room):
    def __init__(self, title, bg_color, button_list):
        super(MainMenu, self).__init__()
        self.title = title
        self.bg_color = bg_color
        self.button_list = button_list

    def show(self, surface, (x, y)=(300, 200)):
        surface.fill(self.bg_color)
        surface.blit(self.title, (x, y))
        for button in self.button_list:
            button.show(surface)
        pygame.display.update()

    def button_pressed(self):
        for i, button in enumerate(self.button_list):
            if button.pressed():
                return i
        return 16


class Button(object):
    def __init__(self, text, (x, y), font, actual_text):
        self.text = text
        self.x = x
        self.y = y
        self.width = font.size(actual_text)[0]
        self.height = font.size(actual_text)[1]

    def show(self, surface):
        pygame.draw.rect(surface, (255, 16, 16), (self.x, self.y, self.width, self.height))
        surface.blit(self.text, (self.x, self.y))

    def pressed(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.x + self.width > mouse_pos[0] > self.x:
            if self.y + self.height > mouse_pos[1] > self.y and pygame.mouse.get_pressed()[0]:
                return True
        else:
            return False
