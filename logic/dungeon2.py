from .requirements import *
from .location import Location
from locations import *


class Dungeon2:
    def __init__(self, options):
        entrance = Location(2)
        Location(2).add(DungeonChest(0x136)).connect(entrance, POWER_BRACELET)  # chest at entrance
        dungeon2_l2 = Location(2).connect(entrance, AND(KEY2, FOUND(KEY2, 5)))  # towards map chest
        Location(2).add(DungeonChest(0x12E)).connect(dungeon2_l2, AND(attack_hookshot_powder, OR(FEATHER, HOOKSHOT)))  # map chest
        dungeon2_r2 = Location(2).connect(entrance, fire)
        Location(2).add(DroppedKey(0x132)).connect(dungeon2_r2, attack_skeleton)
        Location(2).add(DungeonChest(0x137)).connect(dungeon2_r2, AND(KEY2, FOUND(KEY2, 5), OR(rear_attack, rear_attack_range)))  # compass chest
        Location(2).add(OwlStatue(0x133)).connect(dungeon2_r2, STONE_BEAK2)
        dungeon2_r3 = Location(2).add(DungeonChest(0x138)).connect(dungeon2_r2, attack)  # first chest with key
        dungeon2_r4 = Location(2).add(DungeonChest(0x139)).connect(dungeon2_r3, FEATHER) # button spawn chest
        Location(2).add(DroppedKey(0x134)).connect(dungeon2_r3, OR(rear_attack, AND(FEATHER, rear_attack_range))) # shyguy drop key
        dungeon2_r5 = Location(2).add(DungeonChest(0x126)).add(DungeonChest(0x121)).connect(dungeon2_r4, AND(KEY2, FOUND(KEY2, 3), attack_hookshot)) # post hinox
        Location(2).add(OwlStatue(0x129), OwlStatue(0x12F)).connect(dungeon2_r5, STONE_BEAK2)
        Location(2).add(DungeonChest(0x120)).connect(dungeon2_r5, AND(KEY2, FOUND(KEY2, 4), OR(fire, BOW)))  # bracelet chest
        dungeon2_r6 = Location(2).add(DungeonChest(0x122)).add(DungeonChest(0x127)).connect(dungeon2_r5, POWER_BRACELET)
        dungeon2_pre_boss = Location(2).connect(dungeon2_r6, AND(KEY2, FOUND(KEY2, 5)))
        # If we can get here, we have everything for the boss. So this is also the goal room.
        dungeon2_boss = Location(2).add(HeartContainer(0x12B)).connect(dungeon2_pre_boss, AND(NIGHTMARE_KEY2, OR(SWORD, MAGIC_ROD), POWER_BRACELET))
        self.entrance = entrance
