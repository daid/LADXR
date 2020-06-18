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
        Location().add(Chest(0x2BE)).connect(dream_hut, PEGASUS_BOOTS)
        Location().add(HeartPiece(0x2A4)).connect(start, bush)  # well
        # Location().add(HeartPiece(0x2B1)).connect(start, AND(bush, COUNT("RUPEES", 20)))  # fishing game, hearth piece is directly done by the minigame.
        Location().add(Seashell(0x0A3)).connect(start, bush)  # bushes below the shop
        Location().add(Seashell(0x2B2)).connect(start, SHOVEL)  # in the kennel
        Location().add(Seashell(0x0D2)).connect(start, PEGASUS_BOOTS)  # smash into tree next to lv1

        sword_beach = Location().add(BeachSword()).connect(start, OR(bush, SHIELD))
        if options.boomerangtrade:
            Location().add(BoomerangGuy()).connect(sword_beach, AND(BOMB, OR(BOOMERANG, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS, FEATHER, SHOVEL)))
        sword_beach_to_ghost_hut = Location().add(Chest(0x0E5))
        sword_beach_to_ghost_hut.connect(sword_beach, POWER_BRACELET)
        ghost_hut = Location()
        ghost_hut.connect(sword_beach_to_ghost_hut, POWER_BRACELET) #ghost_hut is redundant to sword_beach_to_ghost_hut, might as well combine those
        Location().add(Seashell(0x1E3)).connect(ghost_hut, POWER_BRACELET)

        forest = Location().add(Toadstool()).connect(start, bush)  # forest stretches all the way from the start town to the witch hut
        Location().add(HeartPiece(0x044)).connect(forest, OR(BOOMERANG, FEATHER, HOOKSHOT))  # next to the forest, surrounded by pits
        Location().add(Witch()).connect(forest, TOADSTOOL)
        Location().add(Chest(0x071)).connect(forest, POWER_BRACELET) #chest at start forest with 2 zols
        Location().add(MadBatter(0x1E1)).connect(forest, AND(POWER_BRACELET, MAGIC_POWDER))
        swamp = Location().connect(forest, OR(MAGIC_POWDER, FEATHER, POWER_BRACELET))
        Location().add(Chest(0x034)).connect(swamp, OR(BOWWOW, HOOKSHOT, MAGIC_ROD, BOOMERANG))
        forest_rear_chest = Location().add(Chest(0x041)).connect(swamp, bush)
        Location().add(Chest(0x2BD)).connect(forest, SWORD)  # chest in forest cave on route to mushroom
        Location().add(HeartPiece(0x2AB)).connect(forest, POWER_BRACELET)  # piece of heart in the forest cave on route to the mushroom
        Location().add(Chest(0x2B3)).connect(forest, AND(POWER_BRACELET, HOOKSHOT))  # hookshot cave

        writes_hut = Location().add(Chest(0x2AE)).connect(swamp, FEATHER)  # includes the cave behind the hut
        writes_hut.add(OwlStatue(0x11))
        Location().add(Chest(0x2AF)).connect(writes_hut, POWER_BRACELET)  # 2nd chest in the cave behind the hut.

        graveyard = Location().connect(forest, OR(FEATHER, POWER_BRACELET))  # whole area from the graveyard up to the moblin cave
        graveyard.add(OwlStatue(0x035))
        Location().add(HeartPiece(0x2DF)).connect(graveyard, AND(BOMB, OR(HOOKSHOT, PEGASUS_BOOTS), FEATHER))  # grave cave
        Location().add(Seashell(0x074)).connect(graveyard, AND(POWER_BRACELET, SHOVEL))  # next to grave cave, digging spot
        Location().add(Chest(0x2E2)).connect(graveyard, SWORD)  # moblin cave, boss requires sword, contains Bowwow

        # "Ukuku Prairie"
        # The center_area is the whole area right of the start town, up to the river, and the castle.
        # Dungeon 3 and 5 are accessed from here
        center_area = Location().connect(start, POWER_BRACELET)
        center_area.connect(graveyard, POWER_BRACELET)
        center_area.add(Chest(0x2CD))  # cave next to town
        Location().add(Chest(0x2F4), HeartPiece(0x2E5)).connect(center_area, AND(BOMB, PEGASUS_BOOTS))  # cave near honeycomb
        Location().add(Seashell(0x0A5)).connect(center_area, AND(OR(FEATHER, FLIPPERS), SHOVEL))  # above lv3
        Location().add(Seashell(0x0A6)).connect(center_area, AND(FLIPPERS, bush))  # next to lv3
        Location().add(Seashell(0x08B)).connect(center_area, bush)  # next to seashell house
        Location().add(Seashell(0x0A4)).connect(center_area, PEGASUS_BOOTS)  # smash into tree next to phonehouse
        Location().add(Chest(0x1FD)).connect(center_area, AND(FEATHER, PEGASUS_BOOTS))  # left of the castle, 5 holes turned into 3
        Location().add(Seashell(0x0B9)).connect(center_area, POWER_BRACELET)  # under the rock
        Location().add(Seashell(0x0E9)).connect(center_area, bush)  # same screen as mermaid statue
        Location().add(Seashell(0x0F8)).connect(center_area, AND(FLIPPERS, bush))  # tiny island
        Location().add(OwlStatue(0x0A8)).connect(center_area, AND(BOMB, FEATHER))  # at the owl statue
        Location().add(Seashell(0x0A8)).connect(center_area, AND(BOMB, FEATHER, SHOVEL))  # at the owl statue
        Location().add(MadBatter(0x1E0)).connect(center_area, AND(FEATHER, OR(SWORD, MAGIC_ROD, BOOMERANG), FLIPPERS, MAGIC_POWDER))  # you can use powder instead of sword/magic-rod to clear the bushes, but it is a bit of an advanced action

        # Richard
        richard_cave = Location().connect(center_area, COUNT(GOLD_LEAF, 5))
        Location().add(OwlStatue(0x0C6)).connect(richard_cave, bush)
        Location().add(SlimeKey()).connect(richard_cave, AND(bush, SHOVEL))
        Location().add(Chest(0x2C8)).connect(richard_cave, OR(FEATHER, HOOKSHOT))

        castle = Location().connect(center_area, AND(FEATHER, OR(BOMB, BOOMERANG, MAGIC_POWDER, MAGIC_ROD, SWORD)))  # assumes the bridge is build. Passage blocked by bush
        Location().add(HeartPiece(0x078)).connect(center_area, FLIPPERS)  # in the moat of the castle
        castle_inside = Location().connect(castle, bush)
        Location().add(GoldLeaf(0x05A)).connect(castle, OR(SWORD, BOW, MAGIC_ROD))  # mad bomber, enemy hiding in the 6 holes
        Location().add(GoldLeaf(0x058)).connect(castle, AND(POWER_BRACELET, attack_hookshot_powder))  # bird on tree, can kill with second rock
        Location().add(GoldLeaf(0x2D2)).connect(castle_inside, attack_hookshot_powder)  # in the castle, kill enemies
        Location().add(GoldLeaf(0x2C5)).connect(castle_inside, AND(BOMB, attack_hookshot_powder))  # in the castle, bomb wall to show enemy
        Location().add(GoldLeaf(0x2C6)).connect(castle_inside, OR(BOOMERANG, AND(POWER_BRACELET, attack_hookshot)))  # in the castle, spinning spikeball enemy

        animal_town = Location().connect(center_area, OR(FLIPPERS, HOOKSHOT, AND(PEGASUS_BOOTS, OR(BOMB, BOOMERANG, MAGIC_POWDER, MAGIC_ROD, SWORD)))) # passage under river blocked by bush
        animal_town.add(OwlStatue(0x0DA))
        Location().add(Seashell(0x0DA)).connect(animal_town, SHOVEL)  # owl statue at the water
        desert = Location().connect(animal_town, bush)  # Note: We removed the walrus blocking the desert.
        desert.add(OwlStatue(0x0CF))
        Location().add(AnglerKey()).connect(desert, OR(BOW, SWORD, HOOKSHOT, MAGIC_ROD))
        Location().add(HeartPiece(0x2E6)).connect(desert, AND(BOMB, FEATHER, HOOKSHOT))  # cave in the upper right of animal town
        Location().add(HeartPiece(0x1E8)).connect(desert, BOMB)  # above the quicksand cave
        Location().add(Seashell(0x0FF)).connect(desert, POWER_BRACELET)

        # Area below the windfish egg
        below_mountains = Location().connect(graveyard, POWER_BRACELET)
        into_to_mountains = Location().add(Chest(0x018)).connect(below_mountains, AND(POWER_BRACELET, SWORD)) # chest outside obstacle cave
        Location().add(Chest(0x2BB)).connect(into_to_mountains, HOOKSHOT) # chest at obstacles
        right_mountains_1 = Location().add(Chest(0x28A)).connect(into_to_mountains, PEGASUS_BOOTS) # chest in passage to papahl
        Location().add(HeartPiece(0x1F2)).connect(below_mountains, FLIPPERS)  # cave next to level 4

        face_shrine = Location().add(Chest(0x2FC)).connect(animal_town, AND(bush, POWER_BRACELET))
        face_shrine.add(OwlStatue(0x08F))
        Location().add(FaceKey()).connect(face_shrine, OR(BOW, MAGIC_ROD, SWORD))

        dungeon6_entrance = Location().connect(animal_town, AND(FLIPPERS, HOOKSHOT))

        # Raft game.
        raft_game = Location().add(Chest(0x05C), Chest(0x05D))
        raft_game.add(OwlStatue(0x5D))
        raft_game.connect(below_mountains, OR(FLIPPERS, HOOKSHOT)) # flippers from d6 water area to one way cave. Flippers guarantee way back
        raft_game.connect(center_area, FLIPPERS)


        right_mountains_2 = Location().connect(right_mountains_1, FLIPPERS)
        right_mountains_2.add(OwlStatue(0x1E))
        Location().add(Seashell(0x00C)).connect(right_mountains_2, AND(FEATHER, POWER_BRACELET)) # seashell right of rooster house, there is a hole in the bridge
        Location().add(BirdKey()).connect(right_mountains_2, COUNT(POWER_BRACELET, 2))
        # Location().add(MultiChest(0x2F2), Chest(0x01D)).connect(right_mountains_2, BOMB)  # the multi-chest puzzle and chest after it.
        right_mountains_3 = Location().connect(right_mountains_2, AND(FEATHER, HOOKSHOT))

        left_side_mountain = Location().connect(right_mountains_2, AND(HOOKSHOT, OR(BOMB, BOOMERANG, MAGIC_POWDER, MAGIC_ROD, SWORD)))
        left_side_mountain.add(Chest(0x004)) # top of falling rocks hill
        Location().add(MadBatter(0x1E2)).connect(left_side_mountain, AND(POWER_BRACELET, MAGIC_POWDER))
        Location().add(HeartPiece(0x2BA)).connect(left_side_mountain, BOMB)  # in the connecting cave from right to left

        self.start = start
        self.swamp = swamp
        self.graveyard = graveyard
        self.center_area = center_area
        self.right_mountains_1 = right_mountains_1
        self.dungeon6_entrance = dungeon6_entrance
        self.right_mountains_3 = right_mountains_3
        self.left_side_mountain = left_side_mountain
