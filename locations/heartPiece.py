from .itemInfo import ItemInfo
from .items import *


class HeartPiece(ItemInfo):
    OPTIONS = [HEART_PIECE]

    def __init__(self, room):
        super().__init__()
        self.room = room

    def patch(self, rom, option):
        pass

    def read(self, rom):
        return HEART_PIECE

    def __repr__(self):
        return "%s:%03x" % (self.__class__.__name__, self.room)
