
class Deck:

    def __init__(self, hp, attk, hab, drop):
        self.hp = hp
        self.attk = attk
        self.hab = hab
        self.drop = drop

# metodos observadores
    def get_hp(self):
        return self.hp
    def get_attack(self):
        return self.attk
    def get_habilities(self):
        return self.hab
    def get_drops(self):
        return self.drop
    
    