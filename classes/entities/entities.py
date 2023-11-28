import pygame
from classes.utilities.Spritesheets import Spritesheet

class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self, screen: pygame.Surface, camera_offset_x, camera_offset_y, camera_zoom):
        self.draw(screen, camera_offset_x, camera_offset_y, camera_zoom)

class Player(Entity):

    def __init__(self, x, y, hp, attk, dck, file, drop):
        super().__init__(x, y)

        spritesheet = Spritesheet(file)
        # down = 0, down_right = 1, down_left = 2, right = 3, up = 4, up_left = 5, up_right = 6, left = 7
        self.imgs = spritesheet.images_at([(0,0,19,19), (20, 0, 19, 19), (40,0, 19, 19), (60,0, 19, 19), (0, 19, 19, 19), (20,19, 19, 19), (40,19, 19, 19), (60,19, 19, 19)], (0,0,0))
        self.img = self.imgs[0]

        self.tile = None
        self.next_tile = None
        self.hp = hp
        self.attk = attk
        self.dck = dck
        self.drop = drop
        self.camera = None
        self.selected_tile = None
        self.speed = 0.05
        self.path = list()
        self.tick = 0

# metodos observadores
    def get_pos(self):
        return self.pos
    def get_cell(self):
        return self.cell
    def get_hp(self):
        return self.hp
    def get_attack(self):
        return self.attk
    def get_deck(self):
        return self.dck
    def get_drops(self):
        return self.drop
    
    def set_tile(self, tile):
        if self.tile is not None:
            self.tile.set_player_in_tile(False)
        self.tile = tile
        self.x = tile.x + tile.width/2
        self.y = tile.y + tile.height/2 - self.img.get_size()[1]
        tile.set_player_in_tile(True)
    
    def set_path(self, path):
        if self.next_tile is not None:
            self.next_tile.set_player_in_tile(False)
        self.path = path if path is not None else list()

    def set_selected_tile(self, tile):
        self.selected_tile = tile
    
    def set_facing_dir(self):
        x = self.next_tile.tileID[0] - self.tile.tileID[0]
        y = self.next_tile.tileID[1] - self.tile.tileID[1]

        if x == -1:
            if y == -1:
                self.img = self.imgs[4]
            elif y==0:
                self.img = self.imgs[5]
            elif y == 1:
                self.img = self.imgs[7]
        elif x == 0:
            if y == -1:
                self.img = self.imgs[6]
            elif y == 1:
                self.img = self.imgs[2]
        elif x == 1:
            if y == -1:
                self.img = self.imgs[3]
            elif y==0:
                self.img = self.imgs[1]
            elif y == 1:
                self.img = self.imgs[0]

    def move(self, grid):
        if len(self.path) > 0:
            self.tile.set_player_in_tile(False)
            self.next_tile = grid.get_tile(self.path[0][0], self.path[0][1])
            self.set_facing_dir()
            self.x = self.x * (1 - self.speed) + (self.next_tile.x + self.next_tile.width/2) * (0 + self.speed)
            self.y = self.y * (1 - self.speed) + (self.next_tile.y + self.next_tile.height/2 - self.img.get_size()[1]) * (0 + self.speed)
            self.next_tile.set_player_in_tile(True)

            if round(self.x) == (self.next_tile.x + self.next_tile.width/2) and round(self.y) == (self.next_tile.y + self.next_tile.height/2 - self.img.get_size()[1]):
                self.set_tile(self.next_tile)
                self.path.pop(0)
    
    def draw(self, screen: pygame.Surface, camera_x, camera_y, camera_zoom):
        # self.tick += 1
        # if self.tick == 200 and self.img == self.imgs[0]:
        #     self.img = self.imgs[1]
        #     self.tick = 0
        # elif self.tick == 200 and self.img == self.imgs[1]:
        #     self.img = self.imgs[0]
        #     self.tick = 0

        img_width = int(self.img.get_rect().w * camera_zoom)
        img_height = int(self.img.get_rect().h * camera_zoom)

        pos_x = int((self.x + ((self.tile.pos_img_x-1)*(img_width - self.img.get_rect().w)/2) - ((self.tile.pos_img_y-1)*(img_width - self.img.get_rect().w)/2)))
        pos_y = int((self.y + ((self.tile.pos_img_y-1)*(img_height - self.img.get_rect().h)/2) + ((self.tile.pos_img_x-1)*(img_width - self.img.get_rect().w)/2/2)))

        img_width = int(self.img.get_rect().w * camera_zoom)
        img_height = int(self.img.get_rect().h * camera_zoom)
        pos_x = self.x * camera_zoom
        pos_y = self.y * camera_zoom
        screen.blit(pygame.transform.scale(self.img, (img_width, img_height)), (pos_x + camera_x - self.tile.width/4, pos_y + camera_y))

