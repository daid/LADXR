from .droppedKey import DroppedKey
from roomEditor import RoomEditor
from assembler import ASM


class BirdKey(DroppedKey):
    def __init__(self):
        super().__init__(0x27A)

    def patch(self, rom, option, *, multiworld=None):
        super().patch(rom, option, multiworld=multiworld)

        re = RoomEditor(rom, self.room)

        # Make the bird key accessible without the rooster
        re.removeObject(1, 6)
        re.removeObject(2, 6)
        re.removeObject(3, 5)
        re.removeObject(3, 6)
        re.moveObject(1, 5, 2, 6)
        re.moveObject(2, 5, 3, 6)
        re.addEntity(3, 5, 0x9D)
        re.store(rom)
        rom.patch(0x19, 0x0010,
                  "F0007806F008782600007A0600087A26",
                  "F000640FF008642F0000660F0008662F")
        rom.patch(0x19, 0x004F, ASM("cp $01"), ASM("cp $0A"))

        # Do not give the rooster
        rom.patch(0x19, 0x0E9D, ASM("ld [$DB7B], a"), "", fill_nop=True)
