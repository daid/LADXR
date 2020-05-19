from .itemInfo import ItemInfo
from .items import *
from roomEditor import RoomEditor


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
    OPTIONS = [GOLD_LEAF]

    def patch(self, rom, option):
        pass

    def read(self, rom):
        return GOLD_LEAF
