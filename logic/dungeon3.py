from .requirements import *
from .location import Location
from locations.all import *


class Dungeon3:
    def __init__(self, options, world_setup, r):

        # locations
        entrance = Location("D3 Entrance", dungeon=3)
        after_vacuum = Location(dungeon=3).add(DungeonChest(0x153)) #small key
        after_pot_door = Location("D3 After Pot Door", dungeon=3)
        after_pot_door_chest1 = Location(dungeon=3).add(DungeonChest(0x151)) # small key
        slime_room = Location("D3 Four Zol Chest Room")
        slime_room_chest2 = Location(dungeon=3).add(DungeonChest(0x14F)) # slime
        swordstalfos_room = Location("D3 Sword Stalfos Room Entrance", dungeon=3)
        swordstalfos_room_chest5 = Location(dungeon=3).add(DungeonChest(0x150)) # map
        stairs_a_room = Location("D3 Near First Staircase", dungeon=3)
        stairs_a_room_switched = Location("D3 Near First Staircase Switched", dungeon=3)
        stairs_a_room_chest3 = Location(dungeon=3).add(DungeonChest(0x14E)) # 200 rupees
        switch_locked_chest4 = Location(dungeon=3).add(DungeonChest(0x14C)) # beak
        # 4 key door room
        south_4way = Location("D3 South Room", dungeon=3)
        south_4way_drop1 = Location(dungeon=3).add(DroppedKey(0x158)) # small key
        west_4way = Location("D3 West Room", dungeon=3)
        west_4way_drop2 = Location(dungeon=3).add(DroppedKey(0x155)) # small key
        north_4way = Location("D3 North Room", dungeon=3)
        north_4way_drop3 = Location(dungeon=3).add(DroppedKey(0x154)) # small key
        
        

        
        area_right = Location("D3 East Room", dungeon=3).connect(stairs_a_room, AND(KEY3, FOUND(KEY3, 4))) # We enter the top part of the map here.
        Location(dungeon=3).add(DroppedKey(0x14D)).connect(area_right, r.enemy_requirements["HIDING_ZOL"]) # key after the stairs.

        dungeon3_nightmare_key_chest = Location(dungeon=3).add(DungeonChest(0x147)).connect(area_right, AND(BOMB, FEATHER, PEGASUS_BOOTS)) # nightmare key
        dungeon3_miniboss_room = Location("D3 Miniboss Room", dungeon=3).connect(area_right, AND(r.enemy_requirements["ZOL"], r.enemy_requirements["GEL"]))
        dungeon3_post_dodongo_chest = Location(dungeon=3).add(DungeonChest(0x146)).connect(dungeon3_miniboss_room, r.miniboss_requirements[world_setup.miniboss_mapping[2]]) # pegasus boots
        compass_chest = Location(dungeon=3).add(DungeonChest(0x142)).connect(area_right, AND(r.enemy_requirements["HIDING_ZOL"], r.enemy_requirements["TIMER_BOMBITE"])) # compass
        dungeon3_3_bombite_room = Location(dungeon=3).add(DroppedKey(0x141)).connect(compass_chest, AND(r.enemy_requirements["BOUNCING_BOMBITE"], BOMB)) # small key
        Location(dungeon=3).add(DroppedKey(0x148)).connect(area_right, AND(r.enemy_requirements["HIDING_ZOL"], r.enemy_requirements["PAIRODD"])) # small key
        Location(dungeon=3).add(DungeonChest(0x144)).connect(area_right, AND(r.enemy_requirements["STALFOS_AGGRESSIVE"], r.enemy_requirements["ZOL"])) # 50 rupees

        towards_boss1 = Location("D3 Boss Path 1", dungeon=3).connect(area_right, AND(KEY3, FOUND(KEY3, 5)))
        towards_boss2 = Location("D3 Boss Path 2", dungeon=3).connect(towards_boss1, AND(KEY3, FOUND(KEY3, 6)))
        towards_boss3 = Location("D3 Boss Path 3", dungeon=3).connect(towards_boss2, AND(KEY3, FOUND(KEY3, 7)))
        towards_boss4 = Location("D3 Boss Path 4", dungeon=3).connect(towards_boss3, AND(KEY3, FOUND(KEY3, 8)))

        # Just the whole area before the boss, requirements for the boss itself and the rooms before it are the same.
        pre_boss = Location(dungeon=3).connect(towards_boss4, AND(r.enemy_requirements["PAIRODD"], FEATHER, PEGASUS_BOOTS))
        Location("D3 BEFORE NIGHTMARE").add(DroppedKey(0x15B)).connect(pre_boss, r.enemy_requirements["KEESE"]) # small key

        boss_room = Location("D3 Boss Room", dungeon=3).connect(pre_boss, NIGHTMARE_KEY3)
        boss = Location(dungeon=3).add(HeartContainer(0x15A), Instrument(0x159)).connect(boss_room, r.boss_requirements[world_setup.boss_mapping[2]])

        # owl statues
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=3).add(OwlStatue(0x154)).connect(north_4way, STONE_BEAK3)
            Location(dungeon=3).add(OwlStatue(0x140)).connect(area_right, STONE_BEAK3)
            Location(dungeon=3).add(OwlStatue(0x147)).connect(area_right, STONE_BEAK3)

        # connections
        entrance.connect(after_vacuum, PEGASUS_BOOTS) # Right side reverse eye
        entrance.connect(after_pot_door, r.throw_pot)
        after_pot_door.connect(after_pot_door_chest1, AND(r.enemy_requirements["GEL"], r.enemy_requirements["MOBLIN_SWORD"], r.enemy_requirements["BOUNCING_BOMBITE"]))  # First chest with key
        after_pot_door.connect(slime_room, None)
        after_pot_door.connect(stairs_a_room, PEGASUS_BOOTS) # REMOVE THIS, it exists to make logic match for test
        slime_room.connect(slime_room_chest2, None)
        slime_room.connect(swordstalfos_room, r.enemy_requirements["HIDING_ZOL"])
        slime_room.connect(stairs_a_room, r.enemy_requirements["HIDING_ZOL"]) # need to kill slimes to continue
        stairs_a_room.connect(stairs_a_room_chest3, AND(PEGASUS_BOOTS, r.enemy_requirements["GEL"], r.enemy_requirements["STALFOS_EVASIVE"]))  # 3th chest requires killing the slime behind the crystal pillars
        stairs_a_room.connect(south_4way, AND(KEY3, FOUND(KEY3, 8)))
        south_4way.connect(south_4way_drop1, AND(r.enemy_requirements["HIDING_ZOL"], r.enemy_requirements["MOBLIN"], OR(r.enemy_requirements["PAIRODD"], BOOMERANG))) # south keydrop, can use boomerang to knock owls into pit
        stairs_a_room.connect(west_4way, AND(KEY3, FOUND(KEY3, 8)))
        west_4way.connect(west_4way_drop2, AND(r.enemy_requirements["HIDING_ZOL"], OR(r.enemy_requirements["PAIRODD"], BOOMERANG))) # west key drop (no longer requires feather to get across hole), can use boomerang to knock owls into pit
        #add logic for west 4way with feather and no range? Maybe casual
        stairs_a_room.connect(north_4way, AND(KEY3, FOUND(KEY3, 8)))
        north_4way.connect(north_4way_drop3, AND(r.enemy_requirements["STALFOS_AGGRESSIVE"], r.enemy_requirements["MOBLIN"])) # north key drop
        north_4way.connect(stairs_a_room_switched, r.hit_switch, one_way=True) # hit switch to visit upstairs variant
        stairs_a_room_switched.connect(switch_locked_chest4, None, one_way=True) # after hit switch get zol switch chest
        stairs_a_room_switched.connect(swordstalfos_room_chest5, r.enemy_requirements["HIDING_ZOL"], one_way=True)

        if options.dungeon_items not in {'localnightmarekey', 'keysanity', 'keysy', 'smallkeys'}:
            # Without keysanity we need to fix the keylogic here, else we can never generate proper placement.
            west_4way.connect(stairs_a_room, KEY3)
            west_4way_drop2.items[0].forced_item = KEY3
            south_4way.connect(stairs_a_room, KEY3)
            south_4way_drop1.items[0].forced_item = KEY3

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            north_4way.connect(stairs_a_room_switched, r.throw_pot, one_way=True) # hit switch to visit upstairs with platforms switched
            after_vacuum.connect(entrance, r.hookshot_over_pit) # hookshot the chest to get to the right side
            north_4way_drop3.connect(north_4way, r.throw_pot) # use pots to kill the enemies
            south_4way_drop1.connect(south_4way, r.throw_pot) # use pots to kill enemies
            north_4way.connect(switch_locked_chest4, r.throw_pot, one_way=True) # use pots to hit the switch
            dungeon3_3_bombite_room.connect(area_right, BOOMERANG) # 3 bombite room from the left side, grab item with boomerang

        if options.logic == 'glitched' or options.logic == 'hell':
            #after_pot_door.connect(stairs_a_room, AND(PEGASUS_BOOTS, r.shaq_jump)) # new connection after logic_tester passes
            #after_pot_door.connect(switch_locked_chest4, AND(PEGASUS_BOOTS, r.shaq_jump)) # new connection after logic_tester passes
            swordstalfos_room.connect(swordstalfos_room_chest5, r.super_jump_feather) # use superjump to get over the bottom left block
            stairs_a_room.connect(switch_locked_chest4, AND(OR(PEGASUS_BOOTS, r.hookshot_clip_block), r.shaq_jump), one_way=True) # boots from south or hookshot clip weith pushblock & zols to get behing the chest, then shaq jump using the pushblock to get on raised platforms
            stairs_a_room.connect(stairs_a_room_chest3, AND(r.enemy_requirements["GEL"], r.enemy_requirements["STALFOS_EVASIVE"], r.hookshot_clip_block)) # hookshot clip through the northern push block next to raised blocks chest to get to the zol
            dungeon3_nightmare_key_chest.connect(area_right, AND(r.super_jump_feather, BOMB)) # superjump to right side 3 gap via top wall and jump the 2 gap
            dungeon3_post_dodongo_chest.connect(area_right, AND(r.super_jump_feather, FOUND(KEY3, 6))) # superjump from keyblock path. use 2 keys to open enough blocks TODO: text skip skips 1 key
        
        if options.logic == 'hell':
            #after_pot_door.connect(stairs_a_room, AND(PEGASUS_BOOTS, r.boots_superhop)) # not relevant since it means you have a switch hitter, but techinically correct
            swordstalfos_room.connect(swordstalfos_room_chest5, r.boots_superhop) # use boots superhop to get over the bottom left block
            stairs_a_room.connect(switch_locked_chest4, r.boots_superhop, one_way=True) # REMOVE or connect to after_pot_door instead after logic_tester passes - use boots superhop off top wall or left wall to get on raised blocks
            stairs_a_room_switched.connect(stairs_a_room_chest3, AND(r.super_jump_feather, r.enemy_requirements["GEL"], r.enemy_requirements["STALFOS_EVASIVE"]), one_way=True) # use superjump near top blocks chest to get to zol without boots, keep wall clip on right wall to get a clip on left wall or use obstacles
            west_4way_drop2.connect(west_4way, r.shield_bump) # knock everything into the pit including the teleporting owls
            south_4way_drop1.connect(south_4way, r.shield_bump) # knock everything into the pit including the teleporting owls
            dungeon3_nightmare_key_chest.connect(area_right, AND(r.super_jump_feather, r.shield_bump)) # superjump into jumping stalfos and shield bump to right ledge
            dungeon3_nightmare_key_chest.connect(area_right, AND(BOMB, r.pit_buffer_boots, HOOKSHOT)) # boots bonk across the pits with pit buffering and hookshot to the chest
            compass_chest.connect(dungeon3_3_bombite_room, AND(r.enemy_requirements["BOUNCING_BOMBITE"], OR(BOW, MAGIC_ROD, AND(OR(FEATHER, PEGASUS_BOOTS), OR(SWORD, MAGIC_POWDER)))), one_way=True) # 3 bombite room from the left side, use a bombite to blow open the wall without bombs
            pre_boss.connect(towards_boss4, AND(r.enemy_requirements["PAIRODD"], FEATHER, POWER_BRACELET)) # use bracelet super bounce glitch to pass through first part underground section
            pre_boss.connect(towards_boss4, AND(r.enemy_requirements["PAIRODD"], r.boots_bonk_2d_spikepit)) # use medicine invulnerability to pass through the 2d section with a boots bonk to reach the staircase
            
        self.entrance = entrance
        self.final_room = boss


class NoDungeon3:
    def __init__(self, options, world_setup, r):
        entrance = Location("D3 Entrance", dungeon=3)
        Location(dungeon=3).add(HeartContainer(0x15A), Instrument(0x159)).connect(entrance, AND(POWER_BRACELET, r.boss_requirements[
            world_setup.boss_mapping[2]]))

        self.entrance = entrance
