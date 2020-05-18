from .chest import Chest
from .items import *
from roomEditor import RoomEditor


class BeachSword(Chest):
    def __init__(self):
        super().__init__(0x0F2)
        self.room = 0x0F2

    def patch(self, rom, option):
        if option != SWORD:
            # Set the chest data
            super().patch(rom, option)

            # Patch the room to contain a chest instead of the sword on the beach
            re = RoomEditor(rom, 0x0F2)
            re.changeObject(7, 4, 0xA0)
            re.moveObject(7, 4, 5, 4)
            re.removeEntities(0x31)  # remove sword
            re.removeEntities(0x41)  # remove owl
            re.store(rom)

    def read(self, rom):
        re = RoomEditor(rom, 0x0F2)
        if re.hasEntity(0x31):
            return SWORD
        return super().read(rom)
