from assembler import ASM
from backgroundEditor import BackgroundEditor


def selectToSwitchSongs(rom):
    # Do not ignore left/right keys when ocarina is selected
    rom.patch(0x20, 0x1F18, ASM("and a"), ASM("xor a"))
    # Change the keys which switch the ocarina song to select and no key.
    rom.patch(0x20, 0x21A9, ASM("and $01"), ASM("and $40"))
    rom.patch(0x20, 0x21C7, ASM("and $02"), ASM("and $00"))

def moreSlots(rom):
    #Move flippers, medicine, trade item and seashells to DB3E+
    rom.patch(0x02, 0x292B, ASM("ld a, [$DB0C]"), ASM("ld a, [$DB3E]"))
    #rom.patch(0x02, 0x2E8F, ASM("ld a, [$DB0C]"), ASM("ld a, [$DB3E]"))
    rom.patch(0x02, 0x3713, ASM("ld a, [$DB0C]"), ASM("ld a, [$DB3E]"))
    rom.patch(0x20, 0x1A23, ASM("ld de, $DB0C"), ASM("ld de, $DB3E"))
    rom.patch(0x02, 0x23a3, ASM("ld a, [$DB0D]"), ASM("ld a, [$DB3F]"))
    rom.patch(0x02, 0x23d7, ASM("ld a, [$DB0D]"), ASM("ld a, [$DB3F]"))
    rom.patch(0x02, 0x23aa, ASM("ld [$DB0D], a"), ASM("ld [$DB3F], a"))
    rom.patch(0x04, 0x3b1f, ASM("ld [$DB0D], a"), ASM("ld [$DB3F], a"))
    rom.patch(0x06, 0x1f58, ASM("ld a, [$DB0D]"), ASM("ld a, [$DB3F]"))
    rom.patch(0x06, 0x1ff5, ASM("ld hl, $DB0D"), ASM("ld hl, $DB3F"))
    rom.patch(0x07, 0x3c33, ASM("ld [$DB0D], a"), ASM("ld [$DB3F], a"))
    rom.patch(0x00, 0x1e01, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x00, 0x2d21, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x00, 0x3199, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x03, 0x0ae6, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x03, 0x0b6d, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x03, 0x0f68, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x04, 0x2faa, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x04, 0x3502, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x04, 0x3624, ASM("ld [$DB0E], a"), ASM("ld [$DB40], a"))
    rom.patch(0x05, 0x0bff, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x05, 0x0d20, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x05, 0x0db1, ASM("ld [$DB0E], a"), ASM("ld [$DB40], a"))
    rom.patch(0x05, 0x0dd5, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x05, 0x0e8e, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x05, 0x11ce, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x06, 0x1a2c, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x06, 0x1a7c, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x06, 0x1ab1, ASM("ld [$DB0E], a"), ASM("ld [$DB40], a"))
    rom.patch(0x06, 0x2214, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x06, 0x223e, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x07, 0x02f8, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x07, 0x04bf, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x07, 0x057f, ASM("ld [$DB0E], a"), ASM("ld [$DB40], a"))
    rom.patch(0x07, 0x0797, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x07, 0x0856, ASM("ld [$DB0E], a"), ASM("ld [$DB40], a"))
    rom.patch(0x07, 0x0a21, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x07, 0x0a33, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x07, 0x0a58, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x07, 0x0a81, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x07, 0x0acf, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x07, 0x0af9, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x07, 0x0b31, ASM("ld [$DB0E], a"), ASM("ld [$DB40], a"))
    rom.patch(0x07, 0x0bcc, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x07, 0x0c23, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x07, 0x0c3c, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x07, 0x0c60, ASM("ld [$DB0E], a"), ASM("ld [$DB40], a"))
    rom.patch(0x07, 0x0d73, ASM("ld [$DB0E], a"), ASM("ld [$DB40], a"))
    rom.patch(0x07, 0x1549, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x07, 0x155d, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x07, 0x159f, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x07, 0x18e6, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x07, 0x19ce, ASM("ld [$DB0E], a"), ASM("ld [$DB40], a"))
    #rom.patch(0x15, 0x3F23, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x18, 0x0966, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x18, 0x0972, ASM("ld [$DB0E], a"), ASM("ld [$DB40], a"))
    rom.patch(0x18, 0x09f3, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x18, 0x0bf1, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x18, 0x0c2c, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x18, 0x0c6d, ASM("ld [$DB0E], a"), ASM("ld [$DB40], a"))
    rom.patch(0x18, 0x0c8b, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x18, 0x0ce4, ASM("ld [$DB0E], a"), ASM("ld [$DB40], a"))
    rom.patch(0x18, 0x0d3c, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x18, 0x0d4a, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x18, 0x0d95, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x18, 0x0da3, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x18, 0x0de4, ASM("ld [$DB0E], a"), ASM("ld [$DB40], a"))
    rom.patch(0x18, 0x0e7a, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x18, 0x0e91, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x18, 0x0eb6, ASM("ld [$DB0E], a"), ASM("ld [$DB40], a"))
    rom.patch(0x18, 0x219e, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x19, 0x05ec, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x19, 0x2d54, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x19, 0x2df2, ASM("ld [$DB0E], a"), ASM("ld [$DB40], a"))
    rom.patch(0x19, 0x2ef1, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x19, 0x2f95, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x20, 0x1b04, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x20, 0x1e42, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x36, 0x0948, ASM("ld a, [$DB0E]"), ASM("ld a, [$DB40]"))
    rom.patch(0x19, 0x31Ca, ASM("ld a, [$DB0F]"), ASM("ld a, [$DB41]"))
    rom.patch(0x19, 0x3215, ASM("ld a, [$DB0F]"), ASM("ld a, [$DB41]"))
    rom.patch(0x19, 0x32a2, ASM("ld a, [$DB0F]"), ASM("ld a, [$DB41]"))
    rom.patch(0x19, 0x3700, ASM("ld [$DB0F], a"), ASM("ld [$DB41], a"))
    rom.patch(0x19, 0x38b3, ASM("ld a, [$DB0F]"), ASM("ld a, [$DB41]"))
    rom.patch(0x19, 0x38c3, ASM("ld [$DB0F], a"), ASM("ld [$DB41], a"))
    rom.patch(0x20, 0x1a83, ASM("ld a, [$DB0F]"), ASM("ld a, [$DB41]"))

    # Fix the whole inventory rendering, this needs to extend a few tables with more entries so it moves tables
    # to the end of the bank as well.
    rom.patch(0x20, 0x3E53, "00" * 32,
        "9C019C06"
        "9C619C65"
        "9CA19CA5"
        "9CE19CE5"
        "9D219D25"
        "9D619D65"
        "9DA19DA5"
        "9DE19DE5")
    rom.patch(0x20, 0x1CC7, ASM("ld hl, $5C84"), ASM("ld hl, $7E53"))
    rom.patch(0x20, 0x1BCC, ASM("ld hl, $5C84"), ASM("ld hl, $7E53"))
    rom.patch(0x20, 0x1CF0, ASM("ld hl, $5C84"), ASM("ld hl, $7E53"))

    rom.patch(0x20, 0x1C8C,
        "9CC19CC59D219D259D819D859DE19DE5",
        "28283838484858586868787888889898")
    rom.patch(0x20, 0x22b3, ASM("ld hl, $6298"), ASM("ld hl, $5C8C"))
    rom.patch(0x20, 0x2298, "28284040", "08280828")

    # Piece of power overlay positions
    rom.patch(0x20, 0x233A,
        "1038103010301030103010300E0E2626",
        "10381030103010301030103010301030")
    rom.patch(0x20, 0x3E73, "00" * 16,
        "0E0E2626363646465656666676768686")
    rom.patch(0x20, 0x2377, ASM("ld hl, $6346"), ASM("ld hl, $7E73"))

    # Allow selecting the 4 extra slots.
    rom.patch(0x20, 0x1F33, ASM("ld a, $09"), ASM("ld a, $0D"))
    rom.patch(0x20, 0x1F54, ASM("ld a, $09"), ASM("ld a, $0D"))
    rom.patch(0x20, 0x1F2A, ASM("cp $0A"), ASM("cp $0E"))
    rom.patch(0x20, 0x1F4B, ASM("cp $0A"), ASM("cp $0E"))
    rom.patch(0x02, 0x217E, ASM("ld a, $0B"), ASM("ld a, $0F"))

    # Patch all the locations that iterate over inventory to check the extra slots
    rom.patch(0x02, 0x33FC, ASM("cp $0C"), ASM("cp $10"))
    rom.patch(0x03, 0x2475, ASM("ld e, $0C"), ASM("ld e, $10"))
    rom.patch(0x03, 0x248a, ASM("cp $0C"), ASM("cp $10"))
    rom.patch(0x04, 0x3849, ASM("ld c, $0B"), ASM("ld c, $0F"))
    rom.patch(0x04, 0x3862, ASM("ld c, $0B"), ASM("ld c, $0F"))
    rom.patch(0x04, 0x39C2, ASM("ld d, $0C"), ASM("ld d, $10"))
    rom.patch(0x04, 0x39E0, ASM("ld d, $0C"), ASM("ld d, $10"))
    rom.patch(0x04, 0x39FE, ASM("ld d, $0C"), ASM("ld d, $10"))
    rom.patch(0x05, 0x0F95, ASM("ld e, $0B"), ASM("ld e, $0F"))
    rom.patch(0x05, 0x0FD1, ASM("ld c, $0B"), ASM("ld c, $0F"))
    rom.patch(0x05, 0x1324, ASM("ld e, $0C"), ASM("ld e, $10"))
    rom.patch(0x05, 0x1339, ASM("cp $0C"), ASM("cp $10"))
    rom.patch(0x18, 0x005A, ASM("ld e, $0B"), ASM("ld e, $0F"))
    rom.patch(0x18, 0x0571, ASM("ld e, $0B"), ASM("ld e, $0F"))
    rom.patch(0x19, 0x0703, ASM("cp $0C"), ASM("cp $10"))
    rom.patch(0x20, 0x235C, ASM("ld d, $0C"), ASM("ld d, $10"))
    rom.patch(0x36, 0x31B8, ASM("ld e, $0C"), ASM("ld e, $10"))


    # Patch the toadstool as a different item
    rom.patch(0x20, 0x1C84, "9C019C" "069C61", "4C7F7F" "4D7F7F")
    rom.banks[0x20][0x1C32:0x1C8C] = rom.banks[0x20][0x1C30:0x1C8A]
    rom.patch(0x20, 0x1CDB, ASM("ld hl, $5C30"), ASM("ld hl, $5C32"))
    rom.patch(0x20, 0x1D0D, ASM("ld hl, $5C33"), ASM("ld hl, $5C35"))
    rom.patch(0x20, 0x1C30, "7F7F", "0A0B")

    # Allow usage of the toadstool
    rom.patch(0x00, 0x12CC, ASM("jp z, $148d"), ASM("jp $3FEF"))
    rom.patch(0x00, 0x3FEF, "00" * 17, ASM("""
        jr z, UseMagicPowder
        cp $0E
        jp nz, $12CF
        jp $1498
UseMagicPowder:
        jp $14A7
    """), fill_nop=True)
    # Fix the graphics of the toadstool hold over your head
    rom.patch(0x02, 0x121E, ASM("ld e, $8E"), ASM("ld e, $4C"))
    rom.patch(0x02, 0x1241, ASM("ld a, $14"), ASM("ld a, $1C"))

    # Do not remove powder when it is used up.
    rom.patch(0x20, 0x0C59, ASM("jr nz, $12"), ASM("jr $12"))

    # Patch the toadstool entity code to give the proper item, and not set the has-toadstool flag.
    rom.patch(0x03, 0x1D6F, ASM("""
        ld   a, $0A
        ldh  [$A5], a
        ld   d, $0C
        call $6472
        ld   a, $01
        ld   [$DB4B], a
    """), ASM("""
        ld   d, $0E
        call $6472
    """), fill_nop=True)

    # Patch the debug save game so it does not give a bunch of swords
    rom.patch(0x01, 0x0673, "01010100", "0D0E0000")

    # Patch the witch to use the new toadstool instead of the old flag
    rom.patch(0x05, 0x081A, ASM("ld a, [$DB4B]"), ASM("ld a, $01"), fill_nop=True)
    rom.patch(0x05, 0x082A, ASM("cp $0C"), ASM("cp $0E"))
    rom.patch(0x05, 0x083E, ASM("cp $0C"), ASM("cp $0E"))


