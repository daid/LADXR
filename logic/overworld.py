from .requirements import *
from .location import Location
from locations.all import *
import worldSetup
# from worldSetup import ENTRANCE_INFO


class World:
    def __init__(self, options, world_setup, r):
        self.entrances = {}

        mabe_village = Location("Mabe Village")
        Location().add(HeartPiece(0x2A4)).connect(mabe_village, r.bush, id="0")  # well
        Location().add(FishingMinigame()).connect(mabe_village, AND(r.bush, COUNT("RUPEES", 20)), id="1")  # fishing game, heart piece is directly done by the minigame.
        Location().add(Seashell(0x0A3)).connect(mabe_village, r.bush, id="2")  # bushes below the shop
        Location().add(Seashell(0x0D2)).connect(mabe_village, PEGASUS_BOOTS, id="3")  # smash into tree next to lv1
        Location().add(Song(0x092)).connect(mabe_village, OCARINA, id="4")  # Marins song
        Location().add(KeyHole(0x0D3, TAIL_CAVE_OPENED)).connect(mabe_village, TAIL_KEY, id="5")  # Marins song
        rooster_cave = Location("Rooster Cave")
        Location().add(DroppedKey(0x1E4)).connect(rooster_cave, AND(OCARINA, SONG3), id="6")

        papahl_house = Location("Papahl House")
        mamasha_trade = Location().add(TradeSequenceItem(0x2A6, TRADING_ITEM_RIBBON))
        papahl_house.connect(mamasha_trade, TRADING_ITEM_YOSHI_DOLL, id="7")

        trendy_shop = Location("Trendy Shop")
        trendy_shop.connect(Location().add(TradeSequenceItem(0x2A0, TRADING_ITEM_YOSHI_DOLL)), FOUND("RUPEES", 50), id="8")
        outside_trendy = Location()
        outside_trendy.connect(mabe_village, r.bush, id="9")

        self._addEntrance("papahl_house_left", mabe_village, papahl_house, None)
        self._addEntrance("papahl_house_right", mabe_village, papahl_house, None)
        self._addEntrance("rooster_grave", mabe_village, rooster_cave, COUNT(POWER_BRACELET, 2))
        self._addEntranceRequirementExit("rooster_grave", None, id="a") # if exiting, you do not need l2 bracelet
        self._addEntrance("madambowwow", mabe_village, Location(), None)
        self._addEntrance("ulrira", mabe_village, Location(), None)
        self._addEntrance("mabe_phone", mabe_village, self._createShopSanity(options, 1, 0x2CB, id="b"), None)
        self._addEntrance("library", mabe_village, Location("Library"), None)
        self._addEntrance("trendy_shop", mabe_village, trendy_shop, r.bush)
        self._addEntrance("d1", mabe_village, None, TAIL_CAVE_OPENED)
        self._addEntranceRequirementExit("d1", None, id="c") # if exiting, you do not need the key

        start_house = Location("Start House").add(StartItem())
        self._addEntrance("start_house", mabe_village, start_house, None)

        shop = Location("Shop")
        if options.shopsanity == '':
            Location().add(ShopItem(0)).connect(shop, COUNT("RUPEES", 200), id="d")
            Location().add(ShopItem(1)).connect(shop, COUNT("RUPEES", 980), id="e")
        else:
            Location().add(ShopItem(0)).connect(shop, FOUND("RUPEES", 100), id="f")
            Location().add(ShopItem(1)).connect(shop, FOUND("RUPEES", 200), id="g")
        self._addEntrance("shop", mabe_village, shop, None)

        dream_hut = Location("Dream Hut")
        dream_hut_right = Location().add(Chest(0x2BF)).connect(dream_hut, SWORD, id="h")
        if options.logic != "casual":
            dream_hut_right.connect(dream_hut, OR(BOOMERANG, HOOKSHOT, FEATHER), id="i")
        dream_hut_left = Location().add(Chest(0x2BE)).connect(dream_hut_right, PEGASUS_BOOTS, id="j")
        outside_dream_hut = Location()
        outside_dream_hut.connect(mabe_village, POWER_BRACELET, id="k")
        self._addEntrance("dream_hut", outside_dream_hut, dream_hut, None)

        kennel = Location("Kennel").connect(Location().add(Seashell(0x2B2)), SHOVEL, id="l")  # in the kennel
        kennel.connect(Location().add(TradeSequenceItem(0x2B2, TRADING_ITEM_DOG_FOOD)), TRADING_ITEM_RIBBON, id="m")
        self._addEntrance("kennel", mabe_village, kennel, None)

        sword_beach = Location("Sword Beach").add(BeachSword()).connect(mabe_village, OR(r.bush, SHIELD, r.attack_hookshot), id="n")
        banana_seller = Location("Banana Seller")
        banana_seller.connect(Location().add(TradeSequenceItem(0x2FE, TRADING_ITEM_BANANAS)), TRADING_ITEM_DOG_FOOD, id="o")
        outside_banana_seller = Location()
        outside_banana_seller.connect(sword_beach, r.bush, id="p")
        self._addEntrance("banana_seller", outside_banana_seller, banana_seller, None)
        boomerang_cave = Location("Boomerang Cave")
        if options.boomerang == 'trade':
            Location().add(BoomerangGuy()).connect(boomerang_cave, AND(r.shuffled_magnifier, OR(BOOMERANG, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS, FEATHER, SHOVEL)), id="q")
        elif options.boomerang == 'gift':
            Location().add(BoomerangGuy()).connect(boomerang_cave, r.shuffled_magnifier, id="r")
        self._addEntrance("boomerang_cave", sword_beach, boomerang_cave, BOMB)
        self._addEntranceRequirementExit("boomerang_cave", None, id="s") # if exiting, you do not need bombs

        sword_beach_to_ghost_hut = Location("Sword Beach to Ghost House").add(Chest(0x0E5)).connect(sword_beach, POWER_BRACELET, id="t")
        ghost_hut_outside = Location("Outside Ghost House").connect(sword_beach_to_ghost_hut, POWER_BRACELET, id="u")
        ghost_hut_inside = Location("Ghost House").connect(Location().add(Seashell(0x1E3)), POWER_BRACELET, id="v")
        self._addEntrance("ghost_house", ghost_hut_outside, ghost_hut_inside, None)

        ## Forest area
        forest = Location("Forest").connect(mabe_village, r.bush, id="w") # forest stretches all the way from the start town to the witch hut
        Location().add(Chest(0x071)).connect(forest, POWER_BRACELET, id="x")  # chest at start forest with 2 zols
        forest_heartpiece = Location("Forest Heart Piece").add(HeartPiece(0x044))  # next to the forest, surrounded by pits
        forest.connect(forest_heartpiece, OR(BOOMERANG, FEATHER, HOOKSHOT, ROOSTER), id="y", one_way=True)

        witch_hut = Location("Witch's Hut").connect(Location().add(Witch()), TOADSTOOL, id="z")
        self._addEntrance("witch", forest, witch_hut, None)
        crazy_tracy_hut = Location("Outside Crazy Tracy's House").connect(forest, POWER_BRACELET, id="00")
        crazy_tracy_hut_inside = Location("Crazy Tracy's House")
        Location().add(KeyLocation("MEDICINE2")).connect(crazy_tracy_hut_inside, FOUND("RUPEES", 50), id="01")
        self._addEntrance("crazy_tracy", crazy_tracy_hut, crazy_tracy_hut_inside, None)
        start_house.connect(crazy_tracy_hut, AND(OCARINA, SONG2), id="02", one_way=True) # Manbo's Mambo into the pond outside Tracy

        forest_madbatter = Location("Forest Mad Batter")
        Location().add(MadBatter(0x1E1)).connect(forest_madbatter, MAGIC_POWDER, id="03")
        self._addEntrance("forest_madbatter", forest, forest_madbatter, POWER_BRACELET)
        self._addEntranceRequirementExit("forest_madbatter", None, id="04") # if exiting, you do not need bracelet

        forest_cave = Location("Forest Cave")
        forest_cave_crystal_chest = Location().add(Chest(0x2BD)).connect(forest_cave, SWORD, id="05")  # chest in forest cave on route to mushroom
        log_cave_heartpiece = Location().add(HeartPiece(0x2AB)).connect(forest_cave, POWER_BRACELET, id="06")  # piece of heart in the forest cave on route to the mushroom
        forest_toadstool = Location().add(Toadstool())
        self._addEntrance("toadstool_entrance", forest, forest_cave, None)
        self._addEntrance("toadstool_exit", forest_toadstool, forest_cave, None)

        hookshot_cave = Location("Hookshot Cave")
        hookshot_cave_chest = Location().add(Chest(0x2B3)).connect(hookshot_cave, OR(HOOKSHOT, ROOSTER), id="07")
        self._addEntrance("hookshot_cave", forest, hookshot_cave, POWER_BRACELET)

        swamp = Location("Swamp").connect(forest, AND(OR(MAGIC_POWDER, FEATHER, ROOSTER), r.bush), id="08")
        swamp.connect(forest, r.bush, id="09", one_way=True) # can go backwards past Tarin
        swamp.connect(forest_toadstool, OR(FEATHER, ROOSTER), id="0a")
        swamp_chest = Location("Swamp Chest").add(Chest(0x034)).connect(swamp, OR(BOWWOW, HOOKSHOT, MAGIC_ROD, BOOMERANG), id="0b")
        outside_d2 = Location()
        swamp.connect(outside_d2, OR(BOWWOW, HOOKSHOT, MAGIC_ROD, BOOMERANG), id="0c")
        self._addEntrance("d2", outside_d2, None, None)
        forest_rear_chest = Location().add(Chest(0x041)).connect(swamp, r.bush, id="0d")  # tail key
        self._addEntrance("writes_phone", swamp, self._createShopSanity(options, 2, 0x29B, id="0e"), None)

        writes_hut_outside = Location("Outside Write's House").connect(swamp, OR(FEATHER, ROOSTER), id="0f")  # includes the cave behind the hut
        writes_house = Location("Write's House")
        writes_house.connect(Location().add(TradeSequenceItem(0x2a8, TRADING_ITEM_BROOM)), TRADING_ITEM_LETTER, id="0g")
        self._addEntrance("writes_house", writes_hut_outside, writes_house, None)
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            writes_hut_outside.add(OwlStatue(0x11))
        writes_cave = Location("Write's Cave")
        writes_cave_left_chest = Location().add(Chest(0x2AE)).connect(writes_cave, OR(FEATHER, ROOSTER, HOOKSHOT), id="0h") # 1st chest in the cave behind the hut
        Location().add(Chest(0x2AF)).connect(writes_cave, POWER_BRACELET, id="0i")  # 2nd chest in the cave behind the hut.
        self._addEntrance("writes_cave_left", writes_hut_outside, writes_cave, None)
        self._addEntrance("writes_cave_right", writes_hut_outside, writes_cave, None)

        graveyard = Location("Graveyard").connect(forest, OR(FEATHER, ROOSTER, POWER_BRACELET), id="0j")  # whole area from the graveyard up to the moblin cave
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            graveyard.add(OwlStatue(0x035))  # Moblin cave owl
        self._addEntrance("photo_house", graveyard, Location(), None)
        self._addEntrance("d0", graveyard, None, POWER_BRACELET)
        self._addEntranceRequirementExit("d0", None, id="0k") # if exiting, you do not need bracelet
        ghost_grave = Location("Ghost Grave").connect(forest, POWER_BRACELET, id="0l")
        Location().add(Seashell(0x074)).connect(ghost_grave, AND(r.bush, SHOVEL), id="0m")  # next to grave cave, digging spot
        graveyard.connect(forest_heartpiece, OR(BOOMERANG, HOOKSHOT), id="0n", one_way=True) # grab the heart piece surrounded by pits from the north

        graveyard_cave_left = Location("Graveyard Cave West")
        graveyard_cave_right = Location("Graveyard Cave East").connect(graveyard_cave_left, OR(FEATHER, ROOSTER), id="0o")
        graveyard_heartpiece = Location().add(HeartPiece(0x2DF)).connect(graveyard_cave_right, OR(AND(BOMB, OR(HOOKSHOT, PEGASUS_BOOTS), FEATHER), ROOSTER), id="0p")  # grave cave
        outside_graveyard_left = Location()
        ghost_grave.connect(outside_graveyard_left, POWER_BRACELET, id="0q")
        self._addEntrance("graveyard_cave_left", outside_graveyard_left, graveyard_cave_left, None)
        self._addEntrance("graveyard_cave_right", graveyard, graveyard_cave_right, None)
        moblin_cave = Location("Moblin Cave").connect(Location().add(Chest(0x2E2)), AND(r.attack_hookshot_powder, r.miniboss_requirements[world_setup.miniboss_mapping["moblin_cave"]]), id="0r")
        self._addEntrance("moblin_cave", graveyard, moblin_cave, None)

        # "Ukuku Prairie"
        ukuku_prairie = Location("Ukuku Prairie").connect(mabe_village, POWER_BRACELET, id="0s").connect(graveyard, POWER_BRACELET, id="0t")
        ukuku_prairie.connect(Location().add(TradeSequenceItem(0x07B, TRADING_ITEM_STICK)), TRADING_ITEM_BANANAS, id="0u")
        ukuku_prairie.connect(Location().add(TradeSequenceItem(0x087, TRADING_ITEM_HONEYCOMB)), TRADING_ITEM_STICK, id="0v")
        ukuku_prairie.connect(Location().add(KeyHole(0x0B5, KEY_CAVERN_OPENED)), SLIME_KEY, id="0w")
        self._addEntrance("prairie_left_phone", ukuku_prairie, self._createShopSanity(options, 3, 0x2B4, id="0x"), None)
        self._addEntrance("prairie_right_phone", ukuku_prairie, self._createShopSanity(options, 4, 0x29C, id="0y"), None)
        self._addEntrance("prairie_left_cave1", ukuku_prairie, Location().add(Chest(0x2CD)), None) # cave next to town
        self._addEntrance("prairie_left_fairy", ukuku_prairie, Location(), BOMB)
        self._addEntranceRequirementExit("prairie_left_fairy", None, id="0z") # if exiting, you do not need bombs

        prairie_left_cave2 = Location("Boots 'n' Bomb Cave")  # Bomb cave
        Location().add(Chest(0x2F4)).connect(prairie_left_cave2, PEGASUS_BOOTS, id="10")
        Location().add(HeartPiece(0x2E5)).connect(prairie_left_cave2, AND(BOMB, PEGASUS_BOOTS), id="11")
        self._addEntrance("prairie_left_cave2", ukuku_prairie, prairie_left_cave2, BOMB)
        self._addEntranceRequirementExit("prairie_left_cave2", None, id="12") # if exiting, you do not need bombs

        mamu = Location("Mamu").connect(Location().add(Song(0x2FB)), AND(OCARINA, COUNT("RUPEES", 300)), id="13")
        self._addEntrance("mamu", ukuku_prairie, mamu, AND(OR(AND(FEATHER, PEGASUS_BOOTS), ROOSTER), OR(HOOKSHOT, ROOSTER), POWER_BRACELET))

        dungeon3_entrance = Location("Outside D3").connect(ukuku_prairie, OR(FEATHER, ROOSTER, FLIPPERS), id="14")
        self._addEntrance("d3", dungeon3_entrance, None, KEY_CAVERN_OPENED)
        self._addEntranceRequirementExit("d3", None, id="15") # if exiting, you do not need to open the door
        Location().add(Seashell(0x0A5)).connect(dungeon3_entrance, SHOVEL, id="16")  # above lv3
        dungeon3_entrance.connect(ukuku_prairie, None, id="17", one_way=True) # jump down ledge back to ukuku_prairie

        prairie_island_seashell = Location().add(Seashell(0x0A6)).connect(ukuku_prairie, AND(FLIPPERS, r.bush), id="18")  # next to lv3
        seashell_mansion_bush = Location().add(Seashell(0x08B)).connect(ukuku_prairie, r.bush, id="19")
        Location().add(Seashell(0x0A4)).connect(ukuku_prairie, PEGASUS_BOOTS, id="1a")  # smash into tree next to phonehouse
        self._addEntrance("castle_jump_cave", ukuku_prairie, Location().add(Chest(0x1FD)), ROOSTER)
        if not options.rooster:
            self._addEntranceRequirement("castle_jump_cave", AND(FEATHER, PEGASUS_BOOTS), id="1b") # left of the castle, 5 holes turned into 3
        Location().add(Seashell(0x0B9)).connect(ukuku_prairie, POWER_BRACELET, id="1c")  # under the rock

        left_bay_area = Location("Western Bay")
        left_bay_area.connect(ghost_hut_outside, OR(AND(FEATHER, PEGASUS_BOOTS), ROOSTER), id="1d")
        self._addEntrance("prairie_low_phone", left_bay_area, self._createShopSanity(options, 5, 0x29D, id="1e"), None)

        Location().add(Seashell(0x0E9)).connect(left_bay_area, r.bush, id="1f")  # same screen as mermaid statue
        tiny_island = Location().add(Seashell(0x0F8)).connect(left_bay_area, AND(OR(FLIPPERS, ROOSTER), r.bush), id="1g")  # tiny island

        prairie_plateau = Location("Bay Plateau")  # prairie plateau at the owl statue
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            prairie_plateau.add(OwlStatue(0x0A8))
        Location().add(Seashell(0x0A8)).connect(prairie_plateau, SHOVEL, id="1h")  # at the owl statue

        prairie_cave = Location("Bay Cliff Cave")
        prairie_cave_secret_exit = Location("Bay Cliff to Plateau").connect(prairie_cave, OR(FEATHER, ROOSTER), id="1i", one_way=True)
        prairie_cave.connect(prairie_cave_secret_exit, AND(BOMB, OR(FEATHER, ROOSTER)), id="1j", one_way=True) # bomb walls are one-way        
        self._addEntrance("prairie_right_cave_top", ukuku_prairie, prairie_cave, None)
        self._addEntrance("prairie_right_cave_bottom", left_bay_area, prairie_cave, None)
        self._addEntrance("prairie_right_cave_high", prairie_plateau, prairie_cave_secret_exit, None)

        bay_madbatter_connector_entrance = Location("Bay Batter Tunnel Entrance")
        bay_madbatter_connector_exit = Location("Bay Batter Tunnel Exit").connect(bay_madbatter_connector_entrance, FLIPPERS, id="1k")
        bay_madbatter_connector_outside = Location("Outside Bay Batter")
        bay_madbatter = Location("Bay Batter").connect(Location().add(MadBatter(0x1E0)), MAGIC_POWDER, id="1l")
        outside_bay_madbatter_entrance = Location()
        left_bay_area.connect(outside_bay_madbatter_entrance, AND(OR(FEATHER, ROOSTER), OR(SWORD, MAGIC_ROD, BOOMERANG)), id="1m")
        outside_bay_madbatter_entrance.connect(left_bay_area, AND(OR(FEATHER, ROOSTER), r.bush), id="1n", one_way=True) # if exiting, you can pick up the bushes by normal means
        self._addEntrance("prairie_madbatter_connector_entrance", outside_bay_madbatter_entrance, bay_madbatter_connector_entrance, None)
        self._addEntrance("prairie_madbatter_connector_exit", bay_madbatter_connector_outside, bay_madbatter_connector_exit, None)
        self._addEntrance("prairie_madbatter", bay_madbatter_connector_outside, bay_madbatter, None)

        seashell_mansion = Location("Seashell Mansion")
        if options.goal != "seashells":
            Location().add(SeashellMansionBonus(0)).connect(seashell_mansion, COUNT(SEASHELL, 5), id="1o")
            Location().add(SeashellMansionBonus(1)).connect(seashell_mansion, COUNT(SEASHELL, 10), id="1p")
            Location().add(SeashellMansion(0x2E9)).connect(seashell_mansion, COUNT(SEASHELL, 20), id="1q")
        else:
            seashell_mansion.add(DroppedKey(0x2E9))
        self._addEntrance("seashell_mansion", ukuku_prairie, seashell_mansion, None)

        bay_water = Location("Bay Water")
        bay_water.connect(ukuku_prairie, FLIPPERS, id="1r")
        bay_water.connect(left_bay_area, FLIPPERS, id="1s")
        fisher_under_bridge = Location().add(TradeSequenceItem(0x2F5, TRADING_ITEM_NECKLACE))
        fisher_under_bridge.connect(bay_water, AND(TRADING_ITEM_FISHING_HOOK, FEATHER, FLIPPERS), id="1t")
        bay_water.connect(Location().add(TradeSequenceItem(0x0C9, TRADING_ITEM_SCALE)), AND(TRADING_ITEM_NECKLACE, FLIPPERS), id="1u")
        d5_entrance = Location("Outside D5").connect(bay_water, FLIPPERS, id="1v")
        self._addEntrance("d5", d5_entrance, None, None)

        # Richard
        richard_house = Location("Richard's Villa")
        richard_cave = Location("Richard's Cave").connect(richard_house, COUNT(GOLD_LEAF, 5), id="1w")
        richard_cave.connect(richard_house, None, id="1x", one_way=True) # can exit richard's cave even without leaves
        richard_cave_chest = Location().add(Chest(0x2C8)).connect(richard_cave, OR(FEATHER, HOOKSHOT, ROOSTER), id="1y")
        richard_maze = Location("Pothole Maze")
        self._addEntrance("richard_house", ukuku_prairie, richard_house, None)
        self._addEntrance("richard_maze", richard_maze, richard_cave, None)
        slime_key_area = Location("Near Slime Key").connect(richard_maze, OR(SWORD, AND(MAGIC_POWDER, MAX_POWDER_UPGRADE), MAGIC_ROD, POWER_BRACELET, BOOMERANG), id="1z")
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            Location().add(OwlStatue(0x0C6)).connect(slime_key_area, None, id="20")
        Location().add(SlimeKey()).connect(slime_key_area, SHOVEL, id="21")

        next_to_castle = Location("Next to Kanalet")
        if options.tradequest:
            ukuku_prairie.connect(next_to_castle, TRADING_ITEM_BANANAS, id="22", one_way=True) # can only give bananas from ukuku prairie side
        else:
            next_to_castle.connect(ukuku_prairie, None, id="23")
        next_to_castle.connect(ukuku_prairie, FLIPPERS, id="24")
        self._addEntrance("castle_phone", next_to_castle, self._createShopSanity(options, 6, 0x2CC, id="25"), None)
        castle_secret_entrance_left = Location("Kanalet Tunnel West")
        castle_secret_entrance_right = Location("Kanalet Tunnel East").connect(castle_secret_entrance_left, FEATHER, id="26")
        castle_courtyard = Location("Kanalet Courtyard")
        castle_frontdoor = Location("Kanalet Front Door").connect(castle_courtyard, r.bush, id="27")
        castle_frontdoor.connect(ukuku_prairie, CASTLE_GATE_OPENED, id="28") # the button in the castle connector allows access to the castle grounds in ER
        self._addEntrance("castle_secret_entrance", next_to_castle, castle_secret_entrance_right, r.pit_bush)
        self._addEntranceRequirementExit("castle_secret_entrance", None, id="29") # leaving doesn't require pit_bush
        self._addEntrance("castle_secret_exit", castle_courtyard, castle_secret_entrance_left, None)

        Location().add(HeartPiece(0x078)).connect(bay_water, FLIPPERS, id="2a")  # in the moat of the castle
        castle_inside = Location("Inside Kanalet")
        Location().add(KeyHole(0x2C3, CASTLE_GATE_OPENED)).connect(castle_inside, None, id="2b")
        castle_top_outside = Location("Outside Top of Kanalet")
        castle_top_inside = Location("Inside Top of Kanalet")
        self._addEntrance("castle_main_entrance", castle_frontdoor, castle_inside, None)
        self._addEntrance("castle_upper_left", castle_top_outside, castle_inside, None)
        self._addEntrance("castle_upper_right", castle_top_outside, castle_top_inside, None)
        Location().add(GoldLeaf(0x05A)).connect(castle_courtyard, OR(SWORD, BOW, MAGIC_ROD), id="2c")  # mad bomber, enemy hiding in the 6 holes
        crow_gold_leaf = Location().add(GoldLeaf(0x058)).connect(castle_courtyard, AND(POWER_BRACELET, r.attack_hookshot_no_bomb), id="2d")  # bird on tree, can't kill with bomb cause it flies off. immune to magic_powder
        Location().add(GoldLeaf(0x2D2)).connect(castle_inside, r.attack_hookshot_powder, id="2e")  # in the castle, kill enemies
        Location().add(GoldLeaf(0x2C5)).connect(castle_inside, AND(BOMB, r.attack_hookshot_powder), id="2f")  # in the castle, bomb wall to show enemy
        kanalet_chain_trooper = Location().add(GoldLeaf(0x2C6))  # in the castle, spinning spikeball enemy
        castle_top_inside.connect(kanalet_chain_trooper, AND(POWER_BRACELET, r.attack_hookshot), id="2g", one_way=True)

        animal_village = Location("Animal Village")
        animal_village.connect(Location().add(TradeSequenceItem(0x0CD, TRADING_ITEM_FISHING_HOOK)), TRADING_ITEM_BROOM, id="2h")
        cookhouse = Location("Bear Chef's House")
        cookhouse.connect(Location().add(TradeSequenceItem(0x2D7, TRADING_ITEM_PINEAPPLE)), TRADING_ITEM_HONEYCOMB, id="2i")
        goathouse = Location("Goat's House")
        goathouse.connect(Location().add(TradeSequenceItem(0x2D9, TRADING_ITEM_LETTER)), TRADING_ITEM_HIBISCUS, id="2j")
        mermaid_statue = Location("Inside Mermaid Statue")
        mermaid_statue.connect(animal_village, AND(TRADING_ITEM_SCALE, HOOKSHOT), id="2k")
        mermaid_statue.add(TradeSequenceItem(0x297, TRADING_ITEM_MAGNIFYING_GLASS))
        self._addEntrance("animal_phone", animal_village, self._createShopSanity(options, 7, 0x2E3, id="2l"), None)
        self._addEntrance("animal_house1", animal_village, Location(), None)
        self._addEntrance("animal_house2", animal_village, Location(), None)
        self._addEntrance("animal_house3", animal_village, goathouse, None)
        self._addEntrance("animal_house4", animal_village, Location(), None)
        self._addEntrance("animal_house5", animal_village, cookhouse, None)
        animal_village.connect(bay_water, FLIPPERS, id="2m")
        animal_village.connect(ukuku_prairie, OR(HOOKSHOT, ROOSTER), id="2n")
        animal_village_connector_left = Location("Under the River West")
        animal_village_connector_right = Location("Under the River East").connect(animal_village_connector_left, PEGASUS_BOOTS, id="2o")
        self._addEntrance("prairie_to_animal_connector", ukuku_prairie, animal_village_connector_left, r.pit_bush) # passage under river blocked by bush
        self._addEntranceRequirementExit("prairie_to_animal_connector", None, id="2p") # leaving doesn't require pit_bush
        self._addEntrance("animal_to_prairie_connector", animal_village, animal_village_connector_right, None)
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            animal_village.add(OwlStatue(0x0DA))
        Location().add(Seashell(0x0DA)).connect(animal_village, SHOVEL, id="2q")  # owl statue at the water
        desert = Location("Desert").connect(animal_village, r.bush, id="2r")  # Note: We moved the walrus blocking the desert.
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            desert.add(OwlStatue(0x0CF))
        desert_lanmola = Location().add(AnglerKey()).connect(desert, r.attack_hookshot_no_bomb, id="2s")

        animal_village_bombcave = Location("Bomb Arrow Cave")
        self._addEntrance("animal_cave", desert, animal_village_bombcave, BOMB)
        self._addEntranceRequirementExit("animal_cave", None, id="2t") # if exiting, you do not need bombs
        animal_village_bombcave_heartpiece = Location().add(HeartPiece(0x2E6)).connect(animal_village_bombcave, OR(AND(BOMB, FEATHER, HOOKSHOT), ROOSTER), id="2u")  # cave in the upper right of animal town

        desert_cave = Location("Desert Cave")
        self._addEntrance("desert_cave", desert, desert_cave, None)
        desert.connect(desert_cave, None, id="2v", one_way=True) # Drop down the sinkhole

        Location().add(HeartPiece(0x1E8)).connect(desert_cave, BOMB, id="2w")  # above the quicksand cave
        Location().add(Seashell(0x0FF)).connect(desert, POWER_BRACELET, id="2x") # bottom right corner of the map

        armos_maze = Location("Armos Maze").connect(animal_village, POWER_BRACELET, id="2y")
        armos_temple = Location("Southern Shrine")
        Location().add(FaceKey()).connect(armos_temple, r.miniboss_requirements[world_setup.miniboss_mapping["armos_temple"]], id="2z")
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            armos_maze.add(OwlStatue(0x08F))
        outside_armos_cave = Location("Outside Armos Maze Cave").connect(armos_maze, OR(r.attack_hookshot, SHIELD), id="30")
        outside_armos_temple = Location("Outside Southern Shrine").connect(armos_maze, OR(r.attack_hookshot, SHIELD), id="31")
        self._addEntrance("armos_maze_cave", outside_armos_cave, Location().add(Chest(0x2FC)), None)
        self._addEntrance("armos_temple", outside_armos_temple, armos_temple, None)

        armos_fairy_entrance = Location("Outside D6 Fairy").connect(bay_water, FLIPPERS, id="32").connect(animal_village, POWER_BRACELET, id="33")
        self._addEntrance("armos_fairy", armos_fairy_entrance, Location(), BOMB)
        self._addEntranceRequirementExit("armos_fairy", None, id="34") # if exiting, you do not need bombs

        d6_connector_left = Location("To D6 West")
        d6_connector_right = Location("To D6 East").connect(d6_connector_left, OR(AND(HOOKSHOT, OR(FLIPPERS, AND(FEATHER, PEGASUS_BOOTS))), ROOSTER), id="35")
        d6_entrance = Location("Outside D6")
        d6_entrance.connect(bay_water, FLIPPERS, id="36", one_way=True)
        d6_entrance.connect(Location().add(KeyHole(0x08C, FACE_SHRINE_OPENED)), FACE_KEY, id="37")
        d6_armos_island = Location("Armos Island").connect(bay_water, FLIPPERS, id="38")
        self._addEntrance("d6_connector_entrance", d6_armos_island, d6_connector_right, None)
        self._addEntrance("d6_connector_exit", d6_entrance, d6_connector_left, None)
        self._addEntrance("d6", d6_entrance, None, FACE_SHRINE_OPENED)
        self._addEntranceRequirementExit("d6", None, id="39") # if exiting, you do not need to open the dungeon

        windfish_egg = Location("Outside the Egg").connect(swamp, POWER_BRACELET, id="3a").connect(graveyard, POWER_BRACELET, id="3b")
        windfish_egg.connect(graveyard, None, id="3c", one_way=True) # Ledge jump

        obstacle_cave_entrance = Location("Mountain Access Entrance")
        obstacle_cave_inside = Location("Mountain Access Inside").connect(obstacle_cave_entrance, SWORD, id="3d")
        obstacle_cave_inside.connect(obstacle_cave_entrance, FEATHER, id="3e", one_way=True) # can get past the rock room from right to left pushing blocks and jumping over the pit
        obstacle_cave_inside_chest = Location().add(Chest(0x2BB)).connect(obstacle_cave_inside, OR(HOOKSHOT, ROOSTER), id="3f")  # chest at obstacles
        obstacle_cave_exit = Location("Mountain Access Exit").connect(obstacle_cave_inside, OR(PEGASUS_BOOTS, ROOSTER), id="3g")

        outside_obstacle_cave = Location()
        windfish_egg.connect(outside_obstacle_cave, POWER_BRACELET, id="3h")

        lower_right_taltal = Location("Lower Tal Tal")
        self._addEntrance("obstacle_cave_entrance", outside_obstacle_cave, obstacle_cave_entrance, None)
        self._addEntrance("obstacle_cave_outside_chest", Location().add(Chest(0x018)), obstacle_cave_inside, None)
        self._addEntrance("obstacle_cave_exit", lower_right_taltal, obstacle_cave_exit, None)

        papahl_cave = Location().add(Chest(0x28A))
        papahl = Location("Papahl's Ledge").connect(lower_right_taltal, None, id="3i", one_way=True)
        hibiscus_item = Location().add(TradeSequenceItem(0x019, TRADING_ITEM_HIBISCUS))
        papahl.connect(hibiscus_item, TRADING_ITEM_PINEAPPLE, id="3j", one_way=True)
        self._addEntrance("papahl_entrance", lower_right_taltal, papahl_cave, None)
        self._addEntrance("papahl_exit", papahl, papahl_cave, None)

        # D4 entrance and related things
        below_right_taltal = Location('Near D4 Keyhole').connect(windfish_egg, POWER_BRACELET, id="3k")
        angler_tunnel_keyhole = Location('D4 Keyhole').connect(Location().add(KeyHole(0x02B, ANGLER_TUNNEL_OPENED)), ANGLER_KEY, id="3l")
        
        d4_entrance_locked = Location("Outside D4 Closed").connect(below_right_taltal, FLIPPERS, id="3m")
        d4_entrance_unlocked = Location("Outside D4 Open").connect(d4_entrance_locked, ANGLER_TUNNEL_OPENED, id="3n")
        
        below_right_taltal.connect(angler_tunnel_keyhole, None, id="3o", one_way=True)
        below_right_taltal.connect(bay_water, FLIPPERS, id="3p")
        below_right_taltal.connect(next_to_castle, ROOSTER, id="3q") # fly from staircase to staircase on the north side of the moat
        lower_right_taltal.connect(d4_entrance_locked, FLIPPERS, id="3r", one_way=True) # fall down waterfall
        lower_right_taltal.connect(d4_entrance_unlocked, ANGLER_TUNNEL_OPENED, id="3s", one_way=True) # fall down waterfall

        heartpiece_swim_cave = Location("Damp Cave").connect(Location().add(HeartPiece(0x1F2)), FLIPPERS, id="3t")
        outside_swim_cave = Location()
        below_right_taltal.connect(outside_swim_cave, FLIPPERS, id="3u")
        self._addEntrance("heartpiece_swim_cave", outside_swim_cave, heartpiece_swim_cave, None)  # cave next to level 4
        self._addEntrance("d4", d4_entrance_locked, None, ANGLER_TUNNEL_OPENED)
        self._addEntranceRequirementExit("d4", FLIPPERS, id="3v") # if exiting, you can leave with flippers without opening the dungeon
        #self._addEntrance("d4_connector", below_right_taltal, d4_connector_right, None) # TODO d4_connector
        #self._addEntrance("d4_connector_exit", d4_entrance_unlocked, d4_connector_left, None) # TODO d4_connector
        d4_entrance_unlocked.connect(below_right_taltal, None, id="3w", one_way=True) # one way underwater passage only accessible when d4 is opened, modified to remove pit # TODO d4_connector
        outside_mambo = Location("Outside Manbo").connect(d4_entrance_locked, FLIPPERS, id="3x")
        inside_mambo = Location("Manbo's Cave")
        mambo = Location().add(Song(0x2FD)).connect(inside_mambo, AND(OCARINA, FLIPPERS), id="3y")  # Manbo's Mambo
        self._addEntrance("mambo", outside_mambo, inside_mambo, None)

        # Raft game.
        raft_house = Location("Raft House")
        Location().add(KeyLocation("RAFT")).connect(raft_house, COUNT("RUPEES", 100), id="3z")
        raft_return_upper = Location("Raft Return North")
        raft_return_lower = Location("Raft Return South").connect(raft_return_upper, None, id="40", one_way=True)
        outside_raft_house = Location("Outside Raft House").connect(below_right_taltal, HOOKSHOT, id="41").connect(below_right_taltal, FLIPPERS, id="42", one_way=True)
        raft_game = Location()
        raft_game.connect(outside_raft_house, "RAFT", id="43")
        raft_game.add(Chest(0x05C), Chest(0x05D)) # Chests in the rafting game
        raft_exit = Location("Raft Exit")
        if options.logic != "casual":  # use raft to reach north armos maze entrances without flippers
            raft_game.connect(raft_exit, None, id="44", one_way=True)
            raft_game.connect(armos_fairy_entrance, None, id="45", one_way=True)
        self._addEntrance("raft_return_exit", outside_raft_house, raft_return_upper, None)
        self._addEntrance("raft_return_enter", raft_exit, raft_return_lower, None)
        raft_exit.connect(armos_fairy_entrance, FLIPPERS, id="46")
        self._addEntrance("raft_house", outside_raft_house, raft_house, None)
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            raft_game.add(OwlStatue(0x5D))
        
        middle_right_taltal = Location("Between Waterfall and Mountain Stairs").connect(lower_right_taltal, OR(FLIPPERS, ROOSTER, ANGLER_TUNNEL_OPENED), id="47")
        outside_rooster_house = Location("Outside Rooster House").connect(middle_right_taltal, OR(FLIPPERS, ROOSTER), id="48")
        self._addEntrance("rooster_house", outside_rooster_house, Location(), None)
        bird_cave = Location("Bird Cave")
        bird_key = Location().add(BirdKey())
        bird_cave.connect(bird_key, ROOSTER, id="49")
        if not options.rooster:
            bird_cave.connect(bird_key, AND(FEATHER, COUNT(POWER_BRACELET, 2)), id="4a") # elephant statue added
        if options.logic != "casual":
            bird_cave.connect(lower_right_taltal, None, id="4b", one_way=True)  # Drop in a hole at bird cave
        self._addEntrance("bird_cave", outside_rooster_house, bird_cave, None)
        bridge_seashell = Location().add(Seashell(0x00C)).connect(outside_rooster_house, AND(OR(FEATHER, ROOSTER), POWER_BRACELET), id="4c")  # seashell right of rooster house, there is a hole in the bridge

        multichest_cave = Location("5 Chest Game Tunnel")
        multichest_cave_secret = Location("To 5 Chest Game").connect(multichest_cave, None, id="4d", one_way=True) # bomb walls are one-way
        multichest_cave.connect(multichest_cave_secret, BOMB, id="4e", one_way=True)
        water_cave_hole = Location("Near Hole to Damp Cave")  # Location with the hole that drops you onto the heart piece under water
        if options.logic != "casual":
            water_cave_hole.connect(heartpiece_swim_cave, FLIPPERS, id="4f", one_way=True)
        multichest_outside = Location().add(Chest(0x01D))  # chest after multichest puzzle outside
        outside_multichest_left = Location()
        lower_right_taltal.connect(outside_multichest_left, OR(FLIPPERS, ROOSTER), id="4g")
        self._addEntrance("multichest_left", outside_multichest_left, multichest_cave, None)
        self._addEntrance("multichest_right", water_cave_hole, multichest_cave, None)
        self._addEntrance("multichest_top", multichest_outside, multichest_cave_secret, None)
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            water_cave_hole.add(OwlStatue(0x1E)) # owl statue below d7

        right_taltal_connector1 = Location("Outer Rainbow Cave")
        right_taltal_connector_outside1 = Location("Rainbow Ledge")
        right_taltal_connector2 = Location("Inner Rainbow Cave Entrance")
        right_taltal_connector3 = Location("Inner Rainbow Cave Exit")
        right_taltal_connector2.connect(right_taltal_connector3, AND(OR(FEATHER, ROOSTER), HOOKSHOT), id="4h", one_way=True)
        right_taltal_connector_outside2 = Location("After Rainbow Caves")
        right_taltal_connector4 = Location("Path to D7")
        d7_platau = Location("D7 Plateau")
        d7_tower = Location("D7 Tower")
        d7_platau.connect(Location().add(KeyHole(0x00E, EAGLE_TOWER_OPENED)), AND(POWER_BRACELET, BIRD_KEY), id="4i")
        d7_platau.connect(d7_tower, EAGLE_TOWER_OPENED, id="4j", one_way=True)
        d7_tower.connect(d7_platau, None, id="4k", one_way=True)
        self._addEntrance("right_taltal_connector1", water_cave_hole, right_taltal_connector1, None)
        self._addEntrance("right_taltal_connector2", right_taltal_connector_outside1, right_taltal_connector1, None)
        self._addEntrance("right_taltal_connector3", right_taltal_connector_outside1, right_taltal_connector2, None)
        self._addEntrance("right_taltal_connector4", right_taltal_connector_outside2, right_taltal_connector3, None)
        self._addEntrance("right_taltal_connector5", right_taltal_connector_outside2, right_taltal_connector4, None)
        self._addEntrance("right_taltal_connector6", d7_platau, right_taltal_connector4, None)
        self._addEntrance("right_fairy", right_taltal_connector_outside2, Location(), BOMB)
        self._addEntranceRequirementExit("right_fairy", None, id="4l") # if exiting, you do not need bombs
        self._addEntrance("d7", d7_tower, None, None)
        if options.logic != "casual": # D7 area ledge drops
            d7_platau.connect(heartpiece_swim_cave, FLIPPERS, id="4m", one_way=True)
            d7_platau.connect(right_taltal_connector_outside1, None, id="4n", one_way=True)

        mountain_bridge_staircase = Location("Bridge Towards D8").connect(outside_rooster_house, OR(HOOKSHOT, ROOSTER), id="4o") # cross bridges to staircase
        if options.logic != "casual":  # ledge drop
            mountain_bridge_staircase.connect(windfish_egg, None, id="4p", one_way=True)

        left_right_connector_cave_entrance = Location("Path to West Tal Tal Entrance")
        left_right_connector_cave_exit = Location("Path to West Tal Tal Exit")
        left_right_connector_cave_entrance.connect(left_right_connector_cave_exit, OR(HOOKSHOT, ROOSTER), id="4q", one_way=True)  # pass through the underground passage to left side
        taltal_boulder_zone = Location("Falling Rocks")
        self._addEntrance("left_to_right_taltalentrance", mountain_bridge_staircase, left_right_connector_cave_entrance, r.pit_bush)
        self._addEntranceRequirementExit("left_to_right_taltalentrance", None, id="4r") # leaving doesn't require pit_bush
        self._addEntrance("left_taltal_entrance", taltal_boulder_zone, left_right_connector_cave_exit, None)
        mountain_heartpiece = Location().add(HeartPiece(0x2BA)) # heartpiece in connecting cave
        left_right_connector_cave_entrance.connect(mountain_heartpiece, BOMB, id="4s", one_way=True)  # in the connecting cave from right to left. one_way to prevent access to left_side_mountain via glitched logic

        taltal_boulder_zone.add(Chest(0x004)) # top of falling rocks hill
        taltal_madbatter = Location("Mountain Mad Batter").connect(Location().add(MadBatter(0x1E2)), MAGIC_POWDER, id="4t")
        self._addEntrance("madbatter_taltal", taltal_boulder_zone, taltal_madbatter, POWER_BRACELET)
        self._addEntranceRequirementExit("madbatter_taltal", None, id="4u") # if exiting, you do not need bracelet

        outside_fire_cave = Location("Outside Fire Cave")
        if options.logic != "casual":
            outside_fire_cave.connect(writes_hut_outside, None, id="4v", one_way=True)  # Jump down the ledge
        taltal_boulder_zone.connect(outside_fire_cave, None, id="4w", one_way=True)
        fire_cave_bottom = Location("Fire Cave South")
        fire_cave_top = Location("Fire Cave North").connect(fire_cave_bottom, COUNT(SHIELD, 2), id="4x")
        self._addEntrance("fire_cave_entrance", outside_fire_cave, fire_cave_bottom, BOMB)
        self._addEntranceRequirementExit("fire_cave_entrance", None, id="4y") # if exiting, you do not need bombs

        d8_entrance = Location("Outside D8")
        if options.logic != "casual":
            d8_entrance.connect(writes_hut_outside, None, id="4z", one_way=True) # Jump down the ledge
            d8_entrance.connect(outside_fire_cave, None, id="50", one_way=True) # Jump down the other ledge
        self._addEntrance("fire_cave_exit", d8_entrance, fire_cave_top, None)
        self._addEntrance("phone_d8", d8_entrance, self._createShopSanity(options, 8, 0x299, id="51"), None)
        self._addEntrance("d8", d8_entrance, None, AND(OCARINA, SONG3, SWORD))
        self._addEntranceRequirementExit("d8", None, id="52") # if exiting, you do not need to wake the turtle

        nightmare = Location("Nightmare")
        windfish = Location("Windfish").connect(nightmare, AND(MAGIC_POWDER, SWORD, OR(BOOMERANG, BOW)), id="53")

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            hookshot_cave.connect(hookshot_cave_chest, r.boots_jump, id="54") # boots jump the gap to the chest
            graveyard_cave_left.connect(graveyard_cave_right, r.hookshot_over_pit, id="55", one_way=True) # hookshot the block behind the stairs while over the pit
            swamp_chest.connect(swamp, r.wall_clip, id="56")  # Clip past the flower
            swamp.connect(outside_d2, AND(r.wall_clip, POWER_BRACELET), id="57", one_way=True) # clip the top wall to walk between the goponga flower and the wall
            swamp.connect(outside_d2, COUNT(SWORD, 2), id="58") # use l2 sword spin to kill goponga flowers
            outside_d2.connect(swamp, r.wall_clip, id="59", one_way=True) # Clip out at d2 entrance door
            swamp.connect(writes_hut_outside, r.hookshot_over_pit, id="5a", one_way=True) # hookshot the sign in front of writes hut
            graveyard_heartpiece.connect(graveyard_cave_right, FEATHER, id="5b") # jump to the bottom right tile around the blocks
            graveyard_heartpiece.connect(graveyard_cave_right, AND(r.wall_clip, OR(HOOKSHOT, BOOMERANG)), id="5c") # push bottom block, wall clip and hookshot/boomerang corner to grab item
            
            self._addEntranceRequirement("mamu", AND(r.wall_clip, FEATHER, POWER_BRACELET), id="5d") # can clear the gaps at the start with just feather, can reach bottom left sign with a well timed jump while wall clipped
            left_bay_area.connect(outside_bay_madbatter_entrance, AND(OR(FEATHER, ROOSTER), OR(MAGIC_POWDER, BOMB)), id="5e") # use bombs or powder to get rid of a bush on the other side by jumping across and placing the bomb/powder before you fall into the pit
            crow_gold_leaf.connect(castle_courtyard, POWER_BRACELET, id="5f") # bird on tree at left side kanalet, can use both rocks to kill the crow removing the kill requirement
            castle_inside.connect(kanalet_chain_trooper, BOOMERANG, id="5g", one_way=True) # kill the ball and chain trooper from the left side, then use boomerang to grab the dropped item
            animal_village_bombcave_heartpiece.connect(animal_village_bombcave, r.boots_jump, id="5h") # jump across horizontal 4 gap to heart piece
            animal_village_bombcave_heartpiece.connect(animal_village_bombcave, AND(BOMB, FEATHER, BOOMERANG), id="5i")  # use jump + boomerang to grab the item from below the ledge
            desert_lanmola.connect(desert, BOMB, id="5j") # use bombs to kill lanmola

            armos_maze.connect(outside_armos_cave, None, id="5k") # dodge the armos statues by activating them and running
            armos_maze.connect(outside_armos_temple, None, id="5l") # dodge the armos statues by activating them and running
            d6_connector_left.connect(d6_connector_right, AND(OR(FLIPPERS, PEGASUS_BOOTS), FEATHER), id="5m")  # jump the gap in underground passage to d6 left side to skip hookshot
            obstacle_cave_exit.connect(obstacle_cave_inside, AND(FEATHER, r.hookshot_over_pit), id="5n", one_way=True) # one way from right exit to middle, jump past the obstacle, and use hookshot to pull past the double obstacle
            d4_entrance_unlocked.connect(angler_tunnel_keyhole, None, id="5o", one_way=True) # walk backwards into the keyhole to obtain the item
            if not options.rooster:
                bird_key.connect(bird_cave, COUNT(POWER_BRACELET, 2), id="5p")  # corner walk past the one pit on the left side to get to the elephant statue
            right_taltal_connector2.connect(right_taltal_connector3, ROOSTER, id="5q", one_way=True) # jump off the ledge and grab rooster after landing on the pit
            fire_cave_bottom.connect(fire_cave_top, AND(r.damage_boost_special, PEGASUS_BOOTS), id="5r", one_way=True) # flame skip

        if options.logic == 'glitched' or options.logic == 'hell':
            papahl_house.connect(mamasha_trade, r.bomb_trigger, id="5s") # use a bomb trigger to trade with mamasha without having yoshi doll
            mabe_village.connect(outside_dream_hut, r.hookshot_clip, id="5t", one_way=True) # clip past the rocks in front of dream hut
            dream_hut_right.connect(dream_hut_left, r.super_jump_feather, id="5u") # super jump
            forest.connect(swamp, r.bomb_trigger, id="5v")  # bomb trigger tarin
            forest.connect(forest_heartpiece, r.bomb_trigger, id="5w", one_way=True) # bomb trigger heartpiece
            self._addEntranceRequirementEnter("hookshot_cave", r.hookshot_clip, id="5x") # clip past the rocks in front of hookshot cave
            swamp.connect(forest_toadstool, r.pit_buffer_itemless, id="5y", one_way=True) # villa buffer from top (swamp phonebooth area) to bottom (toadstool area)
            writes_hut_outside.connect(swamp, r.pit_buffer_itemless, id="5z", one_way=True) # villa buffer from top (writes hut) to bottom (swamp phonebooth area) or damage boost
            graveyard.connect(forest_heartpiece, r.pit_buffer_itemless, id="60", one_way=True) # villa buffer from top.
            graveyard.connect(forest, None, id="61", one_way=True) # villa buffer from the top twice to get to the main forest area
            log_cave_heartpiece.connect(forest_cave, r.super_jump_feather, id="62") # super jump
            log_cave_heartpiece.connect(forest_cave, r.bomb_trigger, id="63") # bomb trigger
            graveyard_cave_left.connect(graveyard_heartpiece, r.bomb_trigger, id="64", one_way=True) # bomb trigger the heartpiece from the left side
            graveyard_heartpiece.connect(graveyard_cave_right, r.sideways_block_push, id="65") # sideways block push from the right staircase.
            
            prairie_island_seashell.connect(ukuku_prairie, AND(r.jesus_jump, r.bush), id="66") # jesus jump from right side, screen transition on top of the water to reach the island
            self._addEntranceRequirement("castle_jump_cave", r.pit_buffer, id="67") # 1 pit buffer to clip bottom wall and jump across.
            left_bay_area.connect(ghost_hut_outside, r.pit_buffer, id="68") # 1 pit buffer to get across
            tiny_island.connect(left_bay_area, AND(r.jesus_jump, r.bush), id="69") # jesus jump around
            bay_madbatter_connector_exit.connect(bay_madbatter_connector_entrance, r.jesus_jump, id="6a", one_way=True) # jesus jump (3 screen) through the underground passage leading to martha's bay mad batter
            left_bay_area.connect(outside_bay_madbatter_entrance, AND(r.pit_buffer, POWER_BRACELET), id="6b") # villa buffer into the top side of the bush, then pick it up
            
            ukuku_prairie.connect(richard_maze, AND(r.pit_buffer_itemless, OR(AND(MAGIC_POWDER, MAX_POWDER_UPGRADE), BOMB, BOOMERANG, MAGIC_ROD, SWORD)), id="6c", one_way=True) # break bushes on north side of the maze, and 1 pit buffer into the maze
            richard_maze.connect(ukuku_prairie, AND(r.pit_buffer_itemless, OR(MAGIC_POWDER, BOMB, BOOMERANG, MAGIC_ROD, SWORD)), id="6d", one_way=True) # same as above (without powder upgrade) in one of the two northern screens of the maze to escape
            fisher_under_bridge.connect(bay_water, AND(r.bomb_trigger, AND(FEATHER, FLIPPERS)), id="6e") # up-most left wall is a pit: bomb trigger with it. If photographer is there, clear that first which is why feather is required logically
            animal_village.connect(ukuku_prairie, r.jesus_jump, id="6f") # jesus jump
            below_right_taltal.connect(next_to_castle, r.jesus_jump, id="6g") # jesus jump (north of kanalet castle phonebooth)
            #animal_village_connector_right.connect(animal_village_connector_left, AND(r.text_clip, FEATHER), id="b4") # text clip past the obstacles (can go both ways), feather to wall clip the obstacle without triggering text
            animal_village_bombcave_heartpiece.connect(animal_village_bombcave, AND(r.bomb_trigger, OR(HOOKSHOT, FEATHER, r.boots_bonk_pit)), id="6h") # bomb trigger from right side, corner walking top right pit is stupid so hookshot or boots added
            animal_village_bombcave_heartpiece.connect(animal_village_bombcave,  r.pit_buffer, id="6i") # villa buffer across the pits


            d6_entrance.connect(ukuku_prairie, r.jesus_jump, id="6j", one_way=True) # jesus jump (2 screen) from d6 entrance bottom ledge to ukuku prairie
            d6_entrance.connect(armos_fairy_entrance, r.jesus_jump, id="6k", one_way=True) # jesus jump (2 screen) from d6 entrance top ledge to armos fairy entrance
            d6_connector_left.connect(d6_connector_right, r.jesus_jump, id="6l") # jesus jump over water; left side is jumpable, or villa buffer if it's easier for you
            armos_fairy_entrance.connect(d6_armos_island, r.jesus_jump, id="6m", one_way=True) # jesus jump from top (fairy bomb cave) to armos island
            armos_fairy_entrance.connect(raft_exit, r.jesus_jump, id="6n") # jesus jump (2-ish screen) from fairy cave to lower raft connector
            windfish_egg.connect(outside_obstacle_cave, r.hookshot_clip, id="6o", one_way=True) # clip past the rocks in front of obstacle cave entrance
            obstacle_cave_inside_chest.connect(obstacle_cave_inside, r.pit_buffer, id="6p") # jump to the rightmost pits + 1 pit buffer to jump across
            obstacle_cave_exit.connect(obstacle_cave_inside, r.pit_buffer, id="6q") # 1 pit buffer above boots crystals to get past
            lower_right_taltal.connect(hibiscus_item, AND(TRADING_ITEM_PINEAPPLE, r.bomb_trigger), id="6r", one_way=True) # bomb trigger papahl from below ledge, requires pineapple
            lower_right_taltal.connect(d4_entrance_locked, r.jesus_jump, id="6s", one_way=True) # jump down waterfall
            self._addEntranceRequirementExit("d4", None, id="6t") # if exiting, you can access d4_entrance_locked. From there apply jesus jumps/roosters/flippers/unlock requirements
            d4_entrance_locked.connect(angler_tunnel_keyhole, r.jesus_jump, id="6u", one_way=True) # use jesus jumps to face upwards into the keyhole from above
            below_right_taltal.connect(d4_entrance_locked, OR(r.super_jump_boots, HOOKSHOT), id="6v", one_way=True) # superjump off bottom wall, or hookshot clip the block as it's moving up # TODO d4_connector
            
            below_right_taltal.connect(outside_swim_cave, r.jesus_jump, id="6w") # jesus jump into the cave entrance after jumping down the ledge, can jesus jump back to the ladder 1 screen below
            outside_mambo.connect(d4_entrance_locked, r.jesus_jump, id="6x")  # jesus jump from d4 entrance to mambo's cave entrance
            outside_raft_house.connect(below_right_taltal, r.jesus_jump, id="6y", one_way=True) # jesus jump from the ledge at raft to the staircase 1 screen south

            lower_right_taltal.connect(outside_multichest_left, r.jesus_jump, id="6z") # jesus jump past staircase leading up the mountain 
            outside_rooster_house.connect(lower_right_taltal, r.jesus_jump, id="70") # jesus jump (1 or 2 screen depending if angler key is used) to staircase leading up the mountain
            d7_platau.connect(water_cave_hole, None, id="71", one_way=True) # use save and quit menu to gain control while falling to dodge the water cave hole
            water_cave_hole.connect(heartpiece_swim_cave, r.jesus_jump, id="72", one_way=True) # use jesus jumps to jump out of the cave after falling down the hole
            mountain_bridge_staircase.connect(outside_rooster_house, AND(r.boots_jump, r.pit_buffer), id="73") # cross bridge to staircase with pit buffer to clip bottom wall and jump across. added boots_jump to not require going through this section with just feather
            bird_key.connect(bird_cave, r.hookshot_jump, id="74")  # hookshot jump across the big pits room
            right_taltal_connector2.connect(right_taltal_connector3, OR(r.pit_buffer, ROOSTER), id="75", one_way=True) # trigger a quick fall on the screen above the exit by transitioning down on the leftmost/rightmost pit and then buffering sq menu for control while in the air. or pick up the rooster while dropping off the ledge at exit
            left_right_connector_cave_exit.connect(left_right_connector_cave_entrance, AND(HOOKSHOT, r.super_jump_feather), id="76", one_way=True)  # pass through the passage in reverse using a superjump to get out of the dead end
            obstacle_cave_inside.connect(mountain_heartpiece, r.bomb_trigger, id="77", one_way=True) # bomb trigger from boots crystal cave
            self._addEntranceRequirement("d8", OR(r.bomb_trigger, AND(OCARINA, SONG3)), id="78") # bomb trigger the head and walk through, or play the ocarina song 3 and walk through

        if options.logic == 'hell':
            dream_hut_right.connect(dream_hut, None, id="79") # alternate diagonal movement with orthogonal movement to control the mimics. Get them clipped into the walls to walk past
            swamp.connect(forest_toadstool, r.damage_boost, id="7a") # damage boost from toadstool area across the pit
            swamp.connect(forest, AND(r.bush, OR(r.boots_bonk_pit, r.hookshot_spam_pit)), id="7b") # boots bonk / hookshot spam over the pits right of forest_rear_chest
            forest.connect(forest_heartpiece, r.boots_bonk_pit, id="7c", one_way=True) # boots bonk across the pits
            forest_cave_crystal_chest.connect(forest_cave, AND(r.super_jump_feather, r.hookshot_clip_block, r.sideways_block_push), id="7d") # superjump off the bottom wall to get between block and crystal, than use 3 keese to hookshot clip while facing right to get a sideways blockpush off
            log_cave_heartpiece.connect(forest_cave, BOOMERANG, id="7e") # clip the boomerang through the corner gaps on top right to grab the item
            log_cave_heartpiece.connect(forest_cave, OR(r.super_jump_rooster, r.boots_roosterhop), id="7f") # boots rooster hop in bottom left corner to "superjump" into the area. use buffers after picking up rooster to gain height / time to throw rooster again facing up
            writes_hut_outside.connect(swamp, r.damage_boost, id="7g") # damage boost with moblin arrow next to telephone booth
            writes_cave_left_chest.connect(writes_cave, r.damage_boost, id="7h") # damage boost off the zol to get across the pit.
            graveyard.connect(crazy_tracy_hut, r.hookshot_spam_pit, id="7i", one_way=True) # use hookshot spam to clip the rock on the right with the crow
            graveyard.connect(forest, OR(r.boots_bonk_pit, r.hookshot_spam_pit), id="7j") # boots bonk over pits by witches hut, or hookshot spam across the pit
            graveyard_cave_left.connect(graveyard_cave_right, r.hookshot_spam_pit, id="7k") # hookshot spam over the pit
            graveyard_cave_right.connect(graveyard_cave_left, OR(r.damage_boost, r.boots_bonk_pit), id="7l", one_way=True) # boots bonk off the cracked block, or set up a damage boost with the keese
            
            self._addEntranceRequirementEnter("mamu", AND(r.pit_buffer_itemless, r.pit_buffer_boots, POWER_BRACELET), id="7m") # can clear the gaps at the start with multiple pit buffers, can reach bottom left sign with bonking along the bottom wall
            self._addEntranceRequirement("castle_jump_cave", r.pit_buffer_boots, id="7n") # pit buffer to clip bottom wall and boots bonk across
            prairie_cave_secret_exit.connect(prairie_cave, AND(BOMB, OR(r.boots_bonk_pit, r.hookshot_spam_pit)), id="7o") # hookshot spam or boots bonk across pits can go from left to right by pit buffering on top of the bottom wall then boots bonk across
            richard_cave_chest.connect(richard_cave, r.damage_boost, id="7p") # use the zol on the other side of the pit to damage boost across (requires damage from pit + zol)
            castle_secret_entrance_right.connect(castle_secret_entrance_left, r.boots_bonk_2d_spikepit, id="7q") # medicine iframe abuse to get across spikes with a boots bonk
            left_bay_area.connect(ghost_hut_outside, r.pit_buffer_boots, id="7r") # multiple pit buffers to bonk across the bottom wall
            left_bay_area.connect(ukuku_prairie, r.hookshot_clip_block, id="7s", one_way=True) # clip through the donuts blocking the path next to prairie plateau cave by hookshotting up and killing the two moblins that way which clips you further up two times. This is enough to move right
            tiny_island.connect(left_bay_area, AND(r.jesus_buffer, r.boots_bonk_pit, r.bush), id="7t") # jesus jump around with boots bonks, then one final bonk off the bottom wall to get on the staircase (needs to be centered correctly)
            left_bay_area.connect(outside_bay_madbatter_entrance, AND(r.pit_buffer_boots, OR(MAGIC_POWDER, SWORD, MAGIC_ROD, BOOMERANG)), id="7u") # Boots bonk across the bottom wall, then remove one of the bushes to get on land
            left_bay_area.connect(outside_bay_madbatter_entrance, AND(r.pit_buffer, r.hookshot_spam_pit, r.bush), id="7v") # hookshot spam to cross one pit at the top, then buffer until on top of the bush to be able to break it
            outside_bay_madbatter_entrance.connect(left_bay_area, AND(r.pit_buffer_boots, r.bush), id="7w", one_way=True) # if exiting, you can pick up the bushes by normal means and boots bonk across the bottom wall

            # bay_water connectors, only left_bay_area, ukuku_prairie and animal_village have to be connected with jesus jumps. below_right_taltal, d6_armos_island and armos_fairy_entrance are accounted for via ukuku prairie in glitch logic
            left_bay_area.connect(bay_water, OR(r.jesus_jump, r.jesus_rooster), id="7x") # jesus jump/rooster (can always reach bay_water with jesus jumping from every way to enter bay_water, so no one_way)
            animal_village.connect(bay_water, OR(r.jesus_jump, r.jesus_rooster), id="7y") # jesus jump/rooster (can always reach bay_water with jesus jumping from every way to enter bay_water, so no one_way)
            ukuku_prairie.connect(bay_water, OR(r.jesus_jump, r.jesus_rooster), id="7z", one_way=True) # jesus jump/rooster
            bay_water.connect(d5_entrance, OR(r.jesus_jump, r.jesus_rooster), id="80") # jesus jump/rooster into d5 entrance (wall clip), wall clip + jesus jump to get out
            prairie_island_seashell.connect(ukuku_prairie, AND(r.jesus_rooster, r.bush), id="81") # jesus rooster from right side, screen transition on top of the water to reach the island
            bay_madbatter_connector_exit.connect(bay_madbatter_connector_entrance, r.jesus_rooster, id="82", one_way=True) # jesus rooster (3 screen) through the underground passage leading to martha's bay mad batter
            # fisher_under_bridge.connect(bay_water, AND(TRADING_ITEM_FISHING_HOOK, OR(FEATHER, SWORD, BOW), FLIPPERS), id="b5") # just swing/shoot at fisher, if photographer is on screen it is dumb
            fisher_under_bridge.connect(bay_water, AND(TRADING_ITEM_FISHING_HOOK, FLIPPERS), id="83") # face the fisherman from the left, get within 4 pixels (a range, not exact) of his left side, hold up, and mash a until you get the textbox.

			#TODO: add jesus rooster to trick list
            
            below_right_taltal.connect(next_to_castle, r.jesus_buffer, id="84", one_way=True) # face right, boots bonk and get far enough left to jesus buffer / boots bonk across the bottom wall to the stairs
            crow_gold_leaf.connect(castle_courtyard, BOMB, id="85") # bird on tree at left side kanalet, place a bomb against the tree and the crow flies off. With well placed second bomb the crow can be killed
            mermaid_statue.connect(animal_village, AND(TRADING_ITEM_SCALE, r.super_jump_feather), id="86") # early mermaid statue by buffering on top of the right ledge, then superjumping to the left (horizontal pixel perfect)
            animal_village_connector_right.connect(animal_village_connector_left, r.shaq_jump, id="87") # shaq jump off the obstacle to get through 
            animal_village_connector_left.connect(animal_village_connector_right, r.hookshot_clip_block, id="88", one_way=True) # use hookshot with an enemy to clip through the obstacle
            animal_village_bombcave_heartpiece.connect(animal_village_bombcave, r.pit_buffer_boots, id="89") # boots bonk across bottom wall (both at entrance and in item room)

            d6_armos_island.connect(ukuku_prairie, OR(r.jesus_jump, r.jesus_rooster), id="8a") # jesus jump/rooster (3 screen) from seashell mansion to armos island
            armos_fairy_entrance.connect(d6_armos_island, r.jesus_buffer, id="8b", one_way=True) # jesus jump from top (fairy bomb cave) to armos island with fast falling 
            d6_connector_right.connect(d6_connector_left, r.pit_buffer_boots, id="8c") # boots bonk across bottom wall at water and pits (can do both ways)

            d6_entrance.connect(ukuku_prairie, r.jesus_rooster, id="8d", one_way=True) # jesus rooster (2 screen) from d6 entrance bottom ledge to ukuku prairie
            d6_entrance.connect(armos_fairy_entrance, r.jesus_rooster, id="8e", one_way=True) # jesus rooster (2 screen) from d6 entrance top ledge to armos fairy entrance
            armos_fairy_entrance.connect(d6_armos_island, r.jesus_rooster, id="8f", one_way=True) # jesus rooster from top (fairy bomb cave) to armos island
            armos_fairy_entrance.connect(raft_exit, r.jesus_rooster, id="8g") # jesus rooster (2-ish screen) from fairy cave to lower raft connector
            

            obstacle_cave_entrance.connect(obstacle_cave_inside, OR(r.hookshot_clip_block, r.shaq_jump), id="8h") # get past crystal rocks by hookshotting into top pushable block, or boots dashing into top wall where the pushable block is to superjump down
            obstacle_cave_entrance.connect(obstacle_cave_inside, r.boots_roosterhop, id="8i") # get past crystal rocks pushing the top pushable block, then boots dashing up picking up the rooster before bonking. Pause buffer until rooster is fully picked up then throw it down before bonking into wall
            d4_entrance_locked.connect(below_right_taltal, OR(r.jesus_jump, r.jesus_rooster), id="8j") # jesus jump/rooster 5 screens to staircase below damp cave
            d4_entrance_locked.connect(angler_tunnel_keyhole, OR(ROOSTER, r.jesus_buffer), id="8k", one_way=True) # use boots bonk or rooster while leaving d4 to face upwards and buffer into the keyhole from above (other options are covered in d4_entrance_locked access like getting here from a different screen)
            below_right_taltal.connect(d4_entrance_locked, AND(r.shaq_jump, r.super_jump_feather), id="8l", one_way=True) # shaq jump off the pushable block to clip the right wall, then feather only superjump in the top right corner over the block # TODO d4_connector
            lower_right_taltal.connect(angler_tunnel_keyhole, OR(ROOSTER, AND(r.jesus_buffer, r.midair_turn)), id="8m", one_way=True) # activate angler keyhole from the back, has to face up and press up on keyblock. From top mountains, use either rooster or boots bonks to get there and use an item to face upwards. With rooster you can face up before jumping down waterfall
            middle_right_taltal.connect(angler_tunnel_keyhole, OR(ROOSTER, AND(r.jesus_buffer, r.midair_turn)), id="8n", one_way=True) # activate angler keyhole from the back, has to face up and press up on keyblock. From top mountains, use either rooster or boots bonks to get there and use an item to face upwards. With rooster you can face up before jumping down waterfall

            lower_right_taltal.connect(below_right_taltal, OR(r.jesus_jump, r.jesus_rooster), id="8o", one_way=True) # jesus jump/rooster to upper ledges, jump off, enter and exit s+q menu to regain pauses, then jesus jump 4 screens to staircase below damp cave
            below_right_taltal.connect(outside_swim_cave, r.jesus_rooster, id="8p") # jesus rooster into the cave entrance after jumping down the ledge, can jesus jump back to the ladder 1 screen below
            outside_mambo.connect(d4_entrance_locked, OR(r.jesus_rooster, r.jesus_jump), id="8q")  # jesus jump/rooster to mambo's cave entrance
            if options.hardmode != "oracle": # don't take damage from drowning in water. Could get it with more health probably but standard 3 hearts is not enough
                mambo.connect(inside_mambo, AND(OCARINA, r.bomb_trigger), id="8r")  # while drowning, buffer a bomb and after it explodes, buffer another bomb out of the save and quit menu. 
            outside_raft_house.connect(below_right_taltal, r.jesus_rooster, id="8s", one_way=True) # jesus rooster from the ledge at raft to the staircase 1 screen south
            lower_right_taltal.connect(outside_multichest_left, r.jesus_rooster, id="8t") # jesus rooster past staircase leading up the mountain 
            outside_rooster_house.connect(below_right_taltal, r.jesus_rooster, id="8u", one_way=True) # jesus rooster down to staircase below damp cave
            outside_rooster_house.connect(middle_right_taltal, r.jesus_buffer, id="8v", one_way=True) # boots bonk from the staircase to the bottom left next to the waterfall to avoid falling down
            
            if options.entranceshuffle in ("default", "simple"): # connector cave from armos d6 area to raft shop may not be randomized to add a flippers path since flippers stop you from jesus jumping
                below_right_taltal.connect(raft_game, AND(OR(r.jesus_jump, r.jesus_rooster), r.attack_hookshot_powder), id="8w", one_way=True) # jesus jump from heartpiece water cave, around the island and clip past the diagonal gap in the rock, then jesus jump all the way down the waterfall to the chests (attack req for hardlock flippers+feather scenario)
            outside_raft_house.connect(below_right_taltal, AND(r.super_jump, PEGASUS_BOOTS), id="8x") # superjump from ledge left to right, can buffer to land on ledge instead of water, then superjump right which is pixel perfect. Boots to get out of wall after landing
            bridge_seashell.connect(outside_rooster_house, AND(OR(r.hookshot_spam_pit, r.boots_bonk_pit), POWER_BRACELET), id="8y") # boots bonk or hookshot spam over the pit to get to the rock
            bird_key.connect(bird_cave, AND(r.boots_jump, r.pit_buffer), id="8z") # boots jump above wall, use multiple pit buffers to get across
            right_taltal_connector2.connect(right_taltal_connector3, r.pit_buffer_itemless, id="90", one_way=True) # 2 separate pit buffers so not obnoxious to get past the two pit rooms before d7 area. 2nd pits can pit buffer on top right screen, bottom wall to scroll on top of the wall on bottom screen
            water_cave_hole.connect(heartpiece_swim_cave, r.jesus_buffer_itemless, id="91", one_way=True) # after falling down the hole, use pause buffers to get down towards the entrance
            mountain_bridge_staircase.connect(outside_rooster_house, r.pit_buffer_boots, id="92") # cross bridge to staircase with pit buffer to clip bottom wall and jump or boots bonk across
            left_right_connector_cave_entrance.connect(left_right_connector_cave_exit, AND(r.boots_jump, r.pit_buffer), id="93", one_way=True) # boots jump to bottom left corner of pits, pit buffer and jump to left
            left_right_connector_cave_exit.connect(left_right_connector_cave_entrance, AND(ROOSTER, OR(r.boots_roosterhop, r.super_jump_rooster)), id="94", one_way=True)  # pass through the passage in reverse using a boots rooster hop or rooster superjump in the one way passage area
            
            windfish.connect(nightmare, AND(SWORD, OR(BOOMERANG, BOW, BOMB, COUNT(SWORD, 2), AND(OCARINA, OR(SONG1, SONG3)))), id="95") # sword quick kill blob, can kill dethl with bombs or sword beams, and can use ocarina to freeze one of ganon's bats to skip dethl eye phase
            
        self.start = start_house
        self.egg = windfish_egg
        self.nightmare = nightmare
        self.windfish = windfish

    def _addEntrance(self, name, outside, inside, requirement):
        assert name not in self.entrances, "Duplicate entrance: %s" % name
        assert name in worldSetup.ENTRANCE_INFO
        self.entrances[name] = EntranceExterior(outside, requirement, id=name)
        self.entrances[f"{name}:inside"] = EntranceExterior(inside, None, id=name)

    def _addEntranceRequirement(self, name, requirement, id=None):
        assert name in self.entrances
        self.entrances[name].addRequirement(requirement, id)

    def _addEntranceRequirementEnter(self, name, requirement, id=None):
        assert name in self.entrances
        self.entrances[name].addEnterRequirement(requirement, id)

    def _addEntranceRequirementExit(self, name, requirement, id=None):
        assert name in self.entrances
        self.entrances[name].addExitRequirement(requirement, id)

    def updateIndoorLocation(self, name, location):
        name = f"{name}:inside"
        assert name in self.entrances, name
        assert self.entrances[name].location is None
        self.entrances[name].location = location

    def _createShopSanity(self, options, index, room, id=None):
        if options.shopsanity == '':
            return Location()
        shop = Location(f"Shop_{room:03X}")
        Location().add(ShopItem(0, room=room)).connect(shop, FOUND("RUPEES", 100 + 100 * index), id=f"{id}-0")
        Location().add(ShopItem(1, room=room)).connect(shop, FOUND("RUPEES", 150 + 100 * index), id=f"{id}-1")
        return shop


