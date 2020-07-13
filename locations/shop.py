from .itemInfo import ItemInfo
from .constants import *
from utils import formatText
from assembler import ASM


class ShopItem(ItemInfo):
    OPTIONS = [BOMB]

    def __init__(self, index):
        self.__index = index
        super().__init__(0x2A1)

    def configure(self, options):
        if self.__index < 2:
            self.OPTIONS = [SWORD, POWER_BRACELET, SHIELD, BOW, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS,
                            OCARINA, FEATHER, SHOVEL, BOOMERANG,
                            FLIPPERS, SLIME_KEY, TAIL_KEY, ANGLER_KEY, FACE_KEY, BIRD_KEY, GOLD_LEAF,
                            RUPEES_50, RUPEES_20, RUPEES_100, RUPEES_200, RUPEES_500, SEASHELL,
                            HEART_PIECE, BOWWOW,
                            MAX_POWDER_UPGRADE, MAX_BOMBS_UPGRADE, MAX_ARROWS_UPGRADE, RED_TUNIC, BLUE_TUNIC,
                            HEART_CONTAINER, BAD_HEART_CONTAINER]
            if options.keysanity:
                for n in range(10):
                    self.OPTIONS += ["KEY%d" % (n), "MAP%d" % (n), "COMPASS%d" % (n), "STONE_BEAK%d" % (n),
                                     "NIGHTMARE_KEY%d" % (n)]

    def patch(self, rom, option, *, multiworld=None):
        assert multiworld is None
        if self.__index == 0:
            rom.patch(0x04, 0x37C5, "08", "%02X" % (CHEST_ITEMS[option]))
            rom.texts[0x030] = formatText(b"Deluxe %s 200 Rupees!" % (INVENTORY_NAME[option]), ask=b"Buy  No Way")
        elif self.__index == 1:
            rom.patch(0x04, 0x37C6, "02", "%02X" % (CHEST_ITEMS[option]))
            rom.texts[0x02C] = formatText(b"%s Only 980 Rupees!" % (INVENTORY_NAME[option]), ask=b"Buy  No Way")

    def read(self, rom):
        if self.__index < 2:
            value = rom.banks[0x04][0x37C5 + self.__index]
            for k, v in CHEST_ITEMS.items():
                if v == value:
                    return k
            raise ValueError("Could not find start item contents in ROM (0x%02x)" % (value))
        return self.OPTIONS[0]

    @property
    def nameId(self):
        return "0x%03X-%s" % (self.room, self.__index)
