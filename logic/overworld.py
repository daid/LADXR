from .requirements import *
from .location import Location
from locations import *


class World:
    def __init__(self, options):
        start = Location().add(StartItem())
        Location().add(ShopItem(2)).connect(start, COUNT("RUPEES", 10))
        Location().add(ShopItem(0)).connect(start, COUNT("RUPEES", 200))
        Location().add(ShopItem(1)).connect(start, COUNT("RUPEES", 980))
        dream_hut = Location().add(Chest(0x2BF)).connect(start, AND(POWER_BRACELET, OR(SWORD, BOOMERANG, HOOKSHOT, FEATHER)))
        dream_hut2 = Location().add(Chest(0x2BE)).connect(dream_hut, PEGASUS_BOOTS)
        Location().add(HeartPiece(0x2A4)).connect(start, bush)  # well
        # Location().add(HeartPiece(0x2B1)).connect(start, AND(bush, COUNT("RUPEES", 20)))  # fishing game, hearth piece is directly done by the minigame.
        Location().add(Seashell(0x0A3)).connect(start, bush)  # bushes below the shop
        Location().add(Seashell(0x2B2)).connect(start, SHOVEL)  # in the kennel
        Location().add(Seashell(0x0D2)).connect(start, PEGASUS_BOOTS)  # smash into tree next to lv1
        Location().add(Song(0x092)).connect(start, OCARINA)  # Marins song

        sword_beach = Location().add(BeachSword()).connect(start, OR(bush, SHIELD, attack_hookshot))
        if options.boomerang == 'trade':
            Location().add(BoomerangGuy()).connect(sword_beach, AND(BOMB, OR(BOOMERANG, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS, FEATHER, SHOVEL)))
        elif options.boomerang == 'gift':
            Location().add(BoomerangGuy()).connect(sword_beach, BOMB)
        sword_beach_to_ghost_hut = Location().add(Chest(0x0E5)).connect(sword_beach, POWER_BRACELET)
        ghost_hut = Location().connect(sword_beach_to_ghost_hut, POWER_BRACELET) 
        Location().add(Seashell(0x1E3)).connect(ghost_hut, POWER_BRACELET)

        forest = Location().add(Toadstool()).connect(start, bush)  # forest stretches all the way from the start town to the witch hut
        forest_heartpiece = Location().add(HeartPiece(0x044)).connect(forest, OR(BOOMERANG, FEATHER, HOOKSHOT))  # next to the forest, surrounded by pits
        Location().add(Witch()).connect(forest, TOADSTOOL)
        Location().add(Chest(0x071)).connect(forest, POWER_BRACELET) #chest at start forest with 2 zols
        Location().add(MadBatter(0x1E1)).connect(forest, AND(POWER_BRACELET, MAGIC_POWDER))
        swamp = Location().connect(forest, OR(MAGIC_POWDER, FEATHER, POWER_BRACELET))
        swamp_chest = Location().add(Chest(0x034)).connect(swamp, OR(BOWWOW, HOOKSHOT, MAGIC_ROD, BOOMERANG))
        dungeon2_entrance = Location().connect(swamp, OR(BOWWOW, HOOKSHOT, MAGIC_ROD, BOOMERANG))
        forest_rear_chest = Location().add(Chest(0x041)).connect(swamp, bush)  # tail key
        Location().add(Chest(0x2BD)).connect(forest, SWORD)  # chest in forest cave on route to mushroom
        log_cave_heartpiece = Location().add(HeartPiece(0x2AB)).connect(forest, POWER_BRACELET)  # piece of heart in the forest cave on route to the mushroom
        hookshot_cave = Location().add(Chest(0x2B3)).connect(forest, AND(POWER_BRACELET, HOOKSHOT))

        writes_hut = Location().connect(swamp, FEATHER)  # includes the cave behind the hut
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            writes_hut.add(OwlStatue(0x11))
        writes_cave_left_chest = Location().add(Chest(0x2AE)).connect(writes_hut, OR(FEATHER, HOOKSHOT)) # 1st chest in the cave behind the hut
        Location().add(Chest(0x2AF)).connect(writes_hut, POWER_BRACELET)  # 2nd chest in the cave behind the hut.

        graveyard = Location().connect(forest, OR(FEATHER, POWER_BRACELET))  # whole area from the graveyard up to the moblin cave
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            graveyard.add(OwlStatue(0x035))
        graveyard_heartpiece = Location().add(HeartPiece(0x2DF)).connect(graveyard, AND(BOMB, OR(HOOKSHOT, PEGASUS_BOOTS), FEATHER))  # grave cave
        Location().add(Seashell(0x074)).connect(graveyard, AND(POWER_BRACELET, SHOVEL))  # next to grave cave, digging spot
        Location().add(Chest(0x2E2)).connect(graveyard, SWORD)  # moblin cave, boss requires sword, contains Bowwow

        # "Ukuku Prairie"
        # The center_area is the whole area right of the start town, up to the river, and the castle.
        # Dungeon 3 and 5 are accessed from here
        center_area = Location().connect(start, POWER_BRACELET)
        center_area.connect(graveyard, POWER_BRACELET)
        center_area.add(Chest(0x2CD))  # cave next to town
        mamu = Location().add(Song(0x2FB)).connect(center_area, AND(FEATHER, PEGASUS_BOOTS, HOOKSHOT, POWER_BRACELET, OCARINA))
        Location().add(Chest(0x2F4), HeartPiece(0x2E5)).connect(center_area, AND(BOMB, PEGASUS_BOOTS))  # cave near honeycomb
        dungeon3_entrance = Location().connect(center_area, OR(FEATHER, FLIPPERS)) 
        Location().add(Seashell(0x0A5)).connect(dungeon3_entrance, SHOVEL)  # above lv3
        prairie_island_seashell = Location().add(Seashell(0x0A6)).connect(center_area, AND(FLIPPERS, bush))  # next to lv3
        Location().add(Seashell(0x08B)).connect(center_area, bush)  # next to seashell house
        Location().add(Seashell(0x0A4)).connect(center_area, PEGASUS_BOOTS)  # smash into tree next to phonehouse
        prairie_3gap_stairs = Location().add(Chest(0x1FD)).connect(center_area, AND(FEATHER, PEGASUS_BOOTS))  # left of the castle, 5 holes turned into 3
        Location().add(Seashell(0x0B9)).connect(center_area, POWER_BRACELET)  # under the rock
        Location().add(Seashell(0x0E9)).connect(center_area, bush)  # same screen as mermaid statue
        tiny_island = Location().add(Seashell(0x0F8)).connect(center_area, AND(FLIPPERS, bush))  # tiny island
        prairie_plateau = Location().connect(center_area, AND(BOMB, FEATHER))  # prairie plateau at the owl statue
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            prairie_plateau.add(OwlStatue(0x0A8))
        Location().add(Seashell(0x0A8)).connect(prairie_plateau, SHOVEL)  # at the owl statue
        Location().add(MadBatter(0x1E0)).connect(center_area, AND(FEATHER, OR(SWORD, MAGIC_ROD, BOOMERANG), FLIPPERS, MAGIC_POWDER))  # you can use powder instead of sword/magic-rod to clear the bushes, but it is a bit of an advanced action
        Location().add(SeashellMansion(0x2E9)).connect(center_area, COUNT(SEASHELL, 20))
        
        dungeon5_entrance = Location().connect(center_area, FLIPPERS)
        
        # Richard
        richard_cave = Location().connect(center_area, COUNT(GOLD_LEAF, 5))
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            Location().add(OwlStatue(0x0C6)).connect(richard_cave, bush)
        Location().add(SlimeKey()).connect(richard_cave, AND(bush, SHOVEL))
        richard_cave_chest = Location().add(Chest(0x2C8)).connect(richard_cave, OR(FEATHER, HOOKSHOT))

        castle = Location().connect(center_area, AND(FEATHER, OR(BOMB, BOOMERANG, MAGIC_POWDER, MAGIC_ROD, SWORD)))  # assumes the bridge is build. Passage blocked by bush
        Location().add(HeartPiece(0x078)).connect(center_area, FLIPPERS)  # in the moat of the castle
        castle_inside = Location().connect(castle, bush)
        Location().add(GoldLeaf(0x05A)).connect(castle, OR(SWORD, BOW, MAGIC_ROD))  # mad bomber, enemy hiding in the 6 holes
        Location().add(GoldLeaf(0x058)).connect(castle, AND(POWER_BRACELET, attack_hookshot_powder))  # bird on tree, can kill with second rock
        Location().add(GoldLeaf(0x2D2)).connect(castle_inside, attack_hookshot_powder)  # in the castle, kill enemies
        Location().add(GoldLeaf(0x2C5)).connect(castle_inside, AND(BOMB, attack_hookshot_powder))  # in the castle, bomb wall to show enemy
        Location().add(GoldLeaf(0x2C6)).connect(castle_inside, OR(BOOMERANG, AND(POWER_BRACELET, attack_hookshot)))  # in the castle, spinning spikeball enemy

        animal_town = Location().connect(center_area, OR(FLIPPERS, HOOKSHOT, AND(PEGASUS_BOOTS, OR(BOMB, BOOMERANG, MAGIC_POWDER, MAGIC_ROD, SWORD)))) # passage under river blocked by bush
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            animal_town.add(OwlStatue(0x0DA))
        Location().add(Seashell(0x0DA)).connect(animal_town, SHOVEL)  # owl statue at the water
        desert = Location().connect(animal_town, bush)  # Note: We removed the walrus blocking the desert.
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            desert.add(OwlStatue(0x0CF))
        Location().add(AnglerKey()).connect(desert, OR(BOW, SWORD, HOOKSHOT, MAGIC_ROD, BOOMERANG))
        animal_town_bombcave = Location().add(HeartPiece(0x2E6)).connect(desert, AND(BOMB, FEATHER, HOOKSHOT))  # cave in the upper right of animal town
        Location().add(HeartPiece(0x1E8)).connect(desert, BOMB)  # above the quicksand cave
        Location().add(Seashell(0x0FF)).connect(desert, POWER_BRACELET)

        # Area below the windfish egg
        below_mountains = Location().connect(graveyard, POWER_BRACELET)
        into_to_mountains = Location().add(Chest(0x018)).connect(below_mountains, AND(POWER_BRACELET, SWORD)) # chest outside obstacle cave
        obstacle_cave_chest = Location().add(Chest(0x2BB)).connect(into_to_mountains, HOOKSHOT) # chest at obstacles
        right_mountains_1 = Location().add(Chest(0x28A)).connect(into_to_mountains, PEGASUS_BOOTS) # chest in passage to papahl
        Location().add(HeartPiece(0x1F2)).connect(below_mountains, FLIPPERS)  # cave next to level 4
        dungeon4_entrance = Location().connect(below_mountains, FLIPPERS) # swim
        dungeon4_entrance.connect(right_mountains_1, ANGLER_KEY) # go around right_mountains_1, "needs" angler key to unlock ledge
        Location().add(Song(0x2FD)).connect(below_mountains, AND(OCARINA, FLIPPERS))  # Manbo's Mambo

        face_shrine = Location().add(Chest(0x2FC)).connect(animal_town, AND(bush, POWER_BRACELET))
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            face_shrine.add(OwlStatue(0x08F))
        Location().add(FaceKey()).connect(face_shrine, OR(BOW, MAGIC_ROD, SWORD))

        dungeon6_entrance = Location().connect(animal_town, AND(FLIPPERS, HOOKSHOT))

        # Raft game.
        raft_game = Location().add(Chest(0x05C), Chest(0x05D))
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            raft_game.add(OwlStatue(0x5D))
        raft_game.connect(below_mountains, OR(FLIPPERS, HOOKSHOT)) # flippers from d6 water area to one way cave. Flippers guarantee way back
        raft_game.connect(center_area, FLIPPERS)

        right_mountains_2 = Location().connect(right_mountains_1, FLIPPERS) # towards d7
        luigi_rooster_house = Location().connect(right_mountains_1, FLIPPERS) # up the ladder
        if options.owlstatues == "both" or options.owlstatues == "overworld":
            right_mountains_2.add(OwlStatue(0x1E)) # owl statue below d7
        bridge_seashell = Location().add(Seashell(0x00C)).connect(luigi_rooster_house, AND(FEATHER, POWER_BRACELET)) # seashell right of rooster house, there is a hole in the bridge
        bird_key = Location().add(BirdKey()).connect(luigi_rooster_house, COUNT(POWER_BRACELET, 2)) # assumes rooster to cross the pits before the statue?
        # MultiChest is causing issues with the sanity checker when keysanity is disabled, so disabled it for now.
        # Location().add(MultiChest(0x2F2), Chest(0x01D)).connect(right_mountains_2, BOMB)  # the multi-chest puzzle.
        Location().add(Chest(0x01D)).connect(right_mountains_2, BOMB)  # chest after multichest puzzle outside
        right_mountains_3 = Location().connect(right_mountains_2, AND(FEATHER, HOOKSHOT)) # d7 area

        mountain_bridge_staircase = Location().connect(luigi_rooster_house, AND(HOOKSHOT, OR(BOMB, BOOMERANG, MAGIC_POWDER, MAGIC_ROD, SWORD))) # cross bridges to staircase
        mountain_heartpiece = Location().add(HeartPiece(0x2BA)) # heartpiece in connecting cave
        mountain_bridge_staircase.connect(mountain_heartpiece, BOMB, one_way=True)  # in the connecting cave from right to left. one_way to prevent access to left_side_mountain via glitched logic
        left_side_mountain = Location().connect(mountain_bridge_staircase, HOOKSHOT) # pass through the underground passage to left side
        left_side_mountain.add(Chest(0x004)) # top of falling rocks hill
        Location().add(MadBatter(0x1E2)).connect(left_side_mountain, AND(POWER_BRACELET, MAGIC_POWDER))
        dungeon8_phone = Location().connect(left_side_mountain, AND(BOMB, COUNT(SHIELD, 2)))
        dungeon8_entrance = Location().connect(dungeon8_phone, AND(OCARINA, SONG3, SWORD))

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            dream_hut.connect(start, HOOKSHOT) # clip past the rocks in front of dream hut
            hookshot_cave.connect(forest, HOOKSHOT) # clip past the rocks in front of log cave
            hookshot_cave.connect(forest, AND(POWER_BRACELET, FEATHER, PEGASUS_BOOTS)) # boots jump the gap to the chest
            swamp_chest.connect(swamp, bush) # added bush requirement since a requirement is necessary
            dungeon2_entrance.connect(swamp, POWER_BRACELET) # clip the top wall to walk between the goponga flower and the wall
            writes_hut.connect(swamp, HOOKSHOT) # hookshot the sign in front of writes hut
            graveyard_heartpiece.connect(graveyard, FEATHER) # jump to the bottom right tile around the blocks
            graveyard_heartpiece.connect(graveyard, OR(HOOKSHOT, BOOMERANG)) # push bottom block, wall clip and hookshot/boomerang corner to grab item
            animal_town_bombcave.connect(desert, AND(BOMB, PEGASUS_BOOTS, FEATHER)) # jump across horizontal 4 gap to heart piece
            dungeon6_entrance.connect(animal_town, AND(FLIPPERS, FEATHER)) # jump the gap in underground passage to d6
            dungeon8_phone.connect(left_side_mountain, AND(BOMB, PEGASUS_BOOTS)) # flame skip
        
        if options.logic == 'glitched' or options.logic == 'hell':
            #dream_hut.connect(start, FEATHER) # flock clip TODO: require nag messages
            dream_hut2.connect(dream_hut, FEATHER)  # super jump
            forest.connect(swamp, BOMB)  # bomb trigger tarin
            forest_heartpiece.connect(forest, BOMB) # bomb trigger heartpiece
            forest_heartpiece.connect(graveyard, bush) # villa buffer from top. added bush requirement since a requirement is necessary
            log_cave_heartpiece.connect(forest, FEATHER) # super jump
            log_cave_heartpiece.connect(forest, BOMB) # bomb trigger
            graveyard_heartpiece.connect(graveyard, bush) # sideways block push. added bush requirement since a requirement is necessary
            prairie_island_seashell.connect(center_area, AND(FEATHER, bush)) # jesus jump from right side
            prairie_3gap_stairs.connect(center_area, FEATHER) # 1 pit buffer to clip bottom wall and jump across
            tiny_island.connect(center_area, AND(FEATHER, bush)) # jesus jump around
            richard_cave.connect(center_area, OR(BOMB, BOOMERANG, MAGIC_POWDER, MAGIC_ROD, SWORD)) # break bushes on north side of the maze, and 1 pit buffer into the maze
            animal_town.connect(center_area, FEATHER) # jesus jump
            animal_town_bombcave.connect(desert, AND(BOMB, OR(HOOKSHOT, FEATHER, PEGASUS_BOOTS))) # bomb trigger from right side, corner walking top right pit is stupid so hookshot or boots added
            center_area.connect(dungeon6_entrance, FEATHER, one_way=True) # jesus jump (3 screen)
            face_shrine.connect(raft_game, FEATHER, one_way=True) # jesus jump (2-ish screen)
            obstacle_cave_chest.connect(into_to_mountains, FEATHER) # jump to the rightmost pits + 1 pit buffer to jump across
            right_mountains_1.connect(into_to_mountains, FEATHER) #  1 pit buffer above boots crytals to get past
            right_mountains_2.connect(right_mountains_1, FEATHER) # jesus jump (1 or 2 screen)
            luigi_rooster_house.connect(right_mountains_1, FEATHER) # jesus jump (1 or 2 screen)
            mountain_bridge_staircase.connect(luigi_rooster_house, AND(PEGASUS_BOOTS, FEATHER, OR(BOMB, BOOMERANG, MAGIC_POWDER, MAGIC_ROD, SWORD))) # cross bridge to staircase with pit buffer to clip bottom wall and jump across
            bird_key.connect(luigi_rooster_house, AND(FEATHER, HOOKSHOT)) # hookshot jump across the big pits room
            right_mountains_3.connect(right_mountains_2, bush) # 2 seperate pit buffers so not obnoxious to get past the two pit rooms before d7 area. 2nd pits can pit buffer on top right screen, bottom wall to scroll on top of the wall on bottom screen
            into_to_mountains.connect(mountain_heartpiece, BOMB, one_way=True) # bomb trigger from boots crystal cave
            dungeon8_entrance.connect(dungeon8_phone, OR(BOMB, OCARINA)) # bomb trigger the head and walk trough, or play the ocarina song 3 and walk through
            
        if options.logic == 'hell':
            swamp.connect(forest, bush) # damage boost from toadstool area across the pit. added bush requirement since a requirement is necessary
            forest_heartpiece.connect(forest, PEGASUS_BOOTS) # boots bonk across the pits
            log_cave_heartpiece.connect(forest, BOOMERANG) # clip the boomerang through the corner gaps on top right to grab the item
            writes_hut.connect(swamp, PEGASUS_BOOTS) # boots bonk telephone booth
            writes_cave_left_chest.connect(writes_hut, bush) # damage boost off the zol to get across the pit. added bush since a requirement is necessary
            graveyard.connect(forest, OR(PEGASUS_BOOTS, HOOKSHOT)) # boots bonk witches hut, or hookshot spam across the pit
            dungeon3_entrance.connect(center_area, PEGASUS_BOOTS) # boots bonk + water buffer across bottom wall all the way to the entrance 
            prairie_3gap_stairs.connect(center_area, PEGASUS_BOOTS) # pit buffer to clip bottom wall and boots bonk across
            prairie_plateau.connect(center_area, AND(BOMB, OR(PEGASUS_BOOTS, HOOKSHOT))) # boots bonk across pits, or hookshot spam
            dungeon5_entrance.connect(center_area, FEATHER) # jesus jump into d5 entrance (wall clip or fast fall), wall clip to get out
            richard_cave_chest.connect(richard_cave, PEGASUS_BOOTS) # boots bonk
            #castle.connect(center_area, AND(PEGASUS_BOOTS, MEDICINE, OR(BOMB, BOOMERANG, MAGIC_POWDER, MAGIC_ROD, SWORD))) # medicine iframe abuse to get across spikes
            into_to_mountains.connect(below_mountains, OR(HOOKSHOT, AND(FEATHER, PEGASUS_BOOTS, OR(SWORD, MAGIC_ROD, BOW)))) # get past crystal rocks by hookshotting into top pushable block, or boots dashing into top wall where the pushable block is
            face_shrine.connect(dungeon6_entrance, PEGASUS_BOOTS, one_way=True) # jesus jump from top to island with quick falling on top, boots bonk across water and pits
            bridge_seashell.connect(right_mountains_2, AND(PEGASUS_BOOTS, POWER_BRACELET)) # boots bonk
            bird_key.connect(luigi_rooster_house, AND(FEATHER, PEGASUS_BOOTS)) # boots jump above wall, use multiple pit buffers to get across
            mountain_bridge_staircase.connect(luigi_rooster_house, AND(OR(PEGASUS_BOOTS, FEATHER), OR(BOMB, BOOMERANG, MAGIC_POWDER, MAGIC_ROD, SWORD))) # cross bridge to staircase with pit buffer to clip bottom wall and jump or boots bonk across
            #right_mountains_2.connect(right_mountains_1, AND(ANGLER_KEY, PEGASUS_BOOTS)) # boots bonk across bottom wall, dodge waterfalls because of LADXR hacks
            left_side_mountain.connect(mountain_bridge_staircase, AND(PEGASUS_BOOTS, FEATHER)) # boots jump to bottom left corner of pits, pit buffer and jump to left
            
        self.start = start
        self.dungeon2_entrance = dungeon2_entrance
        self.graveyard = graveyard
        self.center_area = center_area
        self.dungeon3_entrance = dungeon3_entrance
        self.right_mountains_1 = right_mountains_1
        self.dungeon4_entrance = dungeon4_entrance
        self.dungeon5_entrance = dungeon5_entrance
        self.dungeon6_entrance = dungeon6_entrance
        self.right_mountains_3 = right_mountains_3
        self.dungeon8_entrance = dungeon8_entrance
