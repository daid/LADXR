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
    elif filename.lower().endswith(".png"):
        import PIL.Image
        img = PIL.Image.open(filename)
        assert (img.size[0] % 8) == 0
        assert (img.size[1] % 16) == 0
        bank_nr = 0x2C
        offset = 0
        for ty in range(img.size[1] // 16):
            for tx in range(img.size[0] // 8):
                for y in range(16):
                    a = 0
                    b = 0
                    for x in range(8):
                        c = img.getpixel((tx*8+x, ty*16+y))
                        if c & 1:
                            a |= 0x80 >> x
                        if c & 2:
                            b |= 0x80 >> x
                    rom.banks[bank_nr][offset+0] = a
                    rom.banks[bank_nr][offset+1] = b
                    offset += 2
                    if offset == 0x4000:
                        offset = 0
                        bank_nr += 1
        for n in range(0x2C, min(bank_nr + 1, 0x34)):
            rom.banks[n - 0x2C + 0x0C] = rom.banks[n].copy()

def createGfxImage(rom, filename):
    import PIL.Image
    bank_count = 8
    img = PIL.Image.new("P", (32 * 8, 32 * 8 * bank_count))
    img.putpalette((
        128, 0, 128,
        0, 0, 0,
        128, 128, 128,
        255, 255, 255,
    ))
    for bank_nr in range(bank_count):
        bank = rom.banks[0x2C + bank_nr]
        for tx in range(32):
            for ty in range(16):
                for y in range(16):
                    a = bank[tx * 32 + ty * 32 * 32 + y * 2]
                    b = bank[tx * 32 + ty * 32 * 32 + y * 2 + 1]
                    for x in range(8):
                        c = 0
                        if a & (0x80 >> x):
                            c |= 1
                        if b & (0x80 >> x):
                            c |= 2
                        img.putpixel((tx*8+x, bank_nr * 32 * 8 + ty*16+y), c)
    img.save(filename)

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


def allowColorDungeonSpritesEverywhere(rom):
    # Set sprite set numbers $01-$40 to map to the color dungeon sprites
    rom.patch(0x00, 0x2E6F, "00", "15")
    # Patch the spriteset loading code to load the 4 entries from the normal table instead of skipping this for color dungeon specific exception weirdness
    rom.patch(0x00, 0x0DA4, ASM("jr nc, $05"), ASM("jr nc, $41"))
    rom.patch(0x00, 0x0DE5, ASM("""
        ldh  a, [$F7]
        cp   $FF
        jr   nz, $06
        ld a, $01
        ldh [$91], a
        jr $40
    """), ASM("""
        jr $0A ; skip over the rest of the code
        cp $FF ; check if color dungeon
        jp nz, $0DAB
        inc d
        jp $0DAA
    """), fill_nop=True)
    # Disable color dungeon specific tile load hacks
    rom.patch(0x00, 0x06A7, ASM("jr nz, $22"), ASM("jr $22"))
    rom.patch(0x00, 0x2E77, ASM("jr nz, $0B"), ASM("jr $0B"))
    
    # Finally fill in the sprite data for the color dungeon
    for n in range(22):
        data = bytearray()
        for m in range(4):
            idx = rom.banks[0x20][0x06AA + 44 * m + n * 2]
            bank = rom.banks[0x20][0x06AA + 44 * m + n * 2 + 1]
            if idx == 0 and bank == 0:
                v = 0xFF
            elif bank == 0x35:
                v = idx - 0x40
            elif bank == 0x31:
                v = idx
            elif bank == 0x2E:
                v = idx + 0x40
            else:
                assert False, "%02x %02x" % (idx, bank)
            data += bytes([v])
        rom.room_sprite_data_indoor[0x200 + n] = data

    # Patch the graphics loading code to use DMA and load all sets that need to be reloaded, not just the first and last
    rom.patch(0x00, 0x06FA, 0x07AF, ASM("""
        ;We enter this code with the right bank selected for tile data copy,
        ;d = tile row (source addr = (d*$100+$4000))
        ;e = $00
        ;$C197 = index of sprite set to update (target addr = ($8400 + $100 * [$C197]))
        ld  a, d
        add a, $40
        ldh [$51], a
        xor a
        ldh [$52], a
        ldh [$54], a
        ld  a, [$C197]
        add a, $84
        ldh [$53], a
        ld  a, $0F
        ldh [$55], a

        ; See if we need to do anything next
        ld  a, [$C10E] ; check the 2nd update flag
        and a
        jr  nz, getNext
        ldh [$91], a ; no 2nd update flag, so clear primary update flag
        ret
    getNext:
        ld  hl, $C197
        inc [hl]
        res 2, [hl]
        ld  a, [$C10D]
        cp  [hl]
        ret nz
        xor a ; clear the 2nd update flag when we prepare to update the last spriteset
        ld  [$C10E], a
        ret
    """), fill_nop=True)
    rom.patch(0x00, 0x073E, "00" * (0x07AF - 0x073E), ASM("""
        ;If we get here, only the 2nd flag is filled and the primary is not. So swap those around.
        ld  a, [$C10D] ;copy the index number
        ld  [$C197], a
        xor a
        ld  [$C10E], a ; clear the 2nd update flag
        inc a
        ldh [$91], a ; set the primary update flag
        ret
    """), fill_nop=True)
