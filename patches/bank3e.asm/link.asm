InitLink:
    ; Switch on the link port in receive mode with interrupts enabled.
    ld   a, $0F
    ldh  [$01], a
    ld   a, $82
    ldh  [$02], a
    ld   a, $09
    ldh  [$FF], a

    ld   a, $01     ; switch to RunLink
    ld   [$CEFF], a
    ret

RunLink:
    ; Load the command byte, and only continue if there is a command.
    ld   a, [$CEFE]
    and  a
    ret  z

    ; Reset our command byte to zero, and set HL to point at the data byte
    ld   hl, $CEFE
    ld   b, $00
    ld   [hl], b

    and  $0F
    rst  0
    dw   LinkTestMessage
    dw   LinkItem

LinkTestMessage:
    ld   a, $41
    call $3273 ; open dialog in table 1
    ret

LinkItem:
    ld   a, [$CEFD] ; get data byte
    ldh  [$F1], a
    call GiveItemFromChestNoLink
    call ItemMessageNoLink
    ret


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

