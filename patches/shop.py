from assembler import ASM


def fixShop(rom):
    # Move shield visuals to the 2nd slot, and arrow to 3th slot
    rom.patch(0x04, 0x3732 + 22, "986A027FB2B098AC01BAB1", "9867027FB2B098A801BAB1")
    rom.patch(0x04, 0x3732 + 55, "986302B1B07F98A4010A09", "986B02B1B07F98AC010A09")

    # Just use a fixed location in memory to store which inventory we give.
    rom.patch(0x04, 0x37C5, "0708", "0802")

    # Patch the code that decides which shop to show.
    rom.patch(0x04, 0x3839, 0x388E, ASM("""
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
        ldh  a, [$FFF8]
        bit  4, a
        jr   nz, checkForSecondKeyItem
        ld   a, $01
        ld   [de], a
        jr   checkForShield
checkForSecondKeyItem:
        bit  5, a
        jr   nz, checkForShield
        ld   a, $05
        ld   [de], a

checkForShield:
        inc  de
        ; Check if we have the shield or the bow to see if we need to remove certain entries from the shop
        ld   a, [$DB44]
        and  a
        jr   z, hasNoShieldLevel
        ld   a, $03
        ld   [de], a ; Add shield buy option
hasNoShieldLevel:

        inc  de
        ld   a, $05
        call checkInventory
        jr   nz, hasNoBow
        ld   a, $06
        ld   [de], a ; Add arrow buy option
hasNoBow:

        inc  de
        ld   a, $02
        call checkInventory
        jr   nz, hasNoBombs
        ld   a, $04
        ld   [de], a ; Add bomb buy option
hasNoBombs:

        pop  bc
        call $3B12 ; increase entity state
    """, 0x7839), fill_nop=True)

    # We do not have enough room at the shovel/bow buy entry to handle this
    # So jump to a bit where we have some more space to work, as there is some dead code in the shop.
    rom.patch(0x04, 0x3AA9, 0x3AAE, ASM("jp $7AC0"), fill_nop=True)
    rom.patch(0x04, 0x3AC0, 0x3AD8, ASM("""
        ; Call our chest item giving code.
        ld   a, [$77C5]
        ldh  [$FFF1], a
        ld   a, $02
        rst  8
        ; Update the room status to mark first item as bought
        ld   hl, $DAA1
        ld   a, [hl]
        or   $10
        ld   [hl], a
        ret
    """), fill_nop=True)
    rom.patch(0x04, 0x3A73, 0x3A7E, ASM("jp $7A91"), fill_nop=True)
    rom.patch(0x04, 0x3A91, 0x3AA9, ASM("""
        ; Call our chest item giving code.
        ld   a, [$77C6]
        ldh  [$FFF1], a
        ld   a, $02
        rst  8
        ; Update the room status to mark second item as bought
        ld   hl, $DAA1
        ld   a, [hl]
        or   $20
        ld   [hl], a
        ret
    """), fill_nop=True)

    # Patch shop item graphics rendering to use some new code at the end of the bank.
    rom.patch(0x04, 0x3B91, 0x3BAC, ASM("""
        call $7FD0
        jr   $16 ; skip over the NOP's
    """), fill_nop=True)
    rom.patch(0x04, 0x3BD3, 0x3BE3, ASM("""
        jp   $7FD0
    """), fill_nop=True)
    rom.patch(0x04, 0x3FD0, "00" * 42, ASM("""
        ; Check if first key item
        and  a
        jr   nz, notShovel
        ld   a, [$77C5]
        ldh  [$FFF1], a
        ld   a, $01
        rst  8
        ret
notShovel:
        cp   $04
        jr   nz, notBow
        ld   a, [$77C6]
        ldh  [$FFF1], a
        ld   a, $01
        rst  8
        ret
notBow:
        cp   $05
        jr   nz, notArrows
        ; Load arrow graphics and render then as a dual sprite
        ld   de, $7B58
        call $3BC0
        ret
notArrows:
        ; Load the normal graphics
        ld   de, $7B5A
        jp   $3C77
    """), fill_nop=True)


def changeShopPrices(rom, price1, price2):
    rom.patch(0x04, 0x37D3 + 1, "09", f"{price1//100:02d}")
    rom.patch(0x04, 0x37DC + 1, "80", f"{price1%100:02d}")
    rom.patch(0x04, 0x37E5 + 1, "03", f"{price1>>8:02x}")
    rom.patch(0x04, 0x37EE + 1, "D4", f"{price1&0xFF:02x}")
    rom.patch(0x04, 0x3732 + 0 * 11 + 3, "B2B0B0", f"B{price1//100:01x}B{(price1//10)%10:01x}B{price1%10:01x}")
    rom.texts[0x030] = rom.texts[0x030].replace(b"200", f"{price1:3d}".encode("ascii"))

    rom.patch(0x04, 0x37D3 + 5, "09", f"{price2//100:02d}")
    rom.patch(0x04, 0x37DC + 5, "80", f"{price2%100:02d}")
    rom.patch(0x04, 0x37E5 + 5, "03", f"{price2>>8:02x}")
    rom.patch(0x04, 0x37EE + 5, "D4", f"{price2&0xFF:02x}")
    rom.patch(0x04, 0x3732 + 4 * 11 + 3, "B9B8B0", f"B{price2//100:01x}B{(price2//10)%10:01x}B{price2%10:01x}")
    rom.texts[0x02C] = rom.texts[0x02C].replace(b"980", f"{price2:3d}".encode("ascii"))
