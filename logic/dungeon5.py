from .requirements import *
from .location import Location
from locations.all import *


class Dungeon5:
    def __init__(self, options, world_setup, r):

        # locations
        entrance = Location("D5 Entrance", dungeon=5)
        entrance_ledge = Location("D5 Entrance Ledge", dungeon=5)
        entrance_ledge_chest1 = Location(dungeon=5).add(DungeonChest(0x1A0)) # 200 rupees
        before_a_passage = Location("D5 Room West of Entrance", dungeon=5)
        before_a_passage_chest2 = Location(dungeon=5).add(DungeonChest(0x19E)) # compass
        after_a_passage = Location("D5 Crystal Room Entrance", dungeon=5)
        crystal_room = Location("D5 Crystal Room", dungeon=5)
        crystal_room_drop1 = Location(dungeon=5).add(DroppedKey(0x181)) # small key
        crystal_puddle_room = Location("D5 Crystal River Area", dungeon=5)
        crystal_puddle_room_owl1 = Location(dungeon=5).add(OwlStatue(0x19A)) # hint
        messy_room = Location("D5 Messy Room", dungeon=5)
        messy_room_chest3 = Location(dungeon=5).add(DungeonChest(0x19B)) # beak?
        statue_room = Location("D5 Fireball Statue Room", dungeon=5)
        after_blade_trap = Location("D5 After Blade Trap", dungeon=5)
        pot_column_room = Location("D5 Pot Column Room", dungeon=5)
        pot_column_room_chest4 = Location(dungeon=5).add(DungeonChest(0x197)) # small key
        before_miniboss = Location("D5 Before Miniboss", dungeon=5)
        miniboss_room = Location("D5 Miniboss Room", dungeon=5)
        before_c_passage = Location("D5 After Miniboss", dungeon=5)
        after_c_passage = Location("D5 Before Boss Keyblock", dungeon=5)
        after_boss_keyblock = Location("D5 After Boss Keyblock", dungeon=5)
        ms_1_room = Location("D5 Master Stalfos 1", dungeon=5)
        ms_1_victory = Location("D5 Master Stalfos 1 Victory", dungeon=5).add(KeyLocation("MS1_KILL"))
        before_d_passage = Location("D5 South of Crossroads", dungeon=5)
        before_d_passage_chest5 = Location(dungeon=5).add(DungeonChest(0x196)) # master stalfos message
        after_d_passage = Location("D5 Fireball Torches Room", dungeon=5)
        star_room = Location("D5 Star Owl Room", dungeon=5)
        star_room_owl2 = Location(dungeon=5).add(OwlStatue(0x18A)) # hint
        spark_hallway = Location("D5 Spark Hallway", dungeon=5)
        north_crossroads = Location("D5 North of Crossroads", dungeon=5)
        single_tile_ledge = Location("D5 Hookshot Tile", dungeon=5)
        middle_ledge = Location("D5 1st Ledge", dungeon=5)
        middle_ledge_chest6 = Location(dungeon=5).add(DungeonChest(0x18E)) # 50 rupees
        north_ledge = Location("D5 North Ledge", dungeon=5)
        north_ledge_chest_7 = Location(dungeon=5).add(DungeonChest(0x188)) # 50 rupees
        east_ledge = Location("D5 East Ledge", dungeon=5)
        east_ledge_chest8 = Location(dungeon=5).add(DungeonChest(0x18F)) # small key
        ms_2_room = Location("D5 Master Stalfos 2", dungeon=5)
        ms_2_victory = Location("D5 Master Stalfos 2 Victory", dungeon=5).add(KeyLocation("MS2_KILL"))
        west_crossroads = Location("D5 West of Crossroads", dungeon=5)
        west_crossroads_zol_clear = Location("D5 Zol Above Water Defeated", dungeon=5).add(KeyLocation("D5_ZOL_CLEAR"))
        before_b_passage = Location("D5 Water Passage Entrance", dungeon=5)
        after_b_passage = Location("D5 Bridge Room Entrance", dungeon=5)
        boss_key_room = Location("D5 Bridge Room", dungeon=5)
        boss_key_room_chest10 = Location(dungeon=5).add(DungeonChest(0x186))  # nightmare key
        ms_3_room = Location("D5 Master Stalfos 3", dungeon=5)
        ms_3_victory = Location("D5 Master Stalfos 3 Victory", dungeon=5).add(KeyLocation("MS3_KILL"))
        pot_locked_room = Location("D5 Pot Locked Room", dungeon=5)
        pot_locked_room_chest9 = Location(dungeon=5).add(DungeonChest(0x183))
        ms_4_room = Location("D5 Master Stalfos 4", dungeon=5)
        ms_4_room_drop2 = Location("D5 Master Stalfos 4 Victory", dungeon=5).add(HookshotDrop()) # hookshot
        pre_boss_room = Location("D5 Before Boss", dungeon=5)
        boss_room = Location("D5 Boss Room", dungeon=5)
        boss_room_drop3 = Location(dungeon=5).add(HeartContainer(0x185)) # heart container
        instrument = Location("D5 Instrument Room", dungeon=5).add(Instrument(0x182)) # wind marimba

        # owl statues
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            crystal_puddle_room.connect(crystal_puddle_room_owl1, STONE_BEAK5)
            star_room.connect(star_room_owl2, STONE_BEAK5)

        # connections
        # entrance / ms1
        entrance.connect(entrance_ledge, HOOKSHOT, back=False)
        entrance_ledge.connect(entrance_ledge_chest1, back=False)
        entrance.connect(before_a_passage, AND(r.enemy_requirements["KEESE"], r.enemy_requirements["IRON_MASK"]), back=r.enemy_requirements["IRON_MASK"])
        entrance.connect(crystal_puddle_room, FOUND(KEY5, 1))
        before_a_passage.connect(before_a_passage_chest2, back=False)
        crystal_puddle_room.connect(messy_room, r.enemy_requirements["IRON_MASK"], back=False)
        crystal_puddle_room.connect(statue_room, r.enemy_requirements["IRON_MASK"], back=None)
        crystal_puddle_room.connect(ms_1_room, AND(r.enemy_requirements["STALFOS_AGGRESSIVE"], r.enemy_requirements["STALFOS_EVASIVE"]), back=False)
        messy_room.connect(messy_room_chest3, r.enemy_requirements["IRON_MASK"], back=False)
        ms_1_room.connect((ms_1_victory, crystal_puddle_room, before_d_passage), r.enemy_requirements["MASTER_STALFOS"], back=False)
        before_d_passage.connect(ms_1_room, back=False)
        # crossroads
        before_d_passage.connect(before_d_passage_chest5, back=False)
        before_d_passage.connect(north_crossroads, FEATHER)
        before_d_passage.connect(after_d_passage, FEATHER)
        before_d_passage.connect((west_crossroads, ms_2_room))
        west_crossroads.connect(west_crossroads_zol_clear, r.enemy_requirements["HIDING_ZOL"], back=False)
        ms_2_room.connect(ms_2_victory, r.enemy_requirements["MASTER_STALFOS"], back=False)
        north_crossroads.connect(single_tile_ledge, HOOKSHOT, back=False)
        north_crossroads.connect(single_tile_ledge, FEATHER)
        single_tile_ledge.connect(middle_ledge, AND(FEATHER, PEGASUS_BOOTS))
        single_tile_ledge.connect(middle_ledge, HOOKSHOT, back=False)
        middle_ledge.connect(middle_ledge_chest6, back=False)
        middle_ledge.connect(east_ledge, HOOKSHOT)
        east_ledge.connect(east_ledge_chest8, back=False)
        middle_ledge.connect(north_ledge, HOOKSHOT, back=False)
        north_ledge.connect(north_ledge_chest_7, back=False)
        north_ledge.connect(north_crossroads, HOOKSHOT)
        north_crossroads.connect(ms_3_room, AND("D5_ZOL_CLEAR", r.enemy_requirements["HIDING_ZOL"]), back=False)
        ms_3_room.connect(ms_3_victory, AND("MS1_KILL", "MS2_KILL", r.enemy_requirements["MASTER_STALFOS"]), back=False)
        ms_3_room.connect(pot_locked_room, POWER_BRACELET, back=False)
        pot_locked_room.connect(pot_locked_room_chest9, AND(r.enemy_requirements["STALFOS_AGGRESSIVE"], r.enemy_requirements["STALFOS_EVASIVE"]), back=False) #TODO: remove kill enemy requirements, it's just here to make logic match stable
        
        # ms4
        before_a_passage.connect(after_a_passage, FEATHER)
        after_a_passage.connect(crystal_room, SWORD, back=False)
        crystal_room.connect(crystal_room_drop1, SWORD, back=False)
        crystal_room.connect(ms_4_room, back=False)
        ms_4_room.connect(ms_4_room_drop2, AND("MS3_KILL", r.enemy_requirements["MASTER_STALFOS"]), back=False)
        # boss key
        west_crossroads.connect(before_b_passage, FLIPPERS)
        before_b_passage.connect(after_b_passage, FLIPPERS)
        after_b_passage.connect(boss_key_room, HOOKSHOT, back=False)
        boss_key_room.connect(boss_key_room_chest10, back=False)
        # miniboss
        statue_room.connect((after_blade_trap, before_miniboss), HOOKSHOT, back=False)
        after_blade_trap.connect(pot_column_room, HOOKSHOT, back=None)
        pot_column_room.connect(pot_column_room_chest4, back=False)
        before_miniboss.connect(miniboss_room, FOUND(KEY5, 2))
        miniboss_room.connect((entrance, before_c_passage), r.miniboss_requirements[world_setup.miniboss_mapping[4]], back=False) # miniboss portal and exit door
        before_c_passage.connect(before_miniboss, POWER_BRACELET, back=False)
        star_room.connect((after_d_passage, spark_hallway), r.enemy_requirements["STAR"], back=None)
        spark_hallway.connect(after_c_passage, back=False)
        before_c_passage.connect(after_c_passage, AND(HOOKSHOT, FEATHER), back=FEATHER)
        # boss
        after_c_passage.connect(after_boss_keyblock, FOUND(KEY5, 3))
        after_boss_keyblock.connect(pre_boss_room, HOOKSHOT)
        pre_boss_room.connect(boss_room, NIGHTMARE_KEY5, back=False)
        boss_room.connect((boss_room_drop3, instrument), r.boss_requirements[world_setup.boss_mapping[4]], back=False)

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            statue_room.connect(after_blade_trap, FEATHER, back=False) # jump past the blade traps
            after_blade_trap.connect(pot_column_room, r.tight_jump, back=False) # tight jump south to get across huge pit
            #TODO: before_miniboss.connect(statue_room, HOOKSHOT) # open the bridge by hookshotting up while almost standing in pit
            after_a_passage.connect(before_a_passage, r.boots_bonk, back=False) # only takes one boots bonk to get on last ladder
            before_d_passage.connect(after_d_passage, r.boots_bonk) # boots charge + bonk to cross 2d bridge #TODO: move to hell?
            before_c_passage.connect(after_c_passage, AND(r.boots_bonk, HOOKSHOT), back=r.boots_bonk) # boots bonk in 2d section to skip feather #TODO: move to hell?
            spark_hallway.connect(after_boss_keyblock, r.tight_jump) # jump from bottom left to top right, skipping the keyblock
            spark_hallway.connect(pre_boss_room, r.boots_jump, back=False) # cross pits room from bottom left to top left with boots jump
            before_d_passage.connect(single_tile_ledge, r.hookshot_over_pit, back=False) # walk into pit and hookshot right to get to single tile ledge
            single_tile_ledge.connect(north_crossroads, r.diagonal_walk) # walk diagonally between pits to get to north crossroads
            north_ledge.connect(middle_ledge, HOOKSHOT, back=False) # open the bridge by hookshotting up while almost standing in pit
            middle_ledge.connect(north_crossroads, r.tight_jump) # tight jump to/from first chest ledge, helps but not required to start wall clipped
            after_b_passage.connect(boss_key_room, r.boots_jump, back=False) # boots jump across
            #TODO: north_crossroads.connect(west_crossroads_zol_clear, OR(SWORD, BOMB), back=False) # left side zol can only be killed with sword and bomb unless you have power bracelet or glitches
            
        if options.logic == 'glitched' or options.logic == 'hell':
            entrance.connect(entrance_ledge, r.pit_buffer, back=False) # pit buffer to clip bottom wall and jump across the pits
            before_miniboss.connect(before_c_passage, r.hookshot_clip_block, back=False) # clip through block from below with hookshot spam by clipping on pot
            north_crossroads.connect(north_ledge, r.pit_buffer) # 1 pit buffer to clip bottom wall and jump across the pits
            middle_ledge.connect(east_ledge, r.pit_buffer) # pit buffer to clip bottom wall and jump across the pits
            after_c_passage.connect(spark_hallway, r.super_jump_boots, back=False) # charge a boots dash in bottom right corner to the right, jump before hitting the wall and use weapon to turn left before hitting the wall
            
        if  options.logic == 'hell':
            entrance.connect(entrance_ledge, r.pit_buffer_boots, back=False) # use pit buffer to clip into the bottom wall and boots bonk off the wall again
            before_a_passage.connect(after_a_passage, r.boots_bonk_2d_hell, back=False) # do an incredibly hard boots bonk setup to get across the hanging platforms in the 2d section
            statue_room.connect(after_blade_trap, r.pit_buffer_boots, back=False) # boots bonk + pit buffer past the blade traps
            after_blade_trap.connect(pot_column_room, r.pit_buffer_itemless, back=False) # pit buffer down 3 tiles
            before_miniboss.connect(statue_room, r.boots_jump, back=False) # boots jump across
            statue_room.connect(before_miniboss, AND(r.boots_jump, r.pit_buffer), back=False) # use boots jump in room with 2 zols + flying arrows to pit buffer above pot, then jump across. #TODO: change to pit_buffer_boots
            #TODO: statue_room.connect(before_miniboss, r.super_bump, back=False) # super bump off zol or fireball to skip bridge pull NOTE: not sure if oob
            before_miniboss.connect(before_c_passage, AND(r.sideways_block_push, POWER_BRACELET), back=False) # Sideways block push + pick up pots to reach stairs after gohma #TODO: move to glitched
            before_c_passage.connect(after_c_passage, r.boots_jump, back=False) # to pass 2d section, tight jump on left screen: hug left wall on little platform, then dash right off platform and jump while in midair to bonk against right wall
            after_c_passage.connect(spark_hallway, OR(r.super_jump_sword, r.zoomerang), back=False) # unclipped superjump in bottom right corner of staircase before boss room or left-facing zoomerang to superjump off right wall
            #TODO: before_d_passage.connect(after_d_passage) # hold the A button when itemless to bounce higher off the cheep-cheeps to cover 2-block gaps. helpful to stand on edge and pause/map buffer to catch the frame where fish starts to leap, then hold left
            #TODO: before_d_passage.connect(north_crossroads, r.boots_bonk_pit) # boots bonk over pit
            north_crossroads.connect(north_ledge, r.pit_buffer_boots) # boots bonk across the pits with pit buffering
            north_ledge.connect(middle_ledge, r.pit_buffer_itemless, back=False) # itemless pit buffer down through where the bridge would be
            middle_ledge.connect(east_ledge, r.pit_buffer_boots) # boots bonk across the pits with pit buffering
            #TODO: ms_3_room.connect(pot_locked_room, AND(r.super_jump_boots, r.zoomerang_buffer), back=False) # skip bracelet requirement by boots superjump to land in pot, then zoomerang to dislodge link to the left
            after_b_passage.connect(boss_key_room, r.pit_buffer_itemless, back=False)  # itemless pit buffer down through where the bridge would be
            if options.owlstatues == "both" or options.owlstatues == "dungeon": #TODO: REMOVE if statement, it's the patch to match upstream logic
                after_boss_keyblock.connect(spark_hallway, AND(STONE_BEAK5, r.pit_buffer_itemless), back=False) #TODO: REMOVE beak from requirement - pit buffer from east of boss door to spark hallway
            spark_hallway.connect(pre_boss_room, r.super_jump_feather, back=False) # wall clip bottom left superjump until clipped on bottom wall, then superjump to land on outcropping, tight jump to before boss

        self.entrance = entrance
        self.final_room = instrument


class NoDungeon5:
    def __init__(self, options, world_setup, r):
        entrance = Location("D5 Entrance", dungeon=5)
        Location(dungeon=5).add(HeartContainer(0x185), Instrument(0x182)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[4]])

        self.entrance = entrance
