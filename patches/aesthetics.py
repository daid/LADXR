from assembler import ASM
from patches import extragfx
from utils import formatText, setReplacementName, randomNumber, randomOrdinal
from roomEditor import RoomEditor
from backgroundEditor import BackgroundEditor
import entityData
import os
import json
import struct
import random
import re
import math
import zlib


def imageTo2bpp(filename, *, tileheight=None, colormap=None):
    import PIL.Image
    if isinstance(filename, str):
        img = PIL.Image.open(filename)
    else:
        img = filename
    if img.mode != "P":
        img = img.convert("P", palette=PIL.Image.ADAPTIVE, colors=4)
    remap = [0, 1, 2, 3]
    if colormap:
        pal3 = img.getpalette()[0:12]
        pal = [(pal3[n*3] << 16) | (pal3[n*3+1] << 8) | (pal3[n*3+2]) for n in range(4)]
        for m in range(4):
            diff = [abs((pal[n] & 0xFF) - (colormap[m] & 0xFF)) + abs(((pal[n] >> 8) & 0xFF) - ((colormap[m] >> 8) & 0xFF)) + abs(((pal[n] >> 16) & 0xFF) - ((colormap[m] >> 16) & 0xFF)) for n in range(4)]
            remap[m] = diff.index(min(diff))
    assert (img.size[0] % 8) == 0
    if tileheight is None:
        tileheight = 8 if img.size[1] == 8 else 16
    assert (img.size[1] % tileheight) == 0

    cols = img.size[0] // 8
    if cols > 32:
        cols = 16
    rows = img.size[1] // tileheight
    result = bytearray(rows * cols * tileheight * 2)
    index = 0
    for ty in range(rows):
        for tx in range(cols):
            for y in range(tileheight):
                a = 0
                b = 0
                for x in range(8):
                    c = remap[img.getpixel((tx * 8 + x, ty * tileheight + y)) & 3]
                    if c & 1:
                        a |= 0x80 >> x
                    if c & 2:
                        b |= 0x80 >> x
                result[index] = a
                result[index+1] = b
                index += 2
    if len(result) > 8 and struct.unpack("<I", result[:4])[0] == 0xDEADCA7E:
        result = result[:1024]
        header_size = struct.unpack("<I", result[4:8])[0]
        info_list = json.loads(zlib.decompress(result[8:8+header_size]))
        bx, by = 0, 32
        max_width = 16
        for info in info_list:
            size = info["size"]
            width, height = 16, math.ceil(size // 32 / 16)
            if info["type"] in {"photo", "bg"}:
                width, height = 20, 9
                size = width * height * 32
            if by + height * 16 > img.size[1]:
                bx += max_width * 8
                by = 0
                max_width = 16
            max_width = max(max_width, width)
            block = bytearray(width * height * 32)
            index = 0
            colormap = [0, 1, 2, 3]
            if "colormap" in info:
                for n in range(4):
                    colormap[n] = (info["colormap"] >> (n * 4)) & 0x0F
            for ty in range(height):
                for tx in range(width):
                    for y in range(tileheight):
                        a = 0
                        b = 0
                        for x in range(8):
                            c = colormap[remap[img.getpixel((bx + tx * 8 + x, by + ty * tileheight + y)) & 3]]
                            if c & 1:
                                a |= 0x80 >> x
                            if c & 2:
                                b |= 0x80 >> x
                        block[index] = a
                        block[index + 1] = b
                        index += 2
            if info["type"] == "sprite":
                pass
            elif info["type"] in {"tile", "photo", "bg"}:
                if info["type"] == "tile":
                    width = min(width, info["size"] // 0x20)
                for row in range(height):
                    a = b''
                    b = b''
                    for x in range(width):
                        a += block[(row * width + x) * 32:(row * width + x) * 32 + 16]
                        b += block[(row * width + x) * 32 + 16:(row * width + x) * 32 + 32]
                    block[row * width * 32:row * width * 32 + width * 16] = a
                    block[row * width * 32 + width * 16:row * width * 32 + width * 32] = b
            elif info["type"] == "tile4":
                for tile_nr in range(len(block) // 64):
                    block[tile_nr*64+16:tile_nr*64+32], block[tile_nr*64+32:tile_nr*64+48] = block[tile_nr*64+32:tile_nr*64+48], block[tile_nr*64+16:tile_nr*64+32]
            else:
                print(info["type"])
            result += block[:size]
            by += height * 16
    return result


def patchGraphics(rom, graphics_data):
    header_id, size = struct.unpack("<II", graphics_data[:8])
    if header_id in {0xDEADBEEF, 0xDEADCA7E} and size < 1024:
        header = graphics_data[8:8+size]
        graphics_data = graphics_data[1024:]
        if header_id == 0xDEADCA7E:
            header = zlib.decompress(header)
        print(header)
        for info in json.loads(header):
            if info.get("type") in {"photo", "bg"}:
                input_tiles = graphics_data[:18*20*16]
                graphics_data = graphics_data[18*20*16:]
                block = bytearray(info["size"])
                tile_map = bytearray()
                tile_lookup = {}
                available_tiles = list(range(len(block) // 16))
                if info.get("bg") in {0x15}:    # Ensure the textbox works properly during the mural
                    available_tiles.remove(126)
                    tile_lookup[bytes([0xFF] * 16)] = 126
                for y in range(18):
                    for x in range(20):
                        tile = bytes(input_tiles[(x+y*20)*16:(x+y*20)*16+16])
                        if tile not in tile_lookup:
                            tile_lookup[tile] = available_tiles.pop(0)
                        tile_map.append(tile_lookup[tile])
                for tile, index in tile_lookup.items():
                    block[index*16:index*16+16] = tile
                if info.get("type") == "photo":
                    rom.banks[info["tilemap"] >> 14][info["tilemap"] & 0x3FFF:(info["tilemap"] & 0x3FFF) + len(tile_map)] = tile_map
                    photo_index = (info["tilemap"] - (0x28 * 0x4000 + 0x1550)) // 720
                    addr = rom.banks[0x3D][0x2534 + photo_index * 2:0x2534 + photo_index * 2 + 2]
                    addr = addr[0] | (addr[1] << 8)
                    if addr != 0 and photo_index not in {4, 10}:
                        rom.banks[0x3D][addr-0x4000:addr-0x4000+len(tile_map)] = tile_map
                if info.get("type") == "bg":
                    be = BackgroundEditor(rom, info["bg"])
                    for y in range(18):
                        for x in range(20):
                            be.tiles[0x9800 + x + y * 32] = tile_map[x + y * 20]
                    be.store(rom)
                assert len(block) <= info["size"], f"{info['type']}:{info.get('bg')} too complex and does not fit. Need more duplicate tiles"
            else:
                block = graphics_data[:info["size"]]
                graphics_data = graphics_data[info["size"]:]
            updateGraphics(rom, info["addr"] // 0x4000, info["addr"] & 0x3FFF, block)
            if info.get("patch") == "extlink":
                enableExtendedLinkSprites(rom)
            if info.get("patch") == "pinkbatman":
                for n in range(16):
                    rom.banks[0x19][0x0FDC + n * 2] |= 6
                rom.banks[0x21][0x0824] = 0x1B
    else:
        # Old style graphics, just fixed bin at 0x2C
        updateGraphics(rom, 0x2C, 0, graphics_data)
    if rom.banks[0x35][0x1A00:0x1A10] != b'\x00\x00\x42\x42\x24\x24\x18\x18\x18\x18\x24\x24\x42\x42\x00\x00':
        # Extra color dungeon guardian sprites
        rom.patch(0x36, 0x1AAC,
                  "40024202422240224A2248224E224C2248024A024C024E02",
                  "50025202522250225A2258225E225C2258025A025C025E02")


def updateGraphics(rom, bank, offset, data):
    if offset + len(data) > 0x4000:
        updateGraphics(rom, bank, offset, data[:0x4000-offset])
        updateGraphics(rom, bank + 1, 0, data[0x4000 - offset:])
    else:
        rom.banks[bank][offset:offset+len(data)] = data
        if 0x20 <= bank < 0x34 and bank != 0x2C:
            rom.banks[bank-0x20][offset:offset + len(data)] = data


def gfxMod(rom, filename):
    if os.path.exists(filename + ".names"):
        for line in open(filename + ".names", "rt"):
            if ":" in line:
                k, v = line.strip().split(":", 1)
                setReplacementName(k, v)

    ext = os.path.splitext(filename)[1].lower()
    if ext == ".bin":
        patchGraphics(rom, open(filename, "rb").read())
    elif ext in (".png", ".bmp"):
        patchGraphics(rom, imageTo2bpp(filename, colormap=[0x800080, 0x000000, 0x808080, 0xFFFFFF]))
    elif ext == ".json":
        import json
        data = json.load(open(filename, "rt"))

        for patch in data:
            if "gfx" in patch:
                updateGraphics(rom, int(patch["bank"], 16), int(patch["offset"], 16), imageTo2bpp(os.path.join(os.path.dirname(filename), patch["gfx"])))
            if "name" in patch:
                setReplacementName(patch["item"], patch["name"])
    else:
        patchGraphics(rom, imageTo2bpp(filename))
    if rom.banks[0x2C][0x0C90:0x0CA0] != b'\xFF' * 0x10:    # Replacement inventory screen split instead of the two diacritics tiles
        be = BackgroundEditor(rom, 0x02)
        be.tiles[0x9C48] = 0xC8
        for n in range(15):
            be.tiles[0x9C68 + n * 0x20] = 0xC9
        be.store(rom)


def createGfxImage(rom, filename):
    import PIL.Image
    info_list = [
        {"addr": 0x2C * 0x4000 + 0x0000, "size": 0x0400, "type": "sprite"},
        {"addr": 0x2C * 0x4000 + 0x0400, "size": 0x0900, "type": "sprite", "colormap": 0x1230},
        {"addr": 0x2C * 0x4000 + 0x0D00, "size": 0x0200, "type": "tile", "colormap": 0x0132},
        {"addr": 0x2C * 0x4000 + 0x0F00, "size": 0x00C0, "type": "sprite", "colormap": 0x0132},
        {"addr": 0x2C * 0x4000 + 0x0FC0, "size": 0x0040, "type": "tile", "colormap": 0x0132},
        {"addr": 0x2C * 0x4000 + 0x1000, "size": 0x0200, "type": "sprite", "colormap": 0x0132},
        {"addr": 0x2C * 0x4000 + 0x1200, "size": 0x0600, "type": "tile", "colormap": 0x0132},
        #{"addr": 0x2C * 0x4000 + 0x1800, "size": 0x1000, "type": "sprite"}, # Link sprites
        {"addr": 0x0C * 0x4000 + 0x1800, "size": 0x80 * 0x40, "type": "sprite", "patch": "extlink"},
        {"addr": 0x2C * 0x4000 + 0x2800, "size": 0x00C0, "type": "tile4", "colormap": 0x1230},
        {"addr": 0x2C * 0x4000 + 0x28C0, "size": 0x0140, "type": "sprite"},
        {"addr": 0x2C * 0x4000 + 0x2A00, "size": 0x1600, "type": "tile4", "colormap": 0x0132},
        {"addr": 0x2D * 0x4000 + 0x0000, "size": 0x0200, "type": "tile4", "colormap": 0x0132},
        {"addr": 0x2D * 0x4000 + 0x0200, "size": 0x0400, "type": "tile", "colormap": 0x0132},
        {"addr": 0x2D * 0x4000 + 0x0600, "size": 0x3A00, "type": "tile4", "colormap": 0x0132},
        {"addr": 0x2E * 0x4000 + 0x0000, "size": 0x4000, "type": "sprite"},
        {"addr": 0x2F * 0x4000 + 0x0000, "size": 0x4000, "type": "tile", "colormap": 0x0132},
        # bank 30 is background map tiles
        {"addr": 0x31 * 0x4000 + 0x0000, "size": 0x4000, "type": "sprite"},
        {"addr": 0x32 * 0x4000 + 0x0000, "size": 0x4000, "type": "sprite"},
        # bank 33 end cutscene
        {"addr": 0x34 * 0x4000 + 0x0000, "size": 0x2000, "type": "sprite"},
        {"addr": 0x35 * 0x4000 + 0x0000, "size": 0x2000, "type": "sprite"},
        {"addr": 0x35 * 0x4000 + 0x2000, "size": 0x1000, "type": "tile"},
        {"addr": 0x38 * 0x4000 + 0x0000, "size": 0x0400, "type": "sprite"},
        {"addr": 0x3B * 0x4000 + 0x3000, "size": 0x1000, "type": "photo", "tilemap": 0x28 * 0x4000 + 0x1550 + 720 * 0, "colormap": 0x0132},
        {"addr": 0x29 * 0x4000 + 0x0000, "size": 0x1000, "type": "photo", "tilemap": 0x28 * 0x4000 + 0x1550 + 720 * 1, "colormap": 0x0132},
        {"addr": 0x29 * 0x4000 + 0x1000, "size": 0x1000, "type": "photo", "tilemap": 0x28 * 0x4000 + 0x1550 + 720 * 2, "colormap": 0x0132},
        {"addr": 0x29 * 0x4000 + 0x2000, "size": 0x1000, "type": "photo", "tilemap": 0x28 * 0x4000 + 0x1550 + 720 * 3, "colormap": 0x0132},
        {"addr": 0x29 * 0x4000 + 0x3000, "size": 0x1000, "type": "photo", "tilemap": 0x28 * 0x4000 + 0x1550 + 720 * 4, "colormap": 0x0132},
        {"addr": 0x2A * 0x4000 + 0x0000, "size": 0x1000, "type": "photo", "tilemap": 0x28 * 0x4000 + 0x1550 + 720 * 5, "colormap": 0x0132},
        {"addr": 0x2A * 0x4000 + 0x1000, "size": 0x1000, "type": "photo", "tilemap": 0x28 * 0x4000 + 0x1550 + 720 * 6, "colormap": 0x0132},
        {"addr": 0x2A * 0x4000 + 0x2000, "size": 0x1000, "type": "photo", "tilemap": 0x28 * 0x4000 + 0x1550 + 720 * 7, "colormap": 0x0132},
        {"addr": 0x2A * 0x4000 + 0x3000, "size": 0x1000, "type": "photo", "tilemap": 0x28 * 0x4000 + 0x1550 + 720 * 8, "colormap": 0x0132},
        {"addr": 0x2B * 0x4000 + 0x0000, "size": 0x1000, "type": "photo", "tilemap": 0x28 * 0x4000 + 0x1550 + 720 * 9, "colormap": 0x0132},
        {"addr": 0x2B * 0x4000 + 0x1000, "size": 0x1000, "type": "photo", "tilemap": 0x28 * 0x4000 + 0x1550 + 720 * 10, "colormap": 0x0132},
        {"addr": 0x2B * 0x4000 + 0x2000, "size": 0x1000, "type": "photo", "tilemap": 0x28 * 0x4000 + 0x1550 + 720 * 11, "colormap": 0x0132},
        {"addr": 0x2B * 0x4000 + 0x3000, "size": 0x1000, "type": "photo", "tilemap": 0x28 * 0x4000 + 0x1550 + 720 * 12, "colormap": 0x0132},
        {"addr": 0x30 * 0x4000 + 0x1800, "size": 0x0800, "type": "bg", "bg": 0x12, "colormap": 0x0132},  # Peach
        {"addr": 0x30 * 0x4000 + 0x2700, "size": 0x0200, "type": "sprite"},
        {"addr": 0x30 * 0x4000 + 0x3000, "size": 0x0800, "type": "bg", "bg": 0x15, "colormap": 0x0132},  # Mural
        {"addr": 0x30 * 0x4000 + 0x3800, "size": 0x0800, "type": "bg", "bg": 0x23, "colormap": 0x0132},  # Painting
        # {"addr": 0x33 * 0x4000 + 0x1000, "size": 0x0800, "type": "photo", "tilemap": 0x17 * 0x4000 + 0x0EEF},  # Windfish, tilemap is BG commands encoded...
    ]
    infoblock = zlib.compress(json.dumps(info_list, separators=(',', ':')).encode('ascii'))
    infoblock = struct.pack("<II", 0xDEADCA7E, len(infoblock)) + infoblock
    print(f"Info block len: {len(infoblock)}")
    assert len(infoblock) < 1024, f"{len(infoblock)} > 1024"
    blocks = [(infoblock + bytes(1024 - len(infoblock)), {"type": "info"})]

    def reversebits(n):
        n = ((n & 0x55) << 1) | ((n & 0xAA) >> 1)
        n = ((n & 0x33) << 2) | ((n & 0xCC) >> 2)
        n = ((n & 0x0F) << 4) | ((n & 0xF0) >> 4)
        return n

    if rom.banks[0x3F][0x0000] != 0:  # LADXR Rom with bank 3F, so grab the ocarina and feather sprites from there.
        rom.banks[0x2C][0x0900:0x0940] = rom.banks[0x3F][0x3000:0x3040]

    for info in info_list:
        data_block = bytearray()
        if info.get("patch") == "extlink" and rom.banks[0x0C][0x37C0:0x3800] != bytes(0x40):
            for n in range(0x80):
                idx1 = rom.banks[0x20][0x1319 + n * 2]
                attr1 = rom.banks[0x20][0x1407 + n * 2]
                idx2 = rom.banks[0x20][0x131A + n * 2]
                attr2 = rom.banks[0x20][0x1408 + n * 2]
                sprite1 = rom.banks[0x2C][0x1800 + idx1 * 16:0x1800 + idx1 * 16 + 32]
                sprite2 = rom.banks[0x2C][0x1800 + idx2 * 16:0x1800 + idx2 * 16 + 32]
                if attr1 & 0x20:
                    sprite1 = bytes(reversebits(b) for b in sprite1)
                if attr1 & 0x40:
                    sprite1 = b''.join(sprite1[30-n*2:32-n*2] for n in range(16))
                if attr2 & 0x20:
                    sprite2 = bytes(reversebits(b) for b in sprite2)
                if attr2 & 0x40:
                    sprite2 = b''.join(sprite2[30-n*2:32-n*2] for n in range(16))
                if n in {0x02, 0x03, 0x08, 0x09, 0x0C, 0x0D, 0x5A, 0x5D} or n > 0x76:
                    sprite1 = bytes(32)
                    sprite2 = bytes(32)
                if n == 0x78:  # Magic rod attack
                    sprite1 = rom.banks[0x2C][0x0040:0x0060]
                    sprite2 = rom.banks[0x2C][0x0060:0x0080]
                if n == 0x79:  # Magic rod attack/capacity upgrade
                    sprite1 = rom.banks[0x2C][0x0080:0x00A0]
                    sprite2 = extragfx.capacityUpgradeIcon() * 2
                if n == 0x7A:  # Song gfx 1/2
                    sprite1 = extragfx.songItemGraphics()[:0x20]
                    sprite2 = extragfx.songItemGraphics()[0x20:0x40]
                if n == 0x7B:  # Song gfx 3/bingo
                    sprite1 = extragfx.songItemGraphics()[0x40:]
                    sprite2 = extragfx.bingoBoard(rom)[:0x20]
                if n == 0x7C:  # Bingo
                    sprite1 = extragfx.bingoBoard(rom)[0x20:0x40]
                    sprite2 = extragfx.bingoBoard(rom)[0x40:0x60]
                if n == 0x7D:  # Bingo
                    sprite1 = extragfx.bingoBoard(rom)[0x60:]
                data_block += sprite1 + sprite2
        elif info.get("type") == "photo":
            tiles = rom.banks[info["addr"] >> 14][info["addr"] & 0x3FFF:]
            tilemap = rom.banks[info["tilemap"] >> 14][info["tilemap"] & 0x3FFF:]
            for y in range(0, 18, 2):
                for x in range(20):
                    for ty in range(2):
                        tile_nr = tilemap[x+(y+ty)*20]
                        data_block += tiles[tile_nr*0x10:tile_nr*0x10+0x10]
        elif info.get("type") == "bg":
            tiles = rom.banks[info["addr"] >> 14][info["addr"] & 0x3FFF:]
            be = BackgroundEditor(rom, info["bg"])
            for y in range(0, 18, 2):
                for x in range(20):
                    for ty in range(2):
                        tile_nr = be.tiles[0x9800+x+(y+ty)*32]
                        data_block += tiles[tile_nr*0x10:tile_nr*0x10+0x10]
        else:
            start = info["addr"]
            end = info["addr"] + info["size"]
            while start < end:
                bank = start >> 14
                addr = start & 0x3FFF
                length = min(end - start, 0x4000 - addr)
                print(f"{bank:02x}:{addr:04x}:{length:04x} {info['type']}")
                data_block += rom.banks[bank][addr:addr+length]
                start += length
            if info["type"] == "tile": # rearrange 8x16 into 8x8
                a = b''
                offset = min(16, len(data_block) // 32)
                for row in range(math.ceil(len(data_block) / 512)):
                    for n in range(min(16, len(data_block) // 32)):
                        a += data_block[n*16:(n+1)*16] + data_block[(n+offset)*16:(n+offset+1)*16]
                    data_block = data_block[512:]
                data_block = a
            if info["type"] == "tile4": # rearrange 2x2 tiles from col/row to row/col
                a = b''
                for n in range(0, len(data_block), 64):
                    a += data_block[n:n+16]
                    a += data_block[n+32:n+32+16]
                    a += data_block[n+16:n+16+16]
                    a += data_block[n+48:n+48+16]
                data_block = a
        data_block += bytes((0x200 - (len(data_block) % 0x200)) % 0x200)
        blocks.append((data_block, info))

    def arrange_blocks(max_height):
        col_height = 0
        col_width = 16
        cols = []
        for block, info in blocks:
            width = 20 if info["type"] in {"photo", "bg"} else 16
            height = math.ceil(len(block) // 32 / width)
            if height + col_height > max_height:
                cols.append((col_width, col_height))
                col_width = 16
                col_height = 0
            col_width = max(col_width, width)
            col_height += height
        cols.append((col_width, col_height))
        return cols
    max_h = 10000
    best_d = 10000
    best_cols = None
    for n in range(100):
        cols = arrange_blocks(max_h - 1)
        total_w = sum(w for w, h in cols) / 4
        max_h = max(h for w, h in cols)
        diagonal = math.sqrt(total_w * total_w + max_h * max_h)
        if diagonal < best_d:
            best_d = diagonal
            best_cols = cols
    assert best_cols is not None
    total_w = sum(w for w, h in best_cols)
    max_h = max(h for w, h in best_cols)
    print(best_cols)

    img = PIL.Image.new("P", (total_w * 8, max_h * 16))
    img.putpalette((
        128, 0, 128,
        0, 0, 0,
        128, 128, 128,
        255, 255, 255,
    ))
    ox = 0
    oy = 0
    max_w = 16
    for block, info in blocks:
        width = 20 if info["type"] in {"photo", "bg"} else 16
        height = len(block) // 32 // width
        if oy + height > max_h:
            oy = 0
            ox += max_w
            max_w = 16
        max_w = max(max_w, width)
        colormap = [0, 1, 2, 3]
        if "colormap" in info:
            for n in range(4):
                colormap[(info["colormap"] >> (n * 4)) & 0x0F] = n
        for ty in range(height):
            for tx in range(width):
                for y in range(16):
                    a = block[tx * 32 + ty * 32 * width + y * 2]
                    b = block[tx * 32 + ty * 32 * width + y * 2 + 1]
                    for x in range(8):
                        c = 0
                        if a & (0x80 >> x):
                            c |= 1
                        if b & (0x80 >> x):
                            c |= 2
                        img.putpixel((ox*8+tx*8+x, oy*16+y), colormap[c])
            oy += 1
    img.save(filename)


def noSwordMusic(rom):
    # Skip no-sword music override
    # Instead of loading the sword level, we put the value 1 in the A register, indicating we have a sword.
    rom.patch(2, 0x0151, ASM("ld a, [wSwordLevel]"), ASM("ld a, $01"), fill_nop=True)
    rom.patch(2, 0x3AEF, ASM("ld a, [wSwordLevel]"), ASM("ld a, $01"), fill_nop=True)
    rom.patch(3, 0x0996, ASM("ld a, [wSwordLevel]"), ASM("ld a, $01"), fill_nop=True)
    rom.patch(3, 0x0B35, ASM("ld a, [wShieldLevel]"), ASM("ld a, $01"), fill_nop=True)


def removeNagMessages(rom):
    # Remove "this object is heavy, bla bla", and other nag messages when touching an object
    rom.patch(0x02, 0x32BB, ASM("ld a, [$C14A]"), ASM("ld a, $01"), fill_nop=True)  # crystal blocks
    rom.patch(0x02, 0x32EC, ASM("ld a, [$C5A6]"), ASM("ld a, $01"), fill_nop=True) # cracked blocks
    rom.patch(0x02, 0x32D3, ASM("jr nz, $25"), ASM("jr $25"), fill_nop=True)  # stones/pots
    rom.patch(0x02, 0x2B88, ASM("jr nz, $0F"), ASM("jr $0F"), fill_nop=True)  # ice blocks


def removeLowHPBeep(rom):
    rom.patch(2,  0x233A, ASM("ld hl, hWaveSfx\nld [hl], $04"), b"", fill_nop=True) # Remove health beep


def slowLowHPBeep(rom):
    rom.patch(2, 0x2338, ASM("ld a, $30"), ASM("ld a, $60"))  # slow slow hp beep


def removeFlashingLights(rom):
    # Remove the switching between two backgrounds at mamu, always show the spotlights.
    rom.patch(0x00, 0x01EB, ASM("ldh a, [hFrameCounter]\nrrca\nand $80"), ASM("ld a, $80"), fill_nop=True)
    # Remove flashing colors from shopkeeper killing you after stealing and the mad batter giving items.
    rom.patch(0x24, 0x3B77, ASM("push bc"), ASM("ret"))


def forceLinksPalette(rom, index):
    # This forces the link sprite into a specific palette index ignoring the tunic options.
    rom.patch(0, 0x1D8C,
            ASM("ld a, [$DC0F]\nand a\njr z, $03\ninc a"),
            ASM("ld a, $%02X" % (index)), fill_nop=True)
    rom.patch(0, 0x1DD2,
            ASM("ld a, [$DC0F]\nand a\njr z, $03\ninc a"),
            ASM("ld a, $%02X" % (index)), fill_nop=True)
    # Fix the waking up from bed palette
    if index == 1:
        rom.patch(0x21, 0x33FC, "A222", "FF05")
    elif index == 2:
        rom.patch(0x21, 0x33FC, "A222", "3F14")
    elif index == 3:
        rom.patch(0x21, 0x33FC, "A222", "037E")
    for n in range(6):
        rom.patch(0x05, 0x1261 + n * 2, "00", f"{index:02x}")
    # Fix entering dream bed
    rom.patch(0x21, 0x0228, 0x0238, ASM(f"ld hl, 5518 + 4 + {index*8}"), fill_nop=True)
    rom.patch(0x15, 0x3D50 + 5, "00", f"{index:02x}")
    rom.patch(0x15, 0x3D50 + 7, "00", f"{index:02x}")
    rom.patch(0x15, 0x3D58 + 5, "02", f"{index:02x}")
    rom.patch(0x15, 0x3D58 + 7, "02", f"{index:02x}")
    rom.patch(0x15, 0x3D60 + 5, "03", f"{index:02x}")
    rom.patch(0x15, 0x3D60 + 7, "03", f"{index:02x}")


def fastText(rom):
    rom.patch(0x00, 0x24CA, ASM("jp $2485"), ASM("call $2485"))


def noText(rom):
    for idx in range(len(rom.texts)):
        if not isinstance(rom.texts[idx], int) and (idx < 0x217 or idx > 0x21A):
            rom.texts[idx] = rom.texts[idx][-1:]

def getMarinStartingText(rnd: random.Random):
    lines = open(os.path.join(os.path.dirname(__file__), "marin.txt"), "rb").readlines()
    while lines[-1].strip() == b'':
        lines.pop(-1)
    
    # generate random numbers
    # [1;101[, so [1;100]
    
    line = rnd.choice(lines).strip().decode("unicode_escape")\
        .replace('<marinLinesAmount>', str(len(lines)))
    line = re.sub(r'<rnd(?:(-?\d+),)?(-?\d+)>', lambda m: randomNumber(int(m.group(1)) if m.group(1) != None else 1, int(m.group(2))+1, rnd), line)
    line = re.sub(r'<ord(?:(-?\d+),)?(-?\d+)>', lambda m: randomOrdinal(int(m.group(1)) if m.group(1) != None else 1, int(m.group(2))+1, rnd), line)

    return formatText(line)

def reduceMessageLengths(rom, rnd):
    # Into text from Marin. Got to go fast, so less text. (This intro text is very long)
    rom.texts[0x01] = getMarinStartingText(rnd)

    # Reduce length of a bunch of common texts
    rom.texts[0xEA] = formatText("You've got a Guardian Acorn!")
    rom.texts[0xEB] = rom.texts[0xEA]
    rom.texts[0xEC] = rom.texts[0xEA]
    rom.texts[0x08] = formatText("You got a Piece of Power!")
    rom.texts[0xEF] = formatText("You found a {SEASHELL}!")
    rom.texts[0xA7] = formatText("You've got the {COMPASS}!")

    rom.texts[0x07] = formatText("You need the {NIGHTMARE_KEY}!")
    rom.texts[0x8C] = formatText("You need a {KEY}!")  # keyhole block

    rom.texts[0x09] = formatText("Ahhh... It has  the Sleepy {TOADSTOOL}, it does! We'll mix it up something in a jiffy, we will!")
    rom.texts[0x0A] = formatText("The last thing I kin remember was bitin' into a big juicy {TOADSTOOL}... Then, I had the darndest dream... I was a raccoon! Yeah, sounds strange, but it sure was fun!")
    rom.texts[0x0F] = formatText("You pick the {TOADSTOOL}... As you hold it over your head, a mellow aroma flows into your nostrils.")
    rom.texts[0x13] = formatText("You've learned the ^{SONG1}!^ This song will always remain in your heart!")
    rom.texts[0x18] = formatText("Will you give me 28 {RUPEES} for my secret?", ask="Give Don't")
    rom.texts[0x19] = formatText("How about it? 42 {RUPEES} for my little secret...", ask="Give Don't")
    rom.texts[0x1e] = formatText("...You're so cute! I'll give you a 7 {RUPEE} discount!")
    rom.texts[0x2d] = formatText("{ARROWS_10}\n10 {RUPEES}!", ask="Buy  Don't")
    rom.texts[0x32] = formatText("{SHIELD}\n20 {RUPEES}!", ask="Buy  Don't")
    rom.texts[0x33] = formatText("Ten {BOMB}\n10 {RUPEES}", ask="Buy  Don't")
    rom.texts[0x3d] = formatText("It's a {SHIELD}! There is space for your name!")
    rom.texts[0x42] = formatText("It's 30 {RUPEES}! You can play the game three more times with this!")
    rom.texts[0x44] = formatText("You got a {TRADING_ITEM_YOSHI_DOLL}! Recently, he seems to be showing up in many games!")
    rom.texts[0x45] = formatText("How about some fishing, little buddy? I'll only charge you 10 {RUPEES}...", ask="Fish Not Now")
    rom.texts[0x4b] = formatText("Wow! Nice Fish! It's a lunker!! I'll give you a 20 {RUPEE} prize! Try again?", ask="Cast Not Now")
    rom.texts[0x4e] = formatText("You're short of {RUPEES}? Don't worry about it. You just come back when you have more money, little buddy.")
    rom.texts[0x4f] = formatText("You've got a {HEART_PIECE}! Press SELECT on the Subscreen to see.")
    rom.texts[0x8e] = formatText("Well, it's an {OCARINA}, but you don't know how  to play it...")
    rom.texts[0x90] = formatText("You found the {POWER_BRACELET}! At last, you can pick up pots and stones!")
    rom.texts[0x91] = formatText("You got your {SHIELD} back! Press the button and repel enemies with it!")
    rom.texts[0x93] = formatText("You've got the {HOOKSHOT}! Its chain stretches long when you use it!")
    rom.texts[0x94] = formatText("You've got the {MAGIC_ROD}! Now you can burn things! Burn it! Burn, baby burn!")
    rom.texts[0x95] = formatText("You've got the {PEGASUS_BOOTS}! If you hold down the Button, you can dash!")
    rom.texts[0x96] = formatText("You've got the {OCARINA}! You should learn to play many songs!")
    rom.texts[0x97] = formatText("You've got the {FEATHER}! It feels like your body is a  lot lighter!")
    rom.texts[0x98] = formatText("You've got a {SHOVEL}! Now you can feel the joy of digging!")
    rom.texts[0x99] = formatText("You've got some {MAGIC_POWDER}! Try sprinkling it on a variety of things!")
    rom.texts[0x9b] = formatText("You found your {SWORD}!  It must be yours because it has your name engraved on it!")
    rom.texts[0x9c] = formatText("You've got the {FLIPPERS}! If you press the B Button while you swim, you can dive underwater!")
    rom.texts[0x9d] = formatText("You've got the {TRADING_ITEM_MAGNIFYING_GLASS}! This will reveal many things you couldn't see before!")
    rom.texts[0x9e] = formatText("You've got a new {SWORD}! You should put your name on it right away!")
    rom.texts[0x9f] = formatText("You've got a new {SWORD}! You should put your name on it right away!")
    rom.texts[0xa0] = formatText("You found the {MEDICINE}! You should apply this and see what happens!")
    rom.texts[0xa1] = formatText("You've got the {TAIL_KEY}! Now you can open the Tail Cave gate!")
    rom.texts[0xa2] = formatText("You've got the {SLIME_KEY}! Now you can open the gate in Ukuku Prairie!")
    rom.texts[0xa3] = formatText("You've got the {ANGLER_KEY}!")
    rom.texts[0xa4] = formatText("You've got the {FACE_KEY}!")
    rom.texts[0xa5] = formatText("You've got the {BIRD_KEY}!")
    rom.texts[0xa6] = formatText("At last, you got a {MAP}! Press the START Button to look at it!")
    rom.texts[0xa8] = formatText("You found a {STONE_BEAK}! Let's find the owl statue that belongs to it.")
    rom.texts[0xa9] = formatText("You've got the {NIGHTMARE_KEY}! Now you can open the door to the Nightmare's Lair!")
    rom.texts[0xaa] = formatText("You got a {KEY}! You can open a locked door.")
    rom.texts[0xab] = formatText("You got 20 {RUPEES}! JOY!", center=True)
    rom.texts[0xac] = formatText("You got 50 {RUPEES}! Very Nice!", center=True)
    rom.texts[0xad] = formatText("You got 100 {RUPEES}! You're Happy!", center=True)
    rom.texts[0xae] = formatText("You got 200 {RUPEES}! You're Ecstatic!", center=True)
    rom.texts[0xdc] = formatText("Ribbit! Ribbit! I'm Mamu, on vocals! But I don't need to tell you that, do I? Everybody knows me! Want to hang out and listen to us jam? For 300 {RUPEES}, we'll let you listen to a previously unreleased cut! What do you do?", ask="Pay Leave")
    rom.texts[0xe8] = formatText("You've found a {GOLD_LEAF}! Press START to see how many you've collected!")
    rom.texts[0xed] = formatText("You've got the Mirror {SHIELD}! You can now turn back the beams you couldn't block before!")
    rom.texts[0xee] = formatText("You've got a more Powerful {POWER_BRACELET}! Now you can almost lift a whale!")
    rom.texts[0xf0] = formatText("Want to go on a raft ride for a hundred {RUPEES}?", ask="Yes No Way")


def enableExtendedLinkSprites(rom):
    # Instead of loading flipped sprites from a lookup table (bank20) in graphics bank 2C,
    # Load the graphics from bank 0C and index directly by hLinkAnimationState
    rom.patch(0x20, 0x14FA, 0x155F, ASM("""
    ; Convert hLinkAnimationState into a tile number offset
    ld   b, a
    ld   c, 0
    srl  b
    rr   c
    srl  b
    rr   c
    ld   hl, $5800
    add  hl, bc
    ld   c, l
    ld   b, h
    ld   hl, $8000
    ld   d, $40
    call $1D0A ; CopyLinkTilesPair
    ret
    """), fill_nop=True)
    rom.patch(0x00, 0x1D0C, ASM("call $0B0B"), "", fill_nop=True)
    rom.patch(0x00, 0x1DE5, ASM("ld [hl], $23"), ASM("ld [hl], $03"))  # Fix the diving sprite


def allowOverworldBackgroundTileTransitions(rom):
    rom.patch(0x00, 0x0656, 0x069E, ASM("""
    ld   a, $2F
    ld   [$2100], a
    ld   hl, wTransitionZeroNeverUsed
    ld   a, [hl]
    xor  $01
    ld   [hl], a
    ldh  [rVBK], a
    ; run HDMA for copy
    ld   hl, rHDMA1
    ldh  a, [hWorldTileset]
    ; source address
    add  a, $40
    ld   [hl+], a
    xor  a
    ld   [hl+], a
    ; target address
    ld   a, $90
    ld   [hl+], a
    xor  a
    ld   [hl+], a
    ; amount of tiles, and start
    ld   a, 31
    ld   [hl], a
    
    ; Mark loading as done
    xor  a
    ldh  [rVBK], a
    ldh  [hBGTilesLoadingStage], a
    ldh  [hNeedsUpdatingBGTiles], a
    ;ret

    nop
    jp  $078E
    
LoadBaseOverworldTilesImpl:
    ld   a, $2C
    ld   [$2100], a
    ld   hl, $5200
    ld   de, $9200
    ld   bc, $600
    call CopyData
    ld   hl, $4F00
    ld   de, $8F00
    ld   bc, $100
    jp   CopyData
"""))
    rom.patch(0x00, 0x2D2D, 0x2D3E, ASM("""
    call $0681
    ld   a, $01
    ldh  [rVBK], a
    call $0681
    xor  a
    ldh  [rVBK], a
"""), fill_nop=True)

    rom.patch(0x00, 0x074C, "00" * 27, ASM("""
CopyObjectRowToBGAttr:
    ld   a, [wTransitionZeroNeverUsed]
    and  a
    jp   z, $2214 ; normal handler 

    ld   a, [wBGUpdateRegionOriginLow]
    and  $20
    jr   z, .lowerPartEnd
    inc  hl
    inc  hl
.lowerPartEnd:
    ld   a, [hl+]
    or   $08
    ld   [bc], a
    inc  bc
    ld   a, [hl]
    or   $08
    ld   [bc], a
    inc  bc
    ret
"""))
    rom.patch(0x00, 0x0767, "00" * 27, ASM("""
CopyObjectColumnToBGAttr:
    ld   a, [wTransitionZeroNeverUsed]
    and  a
    jp   z, $2224 ; normal handler 
    ld   a, [wBGUpdateRegionOriginLow]
    and  $01
    jr   z, .rightHandEnd
    inc  hl
.rightHandEnd:
    ld   a, [hl+]
    or   $08
    ld   [bc], a
    inc  hl
    inc  bc
    ld   a, [hl]
    or   $08
    ld   [bc], a
    inc  bc
    ret
"""))
    rom.patch(0x00, 0x22BD, ASM("call $2214"), ASM("call $074C"))
    rom.patch(0x00, 0x22EA, ASM("call $2224"), ASM("call $0767"))
    rom.patch(0x00, 0x0782, "00" * 12, ASM("""
        ld   a, [wTransitionZeroNeverUsed]
        ldh  [rVBK], a
        call CopyData
        xor  a
        ldh  [rVBK], a
        ret
    """))
    rom.patch(0x00, 0x078E, "00" * 11, ASM("""
        xor  a
        ldh  [hAnimatedTilesFrameCount], a
        ld   a, $2C
        ld   [$2100], a
        jp   $1BD2
    """))
    rom.patch(0x00, 0x1C57, ASM("call CopyData"), ASM("call $0782"))
    rom.patch(0x02, 0x3BFA, ASM("ld [wTransitionZeroNeverUsed], a"), "", fill_nop=True)

def allowColorDungeonSpritesEverywhere(rom):
    # Set sprite set numbers $01-$40 to map to the color dungeon sprites
    rom.patch(0x00, 0x2E6F, "00", "15")
    # Patch the spriteset loading code to load the 4 entries from the normal table instead of skipping this for color dungeon specific exception weirdness
    rom.patch(0x00, 0x0DA4, ASM("jr nc, $05"), ASM("jr nc, $41"))
    rom.patch(0x00, 0x0DE5, ASM("""
        ldh  a, [hMapId]
        cp   $FF
        jr   nz, $06
        ld a, $01
        ldh [$FF91], a
        jr $40
    """), ASM("""
        jr $0A ; skip over the rest of the code
        cp $FF ; check if color dungeon
        jp nz, $0DAB
        inc d
        jp $0DAA
    """), fill_nop=True)
    # Disable color dungeon specific tile load hacks
    rom.patch(0x00, 0x06A7, ASM("jr nz, $22"), ASM("jr $22"))
    rom.patch(0x00, 0x2E77, ASM("jr nz, $0B"), ASM("jr $0B"))
    
    # Finally fill in the sprite data for the color dungeon
    for n in range(22):
        data = bytearray()
        for m in range(4):
            idx = rom.banks[0x20][0x06AA + 44 * m + n * 2]
            bank = rom.banks[0x20][0x06AA + 44 * m + n * 2 + 1]
            if idx == 0 and bank == 0:
                v = 0xFF
            elif bank == 0x35:
                v = idx - 0x40
            elif bank == 0x31:
                v = idx
            elif bank == 0x2E:
                v = idx + 0x40
            else:
                assert False, "%02x %02x" % (idx, bank)
            data += bytes([v])
        rom.room_sprite_data_indoor[0x200 + n] = data

    # Patch the graphics loading code to use DMA and load all sets that need to be reloaded, not just the first and last
    rom.patch(0x00, 0x06FA, 0x07AF, ASM("""
        ;We enter this code with the right bank selected for tile data copy,
        ;d = tile row (source addr = (d*$100+$4000))
        ;e = $00
        ;$C197 = index of sprite set to update (target addr = ($8400 + $100 * [$C197]))
        ld  a, d
        add a, $40
        ldh [$FF51], a
        xor a
        ldh [$FF52], a
        ldh [$FF54], a
        ld  a, [$C197]
        add a, $84
        ldh [$FF53], a
        ld  a, $0F
        ldh [$FF55], a

        ; See if we need to do anything next
        ld  a, [$C10E] ; check the 2nd update flag
        and a
        jr  nz, getNext
        ldh [$FF91], a ; no 2nd update flag, so clear primary update flag
        ret
    getNext:
        ld  hl, $C197
        inc [hl]
        res 2, [hl]
        ld  a, [$C10D]
        cp  [hl]
        ret nz
        xor a ; clear the 2nd update flag when we prepare to update the last spriteset
        ld  [$C10E], a
        ret
    """), fill_nop=True)
    rom.patch(0x00, 0x0738, "00" * (0x073E - 0x0738), ASM("""
        ; we get here by some color dungeon specific code jumping to this position
        ; We still need that color dungeon specific code as it loads background tiles
        xor a
        ldh [$FF91], a
        ldh [$FF93], a
        ret
    """))
    rom.patch(0x00, 0x073E, "00" * (0x07AF - 0x073E), ASM("""
        ;If we get here, only the 2nd flag is filled and the primary is not. So swap those around.
        ld  a, [$C10D] ;copy the index number
        ld  [$C197], a
        xor a
        ld  [$C10E], a ; clear the 2nd update flag
        inc a
        ldh [$FF91], a ; set the primary update flag
        ret
    """), fill_nop=True)


def updateSpriteData(rom):
    # Change the special sprite change exceptions
    rom.patch(0x00, 0x0DAD, 0x0DDB, ASM("""
    ; Check for indoor
    ld   a, d
    and  a
    jr   nz, noChange

    ldh  a, [hMapRoom]
    cp   $C9
    jr   nz, sirenRoomEnd
    ld   a, [$D8C9] ; wOverworldRoomStatus + ROOM_OW_SIREN
    and  $20
    jr   z, noChange
    ld   hl, $7837
    jp   $0DFE

sirenRoomEnd:
    ldh  a, [hMapRoom]
    cp   $D8
    jr   nz, noChange
    ld   a, [$D8FD] ; wOverworldRoomStatus + ROOM_OW_WALRUS 
    and  $20
    jr   z, noChange
    ld   hl, $783B
    jp   $0DFE

noChange:
    """), fill_nop=True)
    rom.patch(0x20, 0x3837, "A4FF8BFF", "A461FF72")
    rom.patch(0x20, 0x383B, "A44DFFFF", "A4C5FF70")

    # For each room update the sprite load data based on which entities are in there.
    for room_nr in range(0x316):
        if room_nr == 0x2FF:
            continue
        values = [None, None, None, None]
        if room_nr == 0x00E:  # D7 entrance opening
            values[2] = 0xD6
            values[3] = 0xD7
        if 0x211 <= room_nr <= 0x21E:  # D7 throwing ball thing.
            values[0] = 0x66
        r = RoomEditor(rom, room_nr)
        for obj in r.objects:
            if obj.type_id == 0xC5 and room_nr < 0x100: # Pushable Gravestone
                values[3] = 0x82
        for x, y, entity in r.entities:
            sprite_data = entityData.SPRITE_DATA[entity]
            if callable(sprite_data):
                sprite_data = sprite_data(r)
            if sprite_data is None:
                continue
            for m in range(0, len(sprite_data), 2):
                idx, value = sprite_data[m:m+2]
                if values[idx] is None:
                    values[idx] = value
                elif isinstance(values[idx], set) and isinstance(value, set):
                    values[idx] = values[idx].intersection(value)
                    assert len(values[idx]) > 0
                elif isinstance(values[idx], set) and value in values[idx]:
                    values[idx] = value
                elif isinstance(value, set) and values[idx] in value:
                    pass
                elif values[idx] == value:
                    pass
                else:
                    assert False, "Room: %03x cannot load graphics for entity: %02x (Index: %d Failed: %s, Active: %s)" % (room_nr, entity, idx, value, values[idx])

        data = bytearray()
        for v in values:
            if isinstance(v, set):
                v = next(iter(v))
            elif v is None:
                v = 0xff
            data.append(v)

        if room_nr < 0x100:
            rom.room_sprite_data_overworld[room_nr] = data
        else:
            rom.room_sprite_data_indoor[room_nr - 0x100] = data
