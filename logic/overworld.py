from .requirements import *
from .location import Location
from locations import *


class World:
    def __init__(self):
        start = Location().add(StartItem())
        Location().add(ShopItem(2)).connect(start, COUNT("RUPEES", 10))
        Location().add(ShopItem(0)).connect(start, COUNT("RUPEES", 200))
        Location().add(ShopItem(1)).connect(start, COUNT("RUPEES", 980))
        dream_hut = Location().add(Chest(0x2BF)).connect(start, AND(POWER_BRACELET, OR(SWORD, MAGIC_ROD, FEATHER)))
        Location().add(Chest(0x2BE)).connect(dream_hut, PEGASUS_BOOTS)
        Location().add(HeartPiece(0x2A4)).connect(start, bush)  # well
        # Location().add(HeartPiece(0x2B1)).connect(start, bush)  # fishing game, hearth piece is directly done by the minigame.
        Location().add(Seashell(0x0A3)).connect(start, bush)  # bushes below the shop
        Location().add(Seashell(0x2B2)).connect(start, SHOVEL)  # in the kennel
        Location().add(Seashell(0x0D2)).connect(start, PEGASUS_BOOTS)  # smash into tree next to lv1

        sword_beach = Location().add(BeachSword()).connect(start, bush, SHIELD)
        Location().add(BoomerangGuy()).connect(sword_beach, AND(BOMB, OR(BOOMERANG, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS, FEATHER, SHOVEL)))
        sword_beach_to_ghost_hut = Location().add(Chest(0x0E5))
        sword_beach_to_ghost_hut.connect(sword_beach, POWER_BRACELET)
        ghost_hut = Location()
        ghost_hut.connect(sword_beach_to_ghost_hut, POWER_BRACELET)
        Location().add(Seashell(0x1E3)).connect(ghost_hut, POWER_BRACELET)

        forest = Location().add(Toadstool()).connect(start, bush)  # forest stretches all the way from the start town to the witch hut
        Location().add(HeartPiece(0x044)).connect(forest, FEATHER)  # next to the forest, surrounded by pits
        Location().add(Witch()).connect(forest, "TOADSTOOL")
        Location().add(Chest(0x071)).connect(forest, POWER_BRACELET)
        swamp = Location().connect(forest, MAGIC_POWDER, FEATHER)
        Location().add(Chest(0x034)).connect(swamp, BOWWOW, HOOKSHOT, MAGIC_ROD)
        forest_rear_chest = Location().add(Chest(0x041)).connect(swamp, bush)
        Location().add(Chest(0x2BD)).connect(forest, SWORD)  # chest in forest cave on route to mushroom
        Location().add(HeartPiece(0x2AB)).connect(forest, POWER_BRACELET)  # piece of heart in the forst cave on route to the mushroom
        Location().add(Chest(0x2B3)).connect(forest, AND(POWER_BRACELET, HOOKSHOT))  # hookshot cave

        writes_hut = Location().add(Chest(0x2AE)).connect(swamp, FEATHER)  # includes the cave behind the hut
        Location().add(Chest(0x2AF)).connect(writes_hut, POWER_BRACELET)  # 2nd chest in the cave behind the hut.

        graveyard = Location().connect(forest, FEATHER, POWER_BRACELET)  # whole area from the graveyard up to the moblin cave
        graveyard.connect(swamp, POWER_BRACELET)
        Location().add(HeartPiece(0x2DF)).connect(graveyard, AND(BOMB, HOOKSHOT, FEATHER))  # grave cave
        Location().add(Seashell(0x074)).connect(graveyard, POWER_BRACELET)  # next to grave cave
        Location().add(Chest(0x2E2)).connect(graveyard, SWORD)  # moblin cave, boss requires sword, contains Bowwow

        # "Ukuku Prairie"
        # The center_area is the whole area right of the start town, up to the river, and the castle.
        # Dungeon 3 and 5 are accessed from here
        center_area = Location().connect(start, AND(bush, POWER_BRACELET)).connect(graveyard, POWER_BRACELET)
        center_area.connect(ghost_hut, AND(FEATHER, PEGASUS_BOOTS))
        center_area.add(Chest(0x2CD))  # cave next to town
        Location().add(Chest(0x2F4), HeartPiece(0x2E5)).connect(center_area, AND(BOMB, PEGASUS_BOOTS))  # cave near honeycomb
        Location().add(Seashell(0x0A5)).connect(center_area, AND(OR(FEATHER, FLIPPERS), SHOVEL))  # above lv3
        Location().add(Seashell(0x0A6)).connect(center_area, FLIPPERS)  # next to lv3
        Location().add(Seashell(0x08B)).connect(center_area, bush)  # next to seashell house
        Location().add(Seashell(0x0A4)).connect(center_area, PEGASUS_BOOTS)  # smash into tree next to phonehouse
        Location().add(Chest(0x1FD)).connect(center_area, AND(FEATHER, PEGASUS_BOOTS))  # left of the castle, 5 holes turned into 3
        Location().add(Seashell(0x0B9)).connect(center_area, POWER_BRACELET)  # under the rock
        Location().add(Seashell(0x0E9)).connect(center_area, bush)  # same screen as mermaid statue
        Location().add(Seashell(0x0F8)).connect(center_area, AND(FLIPPERS, bush))  # tiny island
        Location().add(Seashell(0x0A8)).connect(center_area, AND(BOMB, FEATHER, SHOVEL))  # at the owl statue

        # Richard
        richard_cave = Location().connect(center_area, COUNT(GOLD_LEAF, 5))
        Location().add(SlimeKey()).connect(richard_cave, AND(bush, SHOVEL))
        Location().add(Chest(0x2C8)).connect(richard_cave, FEATHER)

        castle = Location().connect(center_area, FEATHER)  # assumes the bridge is build.
        Location().add(HeartPiece(0x078)).connect(castle, FLIPPERS)  # in the moat of the castle
        castle_inside = Location().connect(castle, bush)
        Location().add(GoldLeaf(0x05A)).connect(castle, attack)  # enemy hiding in the 6 holes
        Location().add(GoldLeaf(0x058)).connect(castle, AND(POWER_BRACELET, attack_no_bomb))  # bird on tree
        Location().add(GoldLeaf(0x2D2)).connect(castle_inside, attack)  # in the castle, kill enemies
        Location().add(GoldLeaf(0x2C5)).connect(castle_inside, AND(BOMB, attack))  # in the castle, bomb wall to show enemy
        Location().add(GoldLeaf(0x2C6)).connect(castle_inside, AND(POWER_BRACELET, attack))  # in the castle, spinning spikeball enemy

        animal_town = Location().connect(center_area, FLIPPERS, PEGASUS_BOOTS)
        Location().add(Seashell(0x0DA)).connect(animal_town, SHOVEL)  # owl statue at the water
        desert = Location().add(AnglerKey()).connect(animal_town, bush)  # Note: We removed the walrus blocking the desert.
        Location().add(HeartPiece(0x2E6)).connect(desert, AND(BOMB, HOOKSHOT))  # cave in the upper right of animal town
        Location().add(HeartPiece(0x1E8)).connect(desert, BOMB)  # above the quicksand cave
        Location().add(Seashell(0x0FF)).connect(desert, POWER_BRACELET)

        # Area below the windfish egg
        below_mountains = Location().connect(graveyard, POWER_BRACELET)
        into_to_mountains = Location().add(Chest(0x018)).connect(below_mountains, AND(POWER_BRACELET, SWORD))
        Location().add(Chest(0x2BB)).connect(into_to_mountains, HOOKSHOT)
        right_mountains_1 = Location().add(Chest(0x28A)).connect(into_to_mountains, PEGASUS_BOOTS)
        Location().add(HeartPiece(0x1F2)).connect(below_mountains, FLIPPERS)  # cave next to level 4

        face_shrine = Location().add(Chest(0x2FC)).connect(animal_town, AND(bush, POWER_BRACELET))
        Location().add(FaceKey()).connect(face_shrine, OR(BOW, SWORD))

        dungeon6_entrance = Location().connect(animal_town, AND(FLIPPERS, HOOKSHOT))

        # Raft game.
        raft_game = Location().add(Chest(0x05C), Chest(0x05D))
        raft_game.connect(below_mountains, HOOKSHOT)
        raft_game.connect(center_area, AND(FLIPPERS, HOOKSHOT))


        right_mountains_2 = Location().connect(right_mountains_1, FLIPPERS)
        Location().add(Seashell(0x00C)).connect(right_mountains_2, POWER_BRACELET)
        Location().add(BirdKey()).connect(right_mountains_2, COUNT(POWER_BRACELET, 2))
        Location().add(Chest(0x01D)).connect(right_mountains_2, BOMB)  # Chest(0x2F2) is also here, but that is the multi-chest puzzle.
        right_mountains_3 = Location().connect(right_mountains_2, AND(FEATHER, HOOKSHOT))

        left_side_mountain = Location().connect(right_mountains_2, AND(HOOKSHOT, OR(SWORD, MAGIC_ROD, BOMB, MAGIC_POWDER)))
        left_side_mountain.add(Chest(0x004))
        Location().add(HeartPiece(0x2BA)).connect(left_side_mountain, BOMB)  # in the connecting cave from right to left

        self.start = start
        self.swamp = swamp
        self.graveyard = graveyard
        self.center_area = center_area
        self.right_mountains_1 = right_mountains_1
        self.dungeon6_entrance = dungeon6_entrance
        self.right_mountains_3 = right_mountains_3
        self.left_side_mountain = left_side_mountain
