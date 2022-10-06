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
        self.palette_id = None
        self.attribute_bank = None
        self.attribute_addr = None

    def to_json(self):
        return self.__dict__


class RenderedMap:
    WALL_UP = 0x01
    WALL_DOWN = 0x02
    WALL_LEFT = 0x04
    WALL_RIGHT = 0x08

    def __init__(self, floor_object, overworld=False):
        self.objects = {}
        self.overworld = overworld

        for y in range(8):
            for x in range(10):
                self.objects[(x, y)] = floor_object

    def addWalls(self, flags):
        for x in range(0, 10):
            if flags & RenderedMap.WALL_UP:
                self.placeObject(x, 0, 0x21)
            if flags & RenderedMap.WALL_DOWN:
                self.placeObject(x, 7, 0x22)
        for y in range(0, 8):
            if flags & RenderedMap.WALL_LEFT:
                self.placeObject(0, y, 0x23)
            if flags & RenderedMap.WALL_RIGHT:
                self.placeObject(9, y, 0x24)
        if flags & RenderedMap.WALL_LEFT and flags & RenderedMap.WALL_UP:
            self.placeObject(0, 0, 0x25)
        if flags & RenderedMap.WALL_RIGHT and flags & RenderedMap.WALL_UP:
            self.placeObject(9, 0, 0x26)
        if flags & RenderedMap.WALL_LEFT and flags & RenderedMap.WALL_DOWN:
            self.placeObject(0, 7, 0x27)
        if flags & RenderedMap.WALL_RIGHT and flags & RenderedMap.WALL_DOWN:
            self.placeObject(9, 7, 0x28)

    def placeObject(self, x, y, type_id):
        if self.overworld:
            if type_id == 0xF5:
                if self.getObject(x, y) in (0x28, 0x29, 0x83, 0x90):
                    self.placeObject(x, y, 0x29)
                else:
                    self.placeObject(x, y, 0x25)
                if self.getObject(x + 1, y) in (0x27, 0x2A, 0x82, 0x90):
                    self.placeObject(x + 1, y, 0x2A)
                else:
                    self.placeObject(x + 1, y, 0x26)
                if self.getObject(x, y + 1) in (0x26, 0x2A):
                    self.placeObject(x, y + 1, 0x2A)
                elif self.getObject(x, y + 1) == 0x90:
                    self.placeObject(x, y + 1, 0x82)
                else:
                    self.placeObject(x, y + 1, 0x27)
                if self.getObject(x + 1, y + 1) in (0x25, 0x29):
                    self.placeObject(x + 1, y + 1, 0x29)
                elif self.getObject(x + 1, y + 1) == 0x90:
                    self.placeObject(x + 1, y + 1, 0x83)
                else:
                    self.placeObject(x + 1, y + 1, 0x28)
            elif type_id == 0xF6: # two door house
                self.placeObject(x + 0, y, 0x55)
                self.placeObject(x + 1, y, 0x5A)
                self.placeObject(x + 2, y, 0x5A)
                self.placeObject(x + 3, y, 0x5A)
                self.placeObject(x + 4, y, 0x56)
                self.placeObject(x + 0, y + 1, 0x57)
                self.placeObject(x + 1, y + 1, 0x59)
                self.placeObject(x + 2, y + 1, 0x59)
                self.placeObject(x + 3, y + 1, 0x59)
                self.placeObject(x + 4, y + 1, 0x58)
                self.placeObject(x + 0, y + 2, 0x5B)
                self.placeObject(x + 1, y + 2, 0xE2)
                self.placeObject(x + 2, y + 2, 0x5B)
                self.placeObject(x + 3, y + 2, 0xE2)
                self.placeObject(x + 4, y + 2, 0x5B)
            elif type_id == 0xF7:  # large house
                self.placeObject(x + 0, y, 0x55)
                self.placeObject(x + 1, y, 0x5A)
                self.placeObject(x + 2, y, 0x56)
                self.placeObject(x + 0, y + 1, 0x57)
                self.placeObject(x + 1, y + 1, 0x59)
                self.placeObject(x + 2, y + 1, 0x58)
                self.placeObject(x + 0, y + 2, 0x5B)
                self.placeObject(x + 1, y + 2, 0xE2)
                self.placeObject(x + 2, y + 2, 0x5B)
            elif type_id == 0xF8:  # catfish
                self.placeObject(x + 0, y, 0xB6)
                self.placeObject(x + 1, y, 0xB7)
                self.placeObject(x + 2, y, 0x66)
                self.placeObject(x + 0, y + 1, 0x67)
                self.placeObject(x + 1, y + 1, 0xE3)
                self.placeObject(x + 2, y + 1, 0x68)
            elif type_id == 0xF9:  # palace door
                self.placeObject(x + 0, y, 0xA4)
                self.placeObject(x + 1, y, 0xA5)
                self.placeObject(x + 2, y, 0xA6)
                self.placeObject(x + 0, y + 1, 0xA7)
                self.placeObject(x + 1, y + 1, 0xE3)
                self.placeObject(x + 2, y + 1, 0xA8)
            elif type_id == 0xFA:   # stone pig head
                self.placeObject(x + 0, y, 0xBB)
                self.placeObject(x + 1, y, 0xBC)
                self.placeObject(x + 0, y + 1, 0xBD)
                self.placeObject(x + 1, y + 1, 0xBE)
            elif type_id == 0xFB:  # palmtree
                if x == 15:
                    self.placeObject(x + 1, y + 1, 0xB7)
                    self.placeObject(x + 1, y + 2, 0xCE)
                else:
                    self.placeObject(x + 0, y, 0xB6)
                    self.placeObject(x + 0, y + 1, 0xCD)
                    self.placeObject(x + 1, y + 0, 0xB7)
                    self.placeObject(x + 1, y + 1, 0xCE)
            elif type_id == 0xFC:  # square "hill with hole" (seen near lvl4 entrance)
                self.placeObject(x + 0, y, 0x2B)
                self.placeObject(x + 1, y, 0x2C)
                self.placeObject(x + 2, y, 0x2D)
                self.placeObject(x + 0, y + 1, 0x37)
                self.placeObject(x + 1, y + 1, 0xE8)
                self.placeObject(x + 2, y + 1, 0x38)
                self.placeObject(x - 1, y + 2, 0x0A)
                self.placeObject(x + 0, y + 2, 0x33)
                self.placeObject(x + 1, y + 2, 0x2F)
                self.placeObject(x + 2, y + 2, 0x34)
                self.placeObject(x + 0, y + 3, 0x0A)
                self.placeObject(x + 1, y + 3, 0x0A)
                self.placeObject(x + 2, y + 3, 0x0A)
                self.placeObject(x + 3, y + 3, 0x0A)
            elif type_id == 0xFD:  # small house
                self.placeObject(x + 0, y, 0x52)
                self.placeObject(x + 1, y, 0x52)
                self.placeObject(x + 2, y, 0x52)
                self.placeObject(x + 0, y + 1, 0x5B)
                self.placeObject(x + 1, y + 1, 0xE2)
                self.placeObject(x + 2, y + 1, 0x5B)
            else:
                self.objects[(x & 15), (y & 15)] = type_id
        else:
            if type_id == 0xEC:  # key door
                self.placeObject(x, y, 0x2D)
                self.placeObject(x + 1, y, 0x2E)
            elif type_id == 0xED:
                self.placeObject(x, y, 0x2F)
                self.placeObject(x + 1, y, 0x30)
            elif type_id == 0xEE:
                self.placeObject(x, y, 0x31)
                self.placeObject(x, y + 1, 0x32)
            elif type_id == 0xEF:
                self.placeObject(x, y, 0x33)
                self.placeObject(x, y + 1, 0x34)
            elif type_id == 0xF0:  # closed door
                self.placeObject(x, y, 0x35)
                self.placeObject(x + 1, y, 0x36)
            elif type_id == 0xF1:
                self.placeObject(x, y, 0x37)
                self.placeObject(x + 1, y, 0x38)
            elif type_id == 0xF2:
                self.placeObject(x, y, 0x39)
                self.placeObject(x, y + 1, 0x3A)
            elif type_id == 0xF3:
                self.placeObject(x, y, 0x3B)
                self.placeObject(x, y + 1, 0x3C)
            elif type_id == 0xF4:  # open door
                self.placeObject(x, y, 0x43)
                self.placeObject(x + 1, y, 0x44)
            elif type_id == 0xF5:
                self.placeObject(x, y, 0x8C)
                self.placeObject(x + 1, y, 0x08)
            elif type_id == 0xF6:
                self.placeObject(x, y, 0x09)
                self.placeObject(x, y + 1, 0x0A)
            elif type_id == 0xF7:
                self.placeObject(x, y, 0x0B)
                self.placeObject(x, y + 1, 0x0C)
            elif type_id == 0xF8:  # boss door
                self.placeObject(x, y, 0xA4)
                self.placeObject(x + 1, y, 0xA5)
            elif type_id == 0xF9:  # stairs door
                self.placeObject(x, y, 0xAF)
                self.placeObject(x + 1, y, 0xB0)
            elif type_id == 0xFA:  # flipwall
                self.placeObject(x, y, 0xB1)
                self.placeObject(x + 1, y, 0xB2)
            elif type_id == 0xFB:  # one way arrow
                self.placeObject(x, y, 0x45)
                self.placeObject(x + 1, y, 0x46)
            elif type_id == 0xFC:  # entrance
                self.placeObject(x + 0, y, 0xB3)
                self.placeObject(x + 1, y, 0xB4)
                self.placeObject(x + 2, y, 0xB4)
                self.placeObject(x + 3, y, 0xB5)
                self.placeObject(x + 0, y + 1, 0xB6)
                self.placeObject(x + 1, y + 1, 0xB7)
                self.placeObject(x + 2, y + 1, 0xB8)
                self.placeObject(x + 3, y + 1, 0xB9)
                self.placeObject(x + 0, y + 2, 0xBA)
                self.placeObject(x + 1, y + 2, 0xBB)
                self.placeObject(x + 2, y + 2, 0xBC)
                self.placeObject(x + 3, y + 2, 0xBD)
            elif type_id == 0xFD:  # entrance
                self.placeObject(x, y, 0xC1)
                self.placeObject(x + 1, y, 0xC2)
            else:
                self.objects[(x & 15), (y & 15)] = type_id

    def getObject(self, x, y):
        return self.objects.get(((x & 15), (y & 15)), None)


