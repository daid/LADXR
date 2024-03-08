BuildItemMessage:
    ld   hl, ItemNamePointers
    ldh  a, [$FFF1]
    ld   d, $00
    ld   e, a
    add  hl, de
    add  hl, de
    ldi  a, [hl]
    ld   h, [hl]
    ld   l, a

    ld   de, wCustomMessage
    jp   MessageCopyString

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
    ld   hl, M" for player X"
    call MessageCopyString
    ret

MessageAddFromPlayer:
    call MessagePad
    ld   hl, M" from player X"
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
    dw ItemNameZol
    dw ItemNameKey1
    dw ItemNameKey2
    dw ItemNameKey3
    dw ItemNameKey4
    dw ItemNameKey5
    dw ItemNameKey6
    dw ItemNameKey7
    dw ItemNameKey8
    dw ItemNameKey0
    dw ItemNameMap1
    dw ItemNameMap2
    dw ItemNameMap3
    dw ItemNameMap4
    dw ItemNameMap5
    dw ItemNameMap6
    dw ItemNameMap7
    dw ItemNameMap8
    dw ItemNameMap0
    dw ItemNameCompass1
    dw ItemNameCompass2
    dw ItemNameCompass3
    dw ItemNameCompass4
    dw ItemNameCompass5
    dw ItemNameCompass6
    dw ItemNameCompass7
    dw ItemNameCompass8
    dw ItemNameCompass0
    dw ItemNameStoneBeak1
    dw ItemNameStoneBeak2
    dw ItemNameStoneBeak3
    dw ItemNameStoneBeak4
    dw ItemNameStoneBeak5
    dw ItemNameStoneBeak6
    dw ItemNameStoneBeak7
    dw ItemNameStoneBeak8
    dw ItemNameStoneBeak0
    dw ItemNameNightmareKey1
    dw ItemNameNightmareKey2
    dw ItemNameNightmareKey3
    dw ItemNameNightmareKey4
    dw ItemNameNightmareKey5
    dw ItemNameNightmareKey6
    dw ItemNameNightmareKey7
    dw ItemNameNightmareKey8
    dw ItemNameNightmareKey0
    dw ItemNameToadstool
    dw ItemNameZol ; 0x51
    dw ItemNameZol ; 0x52
    dw ItemNameZol ; 0x53
    dw ItemNameZol ; 0x54
    dw ItemNameZol ; 0x55
    dw ItemNameZol ; 0x56
    dw ItemNameHammer ; 0x57
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

    dw M"Got the {HEART_PIECE}" ; 0x80
    dw M"Got the {BOWWOW}"
    dw M"Got {ARROWS_10}"
    dw M"Got the {SINGLE_ARROW}"
    dw M"Got the {MAX_POWDER_UPGRADE}"
    dw M"Got the {MAX_BOMBS_UPGRADE}"
    dw M"Got the {MAX_ARROWS_UPGRADE}"
    dw M"Got the {RED_TUNIC}"
    dw M"Got the {BLUE_TUNIC}"
    dw M"Got a {HEART_CONTAINER}"
    dw M"Got the {BAD_HEART_CONTAINER}"


    dw M"Got the {SONG1}"
    dw M"Got {SONG2}"
    dw M"Got {SONG3}"

    dw M"You've got the {INSTRUMENT1}"
    dw M"You've got the {INSTRUMENT2}"
    dw M"You've got the {INSTRUMENT3}"
    dw M"You've got the {INSTRUMENT4}"
    dw M"You've got the {INSTRUMENT5}"
    dw M"You've got the {INSTRUMENT6}"
    dw M"You've got the {INSTRUMENT7}"
    dw M"You've got the {INSTRUMENT8}"
    dw M"You've got the {ROOSTER}"

    dw M"You've got the {TRADING_ITEM_YOSHI_DOLL}"
    dw M"You've got the {TRADING_ITEM_RIBBON}"
    dw M"You've got the {TRADING_ITEM_DOG_FOOD}"
    dw M"You've got the {TRADING_ITEM_BANANAS}"
    dw M"You've got the {TRADING_ITEM_STICK}"
    dw M"You've got the {TRADING_ITEM_HONEYCOMB}"
    dw M"You've got the {TRADING_ITEM_PINEAPPLE}"
    dw M"You've got the {TRADING_ITEM_HIBISCUS}"
    dw M"You've got the {TRADING_ITEM_LETTER}"
    dw M"You've got the {TRADING_ITEM_BROOM}"
    dw M"You've got the {TRADING_ITEM_FISHING_HOOK}"
    dw M"You've got the {TRADING_ITEM_NECKLACE}"
    dw M"You've got the {TRADING_ITEM_SCALE}"
    dw M"You've got the {TRADING_ITEM_MAGNIFYING_GLASS}"

ItemNameNone:
    db m"NONE", $ff

ItemNamePowerBracelet:
    db m"Got the {POWER_BRACELET}", $ff
ItemNameShield:
    db m"Got a {SHIELD}", $ff
ItemNameBow:
    db m"Got the {BOW}", $ff
ItemNameHookshot:
    db m"Got the {HOOKSHOT}", $ff
ItemNameMagicRod:
    db m"Got the {MAGIC_ROD}", $ff
ItemNamePegasusBoots:
    db m"Got the {PEGASUS_BOOTS}", $ff
ItemNameOcarina:
    db m"Got the {OCARINA}", $ff
ItemNameFeather:
    db m"Got the {FEATHER}", $ff
ItemNameShovel:
    db m"Got the {SHOVEL}", $ff
ItemNameMagicPowder:
    db m"Got {MAGIC_POWDER}", $ff
ItemNameBomb:
    db m"Got {BOMB}", $ff
