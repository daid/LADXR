; Handle the multiworld link (mostly removed, but lolzols still use this)

MainLoop:
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

    call $280D ; GetRandomByte
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

    call $280D ; GetRandomByte
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

    call $280D ; GetRandomByte
    and  $1F
    ld   [wLinkSpawnDelay], a
    ret

placeRandom:
    ; Place somewhere random
    ld   hl, $C200
    add  hl, de
    call $280D ; GetRandomByte
    and  $7F
    add  a, $08
    ld   [hl], a
    ld   hl, $C210
    add  hl, de
    call $280D ; GetRandomByte
    and  $3F
    add  a, $20
    ld   [hl], a
    ret
