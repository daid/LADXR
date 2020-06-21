from .heartPiece import HeartPiece
from .items import *
from roomEditor import RoomEditor
from assembler import ASM


class BeachSword(HeartPiece):
    def __init__(self):
        super().__init__(0x0F2)

    def patch(self, rom, option, *, cross_world=False):
        if option != SWORD or cross_world or True:
            # Set the heart piece data
            super().patch(rom, option, cross_world=cross_world)

            # Patch the room to contain a chest instead of the sword on the beach
            re = RoomEditor(rom, 0x0F2)
            re.removeEntities(0x31)  # remove sword
            re.addEntity(5, 5, 0x35)  # add heart piece
            re.store(rom)

            # Prevent shield drops from the like-like from turning into swords.
            rom.patch(0x03, 0x1B9C, ASM("ld a, [$DB4E]"), ASM("ld a, $01"), fill_nop=True)
            rom.patch(0x03, 0x244D, ASM("ld a, [$DB4E]"), ASM("ld a, $01"), fill_nop=True)


    def read(self, rom):
        re = RoomEditor(rom, 0x0F2)
        if re.hasEntity(0x31):
            return SWORD
        return super().read(rom)