ItemNameSword:
    db m"Got a {SWORD}", $ff
ItemNameFlippers:
    db m"Got the {FLIPPERS}", $ff
ItemNameBoomerang:
    db m"Got the {BOOMERANG}", $ff
ItemNameSlimeKey:
    db m"Got the {SLIME_KEY}", $ff
ItemNameMedicine:
    db m"Got some {MEDICINE}", $ff
ItemNameTailKey:
    db m"Got the {TAIL_KEY}", $ff
ItemNameAnglerKey:
    db m"Got the {ANGLER_KEY}", $ff
ItemNameFaceKey:
    db m"Got the {FACE_KEY}", $ff
ItemNameBirdKey:
    db m"Got the {BIRD_KEY}", $ff
ItemNameGoldLeaf:
    db m"Got the {GOLD_LEAF}", $ff
ItemNameMap:
    db m"Got the {MAP}", $ff
ItemNameCompass:
    db m"Got the {COMPASS}", $ff
ItemNameStoneBeak:
    db m"Got the {STONE_BEAK}", $ff
ItemNameNightmareKey:
    db m"Got the {NIGHTMARE_KEY}", $ff
ItemNameSmallKey:
    db m"Got a {KEY}", $ff
ItemNameRupees50:
    db m"Got 50 {RUPEES}", $ff
ItemNameRupees20:
    db m"Got 20 {RUPEES}", $ff
ItemNameRupees100:
    db m"Got 100 {RUPEES}", $ff
ItemNameRupees200:
    db m"Got 200 {RUPEES}", $ff
ItemNameRupees500:
    db m"Got 500 {RUPEES}", $ff
ItemNameSeashell:
    db m"Got a {SEASHELL}", $ff
ItemNameMessage:
    db m"Got ... nothing?", $ff
ItemNameZol:
    db m"LOL, ZOL!", $ff
ItemNameHammer:
    db m"Got a HAMMER!", $ff
ItemNameKey1:
    db m"Got a {KEY1}", $ff
ItemNameKey2:
    db m"Got a {KEY2}", $ff
ItemNameKey3:
    db m"Got a {KEY3}", $ff
ItemNameKey4:
    db m"Got a {KEY4}", $ff
ItemNameKey5:
    db m"Got a {KEY5}", $ff
ItemNameKey6:
    db m"Got a {KEY6}", $ff
ItemNameKey7:
    db m"Got a {KEY7}", $ff
ItemNameKey8:
    db m"Got a {KEY8}", $ff
ItemNameKey0:
    db m"Got a {KEY0}", $ff
ItemNameMap1:
    db m"Got the {MAP1}", $ff
ItemNameMap2:
    db m"Got the {MAP2}", $ff
ItemNameMap3:
    db m"Got the {MAP3}", $ff
ItemNameMap4:
    db m"Got the {MAP4}", $ff
ItemNameMap5:
    db m"Got the {MAP5}", $ff
ItemNameMap6:
    db m"Got the {MAP6}", $ff
ItemNameMap7:
    db m"Got the {MAP7}", $ff
ItemNameMap8:
    db m"Got the {MAP8}", $ff
ItemNameMap0:
    db m"Got the {MAP0}", $ff
ItemNameCompass1:
    db m"Got the {COMPASS1}", $ff
ItemNameCompass2:
    db m"Got the {COMPASS2}", $ff
ItemNameCompass3:
    db m"Got the {COMPASS3}", $ff
ItemNameCompass4:
    db m"Got the {COMPASS4}", $ff
ItemNameCompass5:
    db m"Got the {COMPASS5}", $ff
ItemNameCompass6:
    db m"Got the {COMPASS6}", $ff
ItemNameCompass7:
    db m"Got the {COMPASS7}", $ff
ItemNameCompass8:
    db m"Got the {COMPASS8}", $ff
ItemNameCompass0:
    db m"Got the {COMPASS0}", $ff
ItemNameStoneBeak1:
    db m"Got the {STONE_BEAK1}", $ff
ItemNameStoneBeak2:
    db m"Got the {STONE_BEAK2}", $ff
ItemNameStoneBeak3:
    db m"Got the {STONE_BEAK3}", $ff
ItemNameStoneBeak4:
    db m"Got the {STONE_BEAK4}", $ff
ItemNameStoneBeak5:
    db m"Got the {STONE_BEAK5}", $ff
ItemNameStoneBeak6:
    db m"Got the {STONE_BEAK6}", $ff
ItemNameStoneBeak7:
    db m"Got the {STONE_BEAK7}", $ff
ItemNameStoneBeak8:
    db m"Got the {STONE_BEAK8}", $ff
ItemNameStoneBeak0:
    db m"Got the {STONE_BEAK0}", $ff
ItemNameNightmareKey1:
    db m"Got the {NIGHTMARE_KEY1}", $ff
ItemNameNightmareKey2:
    db m"Got the {NIGHTMARE_KEY2}", $ff
ItemNameNightmareKey3:
    db m"Got the {NIGHTMARE_KEY3}", $ff
ItemNameNightmareKey4:
    db m"Got the {NIGHTMARE_KEY4}", $ff
ItemNameNightmareKey5:
    db m"Got the {NIGHTMARE_KEY5}", $ff
ItemNameNightmareKey6:
    db m"Got the {NIGHTMARE_KEY6}", $ff
ItemNameNightmareKey7:
    db m"Got the {NIGHTMARE_KEY7}", $ff
ItemNameNightmareKey8:
    db m"Got the {NIGHTMARE_KEY8}", $ff
ItemNameNightmareKey0:
    db m"Got the {NIGHTMARE_KEY0}", $ff
ItemNameToadstool:
    db m"Got the {TOADSTOOL}", $ff
