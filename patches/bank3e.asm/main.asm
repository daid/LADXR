        call MainJumpTable
        pop af
        jp $080C ; switch bank and return to normal code.

MainJumpTable:
        rst  0 ; JUMP TABLE
        dw   MainLoop                             ; 0
        dw   RenderChestItem                      ; 1
        dw   GiveItemFromChest                    ; 2
        dw   ItemMessage                          ; 3
        dw   RenderDroppedKey                     ; 4
        dw   RenderHeartPiece                     ; 5
        dw   GiveItemFromChestMultiworld          ; 6
        dw   CheckIfLoadBowWow                    ; 7
        dw   BowwowEat                            ; 8
        dw   HandleOwlStatue                      ; 9
        dw   ItemMessageMultiworld                ; A
        dw   GiveItemAndMessageForRoom            ; B
        dw   RenderItemForRoom                    ; C
        dw   StartGameMarinMessage                ; D
        dw   GiveItemAndMessageForRoomMultiworld  ; E
        dw   RenderOwlStatueItem                  ; F
        dw   UpdateInventoryMenu                  ; 10
        dw   HandleSeashellMansionItem            ; 11

StartGameMarinMessage:
        ; Injection to reset our frame counter
        call $27D0 ; Enable SRAM
        ld   hl, $B000
        xor  a
        ldi  [hl], a ;subsecond counter
        ld   a, $08  ;(We set the counter to 8 seconds, as it takes 8 seconds before link wakes up and marin talks to him)
        ldi  [hl], a ;second counter
        xor  a
        ldi  [hl], a ;minute counter
        ldi  [hl], a ;hour counter

        ld   hl, $B010
        ldi  [hl], a ;check counter low
        ldi  [hl], a ;check counter high

        ; Show the normal message
        ld   a, $01
        jp $2385

TradeSequenceItemData:
    ; tile attributes
    db $0D, $0A, $0D, $0D, $0E, $0E, $0D, $0D, $0D, $0E, $09, $0A, $0A, $0D
    ; tile index
    db $1A, $B0, $B4, $B8, $BC, $C0, $C4, $C8, $CC, $D0, $D4, $D8, $DC, $E0

UpdateInventoryMenu:
        ld   a, [wTradeSequenceItem]
        ld   hl, wTradeSequenceItem2
        or   [hl]
        ret  z

        ld   hl, TradeSequenceItemData
        ld   a, [$C109]
        ld   e, a
        ld   d, $00
        add  hl, de

        ; Check if we need to increase the counter
        ldh  a, [$FFE7] ; frame counter
        and  $0F
        jr   nz, .noInc
        ld   a, e
        inc  a
        cp   14
        jr   nz, .noWrap
        xor  a
.noWrap:
        ld   [$C109], a
.noInc:

        ; Check if we have the item
        ld   b, e
        inc  b
        ld   a, $01

        ld   de, wTradeSequenceItem
.shiftLoop:
        dec  b
        jr   z, .shiftLoopDone
        sla  a
        jr   nz, .shiftLoop
        ; switching to second byte
        ld   de, wTradeSequenceItem2
        ld   a, $01
        jr   .shiftLoop
.shiftLoopDone:
        ld   b, a
        ld   a, [de]
        and  b
        ret  z ; skip this item

        ld   b, [hl]
        push hl

        ; Write the tile attribute data
        ld   a, $01
        ldh  [$FF4F], a

        ld   hl, $9C6E
        call WriteToVRAM
        inc  hl
        call WriteToVRAM
        ld   de, $001F
        add  hl, de
        call WriteToVRAM
        inc  hl
        call WriteToVRAM

        ; Write the tile data
        xor  a
        ldh  [$FF4F], a

        pop  hl
        ld   de, 14
        add  hl, de
        ld   b, [hl]

        ld   hl, $9C6E
        call WriteToVRAM
        inc  b
        inc  b
        inc  hl
        call WriteToVRAM
        ld   de, $001F
        add  hl, de
        dec  b
        call WriteToVRAM
        inc  hl
        inc  b
        inc  b
        call WriteToVRAM
        ret

WriteToVRAM:
        ldh  a, [$FF41]
        and  $02
        jr   nz, WriteToVRAM
        ld   [hl], b
        ret

#INCLUDE "multiworld.asm"
#INCLUDE "link.asm"
#INCLUDE "chest.asm"
#INCLUDE "bowwow.asm"
#INCLUDE "message.asm"
#INCLUDE "owl.asm"
