from backgroundEditor import BackgroundEditor
import subprocess
import binascii


CHAR_MAP = {'z': 0x3E, '-': 0x3F, '.': 0x39, ':': 0x42, '?': 0x3C, '!': 0x3D}


def _encode(s):
    result = bytearray()
    for char in s:
        if ord("A") <= ord(char) <= ord("Z"):
            result.append(ord(char) - ord("A"))
        elif ord("a") <= ord(char) <= ord("y"):
            result.append(ord(char) - ord("a") + 26)
        elif ord("0") <= ord(char) <= ord("9"):
            result.append(ord(char) - ord("0") + 0x70)
        else:
            result.append(CHAR_MAP.get(char, 0x7E))
    return result


def setRomInfo(rom, seed, options):
    try:
        version = subprocess.run(['git', 'describe', '--tags', '--dirty=-D'], stdout=subprocess.PIPE).stdout.strip().decode("ascii", "replace")
    except:
        version = ""

    if options.race:
        seed = "Race"
        rom.patch(0x00, 0x07, "00", "01")
        rom.banks[0x05][0x0CCD:0x0CD2] = rom.banks[0x05][0x0CD0:0x0CD2] + rom.banks[0x05][0x0CCD:0x0CD0]
    else:
        rom.patch(0x00, 0x07, "00", "52")

    line_1_hex = _encode(seed[:16])
    line_2_hex = _encode(seed[16:])
    try:
        seednr = int(seed, 16)
    except:
        import hashlib
        seednr = int(hashlib.md5(seed.encode('ascii', 'replace')).hexdigest(), 16)

    for n in (3, 4):
        be = BackgroundEditor(rom, n)
        ba = BackgroundEditor(rom, n, attributes=True)
        for n, v in enumerate(_encode(version)):
            be.tiles[0x98a0 + 0x13 - len(version) + n] = v
            ba.tiles[0x98a0 + 0x13 - len(version) + n] = 0x00
        for n, v in enumerate(line_1_hex):
            be.tiles[0x9a01 + n] = v
            ba.tiles[0x9a01 + n] = 0x00
        for n, v in enumerate(line_2_hex):
            be.tiles[0x9a21 + n] = v
            ba.tiles[0x9a21 + n] = 0x00
        for n in range(0x09, 0x14):
            be.tiles[0x9820 + n] = 0x7F
            be.tiles[0x9840 + n] = 0xA0 + (n % 2)
            be.tiles[0x9860 + n] = 0xA2
        sn = seednr
        for n in range(0x0A, 0x14):
            tilenr = sn % 30
            sn //= 30
            if tilenr > 12:
                tilenr += 2
            if tilenr > 16:
                tilenr += 1
            if tilenr > 19:
                tilenr += 3
            if tilenr > 27:
                tilenr += 1
            if tilenr > 29:
                tilenr += 2
            if tilenr > 35:
                tilenr += 1
            be.tiles[0x9800 + n] = tilenr * 2
            be.tiles[0x9820 + n] = tilenr * 2 + 1
            pal = sn % 8
            sn //= 8
            ba.tiles[0x9800 + n] = 0x08 | pal
            ba.tiles[0x9820 + n] = 0x08 | pal
        be.store(rom)
        ba.store(rom)