class DungeonDiveOverworld:
    def __init__(self, options, r):
        self.entrances = {}

        start_house = Location().add(StartItem())
        Location().add(ShopItem(0)).connect(start_house, COUNT("RUPEES", 200), id="96")
        Location().add(ShopItem(1)).connect(start_house, COUNT("RUPEES", 980), id="97")
        Location().add(Song(0x0B1)).connect(start_house, OCARINA, id="98")  # Marins song
        start_house.add(DroppedKey(0xB2))  # Sword on the beach
        egg = Location().connect(start_house, AND(r.bush, BOMB), id="99")
        Location().add(MadBatter(0x1E1)).connect(start_house, MAGIC_POWDER, id="9a")
        if options.boomerang == 'trade':
            Location().add(BoomerangGuy()).connect(start_house, AND(BOMB, OR(BOOMERANG, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS, FEATHER, SHOVEL)), id="9b")
        elif options.boomerang == 'gift':
            Location().add(BoomerangGuy()).connect(start_house, BOMB, id="9c")

        nightmare = Location()
        windfish = Location().connect(nightmare, AND(MAGIC_POWDER, SWORD, OR(BOOMERANG, BOW)), id="9d")

        self.start = start_house
        self.entrances = {
            "d1": EntranceExterior(start_house, None),
            "d2": EntranceExterior(start_house, None),
            "d3": EntranceExterior(start_house, None),
            "d4": EntranceExterior(start_house, None),
            "d5": EntranceExterior(start_house, FLIPPERS),
            "d6": EntranceExterior(start_house, None),
            "d7": EntranceExterior(start_house, None),
            "d8": EntranceExterior(start_house, None),
            "d0": EntranceExterior(start_house, None),
            "d1:inside": EntranceExterior(None, None),
            "d2:inside": EntranceExterior(None, None),
            "d3:inside": EntranceExterior(None, None),
            "d4:inside": EntranceExterior(None, None),
            "d5:inside": EntranceExterior(None, None),
            "d6:inside": EntranceExterior(None, None),
            "d7:inside": EntranceExterior(None, None),
            "d8:inside": EntranceExterior(None, None),
            "d0:inside": EntranceExterior(None, None),
        }
        self.egg = egg
        self.nightmare = nightmare
        self.windfish = windfish

    def updateIndoorLocation(self, name, location):
        self.entrances[f"{name}:inside"].location = location


