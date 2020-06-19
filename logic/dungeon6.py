from .requirements import *
from .location import Location
from locations import *


class Dungeon6:
    def __init__(self, options):
        entrance = Location(6)
        Location(6).add(DungeonChest(0x1CF)).connect(entrance, OR(BOMB, BOW, MAGIC_ROD, COUNT(POWER_BRACELET, 2))) # 50 rupees
        Location(6).add(DungeonChest(0x1C9)).connect(entrance, COUNT(POWER_BRACELET, 2)) # 100 rupees start
        Location(6).add(OwlStatue(0x1BB)).connect(entrance, STONE_BEAK6)

        # Power bracelet chest
        bracelet_chest = Location(6).add(DungeonChest(0x1CE)).connect(entrance, AND(BOMB, FEATHER))

        # left side
        Location(6).add(DungeonChest(0x1C0)).connect(entrance, AND(POWER_BRACELET, OR(BOMB, BOW, MAGIC_ROD))) # 3 wizrobes raised blocks dont need to hit the switch
        left_side = Location(6).add(DungeonChest(0x1B9)).add(DungeonChest(0x1B3)).connect(entrance, AND(POWER_BRACELET, OR(BOMB, BOOMERANG)))
        Location(6).add(DroppedKey(0x1B4)).connect(left_side, OR(BOMB, BOW, MAGIC_ROD)) # 2 wizrobe drop key
        top_left = Location(6).add(DungeonChest(0x1B0)).connect(left_side, COUNT(POWER_BRACELET, 2)) # top left chest horseheads
        Location().add(Chest(0x06C)).connect(top_left, POWER_BRACELET)  # seashell chest in raft game

        # right side
        to_miniboss = Location(6).connect(entrance, KEY6)
        miniboss = Location(6).connect(to_miniboss, BOMB)
        lower_right_side = Location(6).add(DungeonChest(0x1BE)).connect(entrance, AND(OR(BOMB, BOW, MAGIC_ROD), COUNT(POWER_BRACELET, 2))) # waterway key
        Location(6).add(DungeonChest(0x1D1)).connect(lower_right_side, FEATHER) #ledge chest medicine
        Location(6).add(OwlStatue(0x1D7)).connect(lower_right_side, AND(POWER_BRACELET, STONE_BEAK6))

        center_1 = Location(6).add(DroppedKey(0x1C3)).connect(miniboss, AND(COUNT(POWER_BRACELET, 2), FEATHER)) # tile room key drop
        center_2_and_upper_right_side = Location(6).add(DungeonChest(0x1B1)).connect(center_1, KEY6) # top right chest horseheads
        boss_key = Location(6).add(DungeonChest(0x1B6)).connect(center_2_and_upper_right_side, AND(KEY6, HOOKSHOT))
        Location(6).add(OwlStatue(0x1B6)).connect(boss_key, STONE_BEAK6)

        boss = Location(6).add(HeartContainer(0x1BC)).connect(center_1, AND(NIGHTMARE_KEY6, BOMB))

        if options.logic == 'hard' or options.logic == 'glitched':
            bracelet_chest.connect(entrance, BOMB)

        self.entrance = entrance
