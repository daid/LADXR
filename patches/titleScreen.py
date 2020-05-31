from backgroundEditor import BackgroundEditor

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


def setRomInfo(rom, line_1, line_2):
    line_1_hex = _encode(line_1)
    line_2_hex = _encode(line_2)
    for n in (3, 4):
        be = BackgroundEditor(rom, n)
        for n, v in enumerate(line_1_hex):
            be.tiles[0x9a01 + n] = v
        for n, v in enumerate(line_2_hex):
            be.tiles[0x9a21 + n] = v
        be.store(rom)
