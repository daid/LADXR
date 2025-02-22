from .requirements import *
from .location import Location
from locations.all import *

class Dungeon2:
    def __init__(self, options, world_setup, r):
        
        #locations
        entrance = Location("D2 Entrance", dungeon=2)
        entrance_chest1 = Location(dungeon=2).add(DungeonChest(0x136)) # 50 rupees
        west_torches = Location("D2 West of Torches", dungeon=2)
        west_torches_chest2 = Location(dungeon=2).add(DungeonChest(0x12E)) # beak
        east_torches = Location("D2 East of Torches", dungeon=2)
        east_torches_drop1 = Location(dungeon=2).add(DroppedKey(0x132)) # small key
        east_torches_drop2 = Location(dungeon=2).add(DroppedKey(0x134)) # small key
        east_torches_chest3 = Location(dungeon=2).add(DungeonChest(0x137)) # compass
        east_torches_chest4 = Location(dungeon=2).add(DungeonChest(0x138)) # small key
        east_torches_chest5 = Location(dungeon=2).add(DungeonChest(0x139)) # small key
        mimic_beetle_room = Location("Mimic & Beetle Area", dungeon=2) 
        passage_a_room = Location("D2 Pushblock Room", dungeon=2)
        miniboss_room = Location("D2 Miniboss Room", dungeon=2)
        passage_b_room = Location("D2 After Miniboss", dungeon=2)
        vacuum_pre_boo = Location("Before Boos", dungeon=2)
        vacuum_pre_boo_chest6 = Location(dungeon=2).add(DungeonChest(0x126)) # map
        vacuum_pre_boo_chest7 = Location(dungeon=2).add(DungeonChest(0x121)) # 20 rupees
        boo_room = Location("D2 Boo Buddies Room", dungeon=2)
        boo_room_chest8 = Location(dungeon=2).add(DungeonChest(0x120)) # bracelet
        north_switch_room = Location("D2 After Boo Buddies", dungeon=2)
        north_switch_room_chest8 = Location(dungeon=2).add(DungeonChest(0x122)) # small key
        north_switch_room_chest9 = Location(dungeon=2).add(DungeonChest(0x127)) # nightmare key
        passage_c_room_entrance = Location("D2 Boss Passage Room Entrance", dungeon=2)
        passage_c_room = Location("D2 Boss Passage Room", dungeon=2)
        pre_boss_room = Location("D2 Boss Stairs", dungeon=2)
        pre_boss = Location("D2 Outside Boss Room", dungeon=2)
        # If we can get here, we have everything for the boss. So this is also the goal room.
        boss_room = Location("D2 Boss Room", dungeon=2)
        boss = Location(dungeon=2).add(HeartContainer(0x12B), Instrument(0x12a))
        
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=2).add(OwlStatue(0x133)).connect(east_torches, STONE_BEAK2)
            Location(dungeon=2).add(OwlStatue(0x12F)).connect(passage_a_room, STONE_BEAK2)  # owl statue is before miniboss
            Location(dungeon=2).add(OwlStatue(0x129)).connect(passage_b_room, AND(FEATHER, STONE_BEAK2))  # owl statue after the miniboss

        #connections

        if options.logic == "casual":
            east_torches_drop2.connect(east_torches, AND(FEATHER, r.enemy_requirements["MASKED_MIMIC_GORIYA"]))  # shyguy drop key
        else:
            east_torches_drop2.connect(east_torches, OR(r.rear_attack, AND(FEATHER, r.enemy_requirements["MASKED_MIMIC_GORIYA"])))  # shyguy drop key

        entrance_chest1.connect(entrance, POWER_BRACELET) # chest at entrance
        west_torches.connect(entrance, AND(KEY2, FOUND(KEY2, 5)))  # towards map chest
        west_torches_chest2.connect(west_torches, AND(r.enemy_requirements["KEESE"], OR(FEATHER, HOOKSHOT))) # beak
        east_torches.connect(entrance, r.fire)
        east_torches_drop1.connect(east_torches, AND(r.enemy_requirements["STALFOS_EVASIVE"], r.enemy_requirements["STALFOS_AGGRESSIVE"])) # small key
        east_torches_chest3.connect(east_torches, AND(KEY2, FOUND(KEY2, 5), r.enemy_requirements["MASKED_MIMIC_GORIYA"]))  # compass
        east_torches_chest4.connect(east_torches, r.hit_switch)  # first chest with key, can hookshot the switch in previous room
        east_torches_chest5.connect(east_torches, AND(r.hit_switch, FEATHER))  # button spawn chest
        mimic_beetle_room.connect(east_torches, AND(FEATHER, r.hit_switch))
        passage_a_room.connect(mimic_beetle_room, AND(KEY2, FOUND(KEY2, 3)))  # push two blocks together room with owl statue
        miniboss_room.connect(passage_a_room, FEATHER)
        passage_b_room.connect(miniboss_room, r.miniboss_requirements[world_setup.miniboss_mapping[1]])  # post hinox
        vacuum_pre_boo.connect(passage_a_room, FEATHER)
        vacuum_pre_boo_chest6.connect(vacuum_pre_boo, None)
        vacuum_pre_boo_chest7.connect(vacuum_pre_boo, None)
        boo_room.connect(vacuum_pre_boo, AND(KEY2, FOUND(KEY2, 5)))
        boo_room_chest8.connect(boo_room, OR(r.fire, r.enemy_requirements["BOO_BUDDY"]))
        north_switch_room.connect(vacuum_pre_boo, POWER_BRACELET)
        north_switch_room_chest8.connect(north_switch_room, None)
        north_switch_room_chest9.connect(north_switch_room, AND(r.enemy_requirements["KEESE"], r.enemy_requirements["MOBLIN"], OR(r.enemy_requirements["POLS_VOICE"], POWER_BRACELET)))
        passage_c_room_entrance.connect(north_switch_room, AND(KEY2, FOUND(KEY2, 5)))
        passage_c_room.connect(passage_c_room_entrance, AND(POWER_BRACELET, OR(r.enemy_requirements["ZOL"], r.enemy_requirements["POLS_VOICE"])))
        pre_boss_room.connect(passage_c_room, POWER_BRACELET)
        pre_boss.connect(pre_boss_room, FEATHER)
        boss_room.connect(pre_boss, NIGHTMARE_KEY2)
        boss.connect(boss_room, r.boss_requirements[world_setup.boss_mapping[1]])

        if options.logic == 'glitched' or options.logic == 'hell':
            boo_room_chest8.connect(boo_room, SWORD) # use sword to spawn ghosts on other side of the room so they run away (logically irrelevant because of torches at start)
            north_switch_room.connect(miniboss_room, r.super_jump_feather) # superjump to staircase next to hinox. 
            
        if options.logic == 'hell':    
            west_torches_chest2.connect(west_torches, AND(r.attack_hookshot_powder, r.boots_bonk_pit)) # use boots to jump over the pits
            east_torches_chest5.connect(east_torches, OR(r.boots_bonk_pit, r.hookshot_spam_pit)) # can use both pegasus boots bonks or hookshot spam to cross the pit room
            east_torches_drop2.connect(mimic_beetle_room, AND(r.rear_attack_range, OR(r.boots_bonk_pit, r.hookshot_spam_pit))) # adjust for alternate requirements for dungeon2_r4
            east_torches.connect(mimic_beetle_room, OR(r.boots_bonk_pit, r.hookshot_spam_pit)) # can use both pegasus boots bonks or hookshot spam to cross the pit room
            miniboss_room.connect(passage_a_room, r.boots_dash_2d) # use boots to dash over the spikes in the 2d section
            passage_c_room.connect(passage_c_room_entrance, AND(r.hookshot_clip_block, r.enemy_requirements["ZOL"], r.enemy_requirements["POLS_VOICE"],)) # hookshot clip through the pot using both pol's voice
            pre_boss_room.connect(passage_c_room_entrance, OR(BOMB, r.boots_jump)) # use a bomb to lower the last platform, or boots + feather to cross over top (only relevant in hell logic)
            pre_boss.connect(pre_boss_room, AND(r.boots_bonk_pit, r.hookshot_spam_pit)) # boots bonk off bottom wall + hookshot spam across the two 1 tile pits vertically
            
        self.entrance = entrance
        self.final_room = boss


class NoDungeon2:
    def __init__(self, options, world_setup, r):
        entrance = Location("D2 Entrance", dungeon=2)
        Location(dungeon=2).add(DungeonChest(0x136)).connect(entrance, POWER_BRACELET)  # chest at entrance
        Location(dungeon=2).add(HeartContainer(0x12B), Instrument(0x12a)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[1]])
        self.entrance = entrance
