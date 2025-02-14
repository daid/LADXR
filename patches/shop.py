from assembler import ASM
from roomEditor import RoomEditor, Object, ObjectHorizontal


def fixShop(rom, allow_both=False, shopsanity=False):
    # Move shield visuals to the 2nd slot, and arrow to 3th slot
    rom.patch(0x04, 0x3732 + 22, "986A027FB2B098AC01BAB1", "9867027FB2B098A801BAB1")
    rom.patch(0x04, 0x3732 + 55, "986302B1B07F98A4010A09", "986B02B1B07F98AC010A09")

    if allow_both:
        # Move 2nd item to 2nd slot, move shield to 3th slot, removing the arrow buy option
        rom.patch(0x04, 0x3732 + 4 * 11, "9863", "9867")
        rom.patch(0x04, 0x3732 + 2 * 11, "9867", "986A")
        rom.patch(0x04, 0x3732 + 2 * 11 + 6, "98A8", "98AC")

    # Patch the code that decides which shop to show.
    rom.patch(0x04, 0x3839, 0x388E, ASM(f"""
ALLOW_BOTH_ITEMS := {1 if allow_both else 0}
        push bc
        jr skipSubRoutine

checkInventory:
        ld hl, $DB00 ; inventory
        ld c, INV_SIZE
loop:
        cp [hl]
        ret z
        inc hl
        dec c
        jr nz, loop
        and a
        ret

skipSubRoutine:
        ; Set the shop table to all nothing.
        ld   hl, $C505
        xor  a
        ldi  [hl], a
        ldi  [hl], a
        ldi  [hl], a
        ldi  [hl], a
        ld   de, $C505
        
        ; Check if we want to load a key item into the shop.
        ldh  a, [hRoomStatus]
        bit  4, a
        jr   nz, checkForSecondKeyItem
        ld   a, $01
        ld   [de], a
#IF ALLOW_BOTH_ITEMS == 0
        jr   checkForShield
#ENDIF
checkForSecondKeyItem:
#IF ALLOW_BOTH_ITEMS
        inc  de
        ldh  a, [hRoomStatus]
#ENDIF
        bit  5, a
        jr   nz, checkForShield
        ld   a, $05
        ld   [de], a

checkForShield:
        inc  de
        ; Check if we have the shield or the bow to see if we need to remove certain entries from the shop
        ld   a, [wShieldLevel]
        and  a
        jr   z, hasNoShieldLevel
        ld   a, $03
        ld   [de], a ; Add shield buy option
hasNoShieldLevel:

#IF ALLOW_BOTH_ITEMS == 0
        inc  de
        ld   a, $05
        call checkInventory
        jr   nz, hasNoBow
        ld   a, $06
        ld   [de], a ; Add arrow buy option
hasNoBow:
#ENDIF

        inc  de
        ld   a, $02
        call checkInventory
        jr   nz, hasNoBombs
        ld   a, $04
        ld   [de], a ; Add bomb buy option
hasNoBombs:

        pop  bc
        call IncrementEntityState
    """, 0x7839), fill_nop=True)

    # We do not have enough room at the shovel/bow buy entry to handle this
    # So jump to a bit where we have some more space to work, as there is some dead code in the shop.
    rom.patch(0x04, 0x3AA9, 0x3AAE, ASM("jp $7AC0"), fill_nop=True)
    rom.patch(0x04, 0x3AC0, 0x3AD8, ASM("""
        ; Call our chest item giving code.
        ld   a, $12 ; Get room item (in hActiveEntitySpriteVariant)
        rst  8
        ld   a, $02
        rst  8
        ; Update the room status to mark first item as bought (assumes indoor2)
        ld   h, $DA
        ldh  a, [hMapRoom]
        ld   l, a
        ld   a, [hl]
        or   $10
        ld   [hl], a
        ret
    """), fill_nop=True)
    rom.patch(0x04, 0x3A73, 0x3A7E, ASM("jp $7A91"), fill_nop=True)
    rom.patch(0x04, 0x3A91, 0x3AA9, ASM("""
        ; Call our chest item giving code.
        ld   d, $02
        ldh  a, [hMapRoom]
        ld   e, a
        call $29ED ; Get chest item (in A)
        ldh  [hActiveEntitySpriteVariant], a
        ld   a, $02
        rst  8
        ; Update the room status to mark second item as bought (assumes indoor2)
        ld   h, $DA
        ldh  a, [hMapRoom]
        ld   l, a
        ld   a, [hl]
        or   $20
        ld   [hl], a
        ret
    """), fill_nop=True)

    # Patch shop item graphics rendering to use some new code at the end of the bank.
    rom.patch(0x04, 0x3B91, 0x3BAC, ASM("""
        call $7BD3
        jr   $16 ; skip over the NOP's
    """), fill_nop=True)
    rom.patch(0x04, 0x3BD3, 0x3BE3, ASM("""
        ; Check if first key item
        and  a
        jp   nz, $7FD0 ; notShovel
        ld   a, $12 ; Get room item (in hActiveEntitySpriteVariant)
        rst  8
        ld   a, $01 ; RenderChestItem
        rst  8
        ret
    """), fill_nop=True)
    rom.patch(0x04, 0x3FD0, "00" * 40, ASM("""
    notShovel:
        cp   $04
        jr   nz, notBow
        ld   d, $02
        ldh  a, [hMapRoom]
        ld   e, a
        call $29ED ; Get chest item (in A)
        ldh  [hActiveEntitySpriteVariant], a
        ld   a, $01 ; RenderChestItem
        rst  8
        ret
notBow:
        cp   $05
        jr   nz, notArrows
        ; Load arrow graphics and render then as a dual sprite
        ld   de, $7B58
        call RenderActiveEntitySpritesPair
        ret
notArrows:
        ; Load the normal graphics
        ld   de, $7B5A
        jp   $3C77
    """), fill_nop=True)

    if shopsanity:
        rom.patch(0x04, 0x3952, ASM("call OpenDialogInTable0"), ASM("ld a, $15\nrst 8"))


