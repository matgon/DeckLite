import pygame
from classes.entities.Grid import *

class System:
    def __init__(self):
        pass
    def check(self, entity):
        return True
    def update(self, screen, entities, grid, ui):
        for entity in entities:
            if self.check(entity):
                self.update_entity(screen, entity, entities, grid, ui)

class CameraSys(System):
    def __init__(self):
        super().__init__()
        self.cam_offset_x = 0
        self.cam_offset_x = 0

    def check(self, entity):
        return entity.camera is not None

    def update_entity(self, screen: pygame.Surface, entity, entities, grid: Grid, ui):
        # camera_rect = (100,100, screen.get_size()[0], screen.get_size()[1])
        # screen.set_clip(camera_rect)
        # screen.fill((255,255,255))

        if entity.camera.tracked_entity is not None:

            camera_current_x = entity.camera.world_pos_x
            camera_current_y = entity.camera.world_pos_y
            camera_target_x = entity.camera.tracked_entity.x + entity.camera.tracked_entity.img.get_width()/2
            camera_target_y = entity.camera.tracked_entity.y + entity.camera.tracked_entity.img.get_height()/2

            entity.camera.set_world_pos(camera_current_x * 0.95 + camera_target_x * 0.05, camera_current_y * 0.95 + camera_target_y * 0.05)

        cam_rect = entity.camera.rect
        self.cam_offset_x = cam_rect.x + cam_rect.w/2 - entity.camera.world_pos_x
        self.cam_offset_y = cam_rect.y + cam_rect.h/2 - entity.camera.world_pos_y
        
        # for tile in grid.tiles:
        grid.draw(screen, self.cam_offset_x, self.cam_offset_y, entity.camera.zoom)
        for e in entities:
            e.draw(screen, self.cam_offset_x, self.cam_offset_y, entity.camera.zoom)
        for e in entities:
            if e.datacard:
                e.draw(screen, self.cam_offset_x, self.cam_offset_y, entity.camera.zoom)

        cards_offset_x = 0
        for item in ui:
            item.draw(screen, screen.get_width()/3 + cards_offset_x, screen.get_height() - item.img.get_height()/2, 1)
            cards_offset_x += (item.img.get_width() + 10)
        
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

    def update_screen_size(self):
        self.rect = pygame.Rect(0, 0, pygame.display.Info().current_w, pygame.display.Info().current_h)

    def set_tracked_entity(self, entity):
        self.tracked_entity = entity
        self.set_world_pos(entity.x + entity.img.get_width()/2, entity.y + entity.img.get_height()/2)

    def set_zoom(self, scrolldir):
        if scrolldir > 0:
            if self.zoom + 1 < 10:
                self.zoom += 1
        else:
            if self.zoom - 1 > 0:
                self.zoom -= 1