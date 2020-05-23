
def formatText(s):
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
    return result.rstrip() + b'\xff'


if __name__ == "__main__":
    data = formatText(b"It is dangurous to go alone.\nTake\nthis\na\nline.")
    for i in range(0, len(data), 16):
        print(data[i:i+16])
