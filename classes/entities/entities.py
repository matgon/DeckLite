import pygame
from classes.utilities.Spritesheets import Spritesheet
from classes.utilities.others import distance_from_points

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
        self.imgs = spritesheet.images_at([(0,0,19,19), (20, 0, 19, 19), (40,0, 19, 19), (60,0, 19, 19), (80, 0, 19, 19), (100, 0, 19, 19), (120, 0, 19, 19), (140, 0, 19, 19),
                                           (0, 19, 19, 19), (20, 19, 19, 19), (40, 19, 19, 19), (60, 19, 19, 19), (80, 19, 19, 19), (100, 19, 19, 19), (120, 19, 19, 19), (140, 19, 19, 19)], (0,0,0))
        self.imgs_down = [self.imgs[0], self.imgs[8]]
        self.imgs_down_right = [self.imgs[1], self.imgs[9]]
        self.imgs_down_left = [self.imgs[2], self.imgs[10]]
        self.imgs_right = [self.imgs[3], self.imgs[11]]
        self.imgs_up = [self.imgs[4], self.imgs[12]]
        self.imgs_up_left = [self.imgs[5], self.imgs[13]]
        self.imgs_up_right = [self.imgs[6], self.imgs[14]]
        self.imgs_left = [self.imgs[7], self.imgs[15]]

        self.current_imgs = self.imgs_down
        self.img = self.current_imgs[0]
        self.animation_state = 0

        self.tile = None
        self.next_tile = None
        self.hp = hp
        self.attk = attk
        self.dck = dck
        self.drop = drop
        self.camera = None
        self.selected_tile = None
        self.speed = 0.3
        self.path = list()
        self.game_tick = pygame.time.get_ticks()

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
        self.x = tile.x + self.tile.width/2 - self.img.get_width()
        self.y = tile.y - self.tile.height/2
        # self.tick = 0
        tile.set_player_in_tile(True)
    
    def set_path(self, path):
        if self.next_tile is not None:
            self.next_tile.set_player_in_tile(False)
        self.tick = 0
        if path is not None:
            path.pop(0)
            self.path = path
        else:
            self.path = list()
        # self.path = path if path is not None else list()

    def set_selected_tile(self, tile):
        self.selected_tile = tile
    
    def set_facing_dir(self):
        '''Sets the facing direction of the player. 
        Returns the string code of the direction.
        ["UP", "UP LEFT", "UP RIGHT", "LEFT", "RIGHT", "DOWN", "DOWN LEFT", "DONW RIGHT"]'''
        x = self.next_tile.tileID[0] - self.tile.tileID[0]
        y = self.next_tile.tileID[1] - self.tile.tileID[1]
        ret = ""
        if x == -1:
            if y == -1:
                self.current_imgs = self.imgs_up
                self.img = self.current_imgs[0]
                ret = "UP"
            elif y==0:
                self.current_imgs = self.imgs_up_left
                self.img = self.current_imgs[0]
                ret = "UP LEFT"
            elif y == 1:
                self.current_imgs = self.imgs_left
                self.img = self.current_imgs[0]
                ret = "LEFT"
        elif x == 0:
            if y == -1:
                self.current_imgs = self.imgs_up_right
                self.img = self.current_imgs[0]
                ret = "UP RIGHT"
            elif y == 1:
                self.current_imgs = self.imgs_down_left
                self.img = self.current_imgs[0]
                ret = "DOWN LEFT"
        elif x == 1:
            if y == -1:
                self.current_imgs = self.imgs_right
                self.img = self.current_imgs[0]
                ret = "RIGHT"
            elif y==0:
                self.current_imgs = self.imgs_down_right
                self.img = self.current_imgs[0]
                ret = "DOWN RIGHT"
            elif y == 1:
                self.current_imgs = self.imgs_down
                self.img = self.current_imgs[0]
                ret = "DOWN"
        return ret

    def move(self, grid):
        if len(self.path) > 0:
            self.tile.set_player_in_tile(False)
            self.next_tile = grid.get_tile(self.path[0][0], self.path[0][1])

            dir = self.set_facing_dir()

            distance = distance_from_points((self.tile.x + self.tile.width/2, self.tile.y + self.tile.height/2), 
                                            (self.next_tile.x + self.next_tile.width/2, (self.next_tile.y + self.next_tile.height/2)))

            #camera_current_x * 0.95 + camera_target_x * 0.05


            self.x = self.x * (1 - self.speed) + (self.next_tile.x + self.next_tile.width/2 - self.img.get_width()) * (0 + self.speed)
            self.y = self.y * (1 - self.speed) + (self.next_tile.y + self.next_tile.height/2) * (0 + self.speed)
            self.next_tile.set_player_in_tile(True)

            if round(self.x) == round(self.next_tile.x + self.next_tile.width/2 - self.img.get_width()) and round(self.y) == round(self.next_tile.y + self.next_tile.height/2):
                self.set_tile(self.next_tile)
                self.path.pop(0)
    
    def draw(self, screen: pygame.Surface, camera_x, camera_y, camera_zoom):
        current_game_tick = pygame.time.get_ticks()
        if current_game_tick - self.game_tick >= 500:
            self.game_tick = current_game_tick
            self.animation_state += 1
            if self.animation_state > len(self.current_imgs)-1:
                self.animation_state = 0
            
        self.img = pygame.transform.scale_by(self.current_imgs[self.animation_state], camera_zoom)
        
        img_width = self.img.get_rect().w
        img_height = self.img.get_rect().h

        pos_x = self.x + camera_x
        pos_y = self.y + camera_y

        screen.blit(self.img, (pos_x, pos_y))

