from .requirements import *
from .location import Location
from locations import *


class Dungeon2:
    def __init__(self):
        entrance = Location(2)
        Location(2).add(DungeonChest(0x136)).connect(entrance, POWER_BRACELET)  # chest at entrance
        dungeon2_l2 = Location(2).connect(entrance, KEY2)  # towards map chest
        Location(2).add(DungeonChest(0x12E)).connect(dungeon2_l2, FEATHER)  # map chest
        dungeon2_r2 = Location(2).connect(entrance, fire)
        Location(2).add(DroppedKey(0x132)).connect(dungeon2_r2, attack_skeleton)
        Location(2).add(DungeonChest(0x137)).connect(dungeon2_r2, AND(KEY2, rear_attack))  # compass chest
        dungeon2_r3 = Location(2).add(DungeonChest(0x138)).connect(dungeon2_r2, attack)  # first chest with key
        dungeon2_r4 = Location(2).add(DungeonChest(0x139)).connect(dungeon2_r3, FEATHER)
        Location(2).add(DroppedKey(0x134)).connect(dungeon2_r4, rear_attack)
        dungeon2_r5 = Location(2).add(DungeonChest(0x126)).add(DungeonChest(0x121)).connect(dungeon2_r4, KEY2)
        Location(2).add(DungeonChest(0x120)).connect(dungeon2_r5, AND(KEY2, fire))  # bracelet chest
        dungeon2_r6 = Location(2).add(DungeonChest(0x122)).add(DungeonChest(0x127)).connect(dungeon2_r5, POWER_BRACELET)
        dungeon2_pre_boss = Location(2).connect(dungeon2_r6, KEY2)
        # If we can get here, we have everything for the boss. So this is also the goal room.
        dungeon2_boss = Location(2).connect(dungeon2_pre_boss, NIGHTMARE_KEY2)
        self.entrance = entrance

