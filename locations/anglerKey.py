from .itemInfo import ItemInfo
from .items import *


class AnglerKey(ItemInfo):
    OPTIONS = [ANGLER_KEY]

    def patch(self, rom, option):
        pass

    def read(self, rom):
        return ANGLER_KEY
