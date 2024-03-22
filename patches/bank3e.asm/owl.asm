HandleOwlStatue:
    call GetRoomStatusAddressInHL
    bit  5, [hl]
    ld   d, $01
    ret  nz
    set  5, [hl]

    ld   hl, $7B16
    call OffsetPointerByRoomNumber
    ld   a, [hl]
    ldh  [$FFF1], a
    call ItemMessage
    call GiveItemFromChest
    ld   d, $00
    ret



GetRoomStatusAddressInHL:
    ld   a, [$DBA5] ; isIndoor
    ld   d, a
    ld   hl, $D800
    ldh  a, [$FFF6]   ; room nr
    ld   e, a
    ldh  a, [$FFF7]   ; map nr
    cp   $FF
    jr   nz, .notColorDungeon

    ld   d, $00
    ld   hl, $DDE0
    jr   .notIndoorB

.notColorDungeon:
    cp   $1A
    jr   nc, .notIndoorB

    cp   $06
    jr   c, .notIndoorB

    inc  d

.notIndoorB:
    add  hl, de
    ret


RenderOwlStatueItem:
    ld   hl, $7B16
    call OffsetPointerByRoomNumber
    ld   a, [hl]
    ldh  [$FFF1], a
    jp   RenderChestItem
