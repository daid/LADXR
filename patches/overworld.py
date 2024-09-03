from assembler import ASM
from roomEditor import RoomEditor, ObjectWarp, Object, WARP_TYPE_IDS
import entityData
import os
import json


def patchOverworldTilesets(rom):
    rom.patch(0x00, 0x0D5B, 0x0D79, ASM("""
        ; Instead of loading tileset info from a small 8x8 table, load it from a 16x16 table to give
        ; full control.
        ; A=MapRoom
        ld   hl, $2100
        ld   [hl], $3F
        ld   d, $00
        ld   e, a
        ld   hl, $7F00
        add  hl, de
        ldh  a, [$FF94] ; We need to load the currently loaded tileset in E to compare it
        ld   e, a
        ld   a, [hl]
        ld   hl, $2100
        ld   [hl], $20
    """), fill_nop=True)
    # Remove the camera shop exception
    rom.patch(0x00, 0x0D80, 0x0D8B, "", fill_nop=True)

    for x in range(16):
        for y in range(16):
            rom.banks[0x3F][0x3F00+x+y*16] = rom.banks[0x20][0x2E73 + (x // 2) + (y // 2) * 8]
    rom.banks[0x3F][0x3F07] = rom.banks[0x3F][0x3F08]  # Fix the room next to the egg
    rom.banks[0x3F][0x3F17] = rom.banks[0x3F][0x3F08]  # Fix the room next to the egg
    rom.banks[0x3F][0x3F3A] = 0x0F  # room below mambo cave
    rom.banks[0x3F][0x3F3B] = 0x0F  # room below D4
    rom.banks[0x3F][0x3F4B] = 0x0F  # room next to castle
    rom.banks[0x3F][0x3F5B] = 0x0F  # room next to castle
    # Fix the rooms around the camera shop
    rom.banks[0x3F][0x3F26] = 0x0F
    rom.banks[0x3F][0x3F27] = 0x0F
    rom.banks[0x3F][0x3F36] = 0x0F


def createDungeonOnlyOverworld(rom):
    # Skip the whole egg maze.
    rom.patch(0x14, 0x0453, "75", "73")

    instrument_rooms = [0x102, 0x12A, 0x159, 0x162, 0x182, 0x1B5, 0x22C, 0x230, 0x301]
    path = os.path.dirname(__file__)

    # Start with clearing all the maps, because this just generates a bunch of room in the rom.
    for n in range(0x100):
        re = RoomEditor(rom, n)
        re.entities = []
        re.objects = []
        if os.path.exists("%s/overworld/dive/%02X.json" % (path, n)):
            re.loadFromJson("%s/overworld/dive/%02X.json" % (path, n))
        entrances = list(filter(lambda obj: obj.type_id in WARP_TYPE_IDS, re.objects))
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
                    # Patch the boomerang guy exit
                    other = RoomEditor(rom, "Alt1F5")
                    other.getWarps()[0].room = n
                    other.getWarps()[0].target_x = e.x * 16 + 8
                    other.getWarps()[0].target_y = e.y * 16 + 16
                    other.store(rom)

                if obj.warp_type == 1 and (obj.map_nr < 8 or obj.map_nr == 0xFF) and obj.room not in (0x1B0, 0x23A, 0x23D):
                    other = RoomEditor(rom, instrument_rooms[min(8, obj.map_nr)])
                    for o in other.objects:
                        if isinstance(o, ObjectWarp) and o.warp_type == 0:
                            o.room = n
                            o.target_x = e.x * 16 + 8
                            o.target_y = e.y * 16 + 16
                    other.store(rom)
        re.store(rom)


def exportOverworld(rom, also_underworld=False):
    import PIL.Image

    path = os.path.dirname(__file__)
    for room_index in list(range(0x316 if also_underworld else 0x100)) + ["Alt06", "Alt0E", "Alt1B", "Alt2B", "Alt79", "Alt8C"]:
        if room_index == 0x2FF:
            continue
        room = RoomEditor(rom, room_index)
        if isinstance(room_index, int):
            room_nr = room_index
        else:
            room_nr = int(room_index[3:], 16)
        map_id = None  # TODO set map for indoor rooms
        if room_nr >= 0x300:
            map_id = 0xFF
        if room_nr < 0x100:
            tileset_index = rom.banks[0x3F][0x3F00 + room_nr]
            attributedata_bank = rom.banks[0x1A][0x2476 + room_nr]
            attributedata_addr = rom.banks[0x1A][0x1E76 + room_nr * 2]
            attributedata_addr |= rom.banks[0x1A][0x1E76 + room_nr * 2 + 1] << 8

            metatile_info = rom.banks[0x1A][0x2B1D:0x2B1D + 0x400]

            palette_index = rom.banks[0x21][0x02EF + room_nr]
            palette_addr = rom.banks[0x21][0x02B1 + palette_index * 2]
            palette_addr |= rom.banks[0x21][0x02B1 + palette_index * 2 + 1] << 8
        else:
            tileset_index = rom.banks[0x20][0x2EB3 + room_nr - 0x100]
            attributedata_bank = 0x23 if room_nr < 0x200 else 0x24
            if map_id is None:
                attributedata_addr = rom.banks[0x1A][0x1E76 + room_nr * 2]
                attributedata_addr |= rom.banks[0x1A][0x1E76 + room_nr * 2 + 1] << 8
            elif map_id == 6 or map_id == 7:
                attributedata_bank = 0x23
                attributedata_addr = rom.banks[0x1A][0x1E76 + 0x100 + map_id * 2]
                attributedata_addr |= rom.banks[0x1A][0x1E76 + 0x100 + map_id * 2 + 1] << 8
            else:
                attributedata_addr = rom.banks[0x1A][0x1E76 + (room_nr & 0xF00) * 2 + map_id * 2]
                attributedata_addr |= rom.banks[0x1A][0x1E76 + (room_nr & 0xF00) * 2 + map_id * 2 + 1] << 8

            metatile_info = rom.banks[0x08][0x03B0:0x03B0+0x400]

            if map_id is not None:
                if map_id < 9:
                    palette_addr = rom.banks[0x21][0x03EF + map_id*2] | (rom.banks[0x21][0x03F0 + map_id*2] << 8)
                elif map_id == 0xFF:
                    palette_addr = 0x67D0
                else:
                    lookup_addr = rom.banks[0x21][0x0413 + (map_id - 10)*2] | (rom.banks[0x21][0x0414 + (map_id - 10)*2] << 8)
                    index = rom.banks[0x21][lookup_addr - 0x4000 + (room_nr & 0xFF)] * 2
                    palette_addr = rom.banks[0x21][0x043F + index] | (rom.banks[0x21][0x0440 + index] << 8)
            else:
                palette_addr = rom.banks[0x21][0x02B1] | (rom.banks[0x21][0x02B2] << 8)

        assert attributedata_addr >= 0x4000, f"{attributedata_addr:04x} {room_nr:03x}"
        attributedata_addr -= 0x4000
        attrtile_info = rom.banks[attributedata_bank][attributedata_addr:attributedata_addr+0x400]
        palette_addr -= 0x4000

        hidden_warp_tiles = []
        for obj in room.objects:
            if obj.type_id in WARP_TYPE_IDS and room.overlay and room.overlay[obj.x + obj.y * 10] != obj.type_id:
                if obj.type_id != 0xE1 or room.overlay[obj.x + obj.y * 10] != 0x53: # Ignore the waterfall 'caves'
                    hidden_warp_tiles.append(obj)
            if obj.type_id == 0xC5 and room_nr < 0x100 and room.overlay[obj.x + obj.y * 10] == 0xC4:
                # Pushable gravestones have the wrong overlay by default
                room.overlay[obj.x + obj.y * 10] = 0xC5
            if obj.type_id == 0xDC and room_nr < 0x100:
                # Flowers above the rooster windmill need a different tile
                hidden_warp_tiles.append(obj)

        image_filename = "tiles_%02x_%02x_%02x_%02x_%04x.png" % (tileset_index, room.animation_id, palette_index, attributedata_bank, attributedata_addr)
        if room_nr >= 0x100:
            image_filename = f"indoor_{image_filename}"
        data = {
            "width": 10, "height": 8,
            "type": "map", "renderorder": "right-down", "tiledversion": "1.4.3", "version": 1.4,
            "tilewidth": 16, "tileheight": 16, "orientation": "orthogonal",
            "tilesets": [
                {
                    "columns": 16, "firstgid": 1,
                    "image": image_filename, "imageheight": 256, "imagewidth": 256,
                    "margin": 0, "name": "main", "spacing": 0,
                    "tilecount": 256, "tileheight": 16, "tilewidth": 16
                }
            ],
            "layers": [{
                "data": [n+1 for n in (room.overlay if room.overlay else room.getTileArray())],
                "width": 10, "height": 8,
                "id": 1, "name": "Tiles", "type": "tilelayer", "visible": True, "opacity": 1, "x": 0, "y": 0,
            }, {
                "id": 2, "name": "EntityLayer", "type": "objectgroup", "visible": True, "opacity": 1, "x": 0, "y": 0,
                "objects": [
                    {"width": 16, "height": 16, "x": entity[0] * 16, "y": entity[1] * 16, "name": entityData.NAME[entity[2]], "type": "entity"} for entity in room.entities
                ] + [
                    {"width": 8, "height": 8, "x": 0, "y": idx * 8, "name": "%x:%02x:%03x:%02x:%02x" % (obj.warp_type, obj.map_nr, obj.room, obj.target_x, obj.target_y), "type": "warp"} for idx, obj in enumerate(room.getWarps()) if isinstance(obj, ObjectWarp)
                ] + [
                    {"width": 16, "height": 16, "x": obj.x * 16, "y": obj.y * 16, "name": "%02X" % (obj.type_id), "type": "hidden_tile"} for obj in hidden_warp_tiles
                ],
            }],
            "properties": [
                {"name": "tileset", "type": "string", "value": "%02X" % (tileset_index)},
                {"name": "animationset", "type": "string", "value": "%02X" % (room.animation_id)},
                {"name": "attribset", "type": "string", "value": "%02X:%04X" % (attributedata_bank, attributedata_addr)},
                {"name": "palette", "type": "string", "value": "%02X" % (palette_index)},
            ]
        }
        if isinstance(room_index, str):
            json.dump(data, open("%s/overworld/export/%s.json" % (path, room_index), "wt"))
        else:
            json.dump(data, open("%s/overworld/export/%03X.json" % (path, room_index), "wt"))

        if not os.path.exists("%s/overworld/export/%s" % (path, image_filename)):
            print(f"Creating {image_filename}")
            if room_nr < 0x100:
                if tileset_index == 0x0F:
                    tilemap = bytearray([0x00, 0x55, 0xAA, 0x00] * 4 * 32)
                else:
                    tilemap = rom.banks[0x2F][tileset_index*0x100:tileset_index*0x100+0x200]
                tilemap += rom.banks[0x2C][0x1200:0x1800]
                tilemap += rom.banks[0x2C][0x0800:0x1000]
            else:
                tilemap = bytearray([0x00, 0x55, 0xAA, 0x00] * 4 * 256)
                tilemap[0x200:0x800] = rom.banks[0x2D][0x000:0x600]
                if tileset_index != 0xFF:
                    tilemap[0x000:0x100] = rom.banks[0x2D][0x1000 + tileset_index * 0x100:0x1100 + tileset_index * 0x100]
                tilemap[0x100:0x200] = rom.banks[0x2D][0x2000:0x2100]
                tilemap[0xF00:0x1000] = rom.banks[0x32][0x3800:0x3900]

            anim_addr = {2: 0x2B00, 3: 0x2C00, 4: 0x2D00, 5: 0x2E00, 6: 0x2F00, 7: 0x2D00, 8: 0x3000, 9: 0x3100, 10: 0x3200, 11: 0x2A00, 12: 0x3300, 13: 0x3500, 14: 0x3600, 15: 0x3400, 16: 0x3700}.get(room.animation_id, 0x0000)
            tilemap[0x6C0:0x700] = rom.banks[0x2C][anim_addr:anim_addr + 0x40]

            palette = []
            for n in range(8*4):
                p0 = rom.banks[0x21][palette_addr]
                p1 = rom.banks[0x21][palette_addr + 1]
                pal = p0 | p1 << 8
                palette_addr += 2
                r = (pal & 0x1F) << 3
                g = ((pal >> 5) & 0x1F) << 3
                b = ((pal >> 10) & 0x1F) << 3
                palette += [r, g, b]

            img = PIL.Image.new("P", (16*16, 16*16))
            img.putpalette(palette)
            def drawTile(x, y, index, attr):
                for py in range(8):
                    a = tilemap[index * 16 + py * 2]
                    b = tilemap[index * 16 + py * 2 + 1]
                    if attr & 0x40:
                        a = tilemap[index * 16 + 14 - py * 2]
                        b = tilemap[index * 16 + 15 - py * 2]
                    for px in range(8):
                        bit = 0x80 >> px
                        if attr & 0x20:
                            bit = 0x01 << px
                        c = (attr & 7) << 2
                        if a & bit:
                            c |= 1
                        if b & bit:
                            c |= 2
                        img.putpixel((x+px, y+py), c)
            for x in range(16):
                for y in range(16):
                    idx = x+y*16
                    metatiles = metatile_info[idx*4:idx*4+4]
                    attrtiles = attrtile_info[idx*4:idx*4+4]
                    drawTile(x * 16 + 0, y * 16 + 0, metatiles[0], attrtiles[0])
                    drawTile(x * 16 + 8, y * 16 + 0, metatiles[1], attrtiles[1])
                    drawTile(x * 16 + 0, y * 16 + 8, metatiles[2], attrtiles[2])
                    drawTile(x * 16 + 8, y * 16 + 8, metatiles[3], attrtiles[3])
            img.save("%s/overworld/export/%s" % (path, image_filename))

    world = {
        "maps": [
            {"fileName": "%03X.json" % (n), "height": 128, "width": 160, "x": (n & 0x0F) * 160, "y": (n >> 4) * 128}
            for n in range(0x100)
        ],
        "onlyShowAdjacentMaps": False,
        "type": "world"
    }
    json.dump(world, open("%s/overworld/export/overworld.world" % (path), "wt"))
    if also_underworld:
        world = {
            "maps": [{"fileName": "%03X.json" % (n+0x100), "height": 128, "width": 160, "x": (n & 0x0F) * 160, "y": (n >> 4) * 128} for n in range(0x100)],
            "onlyShowAdjacentMaps": False,
            "type": "world"
        }
        json.dump(world, open("%s/overworld/export/underworld_1.world" % (path), "wt"))
        world = {
            "maps": [{"fileName": "%03X.json" % (n+0x200), "height": 128, "width": 160, "x": (n & 0x0F) * 160, "y": (n >> 4) * 128} for n in range(0xFF)],
            "onlyShowAdjacentMaps": False,
            "type": "world"
        }
        json.dump(world, open("%s/overworld/export/underworld_2.world" % (path), "wt"))
        for map_index in range(8):
            rooms = []
            for y in range(8):
                for x in range(8):
                    addr = 0x0220 + map_index * 8 * 8
                    room_nr = rom.banks[0x14][addr+x+y*8] + 0x100
                    if map_index > 5:
                        room_nr += 0x100
                    if map_index == 11:
                        room_nr += 0x100
                    if (room_nr & 0xFF) != 0:
                        rooms.append({"fileName": "%03X.json" % (room_nr), "height": 128, "width": 160, "x": x * 160, "y": y * 128})
            world = {
                "maps": rooms,
                "onlyShowAdjacentMaps": False,
                "type": "world"
            }
            json.dump(world, open("%s/overworld/export/map_%02x.world" % (path, map_index), "wt"))


def isNormalOverworld(rom):
    return len(RoomEditor(rom, 0x010).getWarps()) > 0
