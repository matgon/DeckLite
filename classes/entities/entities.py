import pygame
from classes.utilities.Spritesheets import Spritesheet
from classes.utilities.others import *

class Entity:
    def __init__(self, x, y, hp, armor, attack, speed, file, camera_zoom):
        self.x = x
        self.y = y
        self.hp = hp
        self.armor = armor
        self.base_attack = attack
        self.tile = None
        self.next_tile = None
        self.facing_dir = "DOWN"
        self.camera = None
        self.speed = 0.1
        self.path = list()
        self.game_tick = pygame.time.get_ticks()
        self.current_imgs = None
        self.img = None
        self.animation_state = 0
        self.camera_zoom = camera_zoom
        self.set_imgs(file, camera_zoom)
        self.datacard = False
        self.datacard_surface = None

    def set_imgs(self, file, camera_zoom):
        self.set_imgs_entity(Spritesheet(file), camera_zoom)

    def set_zoom(self, speed):
        self.speed = speed

    def set_datacard(self, value):
        self.datacard = value
        if value == True:
            self.datacard_surface = pygame.Surface((130,120), pygame.SRCALPHA)
        elif value == False:
            self.datacard_surface = None

    def update_screen_size(self):
        self.set_tile(self.tile)
        self.set_speed(0.1 * self.camera_zoom)
        if self.camera is not None:
            self.camera.set_world_pos(self.x + self.img.get_width()/2, self.y + self.img.get_height()/2)

    def update_zoom(self, camera_zoom):
        self.camera_zoom = camera_zoom
        self.img = pygame.transform.scale_by(self.current_imgs[self.animation_state], camera_zoom)
        self.set_tile(self.tile)
        self.set_speed(0.1 * camera_zoom)
        if self.camera is not None:
            self.camera.set_world_pos(self.x + self.img.get_width()/2, self.y + self.img.get_height()/2)
        # self.x = self.tile.x + self.tile.width/2 - self.img.get_width()/2
        # self.y = self.tile.y - self.tile.height/2

    def set_speed(self, value):
        self.speed = value

    def set_path(self, path):
        if path is not None:
            if self.next_tile is not None:
                self.next_tile.set_entity_in_tile(False)
                self.next_tile.set_obj(None)
            #self.tick = 0
            path.pop(0)
            self.path = path
        else:
            self.path = list()

    def set_tile(self, tile):
        '''set current tile of the entity'''
        if self.tile is not None:
            self.tile.set_obj(None)
            self.tile.set_entity_in_tile(False)
        self.tile = tile
        self.tile.set_obj(self)
        self.x = self.tile.x + self.tile.width/2 - self.img.get_width()/2
        self.y = self.tile.y - self.tile.height/2
        # self.tick = 0
        tile.set_entity_in_tile(True)

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
                self.facing_dir = "UP"
            elif y==0:
                self.current_imgs = self.imgs_up_left
                self.facing_dir = "UP LEFT"
            elif y == 1:
                self.current_imgs = self.imgs_left
                self.facing_dir = "LEFT"
        elif x == 0:
            if y == -1:
                self.current_imgs = self.imgs_up_right
                self.facing_dir = "UP RIGHT"
            elif y == 1:
                self.current_imgs = self.imgs_down_left
                self.facing_dir = "DOWN LEFT"
        elif x == 1:
            if y == -1:
                self.current_imgs = self.imgs_right
                self.facing_dir = "RIGHT"
            elif y==0:
                self.current_imgs = self.imgs_down_right
                self.facing_dir = "DOWN RIGHT"
            elif y == 1:
                self.current_imgs = self.imgs_down
                self.facing_dir = "DOWN"
        #self.img = self.current_imgs[0]

    def perform_attack(self, target):
        if target is not None:
            target.receive_attack(self.base_attack)

    def receive_attack(self, dmg):
        if self.armor > 0:
            if dmg > self.armor:
                dmg -= self.armor
                self.armor = 0
            else:
                self.armor -= dmg
                dmg = 0
        self.hp -= dmg

    def move(self, grid):
        self.move_entity(grid)
    
    def draw(self, screen: pygame.Surface, camera_x, camera_y, camera_zoom):
        if self.camera_zoom != camera_zoom:
            self.camera_zoom = camera_zoom
            self.update_zoom(camera_zoom)
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
        if self.datacard:
            pos_x_datacard = pos_x + self.img.get_width()
            pos_y_datacard = pos_y + self.img.get_height()
            if pos_x_datacard + self.datacard_surface.get_width() >= screen.get_width():
                pos_x_datacard = screen.get_width() - self.datacard_surface.get_width()
            if pos_y_datacard + self.datacard_surface.get_height() >= screen.get_height():
                pos_y_datacard = screen.get_height() - self.datacard_surface.get_height()

            screen.blit(self.datacard_surface, (pos_x_datacard, pos_y_datacard))
            pygame.draw.rect(self.datacard_surface, (0, 0, 0, 100), (0,0,self.datacard_surface.get_width(), self.datacard_surface.get_height()))
            Label(self.datacard_surface, "HP: " + str(self.hp), 20, 20, pygame.font.Font('resources/fonts/Pixel.ttf', 16)).draw()
            Label(self.datacard_surface, "Armor: " + str(self.armor), 20, 40, pygame.font.Font('resources/fonts/Pixel.ttf', 16)).draw()
            Label(self.datacard_surface, "Attack: " + str(self.base_attack), 20, 60, pygame.font.Font('resources/fonts/Pixel.ttf', 16)).draw()
            Label(self.datacard_surface, "Pos: (" + str(self.tile.tileID[0])+ ", " + str(self.tile.tileID[1]) + ")", 20, 80, pygame.font.Font('resources/fonts/Pixel.ttf', 16)).draw()

