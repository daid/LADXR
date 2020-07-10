BuildItemMessage:
    ld   hl, ItemNamePointers
    ldh  a, [$F1]
    ld   d, $00
    ld   e, a
    add  hl, de
    add  hl, de
    ldi  a, [hl]
    ld   h, [hl]
    ld   l, a

    ld   de, wCustomMessage
    jp   MessageCopyString

FoundItemForOtherPlayerPostfix:
    db m" for another    player", $ff
GotItemFromOtherPlayerPostfix:
    db m" from another   player", $ff

MessagePad:
    jr .start
.loop:
    ld   a, $20
    ld   [de], a
    inc  de
    ld   a, $ff
    ld   [de], a
.start:
    ld   a, e
    and  $0F
    jr   nz, .loop
    ret

MessageAddTargetPlayer:
    call MessagePad
    ld   hl, FoundItemForOtherPlayerPostfix
    call MessageCopyString
    ret

MessageAddFromPlayer:
    call MessagePad
    ld   hl, GotItemFromOtherPlayerPostfix
    call MessageCopyString
    ret

MessageCopyString:
.loop:
    ldi  a, [hl]
    ld   [de], a
    cp   $ff
    ret  z
    inc  de
    jr   .loop

MessageAddSpace:
    ld   a, $20
    ld   [de], a
    inc  de
    ld   a, $ff
    ld   [de], a
    ret

ItemNamePointers:
    dw ItemNamePowerBracelet
    dw ItemNameShield
    dw ItemNameBow
    dw ItemNameHookshot
    dw ItemNameMagicRod
    dw ItemNamePegasusBoots
    dw ItemNameOcarina
    dw ItemNameFeather
    dw ItemNameShovel
    dw ItemNameMagicPowder
    dw ItemNameBomb
    dw ItemNameSword
    dw ItemNameFlippers
    dw ItemNameNone
    dw ItemNameBoomerang
    dw ItemNameSlimeKey
    dw ItemNameMedicine
    dw ItemNameTailKey
    dw ItemNameAnglerKey
    dw ItemNameFaceKey
    dw ItemNameBirdKey
    dw ItemNameGoldLeaf
    dw ItemNameMap
    dw ItemNameCompass
    dw ItemNameStoneBeak
    dw ItemNameNightmareKey
    dw ItemNameSmallKey
    dw ItemNameRupees50
    dw ItemNameRupees20
    dw ItemNameRupees100
    dw ItemNameRupees200
    dw ItemNameRupees500
    dw ItemNameSeashell
    dw ItemNameMessage
    dw ItemNameNone
    dw ItemNameKey1
    dw ItemNameKey2
    dw ItemNameKey3
    dw ItemNameKey4
    dw ItemNameKey5
    dw ItemNameKey6
    dw ItemNameKey7
    dw ItemNameKey8
    dw ItemNameKey9
    dw ItemNameMap1
    dw ItemNameMap2
    dw ItemNameMap3
    dw ItemNameMap4
    dw ItemNameMap5
    dw ItemNameMap6
    dw ItemNameMap7
    dw ItemNameMap8
    dw ItemNameMap9
    dw ItemNameCompass1
    dw ItemNameCompass2
    dw ItemNameCompass3
    dw ItemNameCompass4
    dw ItemNameCompass5
    dw ItemNameCompass6
    dw ItemNameCompass7
    dw ItemNameCompass8
    dw ItemNameCompass9
    dw ItemNameStoneBeak1
    dw ItemNameStoneBeak2
    dw ItemNameStoneBeak3
    dw ItemNameStoneBeak4
    dw ItemNameStoneBeak5
    dw ItemNameStoneBeak6
    dw ItemNameStoneBeak7
    dw ItemNameStoneBeak8
    dw ItemNameStoneBeak9
    dw ItemNameNightmareKey1
    dw ItemNameNightmareKey2
    dw ItemNameNightmareKey3
    dw ItemNameNightmareKey4
    dw ItemNameNightmareKey5
    dw ItemNameNightmareKey6
    dw ItemNameNightmareKey7
    dw ItemNameNightmareKey8
    dw ItemNameNightmareKey9
    dw ItemNameToadstool
    dw ItemNameNone ; 0x51
    dw ItemNameNone ; 0x52
    dw ItemNameNone ; 0x53
    dw ItemNameNone ; 0x54
    dw ItemNameNone ; 0x55
    dw ItemNameNone ; 0x56
    dw ItemNameNone ; 0x57
    dw ItemNameNone ; 0x58
    dw ItemNameNone ; 0x59
    dw ItemNameNone ; 0x5a
    dw ItemNameNone ; 0x5b
    dw ItemNameNone ; 0x5c
    dw ItemNameNone ; 0x5d
    dw ItemNameNone ; 0x5e
    dw ItemNameNone ; 0x5f
    dw ItemNameNone ; 0x60
    dw ItemNameNone ; 0x61
    dw ItemNameNone ; 0x62
    dw ItemNameNone ; 0x63
    dw ItemNameNone ; 0x64
    dw ItemNameNone ; 0x65
    dw ItemNameNone ; 0x66
    dw ItemNameNone ; 0x67
    dw ItemNameNone ; 0x68
    dw ItemNameNone ; 0x69
    dw ItemNameNone ; 0x6a
    dw ItemNameNone ; 0x6b
    dw ItemNameNone ; 0x6c
    dw ItemNameNone ; 0x6d
    dw ItemNameNone ; 0x6e
    dw ItemNameNone ; 0x6f
    dw ItemNameNone ; 0x70
    dw ItemNameNone ; 0x71
    dw ItemNameNone ; 0x72
    dw ItemNameNone ; 0x73
    dw ItemNameNone ; 0x74
    dw ItemNameNone ; 0x75
    dw ItemNameNone ; 0x76
    dw ItemNameNone ; 0x77
    dw ItemNameNone ; 0x78
    dw ItemNameNone ; 0x79
    dw ItemNameNone ; 0x7a
    dw ItemNameNone ; 0x7b
    dw ItemNameNone ; 0x7c
    dw ItemNameNone ; 0x7d
    dw ItemNameNone ; 0x7e
    dw ItemNameNone ; 0x7f
    dw ItemNameHeartPiece ; 0x80
    dw ItemNameBowwow
    dw ItemName10Arrows
    dw ItemNameSingleArrow
    dw ItemNamePowderUpgrade
    dw ItemNameBombUpgrade
    dw ItemNameArrowUpgrade
    dw ItemNameRedTunic
    dw ItemNameBlueTunic
    dw ItemNameHeartContainer
    dw ItemNameBadHeartContainer
    dw ItemNameSong1
    dw ItemNameSong2
    dw ItemNameSong3

