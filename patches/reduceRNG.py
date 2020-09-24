from assembler import ASM


def slowdownThreeOfAKind(rom):
    rom.patch(0x06, 0x096B, ASM("ldh a, [$E7]\nand $0F"), ASM("ldh a, [$E7]\nand $3F"))


def fixHorseHeads(rom):
    rom.patch(0x07, 0x366D, ASM("ld a, [hl]"), ASM("xor a"))
