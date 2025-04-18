from .requirements import *
from .location import Location
from locations.all import *


class Dungeon2:
    def __init__(self, options, world_setup, r):
        entrance = Location("D2 Entrance", dungeon=2)
        Location(dungeon=2).add(DungeonChest(0x136)).connect(entrance, POWER_BRACELET)  # chest at entrance
        dungeon2_l2 = Location("D2 Left Door", dungeon=2).connect(entrance, FOUND(KEY2, 5))  # towards map chest
        dungeon2_map_chest = Location(dungeon=2).add(DungeonChest(0x12E)).connect(dungeon2_l2, AND(r.enemy_requirements["KEESE"], OR(FEATHER, HOOKSHOT)))  # map chest
        dungeon2_r2 = Location("D2 After Torches", dungeon=2).connect(entrance, r.fire)
        Location(dungeon=2).add(DroppedKey(0x132)).connect(dungeon2_r2, AND(r.enemy_requirements["STALFOS_EVASIVE"], r.enemy_requirements["STALFOS_AGGRESSIVE"]))
        Location(dungeon=2).add(DungeonChest(0x137)).connect(dungeon2_r2, AND(FOUND(KEY2, 5), r.enemy_requirements["MASKED_MIMIC_GORIYA"]))  # compass chest
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=2).add(OwlStatue(0x133)).connect(dungeon2_r2, STONE_BEAK2)
        dungeon2_r3 = Location(dungeon=2).add(DungeonChest(0x138)).connect(dungeon2_r2, r.hit_switch)  # first chest with key, can hookshot the switch in previous room
        dungeon2_r4 = Location(dungeon=2).add(DungeonChest(0x139)).connect(dungeon2_r3, FEATHER)  # button spawn chest
        if options.logic == "casual":
            shyguy_key_drop = Location(dungeon=2).add(DroppedKey(0x134)).connect(dungeon2_r3, AND(FEATHER, r.enemy_requirements["MASKED_MIMIC_GORIYA"]))  # shyguy drop key
        else:
            shyguy_key_drop = Location(dungeon=2).add(DroppedKey(0x134)).connect(dungeon2_r3, OR(r.rear_attack, AND(FEATHER, r.enemy_requirements["MASKED_MIMIC_GORIYA"])))  # shyguy drop key
        dungeon2_r5 = Location("D2 Pushblock Room", dungeon=2).connect(dungeon2_r4, FOUND(KEY2, 3))  # push two blocks together room with owl statue
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=2).add(OwlStatue(0x12F)).connect(dungeon2_r5, STONE_BEAK2)  # owl statue is before miniboss
        miniboss_room = Location("D2 Miniboss Room", dungeon=2).connect(dungeon2_r5, FEATHER)
        miniboss = Location(dungeon=2).add(DungeonChest(0x126)).add(DungeonChest(0x121)).connect(miniboss_room, r.miniboss_requirements[world_setup.miniboss_mapping[1]])  # post hinox
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=2).add(OwlStatue(0x129)).connect(miniboss, STONE_BEAK2)  # owl statue after the miniboss

        dungeon2_ghosts_room = Location("D2 Boo Buddies Room", dungeon=2).connect(miniboss, FOUND(KEY2, 5))
        dungeon2_ghosts_chest = Location(dungeon=2).add(DungeonChest(0x120)).connect(dungeon2_ghosts_room, OR(r.fire, r.enemy_requirements["BOO_BUDDY"]))  # bracelet chest
        dungeon2_r6 = Location("D2 After Boo Buddies", dungeon=2).add(DungeonChest(0x122)).connect(miniboss, POWER_BRACELET)
        dungeon2_boss_key = Location(dungeon=2).add(DungeonChest(0x127)).connect(dungeon2_r6, AND(r.enemy_requirements["KEESE"], r.enemy_requirements["MOBLIN"], OR(r.enemy_requirements["POLS_VOICE"], POWER_BRACELET)))
        dungeon2_pre_stairs_boss = Location("D2 Before Boss Stairs", dungeon=2).connect(dungeon2_r6, AND(r.enemy_requirements["ZOL"], OR(r.enemy_requirements["POLS_VOICE"], POWER_BRACELET), POWER_BRACELET, FOUND(KEY2, 5)))
        dungeon2_post_stairs_boss = Location("D2 Boss Stairs", dungeon=2).connect(dungeon2_pre_stairs_boss, POWER_BRACELET)
        dungeon2_pre_boss = Location("D2 Outside Boss Room", dungeon=2).connect(dungeon2_post_stairs_boss, FEATHER)
        # If we can get here, we have everything for the boss. So this is also the goal room.
        dungeon2_boss_room = Location("D2 Boss Room", dungeon=2).connect(dungeon2_pre_boss, NIGHTMARE_KEY2)
        dungeon2_boss = Location(dungeon=2).add(HeartContainer(0x12B), Instrument(0x12a)).connect(dungeon2_boss_room, r.boss_requirements[world_setup.boss_mapping[1]])

        if options.logic == 'glitched' or options.logic == 'hell':
            dungeon2_ghosts_chest.connect(dungeon2_ghosts_room, SWORD) # use sword to spawn ghosts on other side of the room so they run away (logically irrelevant because of torches at start)
            dungeon2_r6.connect(miniboss, r.super_jump_feather) # superjump to staircase next to hinox.

        if options.logic == 'hell':
            dungeon2_map_chest.connect(dungeon2_l2, AND(r.attack_hookshot_powder, r.boots_bonk_pit)) # use boots to jump over the pits
            dungeon2_r4.connect(dungeon2_r3, OR(r.boots_bonk_pit, r.hookshot_spam_pit)) # can use both pegasus boots bonks or hookshot spam to cross the pit room
            dungeon2_r4.connect(shyguy_key_drop, r.rear_attack_range, one_way=True) # adjust for alternate requirements for dungeon2_r4
            miniboss_room.connect(dungeon2_r5, r.boots_dash_2d) # use boots to dash over the spikes in the 2d section
            dungeon2_pre_stairs_boss.connect(dungeon2_r6, AND(r.hookshot_clip_block, r.enemy_requirements["ZOL"], r.enemy_requirements["POLS_VOICE"], FOUND(KEY2, 5))) # hookshot clip through the pot using both pol's voice
            dungeon2_post_stairs_boss.connect(dungeon2_pre_stairs_boss, OR(BOMB, r.boots_jump)) # use a bomb to lower the last platform, or boots + feather to cross over top (only relevant in hell logic)
            dungeon2_pre_boss.connect(dungeon2_post_stairs_boss, AND(r.boots_bonk_pit, r.hookshot_spam_pit)) # boots bonk off bottom wall + hookshot spam across the two 1 tile pits vertically

        self.entrance = entrance
        self.final_room = dungeon2_boss


class NoDungeon2:
    def __init__(self, options, world_setup, r):
        entrance = Location("D2 Entrance", dungeon=2)
        Location(dungeon=2).add(DungeonChest(0x136)).connect(entrance, POWER_BRACELET)  # chest at entrance
        Location(dungeon=2).add(HeartContainer(0x12B), Instrument(0x12a)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[1]])
        self.entrance = entrance
