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

ShopItemPresentationDialogs:
    db $30 ; Item 1
    db $31 ; 3 hearts
    db $32 ; Shield
    db $33 ; 10 bombs
    db $2C ; Item 2
    db $2D ; 10 arrows

OverrideShopMessage:
    ld   a, [wItemPickedUpInShop]
    dec  a
    jr   z, DoShopMessage1
    cp   4
    jr   z, DoShopMessage2
    ld   e, a
    ld   d, b
    ld   hl, ShopItemPresentationDialogs
    add  hl, de
    ld   a, [hl]
    call OpenDialogInTable0
    ret

DoShopMessage1:
    call GetRoomItem
    ld   hl, ShopItemNamePointers
    ldh  a, [$FFF1]
    ld   d, $00
    ld   e, a
    add  hl, de
    add  hl, de
    ldi  a, [hl]
    ld   h, [hl]
    ld   l, a

    ld   de, wCustomMessage
    call MessageCopyString
    call MessagePad
    ld   hl, M"Only 100 {RUPEES}? _ _ Buy  No Way"
    call MessageCopyString
    ld   a, $FE
    ld   [de], a
    ld   a, $C9
    call OpenDialogInTable0
    ret

DoShopMessage2:
    ld   d, $02
    ldh  a, [hMapRoom]
    ld   e, a
    call $29ED ; Get chest item (in A)
    ld   hl, ShopItemNamePointers
    ld   d, $00
    ld   e, a
    add  hl, de
    add  hl, de
    ldi  a, [hl]
    ld   h, [hl]
    ld   l, a

    ld   de, wCustomMessage
    call MessageCopyString
    call MessagePad
    ld   hl, M"Only 200 {RUPEES}? _ _ Buy  No Way"
    call MessageCopyString
    ld   a, $FE
    ld   [de], a
    ld   a, $C9
    call OpenDialogInTable0
    ret

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
    dw M"Got the {POWER_BRACELET}"
    dw M"Got a {SHIELD}"
    dw M"Got the {BOW}"
    dw M"Got the {HOOKSHOT}"
    dw M"Got the {MAGIC_ROD}"
    dw M"Got the {PEGASUS_BOOTS}"
    dw M"Got the {OCARINA}"
    dw M"Got the {FEATHER}"
    dw M"Got the {SHOVEL}"
    dw M"Got {MAGIC_POWDER}"
    dw M"Got {BOMB}"
    dw M"Got a {SWORD}"
    dw M"Got the {FLIPPERS}"
    dw ItemNameNone
    dw M"Got the {BOOMERANG}"
    dw M"Got the {SLIME_KEY}"
    dw M"Got some {MEDICINE}"
    dw M"Got the {TAIL_KEY}"
    dw M"Got the {ANGLER_KEY}"
    dw M"Got the {FACE_KEY}"
    dw M"Got the {BIRD_KEY}"
    dw M"Got the {GOLD_LEAF}"
    dw M"Got the {MAP}"
    dw M"Got the {COMPASS}"
    dw M"Got the {STONE_BEAK}"
    dw M"Got the {NIGHTMARE_KEY}"
    dw M"Got a {KEY}"
    dw M"Got 50 {RUPEES}"
    dw M"Got 20 {RUPEES}"
    dw M"Got 100 {RUPEES}"
    dw M"Got 200 {RUPEES}"
    dw M"Got 500 {RUPEES}!"
    dw M"Got a {SEASHELL}"
    dw M"Got ... nothing?"
    dw ItemNameZol
    dw M"Got a {KEY1}"
    dw M"Got a {KEY2}"
    dw M"Got a {KEY3}"
    dw M"Got a {KEY4}"
    dw M"Got a {KEY5}"
    dw M"Got a {KEY6}"
    dw M"Got a {KEY7}"
    dw M"Got a {KEY8}"
    dw M"Got a {KEY0}"
    dw M"Got the {MAP1}"
    dw M"Got the {MAP2}"
    dw M"Got the {MAP3}"
    dw M"Got the {MAP4}"
    dw M"Got the {MAP5}"
    dw M"Got the {MAP6}"
    dw M"Got the {MAP7}"
    dw M"Got the {MAP8}"
    dw M"Got the {MAP0}"
    dw M"Got the {COMPASS1}"
    dw M"Got the {COMPASS2}"
    dw M"Got the {COMPASS3}"
    dw M"Got the {COMPASS4}"
    dw M"Got the {COMPASS5}"
    dw M"Got the {COMPASS6}"
    dw M"Got the {COMPASS7}"
    dw M"Got the {COMPASS8}"
    dw M"Got the {COMPASS0}"
    dw M"Got the {STONE_BEAK1}"
    dw M"Got the {STONE_BEAK2}"
    dw M"Got the {STONE_BEAK3}"
    dw M"Got the {STONE_BEAK4}"
    dw M"Got the {STONE_BEAK5}"
    dw M"Got the {STONE_BEAK6}"
    dw M"Got the {STONE_BEAK7}"
    dw M"Got the {STONE_BEAK8}"
    dw M"Got the {STONE_BEAK0}"
    dw M"Got the {NIGHTMARE_KEY1}"
    dw M"Got the {NIGHTMARE_KEY2}"
    dw M"Got the {NIGHTMARE_KEY3}"
    dw M"Got the {NIGHTMARE_KEY4}"
    dw M"Got the {NIGHTMARE_KEY5}"
    dw M"Got the {NIGHTMARE_KEY6}"
    dw M"Got the {NIGHTMARE_KEY7}"
    dw M"Got the {NIGHTMARE_KEY8}"
    dw M"Got the {NIGHTMARE_KEY0}"
    dw M"Got the {TOADSTOOL}"
    dw ItemNameZol ; 0x51
    dw ItemNameZol ; 0x52
    dw ItemNameZol ; 0x53
    dw ItemNameZol ; 0x54
    dw ItemNameZol ; 0x55
    dw ItemNameZol ; 0x56
    dw M"Got the {HAMMER}!" ; 0x57
    dw M"Tail Cave opened!" ; 0x58
    dw M"Key Cavern opened!" ; 0x59
    dw M"Angler Tunnel opened!" ; 0x5a
    dw M"Face Shrine opened!" ; 0x5b
    dw M"Castle gate opened!" ; 0x5c
    dw M"Eagle tower opened!" ; 0x5d
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

