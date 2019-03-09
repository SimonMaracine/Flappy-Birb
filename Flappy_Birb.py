# The code is quite bad. I know.

from engine.room import Room, MainMenu, Settings
from engine.room_button import Button
from engine.room_slider import VolumeSlider
from engine.useful_functions import load_image
import pygame
from random import randint

version = "v1.1.0"
width = 600
height = 750
SCL = 1
running = True
fullscreen = True


class Player(object):
    def __init__(self):
        self.x = 228 * SCL
        self.y = 338 * SCL
        self.width = 57 * SCL
        self.height = 50 * SCL
        self.up_force = -33.8 * SCL
        self.fly_path = [self.y, 360 * SCL]
        self.velocity = 0
        self.gravity = 1.07 * SCL
        self.in_air = True
        self.fly_speed = 0.36 * SCL
        self.sprite_count = 0

    def show(self):
        if self.sprite_count > 18:
            self.sprite_count = 0
        if not start:
            screen.blit(bird2, (self.x - 6 * SCL, self.y - 1 * SCL))
        else:
            screen.blit(bird_sprites[self.sprite_count / 7], (self.x - 10 * SCL, self.y - 10 * SCL))
            self.sprite_count += 1
        # pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width + 3, self.height), 2)

    def fall(self):
        if start:
            if self.velocity < 10:
                self.velocity += self.gravity
            self.velocity *= 0.905
            self.y += self.velocity

    def up(self):
        if height - 130 * SCL >= self.y > 0 and self.in_air:
            self.velocity += self.up_force

    def fly(self):
        if not start:
            # print "FLYING"
            if self.y < self.fly_path[1]:
                self.y += self.fly_speed
            else:
                self.fly_speed *= -1
            if self.y > self.fly_path[0]:
                self.y += self.fly_speed
            else:
                self.fly_speed *= -1


class Pipe(object):
    def __init__(self):
        self.x = width + 350 * SCL
        self.width = 105 * SCL
        self.gap = 204 * SCL
        self.pipe_ground = 115 * SCL
        self.start_gap = randint(int(25 * SCL), int(height - 25 * SCL - self.gap - self.pipe_ground))
        self.top_height = self.start_gap
        self.bottom_height = height - self.start_gap - self.gap - self.pipe_ground
        if start:
            self.vel = 3.2 * SCL
        else:
            self.vel = 0

    def show(self):
        screen.blit(pipe1, (self.x - 4 * SCL, self.start_gap - height))
        screen.blit(pipe2, (self.x - 4 * SCL, self.start_gap + self.gap))

    def move(self, bird_):
        if bird_.in_air:
            self.x -= self.vel

    def offscreen(self):
        if self.x < 0 - self.width:
            return True
        else:
            return False

    def hit(self, bird_):
        if bird_.y + 8 * SCL < self.top_height or bird_.y + bird_.height - 7 * SCL > height - self.bottom_height - self.pipe_ground:
            if bird_.x - 4 * SCL + bird_.width > self.x and bird_.x + 4 * SCL < self.x + self.width + 3 * SCL:
                return True
        else:
            return False

    def score_up(self, bird_):
        if bird_.x < self.x < bird_.x + 4 * SCL:
            # print "SCORE"
            return True
        else:
            return False


class Ground(object):
    def __init__(self):
        self.x = 0
        self.height = 105 * SCL
        self.vel = 3.2 * SCL

    def show(self):
        screen.blit(ground, (self.x, height - self.height))
        screen.blit(ground, (width + self.x, height - self.height))
        if self.offscreen():
            self.x = -1

    def move(self):
        self.x -= self.vel

    def offscreen(self):
        if width + self.x < 0:
            return True
        else:
            return False


def check_data_file():  # checks if the file exists
    try:
        open("Data\\Data.txt")
    except IOError:
        data_file = open("Data\\Data.txt", "w")
        data_file.write("000@1.00@0")
        data_file.close()
        print "Data file not found; creating a new one."


