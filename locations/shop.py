from .itemInfo import ItemInfo
from .items import *


class ShopItem(ItemInfo):
    OPTIONS = []

    def __init__(self, index):
        super().__init__()
        if index == 0:
            self.OPTIONS = [SHOVEL]
        elif index == 1:
            self.OPTIONS = [BOW]
        elif index == 2:
            self.OPTIONS = [BOMB]

    def patch(self, rom, option):
        # Quick patch to allow buying bombs at all times
        if option == BOMB:
            rom.patch(0x04, 0x37b5, "01020300", "01020304")

    def read(self, rom):
        return self.OPTIONS[0]
