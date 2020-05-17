from .itemInfo import ItemInfo


class Witch(ItemInfo):
    OPTIONS = ["MAGIC_POWDER"]

    def patch(self, rom, option):
        pass

    def read(self, rom):
        return "MAGIC_POWDER"
