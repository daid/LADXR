from assembler import ASM


def fixShop(rom):
    # Turn the shop into:
    # KEYITEM (x2), SHIELD, ARROWS, BOMBS
    rom.patch(0x04, 0x37b5,
              "01020300" "01020304" "05020304" "06020304",
              "01030604" "05030604" "00030604" "00000000")
    # Move shield visuals to the 2nd slot, and arrow to 3th slot
    rom.patch(0x04, 0x3732 + 22, "986A027FB2B098AC01BAB1", "9867027FB2B098A801BAB1")
    rom.patch(0x04, 0x3732 + 55, "986302B1B07F98A4010A09", "986B02B1B07F98AC010A09")

    # Just use a fixed location in memory to store which inventory we check for, easier to patch later on.
    rom.patch(0x04, 0x37C5, "0708", "0802")
    # Patch the code that decides which shop to show.
    rom.patch(0x04, 0x3839, 0x388E, ASM("""
        push bc

        ; load $0000 into de
        ld d, b
        ld e, b
        
        ; Get the room status, and check if bits are set for buying one time items
        ldh  a, [$F8]
        and  $10
        jr   z, shopEntrySelected
        ld   e, $04
        
        ldh  a, [$F8]
        and  $20
        jr   z, shopEntrySelected
        ld   e, $08

        jr shopEntrySelected

checkInventory:
        ld hl, $DB7D ; item traded for the boomerang
        cp [hl]
        ret z
        ld hl, $DB00 ; inventory
        ld c, $0C
loop:
        cp [hl]
        ret z
        inc hl
        dec c
        jr nz, loop
        and a
        ret

shopEntrySelected:

        ld   hl, $77B5 ; load shop table into C505-C509
        add  hl, de
        ld   de, $C505 
        ld   c, $04
loop2:
        ldi  a, [hl]
        ld   [de], a
        inc  de
        dec  c
        jr   nz, loop2
    
        ; Check if we have the shield or the bow to see if we need to remove certain entries from the shop
        ld   a, [$DB44]
        and  a
        jr   nz, hasShield
        ld   [$C506], a ; Remove shield buy option
hasShield:

        ld   a, $05
        call checkInventory
        jr   z, hasBow
        xor  a
        ld   [$C507], a ; Remove arrow buy option
hasBow:

        pop  bc
        call $3B12 ; increase entity state
    """, 0x7839), fill_nop=True)

    # We do not have enough room at the shovel/bow buy entry to handle this
    # So jump to a bit where we have some more space to work, as there is some dead code in the shop.
    rom.patch(0x04, 0x3AA9, 0x3AAE, ASM("jp $7AC3"), fill_nop=True)
    rom.patch(0x04, 0x3AC3, 0x3AD8, ASM("""
        ; Call our chest item giving code.
        ld   a, [$77C5]
        ldh  [$F1], a
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
        ldh  [$F1], a
        ld   a, $02
        rst  8
        ; Update the room status to mark second item as bought
        ld   hl, $DAA1
        ld   a, [hl]
        or   $20
        ld   [hl], a
        ret
    """), fill_nop=True)
