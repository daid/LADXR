import typing


class ItemInfo:
    OPTIONS = []
    all = []  # type: typing.List[ItemInfo]

    def __init__(self):
        self.item = None
        self._location = None
        ItemInfo.all.append(self)

    def setLocation(self, location):
        self._location = location

    def getOptions(self):
        return self.OPTIONS

    def patch(self, rom, option):
        raise NotImplementedError()

    def read(self, rom):
        raise NotImplementedError()
