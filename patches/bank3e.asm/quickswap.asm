QuickswapDraw:
    ld   bc, $2000
    call DrawQuickswapIndicator
    ld   bc, $2501
    jr   DrawQuickswapIndicator

QuickswapRemoveArrow:
    ld   bc, $2002
    call DrawQuickswapIndicator
    ld   bc, $2502

DrawQuickswapIndicator:
    ld   a, [wDrawCommandsSize]
    ld   e, a
    ld   d, $00
    add  $04
    ld   [wDrawCommandsSize], a
    ld   hl, wDrawCommand
    add  hl, de
    ld   a, $9C
    ldi  [hl], a
    ld   a, b
    ldi  [hl], a
    xor  a
    ldi  [hl], a
    push hl
    ld   a, [wQuickswapSlot]
    cp   c
    jr   nz, .blank
    ld   a, $A3
    jr   .arrow
.blank:
    ld   a, $BC
.arrow:
    pop  hl
    ldi  [hl], a
    xor  a
    ldi  [hl], a
    ret

QuickswapResetB:
    ld   a, [wQuickswapSlot]
    and  a
    ret  nz
    call EnableSRAM
    inc  a
    ld   [wQuickswapSlot], a
    xor  a
    ld   [wQuickswapIndex], a
    ld   a, [$DB00]
    ld   hl, wRecentItemListSlotB
    push bc
    call QuickswapInsertItemInFront
    call QuickswapDraw
    pop  bc
    ret

QuickswapResetA:
    ld   a, [wQuickswapSlot]
    and  a
    ret  z
    call EnableSRAM
    xor  a
    ld   [wQuickswapSlot], a
    ld   [wQuickswapIndex], a
    ld   a, [$DB01]
    ld   hl, wRecentItemListSlotA
    push bc
    call QuickswapInsertItemInFront
    call QuickswapDraw
    pop  bc
    ret

QuickswapResetOnGrab:
    ld   a, $01
    ldh  [$FFA1], a
    ld   a, [$DB00]
    cp   $03
    jr   z, QuickswapResetB
    ld   a, [$DB01]
    cp   $03
    jr   z, QuickswapResetA
    ret

QuickswapResetMenuB:
    call EnableSRAM
    ld   a, $01
    ld   [wQuickswapSlot], a
    xor  a
    ld   [wQuickswapIndex], a
    ld   a, [$DB00]
    ld   hl, wRecentItemListSlotB
    jr   QuickswapInsertItemInFront

QuickswapResetMenuA:
    call EnableSRAM
    xor  a
    ld   [wQuickswapSlot], a
    ld   [wQuickswapIndex], a
    ld   a, [$DB01]
    ld   hl, wRecentItemListSlotA
    jr   QuickswapInsertItemInFront

QuickswapResetOnNewItem:
    call EnableSRAM
    ld   a, c
    ld   hl, wRecentItemListSlotB
    call QuickswapInsertItemInFront
    ld   a, c
    ld   hl, wRecentItemListSlotA

QuickswapInsertItemInFront:
    and  a
    ret  z
    ld   b, a
    ld   d, $08
.loop:
    ld   e, [hl]
    ldi  [hl], a
    ld   a, e
    cp   b
    ret  z
    ld   a, [hl]
    ld   [hl], e
    cp   b
    ret  z
    inc  hl
    dec  d
    jr   nz, .loop
    ret

Quickswap:
    ; Check for how many frames the Select button has been held
    ld   a, [$D45F]
    cp   $01
    jr   z, .normalSwap
    cp   $14
    jr   z, .resetSwap
    ret  c
    ; Prevent the counter from overflowing
    ld   a, $15
    ld   [$D45F], a
    ret
.resetSwap:
    xor  a
    ld   [wQuickswapIndex], a
.normalSwap:
    call EnableSRAM
    ld   a, [$DB00]
    ld   b, a
    ld   a, [$DB01]
    ld   c, a
    ld   a, [wQuickswapSlot]
    and  a
    jr   z, .recentItemsB
    ld   hl, wRecentItemListSlotA
    jr   .recentItemsA
