from .requirements import *
from .location import Location
from locations.all import *


class Dungeon3:
    def __init__(self, options, world_setup, r):

        # locations
        entrance = Location("D3 Entrance", dungeon=3)
        after_vacuum = Location("D3 After Vacuum", dungeon=3)
        after_vacuum_chest1 = Location(dungeon=3).add(DungeonChest(0x153)) #small key
        after_pot_door = Location("D3 After Pot Door", dungeon=3)
        after_pot_door_chest2 = Location(dungeon=3).add(DungeonChest(0x151)) # small key
        slime_room = Location("D3 Slime Room")
        slime_room_chest3 = Location(dungeon=3).add(DungeonChest(0x14F)) # slime
        swordstalfos_entry = Location("D3 Sword Stalfos Room Entrance", dungeon=3)
        swordstalfos_room = Location("D3 Sword Stalfos Pedestal", dungeon=3)
        swordstalfos_room_chest6 = Location(dungeon=3).add(DungeonChest(0x150)) # map
        before_a_stairs = Location("D3 Near First Staircase", dungeon=3)
        before_a_stairs_chest4 = Location(dungeon=3).add(DungeonChest(0x14E)) # 200 rupees
        before_a_stairs_chest5 = Location(dungeon=3).add(DungeonChest(0x14C)) # beak
        west_hallway = Location("D3 Long Hallway", dungeon=3)
        center_4way = Location("D3 Key Room Crossroads", dungeon=3)
        south_4way = Location("D3 South Key Room", dungeon=3)
        south_4way_drop1 = Location(dungeon=3).add(DroppedKey(0x158)) # small key
        west_4way = Location("D3 West Key Room", dungeon=3)
        west_4way_drop2 = Location(dungeon=3).add(DroppedKey(0x155)) # small key
        north_4way = Location("D3 North Key Room", dungeon=3)
        north_4way_drop3 = Location(dungeon=3).add(DroppedKey(0x154)) # small key
        east_4way = Location("D3 East Key Room", dungeon=3)
        main_room = Location("D3 Main Area", dungeon=3)
        main_room_drop4 = Location(dungeon=3).add(DroppedKey(0x14D)) # small key
        two_pairodd_room = Location("D3 Two Zol, Two Pairodd Room", dungeon=3)
        two_pairodd_room_drop5 = Location(dungeon=3).add(DroppedKey(0x148)) # small key
        two_zol_stalfos_room = Location("D3 Two Zol, Stalfos Room", dungeon=3)
        flying_bomb_room = Location("D3 Flying Bomb, Owl Room", dungeon=3)
        fenced_walkway = Location("D3 Fenced Walkway", dungeon=3)
        fenced_walkway_chest6 = Location(dungeon=3).add(DungeonChest(0x144)) # 50 rupees
        timer_bombite_room = Location("D3 Timer Bombite Room", dungeon=3)
        three_zol_stalfos_room = Location("D3 Three Zol, Stalfos Room", dungeon=3)
        three_zol_stalfos_room_chest7 = Location(dungeon=3).add(DungeonChest(0x142)) # compass
        three_bombite_room = Location("D3 Three Bombite Room", dungeon=3)
        three_bombite_room_drop_6 = Location(dungeon=3).add(DroppedKey(0x141)) # small key
        big_pit_room = Location("D3 Bombable Wall Room", dungeon=3)
        ledge_pre_pit = Location("D3 East Ledge Before Pit", dungeon=3)
        ledge_post_pit = Location("D3 East Ledge After Pit", dungeon=3)
        ledge_post_pit_chest_8 = Location(dungeon=3).add(DungeonChest(0x147)) # nightmare key
        miniboss_room = Location("D3 Miniboss Room", dungeon=3)
        after_miniboss_room = Location("D3 Miniboss Reward Room", dungeon=3)
        after_miniboss_room_chest9 = Location(dungeon=3).add(DungeonChest(0x146)) # pegasus boots
        towards_boss1 = Location("D3 Boss Path 1", dungeon=3)
        towards_boss2 = Location("D3 Boss Path 2", dungeon=3)
        towards_boss3 = Location("D3 Boss Path 3", dungeon=3)
        towards_boss4 = Location("D3 Boss Path 4", dungeon=3)
        three_pairodd_room = Location("D3 Three Pairodd Room", dungeon=3)
        pre_boss = Location("D3 Room Before Boss", dungeon=3)
        pre_boss_drop7 = Location(dungeon=3).add(DroppedKey(0x15B)) # small key
        boss_room = Location("D3 Boss Room", dungeon=3)
        boss = Location("D3 Boss Rewards", dungeon=3).add(HeartContainer(0x15A), Instrument(0x159)) # heart container, instrument

        # owl statues
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=3).add(OwlStatue(0x154)).connect(north_4way, STONE_BEAK3) # North Key Room <--> North Key Room Owl
            Location(dungeon=3).add(OwlStatue(0x140)).connect(flying_bomb_room, STONE_BEAK3) # Flying Bomb, Owl Room <--> Flying Bomb Owl
            Location(dungeon=3).add(OwlStatue(0x147)).connect(main_room, STONE_BEAK3) # Main Room <--> Tile Arrow Owl

        # connections
        entrance.connect(after_vacuum, PEGASUS_BOOTS) # Entrance <--> After Vacuum
        after_vacuum.connect(after_vacuum_chest1, None) # After Vacuum <--> Vacuum Mouth Chest
        entrance.connect(after_pot_door, r.throw_pot) # Entrance <--> After Pot Door
        after_pot_door.connect(after_pot_door_chest2, AND(r.enemy_requirements["GEL"], r.enemy_requirements["MOBLIN_SWORD"], r.enemy_requirements["BOUNCING_BOMBITE"])) # After Pot Door <--> Two Bombite, Sword Stalfos, Zol Chest
        after_pot_door.connect(slime_room, None) # After Pot Door <--> Slime Room 
        after_pot_door.connect(before_a_stairs, PEGASUS_BOOTS, one_way=True) # After Pot Door <--> Near First Staircase
        #TODO: after_pot_door.connect(west_hallway, PEGASUS_BOOTS) # After Pot Door <--> Long Hallway
        #TODO: west_hallway.connect(before_a_stairs, None, one_way=True) # Long Hallway <--> Near First Staircase
        #TODO: west_hallway.connect(before_a_stairs_chest4, AND(r.enemy_requirements["GEL"], r.enemy_requirements["STALFOS_EVASIVE"])) # Long Hallway <--> Two Stalfos, Zol Chest
        slime_room.connect(slime_room_chest3, None) # Slime Room <--> Four Zol Chest
        slime_room.connect(swordstalfos_entry, r.enemy_requirements["HIDING_ZOL"]) # Slime Room <--> Sword Stalfos Room Entrance
        swordstalfos_room.connect(swordstalfos_room_chest6, None) # Sword Stalfos Room <--> Sword Stalfos, Keese Switch Chest
        slime_room.connect(before_a_stairs, r.enemy_requirements["HIDING_ZOL"]) # Slime Room <--> Near First Staircase
        before_a_stairs.connect(center_4way, None) # Near First Staircase <--> Key Room Crossroads
        before_a_stairs.connect(before_a_stairs_chest4, AND(PEGASUS_BOOTS, r.enemy_requirements["GEL"], r.enemy_requirements["STALFOS_EVASIVE"])) #TODO: Remove this in favor of west hallway connection? Perhaps replace with glitched tier over-wall shield bump kill method
        center_4way.connect(south_4way, AND(KEY3, FOUND(KEY3, 8))) # Key Room Crossroads <--> South Key Room
        south_4way.connect(south_4way_drop1, AND(r.enemy_requirements["HIDING_ZOL"], r.enemy_requirements["MOBLIN"], OR(r.enemy_requirements["PAIRODD"], BOOMERANG))) # South Key Room <--> South Key Room Key
        center_4way.connect(west_4way, AND(KEY3, FOUND(KEY3, 8))) # Key Room Crossroads <--> West Key Room
        west_4way.connect(west_4way_drop2, AND(r.enemy_requirements["HIDING_ZOL"], OR(r.enemy_requirements["PAIRODD"], BOOMERANG))) # West Key Room <--> West Key Room Key
        center_4way.connect(north_4way, AND(KEY3, FOUND(KEY3, 8))) # Key Room Crossroads <--> North Key Room
        north_4way.connect(north_4way_drop3, AND(r.enemy_requirements["STALFOS_AGGRESSIVE"], r.enemy_requirements["MOBLIN"])) # North Key Room <--> North Key Room Key
        north_4way.connect(before_a_stairs_chest5, AND(r.hit_switch), one_way=True) # North Key Room --> Zol Switch Chest
        north_4way.connect(swordstalfos_room, AND(r.hit_switch, r.enemy_requirements["HIDING_ZOL"]), one_way=True) # North Key Room --> Sword Stalfos Pedestal
        center_4way.connect(east_4way, AND(KEY3, FOUND(KEY3, 4))) # Key Room Crossroads <--> East Key Room
        east_4way.connect(main_room, None) # East Key Room <--> Main Area
        main_room.connect(main_room_drop4, r.enemy_requirements["HIDING_ZOL"]) # Main Area <--> After Stairs Key
        main_room.connect(two_pairodd_room, AND(r.enemy_requirements["ZOL"], r.enemy_requirements["GEL"])) # Main Area <--> Two Zol, Two Pairodd Room
        two_pairodd_room.connect(two_pairodd_room_drop5, AND(r.enemy_requirements["HIDING_ZOL"], r.enemy_requirements["PAIRODD"])) # Two Zol, Two Pairodd Room <--> Two Zol, Two Pairodd Key
        two_pairodd_room.connect(two_zol_stalfos_room, None, one_way=True) # Two Zol, Two Pairodd Room --> Two Zol, Stalfos Room
        two_zol_stalfos_room.connect(flying_bomb_room, None, one_way=True) # Two Zol, Stalfos Room --> Flying Bomb, Owl Room
        flying_bomb_room.connect(fenced_walkway, None) # Flying Bomb, Owl Room <--> Fenced Walkway
        main_room.connect(flying_bomb_room, None) #TODO: REMOVE - This exists just to make logic match stable, it's not really in logic
        two_zol_stalfos_room.connect(fenced_walkway_chest6, r.enemy_requirements["STALFOS_AGGRESSIVE"], one_way=True) # Two Zol, Stalfos Room --> Two Zol, Stalfos Ledge Chest
        #TODO: fenced_walkway.connect(fenced_walkway_chest6, OR(COUNT(SWORD, 2), BOW, BOMB, BOOMERANG), one_way=True) # TODO: kill zols and stalfos while on ledge to spawn chest - revisit after dungeon enemizer, it's in hell logic with a shield bump to walkway
        main_room.connect(timer_bombite_room, None) # Main Area <--> Timer Bombite Room
        timer_bombite_room.connect(three_zol_stalfos_room, AND(r.enemy_requirements["HIDING_ZOL"], r.enemy_requirements["TIMER_BOMBITE"])) # Timer Bombite Room <--> Three Zol, Stalfos Room
        three_zol_stalfos_room.connect(three_zol_stalfos_room_chest7, None) # Three Zol, Stalfos Room <--> Three Zol, Stalfos Chest
        three_zol_stalfos_room.connect(three_bombite_room, BOMB) # Three Zol, Stalfos Room <--> Three Bombite Room
        three_bombite_room.connect(three_bombite_room_drop_6, r.enemy_requirements["BOUNCING_BOMBITE"]) # Three Bombite Room <--> Three Bombite Key
        main_room.connect(big_pit_room, BOMB) # Main Area <--> Bombable Wall Room
        big_pit_room.connect(ledge_pre_pit, AND(FEATHER, PEGASUS_BOOTS)) # Bombable Wall Room <--> East Ledge Before Pit
        ledge_pre_pit.connect(ledge_post_pit, OR(FEATHER, HOOKSHOT)) # Ledge Chest Before Pit <--> East Ledge After Pit
        ledge_post_pit.connect(ledge_post_pit_chest_8, None) # East Ledge After Pit <--> Tile Arrow Ledge Chest
        main_room.connect(miniboss_room, AND(r.enemy_requirements["ZOL"], r.enemy_requirements["GEL"])) # Main Area <--> Miniboss Room
        miniboss_room.connect(after_miniboss_room, r.miniboss_requirements[world_setup.miniboss_mapping[2]]) # Miniboss Room <--> Miniboss Reward Room
        after_miniboss_room.connect(after_miniboss_room_chest9, None) # Miniboss Reward Room <--> Boots Chest
        main_room.connect(towards_boss1, AND(KEY3, FOUND(KEY3, 5))) # Main Area <--> Boss Path 1
        towards_boss1.connect(towards_boss2, AND(KEY3, FOUND(KEY3, 6))) # Boss Path 1 <--> Boss Path 2
        towards_boss2.connect(towards_boss3, AND(KEY3, FOUND(KEY3, 7))) # Boss Path 2 <--> Boss Path 3
        towards_boss3.connect(towards_boss4, AND(KEY3, FOUND(KEY3, 8))) # Boss Path 3 <--> Boss Path 4
        towards_boss4.connect(three_pairodd_room, AND(FEATHER, PEGASUS_BOOTS)) # Boss Path 4 <--> Three Pairodd Room
        three_pairodd_room.connect(pre_boss, r.enemy_requirements["PAIRODD"]) # Three Pairodd Room <--> Room Before Boss
        pre_boss.connect(pre_boss_drop7, r.enemy_requirements["KEESE"]) # Room Before Boss <--> Nightmare Door Key
        pre_boss.connect(boss_room, NIGHTMARE_KEY3) # Room Before Boss <--> Boss Room
        boss_room.connect(boss, r.boss_requirements[world_setup.boss_mapping[2]]) # Boss Room <--> Boss Rewards

        # key logic patch
        if options.dungeon_items not in {'localnightmarekey', 'keysanity', 'keysy', 'smallkeys'}:
            # Without keysanity we need to fix the keylogic here, else we can never generate proper placement.
            west_4way.connect(center_4way, KEY3)
            west_4way_drop2.items[0].forced_item = KEY3
            south_4way.connect(center_4way, KEY3)
            south_4way_drop1.items[0].forced_item = KEY3

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            entrance.connect(after_vacuum, r.hookshot_over_pit) # hookshot the chest to get to the right side
            north_4way.connect(before_a_stairs_chest5, AND(r.throw_pot), one_way=True) # after hit switch get zol switch chest
            north_4way.connect(swordstalfos_room, AND(r.throw_pot, r.enemy_requirements["HIDING_ZOL"]), one_way=True) # hit switch with pot, and go back to stalfos pedestal chest
            south_4way.connect(south_4way_drop1, r.throw_pot) # use pots to kill enemies
            north_4way.connect(north_4way_drop3, r.throw_pot) # use pots to kill the enemies
            fenced_walkway.connect(three_bombite_room_drop_6, BOOMERANG, one_way=True) # 3 bombite room from the walkway, grab item with boomerang

        if options.logic == 'glitched' or options.logic == 'hell':
            #TODO: before_a_stairs.connect(west_hallway, r.hookshot_clip_block)
            #TODO: west_hallway.connect(before_a_stairs_chest5, r.shaq_jump, r.enemy_requirements["GEL"], r.enemy_requirements["STALFOS_EVASIVE"], one_way=True) # considers dungeon enemizer for if you can't clear zol room
            swordstalfos_entry.connect(swordstalfos_room, r.super_jump_feather) # use superjump to get over the bottom left block
            before_a_stairs.connect(before_a_stairs_chest5, AND(OR(PEGASUS_BOOTS, r.hookshot_clip_block), r.shaq_jump)) #TODO: connect from west hallway for less logic (?) -  boots from south or hookshot clip weith pushblock & zols to get behing the chest, then shaq jump using the pushblock to get on raised platforms
            before_a_stairs.connect(before_a_stairs_chest4, AND(r.enemy_requirements["GEL"], r.enemy_requirements["STALFOS_EVASIVE"], r.hookshot_clip_block)) # hookshot clip through the northern push block next to raised blocks chest to get to the zol
            big_pit_room.connect(ledge_pre_pit, r.super_jump_feather) # superjump to right side 3 gap via top wall and jump the 2 gap
            #TODO: towards_boss1.connect(miniboss_room, r.super_jump_feather)
            towards_boss2.connect(after_miniboss_room, r.super_jump_feather) # superjump from keyblock path. use 2 keys to open enough blocks 
        
        if options.logic == 'hell':
            #TODO: entrance.connect(after_vacuum, SWORD) # just hold right, more reliable with sword TODO: Tracker hell without sword?
            #TODO: west_hallway.connect(before_a_stairs, r.boots_superhop) # use boots superhop off top wall or left wall to get on raised blocks - keep this logic in case dungeon enemizer, maybe slime room can't be cleared with arrow or rod
            #TODO: west_hallway.connect(before_a_stairs_chest4, r.boots_superhop) # when the switch hasn't been hit (no key) this trick applies
            swordstalfos_entry.connect(swordstalfos_room, r.boots_superhop) # use boots superhop to get over the bottom left block
            swordstalfos_entry.connect(swordstalfos_room, r.hookshot_clip_block) # facing downwards at the pushblock, spam hookshot while a keese passes by
            before_a_stairs.connect(before_a_stairs_chest5, r.boots_superhop, one_way=True) # TODO: CHANGE - connect from west_hallway instead - use boots superhop off top wall or left wall to get on raised blocks
            #TODO: before_a_stairs.connect(west_hallway, r.super_bump) # setup shaq jump off push block and use shield bump to jump over the pushblock
            #TODO: before_a_stairs.connect(before_a_stairs_chest5, r.super_bump) # shaq jump into super bump using zols to land on pegs
            north_4way.connect(before_a_stairs_chest4, AND(OR(r.hit_switch, r.throw_pot), AND(r.super_jump_feather, r.enemy_requirements["GEL"], r.enemy_requirements["STALFOS_EVASIVE"])), one_way=True) #TODO: move to glitched? - use superjump near top blocks chest to get to zol without boots, keep wall clip on right wall to get a clip on left wall or use obstacles
            west_4way.connect(west_4way_drop2, r.shield_bump) # knock everything into the pit including the teleporting owls
            south_4way.connect(south_4way_drop1, r.shield_bump) # knock everything into the pit including the teleporting owls
            #TODO: main_room.connect(fenced_walkway, r.super_bump) # super bump off zols to go past pushblock to the fenced walkway
            #TODO: ledge_pre_pit.connect(ledge_post_pit, r.shield_bump) # shield bump stalfos multiple times to get around pits to nightmare key
            main_room.connect(ledge_pre_pit, AND(r.super_jump_feather, r.shield_bump)) # superjump into jumping stalfos and shield bump to right ledge
            big_pit_room.connect(ledge_pre_pit, r.pit_buffer_boots) # boots bonk across the pits with pit buffering and then hookshot or shield bump to the chest
            #TODO: big_pit_room.connect(ledge_pre_pit, r.hookshot_spam_pit) # hookshot spam to get across 3 block pit and then you can hookshot to nightmare key chest [VERYHARD] - Tracker Hell?
            #TODO: main_room.connect(towards_boss3, r.super_bump, one_way=True) # super bump off stalfos to get in between boss key block 3 and 4. it's possible to land wall clipped, leading to the next trick:
            #TODO: towards_boss3.connect(after_miniboss_room_chest8, r.super_jump_feather, one_way=True) # feather-only super jump facing right into boots chest area
            fenced_walkway.connect(three_bombite_room, AND(r.enemy_requirements["TIMER_BOMBITE"], OR(BOW, MAGIC_ROD, AND(OR(FEATHER, PEGASUS_BOOTS), OR(SWORD, MAGIC_POWDER)))), one_way=True) # 3 bombite room from the left side, use a bombite to blow open the wall without bombs
            towards_boss4.connect(three_pairodd_room, AND(FEATHER, POWER_BRACELET)) # TODO: REMOVE and replace with or(toadstool, bracelet) # current logic was for clearing first half with bracelet, second half with feather
            #TODO: towards_boss4.connect(three_pairodd_room, r.toadstool_bounce_2d_hell) # bracelet or toadstool to get damage boost from 2d spikes to get through passage
            towards_boss4.connect(three_pairodd_room, AND(r.enemy_requirements["PAIRODD"], r.boots_bonk_2d_spikepit)) # use medicine invulnerability to pass through the 2d section with a boots bonk to reach the staircase
            #TODO: consider logic for passageway in reverse, sould some tricks be labeled one-way? Is there different strategies for traversing this passage in reverse? Being mindful of staircase rando

        self.entrance = entrance
        self.final_room = boss


class NoDungeon3:
    def __init__(self, options, world_setup, r):
        entrance = Location("D3 Entrance", dungeon=3)
        Location(dungeon=3).add(HeartContainer(0x15A), Instrument(0x159)).connect(entrance, AND(POWER_BRACELET, r.boss_requirements[
            world_setup.boss_mapping[2]]))

        self.entrance = entrance
