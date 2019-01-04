# The code is quite bad. I know.

from engine.room import Room, MainMenu
from engine.room_button import Button
import pygame
import pygame.gfxdraw
from random import randint, uniform

version = "v0.4.0"
width = 600
height = 750
running = True


class Player(object):
    def __init__(self):
        self.x = 228
        self.y = 338
        self.width = 57
        self.height = 50
        self.up_force = -32
        self.fly_path = [self.y, 360]
        self.velocity = 0
        self.gravity = 1
        self.in_air = True
        self.fly_speed = 0.3

    def show(self):
        pygame.draw.ellipse(screen, (255, 255, 50), (self.x, self.y, self.width, self.height))
        pygame.draw.circle(screen, (250, 250, 250), (int(self.x) + 42, int(self.y) + 18), 13)  # eye
        pygame.draw.ellipse(screen, (225, 110, 100), (self.x + 31, self.y + 29, 33, 19))  # mouth
        pygame.draw.rect(screen, (60, 60, 60), (self.x + 46, self.y + 15, 4, 7))  # pupil
        pygame.draw.ellipse(screen, (255, 255, 240), (self.x - 7, self.y + 12, 26, 24))  # wing

    def fall(self):
        if start:
            if self.velocity < 10:
                self.velocity += self.gravity
            self.velocity *= 0.9
            self.y += self.velocity

    def up(self):
        if height - 130 >= bird.y > 0 and bird.in_air:
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
        pygame.draw.rect(screen, (50, 230, 50), (self.x, 0, self.width, self.top_height))  # top pipe
        pygame.draw.rect(screen, (50, 230, 50), (self.x, height - self.bottom_height - self.pipe_ground,
                                                 self.width, self.bottom_height))  # bottom pipe
        pygame.draw.rect(screen, (43, 223, 43), (self.x - 4, self.start_gap - 50, self.width + 8, 50))  # top cap
        pygame.draw.rect(screen, (43, 223, 43), (self.x - 4, height - self.bottom_height - self.pipe_ground,
                                                 self.width + 8, 50))  # bottom cap
        pygame.draw.rect(screen, (240, 252, 152), (0, height - self.pipe_ground, width, self.pipe_ground))  # ground
        pygame.draw.rect(screen, (50, 250, 50), (0, height - self.pipe_ground, width, 20))  # grass

    def move(self, bird_):
        if bird_.in_air:
            self.x -= self.vel

    def offscreen(self):
        if self.x < 0 - self.width:
            return True
        else:
            return False

    def hit(self, bird_):
        if bird_.y < self.top_height or bird_.y + bird_.height > height - self.bottom_height - self.pipe_ground:
            if bird_.x + bird_.width > self.x and bird_.x < self.x + self.width:
                return True
        else:
            return False

    def score_up(self, bird_):
        if bird_.x < self.x < bird_.x + 4:
            # print "SCORE"
            return True
        else:
            return False


class Dirt(object):
    def __init__(self):
        self.y = randint(height - 95, height - 5)
        self.width = randint(4, 15)
        self.height = randint(4, 11)
        self.x = randint(0, width - 1)
        self.color = (randint(114, 171), randint(76, 113), randint(26, 83))
        self.vel = 3.2

    def show(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self, bird_):
        if bird_.in_air:
            self.x -= self.vel

    def offscreen(self):
        if self.x < 0 - self.width:
            return True
        else:
            return False


class Cloud(object):
    def __init__(self):
        self.y = randint(-8, 80)
        self.width = randint(80, 170)
        self.height = randint(40, 70)
        self.x = randint(-10, width + 10)
        self.vel = uniform(0.1, 0.4)
        self.color = (randint(247, 255), randint(247, 255), 255, 180)
        self.limit = 1

    def move(self):
        self.x -= self.vel

    def show(self):
        # pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        pygame.gfxdraw.filled_ellipse(screen, int(self.x), int(self.y), self.width, self.height, self.color)

    def offscreen(self):
        if self.x < 0 - self.width:
            return True
        else:
            return False

    def reality(self, bird_):
        if not bird_.in_air and self.limit == 1:
            self.limit -= 1
            self.vel *= 0.1


def check_data_file():  # checks if the file exists
    try:
        open("Data\\Data.txt")  # todo check to see if the file is closed
    except IOError:
        data_file = open("Data\\Data.txt", "w")
        data_file.write("000@0")
        data_file.close()
        print "Data file not found; creating a new one."


