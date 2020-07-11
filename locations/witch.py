from .constants import *
from .itemInfo import ItemInfo


class Witch(ItemInfo):

    def __init__(self):
        super().__init__(0x2A2)

    OPTIONS = [POWER_BRACELET, SHIELD, BOW, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS, OCARINA,
        FEATHER, SHOVEL, MAGIC_POWDER, BOMB, SWORD, FLIPPERS, MAGNIFYING_LENS, MEDICINE,
        TAIL_KEY, ANGLER_KEY, FACE_KEY, BIRD_KEY, GOLD_LEAF, SLIME_KEY,
        RUPEES_50, RUPEES_20, RUPEES_100, RUPEES_200, RUPEES_500,
        SEASHELL, BOOMERANG, HEART_PIECE, BOWWOW, ARROWS_10, SINGLE_ARROW,
        MAX_POWDER_UPGRADE, MAX_BOMBS_UPGRADE, MAX_ARROWS_UPGRADE, RED_TUNIC, BLUE_TUNIC,
        HEART_CONTAINER, BAD_HEART_CONTAINER]

    def configure(self, options):
        if not options.witch:
            self.OPTIONS = [MAGIC_POWDER]

    def patch(self, rom, option, *, multiworld=None):
        assert multiworld is None
        if len(self.OPTIONS) == 1:
            return
        rom.banks[0x05][0x08D5] = CHEST_ITEMS[option]

    def read(self, rom):
        if len(self.OPTIONS) == 1:
            return self.OPTIONS[0]
        value = rom.banks[0x05][0x08D5]
        for k, v in CHEST_ITEMS.items():
            if v == value:
                return k
        raise ValueError("Could not find witch contents in ROM (0x%02x)" % (value))
