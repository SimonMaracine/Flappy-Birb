from menu_button import Button
import pygame

class MainMenu(object):
    def __init__(self):
        self.background_color = (100, 100, 160)
        self.button_width = 160
        self.button_height = 40
        self.menu_font = pygame.font.SysFont("calibri", 50)
        self.play_text = self.menu_font.render("PLAY", 0, (255, 255, 255))
        self.quit_text = self.menu_font.render("QUIT", 0, (255, 255, 255))

        self.play_button = Button(self.play_text, 250, 0, self.menu_font, "PLAY")
        self.quit_button = Button(self.quit_text, 350, 0, self.menu_font, "QUIT")

        self.button_list = (self.play_button, self.quit_button)





    def show(self, surface):
        surface.fill(self.background_color)

        for button in self.button_list:
            button.show(surface)

        pygame.display.flip()

    def goto(self, mouse_click):
        if self.button_list[0].pressed(mouse_click):
            return 0
        elif self.button_list[1].pressed(mouse_click):
            return 1
        else:
            return -1
