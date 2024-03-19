from assembler import ASM

def fixTrendy(rom):
    rom.patch(0x04, 0x2F29, "04", "02")  # Patch the trendy game shield to be a rupee

    # Check the room flag to figure out how many items are available in total
    # This ensures we can keep playing until no items remain, and that we can no longer play when a restock is needed
    rom.patch(0x04, 0x2FAA, ASM("ld a, [$DB40]"), ASM("call $7FFA"))
    rom.patch(0x04, 0x3FFA, "00" * 6, ASM("""
        ld  a, [$DAA0]
        and $20
        ret
    """))
