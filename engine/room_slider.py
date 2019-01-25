import pygame

class VolumeSlider(object):
    def __init__(self, (x, y), color, colors, (width, height)):
        self.x = x
        self.y = y
        self.color = color
        self.colors = colors
        self.highlight = False
        self.width = width
        self.height = height
        self.bar_length = self.width - 12
        self.volume = 1.0

    def show(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, self.colors[0 if not self.highlight else 1], (self.x + 6, self.y + 8, self.bar_length, self.height - 18))

    def pressed(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.x + self.width > mouse_pos[0] > self.x:
            if self.y + self.height > mouse_pos[1] > self.y:
                self.highlight = True
                if pygame.mouse.get_pressed()[0]:
                    return True
            else:
                self.highlight = False
        else:
            self.highlight = False
            return False

    def change_volume(self):
        if self.pressed():
            mouse_pos = pygame.mouse.get_pos()[0]
            if mouse_pos <= self.x + self.width - 12:
                self.bar_length = mouse_pos - self.x
                if self.bar_length <= 2:
                    self.volume = 0.0
                elif self.bar_length >= self.width - 14:
                    self.volume = 1.0
                else:
                    self.volume = (self.bar_length * 1.0) / (self.width - 12)

    def reset_volume(self):
        self.bar_length = self.width - 12
        self.volume = 1.0

    def set_volume(self, path):
        with open(path, "r+") as data:
            data.seek(4)
            data.write(str(round(self.volume, 2)))

    def get_volume(self, path):
        with open(path, "r") as data:
            self.volume = float(data.read()[4:7])
        self.bar_length = int(self.volume * (self.width - 12))
