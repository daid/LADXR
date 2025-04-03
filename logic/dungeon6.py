from .requirements import *
from .location import Location
from locations.all import *


class Dungeon6:
    def __init__(self, options, world_setup, r, *, raft_game_chest=True):

        # locations
        entrance = Location("D6 Entrance", dungeon=6)
        entrance_owl1 = Location(dungeon=6).add(OwlStatue(0x1BB)) # hint
        entrance_switch = Location("D6 Entrance Switch", dungeon=6).add(KeyLocation("SWITCH6A"))
        entrance_switch_range = Location("D6 Entrance Switch (Range)", dungeon=6).add(KeyLocation("SWITCH6A_RANGE"))
        first_elephant_room = Location("D6 1st Statue & Chest Room", dungeon=6)
        first_elephant_room_chest1 = Location(dungeon=6).add(DungeonChest(0x1CF)) # 50 rupees
        second_elephant_room = Location("D6 2nd Statue & Chest Room", dungeon=6)
        second_elephant_room_chest2 = Location(dungeon=6).add(DungeonChest(0x1C9)) # 100 rupees
        dark_room = Location("D6 Dark Room", dungeon=6)
        before_a_passage = Location("D6 Dark Room Stairs Spawn", dungeon=6)
        after_a_passage = Location("D6 Passage Inside Pegs", dungeon=6)
        pre_bracelet_room = Location("D6 Before L2 Bracelet Room", dungeon=6)
        bracelet_room = Location("D6 L2 Bracelet Room", dungeon=6)
        bracelet_room_chest3 = Location(dungeon=6).add(DungeonChest(0x1CE)) # L2 bracelet
        after_potbutton_door = Location("D6 After Button Door", dungeon=6)
        after_potbutton_door_chest4 = Location(dungeon=6).add(DungeonChest(0x1C0)) # map
        three_wizrobe_area = Location("D6 Wizrobe Peg Area", dungeon=6)
        three_wizrobe_area_switched = Location("D6 Wizrobe Peg Area (Switched)", dungeon=6)
        three_wizrobe_area_chest5 = Location(dungeon=6).add(DungeonChest(0x1B9)) # beak
        three_wizrobe_area_switch_range = Location("D6 Wizrobe Peg Area Switch", dungeon=6).add(KeyLocation("SWITCH6B_RANGE"))
        star_area = Location("D6 NW Star Area", dungeon=6)
        star_area_switched = Location("D6 NW Star Area (Switched)", dungeon=6)
        star_area_switch = Location("D6 NW Star Area Switch", dungeon=6).add(KeyLocation("SWITCH6C"))
        star_area_chest6 = Location(dungeon=6).add(DungeonChest(0x1B3)) # compass
        star_area_drop1 = Location(dungeon=6).add(DroppedKey(0x1B4)) # small key
        top_left_room = Location("D6 NW Horsehead Room", dungeon=6)
        top_left_room_chest7 = Location(dungeon=6).add(DungeonChest(0x1B0)) # 100 rupees
        top_left_room_switch = Location("D6 NW Horsehead witch", dungeon=6).add(KeyLocation("SWITCH6D"))
        top_left_exit = Location("D6 NW Exit Staircase", dungeon=6)
        rapids_island = Location("D6 Raft Ride Island")
        before_miniboss = Location("D6 Before Miniboss", dungeon=6)
        miniboss_room = Location("D6 Miniboss Room", dungeon=6)
        after_miniboss = Location("D6 After Miniboss", dungeon=6)
        before_b_passage = Location("D6 Statue Stairs Revealed", dungeon=6)
        after_b_passage = Location("D6 2nd Floating Tile Fight", dungeon=6)
        after_b_passage_drop2 = Location(dungeon=6).add(DroppedKey(0x1C3)) # small key
        flying_bomb_room = Location("D6 Flying Bomb Room", dungeon=6)
        before_c_passage = Location("D6 Passageway Below Torch", dungeon=6)
        four_wizrobe_room = Location("D6 Four Wizrobe Room", dungeon=6)
        blade_trap_room = Location("D6 Blade Trap Room", dungeon=6)
        blade_trap_room_owl2 = Location(dungeon=6).add(OwlStatue(0x1D7)) # hint
        after_blade_trap = Location("D6 Ledge After Blade", dungeon=6)
        after_blade_trap_chest8 = Location(dungeon=6).add(DungeonChest(0x1D1)) # medicine
        waterway = Location("D6 Waterway", dungeon=6)
        waterway_chest9 = Location(dungeon=6).add(DungeonChest(0x1BE)) # small key
        after_c_passage = Location("D6 Pols Room", dungeon=6)
        before_spark_pot_maze = Location("D6 Before Pot Maze", dungeon=6)
        after_spark_pot_maze = Location("D6 After Pot Maze", dungeon=6)
        top_right_room = Location("D6 NE Horsehead Room", dungeon=6)
        top_right_room_switch = Location("D6 NE Horsehead Switch", dungeon=6).add(KeyLocation("SWITCH6E"))
        top_right_room_chest10 = Location(dungeon=6).add(DungeonChest(0x1B1)) # 50 rupees
        dodongo_room = Location("D6 Dodongo Room", dungeon=6)
        waterway_east_ledge = Location("D6 Outside Dodongo Room", dungeon=6)
        hookshot_block = Location("D6 Waterway Hookshot Block", dungeon=6)
        waterway_west_ledge = Location("D6 Star Ledge", dungeon=6)
        pot_area = Location("D6 Pot Owl Area", dungeon=6)
        pot_area_owl3 = Location(dungeon=6).add(OwlStatue(0x1B6)) # hint
        pot_area_switch = Location("D6 Pot Owl Area Switch", dungeon=6).add(KeyLocation("SWITCH6F"))
        pot_area_chest11 = Location(dungeon=6).add(DungeonChest(0x1B6)) # nightmare key
        vacuum_room = Location("D6 Vacuum Room", dungeon=6)
        laser_turret_room = Location("D6 Laser Turret Room", dungeon=6)
        pre_boss_room = Location("D6 Room Before Boss", dungeon=6)
        boss_room = Location("D6 Boss Room", dungeon=6)
        boss_room_drop3 = Location(dungeon=6).add(HeartContainer(0x1BC)) # heart container
        instrument = Location("D6 Instrument Room", dungeon=6).add(Instrument(0x1b5)) # coral triangle
    
        # back exit
        if raft_game_chest:
            rapids_island_chest11 = Location().add(Chest(0x06C)) # seashell
            rapids_island.connect(rapids_island_chest11, back=False) #TODO: remove POWER_BRACELET requirement as staircase is accessible by default, connection in reverse is already  handled in connections

        # owl statues
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            entrance.connect(entrance_owl1, STONE_BEAK6, back=False)
            blade_trap_room.connect(blade_trap_room_owl2, AND(POWER_BRACELET, STONE_BEAK6), back=False) #TODO: REMOVE and replace with if statement
            #TODO: if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
                #TODO: blade_trap_room.connect(blade_trap_room_owl2, STONE_BEAK6, back=False)
            #TODO: else:
                #TODO: blade_trap_room.connect(blade_trap_room_owl2, AND(POWER_BRACELET, STONE_BEAK6), back=False)
            pot_area.connect(pot_area_owl3, STONE_BEAK6, back=False)
        
        # connections
        # entrance
        entrance.connect(entrance_switch, r.hit_switch, back=False)
        entrance.connect(entrance_switch_range, OR(BOMB, BOOMERANG), back=False) #TODO: delete in favor of casual logic statement
        entrance.connect(first_elephant_room, r.enemy_requirements["WIZROBE"], back=None)
        entrance.connect(second_elephant_room, COUNT(POWER_BRACELET, 2), back=None)
        first_elephant_room.connect(first_elephant_room_chest1, back=False)
        first_elephant_room.connect(second_elephant_room, COUNT(POWER_BRACELET, 2))
        second_elephant_room.connect(second_elephant_room_chest2, back=False)
        entrance.connect(dark_room, BOMB)
        dark_room.connect(before_a_passage, r.enemy_requirements["HIDING_ZOL"], back=None)
        before_a_passage.connect(after_a_passage, FEATHER)
        after_a_passage.connect(pre_bracelet_room, "SWITCH6A", back=False)
        pre_bracelet_room.connect(bracelet_room, AND(r.enemy_requirements["MINI_MOLDORM"], r.enemy_requirements["WIZROBE"]), back=False)
        bracelet_room.connect(bracelet_room_chest3, back=False)
        bracelet_room.connect(entrance, COUNT(POWER_BRACELET, 2), back=False)
        # west
        entrance.connect(after_potbutton_door, POWER_BRACELET, back=None)
        entrance.connect(three_wizrobe_area_switched, AND("SWITCH6A_RANGE", POWER_BRACELET), back=OR("SWITCH6B_RANGE", "SWITCH6C", "SWITCH6D")) # any switch in northwest area is the requirement to get to entrance
        after_potbutton_door.connect(after_potbutton_door_chest4, r.enemy_requirements["WIZROBE"], back=False) #TODO: REPLACE with below
        #TODO: after_potbutton_door.connect(after_potbutton_door_chest4, OR(BOMB, MAGIC_ROD), back=False) # only bomb and rod can kill all wizrobes while trapped behind pegs
        three_wizrobe_area.connect(after_potbutton_door_chest4, AND(OR("SWITCH6B_RANGE", "SWITCH6C", "SWITCH6D"), r.enemy_requirements["WIZROBE"]), back=False) #TODO: 12-arrow room if got here with only bracelet+bow
        three_wizrobe_area_chest5.connect((three_wizrobe_area, three_wizrobe_area_switched), False, back=None)
        three_wizrobe_area.connect(three_wizrobe_area_switch_range, OR(BOMB, BOW, MAGIC_ROD, BOOMERANG, HOOKSHOT), back=False) # have to stand on pegs while hitting switch for it to be useful
        three_wizrobe_area.connect(three_wizrobe_area_switched, "SWITCH6B_RANGE", back=AND(MAGIC_ROD, BOW, BOMB))
        three_wizrobe_area.connect(star_area, AND("SWITCH6B_RANGE", POWER_BRACELET), back=None)
        three_wizrobe_area_switched.connect(star_area_switched, POWER_BRACELET, back=None)
        # northwest
        star_area_switch.connect((star_area, star_area_switched), False, back=r.hit_switch)
        star_area_switched.connect(star_area, "SWITCH6C")
        star_area.connect(star_area_chest6, back=False)
        star_area.connect(star_area_drop1, OR(r.enemy_requirements["WIZROBE"], BOW), back=False) # add bow since it's just two wizrobes (8 arrows)
        star_area.connect(top_left_room, COUNT(POWER_BRACELET, 2), back=POWER_BRACELET) # solve horseheads and then jump off return ledge to skip L2 bracelet requirement
        top_left_room.connect(top_left_room_chest7, back=False)
        top_left_room.connect(top_left_room_switch, r.hit_switch, back=False)
        top_left_room.connect(top_left_exit)
        top_left_exit.connect(rapids_island)
        # miniboss
        entrance.connect(before_miniboss, FOUND(KEY6, 1))
        before_miniboss.connect(miniboss_room, BOMB)
        miniboss_room.connect(entrance, r.miniboss_requirements[world_setup.miniboss_mapping[5]], back=False) # miniboss portal
        miniboss_room.connect(after_miniboss, r.miniboss_requirements[world_setup.miniboss_mapping[5]], back=COUNT(POWER_BRACELET, 2))
        after_miniboss.connect(before_b_passage, COUNT(POWER_BRACELET, 2), back=None)
        #TODO: after_miniboss.connect(before_miniboss, FOUND(KEY6, 1), back=False) # walk north in room north of miniboss to wrap around NOTE: will get stuck in door if don't have a key
        # center
        before_b_passage.connect(after_b_passage, FEATHER)
        after_b_passage.connect(after_b_passage_drop2, back=False)
        after_b_passage.connect(flying_bomb_room, FOUND(KEY6, 2))
        flying_bomb_room.connect(before_c_passage, COUNT(POWER_BRACELET, 2), back=POWER_BRACELET)
        before_c_passage.connect(after_c_passage, PEGASUS_BOOTS)
        # southeast
        entrance.connect(four_wizrobe_room, COUNT(POWER_BRACELET, 2), back=r.enemy_requirements["WIZROBE"])
        four_wizrobe_room.connect(blade_trap_room, r.enemy_requirements["WIZROBE"], back=r.enemy_requirements["STAR"])
        blade_trap_room.connect(after_blade_trap, AND(FEATHER, OR("SWITCH6A", "SWITCH6E", "SWITCH6F")), back=None)
        after_blade_trap.connect((after_blade_trap_chest8, four_wizrobe_room), back=False)
        four_wizrobe_room.connect(waterway, r.enemy_requirements["WIZROBE"], back=None) #NOTE: not possible to get through tektites itemless without taking damage - problem for OHKO mode
        waterway.connect(waterway_chest9, back=False)
        waterway.connect((hookshot_block, waterway_east_ledge), False, back=None) # jump down into waterway
        # northeast
        after_c_passage.connect(before_spark_pot_maze, r.enemy_requirements["POLS_VOICE"], back=None)
        before_spark_pot_maze.connect(after_spark_pot_maze, POWER_BRACELET) #TODO: REMOVE this and replace with casual statement
        after_spark_pot_maze.connect(top_right_room, POWER_BRACELET)
        top_right_room.connect(top_right_room_chest10, back=False)
        top_right_room.connect(top_right_room_switch, r.hit_switch, back=False)
        after_c_passage.connect(dodongo_room, r.enemy_requirements["POLS_VOICE"], back=OR(FEATHER, r.miniboss_requirements["DODONGO"]))
        dodongo_room.connect(waterway_east_ledge, r.miniboss_requirements["DODONGO"], back=None)
        waterway_east_ledge.connect(hookshot_block, HOOKSHOT, back=False)
        hookshot_block.connect(waterway_west_ledge, FOUND(KEY6, 3))
        waterway_west_ledge.connect(pot_area, POWER_BRACELET, back=False)
        pot_area.connect(pot_area_chest11, POWER_BRACELET, back=False)
        pot_area.connect(pot_area_switch, r.hit_switch, back=False)
        # boss
        after_b_passage.connect(vacuum_room, back=False)
        vacuum_room.connect(pre_boss_room, OR(SHIELD, AND(r.enemy_requirements["HIDING_ZOL"], r.enemy_requirements["WIZROBE"])), back=False) #TODO: REMOVE, replace with statement below as well as casual/hard logic
        #TODO: laser_turret_room.connect(pre_boss_room, AND(FEATHER, OR(SWORD, SHIELD, HOOKSHOT, BOOMERANG, r.enemy_requirements["WIZROBE"])), back=False) 
        pre_boss_room.connect(boss_room, NIGHTMARE_KEY6, back=r.boss_requirements[world_setup.boss_mapping[5]])
        boss_room.connect((boss_room_drop3, instrument), r.boss_requirements[world_setup.boss_mapping[5]], back=False)

        #TODO: if options.logic == "casual":
            #TODO: entrance.connect(entrance_switch_range, BOMB, back=False) # diagonal boomerang throw removed for casual
            #TODO: before_spark_pot_maze.connect(after_spark_pot_maze, AND(POWER_BRACELET) OR(FEATHER, AND((r.enemy_requirements["SPARK_COUNTER_CLOCKWISE"]), (r.enemy_requirements["SPARK_CLOCKWISE"])))) # give the player a way to deal with sparks
            #TODO: vacuum_room.connect(laser_turret_room, r.enemy_requirements["HIDING_ZOL"], back=False)

        #TODO: else:
            #TODO: entrance.connect(entrance_switch_range, OR(BOMB, BOOMERANG)) # hit switch while standing on peg
            #TODO: before_spark_pot_maze.connect(top_right_room, AND(FEATHER, POWER_BRACELET)) # jump over the sparks, but no boomerang like casual
            #TODO: vacuum_room.connect(laser_turret_room, back=False) # vacuum pulls the zols into the pit

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            before_a_passage.connect(after_a_passage) # get through 2d section by "fake" jumping to the ladders, if in reverse, hold A to get more distance
            three_wizrobe_area.connect(three_wizrobe_area_switch_range, AND(r.stun_wizrobe, r.throw_enemy), back=False) # stun wizrobe with powder and throw it at switch - hard due to obscurity
            before_b_passage.connect(after_b_passage, r.boots_dash_2d, back=AND(r.boots_dash_2d, r.boots_bonk)) # boots dash over 1 block gaps in sidescroller
            after_c_passage.connect(before_c_passage, r.damage_boost) # damage_boost past the thwimps #TODO: consider removing damage_boost
            #TODO: before_spark_pot_maze.connect(after_spark_pot_maze, AND(POWER_BRACELET, r.damage_boost)) #TODO: consider removing damage_boost
            #TODO: laser_turret_room.connect(pre_boss_room, AND(r.diagonal_walk, OR(SWORD, SHIELD, HOOKSHOT, BOOMERANG, r.enemy_requirements["WIZROBE"])), back=False) 
            
        if options.logic == 'glitched' or options.logic == 'hell':
            first_elephant_room.connect(second_elephant_room, AND(r.enemy_requirements["MINI_MOLDORM"], r.bomb_trigger), back=False) # kill moldorm from hallway with spark, then bomb trigger through the doorway to break elephant statue
            after_potbutton_door.connect(three_wizrobe_area, r.super_jump_feather, back=False) # path from entrance to left_side: use superjumps to pass raised blocks
            three_wizrobe_area.connect(star_area, AND(r.super_jump_feather, POWER_BRACELET), back=False) # delayed superjump onto raised pegs so that you can pick up pot without switch hitter
            after_c_passage.connect(dodongo_room, r.super_jump_feather, back=False) # superjump to get from pols to dodongos without kill requirements
            after_miniboss.connect(before_b_passage, AND(r.bomb_trigger, r.miniboss_requirements[world_setup.miniboss_mapping[5]], FOUND(KEY6, 1)), back=False) # go through north door exits to wrap-around, then bomb trigger as you transition into 2-statue room #NOTE: left the requirements of entire loop in for stairs shuffle
            flying_bomb_room.connect(after_b_passage, OR(r.shaq_jump, r.super_jump_feather), back=False) # face left and shaq jump off keyblock to get into floating tile room
            flying_bomb_room.connect(entrance, r.super_jump_feather, back=False) # superjumps in corridor to get up to owl statue
            waterway.connect(waterway_east_ledge, r.super_jump, back=False) # superjump from waterway towards dodongos - glitched with weapon assisted superjump, but hell when feather-only
            waterway.connect(waterway_west_ledge, r.super_jump_feather, back=AND(POWER_BRACELET, r.super_jump_feather)) # superjump from waterway to the left, sj return is possible to avoid spending key, but need bracelet to move pots first

        if options.logic == 'hell':
            #TODO: entrance.connect(second_elephant_room, AND(OR(FEATHER, r.boots_superhop), OR(SWORD, HOOKSHOT, POWER_BRACELET, SHOVEL, "TOADSTOOL2"), OR(r.ledge_super_poke, r.ledge_super_bump)), back=False) # super jump into wall, manipulate mimic into position, walk off the ledge while holding sword or shield to slowly get to door with it never closing
            entrance.connect(entrance_switch_range, AND(r.stun_mask_mimic, r.throw_enemy), back=False) #TODO: REMOVE and replace with below
            #TODO: entrance.connect(entrance_switch_range, OR(AND(r.stun_mask_mimic, r.throw_enemy), SWORD), back=False) # spin attack while walking up to step onto peg as it raises, or stun and throw mask mimic
            entrance.connect(three_wizrobe_area_switched, AND("SWITCH6A", r.boots_superhop, POWER_BRACELET), back=False) # boots superhop onto peg
            after_potbutton_door.connect(three_wizrobe_area, r.boots_superhop, back=False) # boots superhop onto peg
            three_wizrobe_area.connect(three_wizrobe_area_switch_range, AND(r.stun_wizrobe, r.throw_enemy), back=False) #TODO: REMOVE and replace with below
            #TODO: three_wizrobe_area.connect(three_wizrobe_area_switch_range, OR(AND(r.stun_wizrobe, r.throw_enemy), SWORD), back=False) # spin attack while walking up to step onto peg as it raises, or stun and throw wizrobe
            three_wizrobe_area.connect(star_area, AND(r.boots_superhop, POWER_BRACELET), back=False) # boots superhop onto peg to get to pots needed to break door
            before_b_passage.connect(after_b_passage, r.damage_boost_special, back=False) #TODO: REPLACE with below
            #TODO: before_b_passage.connect(after_b_passage, r.damage_boost_special, back="TOADSTOOL2") # going left: damage boost off both sparks to get across or going right: use toadstool to damage boost off of spikes and get through passageway. Also helps to hold A button when airborne
            blade_trap_room.connect(after_blade_trap, r.boots_superhop, back=False) # can boots superhop off the top wall with bow or magic rod
            waterway.connect(waterway_east_ledge, r.super_jump_feather, back=False) # superjump from waterway towards dodongos. glitched with weapon assisted superjump, but hell when feather-only
            dodongo_room.connect(after_c_passage, r.boots_bonk, back=False) # boots bonk to escape dodongo room NE corner

        self.entrance = entrance
        self.final_room = instrument


class NoDungeon6:
    def __init__(self, options, world_setup, r):
        entrance = Location("D6 Entrance", dungeon=6)
        Location(dungeon=6).add(HeartContainer(0x1BC), Instrument(0x1b5)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[5]])
        self.entrance = entrance
