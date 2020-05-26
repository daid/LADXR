from assembler import ASM


def addBank3F(rom):
    # Bank3F is used to initialize the tile data in VRAM:1 at the start of the rom.
    # The normal rom does not use this tile data to maintain GB compatibility.
    rom.patch(0, 0x0150, ASM("""
        cp   $11 ; is running on Game Boy Color?
        jr   nz, notGBC
        ldh  a, [$4d]
        and  $80 ; do we need to switch the CPU speed?
        jr   nz, speedSwitchDone
        ; switch to GBC speed
        ld   a, $30
        ldh  [$00], a
        ld   a, $01
        ldh  [$4d], a
        xor  a
        ldh  [$ff], a
        stop
        db $00

    speedSwitchDone:
        xor  a
        ldh  [$70], a
        ld   a, $01 ; isGBC = true
        jr   Init

    notGBC:
        xor  a ; isGBC = false
    Init:
        """), ASM("""
        ; Check if we are a color gameboy, we require a color version now.
    notGBC:
        cp $11
        jr nz, notGBC

        ; Switch to bank $3F to run our custom initializer
        ld   a, $3F
        ld   [$2100], a
        call $4000
        ; Switch back to bank 0 after loading our own initializer
        ld   a, $01
        ld   [$2100], a
        ; set a to 1 to indicate GBC
        ld   a, $01
        """), fill_nop=True)

    rom.patch(0x3F, 0x0000, None, ASM("""
        ; switch speed
        ld   a, $30
        ldh  [$00], a
        ld   a, $01
        ldh  [$4d], a
        xor  a
        ldh  [$ff], a
        stop
        db $00

        ; Switch VRAM bank
        ld   a, $01
        ldh  [$4F], a

        call $28CF ; display off

        ; Use the GBC DMA to transfer our tile data
        ld   a, $70
        ldh  [$51], a
        ld   a, $00
        ldh  [$52], a

        ld   a, $80
        ldh  [$53], a
        ld   a, $00
        ldh  [$54], a

        ld   a, $7F
        ldh  [$55], a

    waitTillTransferDone:
        ldh  a, [$55]
        and  $80
        jr z, waitTillTransferDone

        ld   a, $78
        ldh  [$51], a
        ld   a, $00
        ldh  [$52], a

        ld   a, $88
        ldh  [$53], a
        ld   a, $00
        ldh  [$54], a

        ld   a, $7F
        ldh  [$55], a

    waitTillTransferDone2:
        ldh  a, [$55]
        and  $80
        jr z, waitTillTransferDone2

        ; Switch VRAM bank back
        ld   a, $00
        ldh  [$4F], a

        ; Switch the display back on, else the later code hangs
        ld   a, $80
        ldh  [$40], a

    speedSwitchDone:
        xor  a
        ldh  [$70], a

        ret
        """))

    # Copy all normal item graphics
    rom.banks[0x3F][0x3000:0x3300] = rom.banks[0x2C][0x0800:0x0B00]  # main items
    rom.banks[0x3F][0x3300:0x3400] = rom.banks[0x2C][0x0C00:0x0D00]  # overworld key items
    rom.banks[0x3F][0x3400:0x3500] = rom.banks[0x32][0x3D00:0x3E00]  # dungeon key items
    # Add the slime key and mushroom which are not in the above sets
    rom.banks[0x3F][0x34C0:0x3500] = rom.banks[0x2C][0x28C0:0x2900]

    # Add the bowwow sprites
    rom.banks[0x3F][0x3500:0x3600] = rom.banks[0x2E][0x2400:0x2500]
