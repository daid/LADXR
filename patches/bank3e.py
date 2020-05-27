from assembler import ASM
from utils import formatText


def hasBank3E(rom):
    return rom.banks[0x3E][0] != 0x00

# Bank $3E is used for large chunks of custom code.
#   Mainly for new chest and dropped items handling.
def addBank3E(rom):
    # No default text for getting the bow, so use an unused slot.
    rom.texts[0x89] = formatText(b"Found the bow!")
    rom.texts[0xD9] = formatText(b"Found the boomerang!")  # owl text slot reuse
    rom.texts[0xBE] = rom.texts[0x111]  # owl text slot reuse to get the master skull message in the first dialog group
    for idx in range(8):
        rom.texts[0xBF + idx] = formatText(b"Found an item for dungeon %d" % (idx + 1))
    rom.texts[0xC7] = formatText(b"Found an item for color dungeon")

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
        dw   MainLoop           ; 0
        dw   RenderChestItem    ; 1
        dw   GiveItemFromChest  ; 2
        dw   ItemMessage        ; 3
        dw   RenderDroppedKey   ; 4
        dw   RenderHeartPiece   ; 5

MainLoop:
        ; First, do the thing we injected our code in.
        ld   a, [$C14C]
        and  a
        jr   z, $04
        dec  a
        ld   [$C14C], a

;actualMainLoop
        jp Exit

RenderChestItem:
        ldh  a, [$F1] ; active sprite
        and  $80
        jr   nz, RenderLargeItem

        ld   de, ItemSpriteTable
        call $3C77 ; RenderActiveEntitySprite
        jp   Exit
RenderLargeItem:
        ld   de, LargeItemSpriteTable
        dec  d
        dec  d
        call $3BC0 ; RenderActiveEntitySpritePair
        jp   Exit

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
        dw SlimeKey         ; ?? right side of your trade quest item
        dw Medicine         ; CHEST_MEDICINE
        dw TailKey          ; CHEST_TAIL_KEY
        dw AnglerKey        ; CHEST_ANGLER_KEY
        dw FaceKey          ; CHEST_FACE_KEY
        dw BirdKey          ; CHEST_BIRD_KEY
        dw GoldenLeaf       ; CHEST_GOLD_LEAF
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
        dw AddKey ; KEY1
        dw AddKey ; KEY2
        dw AddKey ; KEY3
        dw AddKey ; KEY4
        dw AddKey ; KEY5
        dw AddKey ; KEY6
        dw AddKey ; KEY7
        dw AddKey ; KEY8
        dw AddKey ; KEY9
        dw AddMap ; MAP1
        dw AddMap ; MAP2
        dw AddMap ; MAP3
        dw AddMap ; MAP4
        dw AddMap ; MAP5
        dw AddMap ; MAP6
        dw AddMap ; MAP7
        dw AddMap ; MAP8
        dw AddMap ; MAP9
        dw AddCompass ; COMPASS1
        dw AddCompass ; COMPASS2
        dw AddCompass ; COMPASS3
        dw AddCompass ; COMPASS4
        dw AddCompass ; COMPASS5
        dw AddCompass ; COMPASS6
        dw AddCompass ; COMPASS7
        dw AddCompass ; COMPASS8
        dw AddCompass ; COMPASS9
        dw AddStoneBeak ; STONE_BEAK1
        dw AddStoneBeak ; STONE_BEAK2
        dw AddStoneBeak ; STONE_BEAK3
        dw AddStoneBeak ; STONE_BEAK4
        dw AddStoneBeak ; STONE_BEAK5
        dw AddStoneBeak ; STONE_BEAK6
        dw AddStoneBeak ; STONE_BEAK7
        dw AddStoneBeak ; STONE_BEAK8
        dw AddStoneBeak ; STONE_BEAK9
        dw AddNightmareKey ; NIGHTMARE_KEY1
        dw AddNightmareKey ; NIGHTMARE_KEY2
        dw AddNightmareKey ; NIGHTMARE_KEY3
        dw AddNightmareKey ; NIGHTMARE_KEY4
        dw AddNightmareKey ; NIGHTMARE_KEY5
        dw AddNightmareKey ; NIGHTMARE_KEY6
        dw AddNightmareKey ; NIGHTMARE_KEY7
        dw AddNightmareKey ; NIGHTMARE_KEY8
        dw AddNightmareKey ; NIGHTMARE_KEY9
        dw Exit ; $50
        dw Exit ; $51
        dw Exit ; $52
        dw Exit ; $53
        dw Exit ; $54
        dw Exit ; $55
        dw Exit ; $56
        dw Exit ; $57
        dw Exit ; $58
        dw Exit ; $59
        dw Exit ; $5A
        dw Exit ; $5B
        dw Exit ; $5C
        dw Exit ; $5D
        dw Exit ; $5E
        dw Exit ; $5F
        dw Exit ; $60
        dw Exit ; $61
        dw Exit ; $62
        dw Exit ; $63
        dw Exit ; $64
        dw Exit ; $65
        dw Exit ; $66
        dw Exit ; $67
        dw Exit ; $68
        dw Exit ; $69
        dw Exit ; $6A
        dw Exit ; $6B
        dw Exit ; $6C
        dw Exit ; $6D
        dw Exit ; $6E
        dw Exit ; $6F
        dw Exit ; $70
        dw Exit ; $71
        dw Exit ; $72
        dw Exit ; $73
        dw Exit ; $74
        dw Exit ; $75
        dw Exit ; $76
        dw Exit ; $77
        dw Exit ; $78
        dw Exit ; $79
        dw Exit ; $7A
        dw Exit ; $7B
        dw Exit ; $7C
        dw Exit ; $7D
        dw Exit ; $7E
        dw Exit ; $7F
        dw PieceOfHeart     ; Heart piece