.recentItemsB:
    ld   hl, wRecentItemListSlotB
.recentItemsA:
    ld   a, [wQuickswapIndex]
    call QuickswapGetNextItem
    and  a
    ret  z
    ; Perform swap
    ld   a, d
    inc  a
    cp   $10
    jr   c, .storeNewIndex
    xor  a
.storeNewIndex:
    ld   [wQuickswapIndex], a
    ld   b, h
    ld   c, l
    ld   a, [wQuickswapSlot]
    and  a
    jr   z, .swapB
    ld   hl, $DB01
    jr   .swapA
.swapB:
    ld   hl, $DB00
.swapA:
    ld   a, [bc]
    ld   e, a
    ld   a, [hl]
    ld   [bc], a
    ld   [hl], e
    ; Play sound
    ld   hl, $FFF2
    ld   [hl], $0A
    ret

QuickswapUpdatePreview:
    call EnableSRAM
    ld   a, c
    and  a
    ld   a, [$DB00]
    ld   b, a
    ld   a, [$DB01]
    ld   c, a
    jr   nz, .previewA
    ld   hl, wRecentItemListSlotB
    ld   a, [wQuickswapSlot]
    and  a
    jr   z, .useIndex
    xor  a
    jr   .startOfListB
.useIndex:
    ld   a, [wQuickswapIndex]
.startOfListB:
    call QuickswapGetNextItem
    ld   [wQuickswapPreviewB1], a
    ld   b, a ; for the second swap, consider which item would be in the B slot after the first swap 
    and  a
    jr   z, .endB
    ld   a, d
    inc  a
    cp   $10
    jr   c, .nextPreviewB
    xor  a
.nextPreviewB:
    ld   hl, wRecentItemListSlotB
    call QuickswapGetNextItem
.endB:
    ld   [wQuickswapPreviewB2], a
    ret

.previewA:
    ld   hl, wRecentItemListSlotA
    ld   a, [wQuickswapSlot]
    and  a
    jr   z, .startOfListA
    ld   a, [wQuickswapIndex]
.startOfListA:
    call QuickswapGetNextItem
    ld   [wQuickswapPreviewA1], a
    ld   c, a ; for the second swap, consider which item would be in the A slot after the first swap
    and  a
    jr   z, .endA
    ld   a, d
    inc  a
    cp   $10
    jr   c, .nextPreviewA
    xor  a
.nextPreviewA:
    ld   hl, wRecentItemListSlotA
    call QuickswapGetNextItem
.endA:
    ld   [wQuickswapPreviewA2], a
    ret

    ; Input:
    ; a:  index in recent items list where the search should start
    ; bc: items that should not get equipped
    ; hl: recent items list
    ; Output:
    ; a:  which item is next, or 0
    ; d:  index in recent items list of the next item if it exists
QuickswapGetNextItem:
    and  a, $0F
    ld   e, a
    ld   d, a
    add  a, l
    ld   l, a
.loop:
    ldi  a, [hl]
    and  a
    jr   z, .continue
    cp   b
    jr   z, .continue
    cp   c
    jr   z, .continue
    ; Check if the selected item is still in the inventory
    push de
    push hl
    ld   e, a
    ld   hl, $DB00
    ld   d, $10
.checkInventorySlot:
    ld   a, [hl]
    cp   e
    jr   z, .foundInventorySlot
    inc  hl
    dec  d
    jr   nz, .checkInventorySlot
    ; The selected item is not in the inventory
    pop  hl
    pop  de
.continue:
    inc  d
    ld   a, d
    cp   $10
    jr   c, .checkFullLoop
    ; Hacky way to loop hl back to the start of the list
    ld   a, l
    dec  a
    and  $F0
    ld   l, a
    xor  a
    ld   d, a
.checkFullLoop:
    cp   e
    jr   nz, .loop
    xor  a
    ret
.foundInventorySlot:
    ld   a, e
    pop  de
    pop  de
    ret

QuickswapResetOnFileLoad:
    ld   a, $02
    ld   [$D6FF], a
    call QuickswapResetMenuB
    jp   QuickswapResetMenuA