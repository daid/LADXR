from assembler import ASM
import utils


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
        jr Init
    notGBC:
        xor a
    Init:
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

        ld   a, $70
        ldh  [$51], a
        ld   a, $00
        ldh  [$52], a

        ld   a, $90
        ldh  [$53], a
        ld   a, $00
        ldh  [$54], a

        ld   a, $7F
        ldh  [$55], a

    waitTillTransferDone3:
        ldh  a, [$55]
        and  $80
        jr z, waitTillTransferDone3

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
    # Create ruppee for palettes 0-3
    rom.banks[0x3F][0x3380:0x33A0] = rom.banks[0x3F][0x3260:0x3280]
    for n in range(0x3380, 0x33A0, 2):
        rom.banks[0x3F][n+1] ^= rom.banks[0x3F][n]

    # Create capacity upgrade arrows
    rom.banks[0x3F][0x3230:0x3240] = utils.createTileData("""
   33
  3113
 311113
33311333
  3113
  3333
""")
    rom.banks[0x3F][0x3220:0x3230] = rom.banks[0x3F][0x3230:0x3240]
    for n in range(0x3220, 0x3240, 2):
        rom.banks[0x3F][n] |= rom.banks[0x3F][n + 1]

    # Add the slime key and mushroom which are not in the above sets
    rom.banks[0x3F][0x34C0:0x3500] = rom.banks[0x2C][0x28C0:0x2900]
    # Add tunic sprites as well.
    rom.banks[0x3F][0x3480:0x34A0] = rom.banks[0x35][0x0F00:0x0F20]

    # Add the bowwow sprites
    rom.banks[0x3F][0x3500:0x3600] = rom.banks[0x2E][0x2400:0x2500]

    # Zol sprites, so we can have zol anywhere from a chest
    rom.banks[0x3F][0x3600:0x3640] = rom.banks[0x2E][0x1120:0x1160]

    # Elephant statue
    rom.banks[0x3F][0x3640:0x3680] = rom.banks[0x2E][0x2680:0x26C0]
    # Cucco
    rom.banks[0x3F][0x3680:0x3700] = rom.banks[0x32][0x2500:0x2580]
    # Song symbols
    rom.banks[0x3F][0x3700:0x3760] = utils.createTileData("""


     ...
  . .222
 .2.2222
.22.222.
.22222.3
.2..22.3
 .33...3
 .33.3.3
 ..233.3
.22.2333
.222.233
 .222...
  ...
""" + """


      ..
     .22
    .223
   ..222
  .33.22
  .3..22
  .33.33
   ..23.
  ..233.
 .22.333
.22..233
 ..  .23
      ..
""" + """


    ...
   .222.
  .2.332
  .23.32
  .233.2
 .222222
.2222222
.2..22.2
.2.3.222
.22...22
 .2333..
  .23333
   .....""", " .23")

    # Instruments
    rom.banks[0x3F][0x3800:0x3A00] = rom.banks[0x31][0x1000:0x1200]

    # Patch the cucco graphics to load from 2nd vram bank
    rom.patch(0x05, 0x0514,
              "5001" "5201" "5401" "5601" "5221" "5021" "5621" "5421",
              "6809" "6A09" "6C09" "6E09" "6A29" "6829" "6E29" "6C29")
