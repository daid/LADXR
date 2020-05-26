from .itemInfo import ItemInfo


class FlyingKey(ItemInfo):
    OPTIONS = ["KEY"]

    def __init__(self, room):
        super().__init__()
        self.room = room

    def configure(self, options):
        self.OPTIONS = ["KEY%d" % (self._location.dungeon)]

    def patch(self, rom, option):
        pass

    def read(self, rom):
        return self.OPTIONS[0]
