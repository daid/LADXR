from assembler import ASM
from utils import formatText

def setRequiredInstrumentCount(rom, count):
    if count >= 8:
        return

    # TODO: Music bugs out at the end, unless you have all instruments.
    rom.texts[0x1A3] = formatText(b"You need %d instruments" % (count))
    rom.patch(0x19, 0x0B79, None, "0000")  # always spawn all instruments, we need the last one as that handles opening the egg.
    rom.patch(0x19, 0x0BF4, ASM("jp $3BC0"), ASM("jp $7FE0")) # instead of rendering the instrument, jump to the code below.
    rom.patch(0x19, 0x0BFE, ASM("""
        ; Normal check fo all instruments
        ld   e, $08
        ld   hl, $DB65
    loop:
        ldi  a, [hl]
        and  $02
        jr   z, $12
        dec  e
        jr   nz, loop
    """), ASM("""
        jp   $7F2B ; jump to the end of the bank, where there is some space for code.
    """), fill_nop=True)
    # Add some code at the end of the bank, as we do not have enough space to do this "in place"
    rom.patch(0x19, 0x3F2B, "0000000000000000000000000000000000000000000000000000", ASM("""
        ld   d, $00
        ld   e, $08
        ld   hl, $DB65 ; start of has instrument memory
loop:
        ld   a, [hl]
        and  $02
        jr   z, noinc
        inc  d
noinc:
        inc  hl
        dec  e
        jr   nz, loop
        ld   a, d
        cp   $%02x    ; check if we have a minimal of this amount of instruments.
        jp   c, $4C1A ; not enough instruments
        jp   $4C0B    ; enough instruments
    """ % (count)), fill_nop=True)
    rom.patch(0x19, 0x3FE0, "0000000000000000000000000000000000000000000000000000", ASM("""
    ; Entry point of render code
        ld   hl, $DB65  ; table of having instruments
        push bc
        ldh  a, [$F1]
        ld   c, a
        add  hl, bc
        pop  bc
        ld   a, [hl]
        and  $02        ; check if we have this instrument
        ret  z
        jp   $3BC0 ; jump to render code
    """), fill_nop=True)
