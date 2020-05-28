from assembler import ASM

def setStartHealth(rom, amount):
    rom.patch(0x01, 0x0B1C, ASM("ld  [hl], $03"), ASM("ld  [hl], $%02X" % (amount)))  # max health of new save
    rom.patch(0x01, 0x0B14, ASM("ld  [hl], $18"), ASM("ld  [hl], $%02X" % (amount * 8)))  # current health of new save

def inverseHealthContainers(rom):
    rom.patch(0x03, 0x19F0, ASM("""
        ld  hl, $DB5B
        inc [hl]
        ld  hl, $DB93
        ld   [hl], $FF
    """), ASM("""
        ld  a, $06
        rst 8
    """), fill_nop=True)  # add heart->remove heart on heart container
    rom.patch(0x03, 0x19D8, "AA14AA34", "AA17AA37")  # Change color of the heart containers
