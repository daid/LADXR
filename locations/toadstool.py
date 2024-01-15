from .droppedKey import DroppedKey
from .items import *


class Toadstool(DroppedKey):
    def __init__(self, room=0x050):
        super().__init__(room)

    def configure(self, options):
        if not options.witch:
            self.OPTIONS = [TOADSTOOL]
        else:
            super().configure(options)

    def read(self, rom):
        if len(self.OPTIONS) == 1:
            return TOADSTOOL
        return super().read(rom)
