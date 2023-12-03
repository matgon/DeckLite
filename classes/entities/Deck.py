import random
from classes.utilities.Spritesheets import Spritesheet
from classes.utilities.others import *

class Deck:
    def __init__(self):
        self.cards = list()
        self.init_deck()
        self.shuffle()

# metodos observadores
    def get_hp(self):
        return self.hp
    def get_attack(self):
        return self.attk
    def get_habilities(self):
        return self.hab
    def get_drops(self):
        return self.drop
    
    def init_deck(self):
        for i in range(5):
            self.cards.append(Basic_attack(2, 'resources/img/cards_spritesheet.png'))
        for i in range(5):
            self.cards.append(Basic_defend(2, 'resources/img/cards_spritesheet.png'))
    
    def shuffle(self):
        random.shuffle(self.cards)

    def add_card(self, card):
        self.cards.append(card)

class Card:
    def __init__(self, cost, file, type):
        self.cost = cost
        self.type = type
        self.original_img = None
        self.img = None
        self.img_mask = None
        self.rect = None
        self.set_imgs(file)
        self.hover = False

    def set_imgs(self, file):
        self.set_imgs_entity(Spritesheet(file))

    def hover_card(self, collide):
        if collide:
            if not self.hover:
                self.hover = True
            return True
            # if self.entity_in_tile and self.obj is not None:
            #     if self.obj.datacard is False:
            #         self.obj.set_datacard(True)
        else:
            if self.hover: #and not self.entity_in_tile:
                self.hover = False
            return False
            # if self.entity_in_tile and self.obj is not None:
            #     if self.obj.datacard is True:
            #         self.obj.set_datacard(False)
            # if self.entity_in_tile and self.obj.datacard is True:
            #     self.obj.set_datacard(False)

    def check_mouse_collision(self, mouse_pos:tuple):
        pos_in_mask = mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y
        return self.rect.collidepoint(mouse_pos) and self.img_mask.get_at(pos_in_mask)

    def update_mask(self, pos_x, pos_y):
        '''Updates the hitbox of the tile if the coordinates had any changes.'''
        if self.img_mask is not None:
            if self.rect.x is not pos_x and self.rect.y is not pos_y:
                self.img_mask = pygame.mask.from_surface(self.img)
                self.rect = self.img.get_rect()
                self.rect.x = pos_x
                self.rect.y = pos_y
        else:
            self.img_mask = pygame.mask.from_surface(self.img)
            self.rect = self.img.get_rect()
            self.rect.x = pos_x
            self.rect.y = pos_y
    
    def use(self):
        self.img_mask = None
        self.rect = None

    def draw(self, screen: pygame.Surface, x, y, camera_zoom):
        # self.img = pygame.transform.scale_by(self.current_imgs[self.animation_state], camera_zoom)
        self.update_mask(x,y)

        if self.hover:
            screen.blit(self.img, (x, y - self.img.get_height()/2))
        else: 
            screen.blit(self.img, (x, y))

class Basic_attack(Card):
    def __init__(self, cost, file):
        super().__init__(cost, file, 'Basic_attack')
    
    def set_imgs_entity(self, spritesheet):
        '''Set the animations of the entity'''
        self.original_img = spritesheet.image_at((0,0,30,40), (0,0,0))
        self.img = pygame.transform.scale_by(self.original_img, 4)

class Basic_defend(Card):
    def __init__(self, cost, file):
        super().__init__(cost, file, 'Basic_defend')
    
    def set_imgs_entity(self, spritesheet):
        '''Set the animations of the entity'''
        self.original_img = spritesheet.image_at((31,0,30,40), (0,0,0))
        self.img = pygame.transform.scale_by(self.original_img, 4)

class Hand:
    def __init__(self):
        self.cards = list()
        self.max_cards = 4
        self.current_cards = 0

    def check_selected_card(self, mouse_pos):
        for card in self.cards:
            if card.check_mouse_collision(mouse_pos):
                return True, card
        return False, None
    
    def hover_card(self, mouse_pos: tuple):
        for card in self.cards:
            collide = card.check_mouse_collision(mouse_pos)
            if card.hover_card(collide):
                return True
        return False

    def draw_card(self, deck: Deck) -> Card:
        card = None
        if self.current_cards + 1 < self.max_cards:
            if len(deck.cards) > 0:
                card = deck.cards.pop(0)
                self.cards.append(card)
            else:
                print('El mazo esta vacio!!!')
        else:
            print('No puedes robar mas!!')
        return card

    def use_card(self, card: Card, deck: Deck):
        deck.add_card(card)
        self.cards.remove(card)