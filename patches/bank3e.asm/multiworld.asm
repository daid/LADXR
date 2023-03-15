; Handle the multiworld link

MainLoop:
#IF HARDWARE_LINK
    call handleSerialLink
#ENDIF
    ; Check if the gameplay is world
    ld   a, [$DB95]
    cp   $0B
    ret  nz
    ; Check if the world subtype is the normal one
    ld   a, [$DB96]
    cp   $07
    ret  nz
    ; Check if we are moving between rooms
    ld   a, [$C124]
    and  a
    ret  nz
    ; Check if link is in a normal walking/swimming state
    ld   a, [$C11C]
    cp   $02
    ret  nc
    ; Check if a dialog is open
    ld   a, [$C19F]
    and  a
    ret  nz
    ; Check if interaction is blocked
    ldh  a, [$FFA1]
    and  a
    ret  nz

    ld   a, [wLinkSpawnDelay]
    and  a
    jr   z, .allowSpawn
    dec  a
    ld   [wLinkSpawnDelay], a
    jr   .noSpawn

.allowSpawn:
    ld   a, [wZolSpawnCount]
    and  a
    call nz, LinkSpawnSlime
    ld   a, [wCuccoSpawnCount]
    and  a
    call nz, LinkSpawnCucco
    ld   a, [wDropBombSpawnCount]
    and  a
    call nz, LinkSpawnBomb
.noSpawn:

    ; Have an item to give?
    ld   hl, wLinkStatusBits
    bit  0, [hl]
    ret  z

    ; Give an item to the player
    ld   a, [wLinkGiveItem]
    cp   $22 ; zol item
    jr   z, LinkGiveSlime
    cp   $F0
    jr   nc, HandleSpecialItem
    ldh  [$FFF1], a
    call GiveItemFromChest
    call BuildItemMessage
    call MessageAddFromPlayer
    dec  de
    ld   a, [wLinkGiveItemFrom]
    add  a, $31 ; '1'
    ld   [de], a
    ld   a, $C9
    ld   hl, wLinkStatusBits
    res  0, [hl]
    jp   $2385 ; Opendialog in $000-$0FF range

LinkGiveSlime:
    ld   a, $05
    ld   [wZolSpawnCount], a
    ld   hl, wLinkStatusBits
    res  0, [hl]
    ret

HandleSpecialItem:
    ld   hl, wLinkStatusBits
    res  0, [hl]

    and  $0F
    rst  0
    dw SpecialSlimeStorm
    dw SpecialCuccoParty
    dw SpecialPieceOfPower
    dw SpecialHealth
    dw SpecialRandomTeleport
    dw .ret
    dw .ret
    dw .ret
    dw .ret
    dw .ret
    dw .ret
    dw .ret
    dw .ret
    dw .ret
    dw .ret
    dw .ret
.ret:
    ret

SpecialSlimeStorm:
    ld   a, $20
    ld   [wZolSpawnCount], a
    ret
SpecialCuccoParty:
    ld   a, $20
    ld   [wCuccoSpawnCount], a
    ret
SpecialPieceOfPower:
    ; Give the piece of power and the music
    ld   a, $01
    ld   [$D47C], a
    ld   a, $27
    ld   [$D368], a
    ld   a, $49
    ldh  [$FFBD], a
    ldh  [$FFBF], a
    ret
SpecialHealth:
    ; Regen all health
    ld   hl, $DB93
    ld   [hl], $FF
    ret

LinkSpawnSlime:
    ld   a, $1B
    ld   e, $08
    call $3B98 ; SpawnNewEntity in range
    ret  c

    ; Place somewhere random
    call placeRandom

    ld   hl, $C310
    add  hl, de
    ld   [hl], $7F

    ld   hl, wZolSpawnCount
    dec  [hl]

    call $280D
    and  $03
    ld   [wLinkSpawnDelay], a
    ret

LinkSpawnCucco:
    ld   a, $6C
    ld   e, $04
    call $3B98 ; SpawnNewEntity in range
    ret  c

    ; Place where link is at.
    ld   hl, $C200
    add  hl, de
    ldh  a, [$FF98]
    ld   [hl], a
    ld   hl, $C210
    add  hl, de
    ldh  a, [$FF99]
    ld   [hl], a

    ; Set the "hits till cucco killer attack" much lower
    ld   hl, $C2B0
    add  hl, de
    ld   a, $21
    ld   [hl], a

    ld   hl, wCuccoSpawnCount
    dec  [hl]

    call $280D
    and  $07
    ld   [wLinkSpawnDelay], a
    ret

