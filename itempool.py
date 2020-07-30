import random
from locations.items import *


DEFAULT_ITEM_POOL = {
    SWORD: 2,
    FEATHER: 1,
    HOOKSHOT: 1,
    BOW: 1,
    BOMB: 2,
    MAGIC_POWDER: 1,
    MAGIC_ROD: 1,
    OCARINA: 1,
    PEGASUS_BOOTS: 1,
    POWER_BRACELET: 2,
    SHIELD: 2,
    SHOVEL: 1,

    TOADSTOOL: 1,

    TAIL_KEY: 1, SLIME_KEY: 1, ANGLER_KEY: 1, FACE_KEY: 1, BIRD_KEY: 1,
    GOLD_LEAF: 5,

    FLIPPERS: 1,
    BOWWOW: 1,
    SONG1: 1, SONG2: 1, SONG3: 1,

    BLUE_TUNIC: 1, RED_TUNIC: 1,
    MAX_ARROWS_UPGRADE: 1, MAX_BOMBS_UPGRADE: 1, MAX_POWDER_UPGRADE: 1,

    HEART_CONTAINER: 8,
    HEART_PIECE: 11,

    RUPEES_100: 3,
    RUPEES_20: 6,
    RUPEES_200: 3,
    RUPEES_50: 19,

    SEASHELL: 24,
    MEDICINE: 2,
    GEL: 4,
    MESSAGE: 1,

    COMPASS1: 1, COMPASS2: 1, COMPASS3: 1, COMPASS4: 1, COMPASS5: 1, COMPASS6: 1, COMPASS7: 1, COMPASS8: 1, COMPASS9: 1,
    KEY1: 3, KEY2: 5, KEY3: 9, KEY4: 5, KEY5: 3, KEY6: 3, KEY7: 3, KEY8: 7, KEY9: 3,
    MAP1: 1, MAP2: 1, MAP3: 1, MAP4: 1, MAP5: 1, MAP6: 1, MAP7: 1, MAP8: 1, MAP9: 1,
    NIGHTMARE_KEY1: 1, NIGHTMARE_KEY2: 1, NIGHTMARE_KEY3: 1, NIGHTMARE_KEY4: 1, NIGHTMARE_KEY5: 1, NIGHTMARE_KEY6: 1, NIGHTMARE_KEY7: 1, NIGHTMARE_KEY8: 1, NIGHTMARE_KEY9: 1,
    STONE_BEAK1: 1, STONE_BEAK2: 1, STONE_BEAK3: 1, STONE_BEAK4: 1, STONE_BEAK5: 1, STONE_BEAK6: 1, STONE_BEAK7: 1, STONE_BEAK8: 1, STONE_BEAK9: 1,
}


class ItemPool:
    def __init__(self, options, rnd):
        self.__pool = {}
        self.__setup(options)
        self.__randomizeRupees(options, rnd)

    def add(self, item, count=1):
        self.__pool[item] = self.__pool.get(item, 0) + count

    def remove(self, item, count=1):
        self.__pool[item] = self.__pool.get(item, 0) - count
        if self.__pool[item] == 0:
            del self.__pool[item]

    def get(self, item):
        return self.__pool.get(item, 0)

    def removeRupees(self, count):
        for n in range(count):
            self.removeRupee()

    def removeRupee(self):
        for item in (RUPEES_20, RUPEES_50, RUPEES_200, RUPEES_500):
            if self.get(item) > 0:
                self.remove(item)
                return
        raise RuntimeError("Wanted to remove more rupees from the pool then we have")

    def __setup(self, options):
        for item, count in DEFAULT_ITEM_POOL.items():
            self.add(item, count)
        if options.boomerang != 'default':
            self.add(BOOMERANG)
        if options.owlstatues == 'both':
            self.add(RUPEES_20, 9 + 24)
        elif options.owlstatues == 'dungeon':
            self.add(RUPEES_20, 24)
        elif options.owlstatues == 'overworld':
            self.add(RUPEES_20, 9)

        if options.bowwow == 'always':
            # Bowwow mode takes a sword from the pool to give as bowwow. So we need to fix that.
            self.add(SWORD)
            self.remove(BOWWOW)
        elif options.bowwow == 'swordless':
            # Bowwow mode takes a sword from the pool to give as bowwow, we need to remove all swords and Bowwow except for 1
            self.add(RUPEES_20, self.get(BOWWOW) + self.get(SWORD) - 1)
            self.remove(SWORD, self.get(SWORD) - 1)
            self.remove(BOWWOW, self.get(BOWWOW))
        if options.hpmode == 'inverted':
            self.add(BAD_HEART_CONTAINER, self.get(HEART_CONTAINER))
            self.remove(HEART_CONTAINER, self.get(HEART_CONTAINER))

        if options.itempool == 'casual':
            self.add(FLIPPERS)
            self.add(FEATHER)
            self.add(HOOKSHOT)
            self.add(BOW)
            self.add(BOMB)
            self.add(MAGIC_POWDER)
            self.add(MAGIC_ROD)
            self.add(OCARINA)
            self.add(PEGASUS_BOOTS)
            self.add(POWER_BRACELET)
            self.add(SHOVEL)
            self.removeRupees(11)

            for n in range(9):
                self.remove("MAP%d" % (n + 1))
                self.remove("COMPASS%d" % (n + 1))
                self.add("KEY%d" % (n +1))
                self.add("NIGHTMARE_KEY%d" % (n +1))
        elif options.itempool == 'pain':
            self.add(BAD_HEART_CONTAINER, 12)
            self.remove(BLUE_TUNIC)
            self.remove(MEDICINE, 2)
            self.remove(HEART_PIECE, 4)
            self.removeRupees(5)
        elif options.itempool == 'keyup':
            for n in range(9):
                self.remove("MAP%d" % (n + 1))
                self.remove("COMPASS%d" % (n + 1))
                self.add("KEY%d" % (n +1))
                self.add("NIGHTMARE_KEY%d" % (n +1))
            if options.owlstatues in ("none", "overworld"):
                for n in range(9):
                    self.remove("STONE_BEAK%d" % (n + 1))
                    self.add("KEY%d" % (n +1))

    def __randomizeRupees(self, options, rnd):
        # Remove rupees from the item pool and replace them with other items to create more variety
        rupee_item = []
        rupee_item_count = []
        for k, v in self.__pool.items():
            if k.startswith("RUPEES_") and v > 0:
                rupee_item.append(k)
                rupee_item_count.append(v)
        rupee_chests = sum(v for k, v in self.__pool.items() if k.startswith("RUPEES_"))
        for n in range(rupee_chests // 5):
            new_item = rnd.choices((BOMB, SINGLE_ARROW, ARROWS_10, MAGIC_POWDER, MEDICINE), (10, 5, 10, 10, 1))[0]
            while True:
                remove_item = rnd.choices(rupee_item, rupee_item_count)[0]
                if self.get(remove_item) > 0:
                    break
            self.add(new_item)
            self.remove(remove_item)

    def toDict(self):
        return self.__pool.copy()