class DungeonChain:
    def __init__(self, options, r):
        start_house = Location().add(StartItem())

        nightmare = Location()
        windfish = Location().connect(nightmare, AND(MAGIC_POWDER, SWORD, OR(BOOMERANG, BOW)), id="b6")

        self.start = start_house
        self.nightmare = nightmare
        self.windfish = windfish
        self.__end = self.start

    def chain(self, dungeon):
        self.__end.connect(dungeon.entrance, None, id="b7")
        self.__end = dungeon.final_room
        # Remove the instruments and fairy rewards from logic, reward room is entrance to next dungeon.
        dungeon.final_room.items = [i for i in dungeon.final_room.items if not isinstance(i, Instrument)]
        dungeon.final_room.items = [i for i in dungeon.final_room.items if not isinstance(i, TunicFairy)]


class ALttP:
    def __init__(self, options, world_setup, r):
        self.entrances = {}

        start_area = Location()
        start_house = Location().add(StartItem())
        self._addEntrance("start_house", start_area, start_house, None)
        Location().add(Song(0x092)).connect(start_area, AND(OCARINA, r.bush), id="9e")  # Marins song
        seashell_mansion = Location()
        if options.goal != "seashells":
            Location().add(SeashellMansionBonus(0)).connect(seashell_mansion, COUNT(SEASHELL, 5), id="9f")
            Location().add(SeashellMansionBonus(1)).connect(seashell_mansion, COUNT(SEASHELL, 10), id="9g")
            Location().add(SeashellMansion(0x2E9)).connect(seashell_mansion, COUNT(SEASHELL, 20), id="9h")
        else:
            seashell_mansion.add(DroppedKey(0x2E9))
        self._addEntrance("seashell_mansion", start_area, seashell_mansion, None)

        start_area.add(Seashell(0x4A))
        graveyard_cave_left = Location()
        graveyard_cave_right = Location().connect(graveyard_cave_left, OR(FEATHER, ROOSTER), id="9i")
        graveyard_heartpiece = Location().add(HeartPiece(0x2DF)).connect(graveyard_cave_right, OR(AND(BOMB, OR(HOOKSHOT, PEGASUS_BOOTS), FEATHER), ROOSTER), id="9j")  # grave cave
        self._addEntrance("graveyard_cave_left", start_area, graveyard_cave_left, None)
        # self._addEntrance("graveyard_cave_right", graveyard, graveyard_cave_right, None)

        start_area.connect(Location().add(Seashell(0xC7)), AND(POWER_BRACELET, HAMMER), id="9k")
        self._addEntrance("d1", start_area, None, None)
        self._addEntrance("prairie_left_cave1", start_area, Location().add(Chest(0x2CD)), BOMB)  # cave next to town
        banana_seller = Location()
        banana_seller.connect(Location().add(TradeSequenceItem(0x2FE, TRADING_ITEM_BANANAS)), TRADING_ITEM_DOG_FOOD, id="9l")
        self._addEntrance("banana_seller", start_area, banana_seller, r.bush)
        boomerang_cave = Location()
        if options.boomerang == 'trade':
            Location().add(BoomerangGuy()).connect(boomerang_cave, OR(BOOMERANG, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS, FEATHER, SHOVEL), id="9m")
        elif options.boomerang == 'gift':
            Location().add(BoomerangGuy()).connect(boomerang_cave, None, id="9n")
        self._addEntrance("boomerang_cave", start_area, boomerang_cave, BOMB)
        self._addEntranceRequirementExit("boomerang_cave", None, id="9o") # if exiting, you do not need bombs
        bay_madbatter = Location().connect(Location().add(MadBatter(0x1E0)), MAGIC_POWDER, id="9p")
        self._addEntrance("prairie_madbatter", start_area, bay_madbatter, None)
        d5_entrance = Location().connect(start_area, FLIPPERS, id="9q")
        self._addEntrance("d5", d5_entrance, None, None)

        maze_entrance = Location()
        maze_exit = Location().add(HeartPiece(0xB0)).connect(maze_entrance, AND(r.bush, POWER_BRACELET), id="9r")
        papahl_house = Location()
        papahl_house.connect(Location().add(TradeSequenceItem(0x2A6, TRADING_ITEM_RIBBON)), TRADING_ITEM_YOSHI_DOLL, id="9s")
        self._addEntrance("papahl_house_left", maze_entrance, papahl_house, None)
        self._addEntrance("papahl_house_right", start_area, papahl_house, None)
        trendy_shop = Location()
        trendy_shop.connect(Location().add(TradeSequenceItem(0x2A0, TRADING_ITEM_YOSHI_DOLL)), FOUND("RUPEES", 50), id="9t")
        self._addEntrance("trendy_shop", start_area, trendy_shop, r.bush)
        shop = Location()
        Location().add(ShopItem(0)).connect(shop, COUNT("RUPEES", 200), id="9u")
        Location().add(ShopItem(1)).connect(shop, COUNT("RUPEES", 980), id="9v")
        self._addEntrance("shop", start_area, shop, None)
        writes_house = Location()
        writes_house.connect(Location().add(TradeSequenceItem(0x2a8, TRADING_ITEM_BROOM)), TRADING_ITEM_LETTER, id="9w")
        self._addEntrance("writes_house", start_area, writes_house, None)
        cookhouse = Location()
        cookhouse.connect(Location().add(TradeSequenceItem(0x2D7, TRADING_ITEM_PINEAPPLE)), TRADING_ITEM_HONEYCOMB, id="9x")
        self._addEntrance("animal_house5", start_area, cookhouse, None)
        goathouse = Location()
        goathouse.connect(Location().add(TradeSequenceItem(0x2D9, TRADING_ITEM_LETTER)), TRADING_ITEM_HIBISCUS, id="9y")
        self._addEntrance("animal_house3", start_area, goathouse, None)
        kennel = Location().connect(Location().add(Seashell(0x2B2)), SHOVEL, id="9z")  # in the kennel
        kennel.connect(Location().add(TradeSequenceItem(0x2B2, TRADING_ITEM_DOG_FOOD)), TRADING_ITEM_RIBBON, id="a0")
        self._addEntrance("kennel", start_area, kennel, None)
        desert_cave = Location()
        Location().add(HeartPiece(0x1E8)).connect(desert_cave, BOMB, id="a1")  # above the quicksand cave
        self._addEntrance("desert_cave", start_area, desert_cave, None)

        castle_courtyard = Location()
        castle_courtyard_secret = Location().connect(castle_courtyard, r.bush, id="a2")
        castle_secret_entrance_left = Location()
        castle_secret_entrance_right = Location().connect(castle_secret_entrance_left, FEATHER, id="a3")
        self._addEntrance("castle_secret_entrance", start_area, castle_secret_entrance_right, r.pit_bush)
        self._addEntrance("castle_secret_exit", castle_courtyard_secret, castle_secret_entrance_left, None)
        castle_inside = Location()
        Location().add(KeyHole(0x2C3, CASTLE_GATE_OPENED)).connect(castle_inside, None, id="a4")
        castle_top_outside = Location()
        castle_top_inside = Location()
        self._addEntrance("castle_main_entrance", castle_courtyard, castle_inside, None)
        self._addEntrance("castle_upper_left", castle_top_outside, castle_inside, None)
        self._addEntrance("castle_upper_right", castle_top_outside, castle_top_inside, None)
        Location().add(GoldLeaf(0x2D2)).connect(castle_inside, r.attack_hookshot_powder, id="a5")  # in the castle, kill enemies
        Location().add(GoldLeaf(0x2C5)).connect(castle_inside, AND(BOMB, r.attack_hookshot_powder), id="a6")  # in the castle, bomb wall to show enemy
        kanalet_chain_trooper = Location().add(GoldLeaf(0x2C6))  # in the castle, spinning spikeball enemy
        castle_top_inside.connect(kanalet_chain_trooper, AND(POWER_BRACELET, r.attack_hookshot), id="a7", one_way=True)

        dream_hut = Location()
        dream_hut_right = Location().add(Chest(0x2BF)).connect(dream_hut, SWORD, id="a8")
        if options.logic != "casual":
            dream_hut_right.connect(dream_hut, OR(BOOMERANG, HOOKSHOT, FEATHER), id="a9")
        Location().add(Chest(0x2BE)).connect(dream_hut_right, PEGASUS_BOOTS, id="aa")
        self._addEntrance("dream_hut", start_area, dream_hut, None)

        desert = Location().connect(start_area, OR(POWER_BRACELET, HAMMER), id="ab")
        self._addEntrance("armos_maze_cave", desert, Location().add(Chest(0x2FC)), None)

        fire_cave_bottom = Location()
        desert_ledge1 = Location().add(HeartPiece(0xD4))
        fire_cave_top = Location().connect(fire_cave_bottom, COUNT(SHIELD, 2), id="ac")
        self._addEntrance("fire_cave_entrance", desert, fire_cave_bottom, None)
        self._addEntrance("fire_cave_exit", desert_ledge1, fire_cave_top, None)
        self._addEntrance("d8", desert, None, AND(OCARINA, SONG3))

        forest = Location().connect(start_area, OR(FEATHER, ROOSTER, AND(COUNT(POWER_BRACELET, 2), HAMMER)), id="ad")
        forest.add(Toadstool(0x11))
        self._addEntrance("d2", forest, None, None)
        hookshot_cave = Location()
        hookshot_cave_chest = Location().add(Chest(0x2B3)).connect(hookshot_cave, OR(HOOKSHOT, ROOSTER), id="ae")
        self._addEntrance("hookshot_cave", forest, hookshot_cave, POWER_BRACELET)
        moblin_cave = Location().connect(Location().add(Chest(0x2E2)), AND(r.attack_hookshot_powder, r.miniboss_requirements[world_setup.miniboss_mapping["moblin_cave"]]), id="af")
        self._addEntrance("moblin_cave", forest, moblin_cave, None)

        ghost_hut_inside = Location().connect(Location().add(Seashell(0x1E3)), POWER_BRACELET, id="ag")
        self._addEntrance("ghost_house", start_area, ghost_hut_inside, None)
        taltal_madbatter = Location().connect(Location().add(MadBatter(0x1E2)), MAGIC_POWDER, id="ah")
        self._addEntrance("madbatter_taltal", start_area, taltal_madbatter, POWER_BRACELET)

        nightmare = Location()
        windfish = Location().connect(nightmare, AND(MAGIC_POWDER, SWORD, OR(BOOMERANG, BOW)), id="ai")

        Location().add(Seashell(0xBF)).connect(start_area, AND(HAMMER, POWER_BRACELET), id="aj")
        armos_maze = Location().connect(start_area, POWER_BRACELET, id="ak")
        armos_temple = Location()
        Location().add(FaceKey()).connect(armos_temple, r.miniboss_requirements[world_setup.miniboss_mapping["armos_temple"]], id="al")
        self._addEntrance("armos_temple", armos_maze, armos_temple, None)
        self._addEntrance("d6", armos_maze, None, None)

        witch_hut_area = Location().connect(start_area, OR(FLIPPERS, r.bush), id="am")
        witch_hut = Location().connect(Location().add(Witch()), TOADSTOOL, id="an")
        self._addEntrance("witch", witch_hut_area, witch_hut, None)
        witch_hut_area.connect(Location().add(Seashell(0x5D)), COUNT(POWER_BRACELET, 2), id="ao")

        to_zora_domain = Location().connect(witch_hut_area, POWER_BRACELET, id="ap")
        self._addEntrance("d4", to_zora_domain, None, None)

        multichest_cave = Location()
        multichest_cave_secret = Location().connect(multichest_cave, None, id="aq", one_way=True) # bomb walls are one-way
        multichest_cave.connect(multichest_cave_secret, BOMB, id="ar", one_way=True)
        multichest_outside = Location().add(HeartPiece(0x25))
        mountain_left = Location()
        self._addEntrance("multichest_left", start_area, multichest_cave, POWER_BRACELET)
        self._addEntrance("multichest_right", mountain_left, multichest_cave, None)
        self._addEntrance("multichest_top", multichest_outside, multichest_cave_secret, None)

        forest_madbatter = Location()
        Location().add(MadBatter(0x1E1)).connect(forest_madbatter, MAGIC_POWDER, id="as")
        self._addEntrance("forest_madbatter", mountain_left, forest_madbatter, None)

        prairie_left_cave2 = Location()  # Bomb cave
        Location().add(Chest(0x2F4)).connect(prairie_left_cave2, PEGASUS_BOOTS, id="at")
        Location().add(HeartPiece(0x2E5)).connect(prairie_left_cave2, AND(BOMB, PEGASUS_BOOTS), id="au")
        self._addEntrance("prairie_left_cave2", mountain_left, prairie_left_cave2, None)
        self._addEntrance("castle_jump_cave", mountain_left, Location().add(Chest(0x1FD)), None)

        mamu = Location().connect(Location().add(Song(0x2FB)), AND(OCARINA, COUNT("RUPEES", 300)), id="av")
        self._addEntrance("mamu", mountain_left, mamu, None)

        mountain_right = Location().connect(mountain_left, OR(HOOKSHOT, AND(FEATHER, PEGASUS_BOOTS)), id="aw")
        writes_cave = Location()
        writes_cave_left_chest = Location().add(Chest(0x2AE)).connect(writes_cave, OR(FEATHER, AND(ROOSTER, POWER_BRACELET), HOOKSHOT), id="ax") # 1st chest in the cave behind the hut
        Location().add(Chest(0x2AF)).connect(writes_cave, POWER_BRACELET, id="ay")  # 2nd chest in the cave behind the hut.
        self._addEntrance("writes_cave_left", mountain_right, writes_cave, None)
        self._addEntrance("writes_cave_right", mountain_right, writes_cave, None)

        mountain_top_right = Location()

        prairie_cave = Location()
        prairie_cave_secret_exit = Location().connect(prairie_cave, OR(FEATHER, AND(ROOSTER, POWER_BRACELET)), id="az", one_way=True)
        prairie_cave.connect(prairie_cave_secret_exit, AND(BOMB, OR(FEATHER, AND(ROOSTER, POWER_BRACELET))), id="b0", one_way=True) # bomb walls are one-way
        self._addEntrance("prairie_right_cave_top", Location(), prairie_cave, None)
        self._addEntrance("prairie_right_cave_bottom", mountain_right, prairie_cave, None)
        self._addEntrance("prairie_right_cave_high", mountain_right, prairie_cave_secret_exit, None)

        papahl_cave = Location().add(Chest(0x28A))
        self._addEntrance("papahl_entrance", mountain_right, papahl_cave, None)
        self._addEntrance("papahl_exit", mountain_top_right, papahl_cave, None)

        animal_village_bombcave = Location()
        self._addEntrance("animal_cave", mountain_top_right, animal_village_bombcave, BOMB)
        animal_village_bombcave_heartpiece = Location().add(HeartPiece(0x2E6)).connect(animal_village_bombcave, OR(AND(BOMB, FEATHER, HOOKSHOT), ROOSTER), id="b1")  # cave in the upper right of animal town
        self._addEntrance("d3", mountain_top_right, None, AND(COUNT(POWER_BRACELET, 2), HAMMER))

        left_right_connector_cave_entrance = Location()
        left_right_connector_cave_exit = Location()
        left_right_connector_cave_entrance.connect(left_right_connector_cave_exit, OR(HOOKSHOT, AND(ROOSTER, POWER_BRACELET)), id="b2", one_way=True)  # pass through the underground passage to left side
        self._addEntrance("left_to_right_taltalentrance", mountain_top_right, left_right_connector_cave_entrance, None)
        self._addEntrance("left_taltal_entrance", mountain_left, left_right_connector_cave_exit, None)
        mountain_heartpiece = Location().add(HeartPiece(0x2BA)) # heartpiece in connecting cave
        left_right_connector_cave_entrance.connect(mountain_heartpiece, BOMB, id="b3", one_way=True)  # in the connecting cave from right to left. one_way to prevent access to left_side_mountain via glitched logic

        self._addEntrance("d7", mountain_top_right, None, HAMMER)

        self.start = start_house
        self.egg = castle_top_outside
        self.nightmare = nightmare
        self.windfish = windfish

    def _addEntrance(self, name, outside, inside, requirement):
        assert name not in self.entrances, "Duplicate entrance: %s" % name
        assert name in worldSetup.ENTRANCE_INFO
        self.entrances[name] = EntranceExterior(outside, requirement, id=name)
        self.entrances[f"{name}:inside"] = EntranceExterior(inside, None, id=name)

    def _addEntranceRequirement(self, name, requirement, id=None):
        assert name in self.entrances
        self.entrances[name].addRequirement(requirement, id)

    def _addEntranceRequirementEnter(self, name, requirement, id=None):
        assert name in self.entrances
        self.entrances[name].addEnterRequirement(requirement, id)

    def _addEntranceRequirementExit(self, name, requirement, id=None):
        assert name in self.entrances
        self.entrances[name].addExitRequirement(requirement, id)

    def updateIndoorLocation(self, name, location):
        name = f"{name}:inside"
        assert name in self.entrances, name
        assert self.entrances[name].location is None
        self.entrances[name].location = location


