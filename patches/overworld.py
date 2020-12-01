from assembler import ASM
from roomEditor import RoomEditor, ObjectWarp, Object
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
    # Skip the whole egg maze.
    rom.patch(0x14, 0x0453, "75", "73")

    # Some sprite patches (should generalize this)
    rom.room_sprite_data_overworld[0x72] = b'\xff\xff\xff\xff'
    rom.room_sprite_data_overworld[0x73] = rom.room_sprite_data_overworld[0x8C]
    rom.room_sprite_data_overworld[0xB1] = rom.room_sprite_data_overworld[0x92]

    instrument_rooms = [0x102, 0x12A, 0x159, 0x162, 0x182, 0x1B5, 0x22C, 0x230, 0x301]

    # Start with clearing all the maps, because this just generates a bunch of room in the rom.
    for n in range(0x100):
        re = RoomEditor(rom, n)
        re.entities = []
        re.objects = []
        if os.path.exists("patches/overworld/%02X.json" % (n)):
            re.loadFromJson("patches/overworld/%02X.json" % (n))
        re.updateOverlay()
        entrances = list(filter(lambda obj: obj.type_id in (0xE1, 0xE2, 0xE3, 0xBA, 0xA8, 0xBE, 0xCB), re.objects))
        for obj in re.objects:
            if isinstance(obj, ObjectWarp) and entrances:
                e = entrances.pop(0)

                other = RoomEditor(rom, obj.room)
                for o in other.objects:
                    if isinstance(o, ObjectWarp) and o.warp_type == 0:
                        o.room = n
                        o.target_x = e.x * 16 + 8
                        o.target_y = e.y * 16 + 16
                other.store(rom)

                if obj.room == 0x1F5:
                    # Patch the boomang guy exit
                    rom.patch(0x0a, 0x3891, "E000F41820", "E000%02x%02x%02x" % (n, e.x * 16 + 8, e.y * 16 + 16))

                if obj.warp_type == 1 and obj.map_nr < 8 or obj.map_nr == 0xFF:
                    other = RoomEditor(rom, instrument_rooms[min(8, obj.map_nr)])
                    for o in other.objects:
                        if isinstance(o, ObjectWarp) and o.warp_type == 0:
                            o.room = n
                            o.target_x = e.x * 16 + 8
                            o.target_y = e.y * 16 + 16
                    other.store(rom)
        if n == 0x06:
            re.objects.insert(0, Object(5, 3, 0xE1))
        re.store(rom)
