from assembler import ASM
from roomEditor import RoomEditor


def updateWitch(rom):
    # Change the toadstool into a chest with the toadstool, so it can be put in the item pool
    re = RoomEditor(rom, 0x050)
    re.changeObject(2, 4, 0xA0)
    re.moveObject(2, 4, 2, 3)
    re.entities.clear()
    re.store(rom)
    rom.banks[0x14][0x560 + 0x050] = 0x50

    rom.patch(0x05, 0x08D4, 0x08F0, ASM("""
        ld  a, $09
        ldh [$F1], a
        ld  a, $02
        rst 8
        ld  a, $03
        rst 8
    """), fill_nop=True)
