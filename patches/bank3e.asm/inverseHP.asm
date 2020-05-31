; Some code that gets injected into the heart containers if you have inverted HP mode.
; We need to take special care, as the game crashes if HP > maxHP
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
    ret
