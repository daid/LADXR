from assembler import ASM


def slowdownThreeOfAKind(rom):
    rom.patch(0x06, 0x096B, ASM("ldh a, [$E7]\nand $0F"), ASM("ldh a, [$E7]\nand $3F"))
