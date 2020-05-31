from .itemInfo import ItemInfo


class Witch(ItemInfo):
    OPTIONS = ["MAGIC_POWDER"]

    def patch(self, rom, option, *, cross_world=False):
        pass

    def read(self, rom):
        return "MAGIC_POWDER"
