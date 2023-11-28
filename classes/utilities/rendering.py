import pygame
from classes.entities.Grid import *

class System:
    def __init__(self):
        pass
    def check(self, entity):
        return True
    def update(self, screen, entities, grid):
        for entity in entities:
            if self.check(entity):
                self.update_entity(screen, entity, entities, grid)

class CameraSys(System):
    def __init__(self):
        super().__init__()

    def check(self, entity):
        return entity.camera is not None

    def update_entity(self, screen: pygame.Surface, entity, entities, grid: Grid):
        # camera_rect = (100,100, screen.get_size()[0], screen.get_size()[1])
        # screen.set_clip(camera_rect)
        # screen.fill((255,255,255))

        if entity.camera.tracked_entity is not None:

            camera_current_x = entity.camera.world_pos_x
            camera_current_y = entity.camera.world_pos_y
            camera_target_x = entity.x
            camera_target_y = entity.y

            entity.camera.set_world_pos(camera_current_x * 0.95 + camera_target_x * 0.05, camera_current_y * 0.95 + camera_target_y * 0.05)

        cam_rect = entity.camera.rect
        cam_offset_x = cam_rect.x + cam_rect.w/2 - entity.camera.world_pos_x
        cam_offset_y = cam_rect.y + cam_rect.h/2 - entity.camera.world_pos_y
        
        for tile in grid.tiles:
            tile.draw(screen, cam_offset_x, cam_offset_y, 1)
        for e in entities:
            e.draw(screen, cam_offset_x, cam_offset_y, 1)
        
        # screen.set_clip(None)
    

class Camera:
    def __init__(self,x,y,w,h):
        self.rect = pygame.Rect(x,y,w,h)
        self.world_pos_x = 0
        self.world_pos_y = 0
        self.zoom = 1
        self.tracked_entity = None
    
    def set_world_pos(self, x, y):
        self.world_pos_x = x
        self.world_pos_y = y

    def set_tracked_entity(self, entity):
        self.tracked_entity = entity
        self.set_world_pos(entity.x, entity.y)

    def set_zoom(self, scrolldir):
        if scrolldir > 0:
            if self.zoom + 1 < 10:
                self.zoom += 1
        else:
            if self.zoom - 1 > 0:
                self.zoom -= 1