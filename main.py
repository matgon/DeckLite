import pygame, sys, time, random

sys.path.append('C:/Users/tetog/Documents/Proyectos/DeckLite')

from pygame.locals import *
from classes.entities.Grid import Grid
from classes.entities.entities import *
from classes.utilities.rendering import *

def main():
    pygame.init()
    pygame.display.set_caption('game base')
    screen = pygame.display.set_mode((800, 800), flags=RESIZABLE | NOFRAME)#(pygame.display.Info().current_w/2, pygame.display.Info().current_h/2)

    myfont = pygame.font.SysFont("monospace", 15)
    mouse_point = pygame.mouse.get_pos()
    mouse_pos_label = Label(screen, "Mouse: (" + str(mouse_point[0]) + ", " + str(mouse_point[1]) +")", 20, 20, pygame.font.SysFont("monospace", 20), 20)


    entities = list()
    grid = Grid(0,0,'resources/level0.txt', camera_zoom=2)
    player = Player(pygame.display.Info().current_w/2, pygame.display.Info().current_h/2, 50, 50, None, 'resources/img/player_spritesheet.png', None)
    player.set_tile(grid.get_tile(0, 0))
    entities.append(player)
    player_pos_label = Label(screen, "Player: (" + str(player.tile.x) + ", " + str(player.tile.y) +")", 20, 50, pygame.font.SysFont("monospace", 20), 20)

    #camera init
    camera = Camera(0, 0, screen.get_size()[0], screen.get_size()[1])
    player.camera = camera
    player.camera.set_tracked_entity(player)
    camSys = CameraSys()

    mouseButton_down = False
    mouseButton_down_pos = (0,0)

    while True:
        screen.fill((0,0,0))
        camSys.update(screen, entities, grid)
        mouse_pos_label.draw()
        player_pos_label.draw()

        player.move(grid)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == VIDEORESIZE:
                grid.resize()
            if event.type == MOUSEBUTTONDOWN and not mouseButton_down:
                mouseButton_down = True
                mouseButton_pos = pygame.mouse.get_pos()
            if event.type == MOUSEBUTTONUP:
                mouseButton_down = False
                mouseButton_pos = pygame.mouse.get_pos()
                tileSelected, tile = grid.check_selected_tile(mouseButton_pos)
                if tileSelected:
                    player.set_path(grid.BFS.BFS_SP(grid.graph, player.tile.tileID, tile.tileID))

            if event.type == MOUSEMOTION and mouseButton_down:
                #grid.move(mouseButton_down_pos, pygame.mouse.get_pos())
                mouseButton_pos = pygame.mouse.get_pos()
            if event.type == MOUSEWHEEL:
                camera.set_zoom(event.y)
                #grid.zoom(event.y)
            mouse_point = pygame.mouse.get_pos()
        mouse_pos_label.change_text("Mouse: (" + str(mouse_point[0]) + ", " + str(mouse_point[1]) +")")
        player_pos_label.change_text("Player: (" + str(player.tile.x) + ", " + str(player.tile.y) +")")
        grid.hover_tile(mouse_point)

        pygame.display.update()

class Label:
    ''' CLASS FOR TEXT LABELS ON THE WIN SCREEN SURFACE '''
    def __init__(self, screen, text, x, y, font, size=20, color="white"):
        if size != 20:
            self.font = font
        else:
            self.font = font
        self.image = self.font.render(text, 1, color)
        _, _, w, h = self.image.get_rect()
        self.rect = pygame.Rect(x, y, w, h)
        self.screen = screen
        self.text = text
    def change_text(self, newtext, color="white"):
        self.image = self.font.render(newtext, 1, color)
    def change_font(self, font, color="white"):
        self.font = font
        self.change_text(self.text, color)
    def draw(self):
        self.screen.blit(self.image, (self.rect))

if __name__ == "__main__":
    main()