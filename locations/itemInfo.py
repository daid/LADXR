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
        self.forced_item = None

    @property
    def location(self):
        return self._location

    def setLocation(self, location):
        self._location = location

    def getOptions(self):
        return self.OPTIONS

    def configure(self, options):
        # Add items that can be anywhere due to dungeon items setting
        self.OPTIONS = self.OPTIONS.copy()
        for n in range(10):
            if options.dungeon_keys == 'keysanity':
                self.OPTIONS += [f"KEY{n}"]
            if options.nightmare_keys == 'keysanity':
                self.OPTIONS += [f"NIGHTMARE_KEY{n}"]
            if options.dungeon_beaks == 'keysanity':
                self.OPTIONS += [f"STONE_BEAK{n}"]
            if options.dungeon_maps == 'keysanity':
                self.OPTIONS += [f"MAP{n}", f"COMPASS{n}"]

        if self._location.dungeon is not None:
            # Add items specific to this dungeon
            d = self._location.dungeon
            if options.dungeon_keys != 'keysanity':
                self.OPTIONS += [f"KEY{d}"]
            if options.nightmare_keys != 'keysanity':
                self.OPTIONS += [f"NIGHTMARE_KEY{d}"]
            if options.dungeon_beaks != 'keysanity':
                self.OPTIONS += [f"STONE_BEAK{d}"]
            if options.dungeon_maps != 'keysanity':
                self.OPTIONS += [f"MAP{d}", f"COMPASS{d}"]

    def read(self, rom):
        raise NotImplementedError()

    def patch(self, rom, option, *, multiworld=None):
        raise NotImplementedError()

    def __repr__(self):
        return self.__class__.__name__
    
    @property
    def nameId(self):
        return "0x%03X" % self.room if self.room is not None else "None"
