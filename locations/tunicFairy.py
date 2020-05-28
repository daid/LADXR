from .itemInfo import ItemInfo
from .items import *


class TunicFairy(ItemInfo):
    OPTIONS = ["TUNIC"]

    def patch(self, rom, option):
        pass

    def read(self, rom):
        return "TUNIC"