def save_load_best():  # saves and loads the best score
    score_ = score
    with open("Data\\Data.txt", "r+") as data_file:
        try:
            prev_best_score = int(data_file.read()[:3])
        except ValueError:
            data_file = open("Data\\Data.txt", "w")
            data_file.write("000@1.00@0")
            data_file.close()
            print "An error occurred; created a new data file."
            return "0"
        else:
            nr_char = len(str(score_))

            if nr_char == 1:
                seek = 2
            elif nr_char == 2:
                seek = 1
            else:
                seek = 0

            if score_ > prev_best_score:
                data_file.seek(seek)
                data_file.write(str(score_))
                return str(score_)
            else:
                return str(prev_best_score)


def statistics():  # saves how many times the user has played
    with open("Data\\Data.txt", "r+") as data_file:
        try:
            prev_times_played = int(data_file.read()[9:])
        except ValueError:
            data_file = open("Data\\Data.txt", "w")
            data_file.write("000@1.00@0")
            data_file.close()
            print "An error occurred; created a new data file."
            return 0
        else:
            if start:
                prev_times_played += 1
            data_file.seek(9)
            data_file.write(str(prev_times_played))
            return prev_times_played


def load_data():
    with open("Data\\Data.txt", "r") as data_file:
        try:
            best_score = int(data_file.read()[:3])
        except ValueError:
            data_file = open("Data\\Data.txt", "w")
            data_file.write("000@1.00@0")
            data_file.close()
            print "An error occurred; created a new data file."
            return 0, "0"
        else:
            data_file.seek(0)
            times_played = data_file.read()[9:]
            return best_score, times_played


def erase_data():
    with open("Data\\Data.txt", "w") as data_file:
        data_file.write("000@1.00@0")
    print "Data erased."


def switch_fullscreen():
    global fullscreen

    if not fullscreen:
        fullscreen = True
        return pygame.display.set_mode((width, height))
    else:
        fullscreen = False
        return pygame.display.set_mode((width, height), pygame.FULLSCREEN)


def change_sound_volume(volume=None, slider=None):
    if slider is not None:
        for sound in all_sounds:
            sound.set_volume(slider.volume)
    else:
        for sound in all_sounds:
            sound.set_volume(volume)


def get_sound_volume():
    with open("Data\\Data.txt", "r") as data:
        return float(data.read()[4:7])


def show_score():  # shows the score while playing
    if start:
        score_text = score_font.render(str(score), True, (0, 0, 0))
        screen.blit(score_text, (width / 2 - 10 * SCL, 130 * SCL))


def show_instructions():  # shows the instructions at the beginning (only once)
    if not start and restart_times < 1:
        screen.blit(instructions_text, (width / 2 - 140 * SCL, height / 2 + 150 * SCL))


def show_fps():
    fps = clock.get_fps()
    fps_text = fps_font.render("FPS: " + str(int(fps * 1000 + 0.5) / 1000.0), False, (0, 0, 0))
    screen.blit(fps_text, (10 * SCL, height - 20 * SCL))


def show_version():
    ver_text = ver_font.render(version, False, (0, 0, 0))
    screen.blit(ver_text, (width - 45 * SCL, height - 20 * SCL))


def game_over_room(bird_):
    global current_room, restart_times

    end_score_text = end_score_font.render("Score: " + str(score), True, (0, 0, 0))
    best_score_text = end_score_font.render("Best: " + save_load_best(), True, (0, 0, 0))
    button_font = pygame.font.SysFont("calibri", int(52 * SCL), True)
    colors = ((0, 0, 0), (235, 212, 222))
    button1 = Button((width / 2 - 145 * SCL, height / 2 + 80 * SCL), (255, 16, 16), button_font, "Replay", colors, True)
    button2 = Button((width / 2 + 55 * SCL, height / 2 + 80 * SCL), (255, 16, 16), button_font, "Exit", colors, True)
    buttons = (button1, button2)

    game_over = Room(game_over_text, buttons, button_sound)

    while game_over.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over.exit()
                current_room = quit
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and not bird_.in_air:
                restart_times += 1
                # print restart_times
                game_over.exit()
                current_room = game_room
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_over.exit()
                current_room = main_room
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over.button_pressed() == 0:
                    restart_times += 1
                    game_over.exit()
                    current_room = game_room
                elif game_over.button_pressed() == 1:
                    game_over.exit()
                    current_room = main_room

        end_background.fill((255, 255, 170))
        screen.blit(end_background, (100 * SCL, 165 * SCL))
        pygame.draw.rect(screen, (200, 0, 0), (98 * SCL, 163 * SCL, 400 * SCL, 410 * SCL), 6)
        game_over.show(screen, (width / 2 - 165 * SCL, 240 * SCL))
        screen.blit(end_score_text, (width / 2 - 145 * SCL, 360 * SCL))
        screen.blit(best_score_text, (width / 2 + 35 * SCL, 360 * SCL))
        pygame.display.flip()
        clock.tick(48)


