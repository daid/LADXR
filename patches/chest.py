from assembler import ASM
from utils import formatText


# TODO: There is a lot more to fix with chests.
def fixChests(rom):
    # Patch the chest message tables to be correct for the dungeon keys
    rom.patch(0x07, 0x3bd5, "909192939495969798999A9B9C9D9E9FA0A1A2A3A4A5",
                            "909189939495969798999A9B9C9D9E9FA0A1A3A4A5E8")
    # No default text for getting the bow, so use an unused slot.
    rom.texts[0x89] = formatText(b"Found the bow!")

    # Patch the chest to give 10 bombs instead of 1
    # (I do not see it limit the amount of bombs here, so this could overflow the bomb count)
    rom.patch(0x03, 0x1111,
        ASM("ld hl, $DB4D\nld a, [hl]\nadd a, $01"),
        ASM("ld hl, $DB4D\nld a, [hl]\nadd a, $0A"))

    # Patch the chest code, so it can give a lvl1 sword.
    # Normally, there is some code related to the owl event when getting the tail key,
    # as we patched out the owl. We can use this area to set the sword level when we get the sword from a chest.
    rom.patch(0x03, 0x109D, ASM("""
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
        and  a
        jr   nz, skip
        inc  a
        ld   [$DB4E], a
    skip:
        pop af
    end:
    """))

    # Patch the palette used for the sword in the chest
    rom.patch(7, 0x3Ba9, "8410", "8415")
    # Alternative, use the basic sword slash sprite:
    #  rom.patch(7, 0x3Ba9, "8410", "0410")
    # Patch the palette used for the bow in the chest
    rom.patch(7, 0x3B97, "8810", "8815")
