from assembler import ASM
from backgroundEditor import BackgroundEditor

def advancedInventorySubscreen(rom):
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
    rom.patch(0x20, 0x3E08+0x32, None, "9DAA08464646464646464646" "9DCA08B0B0B0B0B0B0B0B0B0" "00")

    # instead of doing an GBC specific check, jump to our custom handling
    rom.patch(0x20, 0x19DE, ASM("ldh a, [$FE]\nand a\njr z, $40"), ASM("call $7F00"), fill_nop=True)

    rom.patch(0x20, 0x3F00, 0x4000, ASM("""
        ld   a, [$DBA5] ; isIndoor
        and  a
        jr   z, RenderKeysCounts
        ldh  a, [$F7]   ; mapNr
        cp   $FF
        jr   z, RenderDungeonFix
        cp   $06
        jr   z, D7RenderDungeonFix
        cp   $0A
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
