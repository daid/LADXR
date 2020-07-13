from .droppedKey import DroppedKey


class AnglerKey(DroppedKey):
    def __init__(self):
        super().__init__(0x0CE)

    def patch(self, rom, option, *, multiworld=None):
        super().patch(rom, option, multiworld=multiworld)
        # As the angler key can be in 2 possible rooms, patch both.
        rom.banks[0x3E][0x3800 + 0x1F8] = rom.banks[0x3E][0x3800 + 0x0CE]
        rom.banks[0x3E][0x3300 + 0x1F8] = rom.banks[0x3E][0x3300 + 0x0CE]
