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
    rom.patch(0x04, 0x37C5, "0708", "0B05")
    # Patch the code that decides which shop to show.
    rom.patch(0x04, 0x3839, 0x388E, ASM("""
        push bc
        ld d, b
        ld e, $00

        ld a, [$77C5]
        call checkInventory
        jr nz, shopEntrySelected
        
        ld e, $04

        ld a, [$77C6]
        call checkInventory
        jr nz, shopEntrySelected

        ld e, $08
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
