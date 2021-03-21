import binascii
import utils
import re


REGS8 = {"A": 7, "B": 0, "C": 1, "D": 2, "E": 3, "H": 4, "L": 5, "[HL]": 6}
REGS16A = {"BC": 0, "DE": 1, "HL": 2, "SP": 3}
REGS16B = {"BC": 0, "DE": 1, "HL": 2, "AF": 3}
FLAGS = {"NZ": 0x00, "Z": 0x08, "NC": 0x10, "C": 0x18}

CONST_MAP = {}


class ExprBase:
    def asReg8(self):
        return None

    def isA(self, kind, value=None):
        return False


class Token(ExprBase):
    def __init__(self, kind, value, line_nr):
        self.kind = kind
        self.value = value
        self.line_nr = line_nr

    def isA(self, kind, value=None):
        return self.kind == kind and (value is None or value == self.value)

    def __repr__(self):
        return "[%s:%s:%d]" % (self.kind, self.value, self.line_nr)

    def asReg8(self):
        if self.kind == 'ID':
            return REGS8.get(self.value, None)
        return None


class REF(ExprBase):
    def __init__(self, expr):
        self.expr = expr

    def asReg8(self):
        if self.expr.isA('ID', 'HL'):
            return REGS8['[HL]']
        return None

class Tokenizer:
    TOKEN_REGEX = re.compile('|'.join('(?P<%s>%s)' % pair for pair in [
        ('NUMBER', r'\d+(\.\d*)?'),
        ('HEX', r'\$[0-9A-Fa-f]+'),
        ('ASSIGN', r':='),
        ('COMMENT', r';[^\n]+'),
        ('LABEL', r':'),
        ('DIRECTIVE', r'#[A-Za-z_]+'),
        ('STRING', '[a-zA-Z]?"[^"]*"'),
        ('ID', r'\.?[A-Za-z_][A-Za-z0-9_\.]*'),
        ('OP', r'[+\-*/,]'),
        ('REFOPEN', r'\['),
        ('REFCLOSE', r'\]'),
        ('NEWLINE', r'\n'),
        ('SKIP', r'[ \t]+'),
        ('MISMATCH', r'.'),
    ]))

    def __init__(self, code):
        self.__tokens = []
        line_num = 1
        for mo in self.TOKEN_REGEX.finditer(code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'MISMATCH':
                print(code.split("\n")[line_num-1])
                raise RuntimeError("Syntax error on line: %d: %s\n%s", line_num, value)
            elif kind == 'SKIP':
                pass
            elif kind == 'COMMENT':
                pass
            else:
                if kind == 'NUMBER':
                    value = int(value)
                elif kind == 'HEX':
                    value = int(value[1:], 16)
                    kind = 'NUMBER'
                elif kind == 'ID':
                    value = value.upper()
                self.__tokens.append(Token(kind, value, line_num))
                if kind == 'NEWLINE':
                    line_num += 1
        self.__tokens.append(Token('NEWLINE', '\n', line_num))

    def peek(self):
        return self.__tokens[0]

    def pop(self):
        return self.__tokens.pop(0)

    def expect(self, kind, value=None):
        pop = self.pop()
        if not pop.isA(kind, value):
            if value is not None:
                raise SyntaxError("%s != %s:%s" % (pop, kind, value))
            raise SyntaxError("%s != %s" % (pop, kind))

    def __bool__(self):
        return bool(self.__tokens)


class Assembler:
    SIMPLE_INSTR = {
        'NOP':  0x00,
        'RLCA': 0x07,
        'RRCA': 0x0F,
        'STOP': 0x010,
        'RLA':  0x17,
        'RRA':  0x1F,
        'DAA':  0x27,
        'CPL':  0x2F,
        'SCF':  0x37,
        'CCF':  0x3F,
        'HALT': 0x76,
        'RETI': 0xD9,
        'DI':   0xF3,
        'EI':   0xFB,
    }

    LINK_REL8 = 0
    LINK_ABS16 = 1

    def __init__(self, base_address=None):
        self.__base_address = base_address
        self.__result = bytearray()
        self.__label = {}
        self.__link = {}
        self.__scope = None

        self.__tok = None

    def process(self, code):
        conditional_stack = [True]
        self.__tok = Tokenizer(code)
        try:
            while self.__tok:
                start = self.__tok.pop()
                if start.kind == 'NEWLINE':
                    pass  # Empty newline
                elif start.kind == 'DIRECTIVE':
                    if start.value == '#IF':
                        t = self.parseExpression()
                        conditional_stack.append(conditional_stack[-1] and CONST_MAP.get(t.value, 0) != 0)
                        self.__tok.expect('NEWLINE')
                    elif start.value == '#ELSE':
                        conditional_stack[-1] = not conditional_stack[-1] and conditional_stack[-2]
                        self.__tok.expect('NEWLINE')
                    elif start.value == '#ENDIF':
                        conditional_stack.pop()
                        assert conditional_stack
                        self.__tok.expect('NEWLINE')
                    else:
                        raise SyntaxError(start)
                elif not conditional_stack[-1]:
                    while not self.__tok.pop().isA('NEWLINE'):
                        pass
                elif start.kind == 'ID':
                    if start.value == 'DB':
                        self.instrDB()
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'DW':
                        self.instrDW()
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'LD':
                        self.instrLD()
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'LDH':
                        self.instrLDH()
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'LDI':
                        self.instrLDI()
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'LDD':
                        self.instrLDD()
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'INC':
                        self.instrINC()
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'DEC':
                        self.instrDEC()
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'ADD':
                        self.instrADD()
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'ADC':
                        self.instrALU(0x88)
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'SUB':
                        self.instrALU(0x90)
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'SBC':
                        self.instrALU(0x98)
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'AND':
                        self.instrALU(0xA0)
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'XOR':
                        self.instrALU(0xA8)
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'OR':
                        self.instrALU(0xB0)
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'CP':
                        self.instrALU(0xB8)
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'BIT':
                        self.instrBIT(0x40)
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'RES':
                        self.instrBIT(0x80)
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'SET':
                        self.instrBIT(0xC0)
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'RET':
                        self.instrRET()
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'CALL':
                        self.instrCALL()
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'RLC':
                        self.instrCB(0x00)
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'RRC':
                        self.instrCB(0x08)
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'RL':
                        self.instrCB(0x10)
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'RR':
                        self.instrCB(0x18)
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'SLA':
                        self.instrCB(0x20)
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'SRA':
                        self.instrCB(0x28)
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'SWAP':
                        self.instrCB(0x30)
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'SRL':
                        self.instrCB(0x38)
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'RST':
                        self.instrRST()
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'JP':
                        self.instrJP()
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'JR':
                        self.instrJR()
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'PUSH':
                        self.instrPUSHPOP(0xC5)
                        self.__tok.expect('NEWLINE')
                    elif start.value == 'POP':
                        self.instrPUSHPOP(0xC1)
                        self.__tok.expect('NEWLINE')
                    elif start.value in self.SIMPLE_INSTR:
                        self.__result.append(self.SIMPLE_INSTR[start.value])
                        self.__tok.expect('NEWLINE')
                    elif self.__tok.peek().kind == 'LABEL':
                        self.__tok.pop()
                        self.addLabel(start.value)
                    else:
                        raise SyntaxError(start)
                else:
                    raise SyntaxError(start)
        except SyntaxError:
            print("Syntax error on line: %s" % code.split("\n")[self.__tok.peek().line_nr-1])
            raise

    def insert8(self, expr):
        if expr.isA('NUMBER'):
            self.__result.append(expr.value)
        elif expr.isA('ID') and expr.value in CONST_MAP:
            self.__result.append(CONST_MAP[expr.value])
        else:
            self.__result.append(0x00)

    def insertRel8(self, expr):
        if expr.isA('NUMBER'):
            self.__result.append(expr.value)
        elif expr.isA('ID'):
            label = expr.value
            if label.startswith('.'):
                label = self.__scope + label
            self.__link[len(self.__result)] = (Assembler.LINK_REL8, label)
            self.__result.append(0x00)
        else:
            raise SyntaxError

    def insert16(self, expr):
        if expr.isA('NUMBER'):
            value = expr.value
        elif expr.isA('ID') and expr.value in CONST_MAP:
            value = CONST_MAP[expr.value]
        elif expr.isA('ID'):
            label = expr.value
            if label.startswith('.'):
                label = self.__scope + label
            self.__link[len(self.__result)] = (Assembler.LINK_ABS16, label)
            value = 0
        else:
            raise SyntaxError
        self.__result.append(value & 0xFF)
        self.__result.append(value >> 8)

    def insertString(self, string):
        if string.startswith('"') and string.endswith('"'):
            self.__result += string[1:-1].encode("ascii")
        elif string.startswith("m\"") and string.endswith("\""):
            self.__result += utils.formatText(string[2:-1].replace("|", "\n"))
        else:
            raise SyntaxError

    def instrLD(self):
        left_param = self.parseParam()
        self.__tok.expect('OP', ',')
        right_param = self.parseParam()
        if left_param.asReg8() is not None and right_param.asReg8() is not None:
            self.__result.append(0x40 | (left_param.asReg8() << 3) | right_param.asReg8())
        elif left_param.isA('ID', 'A') and isinstance(right_param, REF):
            if right_param.expr.isA('ID', 'BC'):
                self.__result.append(0x0A)
            elif right_param.expr.isA('ID', 'DE'):
                self.__result.append(0x1A)
            elif right_param.expr.isA('ID', 'HL+'):  # TODO
                self.__result.append(0x2A)
            elif right_param.expr.isA('ID', 'HL-'):  # TODO
                self.__result.append(0x3A)
            elif right_param.expr.isA('ID', 'C'):
                self.__result.append(0xF2)
            else:
                self.__result.append(0xFA)
                self.insert16(right_param.expr)
        elif right_param.isA('ID', 'A') and isinstance(left_param, REF):
            if left_param.expr.isA('ID', 'BC'):
                self.__result.append(0x02)
            elif left_param.expr.isA('ID', 'DE'):
                self.__result.append(0x12)
            elif left_param.expr.isA('ID', 'HL+'):  # TODO
                self.__result.append(0x22)
            elif left_param.expr.isA('ID', 'HL-'):  # TODO
                self.__result.append(0x32)
            elif left_param.expr.isA('ID', 'C'):
                self.__result.append(0xE2)
            else:
                self.__result.append(0xEA)
                self.insert16(left_param.expr)
        elif left_param.isA('ID', 'BC'):
            self.__result.append(0x01)
            self.insert16(right_param)
        elif left_param.isA('ID', 'DE'):
            self.__result.append(0x11)
            self.insert16(right_param)
        elif left_param.isA('ID', 'HL'):
            self.__result.append(0x21)
            self.insert16(right_param)
        elif left_param.isA('ID', 'SP'):
            if right_param.isA('ID', 'HL'):
                self.__result.append(0xF9)
            else:
                self.__result.append(0x31)
                self.insert16(right_param)
        elif right_param.isA('ID', 'SP') and isinstance(left_param, REF):
            self.__result.append(0x08)
            self.insert16(left_param.expr)
        elif left_param.asReg8() is not None:
            self.__result.append(0x06 | (left_param.asReg8() << 3))
            self.insert8(right_param)
        else:
            raise SyntaxError

    def instrLDH(self):
        left_param = self.parseParam()
        self.__tok.expect('OP', ',')
        right_param = self.parseParam()
        if left_param.isA('ID', 'A') and isinstance(right_param, REF):
            if right_param.expr.isA('ID', 'C'):
                self.__result.append(0xF2)
            else:
                self.__result.append(0xF0)
                self.insert8(right_param.expr)
        elif right_param.isA('ID', 'A') and isinstance(left_param, REF):
            if left_param.expr.isA('ID', 'C'):
                self.__result.append(0xE2)
            else:
                self.__result.append(0xE0)
                self.insert8(left_param.expr)
        else:
            raise SyntaxError

    def instrLDI(self):
        left_param = self.parseParam()
        self.__tok.expect('OP', ',')
        right_param = self.parseParam()
        if left_param.isA('ID', 'A') and isinstance(right_param, REF) and right_param.expr.isA('ID', 'HL'):
            self.__result.append(0x2A)
        elif right_param.isA('ID', 'A') and isinstance(left_param, REF) and left_param.expr.isA('ID', 'HL'):
            self.__result.append(0x22)
        else:
            raise SyntaxError

    def instrLDD(self):
        left_param = self.parseParam()
        self.__tok.expect('OP', ',')
        right_param = self.parseParam()
        if left_param.isA('ID', 'A') and isinstance(right_param, REF) and right_param.expr.isA('ID', 'HL'):
            self.__result.append(0x3A)
        elif right_param.isA('ID', 'A') and isinstance(left_param, REF) and left_param.expr.isA('ID', 'HL'):
            self.__result.append(0x32)
        else:
            raise SyntaxError

    def instrINC(self):
        param = self.parseParam()
        if param.asReg8() is not None:
            self.__result.append(0x04 | (param.asReg8() << 3))
        elif param.isA('ID', 'BC'):
            self.__result.append(0x03)
        elif param.isA('ID', 'DE'):
            self.__result.append(0x13)
        elif param.isA('ID', 'HL'):
            self.__result.append(0x23)
        elif param.isA('ID', 'SP'):
            self.__result.append(0x33)
        else:
            raise SyntaxError

    def instrDEC(self):
        param = self.parseParam()
        if param.asReg8() is not None:
            self.__result.append(0x05 | (param.asReg8() << 3))
        elif param.isA('ID', 'BC'):
            self.__result.append(0x0B)
        elif param.isA('ID', 'DE'):
            self.__result.append(0x1B)
        elif param.isA('ID', 'HL'):
            self.__result.append(0x2B)
        elif param.isA('ID', 'SP'):
            self.__result.append(0x3B)
        else:
            raise SyntaxError

    def instrADD(self):
        left_param = self.parseParam()
        self.__tok.expect('OP', ',')
        right_param = self.parseParam()

        if left_param.isA('ID', 'A'):
            if right_param.asReg8() is not None:
                self.__result.append(0x80 | right_param.asReg8())
            else:
                self.__result.append(0xC6)
                self.insert8(right_param)
        elif left_param.isA('ID', 'HL') and right_param.isA('ID') and right_param.value in REGS16A:
            self.__result.append(0x09 | REGS16A[right_param.value] << 4)
        elif left_param.isA('ID', 'SP'):
            self.__result.append(0xE8)
            self.insert8(right_param)
        else:
            raise SyntaxError

    def instrALU(self, code_value):
        param = self.parseParam()
        if param.isA('ID', 'A') and self.__tok.peek().isA('OP', ','):
            self.__tok.pop()
            param = self.parseParam()
        if param.asReg8() is not None:
            self.__result.append(code_value | param.asReg8())
        else:
            self.__result.append(code_value | 0x46)
            self.insert8(param)

    def instrRST(self):
        param = self.parseParam()
        if param.isA('NUMBER') and (param.value & ~0x38) == 0:
            self.__result.append(0xC7 | param.value)
        else:
            raise SyntaxError

    def instrPUSHPOP(self, code_value):
        param = self.parseParam()
        if param.isA('ID') and param.value in REGS16B:
            self.__result.append(code_value | (REGS16B[param.value] << 4))
        else:
            raise SyntaxError

    def instrJR(self):
        param = self.parseParam()
        if self.__tok.peek().isA('OP', ','):
            self.__tok.pop()
            condition = param
            param = self.parseParam()
            if condition.isA('ID') and condition.value in FLAGS:
                self.__result.append(0x20 | FLAGS[condition.value])
            else:
                raise SyntaxError
        else:
            self.__result.append(0x18)
        self.insertRel8(param)

    def instrCB(self, code_value):
        param = self.parseParam()
        if param.asReg8() is not None:
            self.__result.append(0xCB)
            self.__result.append(code_value | param.asReg8())
        else:
            raise SyntaxError

    def instrBIT(self, code_value):
        left_param = self.parseParam()
        self.__tok.expect('OP', ',')
        right_param = self.parseParam()
        if left_param.isA('NUMBER') and right_param.asReg8() is not None:
            self.__result.append(0xCB)
            self.__result.append(code_value | (left_param.value << 3) | right_param.asReg8())
        else:
            raise SyntaxError

    def instrRET(self):
        if self.__tok.peek().isA('ID'):
            condition = self.__tok.pop()
            if condition.isA('ID') and condition.value in FLAGS:
                self.__result.append(0xC0 | FLAGS[condition.value])
            else:
                raise SyntaxError
        else:
            self.__result.append(0xC9)

    def instrCALL(self):
        param = self.parseParam()
        if self.__tok.peek().isA('OP', ','):
            self.__tok.pop()
            condition = param
            param = self.parseParam()
            if condition.isA('ID') and condition.value in FLAGS:
                self.__result.append(0xC4 | FLAGS[condition.value])
            else:
                raise SyntaxError
        else:
            self.__result.append(0xCD)
        self.insert16(param)

    def instrJP(self):
        param = self.parseParam()
        if self.__tok.peek().isA('OP', ','):
            self.__tok.pop()
            condition = param
            param = self.parseParam()
            if condition.isA('ID') and condition.value in FLAGS:
                self.__result.append(0xC2 | FLAGS[condition.value])
            else:
                raise SyntaxError
        elif param.isA('ID', 'HL'):
            self.__result.append(0xE9)
            return
        else:
            self.__result.append(0xC3)
        self.insert16(param)

    def instrDW(self):
        param = self.parseExpression()
        self.insert16(param)
        while self.__tok.peek().isA('OP', ','):
            self.__tok.pop()
            param = self.parseExpression()
            self.insert16(param)

    def instrDB(self):
        param = self.parseExpression()
        if param.isA('STRING'):
            self.insertString(param.value)
        else:
            self.insert8(param)
        while self.__tok.peek().isA('OP', ','):
            self.__tok.pop()
            param = self.parseExpression()
            if param.isA('STRING'):
                self.insertString(param.value)
            else:
                self.insert8(param)

    def addLabel(self, label):
        if label.startswith("."):
            label = self.__scope + label
        else:
            assert "." not in label, label
            self.__scope = label
        assert label not in self.__label, "Duplicate label: %s" % (label)
        self.__label[label] = len(self.__result)

    def parseParam(self):
        t = self.__tok.peek()
        if t.kind == 'REFOPEN':
            self.__tok.pop()
            expr = self.parseExpression()
            self.__tok.expect('REFCLOSE')
            return REF(expr)
        return self.parseExpression()

    def parseExpression(self):
        t = self.__tok.pop()
        if t.kind not in ('ID', 'NUMBER', 'STRING'):
            raise SyntaxError
        return t

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

    def getLabels(self):
        return self.__label.items()


def const(name, value):
    name = name.upper()
    assert name not in CONST_MAP
    CONST_MAP[name] = value


def resetConsts():
    CONST_MAP.clear()


def ASM(code, base_address=None, labels_result=None):
    asm = Assembler(base_address)
    asm.process(code)
    asm.link()
    if labels_result is not None:
        for label, offset in asm.getLabels():
            labels_result[label] = base_address + offset
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
                        name = '$' + name[:-1]
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
