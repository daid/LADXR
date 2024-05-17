
from romTables import ROMWithTables
import PIL.Image
import PIL.ImageDraw
import os
import json
import entityData


acceptable_tile_list = [
    {"tile": 0x05},
    {"tile": 0x03},
    {"tile": 0x07},
    {"tile": 0x8C},
    {"tile": 0x08},
    {"tile": 0x43},
    {"tile": 0x44},
    {"tile": 0x09},
    {"tile": 0x0A},
    {"tile": 0x0B},
    {"tile": 0x0C},
    {"tile": 0x0D},
    {"tile": 0x0E, "anim": [3, 10, 11, 12], "water": True},
    {"tile": 0x0F},
    {"tile": 0x10},
    {"tile": 0x11},
    {"tile": 0x12},
    {"tile": 0x13},
    {"tile": 0x14},
    {"tile": 0x15},
    {"tile": 0x16},
    {"tile": 0x17},
    # {"tile": 0x18},
    {"tile": 0x19},
    {"tile": 0x1A},
    {"tile": 0x93},
    {"tile": 0x94},
    {"tile": 0x95},
    {"tile": 0x96},
    {"tile": 0x1B, "anim": [3, 11, 12]},
    {"tile": 0x1C, "pit": True, "warp": True},
    {"tile": 0x1D, "pit": True, "warp": True},
    {"tile": 0x1E, "pit": True, "warp": True},
    {"tile": 0x1F, "pit": True, "warp": True},
    {"tile": 0x20},
    {"tile": 0x21},
    {"tile": 0x22},
    {"tile": 0x23},
    {"tile": 0x24},
    {"tile": 0x25},
    {"tile": 0x26},
    {"tile": 0x27},
    {"tile": 0x28},
    {"tile": 0x29},
    {"tile": 0x2A},
    {"tile": 0x2B},
    {"tile": 0x2C},
    {"tile": 0x2D, "door": True, "key": True},
    {"tile": 0x2E, "door": True, "key": True},
    {"tile": 0x2F, "door": True, "key": True},
    {"tile": 0x30, "door": True, "key": True},
    {"tile": 0x31, "door": True, "key": True},
    {"tile": 0x32, "door": True, "key": True},
    {"tile": 0x33, "door": True, "key": True},
    {"tile": 0x34, "door": True, "key": True},
    {"tile": 0x35, "door": True},
    {"tile": 0x36, "door": True},
    {"tile": 0x37, "door": True},
    {"tile": 0x38, "door": True},
    {"tile": 0x39, "door": True},
    {"tile": 0x3A, "door": True},
    {"tile": 0x3B, "door": True},
    {"tile": 0x3C, "door": True},
    {"tile": 0x3F, "bomb": True},
    {"tile": 0x40, "bomb": True},
    {"tile": 0x41, "bomb": True},
    {"tile": 0x42, "bomb": True},
    {"tile": 0x45, "door": True},
    {"tile": 0x46, "door": True},
    {"tile": 0x47, "bomb": True},
    {"tile": 0x48, "bomb": True},
    {"tile": 0x49, "bomb": True},
    {"tile": 0x4A, "bomb": True},
    {"tile": 0x98},
    {"tile": 0xA0, "chest": True},
    {"tile": 0xA6},
    {"tile": 0xA7, "move": True},
    {"tile": 0xA9, "bomb": True},
    {"tile": 0xAB, "anim": [4, 6, 7]},
    {"tile": 0xAC, "anim": [4, 6, 7]},
    {"tile": 0x01, "pit": True},
    {"tile": 0xAE, "pit": True},
    {"tile": 0xAF, "pit": True},
    {"tile": 0xB0, "pit": True},
    {"tile": 0xC0},
    {"tile": 0xC7, "anim": [4, 7, 12]},
    {"tile": 0xC8, "anim": [4, 7, 12]},
    {"tile": 0xC9, "anim": [4, 7, 12]},
    {"tile": 0xCA, "anim": [4, 7, 12]},
    {"tile": 0xA3, "stairs": True, "tileset": [0x03, 0x0B, 0x0E]},
    {"tile": 0xBE, "stairs": True},
    {"tile": 0xCB, "stairs": True, "tileset": [0x05, 0x0B, 0x0C]},
#    {"tile": 0xDB, "switchblock": True},
#    {"tile": 0xDC. "switchblock": True},
    {"tile": 0x4E, "tileset": [0x0C]},
    {"tile": 0xDD, "tileset": [0x05]},
    {"tile": 0xDF},
    {"tile": 0xCE, "tileset": [0x08]},
    {"tile": 0x9B, "tileset": [0x08]},
    {"tile": 0x9C, "tileset": [0x08]},
    {"tile": 0xC5, "tileset": [0x08]},
    {"tile": 0xC6, "tileset": [0x08]},
]
entities_list = [
    {"id": 0x09, "tiles": [0, 0], "attr": [0x02, 0x22]},
    {"id": 0x0B, "tiles": [0, 1], "attr": [0x01, 0x01]},
    {"id": 0x14, "tiles": [0, 1, -1, 8], "attr": [0x01, 0x01, 0, 0x100]},
    {"id": 0x19, "tiles": [0, 0], "attr": [0x01, 0x21]},
    {"id": 0x0D, "tiles": [4, 4], "attr": [0x02, 0x22]},
    {"id": 0x0E, "tiles": [0, 0], "attr": [0x01, 0x21]},
    {"id": 0x0F, "tiles": [0, 1], "attr": [0x04, 0x04]},
    {"id": 0x11, "tiles": [3, 4], "attr": [0x02, 0x02]},
    {"id": 0x12, "tiles": [6, 7], "attr": [0x02, 0x02]},
    {"id": 0x15, "tiles": [5, 5], "attr": [0x03, 0x23]},
    {"id": 0x18, "tiles": [0, 0], "attr": [0x01, 0x21]},
    {"id": 0x1A, "tiles": [5, 6], "attr": [0x00, 0x00]},
    {"id": 0x1C, "tiles": [3,-1], "attr": [0x00, 0x00]},
    {"id": 0x1E, "tiles": [5, 6], "attr": [0x01, 0x01]},
    {"id": 0x1B, "tiles": [1, 1], "attr": [0x00, 0x20]},
    {"id": 0x9B, "tiles": [1, 1], "attr": [0x02, 0x22]},
    {"id": 0x1F, "tiles": [10, 11], "attr": [0x01, 0x01]},
    {"id": 0x20, "tiles": [2, 2], "attr": [0x03, 0x23]},
    {"id": 0x21, "tiles": [0, 0], "attr": [0x00, 0x20]},
    {"id": 0x23, "tiles": [6, 6], "attr": [0x01, 0x21]},
    {"id": 0x24, "tiles": [0, 1], "attr": [0x02, 0x02]},
    {"id": 0x27, "tiles": [0, 0], "attr": [0x03, 0x23]},
    {"id": 0x28, "tiles": [0, 1], "attr": [0x01, 0x01]},
    {"id": 0x29, "tiles": [3, 4], "attr": [0x00, 0x00]},
    {"id": 0x2A, "tiles": [0, 0], "attr": [0x00, 0x20]},
    #0x2D: None,      # DROPPABLE_HEART
    {"id": 0x2C, "tiles": [0, 0], "attr": [0x00, 0x20]},
    #0x2E: None,      # DROPPABLE_RUPEE
    #0x2F: None,      # DROPPABLE_FAIRY
    #0x37: None,      # DROPPABLE_ARROWS
    #0x38: None,      # DROPPABLE_BOMBS
    {"id": 0x50, "tiles": [0, 1], "attr": [0x03, 0x03]},
    {"id": 0x51, "tiles": [0, 1], "attr": [0x02, 0x02]},
    {"id": 0x52, "tiles": [6, 6], "attr": [0x03, 0x23]},
    {"id": 0x53, "tiles": [6, 6], "attr": [0x00, 0x20]},
    {"id": 0x55, "tiles": [7, 7], "attr": [0x00, 0x20]},
    {"id": 0x56, "tiles": [0, 1], "attr": [0x00, 0x00]},
    {"id": 0x57, "tiles": [0, 1], "attr": [0x00, 0x00]},
    # {"id": 0x6C}, # CUCCU
    {"id": 0x7A, "tiles": [0, 1], "attr": [0x03, 0x03]},
    {"id": 0x7C, "tiles": [1, 1], "attr": [0x02, 0x22]},
    {"id": 0x7E, "tiles": [1, 1], "attr": [0x02, 0x22]},
    {"id": 0x8F, "tiles": [0, 1], "attr": [0x01, 0x01]},
    {"id": 0x90, "tiles": [0, 1], "attr": [0x01, 0x01]},
    {"id": 0x91, "tiles": [0, 1], "attr": [0x01, 0x01]},
    {"id": 0x99, "tiles": [0, 0], "attr": [0x00, 0x20]},
    {"id": 0x9C, "tiles": [3, 4], "attr": [0x00, 0x00]},
    {"id": 0x9F, "tiles": [5, 6], "attr": [0x02, 0x02]},
    {"id": 0xA0, "tiles": [0, 0], "attr": [0x02, 0x22]},
    {"id": 0xA1, "tiles": [2, 3], "attr": [0x00, 0x00]},
    {"id": 0xAE, "tiles": [0, 0, 9, 9], "attr": [0x02, 0x22, 0x00, 0x20]},
    {"id": 0xB0, "tiles": [0, 0], "attr": [0x02, 0x22]},
    {"id": 0xB2, "tiles": [0, 1], "attr": [0x01, 0x01]},
    {"id": 0xBA, "tiles": [2, 1], "attr": [0x02, 0x02]},
    {"id": 0xBD, "tiles": [0, 1], "attr": [0x02, 0x02]},
    {"id": 0xC5, "tiles": [6, 7], "attr": [0x03, 0x03]},
    {"id": 0xC6, "tiles": [4, 4], "attr": [0x02, 0x22]},
    {"id": 0xCB, "tiles": [3, 3], "attr": [0x01, 0x21]},
    {"id": 0xCC, "tiles": [2, 3], "attr": [0x03, 0x03]},
    {"id": 0xE3, "tiles": [2, 2], "attr": [0x00, 0x20]},
    {"id": 0xEC, "tiles": [0, 0], "attr": [0x02, 0x22]},
    {"id": 0xED, "tiles": [0, 0], "attr": [0x00, 0x20]},
    {"id": 0xEE, "tiles": [0, 0], "attr": [0x03, 0x23]},

    {"id": 0x81, "tiles": [3, 4], "attr": [0x02, 0x02]},
    {"id": 0x89, "tiles": [1, 2], "attr": [0x02, 0x02]},
    {"id": 0x60, "tiles": [0, 0], "attr": [0x00, 0x20]},
    {"id": 0x8E, "tiles": [0, 1], "attr": [0x02, 0x02]},
    {"id": 0x5E, "tiles": [0, 0], "attr": [0x00, 0x20]},
    {"id": 0x92, "tiles": [0, 1], "attr": [0x03, 0x03]},
    {"id": 0xBC, "tiles": [1, 2], "attr": [0x03, 0x03]},
    {"id": 0xBE, "tiles": [4, 5], "attr": [0x01, 0x01]},
    {"id": 0xF4, "tiles": [1, 2], "attr": [0x01, 0x01]},
    {"id": 0xF8, "tiles": [0, 1], "attr": [0x00, 0x00]},
    {"id": 0xE4, "tiles": [13, 14], "attr": [0x02, 0x02]},
    {"id": 0x88, "tiles": [0, 1], "attr": [0x02, 0x02]},

#    {"id": 0xFF},
]
allow_set = {t["tile"] for t in acceptable_tile_list}


