import binascii
import utils

REGS = {"A": 7, "B": 0, "C": 1, "D": 2, "E": 3, "H": 4, "L": 5, "(HL)": 6, "[HL]": 6}
FLAGS = {"NZ": 0x00, "Z": 0x08, "NC": 0x10, "C": 0x18}

CONST_MAP = {}


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
        if code in CONST_MAP:
            return CONST_MAP[code]
        if self.__base_address is not None:
            if code.startswith("."):
                assert self.__scope is not None, code
                code = self.__scope + code
            self.__link[len(self.__result)] = (Assembler.LINK_ABS16, code)
            return b'\x00\x00'
        raise ValueError("Cannot ASM '%s' into 16bit" % (code))

    def assemble(self, line):
        if ";" in line:
            line = line[:line.find(";")]
        input_line = line.strip()
        line = line.strip().replace("\t", " ").upper()
        while "  " in line:
            line = line.strip().replace("  ", " ")
        if line.endswith(":"):
            line = line[:-1]
            if line.startswith("."):
                assert self.__scope + line not in self.__label, "Duplicate label: %s" % (self.__scope + line)
                self.__label[self.__scope + line] = len(self.__result)
            else:
                assert "." not in line, line
                assert line not in self.__label, "Duplicate label: %s" % (line)
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
        elif mnemonic == "HALT":
            assert len(params) == 0, line
            self.__result.append(0x76)
        elif mnemonic == "STOP":
            assert len(params) == 0, line
            self.__result.append(0x10)
        elif mnemonic == "DI":
            assert len(params) == 0, line
            self.__result.append(0xF3)
        elif mnemonic == "EI":
            assert len(params) == 0, line
            self.__result.append(0xFB)
        elif mnemonic == "RLA":
            assert len(params) == 0, line
            self.__result.append(0x17)
        elif mnemonic == "RLCA":
            assert len(params) == 0, line
            self.__result.append(0x07)
        elif mnemonic == "RRA":
            assert len(params) == 0, line
            self.__result.append(0x1f)
        elif mnemonic == "RRCA":
            assert len(params) == 0, line
            self.__result.append(0x0f)
        elif mnemonic == "DAA":
            assert len(params) == 0, line
            self.__result.append(0x27)
        elif mnemonic == "SCF":
            assert len(params) == 0, line
            self.__result.append(0x37)
        elif mnemonic == "CPL":
            assert len(params) == 0, line
            self.__result.append(0x2F)
        elif mnemonic == "CCF":
            assert len(params) == 0, line
            self.__result.append(0x3F)
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
                    assert self.__scope is not None, line
                    params[0] = self.__scope + params[0]
                self.__link[len(self.__result)] = (Assembler.LINK_REL8, params[0])
                self.__result.append(0)
        elif mnemonic == "RETI":
            self.__result.append(0xD9)
        elif mnemonic == "RET":
            if len(params) == 0:
                self.__result.append(0xC9)
            elif len(params) == 1:
                self.__result.append(0xC0 | FLAGS[params[0]])
            else:
                raise RuntimeError("Cannot ASM: %s" % (line))
        elif mnemonic == "RST":
            assert len(params) == 1, line
            value = int(params[0], 16)
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
        elif mnemonic == "LDD":
            assert len(params) == 2, line
            if params[0] == "A" and params[1] == "[HL]":
                self.__result.append(0x3A)
            elif params[0] == "[HL]" and params[1] == "A":
                self.__result.append(0x32)
            else:
                raise RuntimeError("Cannot ASM: %s" % (line))
        elif mnemonic == "LD":
            assert len(params) == 2, line
            dst = REGS.get(params[0])
            src = REGS.get(params[1])
            if params[0] == "A" and src is None and params[1].startswith("[") and params[1].endswith("]"):
                if params[1] == "[BC]":
                    self.__result.append(0x0A)
                elif params[1] == "[DE]":
                    self.__result.append(0x1A)
                elif params[1] == "[C]":
                    self.__result.append(0xF2)
                else:
                    self.__result.append(0xFA)
                    self.__result += self.toWord(params[1][1:-1])
            elif params[1] == "A" and dst is None and params[0].startswith("[") and params[0].endswith("]"):
                if params[0] == "[BC]":
                    self.__result.append(0x02)
                elif params[0] == "[DE]":
                    self.__result.append(0x12)
                elif params[0] == "[C]":
                    self.__result.append(0xE2)
                else:
                    self.__result.append(0xEA)
                    self.__result += self.toWord(params[0][1:-1])
            elif params[1] == "SP" and dst is None and params[0].startswith("[") and params[0].endswith("]"):
                self.__result.append(0x08)
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
            elif params[0] == "SP" and params[1] == "HL":
                self.__result.append(0xF9)
            elif params[0] == "SP":
                self.__result.append(0x31)
                self.__result += self.toWord(params[1])
            elif dst is not None and src is not None:
                assert src != 6 or dst != 6, line
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
            elif params[0] == "SP":
                self.__result.append(0xE8)
                self.__result.append(self.toByte(params[1]))
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
        elif mnemonic == "ADC":
            assert len(params) == 2, line
            assert params[0] == 'A', line
            reg = REGS.get(params[1])
            if reg is not None:
                self.__result.append(0x88 | reg)
            else:
                self.__result.append(0xCE)
                self.__result.append(self.toByte(params[1]))
        elif mnemonic == "SBC":
            assert len(params) == 2, line
            assert params[0] == 'A', line
            reg = REGS.get(params[1])
            if reg is not None:
                self.__result.append(0x98 | reg)
            else:
                self.__result.append(0xDE)
                self.__result.append(self.toByte(params[1]))
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
        elif mnemonic == "RLC":
            assert len(params) == 1
            reg = REGS[params[0]]
            self.__result.append(0xCB)
            self.__result.append(0x00 | reg)
        elif mnemonic == "RRC":
            assert len(params) == 1
            reg = REGS[params[0]]
            self.__result.append(0xCB)
            self.__result.append(0x08 | reg)
        elif mnemonic == "RL":
            assert len(params) == 1
            reg = REGS[params[0]]
            self.__result.append(0xCB)
            self.__result.append(0x10 | reg)
        elif mnemonic == "RR":
            assert len(params) == 1
            reg = REGS[params[0]]
            self.__result.append(0xCB)
            self.__result.append(0x18 | reg)
        elif mnemonic == "SLA":
            assert len(params) == 1
            reg = REGS[params[0]]
            self.__result.append(0xCB)
            self.__result.append(0x20 | reg)
        elif mnemonic == "SRA":
            assert len(params) == 1
            reg = REGS[params[0]]
            self.__result.append(0xCB)
            self.__result.append(0x28 | reg)
        elif mnemonic == "SWAP":
            assert len(params) == 1
            reg = REGS[params[0]]
            self.__result.append(0xCB)
            self.__result.append(0x30 | reg)
        elif mnemonic == "SRL":
            assert len(params) == 1
            reg = REGS[params[0]]
            self.__result.append(0xCB)
            self.__result.append(0x38 | reg)
        elif mnemonic == "CALL":
            if len(params) == 1:
                self.__result.append(0xCD)
                self.__result += self.toWord(params[0])
            elif len(params) == 2:
                flag = FLAGS[params[0]]
                self.__result.append(0xC4 | flag)
                self.__result += self.toWord(params[1])
            else:
                raise RuntimeError("Cannot ASM: %s" % (line))
        elif mnemonic == "DB":
            for param in map(str.strip, input_line[2:].strip().split(",")):
                if param.startswith("\"") and param.endswith("\""):
                    self.__result += param[1:-1].encode("ascii")
                elif param.startswith("m\"") and param.endswith("\""):
                    self.__result += utils.formatText(param[2:-1].encode("ascii"))
                else:
                    self.__result.append(self.toByte(param.strip()))
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
                assert -128 <= byte <= 127, label
                self.__result[offset] = byte & 0xFF
            elif link_type == Assembler.LINK_ABS16:
                self.__result[offset] = (self.__label[label] + self.__base_address) & 0xFF
                self.__result[offset + 1] = (self.__label[label] + self.__base_address) >> 8

    def getResult(self):
        return self.__result


