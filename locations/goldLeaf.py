from .itemInfo import ItemInfo
from .items import *


class GoldLeaf(ItemInfo):
    OPTIONS = [GOLD_LEAF]

    def __init__(self, room):
        super().__init__()
        self.room = room

    def patch(self, rom, option):
        pass

    def read(self, rom):
        return GOLD_LEAF


class SlimeKey(ItemInfo):
    OPTIONS = ["SLIME_KEY"]

    def patch(self, rom, option):
        pass

    def read(self, rom):
        return "SLIME_KEY"
