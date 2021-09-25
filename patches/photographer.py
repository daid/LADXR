from assembler import ASM

def fixPhotographer(rom):
    # Allow richard photo without slime key
    rom.patch(0x36, 0x3234, ASM("jr nz, $52"), "", fill_nop=True)
    rom.patch(0x36, 0x3240, ASM("jr z, $46"), "", fill_nop=True)
    # Allow richard photo when castle is opened
    rom.patch(0x36, 0x71FF, ASM("jp nz, $7288"), "", fill_nop=True)
    # Allow photographer with bowwow saved
    rom.patch(0x36, 0x0398, ASM("or [hl]"), "", fill_nop=True)
    rom.patch(0x36, 0x3180, ASM("or [hl]"), "", fill_nop=True)
    rom.patch(0x36, 0x31CB, ASM("jp nz, $7288"), "", fill_nop=True)
    rom.patch(0x36, 0x03DC, ASM("and $7F"), ASM("and $00"))
