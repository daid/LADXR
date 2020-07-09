
def formatText(s, *, ask=None):
    s = s.replace(b"'", b"^")

    result = b''
    for line in s.split(b'\n'):
        result_line = b''
        for word in line.split(b' '):
            if len(result_line) + 1 + len(word) > 16:
                result += result_line + b' ' * (16 - len(result_line))
                result_line = b''
            elif result_line:
                result_line += b' '
            result_line += word
        if result_line:
            result += result_line + b' ' * (16 - len(result_line))
    if ask is not None:
        result = result.rstrip()
        while len(result) % 32 != 16:
            result += b' '
        return result + b'    ' + ask + b'\xfe'
    return result.rstrip() + b'\xff'


def tileDataToString(data, key=" 123"):
    result = ""
    for n in range(0, len(data), 2):
        a = data[n]
        b = data[n+1]
        for m in range(8):
            bit = 0x80 >> m
            if (a & bit) and (b & bit):
                result += key[3]
            elif (b & bit):
                result += key[2]
            elif (a & bit):
                result += key[1]
            else:
                result += key[0]
        result += "\n"
    return result

def createTileData(data, key=" 123"):
    result = []
    for line in data.split("\n"):
        line = line + "        "
        a = 0
        b = 0
        for n in range(8):
            if line[n] == key[3]:
                a |= 0x80 >> n
                b |= 0x80 >> n
            elif line[n] == key[2]:
                b |= 0x80 >> n
            elif line[n] == key[1]:
                a |= 0x80 >> n
        result.append(a)
        result.append(b)
    assert (len(result) % 16) == 0, len(result)
    return bytes(result)

if __name__ == "__main__":
    data = formatText(b"It is dangurous to go alone.\nTake\nthis\na\nline.")
    for i in range(0, len(data), 16):
        print(data[i:i+16])
