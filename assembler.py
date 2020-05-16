import binascii

REGS = {"A": 7, "B": 0, "C": 1, "D": 2, "E": 3, "H": 4, "L": 5, "(HL)": 6, "[HL]": 6}
FLAGS = {"NZ": 0x00, "Z": 0x08, "NC": 0x10, "C": 0x18}


def toByte(code):
    if code.startswith("$") and len(code) == 3:
        return int(code[1:], 16)
    raise ValueError("Cannot ASM %s" % (code))


def toWord(code):
    if code.startswith("$") and len(code) == 5:
        value = int(code[1:], 16)
        return bytes([value & 0xFF, value >> 8])
    raise ValueError("Cannot ASM %s" % (code))


def ASM(code):
    label = {}
    link = {}
    result = bytearray()
    for line in code.split("\n"):
        if ";" in line:
            line = line[:line.find(";")]
        line = line.strip().replace("\t", " ").upper()
        while "  " in line:
            line = line.strip().replace("  ", " ")
        if line.endswith(":"):
            label[line[:-1]] = len(result)
        elif len(line) > 0:
            mnemonic, params = line.split(" ", 1)
            params = list(map(str.strip, params.split(",")))
            if mnemonic == "NOP":
                assert len(params) == 0
                result.append(0x00)
            elif mnemonic == "CP":
                assert len(params) == 1
                reg = REGS.get(params[0])
                if reg is not None:
                    result.append(0xB8 | reg)
                else:
                    result.append(0xFE)
                    result.append(toByte(params[0]))
            elif mnemonic == "JR":
                if len(params) == 2:
                    result.append(0x20 | FLAGS[params[0]])
                    params.pop(0)
                assert len(params) == 1
                link[len(result)] = params[0]
                result.append(0)
            elif mnemonic == "PUSH":
                assert len(params) == 1
                if params[0] == "BC":
                    result.append(0xC5)
                elif params[0] == "DE":
                    result.append(0xD5)
                elif params[0] == "HL":
                    result.append(0xE5)
                elif params[0] == "AF":
                    result.append(0xF5)
                else:
                    raise RuntimeError("Cannot ASM: %s" % (line))
            elif mnemonic == "POP":
                assert len(params) == 1
                if params[0] == "BC":
                    result.append(0xC1)
                elif params[0] == "DE":
                    result.append(0xD1)
                elif params[0] == "HL":
                    result.append(0xE1)
                elif params[0] == "AF":
                    result.append(0xF1)
                else:
                    raise RuntimeError("Cannot ASM: %s" % (line))
            elif mnemonic == "LD":
                assert len(params) == 2
                dst = REGS.get(params[0])
                src = REGS.get(params[1])
                if params[0] == "A" and src is None and params[1].startswith("[") and params[1].endswith("]"):
                    result.append(0xFA)
                    result += toWord(params[1][1:-1])
                elif params[1] == "A" and dst is None and params[0].startswith("[") and params[0].endswith("]"):
                    result.append(0xEA)
                    result += toWord(params[0][1:-1])
                elif params[0] == "HL":
                    result.append(0x21)
                    result += toWord(params[1])
                elif dst is not None and src is not None:
                    result.append(0x40 | src | (dst << 3))
                elif dst is not None:
                    result.append(0x06 | (dst << 3))
                    result.append(toByte(params[1]))
                else:
                    raise RuntimeError("Cannot ASM: %s" % (line))
            elif mnemonic == "ADD":
                assert len(params) == 2
                src = REGS.get(params[1])
                if params[0] == "A" and src is not None:
                    result.append(0x80 | src)
                elif params[0] == "A":
                    result.append(0xC6)
                    result.append(toByte(params[1]))
                elif params[0] == "HL" and params[1] == "BC":
                    result.append(0x09)
                elif params[0] == "HL" and params[1] == "DE":
                    result.append(0x19)
                elif params[0] == "HL" and params[1] == "HL":
                    result.append(0x29)
                elif params[0] == "HL" and params[1] == "SP":
                    result.append(0x39)
                else:
                    raise RuntimeError("Cannot ASM: %s" % (line))
            elif mnemonic == "XOR":
                assert len(params) == 1
                reg = REGS[params[0]]
                result.append(0xA8 | reg)
            elif mnemonic == "INC":
                assert len(params) == 1
                reg = REGS.get(params[0])
                if reg is not None:
                    result.append(0x04 | (reg << 3))
                elif params[0] == "BC":
                    result.append(0x03)
                elif params[0] == "DE":
                    result.append(0x13)
                elif params[0] == "HL":
                    result.append(0x23)
                elif params[0] == "SP":
                    result.append(0x33)
                else:
                    raise RuntimeError("Cannot ASM: %s" % (line))
            else:
                raise RuntimeError("Cannot ASM: %s" % (line))
    for offset, target in link.items():
        result[offset] = (label[target] - offset - 1) & 0xFF
    return binascii.hexlify(result)
