import pygame, sys, time, random

sys.path.append('C:/Users/tetog/Documents/Proyectos/DeckLite')

from pygame.locals import *
from classes.entities.Grid import Grid
from classes.entities.entities import *
from classes.utilities.rendering import *
from classes.utilities.others import *
from classes.entities.Deck import *

def main():
    pygame.init()
    pygame.display.set_caption('game base')
    screen = pygame.display.set_mode((800, 800), flags=RESIZABLE)#(pygame.display.Info().current_w/2, pygame.display.Info().current_h/2)

    myfont = pygame.font.SysFont("monospace", 15)
    mouse_point = pygame.mouse.get_pos()
    mouse_pos_label = Label(screen, "Mouse: (" + str(mouse_point[0]) + ", " + str(mouse_point[1]) +")", 20, 20, pygame.font.Font('resources/fonts/Pixel.ttf', 20), 20)

    entities = list()
    ui = list()
    grid = Grid(0,0,'resources/level0.txt', camera_zoom=1)
    player = Player(pygame.display.Info().current_w/2, pygame.display.Info().current_h/2, 50, 0, 5, None, 'resources/img/player_spritesheet.png', None, camera_zoom=1)
    player.set_tile(grid.get_tile(0, 0))
    zombie = Zombie(pygame.display.Info().current_w/2, pygame.display.Info().current_h/2, 20, 6, 2, None, 'resources/img/zombie_spritesheet.png', None, camera_zoom=1)
    zombie2 = Zombie(pygame.display.Info().current_w/2, pygame.display.Info().current_h/2, 30, 0, 4, None, 'resources/img/zombie_spritesheet.png', None, camera_zoom=1)
    zombie.set_tile(grid.get_tile(10,10))
    zombie2.set_tile(grid.get_tile(3,5))
    entities.append(player)
    entities.append(zombie)
    entities.append(zombie2)
    player_pos_label = Label(screen, "Player: (" + str(player.tile.x) + ", " + str(player.tile.y) +")", 20, 50, pygame.font.Font('resources/fonts/Pixel.ttf', 20), 20)#pygame.font.SysFont("monospace", 20), 20)

    #camera init
    camera = Camera(0, 0, screen.get_size()[0], screen.get_size()[1])
    player.camera = camera
    player.camera.set_tracked_entity(player)
    camSys = CameraSys()

    player_deck = Deck()
    player_hand = Hand()

    for i in range(player_hand.max_cards):
        card = player_hand.draw_card(player_deck)
        ui.append(card)

    mouseButton_down = False
    mouseButton_down_pos = (0,0)
    zoomed = False

    while True:
        screen.fill((0,0,0))
        camSys.update(screen, entities, grid, ui, zoomed)
        zoomed = False
        mouse_pos_label.draw()
        player_pos_label.draw()

        player.move(grid)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN: # quit the game
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == VIDEORESIZE: # the screen gets resized
                update_screen_size(grid, entities, player.camera) 

            if event.type == MOUSEBUTTONDOWN and not mouseButton_down:
                mouseButton_down = True
                mouseButton_pos = pygame.mouse.get_pos()

            if event.type == MOUSEBUTTONUP and event.button == 1: #left-clic
                mouseButton_down = False
                mouseButton_pos = pygame.mouse.get_pos()
                cardSelected, card = player_hand.check_selected_card(mouseButton_pos) #card selected

                if cardSelected:
                    if player.use_card(card, grid):
                        player_hand.use_card(card, player_deck)
                        card.use()
                        ui.remove(card)

                else:
                    tileSelected, tile = grid.check_selected_tile(mouseButton_pos) #tile selected
                    if tileSelected:
                        player.set_path(grid.BFS.BFS_SP(grid, grid.graph, player.tile.tileID, tile.tileID))

            if event.type == MOUSEMOTION and mouseButton_down:
                mouseButton_pos = pygame.mouse.get_pos()

            if event.type == MOUSEWHEEL: #mouse wheel
                camera.set_zoom(event.y)
                zoomed = True


        mouse_point = pygame.mouse.get_pos()
        mouse_pos_label.change_text("Mouse: (" + str(mouse_point[0]) + ", " + str(mouse_point[1]) +")")
        player_pos_label.change_text("Player: (" + str(player.tile.tileID[0]) + ", " + str(player.tile.tileID[1]) +")")
        if not player_hand.hover_card(mouse_point):
            grid.hover_tile(mouse_point)

        pygame.display.update()

def update_screen_size(grid, entities, camera):
    screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), flags=RESIZABLE)
    grid.update_screen_size()
    for e in entities:
        e.update_screen_size()
    camera.update_screen_size()

if __name__ == "__main__":
    main()