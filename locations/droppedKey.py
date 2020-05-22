from .itemInfo import ItemInfo


class DroppedKey(ItemInfo):
    OPTIONS = ["KEY"]

    def __init__(self, room):
        super().__init__()
        self.room = room

    def setLocation(self, location):
        self.OPTIONS = ["KEY%d" % (location.dungeon)]

    def patch(self, rom, option):
        rom.banks[0x3E][self.room + 0x3800] = 0x1A

    def read(self, rom):
        return self.OPTIONS[0]
