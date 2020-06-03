from assembler import ASM
from roomEditor import RoomEditor


def neverGetBowwow(rom):
    ### BowWow patches
    rom.patch(0x03, 0x1E0E, "EA56DB", "000000")  # Do not mark BowWow as kidnapped after we complete dungeon 1.
    rom.patch(0x15, 0x06B6, "FA56DBFE80C2", "FA56DBFE80CA")  # always load the moblin boss
    rom.patch(0x03, 0x182D, "FA56DBFE80C2", "FA56DBFE80CA")  # always load the cave moblins
    rom.patch(0x07, 0x3947, "FA56DBFE80C2", "FA56DBFE80CA")  # always load the cave moblin with sword

    # Modify the moblin cave to contain a chest at the end, which contains bowwow
    re = RoomEditor(rom, 0x2E2)
    re.removeEntities(0x6D)
    re.changeObject(8, 3, 0xA0)
    re.store(rom)
    rom.banks[0x14][0x560 + 0x2E2] = 0x81

    # Patch bowwow follower sprite to be used from 2nd vram bank
    rom.patch(0x05, 0x001C,
        b"40034023"
        b"42034223"
        b"44034603"
        b"48034A03"
        b"46234423"
        b"4A234823"
        b"4C034C23",
        b"500B502B"
        b"520B522B"
        b"540B560B"
        b"580B5A0B"
        b"562B542B"
        b"5A2B582B"
        b"5C0B5C2B")
    # Patch to use the chain sprite from second vram bank (however, the chain bugs out various things)
    rom.patch(0x05, 0x0282,
        ASM("ld a, $4E\njr nz, $02\nld a, $7E\nld [de], a\ninc de\nld a, $00"),
        ASM("ld a, $5E\nld [de], a\ninc de\nld a, $08"), fill_nop=True)
    # Never load the bowwow tiles in the first VRAM bank, as we do not need them.
    rom.patch(0x00, 0x2EB0, ASM("ld a, [$DB56]\ncp $01\nld a, $A4\njr z, $18"), "", fill_nop=True)

    # Patch the bowwow create code to call our custom check of we are in swamp function.
    rom.patch(0x01, 0x211F, ASM("ldh a, [$F6]\ncp $A7\nret z\nld a, [$DB56]\ncp $01\njr nz, $36"), ASM("""
        ld a, $07
        rst 8
        ld  a, e
        and a
        ret z
    """), fill_nop=True)
    # Patch bowwow to not stay around when we move from map to map
    rom.patch(0x05, 0x0049, ASM("ld [hl], a"), "", fill_nop=True)

    # Patch madam meow meow to not take bowwow
    rom.patch(0x06, 0x1BD7, ASM("ld a, [$DB66]\nand $02"), ASM("ld a, $00\nand $02"), fill_nop=True)

    # Patch kiki not to react to bowwow, as bowwow is not with link at this map
    rom.patch(0x07, 0x18A8, ASM("ld a, [$DB56]\ncp $01"), ASM("ld a, $00\ncp $01"), fill_nop=True)

    # Patch the color dungeon entrance not to check for bowwow
    rom.patch(0x02, 0x340D, ASM("ld hl, $DB56\nor [hl]"), "", fill_nop=True)

    # Patch richard to ignore bowwow
    rom.patch(0x06, 0x006C, ASM("ld a, [$DB56]"), ASM("xor a"), fill_nop=True)

    return
    # Load followers in dungeons
    rom.patch(0x01, 0x1FCA, ASM("ret c"), "", fill_nop=True)

    # Patch to modify how bowwow eats enemies, normally it just unloads them.
    rom.patch(0x05, 0x03A0, 0x03A8, ASM("""
        ; pack 'de' into 'bc', as 'de' get corrupted during the farcall, and we need de to know which entity to hurt
        ld   b, e
        ld   a, $06
        rst  8
        ret
    """), fill_nop=True)
    # Code for bank 3E, but bugs out most bosses if you let bowwow eat them
    """
        dw   BowwowEat          ; 6

BowwowEat:
        ; bc and de where packed into bc, unpack them
        ld  e, b
        xor a
        ld  b, a
        ld  d, a
        
        ld  hl, $C280
        add hl, de
        ld  [hl], $01
        
        ret    
    """
