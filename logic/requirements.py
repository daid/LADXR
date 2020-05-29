from locations.items import *


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
        return "<%dx%s>" % (self.amount, self.item)


def hasConsumableRequirement(requirements):
    if isinstance(requirements, list) or isinstance(requirements, tuple):
        return any(map(hasConsumableRequirement, requirements))
    if isinstance(requirements, COUNT):
        return isConsumable(requirements.item)
    return isConsumable(requirements)


def isConsumable(item):
    if item.startswith("RUPEES_"):
        return True
    if item.startswith("KEY") and len(item) == 4:
        return True
    return False


bush = OR(SWORD, MAGIC_POWDER, MAGIC_ROD, POWER_BRACELET)
attack = OR(SWORD, BOMB, BOW, MAGIC_ROD, BOOMERANG)
attack_hookshot = OR(SWORD, BOMB, BOW, MAGIC_ROD, BOOMERANG, HOOKSHOT)
attack_powder = OR(SWORD, BOMB, BOW, MAGIC_ROD, BOOMERANG, HOOKSHOT, POWDER)
attack_no_bomb = OR(SWORD, BOW, MAGIC_ROD, BOOMERANG, HOOKSHOT)
attack_skeleton = OR(SWORD, BOMB, BOW, BOOMERANG, HOOKSHOT)  # cannot kill skeletons with the fire rod
rear_attack = OR(SWORD, BOMB)
rear_attack_range = OR(MAGIC_ROD, BOW)
fire = OR(MAGIC_POWDER, MAGIC_ROD)