def ask_reset_room():
    global current_room

    title_font = pygame.font.SysFont("calibri", int(55 * SCL), True)
    button_font = pygame.font.SysFont("calibri", int(50 * SCL), True)
    title_text = title_font.render("Are you sure?", True, (0, 0, 0))
    colors = ((0, 0, 0), (235, 212, 222))
    button1 = Button((width / 2 - 120 * SCL, height / 2 + 80 * SCL), (255, 16, 16), button_font, "Yes", colors, True)
    button2 = Button((width / 2 * SCL, height / 2 + 80 * SCL), (255, 16, 16), button_font, "Cancel", colors, True)
    buttons = (button1, button2)
    background = pygame.Surface((380 * SCL, 250 * SCL), pygame.SRCALPHA)
    q = True  # if the exit button is pressed, 'q' is set to False

    ask_reset = Room(title_text, buttons, button_sound)

    while ask_reset.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ask_reset.exit()
                q = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ask_reset.button_pressed() == 0:
                    erase_data()
                    ask_reset.exit()
                elif ask_reset.button_pressed() == 1:
                    ask_reset.exit()

        background.fill((220, 220, 110))
        screen.blit(background, (115 * SCL, 275 * SCL))
        ask_reset.show(screen, (150 * SCL, 340 * SCL))
        pygame.display.flip()
        clock.tick(48)
    return q


def instructions_room():
    global current_room

    title_font = pygame.font.SysFont("calibri", int(80 * SCL), True)
    button_font = pygame.font.SysFont("calibri", int(60 * SCL), True)
    that_font = pygame.font.SysFont("calibri", int(25 * SCL), True)
    that_font2 = pygame.font.SysFont("calibri", int(30 * SCL), True)
    title_text = title_font.render("Instructions", True, (0, 0, 0))
    txt1 = that_font2.render("Objective:", True, (0, 0, 0))
    txt2 = that_font.render("Navigate the bird through the green pipes.", True, (0, 0, 0))
    txt3 = that_font2.render("Controls:", True, (0, 0, 0))
    txt4 = that_font.render("Press Spacebar, Up Arrow or simply left-click to flap.", True, (0, 0, 0))
    txt5 = that_font.render("Quit at anytime by pressing Escape or restart with R.", True, (0, 0, 0))
    colors = ((0, 0, 0), (235, 212, 222))
    button = Button((width / 2 + 40 * SCL, height / 2 + 225 * SCL), (255, 16, 16), button_font, "BACK", colors, True)
    buttons = (button,)

    instructions = MainMenu(title_text, (200, 200, 16), buttons, button_sound)

    while instructions.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                instructions.exit()
                current_room = quit
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if instructions.button_pressed() == 0:
                    instructions.exit()
                    current_room = main_room

        instructions.show(screen, (100 * SCL, 160 * SCL))
        screen.blit(txt1, (20 * SCL, 295 * SCL))
        screen.blit(txt2, (20 * SCL, 330 * SCL))
        screen.blit(txt3, (20 * SCL, 400 * SCL))
        screen.blit(txt4, (20 * SCL, 435 * SCL))
        screen.blit(txt5, (20 * SCL, 520 * SCL))
        pygame.display.flip()
        clock.tick(48)