def advancedInventorySubscreen(rom):
    # Instrument positions
    rom.patch(0x01, 0x2BCF,
              "0F51B1EFECAA4A0C",
              "090C0F12494C4F52")

    be = BackgroundEditor(rom, 2)
    be.tiles[0x9DA9] = 0x4A
    be.tiles[0x9DC9] = 0x4B
    for x in range(1, 10):
        be.tiles[0x9DE9 + x] = 0xB0 + (x % 9)
    be.tiles[0x9DE9] = 0xBA
    be.store(rom)
    be = BackgroundEditor(rom, 2, attributes=True)

    # Remove all attributes out of range.
    for y in range(0x9C00, 0x9E40, 0x20):
        for x in range(0x14, 0x20):
            del be.tiles[x + y]
    for n in range(0x9E40, 0xA020):
        del be.tiles[n]

    # Remove palette of instruments
    for y in range(0x9D00, 0x9E20, 0x20):
        for x in range(0x00, 0x14):
            be.tiles[x + y] = 0x01
    # And place it at the proper location
    for y in range(0x9D00, 0x9D80, 0x20):
        for x in range(0x09, 0x14):
            be.tiles[x + y] = 0x07

    # Key from 2nd vram bank
    be.tiles[0x9DA9] = 0x09
    be.tiles[0x9DC9] = 0x09
    # Nightmare heads from 2nd vram bank with proper palette
    for n in range(1, 10):
        be.tiles[0x9DA9 + n] = 0x0E

    be.store(rom)

    rom.patch(0x20, 0x19D3, ASM("ld bc, $5994\nld e, $33"), ASM("ld bc, $7E08\nld e, $%02x" % (0x33 + 24)))
    rom.banks[0x20][0x3E08:0x3E08+0x33] = rom.banks[0x20][0x1994:0x1994+0x33]
    rom.patch(0x20, 0x3E08+0x32, "00" * 25, "9DAA08464646464646464646" "9DCA08B0B0B0B0B0B0B0B0B0" "00")

    # instead of doing an GBC specific check, jump to our custom handling
    rom.patch(0x20, 0x19DE, ASM("ldh a, [$FE]\nand a\njr z, $40"), ASM("call $7F00"), fill_nop=True)

    rom.patch(0x20, 0x3F00, "00" * 0x100, ASM("""
        ld   a, [$DBA5] ; isIndoor
        and  a
        jr   z, RenderKeysCounts
        ldh  a, [$F7]   ; mapNr
        cp   $FF
        jr   z, RenderDungeonFix
        cp   $06
        jr   z, D7RenderDungeonFix
        cp   $08
        jr   c, RenderDungeonFix 

RenderKeysCounts:
        ; Check if we have each nightmare key, and else null out the rendered tile
        ld   hl, $D636
        ld   de, $DB19
        ld   c, $08
NKeyLoop:
        ld   a, [de]
        and  a
        jr   nz, .hasNKey
        ld   a, $7F
        ld   [hl], a
.hasNKey:
        inc  hl
        inc  de
        inc  de
        inc  de
        inc  de
        inc  de
        dec  c
        jr   nz, NKeyLoop

        ld   a, [$DDDD]
        and  a
        jr   nz, .hasCNKey
        ld   a, $7F
        ld   [hl], a
.hasCNKey:

        ; Check the small key count for each dungeon and increase the tile to match the number
        ld   hl, $D642
        ld   de, $DB1A
        ld   c, $08
KeyLoop:
        ld   a, [de]
        add  a, $B0
        ld   [hl], a
        inc  hl
        inc  de
        inc  de
        inc  de
        inc  de
        inc  de
        dec  c
        jr   nz, KeyLoop

        ld   a, [$DDDE]
        add  a, $B0
        ld   [hl], a
        ret

D7RenderDungeonFix:
        ld   de, D7DungeonFix
        ld   c, $11
        jr   RenderDungeonFixGo   

RenderDungeonFix:
        ld   de, DungeonFix
        ld   c, $0D
RenderDungeonFixGo:
        ld   hl, $D633
.copyLoop:
        ld   a, [de]
        inc  de
        ldi  [hl], a
        dec  c
        jr   nz, .copyLoop
        ret
        
DungeonFix:
        db   $9D, $09, $C7, $7F
        db   $9D, $0A, $C7, $7F
        db   $9D, $13, $C3, $7F
        db   $00
D7DungeonFix:
        db   $9D, $09, $C7, $7F
        db   $9D, $0A, $C7, $7F
        db   $9D, $6B, $48, $7F
        db   $9D, $0F, $C7, $7F
        db   $00

    """, 0x7F00), fill_nop=True)