class EntranceExterior:
    def __init__(self, outside, requirement, one_way_enter_requirement="UNSET", one_way_exit_requirement="UNSET", id=None, enter_id=None, exit_id=None):
        self.location = outside
        self.requirement = requirement
        self.one_way_enter_requirement = one_way_enter_requirement
        self.one_way_exit_requirement = one_way_exit_requirement
        self.enter_id = enter_id
        self.exit_id = exit_id
        self.id = id
    
    def addRequirement(self, new_requirement, id=None):
        self.requirement = OR(self.requirement, new_requirement)

        if id:
            self.id = id

    def addExitRequirement(self, new_requirement, id=None):
        if self.one_way_exit_requirement == "UNSET":
            self.one_way_exit_requirement = new_requirement
        else:
            self.one_way_exit_requirement = OR(self.one_way_exit_requirement, new_requirement)

        if id:
            self.exit_id = id

    def addEnterRequirement(self, new_requirement, id=None):
        if self.one_way_enter_requirement == "UNSET":
            self.one_way_enter_requirement = new_requirement
        else:
            self.one_way_enter_requirement = OR(self.one_way_enter_requirement, new_requirement)

        if id:
            self.enter_id = id
    
    def enterIsSet(self):
        return self.one_way_enter_requirement != "UNSET"
    
    def exitIsSet(self):
        return self.one_way_exit_requirement != "UNSET"
