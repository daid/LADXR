evilShopItemNames:
    dw M"100 to 200 Rupees"
    dw M"1 to 3 Seashells"
    dw M"Random key"

evilShopPostMessage:
    db "for one heart   container?          Yes  No", $ff

EvilShopQuestion:
    ld   a, [$C509] ; carry item
    add  a, a
    jr   z, .noItem ; check if we have something to buy
    sub  $02

    ld   hl, evilShopItemNames
    ld   e, a
    ld   d, b ; b=0
    add  hl, de
    ld   a, [hl+]
    ld   h, [hl]
    ld   l, a

    ld   de, wCustomMessage
    call MessageCopyString
    call MessagePad
    ld   hl, evilShopPostMessage
    call MessageCopyString
    ld   a, $fe
    ld   [de], a

    ld   a, $C9
    call OpenDialogInTable0
    call IncrementEntityState
    ret

.noItem:
    ld   hl, M"He he he. Want to buy something with your life?"

EvilShopDisplaySimpleMessage:
    ld   de, wCustomMessage
    call MessageCopyString
    ld   a, $C9
    call OpenDialogInTable0
    ret

EvilShopBuy:
    ld   a, [$DB5B]
    cp   $01
    ld   hl, M"I cannot take your last heart."
    jr   z, EvilShopDisplaySimpleMessage
    call TakeHeart

    ld   hl, $C509 ; carry item
    ld   a, [hl]
    dec  a
    ld   [hl], 0
    rst  0
    dw   .Rupees
    dw   .Seashell
    dw   .Key

.Rupees:
    call GetRandomByte
    cp   100
    jr   nc, .Rupees
    add  100
    ld   [wAddRupeeBufferLow], a
    ld   hl, M"Some rupees for you, enjoy. He he he..."
    jp   EvilShopDisplaySimpleMessage

.Seashell:
    call GetRandomByte
    and  3
    jr   z, .Seashell

    ld   h, a
    ld   a, [wSeashellsCount]
    add  a, h
    daa
    ld   [wSeashellsCount], a

    ld   hl, M"Seashells for you, enjoy. He he he..."
    jp   EvilShopDisplaySimpleMessage

.Key:
    call GetRandomByte
    and  $0F
    cp   9 ; D1-D8/D0
    jr   nc, .Key

    push af
    ld   de, $0004
    call AddDungeonItem

    ld   hl, M"DX key for you! He he he..."
    ld   de, wCustomMessage
    call MessageCopyString

    pop  af
    cp   8 ; D0
    jr   nz, .NotKeyD0
    ld   a, $FF
.NotKeyD0:
    add  $31
    ld   [wCustomMessage+1], a ; Set the dungeon key number

    ld   a, $C9
    call OpenDialogInTable0
    ret
