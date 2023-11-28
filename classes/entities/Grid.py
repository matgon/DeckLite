import pygame
from classes.utilities.Spritesheets import Spritesheet
import os

class Grid():
    def __init__(self, grid_x, grid_y, file):
        self.pos = [grid_x, grid_y]
        self.tiles = list()
        self.graph = dict()

        f = open(file)
        map_data = [[int(c) for c in row] for row in f.read().split('\n')]
        f.close()
        spritesheet = Spritesheet('resources/img/Blocks_Spritesheet.png')
        block_imgs = spritesheet.images_at([(0,0,40,19), (40, 0, 40, 31)], (0,0,0))#, (60,0,80,31)], (0,0,0))
        #pygame.image.load('resources/img/Blocks_Spritesheet.png').convert_alpha()

        tile_width = 40
        tile_height = 20
        for y, row in enumerate(map_data):
            for x, tile in enumerate(row):
                if tile:
                    tile_x = (pygame.display.Info().current_w/2 - tile_width/2) + (x*tile_width/2) - (y*tile_width/2)
                    tile_y = (pygame.display.Info().current_h/3 + tile_height/2) + (x*tile_height/2) + (y*tile_height/2)
                    self.tiles.append(Tile(tile_x, tile_y, (x, y), tile_width, tile_height, 0, block_imgs))
                    self.graph.update({(x,y): []})
                    if self.graph.get((x, y-1)) is not None:
                        self.graph[(x,y-1)].append((x,y))
                        self.graph[(x,y)].append((x,y-1))
                    if self.graph.get((x-1, y)) is not None:
                        self.graph[(x-1,y)].append((x,y))
                        self.graph[(x,y)].append((x-1,y))
                    if self.graph.get((x-1, y-1)) is not None:
                        self.graph[(x-1,y-1)].append((x,y))
                        self.graph[(x,y)].append((x-1,y-1))
                    if self.graph.get((x-1, y+1)) is not None:
                        self.graph[(x-1,y+1)].append((x,y))
                        self.graph[(x,y)].append((x-1,y+1))
                    if self.graph.get((x+1, y-1)) is not None:
                        self.graph[(x+1,y-1)].append((x,y))
                        self.graph[(x,y)].append((x+1,y-1))

        pass


    #======================================
    class BFS:
        def __init__(self):
            self.visited = list()
            self.queue = list()

        def bfs(self, visited, graph, node):
            self.visited.append(node)
            self.queue.append(node)

            while self.queue:
                m = self.queue.pop(0) 
                print (m, end = " ") 

                for neighbour in graph[m]:
                    if neighbour not in visited:
                        visited.append(neighbour)
                        self.queue.append(neighbour)
        
        def BFS_SP(graph, start, goal):
            visited = []
            queue = [[start]]
            if start == goal:
                print("BFS same node")
                return
            while queue:
                path = queue.pop(0)
                node = path[-1]
                
                if node not in visited:
                    neighbours = graph[node]
                    
                    for neighbour in neighbours:
                        new_path = list(path)
                        new_path.append(neighbour)
                        queue.append(new_path)
                        
                        if neighbour == goal:
                            return new_path
                    visited.append(node)
        
            print("A connecting path doesn't exist")
            return
    #======================================

    def get_tile(self, grid_x, grid_y):
        for tile in self.tiles:
            if tile.tileID == (grid_x, grid_y):
                return tile

    def resize(self):
        for tile in self.tiles:
            tile.resize()

    def move(self, mouse_startPos, mouse_actualPos):
        x_offset = mouse_actualPos[0] - mouse_startPos[0]
        y_offset = mouse_actualPos[1] - mouse_startPos[1]
        for tile in self.tiles:
            tile.move(x_offset, y_offset)
    
    def zoom(self, scrolldir):
        for tile in self.tiles:
            tile.zoom(scrolldir)

    def hover_tile(self, mouse_pos: tuple):
        for tile in self.tiles:
            collide = tile.check_mouse_collision(mouse_pos)
            tile.hover_tile(collide)

    def check_selected_tile(self, mouse_pos):
        for tile in self.tiles:
            if tile.check_mouse_collision(mouse_pos):
                return True, tile
        return False, None
        
    def draw(self, screen, camera_x, camera_y, camera_zoom):
        for tile in self.tiles:
            #for tile in row:
            tile.draw(screen, camera_x, camera_y, camera_zoom)

class Tile():
    def __init__(self, x, y, cell, width, height, level, imgs: list[pygame.Surface]):
        self.x = x
        self.y = y
        self.tileID = cell
        self.width = width
        self.height = height
        self.level = level
        self.original_img = imgs
        self.hover = False
        self.player_in_tile = False
        self.scale = (0,0)

        self.original_top_img = imgs[0]
        self.original_bot_img = imgs[1]
        #self.original_bottomRight_img = imgs[2]
        self.top_img = self.original_top_img
        self.bot_img = self.original_bot_img
        #self.bottomRight_img = self.original_bottomRight_img

        self.pos_img_x = self.x
        self.pos_img_y = self.y

        self.img_mask = pygame.mask.from_surface(self.top_img)
        self.rect = self.top_img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def check_mouse_collision(self, mouse_pos:tuple):
        pos_in_mask = mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y
        return self.rect.collidepoint(mouse_pos) and self.img_mask.get_at(pos_in_mask)
        
    def set_player_in_tile(self, value):
        self.player_in_tile = value

    def hover_tile(self, collide):
        if collide or self.player_in_tile:
            if not self.hover:
                self.hover = True
                self.y -= 5
        else:
            if self.hover:
                self.hover = False
                self.y += 5

    
    def update_mask(self, x, y, w, h):
        self.img_mask = pygame.mask.from_surface(pygame.transform.scale(self.original_top_img, (w, h)))
        self.rect = pygame.Rect(x,y if not self.hover else y+5,w,h)

    def check_selected(self, mouse_pos):
        pass

    def draw(self, screen: pygame.Surface, camera_x, camera_y, camera_zoom):
        img_top_width = int(self.top_img.get_rect().w * camera_zoom)
        img_top_height = int(self.top_img.get_rect().h * camera_zoom)

        self.pos_img_x = int((self.x + ((self.tileID[0]-1)*(img_top_width - self.top_img.get_rect().w)/2) - ((self.tileID[1]-1)*(img_top_width - self.top_img.get_rect().w)/2)))
        self.pos_img_y = int((self.y + ((self.tileID[1]-1)*(img_top_height - self.top_img.get_rect().h)/2) + ((self.tileID[0]-1)*(img_top_width - self.top_img.get_rect().w)/2/2)))
        
        self.update_mask(self.pos_img_x + camera_x, self.pos_img_y + camera_y, img_top_width, img_top_height)

        img_bot_width = self.bot_img.get_rect().w * camera_zoom
        img_bot_height = self.bot_img.get_rect().h * camera_zoom

        screen.blit(pygame.transform.scale(self.original_top_img, (img_top_width, img_top_height)), (self.pos_img_x + camera_x, self.pos_img_y + camera_y))
        screen.blit(pygame.transform.scale(self.original_bot_img, (img_bot_width, img_bot_height)), (self.pos_img_x + camera_x, self.pos_img_y + camera_y + img_top_height/2))