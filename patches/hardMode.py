from assembler import ASM


def enableHardMode(rom):
    # Reduce iframes
    rom.patch(0x03, 0x2DB2, ASM("ld a, $50"), ASM("ld a, $20"))

    # Make bomb explosions damage you.
    rom.patch(0x03, 0x2618, ASM("""
        ld   hl, $C440
        add  hl, bc
        ld   a, [hl]
        and  a
        jr   nz, $05
    """), ASM("""
        call $6625
    """), fill_nop=True)
    # Reduce bomb blast push back on link
    rom.patch(0x03, 0x2643, ASM("sla [hl]"), ASM("sra [hl]"), fill_nop=True)
    rom.patch(0x03, 0x2648, ASM("sla [hl]"), ASM("sra [hl]"), fill_nop=True)

    # Never spawn a piece of power or acorn
    rom.patch(0x03, 0x1608, ASM("jr nz, $05"), ASM("jr $05"))
    rom.patch(0x03, 0x1642, ASM("jr nz, $04"), ASM("jr $04"))

    # Let hearts only recover half a container instead of a full one.
    rom.patch(0x03, 0x24B7, ASM("ld a, $08"), ASM("ld a, $04"))
    # Don't randomly drop fairies from enemies, drop a rupee instead
    rom.patch(0x03, 0x15C7, "2E2D382F2E2D3837", "2E2D382E2E2D3837")

    # Make dropping in water without flippers damage you.
    rom.patch(0x02, 0x3722, ASM("ldh a, [$AF]"), ASM("ld a, $06"))