ItemNameNone:
    db m"NONE", $ff

ItemNamePowerBracelet:
    db m"Got the Power Bracelet", $ff
ItemNameShield:
    db m"Got a Shield", $ff
ItemNameBow:
    db m"Got the Bow", $ff
ItemNameHookshot:
    db m"Got the Hookshot", $ff
ItemNameMagicRod:
    db m"Got the Magic Rod", $ff
ItemNamePegasusBoots:
    db m"Got the Pegasus Boots", $ff
ItemNameOcarina:
    db m"Got the Ocarina", $ff
ItemNameFeather:
    db m"Got the Feather", $ff
ItemNameShovel:
    db m"Got the Shovel", $ff
ItemNameMagicPowder:
    db m"Got Magic Powder", $ff
ItemNameBomb:
    db m"Got Bombs", $ff
ItemNameSword:
    db m"Got a Sword", $ff
ItemNameFlippers:
    db m"Got the Flippers", $ff
ItemNameBoomerang:
    db m"Got the Boomerang", $ff
ItemNameSlimeKey:
    db m"Got the Slime Key", $ff
ItemNameMedicine:
    db m"Got some Medicine", $ff
ItemNameTailKey:
    db m"Got the Tail Key", $ff
ItemNameAnglerKey:
    db m"Got the Angler Key", $ff
ItemNameFaceKey:
    db m"Got the Face Key", $ff
ItemNameBirdKey:
    db m"Got the Bird Key", $ff
ItemNameGoldLeaf:
    db m"Got the Golden Leaf", $ff
ItemNameMap:
    db m"Got the Dungeon Map", $ff
ItemNameCompass:
    db m"Got the Dungeon Compass", $ff
ItemNameStoneBeak:
    db m"Got the Stone Beak", $ff
ItemNameNightmareKey:
    db m"Got the Nightmare Key", $ff
ItemNameSmallKey:
    db m"Got a Small Key", $ff
ItemNameRupees50:
    db m"Got 50 Rupees", $ff
ItemNameRupees20:
    db m"Got 20 Rupees", $ff
ItemNameRupees100:
    db m"Got 100 Rupees", $ff
ItemNameRupees200:
    db m"Got 200 Rupees", $ff
ItemNameRupees500:
    db m"Got 500 Rupees", $ff
ItemNameSeashell:
    db m"Got a Secret Seashell", $ff
ItemNameMessage:
    db m"Got ... nothing?", $ff
ItemNameKey1:
    db m"Got a Tail Cave Small Key", $ff
ItemNameKey2:
    db m"Got a Bottle Grotto Small Key", $ff
ItemNameKey3:
    db m"Got a Key Cavern Small Key", $ff
ItemNameKey4:
    db m"Got a Angler's Tunnel Small Key", $ff
ItemNameKey5:
    db m"Got a Catfish's Maw Small Key", $ff
