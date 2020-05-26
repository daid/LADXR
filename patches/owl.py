from roomEditor import RoomEditor


def removeOwlEvents(rom):
    # Remove all the owl events from the entity tables.
    for room in range(0x100):
        re = RoomEditor(rom, room)
        if re.hasEntity(0x41):
            re.removeEntities(0x41)
            re.store(rom)
    # Clear texts used by the owl. Potentially reused somewhere else.
    rom.texts[0x0D9] = b'\xff'  # used by boomerang
    # 16 more available.
    # 1 Used by empty chest (master stalfos message)
    # 8 used by keysanity items
    for idx in range(0x0BE, 0x0CE):
        rom.texts[idx] = b'\xff'
