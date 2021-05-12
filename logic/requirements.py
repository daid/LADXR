from locations.items import *


class OR(list):
    def __init__(self, *args):
        super().__init__(args)

    def __repr__(self):
        return "or%s" % (super().__repr__())

    def remove(self, item):
        if item in self:
            super().remove(item)


class AND(list):
    def __init__(self, *args):
        super().__init__(args)

    def __repr__(self):
        return "and%s" % (super().__repr__())

    def remove(self, item):
        if item in self:
            super().remove(item)


class COUNT:
    def __init__(self, item, amount):
        self.item = item
        self.amount = amount

    def __eq__(self, other):
        return other.item == self.item and other.amount == self.amount

    def __hash__(self):
        return hash((self.item, self.amount))

    def __repr__(self):
        return "<%dx%s>" % (self.amount, self.item)


class FOUND:
    def __init__(self, item, amount):
        self.item = item
        self.amount = amount

    def __eq__(self, other):
        return other.item == self.item and other.amount == self.amount

    def __hash__(self):
        return hash((self.item, self.amount))

    def __repr__(self):
        return "<%dx%s>" % (self.amount, self.item)


def hasConsumableRequirement(requirements):
    if isinstance(requirements, list) or isinstance(requirements, tuple):
        return any(map(hasConsumableRequirement, requirements))
    if isinstance(requirements, COUNT):
        return hasConsumableRequirement(requirements.item)
    return isConsumable(requirements)


def isConsumable(item):
    if item is None:
        return False
    if item.startswith("RUPEES_") or item == "RUPEES":
        return True
    if item.startswith("KEY"):
        return True
    return False


class RequirementsSettings:
    def __init__(self, options):
        self.bush = OR(SWORD, MAGIC_POWDER, MAGIC_ROD, POWER_BRACELET, BOOMERANG)
        self.attack = OR(SWORD, BOMB, BOW, MAGIC_ROD, BOOMERANG)
        self.attack_hookshot = OR(SWORD, BOMB, BOW, MAGIC_ROD, BOOMERANG, HOOKSHOT) # switches, hinox, shrouded stalfos
        self.attack_hookshot_powder = OR(SWORD, BOMB, BOW, MAGIC_ROD, BOOMERANG, HOOKSHOT, MAGIC_POWDER) # zols, keese, moldorm
        self.attack_no_bomb = OR(SWORD, BOW, MAGIC_ROD, BOOMERANG, HOOKSHOT) # ?
        self.attack_hookshot_no_bomb = OR(SWORD, BOW, MAGIC_ROD, BOOMERANG, HOOKSHOT) # vire
        self.attack_no_boomerang = OR(SWORD, BOMB, BOW, MAGIC_ROD, HOOKSHOT) # teleporting owls
        self.attack_skeleton = OR(SWORD, BOMB, BOW, BOOMERANG, HOOKSHOT)  # cannot kill skeletons with the fire rod
        self.rear_attack = OR(SWORD, BOMB) # mimic
        self.rear_attack_range = OR(MAGIC_ROD, BOW) # mimic
        self.fire = OR(MAGIC_POWDER, MAGIC_ROD) # torches
        self.push_hardhat = OR(SHIELD, SWORD, HOOKSHOT, BOOMERANG)

        self.boss_requirements = [
            SWORD,  # D1 boss
            AND(OR(SWORD, MAGIC_ROD), POWER_BRACELET),  # D2 boss
            AND(PEGASUS_BOOTS, SWORD),  # D3 boss
            AND(FLIPPERS, OR(SWORD, MAGIC_ROD, BOW)),  # D4 boss
            AND(HOOKSHOT, SWORD),  # D5 boss
            BOMB,  # D6 boss
            AND(OR(MAGIC_ROD, SWORD, HOOKSHOT), COUNT(SHIELD, 2)),  # D7 boss
            MAGIC_ROD,  # D8 boss
            self.attack_no_bomb,  # D9 boss
        ]
        self.miniboss_requirements = {
            "ROLLING_BONES":    self.attack_hookshot,
            "HINOX":            self.attack_hookshot,
            "DODONGO":          BOMB,
            "CUE_BALL":         SWORD,
            "GHOMA":            OR(BOW, HOOKSHOT),
            "SMASHER":          POWER_BRACELET,
            "GRIM_CREEPER":     self.attack_no_bomb,
            "BLAINO":           SWORD,
            "AVALAUNCH":        self.attack_hookshot,
            "GIANT_BUZZ_BLOB":  MAGIC_POWDER,
            "MOBLIN_KING":      SWORD,
        }

        # Adjust for options
        if options.bowwow != 'normal':
            # We cheat in bowwow mode, we pretend we have the sword, as bowwow can pretty much do all what the sword ca$            # Except for taking out bushes (and crystal pillars are removed)
            self.bush.remove(SWORD)
        if options.logic == "casual":
            # In casual mode, remove the more complex kill methods
            self.bush.remove(MAGIC_POWDER)
            self.attack_hookshot_powder.remove(MAGIC_POWDER)
            self.attack.remove(BOMB)
            self.attack_hookshot.remove(BOMB)
            self.attack_hookshot_powder.remove(BOMB)
            self.attack_no_boomerang.remove(BOMB)
            self.attack_skeleton.remove(BOMB)


def flatten(req):
    result = set()
    if isinstance(req, OR):
        for r in req:
            for res in flatten(r):
                result.add(res)
    elif isinstance(req, AND):
        sets = []
        for r in req:
            sets.append(flatten(r))

        def _buildAND(target, r, idx):
            for s in sets[idx]:
                if idx < len(sets) - 1:
                    _buildAND(target, r.union(s), idx + 1)
                else:
                    target.add(frozenset(r.union(s)))
        _buildAND(result, set(), 0)
    else:
        result.add(frozenset((req,)))
    return result


def mergeFlat(req1, req2):
    result = req1.union(req2)
    result = set(filter(lambda s: all(map(lambda s2: not (s > s2), result)), result))
    return result


if __name__ == "__main__":
    req = AND("A", "B", "C")
    req = OR(req, "A")
    req = OR(req, "B")
    for res in mergeFlat(flatten(req), set()):
        print(">", res)
