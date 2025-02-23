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
        south_4way = Location("D3 South Room", dungeon=3)
        south_4way_drop1 = Location(dungeon=3).add(DroppedKey(0x158)) # small key
        west_4way = Location("D3 West Room", dungeon=3)
        west_4way_drop2 = Location(dungeon=3).add(DroppedKey(0x155)) # small key
        north_4way = Location("D3 North Room", dungeon=3)
        north_4way_drop3 = Location(dungeon=3).add(DroppedKey(0x154)) # small key
        main_room = Location("D3 East Room", dungeon=3)
        main_room = Location("D3 Main Area", dungeon=3)
        main_room_drop4 = Location(dungeon=3).add(DroppedKey(0x14D)) # small key
        two_pairodd_room = Location("D3 Two Zol, Two Pairodd Room", dungeon=3)
        two_pairodd_room_drop5 = Location(dungeon=3).add(DroppedKey(0x148)) # small key
        two_zol_stalfos_room = Location("D3 Two Zol, Stalfos Room", dungeon=3)
        flying_bomb_room = Location("D3 Flying Bomb, Owl Room", dungeon=3)
        fenced_walkway = Location("D3 Fenced Walkway", dungeon=3)
        fenced_walkway_chest5 = Location(dungeon=3).add(DungeonChest(0x144)) # 50 rupees
        timer_bombite_room = Location(dungeon=3)
        three_zol_stalfos_room = Location(dungeon=3)
        three_zol_stalfos_room_chest6 = Location(dungeon=3).add(DungeonChest(0x142)) # compass
        three_bombite_room = Location(dungeon=3)
        three_bombite_room_drop_6 = Location(dungeon=3).add(DroppedKey(0x141)) # small key
        big_pit_room = Location(dungeon=3)
        tile_arrow_ledge = Location(dungeon=3)
        tile_arrow_ledge_chest_7 = Location(dungeon=3).add(DungeonChest(0x147)) # nightmare key
        miniboss_room = Location("D3 Miniboss Room", dungeon=3)
        after_miniboss_room = Location(dungeon=3)
        after_miniboss_room_chest8 = Location(dungeon=3).add(DungeonChest(0x146)) # pegasus boots
        towards_boss1 = Location("D3 Boss Path 1", dungeon=3)
        towards_boss2 = Location("D3 Boss Path 2", dungeon=3)
        towards_boss3 = Location("D3 Boss Path 3", dungeon=3)
        towards_boss4 = Location("D3 Boss Path 4", dungeon=3)
        three_pairodd_room = Location("D3 Three Pairodd Room", dungeon=3)
        pre_boss = Location("D3 Room Before Boss", dungeon=3)
        pre_boss_drop7 = Location(dungeon=3).add(DroppedKey(0x15B)) # small key
        boss_room = Location("D3 Boss Room", dungeon=3)
        boss = Location(dungeon=3).add(HeartContainer(0x15A), Instrument(0x159))

        # owl statues
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=3).add(OwlStatue(0x154)).connect(north_4way, STONE_BEAK3)
            Location(dungeon=3).add(OwlStatue(0x140)).connect(flying_bomb_room, STONE_BEAK3)
            Location(dungeon=3).add(OwlStatue(0x147)).connect(main_room, STONE_BEAK3)

        # connections
        entrance.connect(after_vacuum, PEGASUS_BOOTS) # Right side reverse eye
        entrance.connect(after_pot_door, r.throw_pot)
        after_pot_door.connect(after_pot_door_chest1, AND(r.enemy_requirements["GEL"], r.enemy_requirements["MOBLIN_SWORD"], r.enemy_requirements["BOUNCING_BOMBITE"]))  # First chest with key
        after_pot_door.connect(slime_room, None)
        after_pot_door.connect(stairs_a_room, PEGASUS_BOOTS) # TODO: REMOVE THIS, it is logically letting the player into staircase A before they really can
        slime_room.connect(slime_room_chest2, None)
        slime_room.connect(swordstalfos_room, r.enemy_requirements["HIDING_ZOL"])
        slime_room.connect(stairs_a_room, r.enemy_requirements["HIDING_ZOL"]) # need to kill slimes to continue
        stairs_a_room.connect(stairs_a_room_chest3, AND(PEGASUS_BOOTS, r.enemy_requirements["GEL"], r.enemy_requirements["STALFOS_EVASIVE"]))  # 3th chest requires killing the slime behind the crystal pillars
        stairs_a_room.connect(south_4way, AND(KEY3, FOUND(KEY3, 8)))
        south_4way.connect(south_4way_drop1, AND(r.enemy_requirements["HIDING_ZOL"], r.enemy_requirements["MOBLIN"], OR(r.enemy_requirements["PAIRODD"], BOOMERANG))) # south keydrop, can use boomerang to knock owls into pit
        stairs_a_room.connect(west_4way, AND(KEY3, FOUND(KEY3, 8)))
        west_4way.connect(west_4way_drop2, AND(r.enemy_requirements["HIDING_ZOL"], OR(r.enemy_requirements["PAIRODD"], BOOMERANG))) # west key drop (no longer requires feather to get across hole), can use boomerang to knock owls into pit
        stairs_a_room.connect(north_4way, AND(KEY3, FOUND(KEY3, 8)))
        north_4way.connect(north_4way_drop3, AND(r.enemy_requirements["STALFOS_AGGRESSIVE"], r.enemy_requirements["MOBLIN"])) # north key drop
        north_4way.connect(stairs_a_room_switched, r.hit_switch, one_way=True) # hit switch to visit upstairs variant
        stairs_a_room_switched.connect(switch_locked_chest4, None, one_way=True) # after hit switch get zol switch chest
        stairs_a_room_switched.connect(swordstalfos_room_chest5, r.enemy_requirements["HIDING_ZOL"], one_way=True)
        stairs_a_room.connect(main_room, AND(KEY3, FOUND(KEY3, 4)))
        main_room.connect(main_room, None)
        main_room.connect(main_room_drop4, r.enemy_requirements["HIDING_ZOL"])
        main_room.connect(two_pairodd_room, AND(r.enemy_requirements["ZOL"], r.enemy_requirements["GEL"]))
        two_pairodd_room.connect(two_zol_stalfos_room, None, one_way=True)
        two_pairodd_room.connect(two_pairodd_room_drop5, AND(r.enemy_requirements["HIDING_ZOL"], r.enemy_requirements["PAIRODD"]))
        two_zol_stalfos_room.connect(flying_bomb_room, None, one_way=True)
        flying_bomb_room.connect(fenced_walkway, None)
        main_room.connect(flying_bomb_room, None) #TODO: This exists just to make logic match stable, it's not really in logic
        two_zol_stalfos_room.connect(fenced_walkway_chest5, r.enemy_requirements["STALFOS_AGGRESSIVE"], one_way=True)
        #TODO: fenced_walkway.connect(fenced_walkway_chest5, OR(COUNT(SWORD, 2), BOW, BOMB, BOOMERANG), one_way=True) # kill zols and stalfos while on ledge to spawn chest - revisit
        main_room.connect(timer_bombite_room, None)
        timer_bombite_room.connect(three_zol_stalfos_room, AND(r.enemy_requirements["HIDING_ZOL"], r.enemy_requirements["TIMER_BOMBITE"]))
        three_zol_stalfos_room.connect(three_zol_stalfos_room_chest6, None)
        three_zol_stalfos_room.connect(three_bombite_room, BOMB)
        three_bombite_room.connect(three_bombite_room_drop_6, r.enemy_requirements["BOUNCING_BOMBITE"])
        main_room.connect(big_pit_room, BOMB)
        big_pit_room.connect(tile_arrow_ledge, AND(FEATHER, PEGASUS_BOOTS))
        tile_arrow_ledge.connect(tile_arrow_ledge_chest_7, OR(FEATHER, HOOKSHOT))
        main_room.connect(miniboss_room, AND(r.enemy_requirements["ZOL"], r.enemy_requirements["GEL"]))
        miniboss_room.connect(after_miniboss_room, r.miniboss_requirements[world_setup.miniboss_mapping[2]])
        after_miniboss_room.connect(after_miniboss_room_chest8, None)
        main_room.connect(towards_boss1, AND(KEY3, FOUND(KEY3, 5)))
        towards_boss1.connect(towards_boss2, AND(KEY3, FOUND(KEY3, 6)))
        towards_boss2.connect(towards_boss3, AND(KEY3, FOUND(KEY3, 7)))
        towards_boss3.connect(towards_boss4, AND(KEY3, FOUND(KEY3, 8)))
        towards_boss4.connect(three_pairodd_room, AND(FEATHER, PEGASUS_BOOTS))
        three_pairodd_room.connect(pre_boss, r.enemy_requirements["PAIRODD"])
        pre_boss.connect(pre_boss_drop7, r.enemy_requirements["KEESE"])
        pre_boss.connect(boss_room, NIGHTMARE_KEY3)
        boss_room.connect(boss, r.boss_requirements[world_setup.boss_mapping[2]])

        if options.dungeon_items not in {'localnightmarekey', 'keysanity', 'keysy', 'smallkeys'}:
            # Without keysanity we need to fix the keylogic here, else we can never generate proper placement.
            west_4way.connect(stairs_a_room, KEY3)
            west_4way_drop2.items[0].forced_item = KEY3
            south_4way.connect(stairs_a_room, KEY3)
            south_4way_drop1.items[0].forced_item = KEY3

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            entrance.connect(after_vacuum, r.hookshot_over_pit) # hookshot the chest to get to the right side
            south_4way.connect(south_4way_drop1, r.throw_pot) # use pots to kill enemies
            north_4way.connect(north_4way_drop3, r.throw_pot) # use pots to kill the enemies
            north_4way.connect(stairs_a_room_switched, r.throw_pot, one_way=True) # hit switch to visit upstairs with platforms switched
            fenced_walkway.connect(three_bombite_room_drop_6, BOOMERANG, one_way=True) # 3 bombite room from the walkway, grab item with boomerang

        if options.logic == 'glitched' or options.logic == 'hell':
            #TODO: after_pot_door.connect(stairs_a_room, AND(PEGASUS_BOOTS, r.shaq_jump)) # new connection after logic_tester passes
            #TODO: after_pot_door.connect(switch_locked_chest4, AND(PEGASUS_BOOTS, r.shaq_jump)) # new connection after logic_tester passes
            swordstalfos_room.connect(swordstalfos_room_chest5, r.super_jump_feather) # use superjump to get over the bottom left block
            stairs_a_room.connect(switch_locked_chest4, AND(OR(PEGASUS_BOOTS, r.hookshot_clip_block), r.shaq_jump)) # boots from south or hookshot clip weith pushblock & zols to get behing the chest, then shaq jump using the pushblock to get on raised platforms
            stairs_a_room.connect(stairs_a_room_chest3, AND(r.enemy_requirements["GEL"], r.enemy_requirements["STALFOS_EVASIVE"], r.hookshot_clip_block)) # hookshot clip through the northern push block next to raised blocks chest to get to the zol
            big_pit_room.connect(tile_arrow_ledge, r.super_jump_feather) # superjump to right side 3 gap via top wall and jump the 2 gap
            towards_boss2.connect(after_miniboss_room, r.super_jump_feather) # superjump from keyblock path. use 2 keys to open enough blocks 
        
        if options.logic == 'hell':
            #TODO: entrance.connect(after_vacuum, SWORD) # just hold right, more reliable with sword
            #TODO: after_pot_door.connect(stairs_a_room, AND(PEGASUS_BOOTS, r.boots_superhop)) # is this even logically relevant since you can get through zol room with bow/rod?
            swordstalfos_room.connect(swordstalfos_room_chest5, r.boots_superhop) # use boots superhop to get over the bottom left block
            stairs_a_room.connect(switch_locked_chest4, r.boots_superhop, one_way=True) # TODO: REMOVE or connect to after_pot_door instead after logic_tester passes - use boots superhop off top wall or left wall to get on raised blocks
            #TODO: stairs_a_room.connect(stairs_a_room_chest3, AND(r.super_bump, r.enemy_requirements["GEL"], r.enemy_requirements["STALFOS_EVASIVE"]))
            #TODO: stairs_a_room.connect(switch_locked_chest4, r.super_bump)
            stairs_a_room_switched.connect(stairs_a_room_chest3, AND(r.super_jump_feather, r.enemy_requirements["GEL"], r.enemy_requirements["STALFOS_EVASIVE"]), one_way=True) # use superjump near top blocks chest to get to zol without boots, keep wall clip on right wall to get a clip on left wall or use obstacles
            west_4way.connect(west_4way_drop2, r.shield_bump) # knock everything into the pit including the teleporting owls
            south_4way.connect(south_4way_drop1, r.shield_bump) # knock everything into the pit including the teleporting owls
            #TODO: main_room.connect(fenced_walkway, r.super_bump) # super bump off zols to go past pushblock in reverse
            #TODO: tile_arrow_ledge.connect(tile_arrow_ledge_chest_7, r.shield_bump) # shield bump stalfos multiple times to get around pits to nightmare key
            main_room.connect(tile_arrow_ledge, AND(r.super_jump_feather, r.shield_bump)) # superjump into jumping stalfos and shield bump to right ledge
            big_pit_room.connect(tile_arrow_ledge, r.pit_buffer_boots) #boots bonk across the pits with pit buffering and hookshot to the chest
            #TODO: main_room.connect(towards_boss3, r.super_bump)
            fenced_walkway.connect(three_bombite_room, AND(r.enemy_requirements["TIMER_BOMBITE"], OR(BOW, MAGIC_ROD, AND(OR(FEATHER, PEGASUS_BOOTS), OR(SWORD, MAGIC_POWDER)))), one_way=True) # 3 bombite room from the left side, use a bombite to blow open the wall without bombs
            towards_boss4.connect(three_pairodd_room, AND(FEATHER, POWER_BRACELET)) # TODO: REMOVE and replace with or(toadstool, bracelet) # current logic was for clearing first half with bracelet, second half with feather
            #TODO: towards_boss4.connect(three_pairodd_room, r.toadstool_bounce_2d_hell) # bracelet or toadstool to get damage boost from 2d spikes to get through passage
            towards_boss4.connect(three_pairodd_room, AND(r.enemy_requirements["PAIRODD"], r.boots_bonk_2d_spikepit)) # use medicine invulnerability to pass through the 2d section with a boots bonk to reach the staircase
            
        #TODO: if options.nagmessages == True: # is this possible along with magpie at the moment?
            #towards_boss3.connect(towards_boss4, None)

        self.entrance = entrance
        self.final_room = boss


class NoDungeon3:
    def __init__(self, options, world_setup, r):
        entrance = Location("D3 Entrance", dungeon=3)
        Location(dungeon=3).add(HeartContainer(0x15A), Instrument(0x159)).connect(entrance, AND(POWER_BRACELET, r.boss_requirements[
            world_setup.boss_mapping[2]]))

        self.entrance = entrance
