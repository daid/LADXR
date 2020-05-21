from assembler import ASM
from roomEditor import RoomEditor


def neverGetBowwow(rom):
    ### BowWow patches
    rom.patch(0x03, 0x1E0E, "EA56DB", "000000")  # Do not mark BowWow as kidnapped after we complete dungeon 1.
    rom.patch(0x15, 0x06B6, "FA56DBFE80C2", "FA56DBFE80CA")  # always load the moblin boss
    rom.patch(0x03, 0x182D, "FA56DBFE80C2", "FA56DBFE80CA")  # always load the cave moblins
    rom.patch(0x07, 0x3947, "FA56DBFE80C2", "FA56DBFE80CA")  # always load the cave moblin with sword
    # TODO: Do something at the end of the bowwow cave, maybe place a chest there?

    re = RoomEditor(rom, 0x024)
    re.removeEntities(0x7E)
    re.store(rom)

    re = RoomEditor(rom, 0x033)
    re.removeEntities(0xCC)
    re.store(rom)
