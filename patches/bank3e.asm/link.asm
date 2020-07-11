; Handle the link cable
; Request status > $EE            $..
;                < $[STATUS_BITS] $[RES_SEQ]
; SendItem       > $E0            $[ITEM] $[PLAYER]
;                < $[STATUS_BITS] $00     $00
; GetItem        > $E1            $..          $..         $..       $..
;                < $[STATUS_BITS] $[ROOM_HIGH] $[ROOM_LOW] $[TARGET] $[ITEM]
; GetID          > $E2            $..    $..    $..    $..    $..
;                < $[STATUS_BITS] $[ID1] $[ID2] $[ID3] $[ID4] $[PLAYER_ID]

MainLoop:
    ; Check if the gameplay is world
    ld   a, [$DB95]
    cp   $0B
    jr   nz, .readLinkCable
    ; Check if the world subtype is the normal one
    ld   a, [$DB96]
    cp   $07
    jr   nz, .readLinkCable
    ; Check if we are moving between rooms
    ld   a, [$C124]
    and  a
    jr   nz, .readLinkCable
    ; Check if link is in a normal walking/swimming state
    ld   a, [$C11C]
    cp   $02
    jr   nc, .readLinkCable
    ; Check if a dialog is open
    ld   a, [$C19F]
    and  a
    jr   nz, .readLinkCable
    ; Check if interaction is blocked
    ldh  a, [$A1]
    and  a
    jr   nz, .readLinkCable

    ; Have an item to give?
    ld   a, [wLinkStatusBits]
    bit  0, a
    jr   z, .readLinkCable
    and  $FE
    ld   [wLinkStatusBits], a

    ; Give it
    ld   a, [wLinkGiveItem]
    cp   $22 ; zol item
    jp   z, LinkSpawnSlime
    ldh  [$F1], a
    call GiveItemFromChest
    call BuildItemMessage
    call MessageAddFromPlayer
    ; TODO: append ' from [player]' to message
    ld   a, $C9
    jp   $2385 ; Opendialog in $000-$0FF range

.readLinkCable:
    ld   a, [wLinkState] ; Get our LinkState
    rst  0
    dw   LinkInit ; 00
    dw   LinkNewCommand ; 01
    dw   LinkHandleSync ; 02
    dw   LinkHandleGiveItem ; 03
    dw   LinkHandleGiveItemFrom ; 04
    dw   LinkHandleSendItemRoomHigh ; 05
    dw   LinkHandleSendItemRoomLow  ; 06
    dw   LinkHandleSendItemTarget ; 07
    dw   LinkHandleSendItemItem ; 08
    dw   LinkHandleSendID1 ; 09
    dw   LinkHandleSendID2 ; 0A
    dw   LinkHandleSendID3 ; 0B
    dw   LinkHandleSendID4 ; 0C
    dw   LinkHandleSendPlayerID ; 0D

LinkInit:
    ld   a, $01     ; switch to LinkNewCommand
    ld   [wLinkState], a

    ; Get the game state to see if a save is loaded or not
    ld   a, [$DB95]
    cp   $06

    ; Switch on the link port in receive mode with interrupts enabled.
    ld   a, [wLinkStatusBits]
    jr   nc, .gotSaveLoaded
    or   $80
.gotSaveLoaded:
    or   $40

LinkStoreReply:
    ldh  [$01], a
    ld   a, $82
    ldh  [$02], a
    ret

LinkNewCommand:
    ; Received a new byte on the link?
    ldh  a, [$02]
    and  $80
    ret  nz

    ; Get the byte and check if it is a command (0xF0-0xFF) or data (0x00-0xEF)
    ldh  a, [$01]

    cp   $EE
    jr   z, LinkSetupSync
    cp   $E0
    jr   z, LinkSetupGiveItem
    cp   $E1
    jr   z, LinkSetupSendItem
    cp   $E2
    jp   z, LinkSetupSendID

    jp   LinkInit