class Exporter:
    def __init__(self, rom_filename, output_path):
        self.rom = ROMWithTables(open(rom_filename, "rb"))
        os.chdir(output_path)
        # Fix tile attributes for bombable walls
        self.rom.patch(0x24, 0x0400 + 0x3F * 4, "00000000040404040000000000000000", "04040404040404040404040404040404")
        self.rom.patch(0x24, 0x0400 + 0x93 * 4, "00000000000000000000000000000000", "01050505050105050505010505050501")  # single tile corners
        self.rom.patch(0x24, 0x0400 + 0xCE * 4, "07070707", "04040404")  # Small table

        self.metatiles = self.rom.banks[0x08][0x03B0:0x03B0+0x400]
        self.attribute_addr = 0x4400
        self.attribute_bank = 0x24
        self.attributes = self.rom.banks[self.attribute_bank][self.attribute_addr-0x4000:self.attribute_addr-0x4000+0x400]
        self.pal = self.getPalette(0x69B0)
        self.__tile_cache = {}
        self.create_tiles_image()
        self.pal = self.getPalette(0x5518)
        for n in range(0, 16, 4):
            self.pal[n] = (255,0,255,0)
        self.create_entities_image()

    def create_tiles_image(self):
        img = PIL.Image.new('RGBA', (16 * len(acceptable_tile_list), 16), (0,0,0,0))
        for idx, info in enumerate(acceptable_tile_list):
            n = info["tile"]
            tileset = self.get_tileset(0x0A, info.get("tileset", [None])[0], info.get("anim", [None])[0])
            metatile = self.metatiles[n*4:n*4+4]
            attrtile = self.attributes[n*4:n*4+4]
            self.drawSubtile(img, idx*16, 0, tileset[metatile[0]], attrtile[0])
            self.drawSubtile(img, idx*16+8, 0, tileset[metatile[1]], attrtile[1])
            self.drawSubtile(img, idx*16, 8, tileset[metatile[2]], attrtile[2])
            self.drawSubtile(img, idx*16+8, 8, tileset[metatile[3]], attrtile[3])
            if info.get("bomb"):
                self.drawSubtile(img, idx*16 + 4, 0, (0x2C, 0x800), 0x100)
                self.drawSubtile(img, idx*16 + 4, 8, (0x2C, 0x810), 0x100)
            if info.get("move"):
                self.drawSubtile(img, idx*16 + 4, 0, (0x2C, 0x7D0), 0x102)
                self.drawSubtile(img, idx*16 + 4, 8, (0x2C, 0x7C0), 0x102)
                self.drawSubtile(img, idx*16 + 0, 5, (0x2C, 0x7E0), 0x106)
                self.drawSubtile(img, idx*16 + 8, 4, (0x2C, 0x7F0), 0x106)
        img.save("tiles.png")
        print(acceptable_tile_list[70])
        print(acceptable_tile_list[85])
        json.dump(acceptable_tile_list, open("tiles.json", "wt"))
        print(json.load(open("tiles.json", "rt"))[70])
        print(json.load(open("tiles.json", "rt"))[85])

    def create_entities_image(self):
        img = PIL.Image.new('RGBA', (16 * len(entities_list), 16*4*4), (0,0,0,0))
        for idx, info in enumerate(entities_list):
            sd = entityData.SPRITE_DATA[info["id"]] if info["id"] in entityData.SPRITE_DATA else None
            if callable(sd):
                class R:
                    pass
                room = R()
                room.room = 0x2B6
                sd = sd(room)
            if sd is None:
                sd = (1, 0x91)
                info["sprites"] = []
            else:
                info["sprites"] = [list(sorted(n))[0] if isinstance(n, set) else n for n in sd]
            tileset = []
            for gfx_idx in range(1, len(sd), 2):
                gfx_nr = sd[gfx_idx]
                if isinstance(gfx_nr, set):
                    gfx_nr = list(sorted(gfx_nr))[0]
                bank = [0x35, 0x31, 0x2E, 0x32][gfx_nr >> 6]
                addr = (gfx_nr & 0x3F) * 0x100
                for n in range(16):
                    tileset.append((bank, addr+0x10*n))
            tileset.append((0x2C, 0x040))
            tileset.append((0x2C, 0x050))
            tileset.append((0x2C, 0x220))
            tileset.append((0x2C, 0x230))
            if "tiles" in info:
                for n in range(len(info["tiles"])):
                    if info["tiles"][n] >= 0:
                        self.drawSubtile(img, idx*16+(n%2*8), 0, tileset[info["tiles"][n]*2], info["attr"][n])
                        self.drawSubtile(img, idx*16+(n%2*8), 8, tileset[info["tiles"][n]*2+1], info["attr"][n])
            else:
                for n, tile in enumerate(tileset):
                    x = idx*16 + (n//32)*8
                    y = (n%32)*8
                    self.drawSubtile(img, x, y, tile, 0)
        img.save("entities.png")
        json.dump(entities_list, open("entities.json", "wt"))

    def tmp(self):
        img = PIL.Image.new('RGBA', (16 + 4*16*17, 16 + 4*16*17), (0,0,0,0))
        for n in range(16):
            print(hex(n))
            img.paste(self.create_full_tileset_image(n), ((n%4)*16*17 + 16, (n//4)*16*17 + 16))
        for n in range(16):
            PIL.ImageDraw.ImageDraw(img).text((16 + n * 16, 3), f"x{n:X}", (0, 0, 0))
            PIL.ImageDraw.ImageDraw(img).text((0, 16 + n * 16), f"{n:X}x", (0, 0, 0))
        img.save("tmp.png")

    def get_tileset(self, map_id, main_tileset=None, anim_tileset=None):
        tileset = [None] * 0x100

        floor_tiles_ptr = (self.rom.banks[0x20][0x0589 + map_id] - 0x40) * 0x100
        wall_tiles_ptr = (self.rom.banks[0x20][0x05A9 + map_id] - 0x40) * 0x100
        for n in range(0x10, 0x20):
            tileset[n] = (0x2D, n * 0x10 + floor_tiles_ptr - 0x100)
        for n in range(0x20, 0x40):
            tileset[n] = (0x2D, n * 0x10 - 0x200 + wall_tiles_ptr)
        for n in range(0x40, 0x80):
            tileset[n] = (0x2D, n * 0x10 - 0x200)
        for n in range(0xF0, 0x100):
            tileset[n] = (0x32, 0x3800 + n * 0x10 - 0xF00)
        for n in range(0x6C, 0x70):
            tileset[n] = None

        #tileset = [None] * 0x100
        if main_tileset is not None:
            for n in range(0, 0x10): # main tileset
                tileset[n] = (0x2D, 0x1000 + n * 0x10 + 0x100 * main_tileset)

        if anim_tileset is not None:
            addr = (0x000, 0x000, 0x2B0, 0x2C0, 0x2D0, 0x2E0, 0x2F0, 0x2D0, 0x300, 0x310, 0x320, 0x2A0, 0x330, 0x350, 0x360, 0x340, 0x370)[anim_tileset]
            for n in range(0x6C, 0x70):
                tileset[n] = (0x2C, + addr * 0x10 + (n - 0x6C) * 0x10)
        return tileset

    def create_full_tileset_image(self, main_tileset):
        self.__tile_cache = {}
        tileset = self.get_tileset(0x0A, main_tileset, None)

        img = PIL.Image.new('RGBA', (16*16, 16*16), (0,0,0,0))
        for n in range(0x100):
            if n in allow_set:
                continue
            x = n % 16
            y = n // 16
            metatile = self.metatiles[n*4:n*4+4]
            attrtile = self.attributes[n*4:n*4+4]
            self.drawSubtile(img, x*16, y*16, tileset[metatile[0]], attrtile[0])
            self.drawSubtile(img, x*16+8, y*16, tileset[metatile[1]], attrtile[1])
            self.drawSubtile(img, x*16, y*16+8, tileset[metatile[2]], attrtile[2])
            self.drawSubtile(img, x*16+8, y*16+8, tileset[metatile[3]], attrtile[3])
        return img

    def drawSubtile(self, img, ox, oy, subtile_id, attr):
        if subtile_id is None:
            return
        pal = self.pal[(attr&7)*4:(attr&7)*4+4]
        if (subtile_id, attr) not in self.__tile_cache:
            result = PIL.Image.new("RGBA", (8, 8), (0, 0, 0, 0))
            addr = subtile_id[1]
            tile_data = self.rom.banks[subtile_id[0]][addr:addr+0x10]
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
                    if v != 0 or (attr & 0x100) == 0:
                        result.putpixel((x,y), pal[v])
            self.__tile_cache[(subtile_id, attr)] = result
        img.paste(self.__tile_cache[(subtile_id, attr)], (ox, oy), self.__tile_cache[(subtile_id, attr)])

    def getPalette(self, palette_addr):
        palette_addr -= 0x4000

        palette = []
        for n in range(8*4):
            p0 = self.rom.banks[0x21][palette_addr]
            p1 = self.rom.banks[0x21][palette_addr + 1]
            pal = p0 | p1 << 8
            palette_addr += 2
            r = (pal & 0x1F) << 3
            g = ((pal >> 5) & 0x1F) << 3
            b = ((pal >> 10) & 0x1F) << 3
            palette.append((r, g, b))
        return palette



Exporter("input.gbc", "/var/www/ladxr/drd/")
