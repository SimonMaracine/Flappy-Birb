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

    def show(self, surface, (x, y)):
        surface.fill(self.bg_color)
        surface.blit(self.title, (x, y))
        for button in self.button_list:
            button.show(surface)

    def button_pressed(self):
        for i, button in enumerate(self.button_list):
            if button.pressed():
                return i
        return 16
