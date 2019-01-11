from pygame import time

class Room(object):
    def __init__(self, title=None, button_list=None, sound=None):
        self.run = True
        self.title = title
        self.button_list = button_list
        self.sound = sound

    def show(self, surface, (x, y)):
        surface.blit(self.title, (x, y))
        for button in self.button_list:
            button.show(surface)
            button.pressed()

    def button_pressed(self):
        for i, button in enumerate(self.button_list):
            if button.pressed():
                if self.sound is not None:
                    self.sound.play()
                return i
        return 16

    def exit(self):
        self.run = False


class MainMenu(Room):
    def __init__(self, title, bg_color, button_list, sound):
        super(MainMenu, self).__init__()
        self.title = title
        self.bg_color = bg_color
        self.button_list = button_list
        self.sound = sound

    def show(self, surface, (x, y)):
        surface.fill(self.bg_color)
        surface.blit(self.title, (x, y))
        for button in self.button_list:
            button.show(surface)
            button.pressed()