LinkSetupSync:
    ld   a, $02
    ld   [wLinkState], a
    ld   a, [wLinkSyncSequenceNumber]
    jp   LinkStoreReply

LinkHandleSync:
    ; Received a new byte on the link?
    ldh  a, [$02]
    and  $80
    ret  nz

    ; Ignore the received byte
    jp   LinkInit


LinkSetupGiveItem:
    ld   a, $03
    ld   [wLinkState], a
    xor  a
    jp   LinkStoreReply

LinkHandleGiveItem:
    ; Received a new byte on the link?
    ldh  a, [$02]
    and  $80
    ret  nz

    ldh  a, [$01] ; get data byte
    ld   [wLinkGiveItem], a
    ld   a, $04
    ld   [wLinkState], a
    xor  a
    jp   LinkStoreReply

LinkHandleGiveItemFrom:
    ; Received a new byte on the link?
    ldh  a, [$02]
    and  $80
    ret  nz

    ldh  a, [$01] ; get data byte
    ld   [wLinkGiveItemFrom], a
    ld   a, [wLinkStatusBits]
    or   $01
    ld   [wLinkStatusBits], a
    ld   hl, wLinkSyncSequenceNumber
    inc  [hl]
    jp   LinkInit

LinkSetupSendItem:
    ld   a, $05
    ld   [wLinkState], a
    ld   a, [wLinkSendItemRoomHigh]
    jp   LinkStoreReply

LinkHandleSendItemRoomHigh:
    ; Received a new byte on the link?
    ldh  a, [$02]
    and  $80
    ret  nz

    ld   a, $06
    ld   [wLinkState], a
    ld   a, [wLinkSendItemRoomLow]
    jp   LinkStoreReply

LinkHandleSendItemRoomLow:
    ; Received a new byte on the link?
    ldh  a, [$02]
    and  $80
    ret  nz

    ld   a, $07
    ld   [wLinkState], a
    ld   a, [wLinkSendItemTarget]
    jp   LinkStoreReply

LinkHandleSendItemTarget:
    ; Received a new byte on the link?
    ldh  a, [$02]
    and  $80
    ret  nz

    ld   a, $08
    ld   [wLinkState], a
    ld   a, [wLinkSendItemItem]
    jp   LinkStoreReply

LinkHandleSendItemItem:
    ; Received a new byte on the link?
    ldh  a, [$02]
    and  $80
    ret  nz

    ; Remove the "got item to send bit"
    ld   a, [wLinkStatusBits]
    and  $FD
    ld   [wLinkStatusBits], a

    ; Ignore the received byte
    jp   LinkInit


LinkSetupSendID:
    ld   a, $09
    ld   [wLinkState], a
    ld   a, [$0051]
    jp   LinkStoreReply

LinkHandleSendID1:
    ; Received a new byte on the link?
    ldh  a, [$02]
    and  $80
    ret  nz

    ld   a, $0A
    ld   [wLinkState], a
    ld   a, [$0052]
    jp   LinkStoreReply

LinkHandleSendID2:
    ; Received a new byte on the link?
    ldh  a, [$02]
    and  $80
    ret  nz

    ld   a, $0B
    ld   [wLinkState], a
    ld   a, [$0053]
    jp   LinkStoreReply

LinkHandleSendID3:
    ; Received a new byte on the link?
    ldh  a, [$02]
    and  $80
    ret  nz

    ld   a, $0C
    ld   [wLinkState], a
    ld   a, [$0054]
    jp   LinkStoreReply

LinkHandleSendID4:
    ; Received a new byte on the link?
    ldh  a, [$02]
    and  $80
    ret  nz

    ld   a, $0D
    ld   [wLinkState], a
    ld   a, [$0055]
    jp   LinkStoreReply

LinkHandleSendPlayerID:
    ; Received a new byte on the link?
    ldh  a, [$02]
    and  $80
    ret  nz

    ; Ignore the received byte
    jp   LinkInit


;; OLD DEAD CODE AHEAD

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
