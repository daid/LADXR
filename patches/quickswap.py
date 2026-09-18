from assembler import ASM

def simple_quickswap(rom, button):
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

def dynamic_quickswap(rom, settings):
    rom.patch(0x00, 0x3E47, ASM("call $6414"), ASM("""
        call $7D00
    """)) # when drawing the current hearts and rupees, also draw the Quickswap arrow

    rom.patch(0x02, 0x3D00, "00" * 8, ASM("""
        call $6414
        ld   a, $16 ; QuickswapDraw
        rst  8
        ret
    """), fill_nop=True)

    rom.patch(0x00, 0x1258, ASM("ld a, [$DB00]"), ASM("""
        call $7D08
    """)) # when using the B item, move it to the front of the list and put the arrow on the A button

    rom.patch(0x02, 0x3D08, "00" * 8, ASM("""
        ld   a, $17 ; QuickswapResetB
        rst  8
        ld   a, [$DB00]
        ret
    """), fill_nop=True)

    rom.patch(0x00, 0x126F, ASM("ld a, [$DB01]"), ASM("""
        call $7D10
    """)) # when using the A item, move it to the front of the list and put the arrow on the B button

    rom.patch(0x02, 0x3D10, "00" * 8, ASM("""
        ld   a, $18 ; QuickswapResetA
        rst  8
        ld   a, [$DB01]
        ret
    """), fill_nop=True)

    # When equipping an item from the menu, move it to the front of the respective list
    rom.patch(0x20, 0x2007, ASM("ld c, $00\nld b, $00"), ASM("call $6020"), fill_nop=True)
    rom.patch(0x20, 0x1FE5, ASM("ld c, $01\nld b, $00"), ASM("call $6028"), fill_nop=True)
    rom.patch(0x20, 0x2020, 0x2028, ASM("""
        ld   a, $19 ; QuickswapResetMenuB
        rst  8
        ld   c, $00
        ld   b, c
        ret
    """), fill_nop=True)
    rom.patch(0x20, 0x2028, 0x2036, ASM("""
        ld   a, $1A ; QuickswapResetMenuA
        rst  8
        ld   c, $01
        ld   b, $00
        ret
    """), fill_nop=True)

    rom.patch(0x03, 0x247E, ASM("ld hl, $DB00"), ASM("""
        call $50C6
    """)) # when obtaining a new item, put it at the front of the lists

    rom.patch(0x03, 0x10C6, "00" * 25, ASM("""
        push bc
        push de
        ld   c, d
        ld   a, [$DBAF]
        push af
        ld   a, $03
        ld   [$DBAF], a
        ld   a, $1B ; QuickswapResetOnNewItem
        rst  8
        pop  af
        ld   [$DBAF], a
        pop  de
        pop  bc
        ld   hl, $DB00
        ret
    """), fill_nop=True)

    rom.patch(0x00, 0x1081, ASM("and $B0"), ASM("and $80")) # enable use of Quickswap while A or B is pressed

    rom.patch(0x00, 0x1092, ASM("cp $04"), ASM("cp $01")) # trigger on first instead of fourth frame of holding Select

    rom.patch(0x00, 0x10BC, # patch the open minimap code to swap your items instead
        ASM("xor a\nld [$C16B], a\nld [$C16C], a\nld [$DB96], a\nld a, $07\nld [$DB95], a"), ASM("""
        ld   a, $1C ; Quickswap
        rst  8
        jp   $10DF
    """), fill_nop=True)

    # When Select is being held, but the Quickswap action interrupted, do not trigger a new Quickswap as soon as it becomes available again
    rom.patch(0x00, 0x109A, ASM("jr z, $3F"), ASM("jr z, $2F"))
    rom.patch(0x00, 0x10A0, ASM("jr z, $39"), ASM("jr z, $29"))
    rom.patch(0x00, 0x10A7, ASM("jr nc, $32"), ASM("jr nc, $22"))
    rom.patch(0x00, 0x10B4, ASM("jr nz, $25"), ASM("jr nz, $15"))
    rom.patch(0x00, 0x10BA, ASM("jr nz, $1F"), ASM("jr nz, $0F"))
    rom.patch(0x00, 0x10CB, ASM("ld a, $02\nld [$2100], a\ncall $755B"), ASM("""
        ld   a, $15
        ld   [$D45F], a
        jp   $10DF
    """), fill_nop=True)

    rom.patch(0x01, 0x138E, ASM("ld a, $02\nld [$D6FF], a\nret"), ASM("""
        ld   a, $20 ; QuickswapResetOnFileLoad
        rst  8
        ret
    """), fill_nop=True) # when loading a file, ensure the currently equipped items are at the front of the respective lists

    rom.patch(0x20, 0x1AFD, ASM("ldh a, [$FFFE]\nand a\njr z, $3B"), ASM("""
        ld   a, $1D ; QuickswapRemoveArrow
        rst  8
    """), fill_nop=True) # remove the arrow when the inventory is opened

    rom.patch(0x00, 0x20F4, ASM("ld a, $01\nldh [$FFA1], a"), ASM("""
        ld   a, $1E ; QuickswapResetOnGrab
        rst  8
    """), fill_nop=True) # grab something using the Power Bracelets

    if settings.boomerang != "gift":
        rom.patch(0x19, 0x06D5, ASM("ld a, $10\nld [$D368], a\nret"), ASM("""
            ld   a, [$DB00]
            jp   $7F70
        """), fill_nop=True) # trade an item for the boomerang

        rom.patch(0x19, 0x071F, ASM("ld a, $10\nld [$D368], a\nret"), ASM("""
            ld   a, [$DB7D]
            jp   $7F70
        """), fill_nop=True) # trade the boomerang back

        rom.patch(0x19, 0x3F70, "00" * 0x10, ASM("""
            push bc
            ld   c, a
            ld   a, $10
            ld   [$D368], a
            ld   a, $1B ; QuickswapResetOnNewItem
            rst  8
            pop  bc
            ret
        """), fill_nop=True)

    # Draw a preview for the next equippable items by using Quickswap
    rom.patch(0x20, 0x1CAD, ASM("ldh a, [$FFFE]\nand a\njr z, $03"), ASM("""
        call $7F90
    """), fill_nop=True) # load the next items in the rotations and update the tile attributes

    rom.patch(0x20, 0x3F90, "00" * 0x30, ASM("""
        ld   a, c
        cp   $02
        ret  nc
        push bc
        ld   a, [$DBAF]
        push af
        ld   a, $20
        ld   [$DBAF], a
        dec  a ; QuickswapUpdatePreview
        rst  8
        pop  af
        ld   [$DBAF], a
        pop  bc
        push bc
        ld   a, c
        and  a
        jr   nz, updateASlot
        ld   de, wQuickswapPreviewB1
        ld   bc, $9C02
        call $7FC0
        pop  bc
        ret

    updateASlot:
        ld   de, wQuickswapPreviewA1
        ld   bc, $9C07
        call $7FC0
        pop  bc
        ret
    """), fill_nop=True)

    rom.patch(0x20, 0x3FC0, "00" * 0x21, ASM("""
        push de
        ld   a, [$DC90]
        ld   e, a
        ld   d, $00
        ld   hl, $DC91
        add  hl, de
        add  $05
        ld   [$DC90], a
        ld   a, b
        ldi  [hl], a
        ld   a, c
        ldi  [hl], a
        ld   a, $01
        ldi  [hl], a
        pop  de
        call $7FE1
        call $7FE1
        xor  a
        ld   [hl], a
        ret
    """), fill_nop=True)

    rom.patch(0x20, 0x3FE1, "00" * 0x1F, ASM("""
        ld   a, [de]
        inc  de
        cp   $03
        jr   nz, notLevel2Bracelet
        ld   a, [$DB43]
        cp   $02
        jr   nz, notLevel2Bracelet
        ldi  [hl], a
        ret
    notLevel2Bracelet:
        sla  a
        ld   c, a
        push hl
        ld   hl, $5C14
        ld   b, $00
        add  hl, bc
        ld   b, h
        ld   c, l
        pop  hl
        ld   a, [bc]
        ldi  [hl], a
        ret
    """), fill_nop=True)

    rom.patch(0x20, 0x1CE5, ASM("ld a, [de]\ninc de\nldi [hl], a\nld a, [de]\ninc de\nldi [hl], a"), ASM("""
        jp $7EC0
    """), fill_nop=True) # draw the item tiles

    rom.patch(0x20, 0x3EB0, "00" * 16, ASM("""
        ld   bc, $5C36
        sla  a
        ld   e, a
        sla  a
        add  e
        add  c ; should not overflow
        ld   c, a
        ld   a, [bc]
        ldi  [hl], a
        ret
    """), fill_nop=True)

    rom.patch(0x20, 0x3EC0, "00" * 64, ASM("""
        pop  bc
        push bc
        ld   a, c
        and  a
        jr   z, bSlot
        dec  a
        jr   z, aSlot
        ld   a, [de]
        inc  de
        ldi  [hl], a
        ld   a, [de]
        inc  de
        ldi  [hl], a
        jp   $5CEB
    bSlot:
        push de
        ld   a, [wQuickswapPreviewB1]
        call $7EB0
        ld   a, [wQuickswapPreviewB2]
        call $7EB0
        jr   end
    aSlot:
        push de
        ld   a, [wQuickswapPreviewA1]
        call $7EB0
        ld   a, [wQuickswapPreviewA2]
        call $7EB0
    end:
        pop  de
        inc  de
        inc  de
        jp   $5CEB
    """), fill_nop=True)