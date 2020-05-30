TakeHeart:
    ld   hl, $DB5B
    dec  [hl]
    ld   a, [hl]
    rlca
    rlca
    rlca
    sub  $01
    ld   hl, $DB5A
    cp   [hl]
    jr   nc, .noNeedToReduceHp
    ld   [hl], a
.noNeedToReduceHp:
    ld   hl, $DB93
    ld   [hl], $FF
    jp Exit
