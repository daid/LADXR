from .itemInfo import ItemInfo
from .constants import *


class MadBatter(ItemInfo):
    OPTIONS = [POWER_BRACELET, SHIELD, BOW, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS, OCARINA,
        FEATHER, SHOVEL, MAGIC_POWDER, BOMB, SWORD, FLIPPERS, MAGNIFYING_LENS, MEDICINE,
        TAIL_KEY, ANGLER_KEY, FACE_KEY, BIRD_KEY, GOLD_LEAF, SLIME_KEY,
        RUPEES_50, RUPEES_20, RUPEES_100, RUPEES_200, RUPEES_500,
        SEASHELL, BOOMERANG, HEART_PIECE, ARROWS_10, SINGLE_ARROW,
        MAX_POWDER_UPGRADE, MAX_BOMBS_UPGRADE, MAX_ARROWS_UPGRADE, RED_TUNIC, BLUE_TUNIC]
    MULTIWORLD = True

    def configure(self, options):
        return

    def patch(self, rom, option, *, multiworld=None):
        rom.banks[0x18][0x0F90 + (self.room & 0x0F)] = CHEST_ITEMS[option]
        if multiworld is not None:
            rom.banks[0x3E][0x3300 + self.room] = multiworld

    def read(self, rom):
        assert self._location is not None, hex(self.room)
        value = rom.banks[0x18][0x0F90 + (self.room & 0x0F)]
        for k, v in CHEST_ITEMS.items():
            if v == value:
                return k
        raise ValueError("Could not find mad batter contents in ROM (0x%02x)" % (value))

    def __repr__(self):
        return "%s:%03x" % (self.__class__.__name__, self.room)
