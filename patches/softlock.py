from roomEditor import RoomEditor


def fixAll(rom):
    # Prevent soft locking in the first mountain cave if we do not have a feather
    re = RoomEditor(rom, 0x2B7)
    re.removeObject(3, 3)
    re.store(rom)

    allowRaftGameWithoutFlippers(rom)
    removeBirdKeyHoleDrop(rom)

def allowRaftGameWithoutFlippers(rom):
    # Allow jumping down the waterfall in the raft game without the flippers.
    rom.patch(0x02, 0x2EB1, ASM("ld a, [$DB0C]"), ASM("ld a, $01"), fill_nop=True)
    # Change the room that goes back up to the raft game from the bottom, so we no longer need flippers
    re = RoomEditor(rom, 0x1F7)
    re.changeObject(3, 2, 0x1B)
    re.changeObject(2, 3, 0x1B)
    re.changeObject(3, 4, 0x1B)
    re.changeObject(4, 5, 0x1B)
    re.changeObject(6, 6, 0x1B)
    re.store(rom)

def removeBirdKeyHoleDrop(rom):
    # Prevent the cave with the bird key from dropping you in the water
    # (if you do not have flippers this would softlock you)
    rom.patch(0x02, 0x1196, ASM("""
        ldh a, [$F7]
        cp $0A
        jr nz, $30
    """), ASM("""
        nop
        nop
        nop
        nop
        jr $30
    """))
    # Remove the hole that drops you all the way from dungeon7 entrance to the water in the cave
    re = RoomEditor(rom, 0x01E)
    re.removeObject(5, 4)
    re.store(rom)
