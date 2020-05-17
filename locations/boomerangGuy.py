from .itemInfo import ItemInfo


class BoomerangGuy(ItemInfo):
    OPTIONS = ["BOOMERANG"]

    def patch(self, rom, option):
        pass

    def read(self, rom):
        return "BOOMERANG"
