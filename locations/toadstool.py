from .chest import Chest
from .items import *


class Toadstool(Chest):
    def __init__(self):
        super().__init__(0x050)

    def configure(self, options):
        if not options.witch:
            self.OPTIONS = [TOADSTOOL]

    def read(self, rom):
        if len(self.OPTIONS) == 1:
            return TOADSTOOL
        return super().read(rom)
