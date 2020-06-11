LinkSendByte:
    ld   e, a
.repeat:
    ld   a, e
    ldh  [$01], a
    ld   a, $83
    ldh  [$02], a
.sendWait:
    ldh  a, [$02]
    and  $80
    jr   nz, .sendWait
    ldh  a, [$01]
    cp   $0F ; Check if our byte is acknowledged.
    jr   nz, .repeat

    ; Back to receive mode
    ld   a, $0F
    ldh  [$01], a
    ld   a, $82
    ldh  [$02], a

    ret

InitLink:
    ; Switch on the link port in receive mode with interrupts enabled.
    ld   a, $0F
    ldh  [$01], a
    ld   a, $82
    ldh  [$02], a

    ld   a, $01     ; switch to RunLink
    ld   [$CEFF], a
    ret

RunLink:
    ; Received a new byte on the link?
    ldh  a, [$02]
    and  $80
    ret  nz

    ; Get the byte and check if it is a command (0xF0-0xFF) or data (0x00-0xEF)
    ldh  a, [$01]

    ; Reset the receiver to receive the next byte
    ld   e, a
    ld   a, $0F
    ldh  [$01], a
    ld   a, $82
    ldh  [$02], a
    ld   a, e

    cp   $F0
    jr   c, .dataByte

    and  $0F
    rst  0
    dw   LinkTestMessage
    dw   LinkItem
    dw   LinkEffect

.dataByte:
    ld   [$CEFE], a ; set data byte
    ret

LinkTestMessage:
    ld   a, $41
    call $2373 ; open dialog in table 1
    ret

LinkItem:
    ld   a, [$CEFE] ; get data byte
    ldh  [$F1], a
    call GiveItemFromChestNoLink
    call ItemMessageNoLink
    ret

LinkEffect:
    ld   a, [$CEFE] ; get data byte
    rst  0
    dw   LinkGive100Rupees
    dw   LinkTake100Rupees
    dw   LinkGiveHealth
    dw   LinkTakeHealth
    dw   LinkSpawnSlime
    dw   LinkSpawnCucco

LinkGive100Rupees:
    ld   a, [$DB90]
    add  a, $64
    ld   [$DB90], a
    ld   a, [$DB8F]
    adc  a, $00
    ld   [$DB8F], a
    ret

LinkTake100Rupees:
    ld   a, [$DB92]
    add  a, $64
    ld   [$DB92], a
    ld   a, [$DB91]
    adc  a, $00
    ld   [$DB91], a
    ret

LinkGiveHealth:
    ld   a, [$DB93]
    add  a, $08
    ld   [$DB93], a
    ret

LinkTakeHealth:
    ld   a, [$DB94]
    add  a, $08
    ld   [$DB94], a
    ret

LinkSpawnSlime:
    ld   a, $1B
    ld   e, $0A
    call $3B98 ; SpawnNewEntity in range
    ret  c

    ; Place somewhere random
    ld   hl, $C200
    add  hl, de
    call $280D
    and  $7F
    add  a, $08
    ld   [hl], a
    ld   hl, $C210
    add  hl, de
    call $280D
    and  $7F
    ld   [hl], a

    ld   hl, $C310
    add  hl, de
    ld   [hl], $7F

    ret

LinkSpawnCucco:
    ld   a, $6C
    ld   e, $0A
    call $3B98 ; SpawnNewEntity in range
    ret  c

    ; Place where link is at.
    ld   hl, $C200
    add  hl, de
    ldh  a, [$98]
    ld   [hl], a
    ld   hl, $C210
    add  hl, de
    ldh  a, [$99]
    ld   [hl], a

    ret
