import utils


def capacityUpgradeIcon():
    return utils.createTileData("""
   33
  3113
 311113
33311333
  3113
  3333
""")


def songItemGraphics():
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


def bingoBoard(rom):
    mural = rom.banks[0x32][0x1500:0x1500 + 8 * 0x10]
    mural[0x28:0x3A] = b'\x55\xAA\x00\xFF\x55\xAA\x00\xFF\x55\xAA\x00\xFF\x55\xAA\x00\xFF\x00\xFF'
    mural[0x48:0x5A] = b'\x55\xAA\x00\xFF\x55\xAA\x00\xFF\x55\xAA\x00\xFF\x55\xAA\x00\xFF\x00\xFF'
    return mural
