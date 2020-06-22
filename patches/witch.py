from assembler import ASM
from roomEditor import RoomEditor


def updateWitch(rom):
    # Change the toadstool into a heartpiece which other patches turn into the toadstool, so it can be put in the item pool
    # This also makes it so you can only get this once.
    re = RoomEditor(rom, 0x050)
    re.entities.clear()
    re.addEntity(2, 3, 0x35)
    re.store(rom)

    # Change what happens when you trade the toadstool with the witch
    rom.patch(0x05, 0x08D4, 0x08F0, ASM("""
        ld  a, $09
        ldh [$F1], a
        ld  a, $02
        rst 8
        ld  a, $03
        rst 8
    """), fill_nop=True)
