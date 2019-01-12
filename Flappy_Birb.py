# The code is quite bad. I know.

from engine.room import Room, MainMenu
from engine.room_button import Button
from engine.useful_functions import load_image
import pygame
from random import randint

version = "v1.0.0"
width = 600
height = 750
running = True

class Player(object):
    def __init__(self):
        self.x = 228
        self.y = 338
        self.width = 57
        self.height = 50
        self.up_force = -33.8
        self.fly_path = [self.y, 360]
        self.velocity = 0
        self.gravity = 1.07
        self.in_air = True
        self.fly_speed = 0.36
        self.sprite_count = 0

    def show(self):
        if self.sprite_count > 18:
            self.sprite_count = 0
        if not start:
            screen.blit(bird2, (self.x - 6, self.y - 1))
        else:
            screen.blit(bird_sprites[self.sprite_count / 7], (self.x - 10, self.y - 10))
            self.sprite_count += 1
        # pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width + 3, self.height), 2)

    def fall(self):
        if start:
            if self.velocity < 10:
                self.velocity += self.gravity
            self.velocity *= 0.905
            self.y += self.velocity

    def up(self):
        if height - 130 >= self.y > 0 and self.in_air:
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
        self.x = width + 350
        self.width = 105
        self.gap = 204
        self.pipe_ground = 115
        self.start_gap = randint(25, height - 25 - self.gap - self.pipe_ground)
        self.top_height = self.start_gap
        self.bottom_height = height - self.start_gap - self.gap - self.pipe_ground
        if start:
            self.vel = 3.2
        else:
            self.vel = 0

    def show(self):
        screen.blit(pipe1, (self.x - 4, self.start_gap - height))
        screen.blit(pipe2, (self.x - 4, self.start_gap + self.gap))

    def move(self, bird_):
        if bird_.in_air:
            self.x -= self.vel

    def offscreen(self):
        if self.x < 0 - self.width:
            return True
        else:
            return False

    def hit(self, bird_):
        if bird_.y + 8 < self.top_height or bird_.y + bird_.height - 7 > height - self.bottom_height - self.pipe_ground:
            if bird_.x - 4 + bird_.width > self.x and bird_.x + 4 < self.x + self.width + 3:
                return True
        else:
            return False

    def score_up(self, bird_):
        if bird_.x < self.x < bird_.x + 4:
            # print "SCORE"
            return True
        else:
            return False

class Ground(object):
    def __init__(self):
        self.x = 0
        self.height = 105
        self.vel = 3.2

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
        open("Data\\Data.txt")  # todo check to see if the file is really closed
    except IOError:
        data_file = open("Data\\Data.txt", "w")
        data_file.write("000@0")
        data_file.close()
        print "Data file not found; creating a new one."

def save_load_best():  # saves and loads the best score
    score_ = score
    with open("Data\\Data.txt", "r+") as data_file:
        try:
            prev_best_score = int(data_file.read()[:3])
        except ValueError:
            data_file = open("Data\\Data.txt", "w")
            data_file.write("000@0")
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
            prev_times_played = int(data_file.read()[4:])
        except ValueError:
            data_file = open("Data\\Data.txt", "w")
            data_file.write("000@0")
            data_file.close()
            print "An error occurred; created a new data file."
            return 0
        else:
            if start:
                prev_times_played += 1
            data_file.seek(4)
            data_file.write(str(prev_times_played))
            return prev_times_played

def load_data():
    with open("Data\\Data.txt", "r") as data_file:
        try:
            best_score = int(data_file.read()[:3])
        except ValueError:
            data_file = open("Data\\Data.txt", "w")
            data_file.write("000@0")
            data_file.close()
            print "An error occurred; created a new data file."
            return 0, "0"
        else:
            data_file.seek(0)
            times_played = data_file.read()[4:]
            return best_score, times_played

def erase_data():
    with open("Data\\Data.txt", "w") as data_file:
        data_file.write("000@0")
    print "Data erased."

def show_score():  # shows the score while playing
    if start:
        score_text = score_font.render(str(score), True, (0, 0, 0))
        screen.blit(score_text, (width / 2 - 10, 130))

def show_instructions():  # shows the instructions at the beginning (only once)
    if not start and restart_times < 1:
        screen.blit(instructions_text, (width / 2 - 140, height / 2 + 150))

def show_fps():
    fps = clock.get_fps()
    fps_text = fps_font.render("FPS: " + str(int(fps * 1000 + 0.5) / 1000.0), False, (0, 0, 0))
    screen.blit(fps_text, (10, height - 20))

def show_version():
    ver_text = ver_font.render(version, False, (0, 0, 0))
    screen.blit(ver_text, (width - 45, height - 20))