ItemNameKey6:
    db m"Got a Face Shrine Small Key", $ff
ItemNameKey7:
    db m"Got a Eagle's Tower Small Key", $ff
ItemNameKey8:
    db m"Got a Turtle Rock Small Key", $ff
ItemNameKey9:
    db m"Got a Color Dungeon Small Key", $ff
ItemNameMap1:
    db m"Got the Tail Cave Map", $ff
ItemNameMap2:
    db m"Got the Bottle Grotto Map", $ff
ItemNameMap3:
    db m"Got the Key Cavern Map", $ff
ItemNameMap4:
    db m"Got the Angler's Tunnel Map", $ff
ItemNameMap5:
    db m"Got the Catfish's Maw Map", $ff
ItemNameMap6:
    db m"Got the Face Shrine Map", $ff
ItemNameMap7:
    db m"Got the Eagle's Tower Map", $ff
ItemNameMap8:
    db m"Got the Turtle Rock Map", $ff
ItemNameMap9:
    db m"Got the Color Dungeon Map", $ff
ItemNameCompass1:
    db m"Got the Tail Cave Compass", $ff
ItemNameCompass2:
    db m"Got the Bottle Grotto Compass", $ff
ItemNameCompass3:
    db m"Got the Key Cavern Compass", $ff
ItemNameCompass4:
    db m"Got the Angler's Tunnel Compass", $ff
ItemNameCompass5:
    db m"Got the Catfish's Maw Compass", $ff
ItemNameCompass6:
    db m"Got the Face Shrine Compass", $ff
ItemNameCompass7:
    db m"Got the Eagle's Tower Compass", $ff
ItemNameCompass8:
    db m"Got the Turtle Rock Compass", $ff
ItemNameCompass9:
    db m"Got the Color Dungeon Compass", $ff
ItemNameStoneBeak1:
    db m"Got the Tail Cave Stone Beak", $ff
ItemNameStoneBeak2:
    db m"Got the Bottle Grotto Stone Beak", $ff
ItemNameStoneBeak3:
    db m"Got the Key Cavern Stone Beak", $ff
ItemNameStoneBeak4:
    db m"Got the Angler's Tunnel Stone Beak", $ff
ItemNameStoneBeak5:
    db m"Got the Catfish's Maw Stone Beak", $ff
ItemNameStoneBeak6:
    db m"Got the Face Shrine Stone Beak", $ff
ItemNameStoneBeak7:
    db m"Got the Eagle's Tower Stone Beak", $ff
ItemNameStoneBeak8:
    db m"Got the Turtle Rock Stone Beak", $ff
ItemNameStoneBeak9:
    db m"Got the Color Dungeon Stone Beak", $ff
ItemNameNightmareKey1:
    db m"Got the Tail Cave Nightmare Key", $ff
ItemNameNightmareKey2:
    db m"Got the Bottle Grotto Nightmare Key", $ff
ItemNameNightmareKey3:
    db m"Got the Key Cavern Nightmare Key", $ff
ItemNameNightmareKey4:
    db m"Got the Angler's Tunnel Nightmare Key", $ff
ItemNameNightmareKey5:
    db m"Got the Catfish's Maw Nightmare Key", $ff
ItemNameNightmareKey6:
    db m"Got the Face Shrine Nightmare Key", $ff
ItemNameNightmareKey7:
    db m"Got the Eagle's Tower Nightmare Key", $ff
ItemNameNightmareKey8:
    db m"Got the Turtle Rock Nightmare Key", $ff
ItemNameNightmareKey9:
    db m"Got the Color Dungeon Nightmare Key", $ff
ItemNameToadstool:
    db m"Got the Toadstool", $ff

ItemNameHeartPiece:
    db m"Got the Piece of Heart", $ff
ItemNameBowwow:
    db m"Got the Bowwow", $ff
ItemName10Arrows:
    db m"Got 10 Arrows", $ff
ItemNameSingleArrow:
    db m"Got the Single Arrow", $ff
ItemNamePowderUpgrade:
    db m"Got the Magic Powder Upgrade", $ff
ItemNameBombUpgrade:
    db m"Got the Bombs Upgrade", $ff
ItemNameArrowUpgrade:
    db m"Got the Arrow Upgrade", $ff
ItemNameRedTunic:
    db m"Got the Red Tunic", $ff
ItemNameBlueTunic:
    db m"Got the Blue Tunic", $ff
ItemNameHeartContainer:
    db m"Got the Heart Container", $ff
ItemNameBadHeartContainer:
    db m"Got the Bad Heart Container", $ff
ItemNameSong1:
    db m"Got the Ballad of the Wind Fish", $ff
ItemNameSong2:
    db m"Got the Manbo's Mambo", $ff
ItemNameSong3:
    db m"Got Frog's Song of Soul", $ff
