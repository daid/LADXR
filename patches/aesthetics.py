from assembler import ASM

def noSwordMusic(rom):
    # Skip no-sword music override
    # Instead of loading the sword level, we put the value 1 in the A register, indicating we have a sword.
    rom.patch(2, 0x0151, ASM("ld a, [$DB4E]"), ASM("ld a, $01"), fill_nop=True)
    rom.patch(2, 0x3AEF, ASM("ld a, [$DB4E]"), ASM("ld a, $01"), fill_nop=True)
    rom.patch(3, 0x0996, ASM("ld a, [$DB4E]"), ASM("ld a, $01"), fill_nop=True)

def removeNagMessages(rom):
    # Remove "this object is heavy, bla bla", and other nag messages when touching an object
    rom.patch(0x02, 0x2B8A, ASM("ld a, [$C5A6]\nand a"), ASM("ld a, $01\nand a"), fill_nop=True)
    rom.patch(0x02, 0x32EC, ASM("ld a, [$C5A6]\nand a"), ASM("ld a, $01\nand a"), fill_nop=True)

def removeLowHPBeep(rom):
    rom.patch(2,  0x233A, ASM("ld hl, $FFF3\nld [hl], $04"), b"", fill_nop=True) # Remove health beep

def slowLowHPBeep(rom):
    rom.patch(2, 0x2338, ASM("ld a, $30"), ASM("ld a, $60"))  # slow slow hp beep

def forceLinksPalette(rom, index):
    # This forces the link sprite into a specific palette index ignoring the tunic options.
    rom.patch(0, 0x1D8C,
            ASM("ld a, [$DC0F]\nand a\njr z, $03\ninc a"),
            ASM("ld a, $%02X" % (index)), fill_nop=True)
    rom.patch(0, 0x1DD2,
            ASM("ld a, [$DC0F]\nand a\njr z, $03\ninc a"),
            ASM("ld a, $%02X" % (index)), fill_nop=True)
