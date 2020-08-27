from .requirements import *
from .location import Location
from locations import *


class Dungeon2:
    def __init__(self, options, boss_requirement):
        entrance = Location(2)
        Location(2).add(DungeonChest(0x136)).connect(entrance, POWER_BRACELET)  # chest at entrance
        dungeon2_l2 = Location(2).connect(entrance, AND(KEY2, FOUND(KEY2, 5)))  # towards map chest
        dungeon2_map_chest = Location(2).add(DungeonChest(0x12E)).connect(dungeon2_l2, AND(attack_hookshot_powder, OR(FEATHER, HOOKSHOT)))  # map chest
        dungeon2_r2 = Location(2).connect(entrance, fire)
        Location(2).add(DroppedKey(0x132)).connect(dungeon2_r2, attack_skeleton)
        Location(2).add(DungeonChest(0x137)).connect(dungeon2_r2, AND(KEY2, FOUND(KEY2, 5), OR(rear_attack, rear_attack_range)))  # compass chest
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(2).add(OwlStatue(0x133)).connect(dungeon2_r2, STONE_BEAK2)
        dungeon2_r3 = Location(2).add(DungeonChest(0x138)).connect(dungeon2_r2, attack)  # first chest with key
        dungeon2_r4 = Location(2).add(DungeonChest(0x139)).connect(dungeon2_r3, FEATHER) # button spawn chest
        shyguy_key_drop = Location(2).add(DroppedKey(0x134)).connect(dungeon2_r3, OR(rear_attack, AND(FEATHER, rear_attack_range))) # shyguy drop key
        dungeon2_r5 = Location(2).add(DungeonChest(0x126)).add(DungeonChest(0x121)).connect(dungeon2_r4, AND(KEY2, FOUND(KEY2, 3), attack_hookshot)) # post hinox
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(2).add(OwlStatue(0x129), OwlStatue(0x12F)).connect(dungeon2_r5, STONE_BEAK2)
        dungeon2_ghosts_room = Location(2).connect(dungeon2_r5, AND(KEY2, FOUND(KEY2, 4)))
        dungeon2_ghosts_chest = Location(2).add(DungeonChest(0x120)).connect(dungeon2_ghosts_room, OR(fire, BOW))  # bracelet chest
        dungeon2_r6 = Location(2).add(DungeonChest(0x122)).connect(dungeon2_r5, POWER_BRACELET)
        dungeon2_boss_key = Location(2).add(DungeonChest(0x127)).connect(dungeon2_r6, OR(BOW, BOMB, MAGIC_ROD, OCARINA, POWER_BRACELET)) # TODO: song 1
        dungeon2_pre_boss = Location(2).connect(dungeon2_r6, AND(POWER_BRACELET, FEATHER, KEY2, FOUND(KEY2, 5)))
        # If we can get here, we have everything for the boss. So this is also the goal room.
        dungeon2_boss = Location(2).add(HeartContainer(0x12B)).connect(dungeon2_pre_boss, AND(NIGHTMARE_KEY2, boss_requirement, FEATHER))
        
        if options.logic == 'glitched' or options.logic == 'hell':
            dungeon2_ghosts_chest.connect(dungeon2_ghosts_room, SWORD) # use sword to spawn ghosts on other side of the room so they run away (logically irrelevant because of torches at start)
            dungeon2_r6.connect(dungeon2_r5, FEATHER) # superjump to staircase next to hinox. 
            
        if options.logic == 'hell':    
            dungeon2_map_chest.connect(dungeon2_l2, AND(attack_hookshot_powder, PEGASUS_BOOTS)) # use boots to jump over the pits
            dungeon2_r4.connect(dungeon2_r3, AND(PEGASUS_BOOTS,HOOKSHOT)) # use pegasus boots to cross the pits, hookshot is nice
            dungeon2_r4.connect(shyguy_key_drop, rear_attack_range, one_way=True) # adjust for alternate requirements for dungeon2_r4
            dungeon2_pre_stairs_boss = Location(2).connect(dungeon2_r6, AND(HOOKSHOT, KEY2, FOUND(KEY2, 5))) # hookshot clip through the pot using both pol's voice
            dungeon2_post_stairs_boss = Location(2).connect(dungeon2_pre_stairs_boss, OR(BOMB, AND(PEGASUS_BOOTS, FEATHER))) # use a bomb to lower the last platform, or boots + feather to cross over top
            dungeon2_pre_boss.connect(dungeon2_post_stairs_boss, AND(PEGASUS_BOOTS, HOOKSHOT)) # boots bonk off bottom wall + hookshot spam across the two 1 tile pits vertically
            
        self.entrance = entrance