def createShopRoom(rom, room_nr):
    re = RoomEditor(rom, room_nr)
    re.objects = [
                     ObjectHorizontal(1, 1, 0x00, 8),
                     ObjectHorizontal(1, 2, 0x00, 8),
                     ObjectHorizontal(1, 3, 0xCD, 8),
                     Object(6, 5, 0xCE),
                     Object(2, 0, 0xC7),
                     Object(7, 0, 0xC7),
                     Object(4, 7, 0xFD),
                 ] + re.getWarps()
    re.entities = [(7, 5, 0x4D)]
    re.animation_id = 0x04
    re.floor_object = 0x0D
    re.store(rom)
    # Fix the tileset
    rom.banks[0x20][0x2EB3 + room_nr - 0x100] = rom.banks[0x20][0x2EB3 + 0x2A1 - 0x100]

def changeShopPrices(rom, price1, price2):
    rom.patch(0x04, 0x37D3 + 1, "02", f"{price1//100:02d}")
    rom.patch(0x04, 0x37DC + 1, "00", f"{price1%100:02d}")
    rom.patch(0x04, 0x37E5 + 1, "00", f"{price1>>8:02x}")
    rom.patch(0x04, 0x37EE + 1, "C8", f"{price1&0xFF:02x}")
    rom.patch(0x04, 0x3732 + 0 * 11 + 3, "B2B0B0", f"B{price1//100:01x}B{(price1//10)%10:01x}B{price1%10:01x}")
    rom.texts[0x030] = rom.texts[0x030].replace(b"200", f"{price1:3d}".encode("ascii"))

    rom.patch(0x04, 0x37D3 + 5, "09", f"{price2//100:02d}")
    rom.patch(0x04, 0x37DC + 5, "80", f"{price2%100:02d}")
    rom.patch(0x04, 0x37E5 + 5, "03", f"{price2>>8:02x}")
    rom.patch(0x04, 0x37EE + 5, "D4", f"{price2&0xFF:02x}")
    rom.patch(0x04, 0x3732 + 4 * 11 + 3, "B9B8B0", f"B{price2//100:01x}B{(price2//10)%10:01x}B{price2%10:01x}")
    rom.texts[0x02C] = rom.texts[0x02C].replace(b"980", f"{price2:3d}".encode("ascii"))


def preventShopSaveAndQuitTheft(rom):
    rom.patch(0x01, 0x1DFA, ASM("call $2802"), ASM("call $7E80"))
    rom.patch(0x01, 0x3E80, "00" * 0x180, ASM(
    """
        call $2802
        ld   hl, wSubstractRupeeBufferHigh
        ld   a, [hl+]
        or   [hl]
        ret  z ; No subtract rupee count
        ld   a, 1
        ld   [wHasStolenFromShop], a ; Have the shopkeeper kill you for your transgression

loop:
        ld   hl, wSubstractRupeeBufferHigh
        ld   a, [hl+]
        or   [hl]
        ret  z
        
        ld   a, [wRupeeCountLow]
        sub  1
        daa
        ld   [wRupeeCountLow], a
        ld   a, [wRupeeCountHigh]
        sbc  0
        daa
        ld   [wRupeeCountHigh], a
        
        ld   a, [wSubstractRupeeBufferLow]
        sub  1
        ld   [wSubstractRupeeBufferLow], a
        ld   a, [wSubstractRupeeBufferHigh]
        sbc  0
        ld   [wSubstractRupeeBufferHigh], a
        
        jr   loop
    """), fill_nop=True)