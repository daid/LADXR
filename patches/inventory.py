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
    rom.patch(0x20, 0x1a83, ASM("ld a, [$DB0F]"), ASM("ld a, [$DB41]"))

    # Remove the gap in the inventory slots
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

    rom.patch(0x20, 0x1C84,
        "9C019C069C619C659CC19CC59D219D25",
        "28283838484858586868787888889898")
    rom.patch(0x20, 0x22b3, ASM("ld hl, $6298"), ASM("ld hl, $5C84"))
    rom.patch(0x20, 0x2298, "28284040", "08280828")

    rom.patch(0x20, 0x1F33, ASM("ld a, $09"), ASM("ld a, $0D"))
    rom.patch(0x20, 0x1F54, ASM("ld a, $09"), ASM("ld a, $0D"))
    rom.patch(0x20, 0x1F2A, ASM("cp $0A"), ASM("cp $0E"))
    rom.patch(0x20, 0x1F4B, ASM("cp $0A"), ASM("cp $0E"))
    rom.patch(0x02, 0x217E, ASM("ld a, $0B"), ASM("ld a, $0F"))


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
