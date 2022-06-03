HandleOwlStatue:
    call GetRoomStatusAddressInHL
    ld   a, [hl]
    and  $20
    ret  nz
    ld   a, [hl]
    or   $20
    ld   [hl], a

    ld   hl, $7B16
    call OffsetPointerByRoomNumber
    ld   a, [hl]
    ldh  [$F1], a
    call ItemMessage
    call GiveItemFromChest
    ret



GetRoomStatusAddressInHL:
    ld   a, [$DBA5] ; isIndoor
    ld   d, a
    ld   hl, $D800
    ldh  a, [$F6]   ; room nr
    ld   e, a
    ldh  a, [$F7]   ; map nr
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
    ldh  [$F1], a
    jp   RenderChestItem
