import pygame
from main_menu import *

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

width = 800
height = 600
running = True

game_font = pygame.font.SysFont("calibri", 60)
in_game_text = game_font.render("IN GAME ROOM", 0, (255, 255, 255))







def main_menu_room():
    global running, current_room

    run = True
    main_menu = MainMenu()
    mouse_click = False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True

        main_menu.show(screen)

        if main_menu.goto(mouse_click) == 0:
            run = False
            current_room = game_room
        elif main_menu.goto(mouse_click) == 1:
            run = False
            running = False

        mouse_click = False

        clock.tick(30)

def game_room():
    global running, current_room
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False
                    current_room = main_menu_room

        screen.fill((150, 100, 150))
        screen.blit(in_game_text, (width / 2 - 200, height / 2))
        pygame.display.flip()
        clock.tick(60)






game_rooms = (main_menu_room, game_room)
current_room = main_menu_room

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_room()

pygame.quit()