def info_room():
    global current_room

    title_font = pygame.font.SysFont("calibri", int(80 * SCL), True)
    button_font = pygame.font.SysFont("calibri", int(60 * SCL), True)
    that_font = pygame.font.SysFont("calibri", int(40 * SCL), True)
    that_font2 = pygame.font.SysFont("calibri", int(15 * SCL), True)
    title_text = title_font.render("Info", True, (0, 0, 0))
    txt1 = that_font.render("Flappy Bird", True, (0, 0, 0))
    txt2 = that_font.render("clone", True, (0, 0, 0))
    txt3 = that_font.render("by Simon", True, (0, 0, 0))
    txt4 = that_font2.render("I do not expect anyone to play this.", True, (0, 0, 0))
    colors = ((0, 0, 0), (235, 212, 222))
    button = Button((width / 2 + 40 * SCL, height / 2 + 225 * SCL), (255, 16, 16), button_font, "BACK", colors, True)
    buttons = (button,)

    info = MainMenu(title_text, (200, 200, 16), buttons, button_sound)

    while info.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                info.exit()
                current_room = quit
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if info.button_pressed() == 0:
                    info.exit()
                    current_room = options_room

        info.show(screen, (240 * SCL, 170 * SCL))
        screen.blit(txt1, (width / 2 - 79 * SCL, 310 * SCL))
        screen.blit(txt2, (width / 2 - 34 * SCL, 370 * SCL))
        screen.blit(txt3, (width / 2 - 63 * SCL, 430 * SCL))
        screen.blit(txt4, (width / 2 + 20 * SCL, 520 * SCL))
        pygame.display.flip()
        clock.tick(48)


def sound_room():
    global current_room

    title_font = pygame.font.SysFont("calibri", int(80 * SCL), True)
    button_font = pygame.font.SysFont("calibri", int(60 * SCL), True)
    title_text = title_font.render("Volume", True, (0, 0, 0))
    colors = ((0, 0, 0), (235, 212, 222))
    button1 = Button((width / 2 - 260 * SCL, height / 2 + 160 * SCL), (255, 16, 16), button_font, "Save", colors, True)
    button2 = Button((width / 2 - 120 * SCL, height / 2 + 160 * SCL), (255, 16, 16), button_font, "Cancel", colors, True)
    button3 = Button((width / 2 + 100 * SCL, height / 2 + 160 * SCL), (255, 16, 16), button_font, "Reset", colors, True)
    slider = VolumeSlider((width / 2 - 200 * SCL, height / 2 + 40 * SCL), (255, 16, 16), colors, (400 * SCL, 60 * SCL))
    buttons = (button1, button2, button3)
    sliders = (slider,)

    sound = Settings(title_text, (200, 200, 16), buttons, button_sound, sliders)

    slider.get_volume("Data\\Data.txt")

    while sound.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sound.exit()
                current_room = quit
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if sound.button_pressed() == 0:
                    change_sound_volume(None, slider)
                    slider.set_volume("Data\\Data.txt")
                    sound.exit()
                    current_room = options_room
                elif sound.button_pressed() == 1:
                    sound.exit()
                    current_room = options_room
                elif sound.button_pressed() == 2:
                    slider.reset_volume()

        sound.show(screen, (175 * SCL, 250 * SCL))
        pygame.display.flip()
        clock.tick(48)


def drawing(bird_, pipes_, ground_):
    global timer

    screen.blit(background, (0, 0))

    if bird_.in_air and timer <= 0:
        if start:
            pipes_.append(Pipe())
        timer = 120
        # print len(pipes)

    for pipe in reversed(pipes_):  # pipes
        pipe.show()
        pipe.move(bird_)
        if pipe.offscreen():
            del pipes_[1]

    ground_.show()
    ground_.move()

    bird_.show()
    bird_.fly()
    bird_.fall()

    show_instructions()
    show_score()
    show_fps()

    pygame.display.flip()


