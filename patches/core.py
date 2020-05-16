from assembler import ASM

def noSwordMusic(rom):
    # Skip no-sword music override (replace specific jump calls with nops)
    rom.patch(2, 0x0151, "FA4EDB", "3E0100")
    rom.patch(2, 0x3B42, "FA4EDB", "3E0100")
    rom.patch(3, 0x0994, "FA4EDB", "3E0100")

def chestForSword(rom):
    # Patch the chest code, so it can give a lvl1 sword.
    # Normally, there is some code related to the owl event when getting the tail key,
    # as we patched out the owl. We can use this area to set the sword level when we get the sword from a chest.
    rom.patch(3, 0x109D, ASM("""
        cp $11
        jr nz, end
        push af
        ld   a, [$C501]
        ld   e, a
        ld   hl, $C2F0
        add  hl, de
        ld   [hl], $38
        pop af
    end:
    """), ASM("""
        cp $0B ; if not sword, skip
        jr nz, end
        push af
        ld   a, [$DB4E] ; load sword level
        xor  a
        jr   nz, skip
        inc  a
        ld   [$DB4E], a
    skip:
        pop af
    end:
    """))
    # Patch the palette used for the sword
    rom.patch(7, 0x3Ba9, "8410", "8415")
