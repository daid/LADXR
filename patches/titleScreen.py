CHAR_MAP = {'z': "3E", '.': "39", ':': "42", '?': "3C", '!': "3D"}

def _encode(s):
    result = ""
    for char in s:
        if ord("A") <= ord(char) <= ord("Z"):
            result += "%02X" % (ord(char) - ord("A"))
        elif ord("a") <= ord(char) <= ord("y"):
            result += "%02X" % (ord(char) - ord("a") + 26)
        elif ord("0") <= ord(char) <= ord("9"):
            result += "%02X" % (ord(char) - ord("0") + 0x70)
        else:
            result += CHAR_MAP.get(char, "7E")
    return result


def setRomInfo(rom, line_1, line_2):
    # It was almost as if this was intended. The file select screen lower line is encoded so
    # poorly, that we can fit 2 lines of tile 17 definitions in there.
    line_1_hex = _encode(line_1)
    line_2_hex = _encode(line_2)
    line_1_hex = (line_1_hex + ("7E" * 17))[0:17*2]
    line_2_hex = (line_2_hex + ("7E" * 17))[0:17*2]
    rom.patch(8, 0x23BE,
            "9A21508F9A22009F9A24009F9A26009F9A28009F9A2A009F9A2C009F9A2E009F9A30009F9A32008F",
            "9A0110" + line_1_hex + "9A2110" + line_2_hex)