def save_load_best():  # saves and loads the best score
    score_ = score
    with open("Data\\Data.txt", "r+") as data_file:
        prev_best_score = int(data_file.read()[:3])
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
        else:
            if start:
                prev_times_played += 1
            data_file.seek(4)
            data_file.write(str(prev_times_played))
            return prev_times_played


def load_data():
    with open("Data\\Data.txt", "r") as data_file:
        best_score = int(data_file.read()[:3])
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
        screen.blit(instructions_text, (width / 2 - 160, height / 2 + 150))


def show_fps():
    fps = clock.get_fps()
    fps_text = fps_font.render("FPS: " + str(int(fps * 1000 + 0.5) / 1000.0), False, (0, 0, 0))
    screen.blit(fps_text, (10, height - 20))


def show_version():
    ver_text = ver_font.render(version, False, (0, 0, 0))
    screen.blit(ver_text, (width - 45, height - 20))


def game_over_room():
    global current_room, restart_times

    end_score_text = end_score_font.render("Score: " + str(score), True, (0, 0, 0))
    best_score_text = best_score_font.render("Best: " + save_load_best(), True, (0, 0, 0))
    button_font = pygame.font.SysFont("calibri", 52, True)
    text1 = button_font.render("Replay", True, (0, 0, 0))
    text2 = button_font.render("Exit", True, (0, 0, 0))
    button1 = Button(text1, (width / 2 - 140, height / 2 + 80), (255, 16, 16), button_font, "Replay")
    button2 = Button(text2, (width / 2 + 55, height / 2 + 80), (255, 16, 16), button_font, "Exit")
    buttons = (button1, button2)

    game_over = Room(game_over_text, buttons)

    while game_over.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over.exit()
                current_room = quit
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and not bird.in_air:
                restart_times += 1
                # print restart_times
                game_over.exit()
                current_room = game_room
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_over.exit()
                current_room = main_room
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over.button_pressed() == 0:
                    game_over.exit()
                    current_room = game_room
                elif game_over.button_pressed() == 1:
                    game_over.exit()
                    current_room = main_room

        end_background.fill((255, 255, 170, 190))
        screen.blit(end_background, (100, 165))
        game_over.show(screen, (width / 2 - 165, 240))
        screen.blit(end_score_text, (width / 2 - 145, 360))
        screen.blit(best_score_text, (width / 2 + 35, 361))
        pygame.display.flip()
        clock.tick(48)


def ask_reset_room():
    global current_room

    title_font = pygame.font.SysFont("calibri", 55, True)
    button_font = pygame.font.SysFont("calibri", 50, True)
    title_text = title_font.render("Are you sure?", True, (0, 0, 0))
    text1 = button_font.render("Yes", True, (0, 0, 0))
    text2 = button_font.render("Cancel", True, (0, 0, 0))
    button1 = Button(text1, (width / 2 - 120, height / 2 + 80), (255, 16, 16), button_font, "Yes")  # todo revise this
    button2 = Button(text2, (width / 2 + 5, height / 2 + 80), (255, 16, 16), button_font, "Cancel")
    buttons = (button1, button2)
    background = pygame.Surface((380, 250), pygame.SRCALPHA)
    q = True  # if the exit button is pressed, 'q' is set to False

    ask_reset = Room(title_text, buttons)

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

        background.fill((235, 235, 110))
        screen.blit(background, (120, 275))
        ask_reset.show(screen, (155, 340))
        pygame.display.flip()
        clock.tick(48)
    return q


def drawing():
    global timer, restart_times

    screen.fill((150, 200, 255))

    if bird.in_air and timer == 0:
        if start:
            pipes.append(Pipe())
        timer = 120
        # print len(pipes)

    for cloud in reversed(clouds):  # clouds
        cloud.show()
        cloud.move()
        cloud.reality(bird)
        if cloud.offscreen() and bird.in_air:  # todo update cloud class
            cloud.y = randint(-8, 80)
            cloud.width = randint(80, 170)
            cloud.height = randint(40, 70)
            cloud.x = randint(width + 160, width + 550)
            cloud.vel = uniform(0.1, 0.4)
            cloud.color = (randint(247, 255), randint(247, 255), 255, 180)

    for pipe in reversed(pipes):  # pipes
        pipe.show()
        pipe.move(bird)
        if pipe.offscreen():
            del pipes[1]

    for dirt in reversed(dirts):  # dirts
        dirt.show()
        dirt.move(bird)
        if dirt.offscreen():
            dirt.y = randint(height - 95, height - 5)  # todo update dirt class
            dirt.width = randint(4, 15)
            dirt.height = randint(4, 11)
            dirt.x = width + randint(10, 80)
            dirt.color = (randint(114, 171), randint(76, 113), randint(26, 83))

    bird.show()
    bird.fly()
    bird.fall()

    show_instructions()
    show_score()
    show_fps()

    pygame.display.flip()


