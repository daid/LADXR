
NightmareMinibossHandler:
    ldh  a, [hActiveEntityState]
    rst  0
    dw   stateInit
    dw   stateCheck

stateInit:
    call IncrementEntityState

    ld   a, $50 ; MUSIC_MINIBOSS
    ld   [wMusicTrackToPlay], a

    call getBossType
    ld   hl, wEntitiesPrivateState1Table
    add  hl, bc
    ld   [hl], a
    and  $7F
    rst  0
    dw   createGel
    dw   createAgahnim
    dw   createMoldorm
    dw   createGanon
    dw   createLanmola

createGel:
    ld   a, 1
    jp   spawnNightmare
createAgahnim:
    ld   a, 2
    jp   spawnNightmare
createMoldorm:
    ld   a, 3
    jp   spawnNightmare
createGanon:
    ld   a, 4
    jp   spawnNightmare
createLanmola:
    ld   a, 4
    call spawnNightmare
    ld   hl, wEntitiesStateTable
    add  hl, de
    ld   [hl], $0A
    ret

spawnNightmare:
    ld   [wFinalNightmareForm], a
    ld   a, $E6 ; ENTITY_FINAL_NIGHTMARE
    call $3B86 ; SpawnNewEntity_trampoline
    ld   hl, wEntitiesPosXTable
    add  hl, de
    ldh  a, [hActiveEntityPosX]
    ld   [hl], a
    ld   hl, wEntitiesPosYTable
    add  hl, de
    ldh  a, [hActiveEntityPosY]
    ld   [hl], a
    xor  a
    ld   [$C116], a
    ld   hl, wEntitiesPrivateState2Table
    add  hl, bc
    ld   [hl], e
    ret

stateCheck:
    ld   hl, wEntitiesPrivateState1Table
    add  hl, bc
    ld   a, [hl]
    and  $7F
    rst  0
    dw   checkGel
    dw   checkAgahnim
    dw   checkMoldorm
    dw   checkGanon
    dw   checkLanmola

checkGel:
    ld   e, 1
    jr   checkNightmareBoss
checkAgahnim:
    ld   e, 2
    jr   checkNightmareBoss
checkMoldorm:
    ld   e, 3
    jr   checkNightmareBoss
checkGanon:
    ld   hl, wEntitiesPrivateState2Table
    add  hl, bc
    ld   e, [hl]
    ld   d, b
    ld   hl, wEntitiesStateTable
    add  hl, de
    ld   a, [hl]
    cp   $0A
    ret  c
    jp   finalNightmareBossEnd
checkLanmola:
    ld   e, 4
    jr   checkNightmareBoss

checkNightmareBoss:
    ld   a, [wFinalNightmareForm]
    cp   e
    ret  z
    jp   finalNightmareBossEnd


finalNightmareBossEnd:
    ld   e, $0F
    ld   d, b
.loop:
    ld   hl, wEntitiesTypeTable
    add  hl, de
    ld   a, [hl]
    cp   $E6
    jr   nz, .skip
    ld   hl, wEntitiesStatusTable
    add  hl, de
    ld   [hl], 0
.skip:
    dec  e
    ld   a, e
    cp   $FF
    jr   nz, .loop

    ldh  a, [hDefaultMusicTrack]
    ld   [wMusicTrackToPlay], a

    ld   hl, wEntitiesPrivateState1Table
    add  hl, bc
    ld   a, [hl]
    and  $80
    call nz, createHeartContainer
    jp   UnloadEntity

getBossType:
    ld   hl, $7E33 ; table of nightmare boss mapping
    ld   b, [hl]
    ldh  a, [hMapRoom]
    ld   e, a
    ld   a, [wIsIndoor]
    ld   d, a
    ldh  a, [hMapId]
    cp   $ff ; color dungeon
    call z, .inc_d
    cp   $1A
    jr   nc, .indoorA
    cp   $06
    jr   c, .indoorA
    inc  d
.indoorA:

.loop:
    inc  hl
    ld   a, [hl+]
    cp   d
    ld   a, [hl+]
    jr   nz, .skip
    cp   e
    jr   nz, .skip

    ld   a, [hl]
    ld   b, 0
    ret

.skip:
    dec  b
    jr   nz, .loop
    xor  a
    ret

.inc_d:
    inc  d
    ret

createHeartContainer:
    ld   a, $36 ; ENTITY_HEART_CONTAINER
    call $3B86 ; SpawnNewEntity_trampoline
    ld   hl, wEntitiesPosXTable
    add  hl, de
    ldh  a, [hActiveEntityPosX]
    ld   [hl], a
    ld   hl, wEntitiesPosYTable
    add  hl, de
    ldh  a, [hActiveEntityPosY]
    ld   [hl], a
    ret
