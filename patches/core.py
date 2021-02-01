from assembler import ASM
from roomEditor import RoomEditor
from backgroundEditor import BackgroundEditor


def bugfixWrittingWrongRoomStatus(rom):
    # The normal rom contains a pretty nasty bug where door closing triggers in D7/D8 can effect doors in
    # dungeons D1-D6. This fix should prevent this.
    rom.patch(0x02, 0x1D21, 0x1D3C, ASM("call $5B9F"), fill_nop=True)

def bugfixBossroomTopPush(rom):
    rom.patch(0x14, 0x14D9, ASM("""
        ldh  a, [$99]
        dec  a
        ldh  [$99], a
    """), ASM("""
        jp   $7F80
    """), fill_nop=True)
    rom.patch(0x14, 0x3F80, "00" * 0x80, ASM("""
        ldh  a, [$99]
        cp   $50
        jr   nc, up
down:
        inc  a
        ldh  [$99], a
        jp   $54DE
up:
        dec  a
        ldh  [$99], a
        jp   $54DE
    """), fill_nop=True)

def bugfixPowderBagSprite(rom):
    rom.patch(0x03, 0x2055, "8E16", "0E1E")

def removeGhost(rom):
    ## Ghost patch
    # Do not have the ghost follow you after dungeon 4
    rom.patch(0x03, 0x1E1B, ASM("LD [$DB79], A"), "", fill_nop=True)

def alwaysAllowSecretBook(rom):
    rom.patch(0x15, 0x3F23, ASM("ld a, [$DB0E]\ncp $0E"), ASM("xor a\ncp $00"), fill_nop=True)

def cleanup(rom):
    # Remove unused rooms to make some space in the rom
    re = RoomEditor(rom, 0x2C4)
    re.objects = []
    re.entities = []
    re.store(rom, 0x2C4)
    re.store(rom, 0x2D4)
    re.store(rom, 0x277)
    re.store(rom, 0x278)
    re.store(rom, 0x279)
    re.store(rom, 0x1ED)
    re.store(rom, 0x1FC)  # Beta room

    rom.texts[0x02B] = b'' # unused text

def quickswap(rom, button):
    rom.patch(0x00, 0x1094, ASM("jr c, $49"), ASM("jr nz, $49"))  # prevent agressive key repeat
    rom.patch(0x00, 0x10BC,  # Patch the open minimap code to swap the your items instead
        ASM("xor a\nld [$C16B], a\nld [$C16C], a\nld [$DB96], a\nld a, $07\nld [$DB95], a"), ASM("""
        ld a, [$DB%02X]
        ld e, a
        ld a, [$DB%02X]
        ld [$DB%02X], a
        ld a, e
        ld [$DB%02X], a
        ret
    """ % (button, button + 2, button, button + 2)))

def injectMainLoop(rom):
    rom.patch(0x00, 0x0346, ASM("""
        ldh  a, [$FE]
        and  a
        jr   z, $08
    """), ASM("""
        ; Call the mainloop handler
        xor  a
        rst  8
    """), fill_nop=True)

def warpHome(rom):
    # Patch the S&Q menu to allow 3 options
    rom.patch(0x01, 0x012A, 0x0150, ASM("""
        ld   hl, $C13F
        call $6BA8 ; make sound on keypress
        ldh  a, [$CC] ; load joystick status
        and  $04      ; if up
        jr   z, noUp
        dec  [hl]
noUp:
        ldh  a, [$CC] ; load joystick status
        and  $08      ; if down
        jr   z, noDown
        inc  [hl]
noDown:

        ld   a, [hl]
        cp   $ff
        jr   nz, noWrapUp
        ld   a, $02
noWrapUp:
        cp   $03
        jr   nz, noWrapDown
        xor  a
noWrapDown:
        ld   [hl], a
        jp   $7E02
    """), fill_nop=True)
    rom.patch(0x01, 0x3E02, 0x3E20, ASM("""
        swap a
        add  a, $48
        ld   hl, $C018
        ldi  [hl], a
        ld   a, $24
        ldi  [hl], a
        ld   a, $BE
        ldi  [hl], a
        ld   [hl], $00
        ret
    """), fill_nop=True)

    rom.patch(0x01, 0x00B7, ASM("""
        ld   a, [$C13F]
        cp   $01
        jr   z, $3B
    """), ASM("""
        ld   a, [$C13F]
        jp $7E20
    """), fill_nop=True)

    re = RoomEditor(rom, 0x2a3)
    warp = re.getWarps()[0]
    rom.patch(0x01, 0x3E20, 0x4000, ASM("""
        ; First, handle save & quit
        cp   $01
        jp   z, $40F9
        and  a
        jp   z, $40BE ; return to normal "return to game" handling

        ld   a, $0B
        ld   [$DB95], a
        call $0C7D

        ; Replace warp0 tile data, and put link on that tile.
        xor  a
        ld   [$D401], a
        ld   [$D402], a
        ld   a, $%02x ; Room
        ld   [$D403], a
        ld   a, $%02x ; X
        ld   [$D404], a
        ld   a, $%02x ; Y
        ld   [$D405], a

        ldh  a, [$98]
        swap a
        and  $0F
        ld   e, a
        ldh  a, [$99]
        sub  $08
        and  $F0
        or   e
        ld   [$D416], a

        ld   a, $07
        ld   [$DB96], a
        ret
        jp   $40BE  ; return to normal "return to game" handling
    """ % (warp.room, warp.target_x, warp.target_y)), fill_nop=True)


    # Patch the S&Q screen to have 3 options.
    be = BackgroundEditor(rom, 0x0D)
    for n in range(2, 18):
        be.tiles[0x99C0 + n] = be.tiles[0x9980 + n]
        be.tiles[0x99A0 + n] = be.tiles[0x9960 + n]
        be.tiles[0x9980 + n] = be.tiles[0x9940 + n]
        be.tiles[0x9960 + n] = be.tiles[0x98e0 + n]
    be.tiles[0x9960 + 10] = 0xCE
    be.tiles[0x9960 + 11] = 0xCF
    be.tiles[0x9960 + 12] = 0xC4
    be.tiles[0x9960 + 13] = 0x7F
    be.tiles[0x9960 + 14] = 0x7F
    be.store(rom)

    sprite_data = [
        0b00000000,
        0b01000100,
        0b01000101,
        0b01000101,
        0b01111101,
        0b01000101,
        0b01000101,
        0b01000100,

        0b00000000,
        0b11100100,
        0b00010110,
        0b00010101,
        0b00010100,
        0b00010100,
        0b00010100,
        0b11100100,
    ]
    for n in range(32):
        rom.banks[0x0F][0x08E0 + n] = sprite_data[n // 2]
