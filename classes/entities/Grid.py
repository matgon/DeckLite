import pygame
from classes.utilities.Spritesheets import Spritesheet
import os

class Grid():
    def __init__(self, grid_x, grid_y, file, camera_zoom):
        self.pos = [grid_x, grid_y]
        self.tiles = list()
        self.graph = dict()

        f = open(file)
        map_data = [[int(c) for c in row] for row in f.read().split('\n')]
        f.close()
        spritesheet = Spritesheet('resources/img/Blocks_Spritesheet.png')
        block_imgs = spritesheet.images_at([(0,0,40,19), (40, 0, 40, 31)], (0,0,0))#, (60,0,80,31)], (0,0,0))

        tile_width = 40 * camera_zoom
        tile_height = 20 * camera_zoom

        self.camera_zoom = camera_zoom

        for y, row in enumerate(map_data):
            for x, tile in enumerate(row):
                if tile:
                    tile_x = (pygame.display.Info().current_w/2 - tile_width/2) + (x*tile_width/2) - (y*tile_width/2)
                    tile_y = (pygame.display.Info().current_h/3 + tile_height/2) + (x*tile_height/2) + (y*tile_height/2)
                    self.tiles.append(Tile(tile_x, tile_y, (x, y), tile_width, tile_height, 0, block_imgs, camera_zoom))
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
        
        for key in self.graph.keys():
            self.graph[key].sort(key = lambda p: abs(key[0] - p[0]) + abs(key[1] - p[1]), )

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
        
        def BFS_SP(grid, graph, start, goal):
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
                        if grid.get_tile(neighbour[0], neighbour[1]).obj is None:
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
        return None

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
    
    def update_zoom(self):
        tile_width = 40 * self.camera_zoom
        tile_height = 20 * self.camera_zoom
        for tile in self.tiles:
            tile_x = (pygame.display.Info().current_w/2 - tile_width/2) + (tile.tileID[0]*tile_width/2) - (tile.tileID[1]*tile_width/2)
            tile_y = (pygame.display.Info().current_h/3 + tile_height/2) + (tile.tileID[0]*tile_height/2) + (tile.tileID[1]*tile_height/2)
            tile.update_zoom(tile_x, tile_y, self.camera_zoom)
        
    def draw(self, screen, camera_x, camera_y, camera_zoom):
        if self.camera_zoom != camera_zoom:
            self.camera_zoom = camera_zoom
            self.update_zoom()
        for tile in self.tiles:
            #for tile in row:
            tile.draw(screen, camera_x, camera_y, camera_zoom)

class Tile():
    def __init__(self, x, y, cell, width, height, level, imgs: list[pygame.Surface], camera_zoom):
        self.x = x
        self.y = y
        self.tileID = cell
        self.width = width
        self.height = height
        self.level = level
        self.original_img = imgs
        self.hover = False
        self.entity_in_tile = False
        self.obj = None
        self.scale = (0,0)

        self.original_top_img = imgs[0]
        self.original_bot_img = imgs[1]

        self.camera_zoom = camera_zoom
        self.top_img = pygame.transform.scale_by(self.original_top_img, camera_zoom)
        self.bot_img = pygame.transform.scale_by(self.original_bot_img, camera_zoom)

        self.pos_img_x = self.x
        self.pos_img_y = self.y

        self.img_mask = pygame.mask.from_surface(self.top_img)
        self.rect = self.top_img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def check_mouse_collision(self, mouse_pos:tuple):
        pos_in_mask = mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y
        return self.rect.collidepoint(mouse_pos) and self.img_mask.get_at(pos_in_mask)
        
    def set_obj(self, value):
        self.obj = value

    def set_entity_in_tile(self, value):
        self.entity_in_tile = value
        if value:
            self.hover = True
        else:
            self.hover = False

    def hover_tile(self, collide):
        if collide:
            if not self.hover:
                self.hover = True
            if self.entity_in_tile and self.obj is not None:
                if self.obj.datacard is False:
                    self.obj.set_datacard(True)
        else:
            if self.hover and not self.entity_in_tile:
                self.hover = False
            if self.entity_in_tile and self.obj is not None:
                if self.obj.datacard is True:
                    self.obj.set_datacard(False)
            # if self.entity_in_tile and self.obj.datacard is True:
            #     self.obj.set_datacard(False)
    
    def update_mask(self, pos_x, pos_y):
        '''Updates the hitbox of the tile if the coordinates had any changes.'''
        if self.rect.x is not pos_x and self.rect.y is not pos_y:
            self.img_mask = pygame.mask.from_surface(self.top_img)
            self.rect = self.top_img.get_rect()
            self.rect.x = pos_x
            self.rect.y = pos_y

    def check_selected(self, mouse_pos):
        pass

    def update_zoom(self, x, y, camera_zoom):
        self.camera_zoom = camera_zoom
        self.width = 40 * self.camera_zoom
        self.height = 20 * self.camera_zoom
        self.x = x
        self.y = y
        self.top_img = pygame.transform.scale_by(self.original_top_img, self.camera_zoom)
        self.bot_img = pygame.transform.scale_by(self.original_bot_img, self.camera_zoom)
        self.pos_img_x = self.x
        self.pos_img_y = self.y
        self.update_mask(x, y)

    def draw(self, screen: pygame.Surface, camera_x, camera_y, camera_zoom):
        self.top_img = pygame.transform.scale_by(self.original_top_img, camera_zoom)
        self.bot_img = pygame.transform.scale_by(self.original_bot_img, camera_zoom)

        self.width = 40 * camera_zoom # width of the new tile
        self.height = 20 * camera_zoom # height of the new tile

        pos_x = self.pos_img_x + camera_x
        pos_y = self.pos_img_y + camera_y

        self.update_mask(pos_x, pos_y)

        if self.hover:
            screen.blit(self.top_img, (pos_x, pos_y - 6))
            screen.blit(self.bot_img, (pos_x, pos_y - 6 + self.height/2))
        else:
            screen.blit(self.top_img, (pos_x, pos_y))
            screen.blit(self.bot_img, (pos_x, pos_y + self.height/2))