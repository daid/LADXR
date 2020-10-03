from .droppedKey import DroppedKey
from .items import *


class Instrument(DroppedKey):
    # Thanks to patches, a seashell is just a dropped key as far as the randomizer is concerned.

    def configure(self, options):
        if not options.instruments:
            self.OPTIONS = ["INSTRUMENT%d" % (self._location.dungeon)]
