from assembler import ASM


def upgradeMamu(rom):
    # Always allow the sign maze instead of only allowing the sign maze if you do not have song3
    rom.patch(0x00, 0x2057, ASM("ld a, [$DB49]"), ASM("ld a, $00"), fill_nop=True)

    # Patch the condition at which Mamu gives you the option to listen to him
    rom.patch(0x18, 0x0031, ASM("""
        ld   a, [$DB49]
        and  $01
    """), ASM("""
        ld   a, [$DAFB] ; load room flag of the Mamu room
        and  $10
    """), fill_nop=True)

    # Patch given an item
    rom.patch(0x18, 0x0270, ASM("""
        ld   a, $02
        ld   [$DB4A], a
        ld   hl, $DB49
        set  0, [hl]
    """), ASM("""
        ld   a, [$474D]
        ldh  [$F1], a
        ; Call rst 8 for chest item
        ld   a, $02
        rst  8
    """), fill_nop=True)
    # Patch show the right item instead of the ocarina
    rom.patch(0x18, 0x0299, ASM("""
        ld   de, $474D
        xor  a
        ldh  [$F1], a
        call $3C77
    """), ASM("""
        ld   a, [$474D]
        ldh  [$F1], a
        ; Call rst 8 to show item
        ld   a, $01
        rst  8
    """), fill_nop=True)
    # Patch to show the right message for the item
    rom.patch(0x18, 0x0282, ASM("""
        ld   a, $DF
        call $4087
    """), ASM("""
        ;ld   a, [$474D]
        ;ldh  [$F1], a
        ; Call rst 8 to show message
        ;ld   a, $03
        ;rst  8

        ; Set the room complete flag.
        ld   hl, $DAFB
        set  4, [hl]
    """), fill_nop=True)

    rom.patch(0x18, 0x074D, "90", "8D")