def const(name, address):
    name = name.upper()
    assert name not in CONST_MAP
    CONST_MAP[name] = bytes([address & 0xFF, address >> 8])


def resetConsts():
    CONST_MAP.clear()


def ASM(code, base_address=None):
    asm = Assembler(base_address)
    conditional_stack = [True]
    for line in code.split("\n"):
        if line.startswith("#"):
            if line.startswith("#IF "):
                conditional_stack.append(conditional_stack[-1] and CONST_MAP.get(line[4:].strip(), 0) != b'\x00\x00')
            elif line == "#ENDIF":
                conditional_stack.pop()
                assert conditional_stack
            else:
                raise RuntimeError("Unknown preprocessor thingy: %s" % (line))
        elif conditional_stack[-1]:
            asm.assemble(line)
    asm.link()
    return binascii.hexlify(asm.getResult())


if __name__ == "__main__":
    import json
    opcodes = json.load(open("Opcodes.json", "rt"))
    for label in (False, True):
        for prefix, codes in opcodes.items():
            for num, op in codes.items():
                if op['mnemonic'].startswith('ILLEGAL_') or op['mnemonic'] == 'PREFIX':
                    continue
                params = []
                postfix = ''
                for o in op['operands']:
                    name = o['name']
                    if name == 'd16' or name == 'a16':
                        if label:
                            name = 'LABEL'
                        else:
                            name = '$0000'
                    if name == 'd8' or name == 'a8':
                        name = '$00'
                    if name == 'r8':
                        if label and num != '0xE8':
                            name = 'LABEL'
                        else:
                            name = '$00'
                    if name[-1] == 'H' and name[0].isnumeric():
                        name = name[:-1]
                    if o['immediate']:
                        params.append(name)
                    else:
                        params.append("[%s]" % (name))
                    if 'increment' in o and o['increment']:
                        postfix = 'I'
                    if 'decrement' in o and o['decrement']:
                        postfix = 'D'
                code = op["mnemonic"] + postfix + " " + ", ".join(params)
                code = code.strip()
                try:
                    data = ASM("LABEL:\n%s" % (code), 0x0000)
                    if prefix == 'cbprefixed':
                        assert data[0:2] == b'cb'
                        data = data[2:]
                    assert data[0:2] == num[2:].encode('ascii').lower(), data[0:2] + b"!=" + num[2:].encode('ascii').lower()
                except Exception as e:
                    print("%s\t\t|%r|\t%s" % (code, e, num))
                    print(op)