def game_room():
    global current_room, score, timer, start, bird, pipes, dirts, clouds

    timer = 120  # for spawning pipes
    score = 0
    start = False  # if player starts to jump
    bird = Player()
    pipes = [Pipe()]
    dirts = []
    clouds = []
    for i in range(7):
        dirts.append(Dirt())
    for i in range(4):
        clouds.append(Cloud())

    game = Room()

    while game.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.exit()
                current_room = quit
                # print "QUIT"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.KEYDOWN and event.key == pygame.K_UP or \
                    event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                start = True
                bird.up()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game.exit()
                current_room = main_room

        for pipe in pipes:  # checking for pipe-bird events
            if pipe.hit(bird):
                # print "HIT"
                bird.in_air = False
                game_over_room()
                game.exit()
            elif pipe.score_up(bird) and bird.in_air:
                # print "SCORE"
                score += 1
                # print score

        if bird.y + bird.height >= height - 105:
            bird.velocity = 0
            bird.gravity = 0
            bird.in_air = False
            game_over_room()
            game.exit()

        if start:
            timer -= 1

        drawing()
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
    button1 = Button((width / 2 - 80, height / 2 - 25), (255, 16, 16), play_button_font, "PLAY", colors, True)
    button2 = Button((width / 2 - 80, height / 2 + 75), (255, 16, 16), button_font, "OPTIONS", colors, True)
    button3 = Button((width / 2 - 80, height / 2 + 150), (255, 16, 16), button_font, "INSTRUCTIONS", colors, True)
    button4 = Button((width / 2 - 80, height / 2 + 225), (255, 16, 16), button_font, "QUIT", colors, True)
    buttons = (button1, button2, button3, button4)

    main = MainMenu(title_text, (230, 230, 16), buttons)

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
                elif main.button_pressed() == 2:  # todo implement INSTRUCTIONS button
                    pass
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
    text1 = button_font.render("RESET DATA", True, (0, 0, 0))
    text2 = button_font.render("INFO", True, (0, 0, 0))
    text3 = button_font.render("BACK", True, (0, 0, 0))
    button1 = Button(text1, (width / 2 - 80, height / 2 + 75), (255, 16, 16), button_font, "RESET DATA")
    button2 = Button(text2, (width / 2 - 80, height / 2 + 150), (255, 16, 16), button_font, "INFO")
    button3 = Button(text3, (width / 2 - 80, height / 2 + 225), (255, 16, 16), button_font, "BACK")
    buttons = (button1, button2, button3)

    options = MainMenu(title_text, (200, 200, 16), buttons)

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
                    pass
                elif options.button_pressed() == 2:
                    options.exit()
                    current_room = main_room

        options.show(screen, (230, 270))
        pygame.display.flip()
        clock.tick(48)


def quit():
    global running
    running = False


pygame.init()
pygame.display.set_icon(pygame.image.load("Data\\BirbIcon.png"))
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Birb")
clock = pygame.time.Clock()
restart_times = 0  # how many times the user restarts

score_font = pygame.font.SysFont("calibri", 65, True)  # score
instructions_font = pygame.font.SysFont("calibri", 18, True)  # instructions
instructions_text = instructions_font.render("Press Spacebar or Up Arrow to get started.", True, (0, 0, 0))
end_score_font = pygame.font.SysFont("calibri", 40, True)  # end score
game_over_font = pygame.font.SysFont("calibri", 70, True)  # game_over
game_over_text = game_over_font.render("Game Over", True, (0, 0, 0))
best_score_font = pygame.font.SysFont("calibri", 35, True)  # best score
fps_font = pygame.font.SysFont("calibri", 15, True)  # fps
ver_font = pygame.font.SysFont("calibri", 15, True)  # version
end_background = pygame.Surface((400, 410), pygame.SRCALPHA)  # for ending description rectangle thingy

current_room = main_room

while running:
    current_room()

pygame.quit()  # Written by Simon. Inspired by The Coding Train.
