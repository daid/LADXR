from assembler import ASM


def neverGetBowwow(rom):
    ### BowWow patches
    rom.patch(0x03, 0x1DFE, "EA56DB", "000000")  # Do not mark BowWow as kidnapped after we complete dungeon 1.
    rom.patch(0x15, 0x06B6, "FA56DBFE80C2", "FA56DBFE80CA")  # always load the moblin boss
    rom.patch(0x03, 0x1824, "FA56DBFE80C2", "FA56DBFE80CA")  # always load the cave moblins
    rom.patch(0x07, 0x3983, "FA56DBFE80C2", "FA56DBFE80CA")  # always load the cave moblin with sword
    # TODO: Do something at the end of the bowwow cave, maybe place a chest there?

    # Basic patch to have the swamp flowers delete themselves directly.
    #  Could also patch to jump to the code area of the owl, and have some custom condition coded there.
    #  Which is why we didn't just delete the entities from the rooms.
    rom.patch(0x20, 0x7C * 3, "B56206", "843f00")
    rom.patch(0x20, 0x7e * 3, "FE6306", "843f00")
