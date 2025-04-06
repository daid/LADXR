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
        potbutton_area_switched = Location("D6 Hidden Button Area", dungeon=6)
        fenced_walkway_switched = Location("D6 Fenced Walkway", dungeon=6)
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
        three_wizrobe_area_clear = Location("D6 Wizrobe Peg Room Clear", dungeon=6).add(KeyLocation("D6_THREE_WIZROBE_CLEAR"))
        three_wizrobe_area_switch_midrange = Location("D6 Wizrobe Peg Area Switch", dungeon=6).add(KeyLocation("SWITCH6B_MIDRANGE"))
        three_wizrobe_area_switch_range = Location("D6 Wizrobe Peg Area Switch (Range)", dungeon=6).add(KeyLocation("SWITCH6B_RANGE"))
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
        south_waterway = Location("D6 South Waterway", dungeon=6)
        north_waterway = Location("D6 North Waterway", dungeon=6)
        north_waterway_chest9 = Location(dungeon=6).add(DungeonChest(0x1BE)) # small key
        after_c_passage = Location("D6 Pols Room", dungeon=6)
        south_spark_pot_maze = Location("D6 Before Pot Maze", dungeon=6)
        north_spark_pot_maze = Location("D6 After Pot Maze", dungeon=6)
        top_right_room = Location("D6 NE Horsehead Room", dungeon=6)
        top_right_room_switch = Location("D6 NE Horsehead Switch", dungeon=6).add(KeyLocation("SWITCH6E"))
        top_right_room_chest10 = Location(dungeon=6).add(DungeonChest(0x1B1)) # 50 rupees
        dodongo_room = Location("D6 Dodongo Room", dungeon=6)
        north_waterway_east_ledge = Location("D6 Outside Dodongo Room", dungeon=6)
        hookshot_block = Location("D6 North Waterway Hookshot Block", dungeon=6)
        north_waterway_west_ledge = Location("D6 Star Ledge", dungeon=6)
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
            entrance_owl1.connect((entrance, fenced_walkway_switched), False, back=STONE_BEAK6)
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
        dark_room.connect(entrance, BOMB) #NOTE: with a rom patch for remembering switch state, could connect dark room to fenced_walkway_switched with OR(all switches)
        first_elephant_room.connect(first_elephant_room_chest1, back=False)
        first_elephant_room.connect(second_elephant_room, COUNT(POWER_BRACELET, 2))
        second_elephant_room.connect(second_elephant_room_chest2, back=False)
        dark_room.connect(before_a_passage, r.enemy_requirements["HIDING_ZOL"], back=None)
        before_a_passage.connect(after_a_passage, FEATHER)
        after_a_passage.connect(pre_bracelet_room, OR("SWITCH6A"), back=False) #NOTE: with a rom patch for remembering switch state, could update this to be OR(all switches) for stairs shuffle. Currently just entrance switch (range) for cosmetic reasons
        pre_bracelet_room.connect(bracelet_room, AND(r.enemy_requirements["MINI_MOLDORM"], r.enemy_requirements["WIZROBE"]), back=False)
        bracelet_room.connect(bracelet_room_chest3, back=False)
        bracelet_room.connect(entrance, COUNT(POWER_BRACELET, 2), back=False)
        # west
        entrance.connect(after_potbutton_door, POWER_BRACELET, back=None)
        entrance.connect((fenced_walkway_switched, potbutton_area_switched), "SWITCH6A_RANGE", back=False)
        fenced_walkway_switched.connect(potbutton_area_switched, back=False) # ledge drop
        potbutton_area_switched.connect(three_wizrobe_area_switched, POWER_BRACELET, back=None)
        after_potbutton_door.connect(three_wizrobe_area_clear, r.enemy_requirements["WIZROBE"], back=False) #TODO: REPLACE with below
        #TODO: after_potbutton_door.connect(three_wizrobe_area_clear, OR(BOMB, MAGIC_ROD)) # excludes bow when can't reach arrow refill on the other side of pegs
        after_potbutton_door.connect(after_potbutton_door_chest4, "D6_THREE_WIZROBE_CLEAR", back=False)
        three_wizrobe_area.connect(after_potbutton_door, "SWITCH6B_RANGE")
        three_wizrobe_area.connect(three_wizrobe_area_switch_midrange, OR(BOMB, BOW, MAGIC_ROD, BOOMERANG, HOOKSHOT), back=False) # hit switch from lowered pegs nearby
        three_wizrobe_area.connect(three_wizrobe_area_switch_range, OR(BOMB, BOW, MAGIC_ROD, BOOMERANG), back=False)  # get on right-side pegs before your item toggles the switch, hookshot can't go through pegs so it's removed
        three_wizrobe_area.connect(three_wizrobe_area_switched, "SWITCH6B_MIDRANGE", back=OR(BOMB, BOW, MAGIC_ROD, BOOMERANG))
        three_wizrobe_area_clear.connect((three_wizrobe_area, three_wizrobe_area_switched), False, back=r.enemy_requirements["WIZROBE"])
        three_wizrobe_area_chest5.connect((three_wizrobe_area, three_wizrobe_area_switched), False, back=None)
        three_wizrobe_area_switched.connect(star_area_switched, POWER_BRACELET, back=None)
        # northwest
        star_area.connect(three_wizrobe_area, back=False)
        star_area_switch.connect((star_area, star_area_switched), False, back=r.hit_switch)
        star_area_switched.connect(star_area, "SWITCH6C")
        star_area_chest6.connect((star_area, star_area_switched), False, back=None)
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
        entrance.connect(four_wizrobe_room, COUNT(POWER_BRACELET, 2), back=False)
        four_wizrobe_room.connect((entrance, blade_trap_room, south_waterway), r.enemy_requirements["WIZROBE"], back=False)
        south_waterway.connect(north_waterway) #TODO: REMOVE and replace with other commented logic
        #TODO: south_waterway.connect(north_waterway, OR(FEATHER, r.enemy_requirements["TEKTITE"])) # impossible to avoid damage from tektites, so jump over or kill them
        blade_trap_room.connect(four_wizrobe_room, r.enemy_requirements["STAR"], back=False)
        blade_trap_room.connect(after_blade_trap, AND(FEATHER, OR("SWITCH6A", "SWITCH6E", "SWITCH6F")), back=None)
        after_blade_trap.connect((after_blade_trap_chest8, four_wizrobe_room), back=False)
        north_waterway.connect(north_waterway_chest9, back=False)
        north_waterway.connect((hookshot_block, north_waterway_east_ledge), False, back=None) # jump down into north_waterway
        # northeast
        after_c_passage.connect(south_spark_pot_maze, r.enemy_requirements["POLS_VOICE"], back=None)
        after_c_passage.connect(dodongo_room, r.enemy_requirements["POLS_VOICE"], back=OR(FEATHER, r.miniboss_requirements["DODONGO"]))
        south_spark_pot_maze.connect(north_spark_pot_maze, POWER_BRACELET) #TODO: REMOVE this and replace with casual statement
        north_spark_pot_maze.connect(top_right_room, POWER_BRACELET)
        top_right_room.connect(top_right_room_chest10, back=False)
        top_right_room.connect(top_right_room_switch, r.hit_switch, back=False)
        dodongo_room.connect(north_waterway_east_ledge, r.miniboss_requirements["DODONGO"], back=None)
        north_waterway_east_ledge.connect(hookshot_block, HOOKSHOT, back=False)
        hookshot_block.connect(north_waterway_west_ledge, FOUND(KEY6, 3))
        north_waterway_west_ledge.connect(pot_area, POWER_BRACELET, back=False)
        pot_area.connect(pot_area_chest11, POWER_BRACELET, back=False)
        pot_area.connect(pot_area_switch, r.hit_switch, back=False)
        # boss
        after_b_passage.connect(vacuum_room, back=False)
        vacuum_room.connect(pre_boss_room, OR(SHIELD, AND(r.enemy_requirements["HIDING_ZOL"], r.enemy_requirements["WIZROBE"])), back=False) #TODO: REMOVE, replace with statement below as well as casual/hard logic
        #TODO: laser_turret_room.connect(pre_boss_room, AND(FEATHER, OR(SWORD, SHIELD, HOOKSHOT, BOOMERANG, r.enemy_requirements["WIZROBE"])), back=False) 
        pre_boss_room.connect(boss_room, NIGHTMARE_KEY6, back=False)
        boss_room.connect((boss_room_drop3, instrument), r.boss_requirements[world_setup.boss_mapping[5]], back=False)

        #TODO: if options.logic == "casual":
            #TODO: entrance.connect(entrance_switch_range, BOMB, back=False) # diagonal boomerang throw removed for casual
            #TODO: south_waterway.connect(north_waterway, AND(r.enemy_requirements["TEKTITE"], r.enemy_requirements["STAR"], OR(r.enemy_requirements["SPARK_CLOCKWISE"]))) # give a bit more options for dealing with enemies in tight corridor
            #TODO: south_spark_pot_maze.connect(north_spark_pot_maze, AND(POWER_BRACELET) OR(FEATHER, AND((r.enemy_requirements["SPARK_COUNTER_CLOCKWISE"]), (r.enemy_requirements["SPARK_CLOCKWISE"])))) # give the player a way to deal with sparks
            #TODO: vacuum_room.connect(laser_turret_room, r.enemy_requirements["HIDING_ZOL"], back=False)

        #TODO: else:
            #TODO: entrance.connect(entrance_switch_range, OR(BOMB, BOOMERANG)) # hit switch while standing on peg
            #TODO: south_waterway.connect(north_waterway, AND(r.enemy_requirements["TEKTITE"], FEATHER)) # impossible to avoid damage from tektites, so jump over or kill them
            #TODO: south_spark_pot_maze.connect(top_right_room, AND(FEATHER, POWER_BRACELET)) # jump over the sparks, but no boomerang like casual
            #TODO: vacuum_room.connect(laser_turret_room, back=False) # vacuum pulls the zols into the pit

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            entrance.connect(entrance_switch, AND(r.stun_mask_mimic, r.throw_enemy), back=False)
            before_a_passage.connect(after_a_passage) # get through 2d section by "fake" jumping to the ladders, if in reverse, hold A to get more distance
            three_wizrobe_area.connect(three_wizrobe_area_switch_midrange, AND(r.stun_wizrobe, r.throw_enemy), back=False) # stun wizrobe with powder and throw it at switch - hard due to obscurity
            #TODO: three_wizrobe_area_clear.connect((three_wizrobe_area, three_wizrobe_area_switched), False, back=AND(FEATHER, BOW)) # bring 2 arrows + feather to grab 10 arrow refill - 12 needed to kill 3 wizrobes
            #TODO: four_wizrobe_room.connect((entrance, blade_trap_room, south_waterway), AND(FEATHER, BOW), back=False) # bring 6 arrows, + feather to grab 10 arrow refill - 16 arrows total to clear room
            #TODO: south_waterway.connect(north_waterway, r.damage_boost) # forced damage from tektites if no weapons
            before_b_passage.connect(after_b_passage, r.boots_dash_2d, back=AND(r.boots_dash_2d, r.boots_bonk)) # boots dash over 1 block gaps in sidescroller
            after_c_passage.connect(south_spark_pot_maze, AND(r.throw_pot, OR(BOW, AND(r.stun_wizrobe, r.throw_enemy))), back=False) # kill one pol with 4 arrows or stun+throw, kill remaining two with pots
            after_c_passage.connect(dodongo_room, AND(r.throw_pot, OR(BOW, AND(r.stun_wizrobe, r.throw_enemy))), back=False) # kill one pol with 4 arrows or stun+throw, kill remaining two with pots
            after_c_passage.connect(before_c_passage, r.damage_boost) # damage_boost past the thwimps #TODO: consider removing damage_boost
            #TODO: south_spark_pot_maze.connect(north_spark_pot_maze, AND(POWER_BRACELET, r.damage_boost)) #TODO: consider removing damage_boost
            #TODO: laser_turret_room.connect(pre_boss_room, AND(r.diagonal_walk, OR(SWORD, SHIELD, HOOKSHOT, BOOMERANG, r.enemy_requirements["WIZROBE"])), back=False)
            #TODO: pot_area.connect(pot_area_switch, r.throw_pot, back=False) # stair shuffle or enemizer relevance only - can't get normally here without bombs
            
        if options.logic == 'glitched' or options.logic == 'hell':
            first_elephant_room.connect(second_elephant_room, AND(r.enemy_requirements["MINI_MOLDORM"], r.bomb_trigger), back=False) # kill moldorm in hallway, then bomb trigger through the doorway to break elephant statue, irrelevant in reverse since the door is L2 bracelet locked
            after_potbutton_door.connect(three_wizrobe_area, r.super_jump_feather, back=False) # path from entrance to left_side: use superjumps to pass raised blocks
            three_wizrobe_area.connect(star_area, AND(r.super_jump_feather, POWER_BRACELET), back=False) # delayed superjump onto raised pegs so that you can pick up pot without switch hitter
            potbutton_area_switched.connect(entrance, r.shaq_jump, back=False)
            after_c_passage.connect(dodongo_room, r.super_jump_feather, back=False) # superjump to get from pols to dodongos without kill requirements
            after_miniboss.connect(before_b_passage, AND(r.bomb_trigger, r.miniboss_requirements[world_setup.miniboss_mapping[5]], FOUND(KEY6, 1)), back=False) # go through north door exits to wrap-around, then bomb trigger as you transition into 2-statue room #NOTE: left the requirements of entire loop in for stairs shuffle
            flying_bomb_room.connect(after_b_passage, OR(r.shaq_jump, r.super_jump_feather), back=False) # face left and shaq jump off keyblock to get into floating tile room
            flying_bomb_room.connect(entrance, r.super_jump_feather, back=False) # superjumps in corridor to get up to owl statue
            north_waterway.connect(north_waterway_east_ledge, r.super_jump, back=False) # superjump from north_waterway towards dodongos - feather-only variant in hell only
            north_waterway.connect(north_waterway_west_ledge, r.super_jump_feather, back=False) # superjump from north_waterway to the left

        if options.logic == 'hell':
            #TODO: entrance.connect(second_elephant_room, AND(OR(FEATHER, r.boots_superhop), OR(SWORD, HOOKSHOT, POWER_BRACELET, SHOVEL, "TOADSTOOL2"), OR(r.ledge_super_poke, r.ledge_super_bump)), back=False) # super jump into wall, manipulate mimic into position, walk off the ledge while holding sword or shield to slowly get to door with it never closing
            entrance.connect(entrance_switch_range, AND(r.stun_mask_mimic, r.throw_enemy), back=False) #TODO: REMOVE and replace with below
            #TODO: entrance.connect(entrance_switch_range, OR(AND(r.stun_mask_mimic, r.throw_enemy), SWORD), back=False) # spin attack while walking up to step onto peg as it raises, or stun and throw mask mimic
            entrance.connect(potbutton_area_switched, AND("SWITCH6A", OR(r.boots_superhop, AND(r.super_jump_feather, r.boots_jump))), back=r.boots_superhop) # boots superhop onto top left peg or wall clip and superjump to bottom-left peg and then boots jump to top left peg
            after_potbutton_door.connect(three_wizrobe_area, r.boots_superhop, back=OR(r.boots_superhop, r.super_jump_boots, "SWITCH6B_RANGE")) # get over the pegs blocking the east doorway
            #TODO: three_wizrobe_area.connect(three_wizrobe_area_switch_midrange, SWORD, back=False) # spin attack while walking up to step onto peg as it raise
            #TODO: three_wizrobe_area.connect(three_wizrobe_area_switch_range, OR(AND(r.stun_wizrobe, r.throw_enemy), COUNT(SWORD, 2), AND(HOOKSHOT, FEATHER)), back=False) # stun+throw wizrobe or while on raised pegs, L2 sword beam, or hit switch with hookshot and feather on the frame the hokshot returns to link to stay on second layer
            three_wizrobe_area.connect(star_area, AND(r.boots_superhop, POWER_BRACELET), back=False) # boots superhop onto peg to get to pots needed to break door
            before_b_passage.connect(after_b_passage, r.damage_boost_special, back=False) #TODO: REPLACE with below
            #TODO: before_b_passage.connect(after_b_passage, r.damage_boost_special, back="TOADSTOOL2") # going left: damage boost off both sparks to get across or going right: use toadstool to damage boost off of spikes and get through passageway. Also helps to hold A button when airborne
            blade_trap_room.connect(after_blade_trap, r.boots_superhop, back=False) # can boots superhop off the top wall with bow or magic rod
            north_waterway.connect(north_waterway_east_ledge, r.super_jump_feather, back=False) # superjump from north_waterway towards dodongos. glitched with weapon assisted superjump, but hell when feather-only
            dodongo_room.connect(after_c_passage, r.boots_bonk, back=False) # boots bonk to escape dodongo room NE corner

        self.entrance = entrance
        self.final_room = instrument


class NoDungeon6:
    def __init__(self, options, world_setup, r):
        entrance = Location("D6 Entrance", dungeon=6)
        Location(dungeon=6).add(HeartContainer(0x1BC), Instrument(0x1b5)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[5]])
        self.entrance = entrance
