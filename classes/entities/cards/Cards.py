
class Card:
    def __init__(self, cost, type):
        self.cost = cost
        self.type = type
# metodos observadores
    def get_cost(self):
        return self.cost
    def get_type(self):
        return self.type

#------------------------------------------------------------
class Sword_slice (Card):
    def __init__(self, cost, attk, drop):
        super().__init__(cost, 'slice')
        self.attk = attk

# metodos observadores
    def get_attack(self):
        return self.attk