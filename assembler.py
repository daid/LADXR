import binascii

REGS = {"A": 7, "B": 0, "C": 1, "D": 2, "E": 3, "H": 4, "L": 5, "(HL)": 6, "[HL]": 6}
FLAGS = {"NZ": 0x00, "Z": 0x08, "NC": 0x10, "C": 0x18}


class Assembler:
    LINK_REL8 = 0
    LINK_ABS16 = 1

    def __init__(self, base_address=None):
        self.__base_address = base_address
        self.__result = bytearray()
        self.__label = {}
        self.__link = {}
        self.__scope = None

    def toByte(self, code):
        if code.startswith("$") and len(code) == 3:
            return int(code[1:], 16)
        raise ValueError("Cannot ASM '%s' into 8bit" % (code))

    def toWord(self, code):
        if code.startswith("$") and len(code) == 5:
            value = int(code[1:], 16)
            return bytes([value & 0xFF, value >> 8])
        if self.__base_address is not None:
            if code.startswith("."):
                code = self.__scope + code
            self.__link[len(self.__result)] = (Assembler.LINK_ABS16, code)
            return b'\x00\x00'
        raise ValueError("Cannot ASM '%s' into 16bit" % (code))

    def assemble(self, line):
        if ";" in line:
            line = line[:line.find(";")]
        line = line.strip().replace("\t", " ").upper()
        while "  " in line:
            line = line.strip().replace("  ", " ")
        if line.endswith(":"):
            line = line[:-1]
            if line.startswith("."):
                self.__label[self.__scope + line] = len(self.__result)
            else:
                assert "." not in line, line
                self.__label[line] = len(self.__result)
                self.__scope = line
            return
        if len(line) < 1:
            return
        if " " in line:
            mnemonic, params = line.split(" ", 1)
            params = list(map(str.strip, params.split(",")))
        else:
            mnemonic = line
            params = []
        if mnemonic == "NOP":
            assert len(params) == 0, line
            self.__result.append(0x00)
        elif mnemonic == "STOP":
            assert len(params) == 0, line
            self.__result.append(0x10)
        elif mnemonic == "JP":
            if len(params) == 2:
                flag = FLAGS[params[0]]
                self.__result.append(0xC2 | flag)
                self.__result += self.toWord(params[1])
            elif len(params) == 1:
                if params[0] == "HL":
                    self.__result.append(0xE9)
                else:
                    self.__result.append(0xC3)
                    self.__result += self.toWord(params[0])
            else:
                raise RuntimeError("Cannot ASM: %s" % (line))
        elif mnemonic == "JR":
            if len(params) == 2:
                self.__result.append(0x20 | FLAGS[params[0]])
                params.pop(0)
            else:
                self.__result.append(0x18)
            assert len(params) == 1, line
            if params[0].startswith("$"):
                self.__result.append(self.toByte(params[0]))
            else:
                if params[0].startswith("."):
                    params[0] = self.__scope + params[0]
                self.__link[len(self.__result)] = (Assembler.LINK_REL8, params[0])
                self.__result.append(0)
        elif mnemonic == "RET":
            if len(params) == 0:
                self.__result.append(0xC9)
            elif len(params) == 1:
                self.__result.append(0xC0 | FLAGS[params[0]])
            else:
                raise RuntimeError("Cannot ASM: %s" % (line))
        elif mnemonic == "RST":
            assert len(params) == 1, line
            value = int(params[0])
            assert (value & 0x07) == 0, line
            assert 0 <= value < 0x40, line
            self.__result.append(0xC7 + value)
        elif mnemonic == "PUSH":
            assert len(params) == 1, line
            if params[0] == "BC":
                self.__result.append(0xC5)
            elif params[0] == "DE":
                self.__result.append(0xD5)
            elif params[0] == "HL":
                self.__result.append(0xE5)
            elif params[0] == "AF":
                self.__result.append(0xF5)
            else:
                raise RuntimeError("Cannot ASM: %s" % (line))
        elif mnemonic == "POP":
            assert len(params) == 1, line
            if params[0] == "BC":
                self.__result.append(0xC1)
            elif params[0] == "DE":
                self.__result.append(0xD1)
            elif params[0] == "HL":
                self.__result.append(0xE1)
            elif params[0] == "AF":
                self.__result.append(0xF1)
            else:
                raise RuntimeError("Cannot ASM: %s" % (line))
        elif mnemonic == "LDI":
            assert len(params) == 2, line
            if params[0] == "A" and params[1] == "[HL]":
                self.__result.append(0x2A)
            elif params[0] == "[HL]" and params[1] == "A":
                self.__result.append(0x22)
            else:
                raise RuntimeError("Cannot ASM: %s" % (line))
        elif mnemonic == "LD":
            assert len(params) == 2, line
            dst = REGS.get(params[0])
            src = REGS.get(params[1])
            if params[0] == "A" and src is None and params[1].startswith("[") and params[1].endswith("]"):
                self.__result.append(0xFA)
                self.__result += self.toWord(params[1][1:-1])
            elif params[1] == "A" and dst is None and params[0].startswith("[") and params[0].endswith("]"):
                if params[0] == "[DE]":
                    self.__result.append(0x12)
                else:
                    self.__result.append(0xEA)
                    self.__result += self.toWord(params[0][1:-1])
            elif params[0] == "BC":
                self.__result.append(0x01)
                self.__result += self.toWord(params[1])
            elif params[0] == "DE":
                self.__result.append(0x11)
                self.__result += self.toWord(params[1])
            elif params[0] == "HL":
                self.__result.append(0x21)
                self.__result += self.toWord(params[1])
            elif params[0] == "SP":
                self.__result.append(0x31)
                self.__result += self.toWord(params[1])
            elif dst is not None and src is not None:
                self.__result.append(0x40 | src | (dst << 3))
            elif dst is not None:
                self.__result.append(0x06 | (dst << 3))
                self.__result.append(self.toByte(params[1]))
            else:
                raise RuntimeError("Cannot ASM: %s" % (line))
        elif mnemonic == "ADD":
            assert len(params) == 2, line
            src = REGS.get(params[1])
            if params[0] == "A" and src is not None:
                self.__result.append(0x80 | src)
            elif params[0] == "A":
                self.__result.append(0xC6)
                self.__result.append(self.toByte(params[1]))
            elif params[0] == "HL" and params[1] == "BC":
                self.__result.append(0x09)
            elif params[0] == "HL" and params[1] == "DE":
                self.__result.append(0x19)
            elif params[0] == "HL" and params[1] == "HL":
                self.__result.append(0x29)
            elif params[0] == "HL" and params[1] == "SP":
                self.__result.append(0x39)
            else:
                raise RuntimeError("Cannot ASM: %s" % (line))
        elif mnemonic == "SUB":
            assert len(params) == 1, line
            reg = REGS.get(params[0])
            if reg is not None:
                self.__result.append(0x90 | reg)
            else:
                self.__result.append(0xD6)
                self.__result.append(self.toByte(params[0]))
        elif mnemonic == "XOR":
            assert len(params) == 1, line
            reg = REGS.get(params[0])
            if reg is not None:
                self.__result.append(0xA8 | reg)
            else:
                self.__result.append(0xEE)
                self.__result.append(self.toByte(params[0]))
        elif mnemonic == "AND":
            assert len(params) == 1, line
            reg = REGS.get(params[0])
            if reg is not None:
                self.__result.append(0xA0 | reg)
            else:
                self.__result.append(0xE6)
                self.__result.append(self.toByte(params[0]))
        elif mnemonic == "OR":
            assert len(params) == 1, line
            reg = REGS.get(params[0])
            if reg is not None:
                self.__result.append(0xB0 | reg)
            else:
                self.__result.append(0xF6)
                self.__result.append(self.toByte(params[0]))
        elif mnemonic == "CP":
            assert len(params) == 1, line
            reg = REGS.get(params[0])
            if reg is not None:
                self.__result.append(0xB8 | reg)
            else:
                self.__result.append(0xFE)
                self.__result.append(self.toByte(params[0]))
        elif mnemonic == "INC":
            assert len(params) == 1, line
            reg = REGS.get(params[0])
            if reg is not None:
                self.__result.append(0x04 | (reg << 3))
            elif params[0] == "BC":
                self.__result.append(0x03)
            elif params[0] == "DE":
                self.__result.append(0x13)
            elif params[0] == "HL":
                self.__result.append(0x23)
            elif params[0] == "SP":
                self.__result.append(0x33)
            else:
                raise RuntimeError("Cannot ASM: %s" % (line))
        elif mnemonic == "DEC":
            assert len(params) == 1, line
            reg = REGS.get(params[0])
            if reg is not None:
                self.__result.append(0x05 | (reg << 3))
            elif params[0] == "BC":
                self.__result.append(0x0B)
            elif params[0] == "DE":
                self.__result.append(0x1B)
            elif params[0] == "HL":
                self.__result.append(0x2B)
            elif params[0] == "SP":
                self.__result.append(0x3B)
            else:
                raise RuntimeError("Cannot ASM: %s" % (line))
        elif mnemonic == "LDH":
            assert len(params) == 2, line
            if params[0] == "A" and params[1].startswith("[") and params[1].endswith("]"):
                self.__result.append(0xF0)
                self.__result.append(self.toByte(params[1][1:-1]))
            elif params[1] == "A" and params[0].startswith("[") and params[0].endswith("]"):
                self.__result.append(0xE0)
                self.__result.append(self.toByte(params[0][1:-1]))
            else:
                raise RuntimeError("Cannot ASM: %s" % (line))
        elif mnemonic == "BIT":
            assert len(params) == 2, line
            reg = REGS[params[1]]
            bit = int(params[0])
            assert 0 <= bit < 8, line
            self.__result.append(0xCB)
            self.__result.append(0x40 | reg | (bit << 3))
        elif mnemonic == "RES":
            assert len(params) == 2, line
            reg = REGS[params[1]]
            bit = int(params[0])
            assert 0 <= bit < 8
            self.__result.append(0xCB)
            self.__result.append(0x80 | reg | (bit << 3))
        elif mnemonic == "SET":
            assert len(params) == 2
            reg = REGS[params[1]]
            bit = int(params[0])
            assert 0 <= bit < 8
            self.__result.append(0xCB)
            self.__result.append(0xC0 | reg | (bit << 3))
        elif mnemonic == "CALL":
            assert len(params) == 1
            self.__result.append(0xCD)
            self.__result += self.toWord(params[0])
        elif mnemonic == "DB":
            for byte in params:
                self.__result.append(self.toByte(byte))
        elif mnemonic == "DW":
            for byte in params:
                self.__result += self.toWord(byte)
        else:
            raise RuntimeError("Cannot ASM: %s" % (line))

    def link(self):
        for offset, target in self.__link.items():
            link_type, label = target
            if link_type == Assembler.LINK_REL8:
                byte = self.__label[label] - offset - 1
                assert -128 <= byte <= 127
                self.__result[offset] = byte & 0xFF
            elif link_type == Assembler.LINK_ABS16:
                self.__result[offset] = (self.__label[label] + self.__base_address) & 0xFF
                self.__result[offset + 1] = (self.__label[label] + self.__base_address) >> 8

    def getResult(self):
        return self.__result


def ASM(code, base_address=None):
    asm = Assembler(base_address)
    for line in code.split("\n"):
        asm.assemble(line)
    asm.link()
    return binascii.hexlify(asm.getResult())
