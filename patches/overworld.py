from assembler import ASM
from roomEditor import RoomEditor
import os


def patchOverworldTilesets(rom):
    rom.patch(0x00, 0x0D5B, 0x0D79, ASM("""
        ; Instead of loading tileset info from a small 8x8 table, load it from a 16x16 table to give
        ; full control.
        ; A=MapRoom
        ld   hl, $2100
        ld   [hl], $3F
        ld   d, $00
        ld   e, a
        ld   hl, $6F00
        add  hl, de
        ldh  a, [$94] ; We need to load the currently loaded tileset in E to compare it
        ld   e, a
        ld   a, [hl]
        ld   hl, $2100
        ld   [hl], $20
    """), fill_nop=True)
    # Remove the camera shop exception
    rom.patch(0x00, 0x0D80, 0x0D8B, "", fill_nop=True)

    for x in range(16):
        for y in range(16):
            rom.banks[0x3F][0x2F00+x+y*16] = rom.banks[0x20][0x2E73 + (x // 2) + (y // 2) * 8]
    rom.banks[0x3F][0x2F07] = rom.banks[0x3F][0x2F08] # Fix the room next to the egg
    # Fix the rooms around the camera shop
    rom.banks[0x3F][0x2F26] = 0x0F
    rom.banks[0x3F][0x2F27] = 0x0F
    rom.banks[0x3F][0x2F36] = 0x0F


def createDungeonOnlyOverworld(rom):
    # Start with clearing all the maps, because this just generates a bunch of room in the rom.
    for n in range(0x100):
        re = RoomEditor(rom, n)
        re.entities = []
        re.objects = []
        if os.path.exists("patches/overworld/%02X.json" % (n)):
            re.loadFromJson("patches/overworld/%02X.json" % (n))
        re.updateOverlay()
        re.store(rom)
