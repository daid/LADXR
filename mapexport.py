import PIL.Image, PIL.ImageDraw
from roomEditor import RoomEditor, ObjectHorizontal, ObjectVertical, ObjectWarp


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
                if self.getObject(x, y) in (0x28, 0x83, 0x90):
                    self.placeObject(x, y, 0x29)
                else:
                    self.placeObject(x, y, 0x25)
                if self.getObject(x + 1, y) in (0x27, 0x82, 0x90):
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

        self.__tiles = {
            0x0C: self.getTiles(0x0C),
            0x0D: self.getTiles(0x0D),
            0x0F: self.getTiles(0x0F),
            0x12: self.getTiles(0x12),
        }
        self.__room_map_info = {}

        f = open("test.html", "wt")
        result = PIL.Image.new("L", (16 * 20 * 8, 16 * 16 * 8))
        for n in range(0x100):
            x = n % 0x10
            y = n // 0x10
            result.paste(self.exportRoom(n), (x * 20 * 8, y * 16 * 8))
        result.save("overworld.png")
        f.write("<img src='overworld.png'><br><br>")
        
        self.exportMetaTiles(f, "metatiles_main.png", 0x0F, 0, lambda n: n >= 32 and (n < 0x6C or n >= 0x70))
        for n in (0x1A, 0x1C, 0x1E, 0x20, 0x22, 0x24, 0x26, 0x28, 0x2A, 0x2C, 0x2E, 0x30, 0x32, 0x34, 0x36, 0x38, 0x3A, 0x3C, 0x3E):
            self.exportMetaTiles(f, "metatiles_%02x.png" % (n), n, 0, lambda n: n < 32)
        for n in range(2, 17):
            self.exportMetaTiles(f, "metatiles_anim_%02x.png" % (n), 0x0F, n, lambda n: n >= 0x6C and n < 0x70)

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
            result.save("dungeon_%d.png" % (n))
            f.write("<img src='dungeon_%d.png'><br><br>" % (n))

        result = PIL.Image.new("L", (16 * 20 * 8, 16 * 16 * 8))
        for n in range(0x100):
            if n + 0x100 in self.__room_map_info:
                continue
            x = n % 0x10
            y = n // 0x10
            result.paste(self.exportRoom(n + 0x100), (x * 20 * 8, y * 16 * 8))
        result.save("caves1.png")
        f.write("<img src='caves1.png'><br><br>")
        result = PIL.Image.new("L", (16 * 20 * 8, 16 * 16 * 8))
        for n in range(0x0FF):
            if n + 0x200 in self.__room_map_info:
                continue
            x = n % 0x10
            y = n // 0x10
            result.paste(self.exportRoom(n + 0x200), (x * 20 * 8, y * 16 * 8))
        result.save("caves2.png")
        f.write("<img src='caves2.png'>")
        f.close()

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
        f.write("%s<br><img src='%s'><br><br>" % (name, name))

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
