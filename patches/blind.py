from assembler import ASM


# Changes that make LADXR barely playable with a blindfold on.
def blindModeAdditions(rom):
    # Make a sound when you bump into solid tiles
    rom.patch(0x02, 0x3338, ASM("ld [$C144], a"), ASM("call $7FF8"))
    rom.patch(0x02, 0x3FF8, "00" * 8, ASM("ld [$C144], a\nld a, $07\nldh [hNoiseSfx], a\nret"))

    # Make a sound on room transitions
    rom.patch(0x02, 0x39CF, "FA79", "F07F")
    rom.patch(0x02, 0x3FF0, "00" * 7, ASM("ld a, $11\nldh [hJingle], a\njp $79FA"))

    # Do not use up bombs/powder/arrows so you can safely always use those
    rom.patch(0x00, 0x1367, ASM("sub a, 1"), "", fill_nop=True) # Bomb
    rom.patch(0x20, 0x0C53, ASM("sub a, 1"), "", fill_nop=True) # Powder
    rom.patch(0x00, 0x13D5, ASM("sub a, 1"), "", fill_nop=True) # Arrows

    # Slime eel always at the top left, if you manage to get this far, it is only fair
    rom.patch(0x05, 0x311F, ASM("and a, 3"), ASM("and a, 0"))
