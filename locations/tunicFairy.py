from .itemInfo import ItemInfo
from .items import *


class TunicFairy(ItemInfo):
    OPTIONS = ["TUNIC"]

    def patch(self, rom, option, *, cross_world=False):
        pass

    def read(self, rom):
        return "TUNIC"
