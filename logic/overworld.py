from .requirements import *

start = Location().add(StartItem())
Location().add(ShopItem(2)).connect(start, COUNT("RUPEES", 10))
Location().add(ShopItem(0)).connect(start, COUNT("RUPEES", 200))
Location().add(ShopItem(1)).connect(start, COUNT("RUPEES", 980))
dream_hut = Location().add(Chest(0x2BF)).connect(start, AND(POWER_BRACELET, OR(SWORD, MAGIC_ROD, FEATHER)))
Location().add(Chest(0x2BE)).connect(dream_hut, PEGASUS_BOOTS)

sword_beach = Location().add(BeachSword()).connect(start, bush, SHIELD)
Location().add(BoomerangGuy()).connect(sword_beach, BOMB)
sword_beach_to_ghost_hut = Location().add(Chest(0x0E5))
sword_beach_to_ghost_hut.connect(sword_beach, POWER_BRACELET)
ghost_hut = Location()
ghost_hut.connect(sword_beach_to_ghost_hut, POWER_BRACELET)

forest = Location().add(Toadstool()).connect(start, bush)  # forest stretches all the way from the start town to the witch hut
Location().add(Witch()).connect(forest, "TOADSTOOL")
Location().add(Chest(0x071)).connect(forest, POWER_BRACELET)
swamp = Location().connect(forest, MAGIC_POWDER, FEATHER)
swamp.add(Chest(0x034)) # Chest in the swamp, assumes no flowers!
forest_rear_chest = Location().add(Chest(0x041)).connect(swamp, bush)
Location().add(Chest(0x2BD)).connect(forest, SWORD)  # chest in forest cave on route to mushroom
Location().add(Chest(0x2B3)).connect(forest, AND(POWER_BRACELET, HOOKSHOT))  # hookshot cave

writes_hut = Location().add(Chest(0x2AE)).connect(swamp, FEATHER)  # includes the cave behind the hut
Location().add(Chest(0x2AF)).connect(writes_hut, POWER_BRACELET)  # 2nd chest in the cave behind the hut.

graveyard = Location().connect(forest, FEATHER, POWER_BRACELET)  # whole area from the graveyard up to the moblin cave
graveyard.connect(swamp, POWER_BRACELET)

# "Ukuku Prairie"
# The center_area is the whole area right of the start town, up to the river, and the castle.
# Dungeon 3 and 5 are accessed from here
center_area = Location().connect(start, AND(bush, POWER_BRACELET)).connect(graveyard, POWER_BRACELET)
center_area.add(Chest(0x2CD))  # cave next to town
Location().add(Chest(0x2F4)).connect(center_area, AND(BOMB, PEGASUS_BOOTS))  # cave near honeycomb

# Richard
richard_cave = Location().connect(center_area, COUNT(GOLD_LEAF, 5))
Location().add(SlimeKey()).connect(richard_cave, AND(bush, SHOVEL))
Location().add(Chest(0x2C8)).connect(richard_cave, FEATHER)

castle = Location().connect(center_area, FEATHER)  # assumes the bridge is build.
castle_inside = Location().connect(castle, bush)
Location().add(GoldLeaf(0x05A)).connect(castle, attack)  # enemy hiding in the 6 holes
Location().add(GoldLeaf(0x058)).connect(castle, AND(POWER_BRACELET, attack_no_bomb))  # bird on tree
Location().add(GoldLeaf(0x2D2)).connect(castle_inside, attack)  # in the castle, kill enemies
Location().add(GoldLeaf(0x2C5)).connect(castle_inside, AND(BOMB, attack))  # in the castle, bomb wall to show enemy
Location().add(GoldLeaf(0x2C6)).connect(castle_inside, AND(POWER_BRACELET, attack))  # in the castle, spinning spikeball enemy

animal_town = Location().connect(center_area, FLIPPERS, PEGASUS_BOOTS)
desert = Location().add(AnglerKey()).connect(animal_town, bush)  # Note: We removed the walrus blocking the desert.

# Area below the windfish egg
below_mountains = Location().connect(graveyard, POWER_BRACELET)
into_to_mountains = Location().add(Chest(0x018)).connect(below_mountains, AND(POWER_BRACELET, SWORD))
Location().add(Chest(0x2BB)).connect(into_to_mountains, HOOKSHOT)
right_mountains_1 = Location().add(Chest(0x28A)).connect(into_to_mountains, PEGASUS_BOOTS)

face_shrine = Location().add(Chest(0x2FC)).connect(animal_town, AND(bush, POWER_BRACELET))
Location().add(FaceKey()).connect(face_shrine, BOW)

dungeon6_entrance = Location().connect(animal_town, AND(FLIPPERS, HOOKSHOT))

# Raft game.
raft_game = Location().add(Chest(0x05C), Chest(0x05D))
raft_game.connect(below_mountains, HOOKSHOT)
raft_game.connect(center_area, AND(FLIPPERS, HOOKSHOT))


right_mountains_2 = Location().connect(right_mountains_1, FLIPPERS)
Location().add(BirdKey()).connect(right_mountains_2, COUNT(POWER_BRACELET, 2))
Location().add(Chest(0x01D)).connect(right_mountains_2, BOMB)  # Chest(0x2F2) is also here, but that is the multi-chest puzzle.
right_mountains_3 = Location().connect(right_mountains_2, AND(FEATHER, HOOKSHOT))