def game_room():
    global current_room, score, timer, start

    timer = 120  # for spawning pipes
    score = 0
    start = False  # if player starts to jump
    bird = Player()
    pipes = [Pipe()]
    ground = Ground()

    game = Room()

    while game.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.exit()
                current_room = quit
                # print "QUIT"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.KEYDOWN and event.key == pygame.K_UP or \
                    event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                flap_sound.play()
                start = True
                bird.up()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game.exit()
                current_room = main_room

        for pipe in pipes:  # checking for pipe-bird events
            if pipe.hit(bird):
                hit_sound.play()
                pygame.time.wait(200)
                # print "HIT"
                bird.in_air = False
                game_over_room(bird)
                game.exit()
            elif pipe.score_up(bird) and bird.in_air:
                ding_sound.play()
                score += 1
                # print "SCORE"
                # print score

        if bird.y + bird.height >= height - 95 * SCL:
            bird.velocity = 0
            bird.gravity = 0
            hit_sound.play()
            pygame.time.wait(200)
            bird.in_air = False
            game_over_room(bird)
            game.exit()

        if start:
            timer -= 1 * SCL

        drawing(bird, pipes, ground)
        clock.tick(65)

    check_data_file()
    save_load_best()
    statistics()


def main_room():
    global current_room

    title_font = pygame.font.SysFont("calibri", int(100 * SCL), True)
    play_button_font = pygame.font.SysFont("calibri", int(75 * SCL), True)
    button_font = pygame.font.SysFont("calibri", int(60 * SCL), True)
    that_font = pygame.font.SysFont("calibri", int(35 * SCL), True)
    title_text = title_font.render("Flappy Birb", True, (0, 0, 0))
    colors = ((0, 0, 0), (235, 212, 222))
    button1 = Button((width / 2 - 90 * SCL, height / 2 - 25 * SCL), (255, 16, 16), play_button_font, "PLAY", colors, True)
    button2 = Button((width / 2 - 90 * SCL, height / 2 + 75 * SCL), (255, 16, 16), button_font, "OPTIONS", colors, True)
    button3 = Button((width / 2 - 90 * SCL, height / 2 + 150 * SCL), (255, 16, 16), button_font, "INSTRUCTIONS", colors, True)
    button4 = Button((width / 2 - 90 * SCL, height / 2 + 225 * SCL), (255, 16, 16), button_font, "QUIT", colors, True)
    buttons = (button1, button2, button3, button4)

    main = MainMenu(title_text, (230, 230, 16), buttons, button_sound)

    check_data_file()
    best_score = str(load_data()[0])
    times_played = load_data()[1]

    while main.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.exit()
                current_room = quit
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if main.button_pressed() == 0:
                    main.exit()
                    current_room = game_room
                elif main.button_pressed() == 1:
                    main.exit()
                    current_room = options_room
                elif main.button_pressed() == 2:
                    main.exit()
                    current_room = instructions_room
                elif main.button_pressed() == 3:
                    main.exit()
                    current_room = quit

        main.show(screen, (75 * SCL, 50 * SCL))
        score_text = that_font.render("Best score: " + best_score, True, (0, 0, 0))
        times_text = that_font.render("Times played: " + times_played, True, (0, 0, 0))
        screen.blit(score_text, (100 * SCL, 220 * SCL))
        screen.blit(times_text, (100 * SCL, 270 * SCL))
        show_version()
        pygame.display.flip()
        clock.tick(48)


def options_room():
    global current_room, screen

    title_font = pygame.font.SysFont("calibri", int(80 * SCL), True)
    button_font = pygame.font.SysFont("calibri", int(60 * SCL), True)
    title_text = title_font.render("Options", True, (0, 0, 0))
    colors = ((0, 0, 0), (235, 212, 222))
    button1 = Button((width / 2 - 90 * SCL, height / 2 - 75), (255, 16, 16), button_font, "RESET DATA", colors, True)
    button2 = Button((width / 2 - 90 * SCL, height / 2), (255, 16, 16), button_font, "INFO", colors, True)
    button3 = Button((width / 2 - 90 * SCL, height / 2 + 75 * SCL), (255, 16, 16), button_font, "VOLUME", colors, True)
    button4 = Button((width / 2 - 90 * SCL, height / 2 + 150 * SCL), (255, 16, 16), button_font, "FULLSCREEN", colors, True)
    button5 = Button((width / 2 - 90 * SCL, height / 2 + 225 * SCL), (255, 16, 16), button_font, "BACK", colors, True)
    buttons = (button1, button2, button3, button4, button5)

    options = MainMenu(title_text, (200, 200, 16), buttons, button_sound)

    while options.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                options.exit()
                current_room = quit
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if options.button_pressed() == 0:
                    if not ask_reset_room():
                        options.exit()
                        current_room = quit
                elif options.button_pressed() == 1:
                    options.exit()
                    current_room = info_room
                elif options.button_pressed() == 2:
                    options.exit()
                    current_room = sound_room
                elif options.button_pressed() == 3:
                    screen = switch_fullscreen()
                elif options.button_pressed() == 4:
                    options.exit()
                    current_room = main_room

        options.show(screen, (225 * SCL, 180 * SCL))
        pygame.display.flip()
        clock.tick(48)


