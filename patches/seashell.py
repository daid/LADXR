from assembler import ASM


def fixSeashell(rom):
    # Do not unload if we have the lvl2 sword.
    rom.patch(0x03, 0x1FD3, ASM("ld a, [$DB4E]\ncp $02\njp nc, $3F8D"), "", fill_nop=True)
    # Do not unload in the ghost house
    rom.patch(0x03, 0x1FE8, ASM("ldh  a, [$F8]\nand  $40\njp z, $3F8D"), "", fill_nop=True)

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
