from roomEditor import RoomEditor


def removeOwlEvents(rom):
    # Remove the owl, just do not run its event (this might break something)
    rom.patch(6, 0x27F7, "79EA01C5", "C9000000")
    # Owl code runs from 0x27F7 to 0x2A74
    rom.patch(6, 0x2A71, "CBA6C9", "CBA6C9")  # patch to check end of owl code

    # Remove all the owl events from the entity tables.
    for room in range(0x100):
        re = RoomEditor(rom, room)
        if re.hasEntity(0x41):
            re.removeEntities(0x41)
            re.store(rom)