#-------------------PLAYER-------------------------------------------------------------------------------
class Player(Entity):

    def __init__(self, x, y, hp, armor, attk, dck, file, drop, camera_zoom):
        super().__init__(x, y, hp, armor, attk, 0.01, file, camera_zoom)

# metodos observadores
    def set_imgs_entity(self, spritesheet, camera_zoom):
        '''Set the animations of the entity'''
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
        self.img = pygame.transform.scale_by(self.current_imgs[0], camera_zoom)
        self.animation_state = 0
    
    def use_card(self, card, grid):
        if card.type == 'Basic_attack':
            target_tile = None
            if self.facing_dir == "DOWN":
                target_tile = grid.get_tile(self.tile.tileID[0] + 1, self.tile.tileID[1] + 1)
            elif self.facing_dir == "DOWN LEFT":
                target_tile = grid.get_tile(self.tile.tileID[0], self.tile.tileID[1] + 1)
            elif self.facing_dir == "LEFT":
                target_tile = grid.get_tile(self.tile.tileID[0] - 1, self.tile.tileID[1] + 1)
            elif self.facing_dir == "UP LEFT":
                target_tile = grid.get_tile(self.tile.tileID[0] - 1, self.tile.tileID[1])
            elif self.facing_dir == "UP":
                target_tile = grid.get_tile(self.tile.tileID[0] - 1, self.tile.tileID[1] - 1)
            elif self.facing_dir == "UP RIGHT":
                target_tile = grid.get_tile(self.tile.tileID[0], self.tile.tileID[1] - 1)
            elif self.facing_dir == "RIGHT":
                target_tile = grid.get_tile(self.tile.tileID[0] + 1, self.tile.tileID[1] - 1)
            elif self.facing_dir == "DOWN RIGHT":
                target_tile = grid.get_tile(self.tile.tileID[0] + 1, self.tile.tileID[1])
            if target_tile is not None:
                self.perform_attack(target_tile.obj)
                return True
            else:
                print("No se puede atacar fuera del tablero.")
                return False

        elif card.type == 'Basic_defend':
            self.armor += 5
            return True

    def move_entity(self, grid):
        if len(self.path) > 0:
            self.tile.set_entity_in_tile(False)
            #self.tile.set_obj(None)
            self.next_tile = grid.get_tile(self.path[0][0], self.path[0][1])
            if self.next_tile.obj is None:
                self.set_facing_dir()

                self.x = self.x * (1 - self.speed) + (self.next_tile.x + self.next_tile.width/2 - self.img.get_width()/2) * (0 + self.speed)
                self.y = self.y * (1 - self.speed) + (self.next_tile.y - self.next_tile.height/2) * (0 + self.speed)
                self.next_tile.set_entity_in_tile(True)
                #self.next_tile.set_obj(self)

                distance = distance_from_points((self.x, self.y), 
                                                ((self.next_tile.x + self.next_tile.width/2 - self.img.get_width()/2), (self.next_tile.y - self.next_tile.height/2)))

                if distance < 0.5:
                    self.set_tile(self.next_tile)
                    self.path.pop(0) 
            else:
                self.set_tile(self.tile)
                self.next_tile = None
                self.path = list()

#-------------------ZOMBIE-------------------------------------------------------------------------------

class Zombie(Entity):

    def __init__(self, x, y, hp, armor, attk, dck, file, drop, camera_zoom):
        super().__init__(x, y, hp, armor, attk, 0.01, file, camera_zoom)

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
    
    def set_imgs_entity(self, spritesheet, camera_zoom):
        '''Set the animations of the entity'''
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
        self.img = pygame.transform.scale_by(self.current_imgs[0], camera_zoom)
        self.animation_state = 0

    def move_entity(self, grid):
        if len(self.path) > 0:
            self.tile.set_entity_in_tile(False)
            self.next_tile = grid.get_tile(self.path[0][0], self.path[0][1])

            self.set_facing_dir()

            self.x = self.x * (1 - self.speed) + (self.next_tile.x + self.next_tile.width/2 - self.img.get_width()/2) * (0 + self.speed)
            self.y = self.y * (1 - self.speed) + (self.next_tile.y - self.next_tile.height/2) * (0 + self.speed)
            self.next_tile.set_entity_in_tile(True)

            if round(self.x) == round(self.next_tile.x + self.next_tile.width/2 - self.img.get_width()/2) and round(self.y) == round(self.next_tile.y - self.next_tile.height/2):
                self.set_tile(self.next_tile)
                self.path.pop(0)