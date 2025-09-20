from assembler import ASM
import utils


def addBank3F(rom):
    # Bank3F is used to initialize the tile data in VRAM:1 at the start of the rom.
    # The normal rom does not use this tile data to maintain GB compatibility.
    rom.patch(0, 0x0150, ASM("""
        cp   $11 ; is running on Game Boy Color?
        jr   nz, notGBC
        ldh  a, [$FF4d]
        and  $80 ; do we need to switch the CPU speed?
        jr   nz, speedSwitchDone
        ; switch to GBC speed
        ld   a, $30
        ldh  [$FF00], a
        ld   a, $01
        ldh  [$FF4d], a
        xor  a
        ldh  [$FFff], a
        stop
        db $00

    speedSwitchDone:
        xor  a
        ldh  [$FF70], a
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

    rom.patch(0x3F, 0x0000, "00" * 0x200, ASM("""
        ; switch speed
        ld   a, $30
        ldh  [$FF00], a
        ld   a, $01
        ldh  [$FF4d], a
        xor  a
        ldh  [$FFff], a
        stop
        db $00

        ; Switch VRAM bank
        ld   a, $01
        ldh  [$FF4F], a

        call $28CF ; display off

        ; Use the GBC DMA to transfer our tile data
        ld   a, $68
        ldh  [$FF51], a
        ld   a, $00
        ldh  [$FF52], a

        ld   a, $80
        ldh  [$FF53], a
        ld   a, $00
        ldh  [$FF54], a

        ld   a, $7F
        ldh  [$FF55], a

        ld   a, $70
        ldh  [$FF51], a
        ld   a, $00
        ldh  [$FF52], a

        ld   a, $88
        ldh  [$FF53], a
        ld   a, $00
        ldh  [$FF54], a

        ld   a, $7F
        ldh  [$FF55], a


        ; Switch VRAM bank back
        ld   a, $00
        ldh  [$FF4F], a

        ; Switch the display back on, else the later code hangs
        ld   a, $80
        ldh  [$FF40], a

    speedSwitchDone:
        xor  a
        ldh  [$FF70], a

        ; Check if we are running on a bad emulator
        ldh  [$FF02], a
        ldh  a, [$FF02]
        and  $7c
        cp   $7c
        jr   nz, badEmu

        ; Enable the timer to run 32 times per second
        xor  a
        ldh  [$FF06], a
        ld   a, $04
        ldh  [$FF07], a

        ; Set SB to $FF to indicate we have no data from hardware
        ld   a, $FF
        ldh  [$FF01], a
        ret
badEmu:
        xor  a
        ldh  [$FF40], a ; switch display off
        ; Load some palette
        ld   a, $80
        ldh  [$FF68], a
        xor  a
        ldh  [$FF69], a
        ldh  [$FF69], a
        ldh  [$FF69], a
        ldh  [$FF69], a

        ; Load a different gfx tile for the first gfx
        cpl
        ld   hl, $8000
        ld   c, $10
.loop:
        ldi  [hl], a
        dec  c
        jr   nz, .loop

        ld   a, $01
        ld   [$9800], a
        ld   [$9820], a
        ld   [$9840], a
        ld   [$9860], a
        ld   [$9880], a

        ld   [$9801], a
        ld   [$9841], a
        ld   [$9881], a

        ld   [$9822], a
        ld   [$9862], a

        ld   [$9824], a
        ld   [$9844], a
        ld   [$9864], a
        ld   [$9884], a

        ld   [$9805], a
        ld   [$9845], a

        ld   [$9826], a
        ld   [$9846], a
        ld   [$9866], a
        ld   [$9886], a

        ld   [$9808], a
        ld   [$9828], a
        ld   [$9848], a
        ld   [$9868], a
        ld   [$9888], a

        ld   [$9809], a
        ld   [$9889], a

        ld   [$982A], a
        ld   [$984A], a
        ld   [$986A], a

        ld   [$9900], a
        ld   [$9920], a
        ld   [$9940], a
        ld   [$9960], a
        ld   [$9980], a

        ld   [$9901], a
        ld   [$9941], a
        ld   [$9981], a

        ld   [$9903], a
        ld   [$9923], a
        ld   [$9943], a
        ld   [$9963], a
        ld   [$9983], a

        ld   [$9904], a
        ld   [$9925], a
        ld   [$9906], a

        ld   [$9907], a
        ld   [$9927], a
        ld   [$9947], a
        ld   [$9967], a
        ld   [$9987], a

        ld   [$9909], a
        ld   [$9929], a
        ld   [$9949], a
        ld   [$9969], a
        ld   [$9989], a

        ld   [$998A], a

        ld   [$990B], a
        ld   [$992B], a
        ld   [$994B], a
        ld   [$996B], a
        ld   [$998B], a

        ; lcd on
        ld   a, $91
        ldh  [$FF40], a
blockBadEmu:
        di
        jr   blockBadEmu
        
        """), fill_nop=True)
    # Copy graphics we permanently want in VRAM bank 1, where we can use tile index 00-EF
    #   (the rest is used during overworld map transitions)
    #   Tiles 80-EF can be used in tilemaps/background. So are important for the inventory screen.
    def addSprite(index, from_bank, from_addr, *, count=2):
        rom.banks[0x3F][0x2800+index*0x10:0x2800+index*0x10+count*0x10] = rom.banks[from_bank][from_addr:from_addr+count*0x10]
    addSprite(0x80, 0x2C, 0x0900)  # Ocarina
    addSprite(0x82, 0x2C, 0x0920)  # Feather
    addSprite(0x84, 0x2C, 0x08E0)  # Magic powder
    addSprite(0x86, 0x2C, 0x28C0)  # Toadstool
    addSprite(0x88, 0x2C, 0x0840)  # Hammer (TODO: proper sprite)

    addSprite(0x8A, 0x2C, 0x28E0)  # Slime key
    addSprite(0x8C, 0x2C, 0x0C00)  # Tail key
    addSprite(0x8E, 0x2C, 0x0C20)  # Angler key
    addSprite(0x90, 0x2C, 0x0C40)  # Face key
    addSprite(0x92, 0x2C, 0x0C60)  # Bird key
    addSprite(0x94, 0x2C, 0x0CA0)  # Gold leaf
    addSprite(0x96, 0x32, 0x3D00)  # Map
    addSprite(0x98, 0x32, 0x3D20)  # Compass
    addSprite(0x9A, 0x32, 0x3D40)  # Beak
    addSprite(0x9C, 0x32, 0x3D60)  # Nightmare key
    addSprite(0x9E, 0x32, 0x3DA0)  # Small key

    addSprite(0x30, 0x2C, 0x0A60) # Create rupee for palettes 0-3
    for n in range(0x2800+0x300, 0x2800+0x300+0x20, 2):
        rom.banks[0x3F][n+1] ^= rom.banks[0x3F][n]
    # Capacity upgrade arrow (0x32)
    rom.banks[0x3F][0x2800+0x320:0x2800+0x320+0x10] = utils.createTileData("""
   33
  3113
 311113
33311333
  3113
  3333
""")
    rom.banks[0x3F][0x2800+0x330:0x2800+0x330+0x10] = rom.banks[0x3F][0x2800+0x320:0x2800+0x320+0x10]
    addSprite(0x34, 0x35, 0x0F00)  # Tunic
    # Song symbols
    rom.banks[0x3F][0x2800 + 0x360:0x2800 + 0x360+0x60] = getSongGraphics(rom)

    addSprite(0xA0, 0x2C, 0x09A0, count=4)  # Yoshi
    addSprite(0xA4, 0x2C, 0x0400, count=52)  # Other trading items

    # Instruments
    addSprite(0x00, 0x31, 0x1000, count=32)  # Instruments
    rom.patch(0x19, 0x0BAC,  # Patch egg song to use 2nd vram bank sprites
          "5006520654065606"
          "58065A065C065E06"
          "6006620664066606"
          "68066A066C066E06",
          "000E020E040E060E"
          "080E0A0E0C0E0E0E"
          "100E120E140E160E"
          "180E1A0E1C0E1E0E"
    )

    # Rooster
    addSprite(0x20, 0x32, 0x1D00, count=16)  # Rooster (side)
    rom.patch(0x19, 0x19BC,  # Rooster OAM data
              "42234023" "46234423" "40034203" "44034603" "4C034C23" "4E034E23" "48034823" "4A034A23",
              "222B202B" "262B242B" "200B220B" "240B260B" "2C0B2C2B" "2E0B2E2B" "280B282B" "2A0B2A2B")
    # Replace some main ocarina/feather item graphics with the rooster for subscreen display
    rom.banks[0x2C][0x0900:0x0940] = utils.createTileData(utils.tileDataToString(rom.banks[0x32][0x1D00:0x1D40]), " 321")

    addSprite(0x70, 0x2E, 0x2400, count=16)  # Bowwow
    addSprite(0x68, 0x32, 0x2500, count=8)  # Cuccu
    rom.patch(0x05, 0x0514,  # Patch the cucco graphics to load from 2nd vram bank
              "5001" "5201" "5401" "5601" "5221" "5021" "5621" "5421",
              "6809" "6A09" "6C09" "6E09" "6A29" "6829" "6E29" "6C29")
    addSprite(0x62, 0x2E, 0x1120, count=6)  # Zol+MiniZol
    # Patch gel(zol) entity to load sprites from the 2nd bank
    rom.patch(0x06, 0x3C09, "5202522254025422" "5200522054005420", "620A622A640A642A" "6208622864086428")
    rom.patch(0x07, 0x329B, "FFFFFFFF" "FFFFFFFF" "54005420" "52005220" "56005600",
                            "FFFFFFFF" "FFFFFFFF" "64086428" "62086228" "66086608")
    rom.patch(0x06, 0x3BFA, "56025622", "660A662A")  # MiniZol

    addSprite(0x5A, 0x32, 0x1800, count=8)  # Ghost sprites (bah, only because sprite data in start house is full...)

    addSprite(0x52, 0x32, 0x1500, count=8)  # Bingo board
    rom.banks[0x3F][0x2800+0x520+0x28:0x2800+0x520+0x3A] = b'\x55\xAA\x00\xFF\x55\xAA\x00\xFF\x55\xAA\x00\xFF\x55\xAA\x00\xFF\x00\xFF'
    rom.banks[0x3F][0x2800+0x520+0x48:0x2800+0x520+0x5A] = b'\x55\xAA\x00\xFF\x55\xAA\x00\xFF\x55\xAA\x00\xFF\x55\xAA\x00\xFF\x00\xFF'

    addSprite(0x3C, 0x2C, 0x0040, count=6)  # Magic rod attack
    for n in range(0x2800+0x3C0, 0x2800+0x3C0+0x20, 2):
        rom.banks[0x3F][n+1] ^= rom.banks[0x3F][n]
    rom.patch(0x02, 0x12F0,
                "0608" "0806" "04FF" "FF04"
                "04FF" "FF04" "0608" "0806"
                "0202" "2222" "2202" "0242"
                "2202" "0222" "0202" "2222",
                "3E40" "403E" "3CFF" "FF3C"
                "3CFF" "FF3C" "3E40" "403E"
                "0A0A" "2A2A" "2A0A" "0A4A"
                "2A0A" "022A" "0A0A" "2A2A")

    # Reserve 8 tiles for pet followers (E8-EF)
    addSprite(0xE8, 0x34, 0x3F00, count=8)


def getSongGraphics(rom):
    return utils.createTileData("""


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