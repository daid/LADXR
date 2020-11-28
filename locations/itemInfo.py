import typing
from checkMetadata import checkMetadataTable


class ItemInfo:
    OPTIONS = []
    MULTIWORLD = False

    def __init__(self, room=None):
        self.item = None
        self._location = None
        self.room = room
        self.metadata = checkMetadataTable.get(self.nameId, checkMetadataTable["None"])
        self.priority = 0
        self.forced_item = None

    @property
    def location(self):
        return self._location

    def setLocation(self, location):
        self._location = location

    def getOptions(self):
        return self.OPTIONS

    def configure(self, options):
        pass

    def read(self, rom):
        raise NotImplementedError()

    def patch(self, rom, option, *, multiworld=None):
        raise NotImplementedError()

    def __repr__(self):
        return self.__class__.__name__
    
    @property
    def nameId(self):
        return "0x%03X" % self.room if self.room is not None else "None"
