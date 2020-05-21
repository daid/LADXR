from .items import *
from .chest import Chest
from roomEditor import RoomEditor
from assembler import ASM


class BirdKey(Chest):
    def __init__(self):
        super().__init__(0x27A)

    def patch(self, rom, option):
        re = RoomEditor(rom, self.room)

        if option != BIRD_KEY:
            super().patch(rom, option)

            # Patch the room to contain a chest instead of the key
            re.removeEntities(0x30)  # remove the key
            re.moveObject(8, 6, 4, 2)  # Change one of the holes into a chest.
            re.changeObject(4, 2, 0xA0)

        # Make the bird key accessible without the rooster
        re.removeObject(1, 6)
        re.removeObject(2, 6)
        re.removeObject(3, 5)
        re.removeObject(3, 6)
        re.moveObject(1, 5, 2, 6)
        re.moveObject(2, 5, 3, 6)
        re.addEntity(3, 5, 0x9D)

        re.store(rom)

        # Do not give the rooster
        rom.patch(0x19, 0x0E9D, ASM("ld [$DB7B], a"), "", fill_nop=True)

    def read(self, rom):
        re = RoomEditor(rom, self.room)
        if re.hasEntity(0x30):
            return BIRD_KEY
        return super().read(rom)
