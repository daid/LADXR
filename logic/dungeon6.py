from .requirements import *
from .location import Location
from locations.all import *


class Dungeon6:
    def __init__(self, options, world_setup, r, *, raft_game_chest=True):

        # locations
        entrance = Location("D6 Entrance", dungeon=6)
        first_elephant_room = Location("D6 Elephant & Chest Room", dungeon=6)
        first_elephant_room_chest1 = Location(dungeon=6).add(DungeonChest(0x1CF)) # 50 rupees
        second_elephant_room = Location("D6 Flying Heart & Statue Room", dungeon=6)
        second_elephant_room_chest2 = Location(dungeon=6).add(DungeonChest(0x1C9)) # 100 rupees
        dark_room = Location("D6 Dark Room", dungeon=6)
        before_a_passage = Location("D6 Dark Room Stairs Spawn", dungeon=6)
        after_a_passage = Location("D6 Inside Pegs Before L2 Bracelet Chest", dungeon=6)
        pre_bracelet_room = Location("D6 Outside Pegs Before L2 Bracelet Room", dungeon=6)
        bracelet_room = Location("D6 L2 Bracelet Room", dungeon=6)
        bracelet_room_chest3 = Location(dungeon=6).add(DungeonChest(0x1CE)) # L2 bracelet
        wizrobe_switch_room = Location("D6 Wizrobe Switch Room", dungeon=6)
        wizrobe_switch_room_chest4 = Location(dungeon=6).add(DungeonChest(0x1C0)) # map
        south_star_area = Location("D6 Before Northwest Area", dungeon=6)
        south_star_area_chest5 = Location(dungeon=6).add(DungeonChest(0x1B9)) # beak
        star_area = Location("D6 Northwest Area", dungeon=6)
        star_area_chest6 = Location(dungeon=6).add(DungeonChest(0x1B3)) # compass
        star_area_drop1 = Location(dungeon=6).add(DroppedKey(0x1B4)) # small key
        top_left_room = Location("D6 Northwest Horse Head Room", dungeon=6)
        top_left_room_chest7 = Location(dungeon=6).add(DungeonChest(0x1B0)) # 100 rupees
        before_miniboss = Location("D6 Before Miniboss", dungeon=6)
        miniboss_room = Location("D6 Miniboss Room", dungeon=6)
        after_miniboss = Location("D6 After Miniboss", dungeon=6)
        before_b_passage = Location("D6 Boss Passageway Revealed", dungeon=6)
        after_b_passage = Location("D6 Second Floating Tile Fight", dungeon=6)
        after_b_passage_drop2 = Location(dungeon=6).add(DroppedKey(0x1C3)) # small key
        four_wizrobe_room = Location("D6 Four Wizrobe Room", dungeon=6)
        blade_trap_room = Location("D6 Blade Trap Room", dungeon=6)
        after_blade_trap = Location("D6 Ledge After Blade Trap", dungeon=6)
        after_blade_trap_chest8 = Location(dungeon=6).add(DungeonChest(0x1D1)) # medicine
        waterway = Location("D6 Waterway", dungeon=6)
        waterway_chest9 = Location(dungeon=6).add(DungeonChest(0x1BE)) # small key
        dodongo_room = Location("D6 Dodongo Room", dungeon=6)
        waterway_east_ledge = Location("D6 Outside Dodongo Room", dungeon=6)
        hookshot_block = Location("D6 Waterway Hookshot Block", dungeon=6)
        waterway_west_ledge = Location("D6 Ledge Left of Waterway", dungeon=6)
        pot_area = Location("D6 Pot Owl Area", dungeon=6)
        pot_ring_chest11 = Location(dungeon=6).add(DungeonChest(0x1B6)) # nightmare key
        after_c_passage = Location("D6 Pols Room", dungeon=6)
        spark_pot_maze = Location("D6 Spark & Pot Maze", dungeon=6)
        top_right_room = Location("D6 Northeast Horse Head Room", dungeon=6)
        top_right_room_chest10 = Location(dungeon=6).add(DungeonChest(0x1B1)) #50 rupees
        before_c_passage = Location("D6 Stairs West of Horsehead Hallway", dungeon=6)
        flying_bomb_room = Location("D6 Flying Bomb Room", dungeon=6)
        vacuum_room = Location("D6 Vacuum Room", dungeon=6)
        laser_turret_room = Location("D6 Laser Turret Room", dungeon=6)
        pre_boss_room = Location("D6 Room Before Boss", dungeon=6)
        boss_room = Location("D6 Boss Room", dungeon=6)
        boss_room_drop3 = Location(dungeon=6).add(HeartContainer(0x1BC)) # heart container
        instrument = Location("D6 Instrument Room", dungeon=6).add(Instrument(0x1b5)) # coral triangle
    
        if raft_game_chest:
            Location().add(Chest(0x06C)).connect(top_left_room, POWER_BRACELET) # seashell chest in raft game #TODO: remove POWER_BRACELET requirement as staircase is accessible by default, connection in reverse is already  handled in connections

        # owl statues
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=6).add(OwlStatue(0x1BB)).connect(entrance, STONE_BEAK6) # Entrance <--> Corridor Owl
            Location(dungeon=6).add(OwlStatue(0x1D7)).connect(blade_trap_room, AND(POWER_BRACELET, STONE_BEAK6)) # Blade Trap Room <--> Blade Trap Owl #TODO: add hard/glitched logic for this check (face left into pot and press A)
            Location(dungeon=6).add(OwlStatue(0x1B6)).connect(pot_area, STONE_BEAK6) # Pot Owl Area <--> Pot Owl
        

        # connections
        # west
        entrance.connect(first_elephant_room, r.enemy_requirements["WIZROBE"]) # Entrance <--> Elephant & Chest Room
        first_elephant_room.connect(first_elephant_room_chest1, None) # Elephant & Chest Room <--> Mini-Moldorm, Spark Chest
        first_elephant_room.connect(second_elephant_room, COUNT(POWER_BRACELET, 2)) # Elephant & Chest Room <--> Flying Heart & Statue Room
        entrance.connect(second_elephant_room, COUNT(POWER_BRACELET, 2)) # Entrance <--> Flying Heart & Statue Room
        second_elephant_room.connect(second_elephant_room_chest2, None) # Flying Heart & Statue Room <--> Flying Heart, Statue Chest
        entrance.connect(dark_room, BOMB) # Entrance <--> Dark Room
        dark_room.connect(before_a_passage, r.enemy_requirements["HIDING_ZOL"]) # Dark Room <--> Dark Room Stairs Spawn #TODO: drop kill requirement for stairs shuffle when arriving from before_a_passage
        before_a_passage.connect(after_a_passage, FEATHER) # Dark Room Stairs Spawn <--> Inside Pegs Before L2 Bracelet Chest
        after_a_passage.connect(pre_bracelet_room, r.hit_switch, one_way=True) # Inside Pegs Before L2 Bracelet Chest --> Outside Pegs Before L2 Bracelet Room #TODO: Consider connect with fake SWITCH_6 item for consciseness, goal for stair shuffle preparedness
        pre_bracelet_room.connect(bracelet_room, AND(r.enemy_requirements["MINI_MOLDORM"], r.enemy_requirements["WIZROBE"])) # Outside Pegs Before L2 Bracelet Room <--> L2 Bracelet Room
        bracelet_room.connect(bracelet_room_chest3, None) # L2 Bracelet Room <--> L2 Bracelet Chest
        bracelet_room.connect(entrance, COUNT(POWER_BRACELET, 2), one_way=True) # L2 Bracelet Room --> Entrance
        entrance.connect(wizrobe_switch_room, POWER_BRACELET) # Entrance <--> Wizrobe Switch Room
        entrance.connect(south_star_area, AND(POWER_BRACELET, OR(BOMB, BOOMERANG))) #TODO: delete in favor of casual logic commented out below #TODO: Consider connect with fake SWITCH_6 item for consciseness, goal for stair shuffle preparedness
        wizrobe_switch_room.connect(wizrobe_switch_room_chest4, r.enemy_requirements["WIZROBE"]) # Wizrobe Switch Room <--> Three Wizrobe, Switch Chest #TODO: 12-arrow room if got here with only bracelet+bow
        south_star_area.connect(south_star_area_chest5, None) # Before Northwest Area <--> Stairs Across Statues Chest
        south_star_area.connect(star_area, AND(POWER_BRACELET, OR(BOMB, BOW, MAGIC_ROD, BOOMERANG, HOOKSHOT))) # Before Northwest Area <--> Northwest Area
        star_area.connect(south_star_area, None, one_way=True) # Northwest Area --> Before Northwest Area
        star_area.connect(star_area_chest6, None) # Northwest Area <--> Switch, Star Above Statues Chest
        star_area.connect(star_area_drop1, OR(r.enemy_requirements["WIZROBE"], BOW)) # Northwest Area <--> Two Wizrobe Key
        star_area.connect(top_left_room, COUNT(POWER_BRACELET, 2)) # Northwest Area <--> Northwest Horse Head Room
        top_left_room.connect(star_area, POWER_BRACELET, one_way=True) # Northwest Horse Head Room --> Northwest Area
        top_left_room.connect(top_left_room_chest7, None) # Northwest Horse Head Room <--> Top Left Horse Heads Chest
        # miniboss
        entrance.connect(before_miniboss, FOUND(KEY6, 1)) # Entrance <--> Before Miniboss
        before_miniboss.connect(miniboss_room, BOMB) # Before Miniboss <--> Miniboss Room
        miniboss_room.connect(after_miniboss, r.miniboss_requirements[world_setup.miniboss_mapping[5]], one_way=True) # Miniboss Room --> After Miniboss
        after_miniboss.connect(miniboss_room, COUNT(POWER_BRACELET, 2), one_way=True) # After Miniboss --> Miniboss Room
        after_miniboss.connect(before_b_passage, COUNT(POWER_BRACELET, 2), one_way=True) # After Miniboss --> Boss Passageway Revealed
        before_b_passage.connect(after_miniboss, None, one_way=True) # Boss Passageway Revealed --> After Miniboss
        #TODO: after_miniboss.connect(before_miniboss, None, one_way=True) # walk north in room north of miniboss to wrap around. NOTE: get stuck in door if you haven't defeated the miniboss, but you can use items to be closer to screen edge, probably oob
        # east
        entrance.connect(four_wizrobe_room, COUNT(POWER_BRACELET, 2), one_way=True) # Entrance --> Four Wizrobe Room
        four_wizrobe_room.connect(entrance, r.enemy_requirements["WIZROBE"], one_way=True) # Four Wizrobe Room --> Entrance
        four_wizrobe_room.connect(blade_trap_room, r.enemy_requirements["WIZROBE"], one_way=True) # Four Wizrobe Room --> Blade Trap Room
        blade_trap_room.connect(after_blade_trap, AND(FEATHER, r.hit_switch), one_way=True) #  --> Ledge After Blade Trap #TODO: Consider connect with fake SWITCH_6 item for consciseness, goal for stair shuffle preparedness
        after_blade_trap.connect(after_blade_trap_chest8, None) # Ledge After Blade Trap <--> Four Wizrobe Ledge Chest
        after_blade_trap.connect(four_wizrobe_room, None, one_way=True) # Ledge After Blade Trap --> Four Wizrobe Room
        four_wizrobe_room.connect(waterway,r.enemy_requirements["WIZROBE"]) # Four Wizrobe Room <--> Waterway #TODO: technically one_way
        waterway.connect(waterway_chest9, None) # Waterway <--> Water Tektite Chest
        dodongo_room.connect(after_c_passage, OR(FEATHER, r.miniboss_requirements["DODONGO"]), one_way=True) # Dodongo Room --> Pols Room
        after_c_passage.connect(spark_pot_maze, r.enemy_requirements["POLS_VOICE"]) # Pols Room <--> Spark & Pot Maze
        after_c_passage.connect(dodongo_room, r.enemy_requirements["POLS_VOICE"], one_way=True) # Pols Room --> Dodongo Room
        spark_pot_maze.connect(top_right_room, POWER_BRACELET) # Spark & Pot Maze <--> Northeast Horse Head Room
        top_right_room.connect(top_right_room_chest10, None) # Northeast Horse Head Room <--> Top Right Horse Heads Chest
        dodongo_room.connect(waterway_east_ledge, r.miniboss_requirements["DODONGO"]) # Dodongo Room <--> Outside Dodongo Room
        waterway_east_ledge.connect(dodongo_room, None, one_way=True) # Outside Dodongo Room --> Dodongo Room
        waterway_east_ledge.connect(waterway, None, one_way=True) # Outside Dodongo Room --> Waterway
        waterway_east_ledge.connect(hookshot_block, HOOKSHOT, one_way=True) # Outside Dodongo Room --> Waterway Hookshot Block
        hookshot_block.connect(waterway_west_ledge, FOUND(KEY6, 3)) # Waterway Hookshot Block --> Ledge Left of Waterway
        waterway_west_ledge.connect(pot_area, POWER_BRACELET) # Ledge Left of Waterway <--> Pot Owl Area
        pot_area.connect(pot_ring_chest11, POWER_BRACELET) # Pot Owl Area <--> Pot Locked Chest
        # boss
        before_b_passage.connect(after_b_passage, FEATHER) # Boss Passageway Revealed <--> Second Floating Tile Fight
        after_c_passage.connect(before_c_passage, PEGASUS_BOOTS) # Pols Room <--> Stairs West of Horsehead Hallway
        before_c_passage.connect(flying_bomb_room, POWER_BRACELET, one_way=True) # Stairs West of Horsehead Hallway --> Flying Bomb Room
        flying_bomb_room.connect(before_c_passage, COUNT(POWER_BRACELET, 2)) # Flying Bomb Room <--> Stairs West of Horsehead Hallway
        flying_bomb_room.connect(after_b_passage, FOUND(KEY6, 2)) # Flying Bomb Room <--> Second Floating Tile Fight
        after_b_passage.connect(after_b_passage_drop2, None) # Second Floating Tile Fight <--> Tile Room Key
        # boss
        after_b_passage.connect(vacuum_room, None) # Second Floating Tile Fight <--> Vacuum Room
        vacuum_room.connect(pre_boss_room, OR(SHIELD, AND(r.enemy_requirements["HIDING_ZOL"], r.enemy_requirements["WIZROBE"]))) # Vacuum Room <--> Room Before Boss #TODO: REMOVE, it's covered in casual logic statement
        #TODO: laser_turret_room.connect(pre_boss_room, OR(SWORD, SHIELD, HOOKSHOT, BOOMERANG, r.enemy_requirements["WIZROBE"])) # Laser Turret Room <--> Room Before Boss #TODO: ADD ways to knock wizrobe into pit
        pre_boss_room.connect(boss_room, NIGHTMARE_KEY6) # Room Before Boss <--> Boss Room
        boss_room.connect(boss_room_drop3, r.boss_requirements[world_setup.boss_mapping[5]]) # Boss Room <--> Heart Container
        boss_room.connect(instrument, r.boss_requirements[world_setup.boss_mapping[5]]) # Boss Room <--> Instrument Room

        #TODO: if options.logic == "casual":
            #TODO: entrance.connect(south_star_area, AND(POWER_BRACELET, BOMB)) # Entrance <--> Before Northwest Area # diagonal boomerang throw removed for casual
            #TODO: spark_pot_maze.connect(top_right_room,AND(POWER_BRACELET) OR(FEATHER, AND((r.enemy_requirements["SPARK_COUNTER_CLOCKWISE"]), (r.enemy_requirements["SPARK_CLOCKWISE"])))) # give the player a way to deal with sparks
            #TODO: vacuum_room.connect(laser_turret_room, r.enemy_requirements["HIDING_ZOL"]) # Vacuum Room <--> Laser Turret Room

        #TODO: else:
            #TODO: entrance.connect(south_star_area, AND(POWER_BRACELET, OR(BOMB, BOOMERANG))) # Entrance <--> Before Northwest Area
            #TODO: spark_pot_maze.connect(top_right_room, POWER_BRACELET) # Spark & Pot Maze <--> Northeast Horse Head Room # it's possible to get through without taking damage
            #TODO: vacuum_room.connect(laser_turret_room, None) # Vacuum Room <--> Laser Turret Room

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            before_a_passage.connect(after_a_passage, None) # get through 2d section by "fake" jumping to the ladders, if in reverse, hold A to get more distance
            #TODO: south_star_area.connect(star_area, AND(OR(AND(r.stun_wizrobe, r.throw_enemy), FOUND(SWORD, 2), POWER_BRACELET) # L2 sword beam, or stun wizrobe with powder and throw it at switch to get access to pots to throw at door - hard due to obscurity
            before_b_passage.connect(after_b_passage, r.boots_dash_2d, one_way=True) # boots dash over 1 block gaps in sidescroller
            after_b_passage.connect(before_b_passage, AND(r.boots_dash_2d, r.boots_bonk), one_way=True) # boots dash over 1 block gaps in sidescroller, then bonk to get on ladder
            after_c_passage.connect(before_c_passage, r.damage_boost) # damage_boost past the mini_thwomps
            #TODO: determine what difficulty the itemless c_passage thromp manip should be and add it to logic
            #TODO: spark_pot_maze.connect(top_right_room, AND(POWER_BRACELET)) #[logic prep for staircase rando] # it's possible to pass through the room with only bracelet and not take damage, but it's hard
            
        if options.logic == 'glitched' or options.logic == 'hell':
            first_elephant_room.connect(second_elephant_room, r.bomb_trigger) # kill moldorm on screen above wizrobes, then bomb trigger on the right side to break elephant statue to get to the second chest
            wizrobe_switch_room.connect(south_star_area, r.super_jump_feather, one_way=True) # path from entrance to left_side: use superjumps to pass raised blocks
            south_star_area.connect(star_area, AND(r.super_jump_feather, POWER_BRACELET)) # delayed superjump onto raised pegs so that you can pick up pot without switch hitter
            after_c_passage.connect(dodongo_room, r.super_jump_feather, one_way=True) # superjump to get from pols to dodongos without kill requirements
            after_miniboss.connect(before_b_passage, r.bomb_trigger) # go through north door exits to wrap-around, then bomb trigger as you transition into 2-statue room
            flying_bomb_room.connect(after_b_passage, r.shaq_jump, one_way=True) # face left and shaq jump off keyblock to get into floating tile room
            waterway.connect(waterway_east_ledge, r.super_jump, one_way=True) # superjump from waterway towards dodongos. glitched with weapon assisted superjump, but hell when feather-only
            waterway.connect(waterway_west_ledge, r.super_jump_feather) # superjump from waterway to the left.

        if options.logic == 'hell':
            #TODO: entrance.connect(second_elephant_room, AND(OR(FEATHER, r.boots_superhop), OR(SWORD, HOOKSHOT, POWER_BRACELET, SHOVEL, "TOADSTOOL2"), OR(r.ledge_super_poke, r.ledge_super_bump))) # super jump into wall, manipulate mimic into position, walk off the ledge while holding sword or shield to slowly get to door with it never closing
            entrance.connect(south_star_area, AND(POWER_BRACELET, r.boots_superhop)) #TODO: REMOVE and replace with below
            entrance.connect(south_star_area, AND(POWER_BRACELET, r.stun_mask_mimic, r.throw_enemy), one_way=True) #TODO: REMOVE and replace with below
            #TODO: entrance.connect(south_star_area, AND(POWER_BRACELET, OR(r.boots_superhop, AND(r.stun_mask_mimic, r.throw_enemy), SWORD)), one_way=True) # very difficult ways to hit the switch while making it over the peg - stun and throw the mask mimic up at the wall and run, or spin atack whilc walking to the peg while wall clipped, or normal boots superhop from NW corner of room
            #TODO: south_star_area.connect(star_area, AND(SWORD, POWER_BRACELET) # hit three wizrobe room switch with sword beam (L2) or spin attack while facing up and a well timed up-press to step onto peg as it raises
            before_b_passage.connect(after_b_passage, r.damage_boost_special) #TODO: change to one_way - #use a double damage boost from the sparks to get across (first one is free, second one needs to buffer while in midair for spark to get close enough)
            #TODO: before_b_passage.connect(after_b_passage, "TOADSTOOL2") # use toadstool to damage boost off of spikes and get through passageway. Also helps to hold A button when airborne
            blade_trap_room.connect(after_blade_trap, r.boots_superhop) # can boots superhop off the top wall with bow or magic rod
            waterway.connect(waterway_east_ledge, r.super_jump_feather, one_way=True) # superjump from waterway towards dodongos. glitched with weapon assisted superjump, but hell when feather-only
            dodongo_room.connect(after_c_passage, r.boots_bonk, one_way=True) # boots bonk to escape dodongo room NE corner

            #TODO: consider fake "SWITCH_6" item for conciseness and preparedness for stair shuffle

        self.entrance = entrance
        self.final_room = instrument


class NoDungeon6:
    def __init__(self, options, world_setup, r):
        entrance = Location("D6 Entrance", dungeon=6)
        Location(dungeon=6).add(HeartContainer(0x1BC), Instrument(0x1b5)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[5]])
        self.entrance = entrance
