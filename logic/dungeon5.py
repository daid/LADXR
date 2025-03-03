from .requirements import *
from .location import Location
from locations.all import *


class Dungeon5:
    def __init__(self, options, world_setup, r):
        entrance = Location("D5 Entrance", dungeon=5)
        entrance_ledge = Location("D5 Entrance Ledge", dungeon=5)
        entrance_ledge_chest1 = Location(dungeon=5).add(DungeonChest(0x1A0)) # 200 rupees
        before_a_passage = Location("D5 Room West of Entrance", dungeon=5)
        before_a_passage_chest2 = Location(dungeon=5).add(DungeonChest(0x19E)) # compass
        after_a_passage = Location("D5 Crystal Room Entrance", dungeon=5)
        crystal_room = Location("D5 Crystal Room", dungeon=5)
        crystal_room_drop1 = Location(dungeon=4).add(DroppedKey(0x181)) # small key
        crystal_puddle_room = Location("D5 After First Key", dungeon=5)
        messy_room = Location("D5 Messy Room", dungeon=5)
        messy_room_chest3 = Location(dungeon=5).add(DungeonChest(0x19B)) # beak?
        statue_room = Location("D5 Fireball Statue Room", dungeon=5)
        blade_trap_room = Location("D5 Fireball Statue Room", dungeon=5)
        blade_trap_room_chest4 = Location(dungeon=4).add(DungeonChest(0x197)) # small key
        before_miniboss = Location("D5 Before Miniboss", dungeon=5)
        miniboss_room = Location("D5 Miniboss Room", dungeon=5)
        before_c_passage = Location("D5 After Miniboss", dungeon=5)
        after_c_passage = Location("D5 Before Boss Keyblock", dungeon=5)
        after_boss_keyblock = Location("D5 After Boss Keyblock", dungeon=5)
        ms_1_room = Location("Master Stalfos Fight 1", dungeon=5)
        before_d_passage = Location("D5 South of Crossroads", dungeon=5)
        before_d_passage_chest5 = Location(dungeon=5).add(DungeonChest(0x196)) # master stalfos message
        after_d_passage = Location("D5 Two Torch Room", dungeon=5)
        star_room = Location("D5 Star Room", dungeon=5)
        spark_hallway = Location("D5 Spark Hallway", dungeon=5)
        north_crossroads = Location("D5 North of Crossroads", dungeon=5)
        middle_ledge = Location("D5 First Ledge Chest", dungeon=5)
        middle_ledge_chest6 = Location(dungeon=5).add(DungeonChest(0x18E)) # 50 rupees
        north_ledge = Location("D5 North Ledge Chest", dungeon=5)
        north_ledge_chest_7 = Location(dungeon=5).add(DungeonChest(0x188)) # 50 rupees
        east_ledge = Location("D5 East Ledge Chest", dungeon=5)
        east_ledge_chest8 = Location(dungeon=5).add(DungeonChest(0x18F)) # small key
        west_crossroads = Location("D5 West of Crossroads", dungeon=5)
        before_b_passage = Location("D5 Deep Water Passage Entrance", dungeon=5)
        after_b_passage = Location("D5 Bridge Chest Room", dungeon=5)
        ms_3_room = Location("D5 Master Stalfos 3", dungeon=5)
        pot_locked_room = Location("D5 Pot Locked Room", dungeon=5)
        pot_locked_room_chest9 = Location(dungeon=5).add(DungeonChest(0x183))
        ms_4_room = Location("D5 Master Stalfos 4", dungeon=5)
        ms_4_room_drop2 = Location(dungeon=5).add(HookshotDrop()) # hookshot
        boss_key_room = Location(dungeon=5)
        boss_key_room_chest10 = Location(dungeon=5).add(DungeonChest(0x186))  # nightmare key
        pre_boss_room = Location("D5 Before Boss", dungeon=5)
        boss_room = Location("D5 Boss Room", dungeon=5)
        boss = Location(dungeon=5).add(HeartContainer(0x185), Instrument(0x182)) # heart container, instrument

        # owl statues
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=5).add(OwlStatue(0x19A)).connect(crystal_puddle_room, STONE_BEAK5)
            Location(dungeon=5).add(OwlStatue(0x18A)).connect(star_room, STONE_BEAK5)

        # connections
        entrance.connect(entrance_ledge, HOOKSHOT)
        entrance_ledge.connect(entrance_ledge_chest1, None)
        entrance.connect(before_a_passage, AND(r.enemy_requirements["KEESE"], r.enemy_requirements["IRON_MASK"]))
        before_a_passage.connect(before_a_passage_chest2, None)
        before_a_passage.connect(after_a_passage, FEATHER)
        after_a_passage.connect(crystal_room, SWORD)
        crystal_room.connect(crystal_room_drop1, SWORD)
        entrance.connect(crystal_puddle_room, KEY5)
        crystal_puddle_room.connect(messy_room, r.enemy_requirements["IRON_MASK"])
        messy_room.connect(messy_room_chest3, r.enemy_requirements["IRON_MASK"])
        crystal_puddle_room.connect(statue_room, r.enemy_requirements["IRON_MASK"])
        statue_room.connect(blade_trap_room, HOOKSHOT)
        blade_trap_room.connect(blade_trap_room_chest4, None)
        statue_room.connect(before_miniboss, HOOKSHOT)
        before_miniboss.connect(miniboss_room, AND(KEY5, FOUND(KEY5, 2)))
        miniboss_room.connect(before_c_passage, r.miniboss_requirements[world_setup.miniboss_mapping[4]])
        before_c_passage.connect(after_c_passage, AND(HOOKSHOT, FEATHER))
        after_c_passage.connect(after_boss_keyblock, AND(KEY5, FOUND(KEY5, 3)))
        crystal_puddle_room.connect(ms_1_room, AND(r.enemy_requirements["STALFOS_AGGRESSIVE"], r.enemy_requirements["STALFOS_EVASIVE"]), one_way=True)
        ms_1_room.connect(before_d_passage, r.enemy_requirements["MASTER_STALFOS"], one_way=True) # l2 sword beams kill but obscure
        before_d_passage.connect(ms_1_room, None, one_way=True)
        ms_1_room.connect(crystal_puddle_room, r.enemy_requirements["MASTER_STALFOS"], one_way=True)
        before_d_passage.connect(before_d_passage_chest5, None)
        before_d_passage.connect(after_d_passage, FEATHER)
        after_d_passage.connect(star_room, None, one_way=True)
        star_room.connect(spark_hallway, r.enemy_requirements["STAR"], one_way=True)
        star_room.connect(after_d_passage, r.enemy_requirements["STAR"], one_way=True)
        spark_hallway.connect(after_c_passage, None, one_way=True)
        spark_hallway.connect(star_room, None, one_way=True)
        before_d_passage.connect(north_crossroads, FEATHER)
        north_crossroads.connect(middle_ledge, OR(HOOKSHOT, AND(FEATHER, PEGASUS_BOOTS)))
        middle_ledge.connect(middle_ledge_chest6, None)
        middle_ledge.connect(east_ledge, HOOKSHOT)
        east_ledge.connect(east_ledge_chest8, None)
        north_crossroads.connect(north_ledge, HOOKSHOT)
        middle_ledge.connect(north_ledge, HOOKSHOT, one_way=True)
        north_ledge.connect(north_ledge_chest_7, None)
        before_d_passage.connect(west_crossroads, None)
        west_crossroads.connect(before_b_passage, FLIPPERS)
        before_b_passage.connect(after_b_passage, FLIPPERS)
        after_b_passage.connect(boss_key_room, HOOKSHOT)
        boss_key_room.connect(boss_key_room_chest10, None)
        north_crossroads.connect(ms_3_room, AND(r.enemy_requirements["HIDING_ZOL"])) #TODO: add POWER_BRACELET to requirement
        ms_3_room.connect(pot_locked_room, AND(POWER_BRACELET, r.enemy_requirements["STALFOS_AGGRESSIVE"], r.enemy_requirements["STALFOS_EVASIVE"])) #TODO: remove kill enemy requirements, it's just here to make logic match stable
        pot_locked_room.connect(pot_locked_room_chest9, None)
        ms_3_room.connect(ms_4_room, AND(FEATHER, SWORD)) # can reach ms4 from entrance with feather and sword after beating ms3
        ms_4_room.connect(ms_4_room_drop2, r.enemy_requirements["MASTER_STALFOS"])
        after_boss_keyblock.connect(pre_boss_room, HOOKSHOT)
        pre_boss_room.connect(boss_room, NIGHTMARE_KEY5)
        boss_room.connect(boss, r.boss_requirements[world_setup.boss_mapping[4]])

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            statue_room.connect(blade_trap_room, FEATHER) # jump past the blade traps
            before_d_passage.connect(after_d_passage, r.boots_bonk) # boots charge + bonk to cross 2d bridge [move to hell?]
            before_c_passage.connect(after_c_passage, AND(r.boots_bonk, HOOKSHOT)) # boots bonk in 2d section to skip feather [move to hell?]
            after_c_passage.connect(before_c_passage, r.boots_bonk, one_way=True) # don't need hookshot in reverse [move to hell?]
            spark_hallway.connect(after_boss_keyblock, r.tight_jump) # jump from bottom left to top right, skipping the keyblock
            spark_hallway.connect(pre_boss_room, r.boots_jump) # cross pits room from bottom left to top left with boots jump
            before_d_passage.connect(north_crossroads, HOOKSHOT) # walk into pit and hookshot right to get to single tile, corner walk up+left or hookshot to first ledge chest
            north_crossroads.connect(middle_ledge, AND(r.wall_clip, r.tight_jump)) # tight jump from bottom wall clipped to make it over the pits
            after_b_passage.connect(boss_key_room, r.boots_jump) # boots jump across
            
        if options.logic == 'glitched' or options.logic == 'hell':
            entrance.connect(entrance_ledge, r.pit_buffer) # 1 pit buffer to clip bottom wall and jump across the pits
            before_miniboss.connect(before_c_passage, r.hookshot_clip_block) # glitch through the blocks/pots with hookshot.
            north_ledge.connect(north_crossroads, r.pit_buffer) # 1 pit buffer to clip bottom wall and jump across the pits
            east_ledge.connect(middle_ledge, r.pit_buffer) # 1 pit buffer to clip bottom wall and jump across the pits
            #after_c_passage.connect(spark_hallway, AND(r.text_clip, r.super_jump)) # use the keyblock to get a wall clip in right wall to perform a superjump over the pushable block
            after_c_passage.connect(spark_hallway, r.super_jump_boots) # charge a boots dash in bottom right corner to the right, jump before hitting the wall and use weapon to the left side before hitting the wall
            #TODO: north_crossroads.connect(ms_3_room, OR(OR(SWORD, BOMB), AND(OR(r.super_jump_boots, POWER_BRACELET), r.enemy_requirements["HIDING_ZOL"])) # glitched logic to clear room before ms3
            #TODO: west_crossroads.connect(ms_3_room, AND(FEATHER, r.enemy_requirements["HIDING_ZOL"])) # glitched logic to clear room before ms3
            
        if  options.logic == 'hell':
            entrance.connect(entrance_ledge, r.pit_buffer_boots) # use pit buffer to clip into the bottom wall and boots bonk off the wall again
            before_a_passage.connect(after_a_passage, r.boots_bonk_2d_hell) # do an incredibly hard boots bonk setup to get across the hanging platforms in the 2d section
            statue_room.connect(blade_trap_room, r.pit_buffer_boots) # boots bonk + pit buffer past the blade traps
            statue_room.connect(before_miniboss, AND(r.boots_jump, r.pit_buffer)) # use boots jump in room with 2 zols + flying arrows to pit buffer above pot, then jump across. #TODO: change to pit_buffer_boots
            before_miniboss.connect(before_c_passage, AND(r.sideways_block_push, POWER_BRACELET)) # Sideways block push + pick up pots to reach post_gohma
            before_c_passage.connect(after_c_passage, r.boots_jump) # to pass 2d section, tight jump on left screen: hug left wall on little platform, then dash right off platform and jump while in midair to bonk against right wall
            after_c_passage.connect(spark_hallway, r.super_jump_sword) # unclipped superjump in bottom right corner of staircase before boss room, jumping left over the pushable block. reverse is push block
            after_c_passage.connect(spark_hallway, r.zoomerang) # use zoomerang dashing left to get an unclipped boots superjump off the right wall over the block. reverse is push block
            #TODO: before_d_passage.connect(north_crossroads, r.boots_bonk) # boots bonk over pit
            north_ledge.connect(north_crossroads, r.boots_bonk_pit) # boots bonk across the pits with pit buffering
            middle_ledge.connect(north_crossroads, r.boots_bonk_pit) # get to first chest via the north chest with pit buffering
            east_ledge.connect(middle_ledge, r.boots_bonk_pit) # boots bonk across the pits with pit buffering
            ms_3_room.connect(ms_4_room, AND(r.boots_bonk_2d_hell, SWORD)) # can reach fourth arena from entrance with pegasus boots and sword
            after_b_passage.connect(boss_key_room, r.pit_buffer_itemless) # pit buffer across
            after_boss_keyblock.connect(spark_hallway, AND(STONE_BEAK5, r.pit_buffer_itemless), one_way=True) #TODO: BEAK is only here to make logic match stable - pit buffer from top right to bottom in right pits room
            spark_hallway.connect(pre_boss_room, r.super_jump_sword) # cross pits room from bottom left to top left by superjump from bottom wall to land on outcropping, then jump across            

        self.entrance = entrance
        self.final_room = boss


class NoDungeon5:
    def __init__(self, options, world_setup, r):
        entrance = Location("D5 Entrance", dungeon=5)
        Location(dungeon=5).add(HeartContainer(0x185), Instrument(0x182)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[4]])

        self.entrance = entrance