ShopItemNamePointers:
    dw M"{POWER_BRACELET}"
    dw M"{SHIELD}"
    dw M"{BOW}"
    dw M"{HOOKSHOT}"
    dw M"{MAGIC_ROD}"
    dw M"{PEGASUS_BOOTS}"
    dw M"{OCARINA}"
    dw M"{FEATHER}"
    dw M"{SHOVEL}"
    dw M"{MAGIC_POWDER}"
    dw M"{BOMB}"
    dw M"{SWORD}"
    dw M"{FLIPPERS}"
    dw ItemNameNone
    dw M"{BOOMERANG}"
    dw M"{SLIME_KEY}"
    dw M"{MEDICINE}"
    dw M"{TAIL_KEY}"
    dw M"{ANGLER_KEY}"
    dw M"{FACE_KEY}"
    dw M"{BIRD_KEY}"
    dw M"{GOLD_LEAF}"
    dw M"{MAP}"
    dw M"{COMPASS}"
    dw M"{STONE_BEAK}"
    dw M"{NIGHTMARE_KEY}"
    dw M"{KEY}"
    dw M"50 {RUPEES}"
    dw M"20 {RUPEES}"
    dw M"100 {RUPEES}"
    dw M"200 {RUPEES}"
    dw M"500 {RUPEES}"
    dw M"{SEASHELL}"
    dw M"Nothing?"
    dw ItemNameZol
    dw M"{KEY1}"
    dw M"{KEY2}"
    dw M"{KEY3}"
    dw M"{KEY4}"
    dw M"{KEY5}"
    dw M"{KEY6}"
    dw M"{KEY7}"
    dw M"{KEY8}"
    dw M"{KEY0}"
    dw M"{MAP1}"
    dw M"{MAP2}"
    dw M"{MAP3}"
    dw M"{MAP4}"
    dw M"{MAP5}"
    dw M"{MAP6}"
    dw M"{MAP7}"
    dw M"{MAP8}"
    dw M"{MAP0}"
    dw M"{COMPASS1}"
    dw M"{COMPASS2}"
    dw M"{COMPASS3}"
    dw M"{COMPASS4}"
    dw M"{COMPASS5}"
    dw M"{COMPASS6}"
    dw M"{COMPASS7}"
    dw M"{COMPASS8}"
    dw M"{COMPASS0}"
    dw M"{STONE_BEAK1}"
    dw M"{STONE_BEAK2}"
    dw M"{STONE_BEAK3}"
    dw M"{STONE_BEAK4}"
    dw M"{STONE_BEAK5}"
    dw M"{STONE_BEAK6}"
    dw M"{STONE_BEAK7}"
    dw M"{STONE_BEAK8}"
    dw M"{STONE_BEAK0}"
    dw M"{NIGHTMARE_KEY1}"
    dw M"{NIGHTMARE_KEY2}"
    dw M"{NIGHTMARE_KEY3}"
    dw M"{NIGHTMARE_KEY4}"
    dw M"{NIGHTMARE_KEY5}"
    dw M"{NIGHTMARE_KEY6}"
    dw M"{NIGHTMARE_KEY7}"
    dw M"{NIGHTMARE_KEY8}"
    dw M"{NIGHTMARE_KEY0}"
    dw M"{TOADSTOOL}"
    dw ItemNameZol ; 0x51
    dw ItemNameZol ; 0x52
    dw ItemNameZol ; 0x53
    dw ItemNameZol ; 0x54
    dw ItemNameZol ; 0x55
    dw ItemNameZol ; 0x56
    dw M"{HAMMER}" ; 0x57
    dw M"Tail Cave opened!" ; 0x58
    dw M"Key Cavern opened!" ; 0x59
    dw M"Angler Tunnel opened!" ; 0x5a
    dw M"Face Shrine opened!" ; 0x5b
    dw M"Castle gate opened!" ; 0x5c
    dw M"Eagle tower opened!" ; 0x5d
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

    dw M"{HEART_PIECE}" ; 0x80
    dw M"{BOWWOW}"
    dw M"{ARROWS_10}"
    dw M"{SINGLE_ARROW}"
    dw M"{MAX_POWDER_UPGRADE}"
    dw M"{MAX_BOMBS_UPGRADE}"
    dw M"{MAX_ARROWS_UPGRADE}"
    dw M"{RED_TUNIC}"
    dw M"{BLUE_TUNIC}"
    dw M"{HEART_CONTAINER}"
    dw M"{BAD_HEART_CONTAINER}"


    dw M"{SONG1}"
    dw M"{SONG2}"
    dw M"{SONG3}"

    dw M"{INSTRUMENT1}"
    dw M"{INSTRUMENT2}"
    dw M"{INSTRUMENT3}"
    dw M"{INSTRUMENT4}"
    dw M"{INSTRUMENT5}"
    dw M"{INSTRUMENT6}"
    dw M"{INSTRUMENT7}"
    dw M"{INSTRUMENT8}"
    dw M"{ROOSTER}"

    dw M"{TRADING_ITEM_YOSHI_DOLL}"
    dw M"{TRADING_ITEM_RIBBON}"
    dw M"{TRADING_ITEM_DOG_FOOD}"
    dw M"{TRADING_ITEM_BANANAS}"
    dw M"{TRADING_ITEM_STICK}"
    dw M"{TRADING_ITEM_HONEYCOMB}"
    dw M"{TRADING_ITEM_PINEAPPLE}"
    dw M"{TRADING_ITEM_HIBISCUS}"
    dw M"{TRADING_ITEM_LETTER}"
    dw M"{TRADING_ITEM_BROOM}"
    dw M"{TRADING_ITEM_FISHING_HOOK}"
    dw M"{TRADING_ITEM_NECKLACE}"
    dw M"{TRADING_ITEM_SCALE}"
    dw M"{TRADING_ITEM_MAGNIFYING_GLASS}"

ItemNameNone:
    db m"NONE", $ff

ItemNameZol:
    db m"LOL, ZOL!", $ff
