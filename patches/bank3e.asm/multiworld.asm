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
    ldh  a, [$A1]
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
    ldh  [$F1], a
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
    jr   z, SpecialSlimeStorm
    dec  a
    jr   z, SpecialCuccoParty
    dec  a
    jr   z, SpecialPieceOfPower
    dec  a
    jr   z, SpecialHealth
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
    ldh  [$BD], a
    ldh  [$BF], a
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
    ret

LinkSpawnCucco:
    ld   a, $6C
    ld   e, $08
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

    ld   hl, wCuccoSpawnCount
    dec  [hl]

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
    call $280D
    and  $7F
    add  a, $08
    ld   [hl], a
    ld   hl, $C210
    add  hl, de
    call $280D
    and  $3F
    add  a, $20
    ld   [hl], a
    ret