ChestPowerBracelet:
        ld   hl, $DB43 ; power bracelet level
        jr   ChestIncreaseItemLevel

ChestShield:
        ld   hl, $DB44 ; shield level
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

Medicine:
        ld   a, $01
        ld   [$DB0D], a
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

SlimeKey:
        ld   a, $01
        ld   [$DB15], a
        jp   Exit

GoldenLeaf:
        ld   hl, $DB6D
        inc  [hl]
        jp   Exit

AddSeaShell:
        ld   hl, $DB0F
        inc  [hl]
        jp Exit

PieceOfHeart:
        ld   a, [$DB5C]
        inc  a
        cp   $04
        jr   z, FullHeart
        ld   [$DB5C], a
        jp Exit
FullHeart:
        xor a
        ld   [$DB5C], a
        ld   hl, $DB93
        ld   [hl], $40 ; Regen HP
        ld   hl, $DB5B
        inc  [hl]      ; Add max health
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

AddKey:
        sub $23 ; Make 'A' our dungeon index
        ld   hl, $DB1A
        jr   AddDungeonItem

AddMap:
        sub $2B ; Make 'A' our dungeon index
        ld   hl, $DB16
        jr   AddDungeonItem

AddCompass:
        sub $33 ; Make 'A' our dungeon index
        ld   hl, $DB17
        jr   AddDungeonItem

AddStoneBeak:
        sub $3B ; Make 'A' our dungeon index
        ld   hl, $DB18
        jr   AddDungeonItem

AddNightmareKey:
        sub $43 ; Make 'A' our dungeon index
        ld   hl, $DB19
        jr   AddDungeonItem

AddDungeonItem:
        ld   e, a
        ld   d, $00
        add  hl, de
        add  hl, de
        add  hl, de
        add  hl, de
        add  hl, de
        inc  [hl]
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

ItemMessage:
        ldh  a, [$F1]
        ld   d, $00
        ld   e, a
        ld   hl, ItemMessageTable
        add  hl, de
        ld   a, [hl]
        call $2385 ; Opendialog
Exit:
        pop af
        jp $080C ; switch bank and return to normal code.

