import PIL.Image
import struct
import argparse
import patches.aesthetics


def convert_endscreen(input_filename, output_filename):
    img = PIL.Image.open(input_filename).convert("RGBA")
    img = img.convert("P", dither=PIL.Image.FLOYDSTEINBERG, palette=PIL.Image.ADAPTIVE, colors=16)
    pal_values = img.getpalette()
    def pal_diff(a, b):
        return sum(abs(pal_values[a * 3 + n] - pal_values[b * 3 + n]) for n in range(3))
    assert img.size == (160, 144)
    for y in range(18):
        for x in range(20):
            tile = img.crop((x * 8, y * 8, x * 8 + 8, y * 8 + 8))
            while len(tile.getcolors()) > 4:
                replace_color = sorted(tile.getcolors())[0][1]
                target_color = None
                for _, idx in sorted(tile.getcolors())[1:]:
                    if target_color is None or pal_diff(replace_color, idx) < pal_diff(replace_color, target_color):
                        target_color = idx
                tile.putdata(bytes(tile.getdata()).replace(bytes([replace_color]), bytes([target_color])))
                img.paste(tile, (x * 8, y * 8))
    img = img.convert("P")
    pal_counts = [{}, {}, {}, {}]
    for y in range(18):
        for x in range(20):
            tile = img.crop((x * 8, y * 8, x * 8 + 8, y * 8 + 8))
            colors = tile.getcolors()
            pal_key = tuple(sorted(c[1] for c in colors))
            n = len(pal_key) - 1
            pal_counts[n][pal_key] = pal_counts[n].get(pal_key, 0) + sum(c[0] for c in colors)
    pal_mapping = {}
    def find_best_pal_for(search_pal):
        best = None
        for pal, counts in pal_counts[3].items():
            if set(search_pal).issubset(set(pal)):
                if best is None or best[1] < counts:
                    best = (pal, counts)
        if best is None:
            for pal, counts in pal_counts[3].items():
                if len(set(search_pal).intersection(set(pal))) > 1:
                    if best is None or best[1] < counts:
                        best = (pal, counts)
        return best[0]
    def find_worst_pal():
        best = None
        for pal, counts in pal_counts[3].items():
            if best is None or best[1] > counts:
                best = pal, counts
        return best
    def find_best_match(match_pal):
        best_match_count = 0
        options = []
        for pal, counts in pal_counts[3].items():
            match_count = len(set(match_pal).intersection(set(pal)))
            if match_count > best_match_count:
                best_match_count = match_count
                options = []
            if match_count == best_match_count:
                options.append(pal)

        best_diff = None
        for pal in options:
            mismatch1 = tuple(sorted(n for n in set(match_pal).difference(set(pal))))
            mismatch2 = tuple(sorted(n for n in set(pal).difference(set(match_pal))))
            diff = 0
            for a, b in zip(mismatch1, mismatch2):
                diff += pal_diff(a, b)
            if best_diff is None or best_diff[1] > diff:
                best_diff = pal, diff, tuple(zip(mismatch1, mismatch2))
        return best_diff[0], best_diff[2]


    for n in range(3):
        for pal, counts in pal_counts[n].items():
            pal_mapping[pal] = find_best_pal_for(pal), tuple()
            pal_counts[3][pal_mapping[pal][0]] += counts

    while len(pal_counts[3]) > 8:
        pal, counts = find_worst_pal()
        del pal_counts[3][pal]
        replacement = find_best_match(pal)
        pal_mapping[pal] = replacement

    all_tile_data = b''
    all_attr_data = b''
    gb_pal_mapping = {}
    for y in range(18):
        for x in range(20):
            tile = img.crop((x * 8, y * 8, x * 8 + 8, y * 8 + 8))
            pal_key = tuple(sorted(c[1] for c in tile.getcolors()))
            new_pal = pal_key
            while new_pal in pal_mapping:
                new_pal, replacements = pal_mapping[new_pal]
                if replacements:
                    data = bytes(tile.getdata())
                    for a, b in replacements:
                        data = data.replace(bytes([a]), bytes([b]))
                    tile.putdata(data)
                    img.paste(tile, (x * 8, y * 8))
            if new_pal not in gb_pal_mapping:
                gb_pal_mapping[new_pal] = len(gb_pal_mapping)
            attr = gb_pal_mapping[new_pal]
            if x + y * 20 > 255:
                attr |= 0x08
            all_attr_data += bytes([attr])
            pal_dict = {p: idx for idx, p in enumerate(new_pal)}
            data = bytes(tile.getdata())
            tile_data = b''
            for by in range(8):
                a, b = 0, 0
                for bx in range(8):
                    n = pal_dict.get(data[bx + by * 8], 0)
                    if n & 1:
                        a |= 0x80 >> bx
                    if n & 2:
                        b |= 0x80 >> bx
                tile_data += bytes([a, b])
            all_tile_data += tile_data

    gb_pal_data = [0] * 4 * 8
    for pal, main_idx in gb_pal_mapping.items():
        for sub_idx, col_idx in enumerate(pal):
            r, g, b = pal_values[col_idx*3:col_idx*3+3]
            r, g, b = r >> 3, g >> 3, b >> 3
            gb_pal_data[main_idx * 4 + sub_idx] = r | (g << 5) | (b << 10)

    all_pal_data = b''.join(struct.pack("<H", p) for p in gb_pal_data)

    img.save("test.png")
    open(output_filename, "wb").write(all_tile_data + all_attr_data + all_pal_data)


def main(mainargs=None):
    parser = argparse.ArgumentParser(description='Convert a png to a bin file')
    parser.add_argument('input_file', type=str)
    parser.add_argument('output_file', type=str)
    parser.add_argument('--endscreen', dest="endscreen", action="store_true", help="Convert image to cats.bin")
    args = parser.parse_args(mainargs)
    if args.endscreen:
        convert_endscreen(args.input_file, args.output_file)
    else:
        data = patches.aesthetics.imageTo2bpp(args.input_file, colormap=[0x800080, 0x000000, 0x808080, 0xFFFFFF])
        open(args.output_file, "wb").write(data)


if __name__ == "__main__":
    main()