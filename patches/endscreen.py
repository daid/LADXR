from assembler import ASM
from utils import formatText
import os


def updateWindfish(rom):
    tiles = open("GDQHotfix.tiles", "rb").read()
    # There are two types of tiles, windfish graphics and cloud graphics, make sure we only write on top of the windfish
    rom.banks[0x33][0x1050:0x10F0] = tiles[0x0000:0x00A0]
    rom.banks[0x33][0x1130:0x1200] = tiles[0x00A0:0x0170]
    rom.banks[0x33][0x1220:0x1300] = tiles[0x0170:0x0250]
    rom.banks[0x33][0x1310:0x1400] = tiles[0x0250:0x0340]
    rom.banks[0x33][0x1400:0x15A0] = tiles[0x0340:0x04E0]
    rom.banks[0x33][0x15B0:0x15B0+len(tiles)-0x04E0] = tiles[0x04E0:]

    tilemap = open("GDQHotfix.map", "rb").read()
    offset = 0x0EEF
    for y in range(10):
        offset += 3
        for x in range(20):
            tile = tilemap[(x + y * 20) * 2]
            tile += 5
            if tile >= 0x0F: tile += 4
            if tile >= 0x20: tile += 2
            if tile >= 0x30: tile += 1
            if tile >= 0x5A: tile += 1
            rom.banks[0x17][offset] = tile

            attr = tilemap[(x + y * 20) * 2 + 1]
            rom.banks[0x17][offset + 0x0FDF - 0x0EEF] = attr + 2

            offset += 1
            
        offset += 1

    palette = open("GDQHotfix.pal", "rb").read()
    for n in range(8):
        for m in range(0, len(palette), 2):
            p = (palette[m] | palette[m + 1] << 8)
            r = p & 0x1F
            g = (p >> 5) & 0x1F
            b = (p >> 10) & 0x1F
            r = r * (8 - n) // 8
            g = g * (8 - n) // 8
            b = b * (8 - n) // 8
            p = r | (g << 5) | (b << 10)
            
            rom.banks[0x17][0x11B7+n*64+m+0] = p & 0xFF
            rom.banks[0x17][0x11B7+n*64+m+1] = (p >> 8) & 0xFF

    rom.texts[0xCE] = formatText(b"""Hoot! Young lad, I mean... #####, the hero! You have defeated the Nightmares! You have proven your wisdom, courage and power!
... ... ... ...
As part of the  Wind Fish's spirit, I am the guardian of his dream world...
But one day, the Nightmares entered the dream and began wreaking havoc. Then you, #####, came to rescue the island...
I have always trusted in your courage to turn back the Nightmares.
Thank you, #####...
My work is done...
GDQ will awake soon.
Good bye...Hoot!""")
    rom.texts[0xCF] = rom.texts[0xCE]
    rom.texts[0xD0] = formatText(b"""... ... ... ...
... ... ... ...
I AM THE GDQ HOTFIX...
LONG HAS BEEN MY SLUMBER...
IN MY DREAMS...
SPEEDRUNNERS WERE GOING FAST, RACES WERE DONE
... ... ... ...
BUT, IT BE THE NATURE OF RACES TO END!
SO NOW, LET US END THIS RACE...
ONLY THE MEMORY OF THE SPEEDRUN WILL EXIST...
AS WELL AS THE RECORDINGS ON TWITCH AND YOUTUBE
SO DO NOT FORGET TO SUBSCRIBE...
... ... ... ...
ALSO JOIN THE LINKS AWAKENING RANDOMIZER COMMUNITY ON DISCORD SEE LADXR.DAID.EU
... ... ... ...
COME, #####...
LET US GO FAST TOGETHER!!""", center=True)


def updateEndScreen(rom):
    updateWindfish(rom)

    # Call our custom data loader in bank 3F
    rom.patch(0x00, 0x391D, ASM("""
        ld   a, $20
        ld   [$2100], a
        jp   $7de6
    """), ASM("""
        ld   a, $3F
        ld   [$2100], a
        jp   $4100
    """))
    rom.patch(0x17, 0x2FCE, "B170", "D070") # Ignore the final tile data load
    
    rom.patch(0x3F, 0x0100, None, ASM("""
    ; Disable LCD
    xor a
    ldh  [$40], a
    
    ld  hl, $8000
    ld  de, $5000
copyLoop:
    ld  a, [de]
    inc de
    ldi [hl], a
    bit 4, h
    jr  z, copyLoop

    ld  a, $01
    ldh [$4F], a

    ld  hl, $8000
    ld  de, $6000
copyLoop2:
    ld  a, [de]
    inc de
    ldi [hl], a
    bit 4, h
    jr  z, copyLoop2

    ld  hl, $9800
    ld  de, $0190
clearLoop1:
    xor a
    ldi [hl], a
    dec de
    ld  a, d
    or  e
    jr  nz, clearLoop1

    ld  de, $0190
clearLoop2:
    ld  a, $08
    ldi [hl], a
    dec de
    ld  a, d
    or  e
    jr  nz, clearLoop2

    xor  a
    ldh  [$4F], a


    ld  hl, $9800
    ld  de, $000C
    xor  a
loadLoop1:
    ldi  [hl], a
    ld   b, a
    ld   a, l
    and  $1F
    cp   $14
    jr   c, .noLineSkip
    add  hl, de
.noLineSkip:
    ld   a, b
    inc  a
    jr   nz, loadLoop1

loadLoop2:
    ldi  [hl], a
    ld   b, a
    ld   a, l
    and  $1F
    cp   $14
    jr   c, .noLineSkip
    add  hl, de
.noLineSkip:
    ld   a, b
    inc  a
    jr   nz, loadLoop2

    ; Load palette
    ld   hl, $DC10
    ld   a, $00
    ldi  [hl], a
    ld   a, $00
    ldi  [hl], a

    ld   a, $ad
    ldi  [hl], a
    ld   a, $35
    ldi  [hl], a

    ld   a, $94
    ldi  [hl], a
    ld   a, $52
    ldi  [hl], a

    ld   a, $FF
    ldi  [hl], a
    ld   a, $7F
    ldi  [hl], a

    ld   a, $00
    ld   [$DDD3], a
    ld   a, $04
    ld   [$DDD4], a
    ld   a, $81
    ld   [$DDD1], a

    ; Enable LCD
    ld  a, $91
    ldh [$40], a
    ld  [$d6fd], a
    
    xor a
    ldh [$96], a
    ldh [$97], a
    ret
    """))
    
    addr = 0x1000
    for c in open(os.path.join(os.path.dirname(__file__), "thanks.bin"), "rb").read():
        rom.banks[0x3F][addr] = c
        addr += 1
