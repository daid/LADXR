import PIL.Image, PIL.ImageDraw
import os
import json
from roomEditor import RoomEditor, ObjectHorizontal, ObjectVertical, ObjectWarp


class Room:
    def __init__(self, n):
        self.n = n
        self.tiles = None
        self.main_tileset_id = None
        self.animation_tileset_id = None
        self.palette_addr = None
        self.attribute_bank = None
        self.attribute_addr = None

    def to_json(self):
        return self.__dict__


class RoomMapInfo:
    def __init__(self):
        self.x = None
        self.y = None
        self.map_id = None
        self.sidescroll = False


class MapExport:
    def __init__(self, rom):
        self.__rom = rom
        self.__tile_cache = {}
        self.__room_map_info = {}
        self.__json_data = {
            "rooms": {},
            "maps": {},
            "attributes": {},
            "overworld_physics_flag": [n for n in self.__rom.banks[8][0x0AD4:0x0AD4+0x100]],
            "indoor1_physics_flag": [n for n in self.__rom.banks[8][0x0BD4:0x0BD4 + 0x100]],
        }
        for n in range(0x316):
            if n == 0x2FF:
                continue
            for warp in RoomEditor(rom, n).getWarps():
                if warp.warp_type > 0:
                    self.room_map_info(warp.room).map_id = warp.map_nr
                if warp.warp_type == 2:
                    self.room_map_info(warp.room).sidescroll = True
        self.room_map_info(0x1FF).sidescroll = True
        self.room_map_info(0x2E8).sidescroll = True

    def export_all(self, w=16, h=16, *, dungeons=True):
        os.makedirs("_map/img", exist_ok=True)
        f = open("_map/test.html", "wt")
        self.buildOverworld(w, h).save("_map/img/overworld.png")
        f.write("<img src='img/overworld.png'><br><br>")

        if dungeons:
            for n in (0,1,2,3,4,5,6,7, 10, 11):
                addr = 0x0220 + n * 8 * 8
                result = PIL.Image.new("RGB", (8 * 161, 8 * 129))
                map_data = {}
                for y in range(8):
                    for x in range(8):
                        room = self.__rom.banks[0x14][addr] + 0x100
                        if n > 5:
                            room += 0x100
                        if n == 11:
                            room += 0x100
                        addr += 1
                        if (room & 0xFF) == 0 and (n != 11 or x != 1 or y != 3):  # ignore room nr 0, except on a very specific spot in the color dungeon.
                            continue
                        map_data[x+y*16] = room
                        self.room_map_info(room).x = x
                        self.room_map_info(room).y = y
                        if self.room_map_info(room).map_id is None:
                            self.room_map_info(room).map_id = n if n < 11 else 0xFF
                        result.paste(self.buildRoom(room), (x * 161, y * 129))
                self.__json_data["maps"][f"dungeon_{n}"] = map_data
                result.save(f"_map/img/dungeon_{n}.png")
                f.write(f"<img src='img/dungeon_{n}.png' map='dungeon_{n}'><br><br>")
            for n in range(1, 3):
                result = PIL.Image.new("RGB", (16 * 161, 16 * 129))
                for y in range(16):
                    for x in range(16):
                        if n != 2 or x != 15 or y != 15:
                            result.paste(self.buildRoom(n << 8 | y << 4 | x), (x * 161, y * 129))
                result.save(f"_map/img/underworld_{n}.png")
                f.write(f"<img src='img/underworld_{n}.png' underworld='{n}'><br><br>")

        f.write("<script>var data = ")
        f.write(json.dumps(self.__json_data))
        f.write("""
function h2(n) { if (n < 16) return "0x0" + n.toString(16); return "0x" + n.toString(16); }
function updateTooltip(e) {
    var map = e.target.getAttribute("map")
    var underworld = e.target.getAttribute("underworld") || 0
    var tooltip = document.getElementById("tooltip");
    tooltip.style.display = 'None';
    var roomx = Math.floor(e.offsetX / 161);
    var roomy = Math.floor(e.offsetY / 129);
    var tilex = Math.floor((e.offsetX - roomx * 161) / 16)
    var tiley = Math.floor((e.offsetY - roomy * 129) / 16)
    if (tilex < 0 || tilex > 9 || tiley < 0 || tiley > 7) return;
    var room = data.rooms[roomx + roomy*16 + underworld*256];
    if (map !== null) {
        var room_id = data.maps[map][roomx + roomy*16];
        if (room_id === undefined) return;
        room = data.rooms[room_id];
    }
    var tile_id = room.tiles[tilex + tiley*10];
    var attributes = data.attributes[(room.attribute_bank << 16) | room.attribute_addr]
    var metatiles = data.overworld_metatiles
    var physics_flag = data.overworld_physics_flag
    if (map !== null) {
        var metatiles = data.indoor1_metatiles
        var physics_flag = data.indoor1_physics_flag
    }

    tooltip.style.left = roomx * 161 + tilex * 16 + e.target.getBoundingClientRect().x - document.body.getBoundingClientRect().x + 24;
    tooltip.style.top = roomy * 129 + tiley * 16 + e.target.getBoundingClientRect().y - document.body.getBoundingClientRect().y + 24;
    tooltip.style.display = ''; 

    tooltip.innerText = `Room ID: ${h2(room.n)}
        Tileset: ${h2(room.main_tileset_id)}
        Palette: ${h2(room.palette_addr)}
        Animation set: ${h2(room.animation_tileset_id)}
        Attribute data: ${h2(room.attribute_bank)}:${h2(room.attribute_addr)}
        
        Tile ID: ${h2(tile_id)}
        Subtiles: ${h2(metatiles[tile_id*4])} ${h2(metatiles[tile_id*4+1])} ${h2(metatiles[tile_id*4+2])} ${h2(metatiles[tile_id*4+3])}
        TileAttr: ${h2(attributes[tile_id*4])} ${h2(attributes[tile_id*4+1])} ${h2(attributes[tile_id*4+2])} ${h2(attributes[tile_id*4+3])}
        Physics: ${h2(physics_flag[tile_id])}
    `
    for(var ent of room.entities) {
        if (ent.x == tilex && ent.y == tiley) {
            tooltip.innerText += `
Entity: ${h2(ent.type)}
`
        }
    }
    for(var warp of room.warps) {
        if (warp.x == tilex && warp.y == tiley) {
            tooltip.innerText += `
Warp to:
Map: ${h2(warp.map)} Room: ${h2(warp.room)}
Target: ${h2(warp.target_x)} ${h2(warp.target_y)}
`
        }
    }
}
for(var e of document.getElementsByTagName("img")) {
    e.onmousemove = updateTooltip
    e.onmouseleave = function() { document.getElementById("tooltip").style.display = 'None'; }
}
        """)
        f.write("</script><div id='tooltip' style='position:absolute; background-color: white; padding: 4px; border: solid black 1px; white-space: nowrap'>X</div><div style='height:300px'></div>")

    def getOverworldTileset(self, main_tileset, animation_id):
        subtiles = [0] * 0x100
        for n in range(0, 0x20):
            subtiles[n] = (0x2F << 10) + (main_tileset << 4) + n
        for n in range(0x20, 0x80):
            subtiles[n] = (0x2C << 10) + 0x100 + n
        for n in range(0x80, 0x100):
            subtiles[n] = (0x2C << 10) + n

        addr = (0x000, 0x000, 0x2B0, 0x2C0, 0x2D0, 0x2E0, 0x2F0, 0x2D0, 0x300, 0x310, 0x320, 0x2A0, 0x330, 0x350, 0x360, 0x340, 0x370)[animation_id]
        for n in range(0x6C, 0x70):
            subtiles[n] = (0x2C << 10) + addr + n - 0x6C
        return subtiles

    def getIndoorTileset(self, room_id, main_tileset, animation_id):
        rmi = self.room_map_info(room_id)

        subtiles = [0] * 0x100
        for n in range(0x20, 0x80):
            subtiles[n] = (0x2D << 10) + n - 0x20
        if main_tileset != 0xFF:
            for n in range(0x00, 0x10):
                subtiles[n] = (0x2D << 10) + 0x100 + main_tileset * 0x10+n
        for n in range(0x10, 0x20):
            subtiles[n] = (0x2D << 10) + 0x200 + n
        for n in range(0xF0, 0x100):
            subtiles[n] = (0x32 << 10) + 0x380 + n - 0xF0

        if rmi.map_id is not None:
            if rmi.sidescroll:
                for n in range(0x00, 0x80):
                    subtiles[n] = (0x2D << 10) + n + 0x300
            else:
                wall_tiles_ptr = (self.__rom.banks[0x20][0x05A9 + rmi.map_id] - 0x40) << 4
                if rmi.map_id == 0xFF:
                    wall_tiles_ptr = (0x4A - 0x40) << 4
                for n in range(0x20, 0x40):
                    subtiles[n] = (0x2D << 10) + n - 0x20 + wall_tiles_ptr

                floor_tiles_ptr = (self.__rom.banks[0x20][0x0589 + rmi.map_id] - 0x40) << 4
                for n in range(0x10, 0x20):
                    subtiles[n] = (0x2D << 10) + n - 0x10 + floor_tiles_ptr

        addr = (0x000, 0x000, 0x2B0, 0x2C0, 0x2D0, 0x2E0, 0x2F0, 0x2D0, 0x300, 0x310, 0x320, 0x2A0, 0x330, 0x350, 0x360, 0x340, 0x370)[animation_id]
        for n in range(0x6C, 0x70):
            subtiles[n] = (0x2C << 10) + addr + n - 0x6C

        return subtiles

    def getPalette(self, palette_addr):
        palette_addr -= 0x4000

        palette = []
        for n in range(8*4):
            p0 = self.__rom.banks[0x21][palette_addr]
            p1 = self.__rom.banks[0x21][palette_addr + 1]
            pal = p0 | p1 << 8
            palette_addr += 2
            r = (pal & 0x1F) << 3
            g = ((pal >> 5) & 0x1F) << 3
            b = ((pal >> 10) & 0x1F) << 3
            palette.append((r, g, b))
        return palette

    def buildOverworld(self, w, h):
        result = PIL.Image.new("RGB", (w * (20 * 8 + 1), h * (16 * 8 + 1)))
        for y in range(h):
            for x in range(w):
                result.paste(self.buildRoom(x + y * 16), (x * (20 * 8 + 1), y * (16 * 8 + 1)))
        return result

    def buildRoom(self, room_id):
        map_id = self.room_map_info(room_id).map_id
        re = RoomEditor(self.__rom, room_id)

        room = Room(room_id)
        if room_id < 0x100:
            room.main_tileset_id = self.__rom.banks[0x20][0x2E73 + (room_id & 0x0F) // 2 + ((room_id >> 5) * 8)]
            if self.__rom.banks[0x3F][0x3F00 + room_id]:  # If we have the the per room tileset patch, use that data
                room.main_tileset_id = self.__rom.banks[0x3F][0x3F00 + room_id]
        else:
            room.main_tileset_id = self.__rom.banks[0x20][0x2eB3 + room_id - 0x100]
        room.animation_tileset_id = re.animation_id
        room.tiles = re.getTileArray()

        if room_id < 0x100:
            room.attribute_bank = self.__rom.banks[0x1A][0x2476 + room_id]
        elif room_id < 0x200:
            room.attribute_bank = 0x23
        else:
            room.attribute_bank = 0x24
        if map_id is None:
            room.attribute_addr = self.__rom.banks[0x1A][0x1E76 + room_id * 2]
            room.attribute_addr |= self.__rom.banks[0x1A][0x1E76 + room_id * 2 + 1] << 8
        elif map_id == 6 or map_id == 7:
            room.attribute_bank = 0x23
            room.attribute_addr = self.__rom.banks[0x1A][0x1E76 + 0x100 + map_id * 2]
            room.attribute_addr |= self.__rom.banks[0x1A][0x1E76 + 0x100 + map_id * 2 + 1] << 8
        else:
            room.attribute_addr = self.__rom.banks[0x1A][0x1E76 + (room_id & 0xF00) * 2 + map_id * 2]
            room.attribute_addr |= self.__rom.banks[0x1A][0x1E76 + (room_id & 0xF00) * 2 + map_id * 2 + 1] << 8

        if room_id < 0x100:
            index = self.__rom.banks[0x21][0x02EF + room_id] * 2
            room.palette_addr = self.__rom.banks[0x21][0x02B1 + index] | (self.__rom.banks[0x21][0x02B2 + index] << 8)
        elif map_id is not None:
            if map_id < 9:
                room.palette_addr = self.__rom.banks[0x21][0x03EF + map_id*2] | (self.__rom.banks[0x21][0x03F0 + map_id*2] << 8)
            elif map_id == 0xFF:
                room.palette_addr = 0x67D0
            else:
                lookup_addr = self.__rom.banks[0x21][0x0413 + (map_id - 10)*2] | (self.__rom.banks[0x21][0x0414 + (map_id - 10)*2] << 8)
                index = self.__rom.banks[0x21][lookup_addr - 0x4000 + (room_id & 0xFF)] * 2
                room.palette_addr = self.__rom.banks[0x21][0x043F + index] | (self.__rom.banks[0x21][0x0440 + index] << 8)
        else:
            room.palette_addr = self.__rom.banks[0x21][0x02B1] | (self.__rom.banks[0x21][0x02B2] << 8)

        self.__json_data["rooms"][room_id] = room.to_json()
        self.__json_data["rooms"][room_id]["entities"] = [{"x": x, "y": y, "type": type_id} for x, y, type_id in re.entities]
        self.__json_data["rooms"][room_id]["warps"] = []
        warp_tiles = [idx for idx, tile_id in enumerate(room.tiles) if tile_id in {0xE1, 0xE2, 0xE3, 0xC6, 0xBA}]
        for idx, obj in enumerate(obj for obj in re.objects if isinstance(obj, ObjectWarp)):
            warp_tile = warp_tiles[idx] if idx < len(warp_tiles) else 0
            self.__json_data["rooms"][room_id]["warps"].append({
                "x": warp_tile % 10,
                "y": warp_tile // 10,
                "type": obj.warp_type,
                "room": obj.room,
                "map": obj.map_nr,
                "target_x": obj.target_x,
                "target_y": obj.target_y,
            })

        # Draw the room
        if room_id < 0x100:
            tileset = self.getOverworldTileset(room.main_tileset_id, room.animation_tileset_id)
            metatiles = self.__rom.banks[0x1A][0x2B1D:0x2B1D+0x400]
            if "overworld_metatiles" not in self.__json_data:
                self.__json_data["overworld_metatiles"] = [n for n in metatiles]
        else:
            tileset = self.getIndoorTileset(room_id, room.main_tileset_id, room.animation_tileset_id)
            metatiles = self.__rom.banks[0x08][0x03B0:0x03B0+0x400]
            if "indoor1_metatiles" not in self.__json_data:
                self.__json_data["indoor1_metatiles"] = [n for n in metatiles]
            if 0xDB in room.tiles or 0xDC in room.tiles: # We have switch block tiles, so we need to update the tiles for those
                for n in range(4):
                    tileset[4 + n] = (0x0C << 10) + 0x280 + n
                    tileset[8 + n] = (0x0C << 10) + 0x288 + n
        attributes = self.__rom.banks[room.attribute_bank][room.attribute_addr-0x4000:room.attribute_addr-0x4000+0x400]
        if (room.attribute_bank << 16) | room.attribute_addr not in self.__json_data["attributes"]:
            self.__json_data["attributes"][(room.attribute_bank << 16) | room.attribute_addr] = [n for n in attributes]
        result = PIL.Image.new('RGB', (8 * 20, 8 * 16))
        draw = PIL.ImageDraw.Draw(result)
        for y in range(8):
            for x in range(10):
                tile_nr = room.tiles[x + y * 10]
                metatile = metatiles[tile_nr*4:tile_nr*4+4]
                attrtile = attributes[tile_nr*4:tile_nr*4+4]
                self.drawSubtile(result, x*16, y*16, tileset[metatile[0]], attrtile[0], room.palette_addr)
                self.drawSubtile(result, x*16+8, y*16, tileset[metatile[1]], attrtile[1], room.palette_addr)
                self.drawSubtile(result, x*16, y*16+8, tileset[metatile[2]], attrtile[2], room.palette_addr)
                self.drawSubtile(result, x*16+8, y*16+8, tileset[metatile[3]], attrtile[3], room.palette_addr)
        for x, y, type_id in re.entities:
            draw.rectangle([(x * 16, y * 16), (x * 16 + 15, y * 16 + 15)], outline=0)
            draw.text((x * 16 + 2, y * 16 + 1), "%02X" % (type_id))
            draw.text((x * 16 + 4, y * 16 + 1), "%02X" % (type_id))
            draw.text((x * 16 + 2, y * 16 + 3), "%02X" % (type_id))
            draw.text((x * 16 + 4, y * 16 + 3), "%02X" % (type_id))
            draw.text((x * 16 + 3, y * 16 + 2), "%02X" % (type_id), fill=0)
        return result

    def drawSubtile(self, img, ox, oy, subtile_id, attr, palette_addr):
        if (subtile_id, attr, palette_addr) not in self.__tile_cache:
            result = PIL.Image.new("RGB", (8, 8))
            palette = self.getPalette(palette_addr)[(attr&7)*4:(attr&7)*4+4]
            addr = (subtile_id&0x3FF)<<4
            tile_data = self.__rom.banks[subtile_id >> 10][addr:addr+0x10]
            for y in range(8):
                a = tile_data[y * 2]
                b = tile_data[y * 2 + 1]
                if attr & 0x40:
                    a = tile_data[14 - y * 2]
                    b = tile_data[15 - y * 2]
                for x in range(8):
                    v = 0
                    bit = 0x80 >> x
                    if attr & 0x20:
                        bit = 0x01 << x
                    if a & bit:
                        v |= 0x01
                    if b & bit:
                        v |= 0x02
                    result.putpixel((x,y), palette[v])
            self.__tile_cache[(subtile_id, attr, palette_addr)] = result
        img.paste(self.__tile_cache[(subtile_id, attr, palette_addr)], (ox, oy))

    def exportMetaTiles(self, f, name, main_set, animation_set, condition_func):
        condition = lambda n: condition_func(n) and (n < 0x80 or n >= 0xF0)

        metatile_info_offset = self.__rom.banks[0x1A].find(b'\x7C\x7C\x7C\x7C\x7D\x7D\x7D\x7D')
        metatile_info = self.__rom.banks[0x1A][metatile_info_offset:metatile_info_offset + 0x100 * 4]

        result = PIL.Image.new("L", (16 * 16, 16 * 16))

        sub_tileset_offset = main_set * 0x10
        tilemap = self.__tiles[0x0f][sub_tileset_offset:sub_tileset_offset+0x20]
        tilemap += self.__tiles[0x0c][0x120:0x180]
        tilemap += self.__tiles[0x0c][0x080:0x100]
        
        addr = (0x000, 0x000, 0x2B0, 0x2C0, 0x2D0, 0x2E0, 0x2F0, 0x2D0, 0x300, 0x310, 0x320, 0x2A0, 0x330, 0x350, 0x360, 0x340, 0x370)[animation_set]
        tilemap[0x6C:0x70] = self.__tiles[0x0c][addr:addr+4]

        for x in range(16):
            for y in range(16):
                obj = x + y * 16
                if condition(metatile_info[obj*4+0]):
                    result.paste(tilemap[metatile_info[obj*4+0]], (x*16+0, y*16+0))
                if condition(metatile_info[obj*4+1]):
                    result.paste(tilemap[metatile_info[obj*4+1]], (x*16+8, y*16+0))
                if condition(metatile_info[obj*4+2]):
                    result.paste(tilemap[metatile_info[obj*4+2]], (x*16+0, y*16+8))
                if condition(metatile_info[obj*4+3]):
                    result.paste(tilemap[metatile_info[obj*4+3]], (x*16+8, y*16+8))

        result.save(name)
        f.write("%s<br><img src='%s'><br><br>" % (name[5:], name[5:]))

    def getTiles(self, bank_nr):
        bank = self.__rom.banks[bank_nr]
        buffer = bytearray(b'\x00' * 16 * 16)
        result = []
        for n in range(0, len(bank), 16):
            for y in range(8):
                a = bank[n + y * 2]
                b = bank[n + y * 2 + 1]
                for x in range(8):
                    v = 0x3F
                    if not a & (0x80 >> x):
                        v |= 0x40
                    if not b & (0x80 >> x):
                        v |= 0x80
                    buffer[x+y*8] = v
            result.append(PIL.Image.frombytes('L', (8, 8), bytes(buffer)))
        return result

    def room_map_info(self, room):
        if room not in self.__room_map_info:
            self.__room_map_info[room] = RoomMapInfo()
        return self.__room_map_info[room]
