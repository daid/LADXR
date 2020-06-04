from backgroundEditor import BackgroundEditor
import subprocess


CHAR_MAP = {'z': 0x3E, '.': 0x39, ':': 0x42, '?': 0x3C, '!': 0x3D}


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


def setRomInfo(rom, seed):
    try:
        version = subprocess.run(['git', 'describe', '--tags', '--dirty'], stdout=subprocess.PIPE).stdout.strip()
    except:
        version = b''

    line_1_hex = _encode(seed[:16])
    line_2_hex = _encode(seed[16:])

    for n in (3, 4):
        be = BackgroundEditor(rom, n)
        ba = BackgroundEditor(rom, n, attributes=True)
        for n, v in enumerate(line_1_hex):
            be.tiles[0x9a01 + n] = v
            ba.tiles[0x9a01 + n] = 0x00
        for n, v in enumerate(line_2_hex):
            be.tiles[0x9a21 + n] = v
            ba.tiles[0x9a21 + n] = 0x00
        for n in range(0x09, 0x14):
            be.tiles[0x9820 + n] = 0xF7
            be.tiles[0x9840 + n] = 0xA0 + (n % 2)
            be.tiles[0x9860 + n] = 0xA2
        be.store(rom)
        ba.store(rom)
        be.dump()
        ba.dump()

    #rom.banks[0x05][0x0CCD:0x0CD2] = rom.banks[0x05][0x0CD0:0x0CD2] + rom.banks[0x05][0x0CCD:0x0CD0]