ItemSpriteTable:
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
        db $4E, $1C        ; Slime key
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
        db $38, $18        ; CHEST_RUPEES_50 (green)
        db $A6, $15        ; CHEST_RUPEES_20 (normal blue)
        db $38, $19        ; CHEST_RUPEES_100 (red)
        db $38, $1A        ; CHEST_RUPEES_200 (yellow)
        db $38, $1A        ; CHEST_RUPEES_500 (yellow)
        db $9E, $14        ; CHEST_SEASHELL
        db $FF, $18        ; CHEST_MESSAGE
        db $FF, $18        ; CHEST_GEL
        db $4A, $1F        ; KEY1
        db $4A, $1F        ; KEY2
        db $4A, $1F        ; KEY3
        db $4A, $1F        ; KEY4
        db $4A, $1F        ; KEY5
        db $4A, $1F        ; KEY6
        db $4A, $1F        ; KEY7
        db $4A, $1F        ; KEY8
        db $4A, $1F        ; KEY9
        db $40, $1C        ; MAP1
        db $40, $1C        ; MAP2
        db $40, $1C        ; MAP3
        db $40, $1C        ; MAP4
        db $40, $1C        ; MAP5
        db $40, $1C        ; MAP6
        db $40, $1C        ; MAP7
        db $40, $1C        ; MAP8
        db $40, $1C        ; MAP9
        db $42, $1D        ; COMPASS1
        db $42, $1D        ; COMPASS2
        db $42, $1D        ; COMPASS3
        db $42, $1D        ; COMPASS4
        db $42, $1D        ; COMPASS5
        db $42, $1D        ; COMPASS6
        db $42, $1D        ; COMPASS7
        db $42, $1D        ; COMPASS8
        db $42, $1D        ; COMPASS9
        db $44, $1C        ; STONE_BEAK1
        db $44, $1C        ; STONE_BEAK2
        db $44, $1C        ; STONE_BEAK3
        db $44, $1C        ; STONE_BEAK4
        db $44, $1C        ; STONE_BEAK5
        db $44, $1C        ; STONE_BEAK6
        db $44, $1C        ; STONE_BEAK7
        db $44, $1C        ; STONE_BEAK8
        db $44, $1C        ; STONE_BEAK9
        db $46, $1C        ; NIGHTMARE_KEY1
        db $46, $1C        ; NIGHTMARE_KEY2
        db $46, $1C        ; NIGHTMARE_KEY3
        db $46, $1C        ; NIGHTMARE_KEY4
        db $46, $1C        ; NIGHTMARE_KEY5
        db $46, $1C        ; NIGHTMARE_KEY6
        db $46, $1C        ; NIGHTMARE_KEY7
        db $46, $1C        ; NIGHTMARE_KEY8
        db $46, $1C        ; NIGHTMARE_KEY9

LargeItemSpriteTable:
        db $AC, $02, $AC, $22 ; heart piece

ItemMessageTable:
        db $90, $3D, $89, $93, $94, $95, $96, $97, $98, $99, $9A, $9B, $9C, $9D, $D9, $A2
        db $A0, $A1, $A3, $A4, $A5, $E8, $A6, $A7, $A8, $A9, $AA, $AC, $AB, $AD, $AE, $AE
        db $EF, $BE, $00, $BF, $C0, $C1, $C2, $C3, $C4, $C5, $C6, $C7, $BF, $C0, $C1, $C2
        db $C3, $C4, $C5, $C6, $C7, $BF, $C0, $C1, $C2, $C3, $C4, $C5, $C6, $C7, $BF, $C0
        ; $40
        db $C1, $C2, $C3, $C4, $C5, $C6, $C7, $BF, $C0, $C1, $C2, $C3, $C4, $C5, $C6, $C7
        db $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
        db $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
        db $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
        ; $80
        db $4F

RenderDroppedKey:
    ;TODO: See EntityInitKeyDropPoint for a few special cases to unload.

RenderHeartPiece:
    ;Load the chest type from the chest table.
    ldh  a, [$F6] ; map room
    ld   e, a
    ld   a, [$DBA5] ; is indoor
    ld   d, a
    ldh  a, [$F7]   ; mapId
    cp   $FF
    jr   nz, .notColorDungeon

    ld   d, $00
    ld   hl, $7B00
    jr   .loadedPointers

.notColorDungeon:
    cp   $1A
    jr   nc, .notCavesA
    cp   $06
    jr   c, .notCavesA
    inc  d
.notCavesA:
    ld   hl, $7800
.loadedPointers:
    add  hl, de

    ld   a, [hl]
    ldh  [$F1], a ; set currentEntitySpriteVariant
    call $3B0C ; SetEntitySpriteVariant

    and  $80
    ld   hl, $C340
    add  hl, bc
    ld   a, [hl]
    jr   z, .singleSprite
    ; We potentially need to fix the physics flags table to allocate 2 sprites for us
    and  $F8
    or   $02
    ld   [hl], a
    jr .droppedKeyTypeLoaded
.singleSprite:
    and  $F8
    or   $01
    ld   [hl], a
.droppedKeyTypeLoaded:
    jp RenderChestItem
    """, 0x4000))
