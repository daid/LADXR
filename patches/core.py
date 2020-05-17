from assembler import ASM

def noSwordMusic(rom):
    # Skip no-sword music override
    # Instead of loading the sword level, we put the value 1 in the A register, indicating we have a sword.
    rom.patch(2, 0x0151, ASM("ld a, [$DB4E]"), ASM("ld a, $01\nNOP"))
    rom.patch(2, 0x3B42, ASM("ld a, [$DB4E]"), ASM("ld a, $01\nNOP"))
    rom.patch(3, 0x0994, ASM("ld a, [$DB4E]"), ASM("ld a, $01\nNOP"))

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
    # Alternative, use the basic sword slash sprite:
    #  rom.patch(7, 0x3Ba9, "8410", "0410")

def removeGhost(rom):
    ## Ghost patch
    # Do not have the ghost follow you after dungeon 4
    rom.patch(0x03, 0x1E0A, ASM("LD [$DB79], A"), ASM("NOP\nNOP\nNOP"))

def removeBirdKeyDrop(rom):
    # Prevent the cave with the bird key from dropping you in the water
    # (if you do not have flippers this would softlock you)
    rom.patch(0x02, 0x1196, ASM("""
        ldh a, [$F7]
        cp $0A
        jr nz, $30
    """), ASM("""
        nop
        nop
        nop
        nop
        jr $30
    """))
