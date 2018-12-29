# The code is quite bad. I know.

import pygame
import pygame.gfxdraw
from random import randint, uniform

version = "v0.4.0"

pygame.init()

display_info = pygame.display.Info()  # for deciding which resolution will the game have
if display_info.current_h <= 800:  # checks if user's screen's height is or is not lower than 800
    width = 580
    height = 700
    mode = 0  # scale for those with lower screen resolutions
else:
    width = 600
    height = 750
    mode = 1  # original scale

# The system that I made for choosing the size of the objects is quite inefficient. I didn't bother changing it. But at least it works.

pygame.display.set_icon(pygame.image.load("Data\\BirbIcon.png"))
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Birb")
clock = pygame.time.Clock()
restart_times = 0  # how many times the user restarts
playing = True

score_font = pygame.font.SysFont("calibri", 65, True)  # score
instructions_font = pygame.font.SysFont("calibri", 18, True)  # instructions
instructions_text = instructions_font.render("Press Spacebar or Up Arrow to get started.", False, (0, 0, 0))
replay_font = pygame.font.SysFont("calibri", 35, True)  # replay
replay_text1 = replay_font.render("Wanna try again?", False, (0, 0, 0))
replay_text2 = replay_font.render("Press R to restart.", False, (0, 0, 0))
end_score_font = pygame.font.SysFont("calibri", 32, True)  # end score
game_over_font = pygame.font.SysFont("calibri", 70, True)  # game_over
game_over_text = game_over_font.render("Game Over", False, (0, 0, 0))
best_score_font = pygame.font.SysFont("calibri", 32, True)  # best score
fps_font = pygame.font.SysFont("calibri", 15, True)  # fps
ver_font = pygame.font.SysFont("calibri", 15, True)  # version

end_surface = pygame.Surface((400 if mode == 1 else 380, 410), pygame.SRCALPHA)  # for ending description rectangle thingy

class Player(object):
    def __init__(self):
        if mode == 1:
            self.x = 228
            self.y = 338
            self.width = 57
            self.height = 50
            self.up_force = -32
            self.fly_path = [self.y, 360]
        else:
            self.x = 213
            self.y = 313
            self.width = 55
            self.height = 48
            self.up_force = -30.8
            self.fly_path = [self.y, 338]
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
            if self.y + self.height >= height - 115 if mode == 1 else self.y + self.height >= height - 100:
                self.velocity = 0
                self.gravity = 0
                self.in_air = False

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
        if mode == 1:
            self.width = 105
            self.gap = 204
            self.pipe_ground = 115
            self.start_gap = randint(25, height - 25 - self.gap - self.pipe_ground)
        else:
            self.width = 97
            self.gap = 188
            self.pipe_ground = 100
            self.start_gap = randint(20, height - 20 - self.gap - self.pipe_ground)
        self.top_height = self.start_gap
        self.bottom_height = height - self.start_gap - self.gap - self.pipe_ground
        if start:
            self.vel = 3.2
        else:
            self.vel = 0

    def show(self):
        pygame.draw.rect(screen, (50, 230, 50), (self.x, 0, self.width, self.top_height))  # top pipe
        pygame.draw.rect(screen, (50, 230, 50), (
            self.x, height - self.bottom_height - self.pipe_ground, self.width, self.bottom_height))  # bottom pipe
        pygame.draw.rect(screen, (43, 223, 43), (self.x - 4, self.start_gap - 50, self.width + 8, 50))  # top cap
        pygame.draw.rect(screen, (43, 223, 43),
                         (self.x - 4, height - self.bottom_height - self.pipe_ground, self.width + 8, 50))  # bottom cap
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
        if mode == 1:
            self.y = randint(height - 95, height - 5)
            self.width = randint(4, 15)
            self.height = randint(4, 11)
        else:
            self.y = randint(height - 80, height - 3)
            self.width = randint(4, 14)
            self.height = randint(4, 10)
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
        if mode == 1:
            self.y = randint(-8, 80)
            self.width = randint(80, 170)
            self.height = randint(40, 70)
        else:
            self.y = randint(-6, 75)
            self.width = randint(72, 157)
            self.height = randint(35, 64)
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
        open("Data\\Data.txt")
    except IOError:
        data_file = open("Data\\Data.txt", "w")
        data_file.write("000,0")
        data_file.close()
        print "File created: Data.txt."
    else:
        print "Found file."

def save_load_best():  # saves and loads the best score
    temp_score = score
    with open("Data\\Data.txt", "r+") as data_file:
        prev_best_score = int(data_file.read()[:3])
        nr_char = len(str(temp_score))

        if nr_char == 1:
            seek = 2
        elif nr_char == 2:
            seek = 1
        else:
            seek = 0

        if temp_score > prev_best_score:
            data_file.seek(seek)
            data_file.write(str(temp_score))
            return str(temp_score)
        else:
            return str(prev_best_score)

