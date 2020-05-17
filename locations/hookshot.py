from .itemInfo import ItemInfo
from .items import *


"""
The hookshot is dropped by the master stalfos.
The master stalfos drops a "key" with, and modifies a bunch of properties:

    ld   a, $30                                   ; $7EE1: $3E $30
    call SpawnNewEntity_trampoline                ; $7EE3: $CD $86 $3B

And then the dropped key handles the rest with room number specific code.
"""


class HookshotDrop(ItemInfo):
    OPTIONS = [HOOKSHOT]

    def __init__(self):
        super().__init__()

    def patch(self, rom, option):
        pass

    def read(self, rom):
        return self.OPTIONS[0]
