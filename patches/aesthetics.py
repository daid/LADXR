from assembler import ASM
from utils import formatText

def gfxMod(rom, filename):
    if filename.lower().endswith(".bin"):
        data = open(filename, "rb").read()
        for n in range(0, len(data), 0x4000):
            new_data = data[n:n+0x4000]
            if (0x0C + n // 0x4000) < 0x14:
                rom.banks[0x0C + n // 0x4000][0:len(new_data)] = new_data
            rom.banks[0x2C + n // 0x4000][0:len(new_data)] = new_data

def noSwordMusic(rom):
    # Skip no-sword music override
    # Instead of loading the sword level, we put the value 1 in the A register, indicating we have a sword.
    rom.patch(2, 0x0151, ASM("ld a, [$DB4E]"), ASM("ld a, $01"), fill_nop=True)
    rom.patch(2, 0x3AEF, ASM("ld a, [$DB4E]"), ASM("ld a, $01"), fill_nop=True)
    rom.patch(3, 0x0996, ASM("ld a, [$DB4E]"), ASM("ld a, $01"), fill_nop=True)
    rom.patch(3, 0x0B35, ASM("ld a, [$DB44]"), ASM("ld a, $01"), fill_nop=True)

def removeNagMessages(rom):
    # Remove "this object is heavy, bla bla", and other nag messages when touching an object
    rom.patch(0x02, 0x32BB, ASM("ld a, [$C14A]"), ASM("ld a, $01"), fill_nop=True)  # crystal blocks
    rom.patch(0x02, 0x32D3, ASM("jr nz, $25"), ASM("jr $25"), fill_nop=True)  # stones/pots
    rom.patch(0x02, 0x2B88, ASM("jr nz, $0F"), ASM("jr $0F"), fill_nop=True)  # ice blocks

def removeLowHPBeep(rom):
    rom.patch(2,  0x233A, ASM("ld hl, $FFF3\nld [hl], $04"), b"", fill_nop=True) # Remove health beep

def slowLowHPBeep(rom):
    rom.patch(2, 0x2338, ASM("ld a, $30"), ASM("ld a, $60"))  # slow slow hp beep

def forceLinksPalette(rom, index):
    # This forces the link sprite into a specific palette index ignoring the tunic options.
    rom.patch(0, 0x1D8C,
            ASM("ld a, [$DC0F]\nand a\njr z, $03\ninc a"),
            ASM("ld a, $%02X" % (index)), fill_nop=True)
    rom.patch(0, 0x1DD2,
            ASM("ld a, [$DC0F]\nand a\njr z, $03\ninc a"),
            ASM("ld a, $%02X" % (index)), fill_nop=True)

def fastText(rom):
    rom.patch(0x00, 0x24CA, ASM("jp $2485"), ASM("call $2485"))

def noText(rom):
    for idx in range(len(rom.texts)):
        if not isinstance(rom.texts[idx], int):
            rom.texts[idx] = rom.texts[idx][-1:]

def reduceMessageLengths(rom):
    # Into text from Marin. Got to go fast, so less text. (This intro text is very long)
    rom.texts[0x01] = formatText(b"Let's a go!")

    # Reduce length of a bunch of common texts
    rom.texts[0xEA] = formatText(b"You've got a Guardian Acorn!")
    rom.texts[0xEB] = rom.texts[0xEA]
    rom.texts[0xEC] = rom.texts[0xEA]
    rom.texts[0x08] = formatText(b"You got a Piece of Power!")
    rom.texts[0xEF] = formatText(b"You found a Secret Seashell!")
    rom.texts[0xA7] = formatText(b"You've got the Compass!")

    rom.texts[0x07] = formatText(b"You need the nightmare key!")
    rom.texts[0x8C] = formatText(b"You need a key!")  # keyhole block