def statistics():  # saves how many times the user has played
    with open("Data\\Data.txt", "r+") as data_file:
        prev_times_played = int(data_file.read()[4:])
        if start:
            prev_times_played += 1
        data_file.seek(4)
        data_file.write(str(prev_times_played))
        return prev_times_played

def erase_data():
    pass

def show_score(bird_):  # shows the score while playing
    if bird_.in_air and start:
        score_text = score_font.render(str(score), False, (0, 0, 0))
        screen.blit(score_text, (width / 2 - 10, 130))

def show_game_over(bird_):  # shows the 'game over interface'
    if not bird_.in_air:
        end_surface.fill((255, 255, 170, 190))
        screen.blit(end_surface, (100, 165))
        screen.blit(game_over_text, (width / 2 - 165, 240))
        screen.blit(replay_text1, (width / 2 - 128, 430))
        screen.blit(replay_text2, (width / 2 - 130, 490))
        end_score_text = end_score_font.render("Score: " + str(score), False, (0, 0, 0))
        screen.blit(end_score_text, (width / 2 - 135, 360))
        best_score_text = best_score_font.render("Best: " + save_load_best(), False, (0, 0, 0))
        screen.blit(best_score_text, (width / 2 + 40, 360))

def show_instructions():  # shows the instructions at the beginning (only twice)
    if not start and restart_times <= 1:
        screen.blit(instructions_text, (width / 2 - 160, height / 2 + 150))

def show_fps():
    fps = clock.get_fps()
    fps_text = fps_font.render("FPS: " + str(int(fps * 1000 + 0.5) / 1000.0), False, (0, 0, 0))
    screen.blit(fps_text, (10, height - 20))

def show_version():
    ver_text = ver_font.render(version, False, (0, 0, 0))
    screen.blit(ver_text, (width - 45, height - 20))

def drawing():
    global timer, restart_times

    screen.fill((150, 200, 255))

    if bird.in_air and timer == 0 if mode == 1 else bird.in_air and timer == 10:
        if start:
            pipes.append(Pipe())
        timer = 120
        # print len(pipes)

    for cloud in reversed(clouds):  # clouds
        cloud.show()
        cloud.move()
        cloud.reality(bird)
        if cloud.offscreen() and bird.in_air:
            if mode == 1:
                cloud.y = randint(-8, 80)
                cloud.width = randint(80, 170)
                cloud.height = randint(40, 70)
            else:
                cloud.y = randint(-6, 75)
                cloud.width = randint(72, 157)
                cloud.height = randint(35, 64)
            cloud.x = randint(width + 160, width + 550)
            cloud.vel = uniform(0.1, 0.4)
            cloud.color = (randint(247, 255), randint(247, 255), 255, 180)

    for pipe_ in reversed(pipes):  # pipes
        pipe_.show()
        pipe_.move(bird)
        if pipe_.offscreen():
            del pipes[1]

    for dirt in reversed(dirts):  # dirts
        dirt.show()
        dirt.move(bird)
        if dirt.offscreen():
            if mode == 1:
                dirt.y = randint(height - 95, height - 5)
                dirt.width = randint(4, 15)
                dirt.height = randint(4, 11)
            else:
                dirt.y = randint(height - 80, height - 3)
                dirt.width = randint(4, 14)
                dirt.height = randint(4, 10)
            dirt.x = width + randint(10, 80)
            dirt.color = (randint(114, 171), randint(76, 113), randint(26, 83))

    bird.show()
    bird.fly()
    bird.fall()

    show_instructions()
    show_score(bird)
    show_game_over(bird)
    show_fps()
    show_version()

    pygame.display.flip()

def main():
    global score, timer, restart_times, playing, start, bird, pipes, dirts, clouds

    run = True
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

    check_data_file()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                playing = False
                # print "QUIT"

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.KEYDOWN and event.key == pygame.K_UP or \
                    event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                start = True
                bird.up()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and not bird.in_air:
                restart_times += 1
                # print restart_times
                run = False

        for pipe in pipes:  # checking for pipe-bird events
            if pipe.hit(bird):
                # print "HIT"
                bird.in_air = False

            if pipe.score_up(bird) and bird.in_air:
                # print "SCORE"
                score += 1
                # print score

        if start:
            timer -= 1

        drawing()
        clock.tick(65)

    save_load_best()
    statistics()

while playing:
    main()

pygame.quit()  # Written by Simon. Inspired by The Coding Train.