class MapExport:
    def __init__(self, rom):
        self.__rom = rom

        #self.__tiles = {
        #    0x0C: self.getTiles(0x0C),
        #    0x0D: self.getTiles(0x0D),
        #    0x0F: self.getTiles(0x0F),
        #    0x12: self.getTiles(0x12),
        #}
        self.__tile_cache = {}
        self.__room_map_info = {}
        self.__json_data = {
            "rooms": {},
            "maps": {},
            "attributes": {},
            "overworld_physics_flag": [n for n in self.__rom.banks[8][0x0AD4:0x0AD4+0x100]],
            "indoor1_physics_flag": [n for n in self.__rom.banks[8][0x0BD4:0x0BD4 + 0x100]],
        }

    def export_all(self, w=16, h=16):
        os.makedirs("_map/img", exist_ok=True)
        f = open("_map/test.html", "wt")
        self.buildOverworld(w, h).save("_map/img/overworld.png")
        f.write("<img src='img/overworld.png'><br><br>")

        for n in (0,1,2,3,4,5,6,7, 10): # skipping 11, color dungeon now
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
                    self.__room_map_info[room] = (x, y, n)
                    result.paste(self.buildRoom(room, n), (x * 161, y * 129))
            self.__json_data["maps"][f"dungeon_{n}"] = map_data
            result.save(f"_map/img/dungeon_{n}.png")
            f.write(f"<img src='img/dungeon_{n}.png' map='dungeon_{n}'><br><br>")

        f.write("<script>var data = ")
        f.write(json.dumps(self.__json_data))
        f.write("""
function h2(n) { if (n < 16) return "0x0" + n.toString(16); return "0x" + n.toString(16); }
function updateTooltip(e) {
    var map = e.target.getAttribute("map")
    var tooltip = document.getElementById("tooltip");
    var roomx = Math.floor(e.offsetX / 161);
    var roomy = Math.floor(e.offsetY / 129);
    var tilex = Math.floor((e.offsetX - roomx * 161) / 16)
    var tiley = Math.floor((e.offsetY - roomy * 129) / 16)
    if (tilex < 0 || tilex > 9 || tiley < 0 || tiley > 7) return;
    var room = data.rooms[roomx + roomy*16];
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

    tooltip.innerText = `Room ID: ${h2(room.n)}
        Tileset: ${h2(room.main_tileset_id)}
        Palette: ${h2(room.palette_id)}
        Animation set: ${h2(room.animation_tileset_id)}
        Attribute data: ${h2(room.attribute_bank)}:${h2(room.attribute_addr)}
        
        Tile ID: ${h2(tile_id)}
        Subtiles: ${h2(metatiles[tile_id*4])} ${h2(metatiles[tile_id*4+1])} ${h2(metatiles[tile_id*4+2])} ${h2(metatiles[tile_id*4+3])}
        TileAttr: ${h2(attributes[tile_id*4])} ${h2(attributes[tile_id*4+1])} ${h2(attributes[tile_id*4+2])} ${h2(attributes[tile_id*4+3])}
        Physics: ${h2(physics_flag[tile_id])}
    `
}
for(var e of document.getElementsByTagName("img")) {
    e.onmousemove = updateTooltip
}
        """)
        f.write("</script><div id='tooltip' style='position:absolute; background-color: white; padding: 4px; border: solid black 1px; white-space: nowrap'>X</div><div style='height:300px'></div>")
        return
        self.exportMetaTiles(f, "_map/img/metatiles_main.png", 0x0F, 0, lambda n: n >= 32 and (n < 0x6C or n >= 0x70))
        for n in (0x1A, 0x1C, 0x1E, 0x20, 0x22, 0x24, 0x26, 0x28, 0x2A, 0x2C, 0x2E, 0x30, 0x32, 0x34, 0x36, 0x38, 0x3A, 0x3C, 0x3E):
            self.exportMetaTiles(f, "_map/img/metatiles_%02x.png" % (n), n, 0, lambda n: n < 32)
        for n in range(2, 17):
            self.exportMetaTiles(f, "_map/img/metatiles_anim_%02x.png" % (n), 0x0F, n, lambda n: n >= 0x6C and n < 0x70)

        for n in (0,1,2,3,4,5,6,7, 10, 11):
            addr = 0x0220 + n * 8 * 8
            result = PIL.Image.new("L", (8 * 20 * 8, 8 * 16 * 8))
            for y in range(8):
                for x in range(8):
                    room = rom.banks[0x14][addr] + 0x100
                    if n > 5:
                        room += 0x100
                    if n == 11:
                        room += 0x100
                    addr += 1
                    if (room & 0xFF) == 0 and (n != 11 or x != 1 or y != 3):  # ignore room nr 0, except on a very specific spot in the color dungeon.
                        continue
                    self.__room_map_info[room] = (x, y, n)
                    result.paste(self.exportRoom(room), (x * 20 * 8, y * 16 * 8))
            result.save("_map/img/dungeon_%d.png" % (n))
            f.write("<img src='img/dungeon_%d.png'><br><br>" % (n))

        result = PIL.Image.new("L", (16 * 20 * 8, 16 * 16 * 8))
        for n in range(0x100):
            if n + 0x100 in self.__room_map_info:
                continue
            x = n % 0x10
            y = n // 0x10
            result.paste(self.exportRoom(n + 0x100), (x * 20 * 8, y * 16 * 8))
        result.save("_map/img/caves1.png")
        f.write("<img src='img/caves1.png'><br><br>")
        result = PIL.Image.new("L", (16 * 20 * 8, 16 * 16 * 8))
        for n in range(0x0FF):
            if n + 0x200 in self.__room_map_info:
                continue
            x = n % 0x10
            y = n // 0x10
            result.paste(self.exportRoom(n + 0x200), (x * 20 * 8, y * 16 * 8))
        result.save("_map/img/caves2.png")
        f.write("<img src='img/caves2.png'>")
        f.close()

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

    def getIndoorTileset(self, main_tileset, animation_id):
        subtiles = [0] * 0x100
        for n in range(0x20, 0x80):
            subtiles[n] = (0x0D << 10) + n - 0x20
        if main_tileset != 0xFF:
            for n in range(0x00, 0x10):
                subtiles[n] = (0x0D << 10) + 0x100 + main_tileset * 0x10+n
        for n in range(0x10, 0x20):
            subtiles[n] = (0x0D << 10) + 0x200 + n
        for n in range(0xF0, 0x100):
            subtiles[n] = (0x12 << 10) + 0x380 + n - 0xF0

        addr = (0x000, 0x000, 0x2B0, 0x2C0, 0x2D0, 0x2E0, 0x2F0, 0x2D0, 0x300, 0x310, 0x320, 0x2A0, 0x330, 0x350, 0x360, 0x340, 0x370)[animation_id]
        for n in range(0x6C, 0x70):
            subtiles[n] = (0x2C << 10) + addr + n - 0x6C
        return subtiles

    def getPalette(self, palette_index):
        if palette_index < 0x100:
            palette_addr = self.__rom.banks[0x21][0x02B1 + palette_index * 2]
            palette_addr |= self.__rom.banks[0x21][0x02B1 + palette_index * 2 + 1] << 8
        else:
            palette_addr = self.__rom.banks[0x21][0x03EF + (palette_index - 0x100) * 2]
            palette_addr |= self.__rom.banks[0x21][0x03EF + (palette_index - 0x100) * 2 + 1] << 8
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

    def buildRoom(self, room_id, map_id=None):
        re = RoomEditor(self.__rom, room_id)

        room = Room(room_id)
        if room_id < 0x100:
            room.main_tileset_id = self.__rom.banks[0x20][0x2E73 + (room_id & 0x0F) // 2 + ((room_id >> 5) * 8)]
            if self.__rom.banks[0x3F][0x2F00 + room_id]:  # If we have the the per room tileset patch, use that data
                room.main_tileset_id = self.__rom.banks[0x3F][0x2F00 + room_id]
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
        room.attribute_addr = self.__rom.banks[0x1A][0x1E76 + room_id * 2]
        room.attribute_addr |= self.__rom.banks[0x1A][0x1E76 + room_id * 2 + 1] << 8
        if room_id < 0x100:
            room.palette_id = self.__rom.banks[0x21][0x02EF + room_id]
        else:
            room.palette_id = 0x100 + map_id

        self.__json_data["rooms"][room_id] = room.to_json()

        # Draw the room
        if room_id < 0x100:
            tileset = self.getOverworldTileset(room.main_tileset_id, room.animation_tileset_id)
            metatiles = self.__rom.banks[0x1A][0x2B1D:0x2B1D+0x400]
            if "overworld_metatiles" not in self.__json_data:
                self.__json_data["overworld_metatiles"] = [n for n in metatiles]
        else:
            tileset = self.getIndoorTileset(room.main_tileset_id, room.animation_tileset_id)
            metatiles = self.__rom.banks[0x08][0x03B0:0x03B0+0x400]
            if "indoor1_metatiles" not in self.__json_data:
                self.__json_data["indoor1_metatiles"] = [n for n in metatiles]
        attributes = self.__rom.banks[room.attribute_bank][room.attribute_addr-0x4000:room.attribute_addr-0x4000+0x400]
        if (room.attribute_bank << 16) | room.attribute_addr not in self.__json_data["attributes"]:
            self.__json_data["attributes"][(room.attribute_bank << 16) | room.attribute_addr] = [n for n in attributes]
        result = PIL.Image.new('RGB', (8 * 20, 8 * 16))
        for y in range(8):
            for x in range(10):
                tile_nr = room.tiles[x + y * 10]
                metatile = metatiles[tile_nr*4:tile_nr*4+4]
                attrtile = attributes[tile_nr*4:tile_nr*4+4]
                self.drawSubtile(result, x*16, y*16, tileset[metatile[0]], attrtile[0], room.palette_id)
                self.drawSubtile(result, x*16+8, y*16, tileset[metatile[1]], attrtile[1], room.palette_id)
                self.drawSubtile(result, x*16, y*16+8, tileset[metatile[2]], attrtile[2], room.palette_id)
                self.drawSubtile(result, x*16+8, y*16+8, tileset[metatile[3]], attrtile[3], room.palette_id)
        return result

    def drawSubtile(self, img, ox, oy, subtile_id, attr, palette_id):
        if (subtile_id, attr, palette_id) not in self.__tile_cache:
            result = PIL.Image.new("RGB", (8, 8))
            palette = self.getPalette(palette_id)[(attr&7)*4:(attr&7)*4+4]
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
            self.__tile_cache[(subtile_id, attr, palette_id)] = result
        img.paste(self.__tile_cache[(subtile_id, attr, palette_id)], (ox, oy))

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

    def exportRoom(self, room_nr):
        re = RoomEditor(self.__rom, room_nr)

        if room_nr < 0x100:
            tile_info_offset = self.__rom.banks[0x1A].find(b'\x7C\x7C\x7C\x7C\x7D\x7D\x7D\x7D')
            tile_info = self.__rom.banks[0x1A][tile_info_offset:tile_info_offset + 0x100 * 4]
        else:
            tile_info_offset = self.__rom.banks[0x08].find(b'\x7F\x7F\x7F\x7F\x7E\x7E\x7E\x7E')
            tile_info = self.__rom.banks[0x08][tile_info_offset:tile_info_offset+0x100*4]

        if room_nr >= 0x100:
            rendered_map = RenderedMap(re.floor_object & 0x0F)
        else:
            rendered_map = RenderedMap(re.floor_object, True)
        def objHSize(type_id):
            if type_id == 0xF5:
                return 2
            return 1
        def objVSize(type_id):
            if type_id == 0xF5:
                return 2
            return 1
        if room_nr >= 0x100:
            if re.floor_object & 0xF0 == 0x00:
                rendered_map.addWalls(RenderedMap.WALL_LEFT | RenderedMap.WALL_RIGHT | RenderedMap.WALL_UP | RenderedMap.WALL_DOWN)
            if re.floor_object & 0xF0 == 0x10:
                rendered_map.addWalls(RenderedMap.WALL_LEFT | RenderedMap.WALL_RIGHT | RenderedMap.WALL_DOWN)
            if re.floor_object & 0xF0 == 0x20:
                rendered_map.addWalls(RenderedMap.WALL_LEFT | RenderedMap.WALL_UP | RenderedMap.WALL_DOWN)
            if re.floor_object & 0xF0 == 0x30:
                rendered_map.addWalls(RenderedMap.WALL_LEFT | RenderedMap.WALL_RIGHT | RenderedMap.WALL_UP)
            if re.floor_object & 0xF0 == 0x40:
                rendered_map.addWalls(RenderedMap.WALL_RIGHT | RenderedMap.WALL_UP | RenderedMap.WALL_DOWN)
            if re.floor_object & 0xF0 == 0x50:
                rendered_map.addWalls(RenderedMap.WALL_LEFT | RenderedMap.WALL_DOWN)
            if re.floor_object & 0xF0 == 0x60:
                rendered_map.addWalls(RenderedMap.WALL_RIGHT | RenderedMap.WALL_DOWN)
            if re.floor_object & 0xF0 == 0x70:
                rendered_map.addWalls(RenderedMap.WALL_RIGHT | RenderedMap.WALL_UP)
            if re.floor_object & 0xF0 == 0x80:
                rendered_map.addWalls(RenderedMap.WALL_LEFT | RenderedMap.WALL_UP)
        for obj in re.objects:
            if isinstance(obj, ObjectWarp):
                pass
            elif isinstance(obj, ObjectHorizontal):
                for n in range(0, obj.count):
                    rendered_map.placeObject(obj.x + n * objHSize(obj.type_id), obj.y, obj.type_id)
            elif isinstance(obj, ObjectVertical):
                for n in range(0, obj.count):
                    rendered_map.placeObject(obj.x, obj.y + n * objVSize(obj.type_id), obj.type_id)
            else:
                rendered_map.placeObject(obj.x, obj.y, obj.type_id)

        tiles = [0] * 20 * 16
        for y in range(8):
            for x in range(10):
                obj = rendered_map.objects[(x, y)]
                tiles[x*2 + y*2*20] = tile_info[obj*4]
                tiles[x*2+1 + y*2*20] = tile_info[obj*4+1]
                tiles[x*2 + (y*2+1)*20] = tile_info[obj*4+2]
                tiles[x*2+1 + (y*2+1)*20] = tile_info[obj*4+3]

        if room_nr < 0x100:
            sub_tileset_offset = self.__rom.banks[0x20][0x2E73 + (room_nr & 0x0F) // 2 + ((room_nr >> 5) * 8)] << 4
            if self.__rom.banks[0x3F][0x2F00 + room_nr]:  # If we have the the per room tileset patch, use that data
                sub_tileset_offset = self.__rom.banks[0x3F][0x2F00 + room_nr] << 4
            tilemap = self.__tiles[0x0f][sub_tileset_offset:sub_tileset_offset+0x20]
            tilemap += self.__tiles[0x0c][0x120:0x180]
            tilemap += self.__tiles[0x0c][0x080:0x100]
        else:
            # TODO: The whole indoor tileset loading seems complex...
            tileset_nr = self.__rom.banks[0x20][0x2eB3 + room_nr - 0x100]
            tilemap = [None] * 0x100
            tilemap[0x20:0x80] = self.__tiles[0x0D][0x000:0x060]
            if tileset_nr != 0xFF:
                tilemap[0x00:0x10] = self.__tiles[0x0D][0x100 + tileset_nr * 0x10:0x110 + tileset_nr * 0x10]
            tilemap[0x10:0x20] = self.__tiles[0x0D][0x210:0x220]
            tilemap[0xF0:0x100] = self.__tiles[0x12][0x380:0x390]

        if re.animation_id == 2:
            addr = 0x2B0
        elif re.animation_id == 3:
            addr = 0x2C0
        elif re.animation_id == 4:
            addr = 0x2D0
        elif re.animation_id == 5:
            addr = 0x2E0
        elif re.animation_id == 6:
            addr = 0x2F0
        elif re.animation_id == 7:
            addr = 0x2D0
        elif re.animation_id == 8:
            addr = 0x300
        elif re.animation_id == 9:
            addr = 0x310
        elif re.animation_id == 10:
            addr = 0x320
        elif re.animation_id == 11:
            addr = 0x2A0
        elif re.animation_id == 12:
            addr = 0x330
        elif re.animation_id == 13:
            addr = 0x350
        elif re.animation_id == 14:
            addr = 0x360
        elif re.animation_id == 15:
            addr = 0x340
        elif re.animation_id == 16:
            addr = 0x370
        else:
            print(hex(room_nr), re.animation_id)
            addr = 0x000
        tilemap[0x6C:0x70] = self.__tiles[0x0c][addr:addr+4]

        assert len(tilemap) == 0x100

        result = PIL.Image.new('L', (8 * 20, 8 * 16))
        draw = PIL.ImageDraw.Draw(result)
        for y in range(16):
            for x in range(20):
                tile = tilemap[tiles[x+y*20]]
                if tile is not None:
                    result.paste(tile, (x * 8, y * 8))
        warp_pos = []
        for y in range(8):
            for x in range(10):
                # draw.text((x * 16 + 3, y * 16 + 2), "%02X" % (rendered_map.objects[(x, y)]))
                # physics_flags = self.__rom.banks[8][0x0AD4 + rendered_map.objects[(x, y)]]
                # if physics_flags != 0:
                #     draw.text((x * 16 + 3, y * 16 + 2), "%02X" % (physics_flags))
                if rendered_map.objects[(x, y)] in (0xE1, 0xE2, 0xE3, 0xBA, 0xD5, 0xA8, 0xBE, 0xCB):
                    warp_pos.append((x, y))
        for x, y, type_id in re.entities:
            draw.rectangle([(x * 16, y * 16), (x * 16 + 15, y * 16 + 15)], outline=0)
            draw.text((x * 16 + 3, y * 16 + 2), "%02X" % (type_id))
        y = 8
        for obj in re.objects:
            if isinstance(obj, ObjectWarp):
                draw.text((8, y), "W%d:%02x:%03x:%d,%d" % (obj.warp_type, obj.map_nr, obj.room, obj.target_x, obj.target_y))
                y += 16
        return result

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
