from .itemInfo import ItemInfo
from .constants import *


class DroppedKey(ItemInfo):
    OPTIONS = [POWER_BRACELET, SHIELD, BOW, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS, OCARINA,
        FEATHER, SHOVEL, MAGIC_POWDER, BOMB, SWORD, FLIPPERS, MAGNIFYING_LENS, MEDICINE,
        TAIL_KEY, ANGLER_KEY, FACE_KEY, BIRD_KEY, GOLD_LEAF, SLIME_KEY,
        RUPEES_50, RUPEES_20, RUPEES_100, RUPEES_200, RUPEES_500,
        SEASHELL, BOOMERANG, HEART_PIECE]
    MULTIWORLD = True

    def __init__(self, room):
        super().__init__()
        self.room = room

    def configure(self, options):
        if options.keysanity:
            self.OPTIONS = DroppedKey.OPTIONS
            for n in range(10):
                self.OPTIONS += ["KEY%d" % (n), "MAP%d" % (n), "COMPASS%d" % (n), "STONE_BEAK%d" % (n), "NIGHTMARE_KEY%d" % (n)]
        elif self._location.dungeon is not None:
            d = self._location.dungeon
            self.OPTIONS = DroppedKey.OPTIONS + ["MAP%d" % (d), "COMPASS%d" % (d), "STONE_BEAK%d" % (d), "NIGHTMARE_KEY%d" % (d), "KEY%d" % (d)]

    def patch(self, rom, option):
        if option.startswith(MAP) or option.startswith(COMPASS) or option.startswith(STONE_BEAK) or option.startswith(NIGHTMARE_KEY) or option.startswith(KEY):
            if self._location.dungeon == int(option[-1]):
                option = option[:-1]
        rom.banks[0x3E][self.room + 0x3800] = CHEST_ITEMS[option]
        if self.room == 0x169:  # Room in D4 where the key drops down the hole into the sidescroller
            rom.banks[0x3E][0x017C + 0x3800] = CHEST_ITEMS[option]


    def read(self, rom):
        assert self._location is not None, hex(self.room)
        value = rom.banks[0x3E][self.room + 0x3800]
        for k, v in CHEST_ITEMS.items():
            if v == value:
                if k in [MAP, COMPASS, STONE_BEAK, NIGHTMARE_KEY, KEY]:
                    assert self._location.dungeon is not None, "Dungeon item outside of dungeon? %r" % (self)
                    return "%s%d" % (k, self._location.dungeon)
                return k
        raise ValueError("Could not find chest contents in ROM (0x%02x)" % (value))

    def __repr__(self):
        if self._location and self._location.dungeon:
            return "%s:%03x:%d" % (self.__class__.__name__, self.room, self._location.dungeon)
        else:
            return "%s:%03x" % (self.__class__.__name__, self.room)
