from .itemInfo import ItemInfo


class KeyLocation(ItemInfo):
    OPTIONS = []

    def __init__(self, key):
        super().__init__()
        self.OPTIONS = [key]

    def patch(self, rom, option):
        pass

    def read(self, rom):
        return self.OPTIONS[0]

    def configure(self, options):
        pass

    @property
    def nameId(self):
        return self.OPTIONS[0] if self.OPTIONS and len(self.OPTIONS) == 1 else "None"
