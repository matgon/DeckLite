

class Enemy:

    def __init__(self, x, y, cell, hp, attk, dck, drop):
        self.pos = [x, y]
        self.cell = cell
        self.hp = hp
        self.attk = attk
        self.hab = dck
        self.drop = drop

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
    
