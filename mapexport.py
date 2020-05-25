import PIL.Image
import os
from roomEditor import RoomEditor, Object, ObjectHorizontal, ObjectVertical, ObjectWarp


class RenderedMap:
    WALL_UP = 0x01
    WALL_DOWN = 0x02
    WALL_LEFT = 0x04
    WALL_RIGHT = 0x08

    def __init__(self, floor_object):
        self.objects = {}

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
        if type_id == 0xF5:
            # TOFIX there seems to be some complex tree overlapping logic
            self.placeObject(x, y, 0x25)
            self.placeObject(x + 1, y, 0x26)
            self.placeObject(x, y + 1, 0x27)
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


class MapExport:
    def __init__(self, rom):
        self.__rom = rom

        self.__tiles = {
            0x0C: self.getTiles(0x0C),
            0x0D: self.getTiles(0x0D),
            0x0F: self.getTiles(0x0F),
        }

        f = open("test.html", "wt")
        result = PIL.Image.new("L", (16 * 20 * 8, 16 * 16 * 8))
        for n in range(0x100):
            x = n % 0x10
            y = n // 0x10
            result.paste(self.exportRoom(n), (x * 20 * 8, y * 16 * 8))
        result.save("overworld.png")
        f.write("<img src='overworld.png'>")
        result = PIL.Image.new("L", (16 * 20 * 8, 16 * 16 * 8))
        for n in range(0x100):
            x = n % 0x10
            y = n // 0x10
            result.paste(self.exportRoom(n + 0x100), (x * 20 * 8, y * 16 * 8))
        result.save("caves1.png")
        f.write("<img src='caves1.png'>")
        f.close()

    def exportRoom(self, room_nr):
        re = RoomEditor(self.__rom, room_nr)
        # TODO: Caves&Dungeons (proper tileset and templates)
        if room_nr < 0x100:
            tile_info_offset = self.__rom.banks[0x1A].find(b'\x7C\x7C\x7C\x7C\x7D\x7D\x7D\x7D')
            tile_info = self.__rom.banks[0x1A][tile_info_offset:tile_info_offset + 0x100 * 4]
        else:
            tile_info_offset = self.__rom.banks[0x08].find(b'\x7F\x7F\x7F\x7F\x7E\x7E\x7E\x7E')
            tile_info = self.__rom.banks[0x08][tile_info_offset:tile_info_offset+0x100*4]

        if room_nr >= 0x100:
            rendered_map = RenderedMap(re.floor_object & 0x0F)
        else:
            rendered_map = RenderedMap(re.floor_object)
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
            tilemap = self.__tiles[0x0f][sub_tileset_offset:sub_tileset_offset+0x20]
            tilemap += self.__tiles[0x0c][0x120:0x180]
            tilemap += self.__tiles[0x0c][0x080:0x100]
        else:
            # TODO: The whole indoor tileset loading seems complex...
            tileset_nr = self.__rom.banks[0x20][0x2e7b + 0x40 + room_nr - 0x100]
            tilemap = [None] * 0x100
            tilemap[0x20:0x80] = self.__tiles[0x0D][0:0x60]

        # Placeholder for animated tiles, this needs a more complex lookup depending on re.animation_id, but not a straight mapping.
        addr = 0x2C0
        tilemap[0x6C:0x70] = self.__tiles[0x0c][addr:addr+4]

        assert len(tilemap) == 0x100

        result = PIL.Image.new('L', (8 * 20, 8 * 16))
        for y in range(16):
            for x in range(20):
                tile = tilemap[tiles[x+y*20]]
                if tile is not None:
                    result.paste(tile, (x * 8, y * 8))
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
