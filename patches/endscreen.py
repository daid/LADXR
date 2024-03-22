from assembler import ASM
import os
import random


def updateEndScreen(rom):
    # Call our custom data loader in bank 3F
    rom.patch(0x00, 0x391D, ASM("""
        ld   a, $20
        ld   [$2100], a
        jp   $7de6
    """), ASM("""
        ld   a, $3F
        ld   [$2100], a
        jp   $4200
    """))
    rom.patch(0x17, 0x2FCE, "B170", "D070") # Ignore the final tile data load
    
    rom.patch(0x3F, 0x0200, "00" * 0xA0, ASM("""
    ; Disable LCD
    xor a
    ldh  [$FF40], a
    
    ld  hl, $8000
    ld  de, $4400
copyLoop:
    ld  a, [de]
    inc de
    ldi [hl], a
    bit 4, h
    jr  z, copyLoop

    ld  a, $01
    ldh [$FF4F], a

    ld  hl, $8000
    ld  de, $5400
copyLoop2:
    ld  a, [de]
    inc de
    ldi [hl], a
    bit 4, h
    jr  z, copyLoop2

    ld  hl, $9800
    ld  de, $4400 + (20 * 18 * $10)
    ld  b, 18
copyAttrLoop2:
    ld  c, 20
copyAttrLoop1:
    ld  a, [de]
    inc de
    ldi [hl], a
    dec c
    jr  nz, copyAttrLoop1
    push de
    ld   de, 32 - 20
    add  hl, de
    pop  de
    dec b
    jr  nz, copyAttrLoop2

    xor  a
    ldh  [$FF4F], a

    ld  hl, $9800
    ld  de, $000C
    xor  a
loadLoop1:
    ldi  [hl], a
    ld   b, a
    ld   a, l
    and  $1F
    cp   $14
    jr   c, .noLineSkip
    add  hl, de
.noLineSkip:
    ld   a, b
    inc  a
    jr   nz, loadLoop1

loadLoop2:
    ldi  [hl], a
    ld   b, a
    ld   a, l
    and  $1F
    cp   $14
    jr   c, .noLineSkip
    add  hl, de
.noLineSkip:
    ld   a, b
    inc  a
    jr   nz, loadLoop2

    ; Load palette
    ld   hl, $DC10
    ld   de, $4400 + (20 * 18 * $10) + 20 * 18
    ld   c, 4 * 8 * 2
.copyPalLoop:
    ld   a, [de]
    inc  de
    ldi  [hl], a
    dec  c
    jr   nz, .copyPalLoop

    ld   a, $00
    ld   [$DDD3], a
    ld   a, $04
    ld   [$DDD4], a
    ld   a, $01
    ld   [$DDD1], a

    ; Enable LCD
    ld  a, $91
    ldh [$FF40], a
    ld  [$d6fd], a
    
    xor a
    ldh [$FF96], a
    ldh [$FF97], a
    ret
    """), fill_nop=True)

    cats = [f for f in os.listdir(os.path.join(os.path.dirname(__file__), "cats")) if f.endswith(".bin")]
    data = open(os.path.join(os.path.dirname(__file__), "cats", random.choice(cats)), "rb").read()
    assert len(data) < 0x2400
    rom.banks[0x3F][0x0400:0x0400+len(data)] = data
