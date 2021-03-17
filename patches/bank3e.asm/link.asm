; Handle the multiworld link

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
    ldh  a, [$A1]
    and  a
    ret  nz

    ; Have an item to give?
    ld   hl, wLinkStatusBits
    bit  0, [hl]
    ret  z

    ; Give an item to the player
    ld   a, [wLinkGiveItem]
    cp   $22 ; zol item
    jp   z, LinkSpawnSlime
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
