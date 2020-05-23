from assembler import ASM


# Bank $3E is used for large chunks of custom code.
#   Mainly for new chest and dropped items handling.
def addBank3E(rom):
    # Create a trampoline to bank 0x3E in bank 0x00.
    # There is very little room in bank 0, so we set this up as a single trampoline for multiple possible usages.
    # the A register is preserved and can directly be used as a jumptable in page 3E.
    rom.patch(0, 0x3FF0, "0000000000000000000000000000", ASM("""
        ld   h, a
        ld   a, [$DBAF]
        push af
        ld   a, $3E
        call $080C ; switch bank
        ld   a, h
        jp $4000
    """), fill_nop=True)

    rom.patch(0x3E, 0x0000, None, ASM("""
        rst  0 ; JUMP TABLE
        dw   RenderChestItem    ; 0 
        dw   GiveItemFromChest  ; 1
        dw   ChestMessage       ; 2
        dw   RenderDroppedKey   ; 3

RenderChestItem:
        ld de, ChestSpriteTable

        ;call $3BC0 ; RenderActiveEntitySpritePair
        call $3C77 ; RenderActiveEntitySprite

        jp Exit

GiveItemFromChest:
        ldh  a, [$F1] ; Load active sprite variant

        rst  0 ; JUMP TABLE
        dw ChestPowerBracelet; CHEST_POWER_BRACELET
        dw ChestShield       ; CHEST_SHIELD
        dw ChestWithItem     ; CHEST_BOW
        dw ChestWithItem     ; CHEST_HOOKSHOT
        dw ChestWithItem     ; CHEST_MAGIC_ROD
        dw ChestWithItem     ; CHEST_PEGASUS_BOOTS
        dw ChestWithItem     ; CHEST_OCARINA
        dw ChestWithItem     ; CHEST_FEATHER
        dw ChestWithItem     ; CHEST_SHOVEL
        dw ChestWithItem     ; CHEST_MAGIC_POWDER_BAG
        dw ChestWithItem     ; CHEST_BOMB
        dw ChestSword        ; CHEST_SWORD
        dw Flippers          ; CHEST_FLIPPERS
        dw Exit             ; CHEST_MAGNIFYING_LENS
        dw ChestWithItem    ; Boomerang (used to be unused)
        dw Exit             ; ?? right side of your trade quest item
        dw Exit             ; CHEST_MEDICINE (handled by base rom during drawing for some reason...)
        dw TailKey          ; CHEST_TAIL_KEY
        dw AnglerKey        ; CHEST_ANGLER_KEY
        dw FaceKey          ; CHEST_FACE_KEY
        dw BirdKey          ; CHEST_BIRD_KEY
        dw Exit             ; CHEST_GOLD_LEAF
        dw ChestWithCurrentDungeonItem ; CHEST_MAP
        dw ChestWithCurrentDungeonItem ; CHEST_COMPASS
        dw ChestWithCurrentDungeonItem ; CHEST_STONE_BEAK
        dw ChestWithCurrentDungeonItem ; CHEST_NIGHTMARE_KEY
        dw ChestWithCurrentDungeonItem ; CHEST_SMALL_KEY
        dw AddRupees50      ; CHEST_RUPEES_50
        dw AddRupees20      ; CHEST_RUPEES_20
        dw AddRupees100     ; CHEST_RUPEES_100
        dw AddRupees200     ; CHEST_RUPEES_200
        dw AddRupees500     ; CHEST_RUPEES_500
        dw AddSeashell      ; CHEST_SEASHELL
        dw Exit             ; CHEST_MESSAGE
        dw Exit             ; CHEST_GEL

ChestPowerBracelet:
        ld   hl, $DB43 ; power bracelet level
        jr   ChestIncreaseItemLevel

ChestShield:
        ld   hl, $DB4f ; shield level
        jr   ChestIncreaseItemLevel

ChestSword:
        ld   hl, $DB4E ; sword level
        jr   ChestIncreaseItemLevel

ChestIncreaseItemLevel:
        ld   a, [hl]
        cp   $02
        jr   z, DoNotIncreaseItemLevel
        inc  [hl]
DoNotIncreaseItemLevel:
        jp   ChestWithItem

Flippers:
        ld   a, $01
        ld   [$DB0C], a    
        jp   Exit

Flippers:
        ld   a, $01
        ld   [$DB0C], a    
        jp   Exit

TailKey:
        ld   a, $01
        ld   [$DB11], a
        jp   Exit

AnglerKey:
        ld   a, $01
        ld   [$DB12], a
        jp   Exit

FaceKey:
        ld   a, $01
        ld   [$DB13], a
        jp   Exit

BirdKey:
        ld   a, $01
        ld   [$DB14], a
        jp   Exit

AddSeaShell:
        ld   hl, $DB0F
        inc  [hl]
        jp Exit

ChestInventoryTable:
        db   $03 ; CHEST_POWER_BRACELET
        db   $04 ; CHEST_SHIELD
        db   $05 ; CHEST_BOW
        db   $06 ; CHEST_HOOKSHOT
        db   $07 ; CHEST_MAGIC_ROD
        db   $08 ; CHEST_PEGASUS_BOOTS
        db   $09 ; CHEST_OCARINA
        db   $0A ; CHEST_FEATHER
        db   $0B ; CHEST_SHOVEL
        db   $0C ; CHEST_MAGIC_POWDER_BAG
        db   $02 ; CHEST_BOMB
        db   $01 ; CHEST_SWORD
        db   $00 ; - (flippers slot)
        db   $00 ; - (magnifier lens slot)
        db   $0D ; Boomerang

ChestWithItem:
        ldh  a, [$F1] ; Load active sprite variant
        ld   d, $00
        ld   e, a
        ld   hl, ChestInventoryTable
        add  hl, de
        ld   d, [hl]
        call $3E6B ; Give Inventory
        jp Exit

ChestWithCurrentDungeonItem:
        sub  $16 ; a -= CHEST_MAP 
        ld   e, a
        ld   d, $00
        ld   hl, $DBCC ; hasDungeonMap
        add  hl, de
        inc  [hl]
        call $2802  ; Sync current dungeon items with dungeon specific table 
        jp Exit

AddRupees20:
        xor  a
        ld   h, $14
        jr   AddRupees 

AddRupees50:
        xor  a
        ld   h, $32
        jr   AddRupees 

AddRupees100:
        xor  a
        ld   h, $64
        jr   AddRupees 

AddRupees200:
        xor  a
        ld   h, $C8
        jr   AddRupees 

AddRupees500:
        ld   a, $01
        ld   h, $F4
        jr   AddRupees 

AddRupees:
        ld   [$DB8F], a
        ld   a, h
        ld   [$DB90], a
        ld   a, $18
        ld   [$C3CE], a
        jp   Exit

ChestMessage:
        ldh  a, [$F1]
        ld   d, $00
        ld   e, a
        ld   hl, ChestMessageTable
        add  hl, de
        ld   a, [hl] 
        call $2385 ; Opendialog
Exit:
        pop af
        jp $080C ; switch bank and return to normal code.

ChestSpriteTable:
        db $82, $15        ; CHEST_POWER_BRACELET
        db $86, $15        ; CHEST_SHIELD
        db $88, $14        ; CHEST_BOW
        db $8A, $14        ; CHEST_HOOKSHOT
        db $8C, $14        ; CHEST_MAGIC_ROD
        db $98, $16        ; CHEST_PEGASUS_BOOTS
        db $90, $17        ; CHEST_OCARINA
        db $92, $16        ; CHEST_FEATHER
        db $96, $10        ; CHEST_SHOVEL
        db $8E, $10        ; CHEST_MAGIC_POWDER_BAG
        db $80, $15        ; CHEST_BOMB
        db $84, $15        ; CHEST_SWORD
        db $94, $15        ; CHEST_FLIPPERS
        db $9A, $10        ; CHEST_MAGNIFYING_LENS
        db $24, $1C        ; Boomerang
        db $9C, $10 ;?? right side of your trade quest item
        db $A0, $14        ; CHEST_MEDICINE
        db $30, $1C        ; CHEST_TAIL_KEY
        db $32, $1C        ; CHEST_ANGLER_KEY
        db $34, $1C        ; CHEST_FACE_KEY
        db $36, $1C        ; CHEST_BIRD_KEY
        db $3A, $1C        ; CHEST_GOLD_LEAF
        db $40, $1C        ; CHEST_MAP
        db $42, $1D        ; CHEST_COMPASS
        db $44, $1C        ; CHEST_STONE_BEAK
        db $46, $1C        ; CHEST_NIGHTMARE_KEY
        db $4A, $1F        ; CHEST_SMALL_KEY
        db $A6, $15        ; CHEST_RUPEES_50
        db $A6, $15        ; CHEST_RUPEES_20
        db $A6, $15        ; CHEST_RUPEES_100
        db $A6, $15        ; CHEST_RUPEES_200
        db $A6, $15        ; CHEST_RUPEES_500
        db $9E, $14        ; CHEST_SEASHELL
        db $FF, $18        ; CHEST_MESSAGE
        db $FF, $18        ; CHEST_GEL

ChestMessageTable:
        db $90, $91, $89, $93, $94, $95, $96, $97
        db $98, $99, $9A, $9B, $9C, $9D, $D9, $9F
        db $A0, $A1, $A3, $A4, $A5, $E8, $A6, $A7
        db $A8, $A9, $AA, $AC, $AB, $AD, $AE, $AE
        db $EF, $BE

RenderDroppedKey:
    ;TODO: See EntityInitKeyDropPoint for a few special cases to unload.

    ; Check if we need to load the chest type
    ld   hl, $C480 ; some unused entity state for the dropped key
    add  hl, bc
    ld   a, [hl]
    and  a
    jr   nz, DroppedKeyTypeLoaded
    inc  a
    ld   [hl], a

    ;TODO: Load the chest type from the chest table.
    ldh  a, [$F6]
    ld   e, a
    ld   a, [$DBA5] ; is indoor
    ld   d, a
    ldh  a, [$F7]   ; mapId
    cp   $FF
    jr   nz, notColorDungeon

    ld   d, $00
    ld   hl, $7E00
    jr   loadedPointers

notColorDungeon:
    cp   $1A
    jr   nc, notCavesA
    cp   $06
    jr   c, notCavesA
    inc  d
notCavesA:
    ld   hl, $7800
loadedPointers:
    add  hl, de

    ld   a, [hl]
    call $3B0C ; SetEntitySpriteVariant
DroppedKeyTypeLoaded:
    jp RenderChestItem
    """, 0x4000))