def game_over_room(bird_):
    global current_room, restart_times

    end_score_text = end_score_font.render("Score: " + str(score), True, (0, 0, 0))
    best_score_text = end_score_font.render("Best: " + save_load_best(), True, (0, 0, 0))
    button_font = pygame.font.SysFont("calibri", 52, True)
    colors = ((0, 0, 0), (235, 212, 222))
    button1 = Button((width / 2 - 145, height / 2 + 80), (255, 16, 16), button_font, "Replay", colors, True)
    button2 = Button((width / 2 + 55, height / 2 + 80), (255, 16, 16), button_font, "Exit", colors, True)
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
        screen.blit(end_background, (100, 165))
        game_over.show(screen, (width / 2 - 165, 240))
        screen.blit(end_score_text, (width / 2 - 145, 360))
        screen.blit(best_score_text, (width / 2 + 35, 360))
        pygame.display.flip()
        clock.tick(48)

def ask_reset_room():
    global current_room

    title_font = pygame.font.SysFont("calibri", 55, True)
    button_font = pygame.font.SysFont("calibri", 50, True)
    title_text = title_font.render("Are you sure?", True, (0, 0, 0))
    colors = ((0, 0, 0), (235, 212, 222))
    button1 = Button((width / 2 - 120, height / 2 + 80), (255, 16, 16), button_font, "Yes", colors, True)
    button2 = Button((width / 2, height / 2 + 80), (255, 16, 16), button_font, "Cancel", colors, True)
    buttons = (button1, button2)
    background = pygame.Surface((380, 250), pygame.SRCALPHA)
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
        screen.blit(background, (115, 275))
        ask_reset.show(screen, (150, 340))
        pygame.display.flip()
        clock.tick(48)
    return q

def instructions_room():
    global current_room

    title_font = pygame.font.SysFont("calibri", 80, True)
    button_font = pygame.font.SysFont("calibri", 60, True)
    that_font = pygame.font.SysFont("calibri", 25, True)
    that_font2 = pygame.font.SysFont("calibri", 30, True)
    title_text = title_font.render("Instructions", True, (0, 0, 0))
    txt1 = that_font2.render("Objective:", True, (0, 0, 0))
    txt2 = that_font.render("Navigate the bird through the green pipes.", True, (0, 0, 0))
    txt3 = that_font2.render("Controls:", True, (0, 0, 0))
    txt4 = that_font.render("Press Spacebar, Up Arrow or simply left-click to flap.", True, (0, 0, 0))
    txt5 = that_font.render("Quit at anytime by pressing Escape or restart with R.", True, (0, 0, 0))
    colors = ((0, 0, 0), (235, 212, 222))
    button = Button((width / 2 + 40, height / 2 + 225), (255, 16, 16), button_font, "BACK", colors, True)
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

        instructions.show(screen, (100, 160))
        screen.blit(txt1, (20, 295))
        screen.blit(txt2, (20, 330))
        screen.blit(txt3, (20, 400))
        screen.blit(txt4, (20, 435))
        screen.blit(txt5, (20, 520))
        pygame.display.flip()
        clock.tick(48)

def info_room():
    global current_room

    title_font = pygame.font.SysFont("calibri", 80, True)
    button_font = pygame.font.SysFont("calibri", 60, True)
    that_font = pygame.font.SysFont("calibri", 40, True)
    that_font2 = pygame.font.SysFont("calibri", 15, True)
    title_text = title_font.render("Info", True, (0, 0, 0))
    txt1 = that_font.render("Flappy Bird", True, (0, 0, 0))
    txt2 = that_font.render("clone", True, (0, 0, 0))
    txt3 = that_font.render("by Simon", True, (0, 0, 0))
    txt4 = that_font2.render("I do not expect anyone to play this.", True, (0, 0, 0))
    colors = ((0, 0, 0), (235, 212, 222))
    button = Button((width / 2 + 40, height / 2 + 225), (255, 16, 16), button_font, "BACK", colors, True)
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

        info.show(screen, (240, 170))
        screen.blit(txt1, (width / 2 - 79, 310))
        screen.blit(txt2, (width / 2 - 34, 370))
        screen.blit(txt3, (width / 2 - 63, 430))
        screen.blit(txt4, (width / 2 + 20, 520))
        pygame.display.flip()
        clock.tick(48)

def drawing(bird_, pipes_, ground_):
    global timer

    # screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    if bird_.in_air and timer == 0:
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

        if bird.y + bird.height >= height - 95:
            bird.velocity = 0
            bird.gravity = 0
            hit_sound.play()
            pygame.time.wait(200)
            bird.in_air = False
            game_over_room(bird)
            game.exit()

        if start:
            timer -= 1

        drawing(bird, pipes, ground)
        clock.tick(65)

    check_data_file()
    save_load_best()
    statistics()

