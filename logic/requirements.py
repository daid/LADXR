from locations import *


class OR(list):
    def __init__(self, *args):
        super().__init__(args)

    def __repr__(self):
        return "or%s" % (super().__repr__())


class AND(list):
    def __init__(self, *args):
        super().__init__(args)

    def __repr__(self):
        return "and%s" % (super().__repr__())


class COUNT:
    def __init__(self, item, amount):
        self.item = item
        self.amount = amount

    def __repr__(self):
        return "%dx%s" % (self.amount, self.item)


bush = OR(SWORD, BOMB, MAGIC_POWDER, MAGIC_ROD, POWER_BRACELET)
attack = OR(SWORD, BOMB, BOW, MAGIC_ROD, BOOMERANG)
attack_no_bomb = OR(SWORD, BOW, MAGIC_ROD, BOOMERANG)
attack_skeleton = OR(SWORD, BOMB, BOW, BOOMERANG)  # cannot kill skeletons with the fire rod
rear_attack = OR(SWORD, BOMB)
fire = OR(MAGIC_POWDER, MAGIC_ROD)