LinkSpawnBomb:
    ld   a, $02
    ld   e, $08
    call $3B98 ; SpawnNewEntity in range
    ret  c

    call placeRandom

    ld   hl, $C310 ; z pos
    add  hl, de
    ld   [hl], $4F

    ld   hl, $C430 ; wEntitiesOptions1Table
    add  hl, de
    res  0, [hl]
    ld   hl, $C2E0 ; wEntitiesTransitionCountdownTable
    add  hl, de
    ld   [hl], $80
    ld   hl, $C440 ; wEntitiesPrivateState4Table
    add  hl, de
    ld   [hl], $01

    ld   hl, wDropBombSpawnCount
    dec  [hl]

    call $280D
    and  $1F
    ld   [wLinkSpawnDelay], a
    ret

placeRandom:
    ; Place somewhere random
    ld   hl, $C200
    add  hl, de
    call $280D ; random number
    and  $7F
    add  a, $08
    ld   [hl], a
    ld   hl, $C210
    add  hl, de
    call $280D ; random number
    and  $3F
    add  a, $20
    ld   [hl], a
    ret

SpecialRandomTeleport:
    xor  a
    ; Warp data
    ld   [$D401], a
    ld   [$D402], a
    call $280D ; random number
    ld   [$D403], a
    ld   hl, RandomTeleportPositions
    ld   d, $00
    ld   e, a
    add  hl, de
    ld   e, [hl]
    ld   a, e
    and  $0F
    swap a
    add  a, $08
    ld   [$D404], a
    ld   a, e
    and  $F0
    add  a, $10
    ld   [$D405], a

    ldh  a, [$FF98]
    swap a
    and  $0F
    ld   e, a
    ldh  a, [$FF99]
    sub  $08
    and  $F0
    or   e
    ld   [$D416], a ; wWarp0PositionTileIndex

    call $0C7D
    ld   a, $07
    ld   [$DB96], a ; wGameplaySubtype

    ret

RandomTeleportPositions:
    db $55, $54, $54, $54, $55, $55, $55, $54, $65, $55, $54, $65, $56, $56, $55, $55
    db $55, $45, $65, $54, $55, $55, $55, $55, $55, $55, $55, $58, $43, $57, $55, $55
    db $55, $55, $55, $55, $55, $54, $55, $53, $54, $56, $65, $65, $56, $55, $57, $65
    db $45, $55, $55, $55, $55, $55, $55, $55, $48, $45, $43, $34, $35, $35, $36, $34
    db $65, $55, $55, $54, $54, $54, $55, $54, $56, $65, $55, $55, $55, $55, $54, $54
    db $55, $55, $55, $55, $56, $55, $55, $54, $55, $55, $55, $53, $45, $35, $53, $46
    db $56, $55, $55, $55, $53, $55, $54, $54, $55, $55, $55, $54, $44, $55, $55, $54
    db $55, $55, $45, $55, $55, $54, $45, $45, $63, $55, $65, $55, $45, $45, $44, $54
    db $56, $56, $54, $55, $54, $55, $55, $55, $55, $55, $55, $56, $54, $55, $65, $56
    db $54, $54, $55, $65, $56, $54, $55, $56, $55, $55, $55, $66, $65, $65, $55, $56
    db $65, $55, $55, $75, $55, $55, $55, $54, $55, $55, $65, $57, $55, $54, $53, $45
    db $55, $56, $55, $55, $55, $45, $54, $55, $54, $55, $56, $55, $55, $55, $55, $54
    db $55, $55, $65, $55, $55, $54, $53, $58, $55, $05, $58, $55, $55, $55, $74, $55
    db $55, $55, $55, $55, $46, $55, $55, $56, $55, $55, $55, $54, $55, $45, $55, $55
    db $55, $55, $54, $55, $55, $55, $65, $55, $55, $46, $55, $55, $56, $55, $55, $55
    db $55, $55, $54, $55, $55, $55, $45, $36, $53, $51, $57, $53, $56, $54, $45, $46
