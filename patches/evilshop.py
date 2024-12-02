from assembler import ASM
from roomEditor import RoomEditor, ObjectHorizontal, ObjectVertical, Object
import entityData


def addEvilShop(rom):
    # Make a copy of the shop into GrandpaUlrira house
    re = RoomEditor(rom, 0x2A9)
    re.objects = [
                     ObjectHorizontal(1, 1, 0x00, 8),
                     ObjectHorizontal(1, 2, 0x00, 8),
                     ObjectHorizontal(1, 3, 0xCD, 8),
                     Object(2, 0, 0xAB),  # hidden unlit torch to make the room dark
                     Object(2, 0, 0xC7),
                     Object(7, 0, 0xC7),
                     Object(4, 7, 0xFD),
                 ] + re.getWarps()
    re.entities = [(8, 4, 0x77)]
    re.animation_id = 0x04
    re.floor_object = 0x0D
    re.store(rom)
    # Fix the tileset
    rom.banks[0x20][0x2EB3 + 0x2A9 - 0x100] = rom.banks[0x20][0x2EB3 + 0x2A1 - 0x100]

    # Load the shopkeeper sprites
    entityData.SPRITE_DATA[0x77] = entityData.SPRITE_DATA[0x4D]
    rom.patch(0x03, 0x00FB + 0x77, "00", "98")  # Fix the hitbox of the ghost to be 16x16

    # Patch grandpa to work as a shop
    rom.patch(0x06, 0x1C0E, 0x1C89, ASM("""
    ld   a, $01
    ld   [wBlockItemUsage], a ; this stops link from using items

;Draw shopkeeper
    ld   de, OwnerSpriteData
    call RenderActiveEntitySpritesPair ; render sprite pair
    ldh  a, [hFrameCounter] ; frame counter
    swap a
    and  $01
    call $3B0C ; set sprite variant

    call PushLinkOutOfEntity_06
    call CheckLinkInteractionWithEntity_06
    call c, startTalking

    call $7F14 ; draw items

    ldh  a, [hActiveEntityState]
    and  a
    jr   nz, checkTalkingResult
    ret

checkTalkingResult:
    ld   a, [wDialogState]
    and  a
    ret  nz ; still taking
    call IncrementEntityState
    ld   [hl], $00
    ld   a, [$C177] ; dialog selection
    and  a
    ret  nz
    ld  a, $14 ; EvilShopQuestion
    rst 8
    ret

startTalking:
    ld  a, $13 ; EvilShopQuestion
    rst 8
    ret

OwnerSpriteData:
    ;db   $60, $03, $62, $03, $62, $23, $60, $23 ; down
    ;db   $64, $03, $66, $03, $66, $23, $64, $23 ; up
    db   $68, $02, $6A, $02, $6C, $02, $6E, $02 ; left
    ;db   $6A, $23, $68, $23, $6E, $23, $6C, $23 ; right

    """, 0x5C0E), fill_nop=True)
    rom.patch(0x06, 0x3F14, "00" * (0x100 - 0x14), ASM("""
    
    shopItemsHandler:
; Render the shop items
    ld   h, $00
loop:
    ; First load links position to render the item at
    ldh  a, [hLinkPositionX] ; LinkX
    ldh  [hActiveEntityPosX], a ; X
    ldh  a, [hLinkPositionY] ; LinkY
    sub  $0E
    ldh  [hActiveEntityVisualPosY], a ; Y
    ; Check if this is the item we have picked up
    ld   a, [$C509] ; picked up item in shop
    dec  a
    cp   h
    jr   z, .renderCarry

    ld   a, h
    swap a
    add  a, a
    add  a, $20
    ldh  [hActiveEntityPosX], a ; X
    ld   a, $30
    ldh  [hActiveEntityVisualPosY], a ; Y
.renderCarry:
    ld   a, h
    push hl
    ldh  [hActiveEntitySpriteVariant], a ; variant
    ld   de, ItemsSpriteData
    call $3C77 ; render sprite

    pop  hl
.skipItem:
    inc  h
    ld   a, $03
    cp   h
    jr   nz, loop

;   check if we want to pickup or drop an item
    ldh  a, [$FFCC]
    and  $30 ; A or B button
    call nz, checkForPickup

;   check if we have an item
    ld   a, [$C509] ; carry item
    and  a
    ret  z

    ; Set that link has picked something up
    ld   a, $01
    ld   [$C15C], a
    call $0CAF ; reset spin attack...

    ; Check if we are trying to exit the shop and so drop our item.
    ldh  a, [hLinkPositionY]
    cp   $78
    ret  c
    xor  a
    ld   [$C509], a

    ret

checkForPickup:
    ldh  a, [hLinkDirection]
    cp   $02
    ret  nz
    ldh  a, [hLinkPositionY] ; LinkY
    cp   $48
    ret  nc

    ld   a, $13
    ldh  [hJingle], a ; play SFX

    ld   a, [$C509] ; picked up shop item
    and  a
    jr   nz, .drop

    ldh  a, [hLinkPositionX] ; LinkX
    add  $10
    swap a
    rrca
    and  $03
    ld   [$C509], a ; picked up shop item
    ret
.drop:
    xor  a
    ld   [$C509], a
    ret

ItemsSpriteData:
    db   $26, $0D
    db   $1E, $0C
    db   $4A, $0F
    """, 0x7F14), fill_nop=True)