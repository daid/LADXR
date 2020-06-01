from .itemInfo import ItemInfo
from .constants import *
from utils import formatText
from assembler import ASM


class ShopItem(ItemInfo):
    OPTIONS = [BOMB]

    def __init__(self, index):
        super().__init__()
        self.__index = index

    def configure(self, options):
        if self.__index < 2:
            self.OPTIONS = [BOW, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS, OCARINA, FEATHER, SHOVEL, BOOMERANG]

    def patch(self, rom, option, *, cross_world=False):
        assert not cross_world
        if self.__index == 0:
            rom.patch(0x04, 0x37C5, "0B", INVENTORY_MAP[option])
            rom.patch(0x04, 0x3AA9, ASM("ld d, $0B"), ASM("ld d, $%s" % (INVENTORY_MAP[option])))
            rom.patch(0x04, 0x3B5A, "9617", INVENTORY_ICON[option])
            rom.texts[0x030] = formatText(b"Deluxe %s 200 Rupees!\n____Buy__No Way" % (INVENTORY_NAME[option]), ask=True)
        elif self.__index == 1:
            rom.patch(0x04, 0x37C6, "05", INVENTORY_MAP[option])
            rom.patch(0x04, 0x3A73, ASM("ld d, $05"), ASM("ld d, $%s" % (INVENTORY_MAP[option])))
            rom.patch(0x04, 0x3B62, "8816", INVENTORY_ICON[option])
            rom.texts[0x02C] = formatText(b"%s Only 980 Rupees!\n____Buy__No Way" % (INVENTORY_NAME[option]), ask=True)

    def read(self, rom):
        if self.__index < 2:
            value = rom.banks[0x04][0x37C5 + self.__index]
            for k, v in INVENTORY_MAP.items():
                if int(v, 16) == value:
                    return k
            raise ValueError("Could not find start item contents in ROM (0x%02x)" % (value))
        return self.OPTIONS[0]
