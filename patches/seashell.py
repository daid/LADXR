from assembler import ASM


def fixSeashell(rom):
    # Do not unload if we have the lvl2 sword.
    rom.patch(0x03, 0x1FD3, ASM("ld a, [$DB4E]\ncp $02\njp nc, $3F8D"), "", fill_nop=True)
    # Do not unload in the ghost house
    rom.patch(0x03, 0x1FE8, ASM("ldh  a, [$FFF8]\nand  $40\njp z, $3F8D"), "", fill_nop=True)

    # Call our special rendering code
    rom.patch(0x03, 0x1FF2, ASM("ld de, $5FD1\ncall $3C77"), ASM("ld a, $05\nrst 8"), fill_nop=True)

    # Call our special handlers for messages and pickup
    rom.patch(0x03, 0x2368, 0x237C, ASM("""
        ld   a, $0A  ; showMessageMultiworld
        rst  8
        ld   a, $06  ; giveItemMultiworld
        rst  8
        call $512A
        ret
    """), fill_nop=True)


def upgradeMansion(rom):
    rom.patch(0x19, 0x38EC, ASM("""
        ld   hl, $78DC
        jr   $03
    """), "", fill_nop=True)
    rom.patch(0x19, 0x38F1, ASM("""
        ld   hl, $78CC
        ld   c, $04
        call $3CE6
    """), ASM("""
        ld   a, $0C
        rst  8
    """), fill_nop=True)
    rom.patch(0x19, 0x3718, ASM("sub $13"), ASM("sub $0D"))
    rom.patch(0x19, 0x3697, ASM("""
        cp   $70
        jr   c, $15
        ld   [hl], $70
    """), ASM("""
        cp   $73
        jr   c, $15
        ld   [hl], $73
    """))
    rom.patch(0x19, 0x36F5, ASM("""
        ld   a, $02
        ld   [$DB4E], a
    """), ASM("""
        ld   a, $0E ; give item and message for current room multiworld
        rst  8
    """), fill_nop=True)
    rom.patch(0x19, 0x36E6, ASM("""
        ld   a, $9F
        call $2385
    """), "", fill_nop=True)
    rom.patch(0x19, 0x31E8, ASM("""
        ld   a, [$DB4E]
        and  $02
    """), ASM("""
        ld   a, [$DAE9]
        and  $10
    """))

    # Do not reset seashell counter
    rom.patch(0x19, 0x3700, ASM("ld [wSeashellsCount], a"), "", fill_nop=True)
    # Prevent missing out on a reward or getting the last reward multiple times
    rom.patch(0x19, 0x31CA, ASM("ld a, [wSeashellsCount]"), ASM("call $7F50"))
    rom.patch(0x19, 0x3215, ASM("ld a, [wSeashellsCount]"), ASM("call $7F50"))
    rom.patch(0x19, 0x32A2, ASM("ld a, [wSeashellsCount]"), ASM("call $7F50"))
    rom.patch(0x19, 0x38B3, ASM("ld a, [wSeashellsCount]"), ASM("call $7F50"))
    # This is using free space in bank 0x19 because we need to return a value in A when called
    rom.patch(0x19, 0x3F50, "00" * 0x30, ASM("""
    ; Maybe pretend like we have fewer seashells to prevent skipping a reward,
    ; or to prevent giving the final reward multiple times
        ld   a, [$DAE9] ; event flags for seashell mansion
        ld   d, a
        ld   a, [wSeashellsCount]
        bit  4, d ; got 20 shells prize
        jr   nz, limit0
        bit  5, d ; got 5 shells prize
        jr   z, limit5
        bit  6, d ; got 10 shells prize
        ret  nz
    limit10:
        cp   $10
        ret  c
        ld   a, $10
        ret
    limit5:
        cp   $05
        ret  c
        ld   a, $05
        ret
    limit0:
        xor  a
        ret
    """), fill_nop=True)
    # Give item after 5 or 10 seashells
    rom.patch(0x19, 0x38C0, 0x38CB, ASM("""
        ld   b, a
        ld   a, $11 ; HandleSeashellMansionItem
        rst  8
        ret
    """), fill_nop=True)