def main_room():
    global current_room

    title_font = pygame.font.SysFont("calibri", 100, True)
    play_button_font = pygame.font.SysFont("calibri", 75, True)
    button_font = pygame.font.SysFont("calibri", 60, True)
    that_font = pygame.font.SysFont("calibri", 35, True)
    title_text = title_font.render("Flappy Birb", True, (0, 0, 0))
    colors = ((0, 0, 0), (235, 212, 222))
    button1 = Button((width / 2 - 90, height / 2 - 25), (255, 16, 16), play_button_font, "PLAY", colors, True)
    button2 = Button((width / 2 - 90, height / 2 + 75), (255, 16, 16), button_font, "OPTIONS", colors, True)
    button3 = Button((width / 2 - 90, height / 2 + 150), (255, 16, 16), button_font, "INSTRUCTIONS", colors, True)
    button4 = Button((width / 2 - 90, height / 2 + 225), (255, 16, 16), button_font, "QUIT", colors, True)
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

        main.show(screen, (75, 50))
        score_text = that_font.render("Best score: " + best_score, True, (0, 0, 0))
        times_text = that_font.render("Times played: " + times_played, True, (0, 0, 0))
        screen.blit(score_text, (100, 220))
        screen.blit(times_text, (100, 270))
        show_version()
        pygame.display.flip()
        clock.tick(48)

def options_room():
    global current_room

    title_font = pygame.font.SysFont("calibri", 80, True)
    button_font = pygame.font.SysFont("calibri", 60, True)
    title_text = title_font.render("Options", True, (0, 0, 0))
    colors = ((0, 0, 0), (235, 212, 222))
    button1 = Button((width / 2 - 90, height / 2 + 75), (255, 16, 16), button_font, "RESET DATA", colors, True)
    button2 = Button((width / 2 - 90, height / 2 + 150), (255, 16, 16), button_font, "INFO", colors, True)
    button3 = Button((width / 2 - 90, height / 2 + 225), (255, 16, 16), button_font, "BACK", colors, True)
    buttons = (button1, button2, button3)

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
                    current_room = main_room

        options.show(screen, (225, 270))
        pygame.display.flip()
        clock.tick(48)

def quit():
    global running
    pygame.time.delay(120)
    running = False

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.display.set_icon(pygame.image.load("Data\\Assets\\BirbIcon2.png"))
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Birb")
clock = pygame.time.Clock()
restart_times = 0  # how many times the user restarts

score_font = pygame.font.SysFont("calibri", 65, True)  # score
instructions_font = pygame.font.SysFont("calibri", 20, True)  # instructions
instructions_text = instructions_font.render("Press the spacebar to get started.", True, (0, 0, 0))
end_score_font = pygame.font.SysFont("calibri", 38, True)  # end score
game_over_font = pygame.font.SysFont("calibri", 70, True)  # game_over
game_over_text = game_over_font.render("Game Over", True, (0, 0, 0))
fps_font = pygame.font.SysFont("calibri", 15, True)  # fps
ver_font = pygame.font.SysFont("calibri", 15, True)  # version
end_background = pygame.Surface((400, 410), pygame.SRCALPHA)  # for ending description rectangle thingy

background = load_image("Data\\Assets\\Background2.png").convert()
background = pygame.transform.scale(background, (width, height - 85))
ground = load_image("Data\\Assets\\Ground.png").convert()
ground = pygame.transform.scale(ground, (width, 105))
pipe = load_image("Data\\Assets\\Pipe.png").convert_alpha()
pipe1 = pygame.transform.scale(pipe, (113, height))
pipe2 = pygame.transform.flip(pipe1, False, True)
bird1 = load_image("Data\\Assets\\Bird1.png").convert_alpha()
bird1 = pygame.transform.scale(bird1, (73, 52))
bird2 = load_image("Data\\Assets\\Bird2.png").convert_alpha()
bird2 = pygame.transform.scale(bird2, (73, 52))
bird3 = load_image("Data\\Assets\\Bird3.png").convert_alpha()
bird3 = pygame.transform.scale(bird3, (73, 52))
bird_sprite1 = pygame.transform.rotate(bird1, 22)
bird_sprite2 = pygame.transform.rotate(bird2, 22)
bird_sprite3 = pygame.transform.rotate(bird3, 22)
bird_sprites = (bird_sprite1, bird_sprite2, bird_sprite3)
button_sound = pygame.mixer.Sound("Data\\Sounds\\Button.wav")
hit_sound = pygame.mixer.Sound("Data\\Sounds\\Hit.wav")
flap_sound = pygame.mixer.Sound("Data\\Sounds\\Flap.wav")
ding_sound = pygame.mixer.Sound("Data\\Sounds\\Ding.wav")

current_room = main_room

while running:
    current_room()

pygame.quit()  # Written by Simon. Inspired by The Coding Train.