def quit():
    global running
    pygame.time.delay(120)
    running = False


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
info = pygame.display.Info()
if info.current_h <= 768:
    width = 560
    height = 700
    SCL = 0.933
pygame.display.set_icon(pygame.image.load("Data\\Assets\\BirbIcon2.png"))
screen = switch_fullscreen()
pygame.display.set_caption("Flappy Birb")
clock = pygame.time.Clock()
restart_times = 0  # how many times the user restarts
volume = get_sound_volume()

score_font = pygame.font.SysFont("calibri", int(65 * SCL), True)  # score
instructions_font = pygame.font.SysFont("calibri", int(20 * SCL), True)  # instructions
instructions_text = instructions_font.render("Press the spacebar to get started.", True, (0, 0, 0))
end_score_font = pygame.font.SysFont("calibri", int(38 * SCL), True)  # end score
game_over_font = pygame.font.SysFont("calibri", int(70 * SCL), True)  # game_over
game_over_text = game_over_font.render("Game Over", True, (0, 0, 0))
fps_font = pygame.font.SysFont("calibri", int(15 * SCL), True)  # fps
ver_font = pygame.font.SysFont("calibri", int(15 * SCL), True)  # version
end_background = pygame.Surface((400 * SCL, 410 * SCL), pygame.SRCALPHA)  # for ending description rectangle thingy

background = load_image("Data\\Assets\\Background.png").convert()
background = pygame.transform.scale(background, (width, int(height - 85 * SCL)))
ground = load_image("Data\\Assets\\Ground.png").convert()
ground = pygame.transform.scale(ground, (width, int(105 * SCL + 1)))
pipe = load_image("Data\\Assets\\Pipe.png").convert_alpha()
pipe1 = pygame.transform.scale(pipe, (int(113 * SCL), height))
pipe2 = pygame.transform.flip(pipe1, False, True)
bird1 = load_image("Data\\Assets\\Bird1.png").convert_alpha()
bird1 = pygame.transform.scale(bird1, (int(73 * SCL), int(52 * SCL)))
bird2 = load_image("Data\\Assets\\Bird2.png").convert_alpha()
bird2 = pygame.transform.scale(bird2, (int(73 * SCL), int(52 * SCL)))
bird3 = load_image("Data\\Assets\\Bird3.png").convert_alpha()
bird3 = pygame.transform.scale(bird3, (int(73 * SCL), int(52 * SCL)))
bird_sprite1 = pygame.transform.rotate(bird1, 22)
bird_sprite2 = pygame.transform.rotate(bird2, 22)
bird_sprite3 = pygame.transform.rotate(bird3, 22)
bird_sprites = (bird_sprite1, bird_sprite2, bird_sprite3)
button_sound = pygame.mixer.Sound("Data\\Sounds\\Button.wav")
hit_sound = pygame.mixer.Sound("Data\\Sounds\\Hit.wav")
flap_sound = pygame.mixer.Sound("Data\\Sounds\\Flap.wav")
ding_sound = pygame.mixer.Sound("Data\\Sounds\\Ding.wav")
all_sounds = (button_sound, hit_sound, flap_sound, ding_sound)

change_sound_volume(volume)
current_room = main_room

while running:
    current_room()

pygame.quit()  # Written by Simon. Inspired by The Coding Train.
