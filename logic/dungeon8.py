from .requirements import *
from .location import Location
from locations.all import *


class Dungeon8:
    def __init__(self, options, world_setup, r, *, back_entrance_heartpiece=0x000):

        # locations
        entrance = Location("D8 Entrance", dungeon=8)
        lava_beamos_room = Location("D8 Lava Beamos Room", dungeon=8)
        miniboss1_room = Location("D8 Hinox Room", dungeon=8)
        sw_zamboni_area = Location("D8 After Hinox", dungeon=8)
        sw_zamboni_area_chest1 = Location(dungeon=8).add(DungeonChest(0x24D)) # 20 rupees
        sw_zamboni_area_chest2 = Location(dungeon=8).add(DungeonChest(0x246)) # small key
        spark_pit_room = Location("D8 Sparks Across Pit", dungeon=8)
        spark_pit_room_chest2 = Location(dungeon=8).add(DungeonChest(0x255)) # 50 rupees
        miniboss2_room = Location("D8 Rolling Bones Room", dungeon=8)
        sw_vire_room = Location("D8 Southwest Vire Room", dungeon=8)
        sw_vire_room_drop1 = Location(dungeon=8).add(DroppedKey(0x24C)) # small key
        vacuum_room = Location("D8 Vacuum Room", dungeon=8)
        vacuum_room_chest3 = Location(dungeon=8).add(DungeonChest(0x25C)) # compass
        spark_pot_room = Location("D8 Sparks Hidden Button Room", dungeon=8)
        slime_trap_room = Location("D8 Slime Trap Chest Room", dungeon=8)
        slime_trap_room_chest4 = Location(dungeon=8).add(DungeonChest(0x259))
        zamboni_pit_west = Location("D8 West of Chasm Zamboni", dungeon=8)
        zamboni_pit_east = Location("D8 East of Chasm Zamboni", dungeon=8)
        zamboni_pit_east_drop2 = Location(dungeon=8).add(DroppedKey(0x25A))
        miniboss3_room = Location("D8 Smasher Room", dungeon=8)
        mimic_room = Location("D8 Mimic Room", dungeon=8)
        before_a_passage = Location("D8 Mimic Passageway Spawned", dungeon=8)
        after_a_passage = Location("D8 Beamos Hidden Button Room", dungeon=8)
        pot_pit_room = Location("D8 Pots & Pits Room", dungeon=8)
        pot_pit_room_doorway = Location("D8 Pots & Pits Room Door", dungeon=8)
        pot_pit_room_chest5 = Location(dungeon=8).add(DungeonChest(0x25F))
        before_e_passage = Location("D8 Pots, & Pits Room Stairs", dungeon=8)
        after_e_passage = Location("D8 Below Peahat Blocks Hallway", dungeon=8)
        pre_center_zamboni = Location("D8 North of Entrance", dungeon=8)
        before_b_passage = Location("D8 Ledge by Entrance Zamboni", dungeon=8)
        after_b_passage = Location("D8 Before Cueball", dungeon=8)
        before_c_passage = Location("D8 Floating Heart Area", dungeon=8)
        switch_room = Location("D8 Switch Room", dungeon=8)
        pushblock_room = Location("D8 Pushblock Chest Area", dungeon=8)
        pushblock_room_chest6 = Location(dungeon=8).add(DungeonChest(0x24F))
        lava_left_corridor = Location("D8 'L' Shaped Corridor", dungeon=8)
        pre_center_keyblock = Location("D8 Before Central Keyblock", dungeon=8)
        loop_ledge = Location("D8 Useless Ledge", dungeon=8)
        peahat_area = Location("D8 Peahat Area", dungeon=8)
        heart_vire = Location("D8 Floating Heart & Vire Area", dungeon=8)
        before_g_passage = Location("D8 Blade Room", dungeon=8)
        hidden_arrow_room = Location("Hidden Arrow Room", dungeon=8)
        dark_east_zol = Location("D8 Dark East (Zol Side)", dungeon=8)
        dark_east_spark = Location("D8 Dark East (Spark Side)", dungeon=8)
        dark_center = Location("D8 Dark Center", dungeon=8)
        dark_center_torches = Location("D8 Dark Center Between Torches", dungeon=8)
        dark_center_pre_keyblock = Location("D8 Dark Center Before Keyblock", dungeon=8)
        dark_west = Location("D8 Dark West", dungeon=8)
        before_d_passage = Location("D8 Dark Room Staircase", dungeon=8)
        after_d_passage = Location("D8 Staircase at Isolated Miniboss Area", dungeon=8)
        miniboss_room = Location("D8 Isolated Miniboss Room", dungeon=8)
        miniboss_cubby = Location("D8 Post Miniboss Room", dungeon=8)
        rod_ledge = Location("D8 Miniboss Reward", dungeon=8)
        rod_ledge_chest7 = Location(dungeon=8).add(DungeonChest(0x237)) # magic rod
        dodongo_area = Location("D8 Dodongo Area", dungeon=8)
        dodongo_area_drop3 = Location(dungeon=8).add(DroppedKey(0x23E))
        pre_lava_ledge = Location("D8 Ledge West of Dodongos", dungeon=8)
        lava_ledge = Location("D8 Lava Ledge", dungeon=8)
        lava_ledge_chest8 = Location(dungeon=8).add(DungeonChest(0x235)) # medicine
        slime_corridor = Location("D8 Corridor by Lava Ledge Chest", dungeon=8)
        after_g_passage = Location("D8 North Refill Room", dungeon=8)
        after_f_stairs = Location("D8 Ledge Above Dodongos", dungeon=8)
        after_f_stairs_chest9 = Location(dungeon=8).add(DungeonChest(0x23D))
        before_f_stairs = Location("D8 Northwest Area", dungeon=8)
        before_f_stairs_chest10 = Location(dungeon=8).add(DungeonChest(0x240))
        before_f_stairs_drop4 = Location(dungeon=8).add(DroppedKey(0x241))
        ledge_west_boss = Location("D8 West of Boss Door Ledge", dungeon=8)
        ledge_west_boss_chest11 = Location(dungeon=8).add(DungeonChest(0x23A))
        miniboss4_room = Location("D8 Cueball Room", dungeon=8)
        nw_zamboni_room = Location("D8 Two Torch Zamboni Puzzle", dungeon=8)
        nw_zamboni_room_chest12 = Location(dungeon=8).add(DungeonChest(0x232))
        after_c_passage = Location("Outside Boss Door", dungeon=8)
        boss_room = Location("D8 Boss Room", dungeon=8)
        boss_room_drop5 = Location(dungeon=8).add(HeartContainer(0x234)) # heart container
        instrument = Location("D8 Instrument Room", dungeon=8).add(Instrument(0x230)) # instrument

        # owl statues
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=8).add(OwlStatue(0x253)).connect(after_a_passage, STONE_BEAK8)
            Location(dungeon=8).add(OwlStatue(0x245)).connect(hidden_arrow_room, STONE_BEAK8)
            Location(dungeon=8).add(OwlStatue(0x241)).connect(before_f_stairs, STONE_BEAK8)
        
        # connections
        #TODO: if options.logic == "casual":
            
        #TODO: else:

        #west   
        entrance.connect(lava_beamos_room, r.enemy_requirements["VIRE"])
        lava_beamos_room.connect(miniboss1_room, r.enemy_requirements["SNAKE"])
        lava_beamos_room.connect(entrance, None, one_way=True)
        miniboss1_room.connect(sw_zamboni_area, r.miniboss_requirements["HINOX"])
        miniboss1_room.connect(lava_beamos_room, None, one_way=True)
        sw_zamboni_area.connect(sw_zamboni_area_chest1, None)
        sw_zamboni_area.connect(sw_zamboni_area_chest2, MAGIC_ROD)
        before_f_stairs.connect(sw_zamboni_area, None, one_way=True)
        sw_zamboni_area.connect(spark_pit_room, OR(HOOKSHOT, FEATHER))
        spark_pit_room.connect(spark_pit_room_chest2, None)
        sw_zamboni_area.connect(miniboss1_room, None, one_way=True)
        sw_zamboni_area.connect(miniboss2_room, None, one_way=True)
        miniboss2_room.connect(sw_vire_room, r.miniboss_requirements["ROLLING_BONES"])
        sw_vire_room.connect(sw_vire_room_drop1, r.attack_hookshot_no_bomb) # takes 11 bombs minimum to get this from entrance, so it is excluded
        miniboss2_room.connect(vacuum_room, r.miniboss_requirements["ROLLING_BONES"])
        vacuum_room.connect(vacuum_room_chest3, None)
        vacuum_room.connect(entrance, None, one_way=True)
        #east
        entrance.connect(spark_pot_room, r.enemy_requirements["VIRE"])
        spark_pot_room.connect(slime_trap_room, POWER_BRACELET)
        slime_trap_room.connect(slime_trap_room_chest4, None)
        spark_pot_room.connect(mimic_room, POWER_BRACELET)
        mimic_room.connect(spark_pot_room, None, one_way=True)
        mimic_room.connect(before_a_passage, r.enemy_requirements["MIMIC"])
        before_a_passage.connect(mimic_room, None, one_way=True)
        before_a_passage.connect(after_a_passage, FEATHER)
        slime_trap_room.connect(spark_pot_room, None, one_way=True)
        slime_trap_room.connect(zamboni_pit_west, FEATHER)
        #TODO: zamboni_pit_west.connect(zamboni_pit_east, AND(PEGASUS_BOOTS, FEATHER)) #new logic r.not_that_tight_jump
        zamboni_pit_east.connect(zamboni_pit_west, None, one_way=True)
        zamboni_pit_east.connect(zamboni_pit_east_drop2, None)
        zamboni_pit_east.connect(miniboss3_room, None, one_way=True)
        miniboss3_room.connect(zamboni_pit_east, r.miniboss_requirements["SMASHER"])
        miniboss3_room.connect(after_a_passage, r.miniboss_requirements["SMASHER"], one_way=True)
        after_a_passage.connect(miniboss3_room, POWER_BRACELET, one_way=True)
        miniboss3_room.connect(pot_pit_room_doorway, r.miniboss_requirements["SMASHER"], one_way=True)
        pot_pit_room_doorway.connect(miniboss3_room, AND(OR(FEATHER, POWER_BRACELET), r.enemy_requirements["SNAKE"]), one_way=True)
        pot_pit_room_doorway.connect(pot_pit_room, OR(FEATHER, POWER_BRACELET))
        pot_pit_room.connect(pot_pit_room_chest5, None)
        pot_pit_room.connect(before_e_passage, POWER_BRACELET)
        #north
        entrance.connect(pre_center_zamboni, FEATHER)
        pre_center_zamboni.connect(before_b_passage, None, one_way=True)
        before_b_passage.connect(spark_pot_room, None, one_way=True)
        pre_center_zamboni.connect(before_c_passage, None, one_way=True) # new logic
        before_c_passage.connect(slime_trap_room, None, one_way=True)
        before_c_passage.connect(switch_room, BOMB)
        switch_room.connect(zamboni_pit_east, BOMB)
        before_e_passage.connect(after_e_passage, FEATHER)
        pre_center_zamboni.connect(after_e_passage, None, one_way=True)
        pre_center_zamboni.connect(lava_left_corridor, None)
        lava_left_corridor.connect(after_e_passage, BOMB)
        lava_left_corridor.connect(pushblock_room, None)
        pushblock_room.connect(pushblock_room_chest6, None)
        pre_center_zamboni.connect(loop_ledge, None, one_way=True)
        loop_ledge.connect(before_c_passage, None, one_way=True)
        pre_center_zamboni.connect(pre_center_keyblock, None, one_way=True)
        pre_center_keyblock.connect(heart_vire, KEY8)
        pre_center_keyblock.connect(peahat_area, KEY8)
        peahat_area.connect(heart_vire, KEY8)
        peahat_area.connect(after_e_passage, None, one_way=True)
        heart_vire.connect(before_g_passage, AND(KEY8, FOUND(KEY8, 2)))
        before_g_passage.connect(hidden_arrow_room, None, one_way=True)
        before_g_passage.connect(after_g_passage, HOOKSHOT, one_way=True)
        after_g_passage.connect(before_g_passage, AND(FEATHER, HOOKSHOT))
        hidden_arrow_room.connect(dodongo_area, r.enemy_requirements["HIDING_ZOL"])
        hidden_arrow_room.connect(dark_east_spark, BOMB)
        #dark
        peahat_area.connect(dark_west, AND(AND(BOMB, BOW), FEATHER))
        dark_west.connect(peahat_area, AND(BOMB, FEATHER), one_way=True)
        peahat_area.connect(dark_west, AND(BOMB, FEATHER)) # could be hard due to obscurity
        peahat_area.connect(dark_center, AND(BOMB, FEATHER)) # could be hard due to obscurity
        dark_west.connect(before_f_stairs, AND(BOMB, FEATHER), one_way=True)
        dark_west.connect(dark_center, AND(r.enemy_requirements["SNAKE"], r.enemy_requirements["PEAHAT"]))
        dark_center.connect(dark_west, r.enemy_requirements["SNAKE"], one_way=True)
        dark_center.connect(dark_east_zol, AND(KEY8, FOUND(KEY8, 4)))
        dark_east_zol.connect(dark_east_spark, FEATHER)
        dark_west.connect(dark_center_torches, KEY8)
        dark_center_torches.connect(dark_center_pre_keyblock, HOOKSHOT)
        dark_center_torches.connect(dark_center, None, one_way=True)
        dark_center_pre_keyblock.connect(before_d_passage, AND(KEY8, FOUND(KEY8, 7)))
        dark_center_pre_keyblock.connect(dark_center, None, one_way=True)
        #miniboss
        before_d_passage.connect(after_d_passage, FEATHER)
        after_d_passage.connect(miniboss_room, None, one_way=True)
        miniboss_room.connect(miniboss_cubby, r.miniboss_requirements[world_setup.miniboss_mapping[7]])
        miniboss_room.connect(entrance, r.miniboss_requirements[world_setup.miniboss_mapping[7]], one_way=True) # TODO: check requirements for blaino to punch you back to entrance, too
        miniboss_cubby.connect(after_d_passage, None, one_way=True)
        rod_ledge.connect(rod_ledge_chest7, None)
        rod_ledge.connect(after_d_passage, None, one_way=True)
        #dodongo
        dodongo_area.connect(hidden_arrow_room, None, one_way=True)
        dodongo_area_drop3.connect(dodongo_area, r.enemy_requirements["GIBDO"]) # 2 gibdos cracked floor; technically possible to use pits to kill but dumb
        dodongo_area.connect(pre_lava_ledge, FEATHER)
        pre_lava_ledge.connect(slime_corridor, FEATHER)
        pre_lava_ledge.connect(slime_corridor, None, one_way=True)
        pre_lava_ledge.connect(lava_ledge, HOOKSHOT)
        pre_lava_ledge.connect(after_g_passage, None, one_way=True)
        lava_ledge.connect(lava_ledge_chest8, None)
        lava_ledge.connect(after_g_passage, None, one_way=True)
        dodongo_area.connect(after_f_stairs_chest9, AND(FEATHER, AND(KEY8, FOUND(KEY8, 4)), r.miniboss_requirements["DODONGO"]), one_way=True) #TODO: assumes vanilla tal tal exits
        after_f_stairs.connect(dodongo_area, None, one_way=True)
        before_f_stairs.connect(after_f_stairs, None) #TODO: assumes vanilla tal tal exits
        #northwest
        slime_corridor.connect(before_f_stairs, AND(KEY8, FOUND(KEY8, 4)))
        before_f_stairs.connect(before_f_stairs_chest10, None)
        before_f_stairs.connect(before_f_stairs_drop4, BOW)
        after_b_passage.connect(ledge_west_boss, HOOKSHOT)
        ledge_west_boss.connect(ledge_west_boss_chest11, None)
        ledge_west_boss.connect(before_f_stairs, None, one_way=True)
        #tal tal
        if back_entrance_heartpiece is not None:
            Location().add(HeartPiece(back_entrance_heartpiece)).connect(before_f_stairs, None)  # Outside the dungeon on the platform
        #cueball
        before_b_passage.connect(after_b_passage, AND(FEATHER, MAGIC_ROD))
        after_b_passage.connect(before_b_passage, MAGIC_ROD, one_way=True)
        before_f_stairs.connect(after_b_passage, AND(r.enemy_requirements["VIRE"], AND(r.enemy_requirements["SNAKE"])))
        after_b_passage.connect(miniboss4_room, AND(KEY8, FOUND(KEY8, 7)))
        miniboss4_room.connect(nw_zamboni_room, AND(FEATHER, r.miniboss_requirements["CUE_BALL"]))
        nw_zamboni_room.connect(nw_zamboni_room_chest12, None)
        #boss
        before_c_passage.connect(after_c_passage, AND(FEATHER, MAGIC_ROD))
        after_c_passage.connect(boss_room, NIGHTMARE_KEY8)
        boss_room.connect(boss_room_drop5, r.boss_requirements[world_setup.boss_mapping[7]])
        boss_room.connect(instrument, AND(FEATHER, r.boss_requirements[world_setup.boss_mapping[7]]))
        

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            zamboni_pit_west.connect(zamboni_pit_east, r.tight_jump) # diagonal jump over the pits to reach zamboni
            #TODO: after_a_passage.connect(before_a_passage, None, one_way=True) # new logic - take some damage but itemless
            pot_pit_room_doorway.connect(miniboss3_room, r.throw_pot, one_way=True) # 4 pots to kill 4 ropes
            dodongo_area.connect(dodongo_area_drop3, OR(HOOKSHOT, MAGIC_ROD)) # crack one of the floor tiles and hookshot the gibdos in, or burn the gibdos and make them jump into pit
            before_f_stairs.connect(sw_vire_room_drop1, AND(r.miniboss_requirements["ROLLING_BONES"], r.enemy_requirements["VIRE"]), one_way=True) # allows bombs to kill vire but only from dropdown in unlit torch room
            peahat_area.connect(heart_vire, r.tight_jump) # around keyblock
            before_f_stairs.connect(dark_west, AND(BOMB, FEATHER)) # hard - yolo into lava and drop bomb, forced damage.
            after_f_stairs.connect(after_f_stairs_chest9, BOMB) # throw bombs from ledge to defeat dodongos

        if options.logic == 'glitched' or options.logic == 'hell':
            sw_zamboni_area.connect(spark_pit_room, r.pit_buffer_itemless) # pit buffer down across the pit then walk diagonally between pits
            before_e_passage.connect(after_e_passage, r.boots_bonk, one_way=True) # boots bonking from rope room to mimic room sidescroller #TODO: move to hard, it's in glitched now to match stable
            before_e_passage.connect(pot_pit_room, AND(r.hookshot_clip_block, r.super_jump_feather), one_way=True) # new logic
            after_e_passage.connect(peahat_area, r.sideways_block_push) # sideways block push in peahat room to get past keyblock
            dark_center_torches.connect(before_d_passage, r.bookshot) # blow up hidden wall for darkroom, use feather + hookshot to clip past keyblock in front of stairs #TODO: make more explicit
            dark_center.connect(dark_center_torches, r.super_jump_feather)
            dark_center.connect(dark_center_pre_keyblock, r.super_jump_feather)
            dark_center.connect(dark_east_zol, r.hookshot_clip, one_way=True)
            peahat_area.connect(before_f_stairs, r.jesus_jump) # use jesus jump in refill room left of peahats to clip bottom wall and push bottom block left, to get a place to super jump
            peahat_area.connect(heart_vire, r.jesus_jump)
            before_f_stairs.connect(slime_corridor, r.jesus_jump) # from up left you can jesus jump / lava swim around the key door next to the boss.
            before_f_stairs.connect(after_b_passage, r.super_jump_feather) # superjump #TODO: make more explicit
            after_g_passage.connect(slime_corridor, r.jesus_jump)
            after_g_passage.connect(lava_ledge, AND(r.jesus_jump, r.super_jump_feather))
            slime_corridor.connect(lava_ledge, AND(r.super_jump_feather, r.jesus_jump))
            before_f_stairs.connect(after_c_passage, r.super_jump_feather, one_way=True) # superjump off the bottom or right wall to jump over to the boss door
            miniboss_cubby.connect(rod_ledge, r.super_jump_feather) # superjump to pegs after blaino
            dodongo_area.connect(after_f_stairs, r.super_jump_feather) # for getting dodongo chest without leaving the room
            dodongo_area.connect(after_f_stairs_chest9, AND(r.miniboss_requirements["DODONGO"], r.super_jump_feather)) # glitched

        if options.logic == 'hell':
            #southwest
            sw_zamboni_area.connect(before_f_stairs, r.zoomerang_buffer) # pixel perfect left-facing zoomerang followed up by another zoomerang to get un-stuck
            #southeast
            before_a_passage.connect(after_a_passage, r.boots_bonk_2d_hell) #TODO: replace with row below
            #TODO: before_a_passage.connect(after_a_passage, OR(r.boots_bonk_2d_hell, r.toadstool_bounce_2d_hell, r.bracelet_bounce_2d_hell), one_way=True) #TODO: 3 ways to cross passage left to right, seems like toadstool doesn't affect logic
            pot_pit_room_doorway.connect(pot_pit_room_chest5, r.pit_buffer_itemless)
            pot_pit_room.connect(pot_pit_room_doorway, AND(r.hookshot_clip_block, r.hookshot_spam_pit))
            pot_pit_room.connect(before_e_passage, r.zoomerang_buffer, one_way=True) # new logic
            before_e_passage.connect(pot_pit_room, r.shaq_jump) # this is wild, maybe need to add sword for consistency?
            zamboni_pit_west.connect(slime_trap_room, r.boots_bonk, one_way=True)
            #center
            entrance.connect(pre_center_zamboni, AND(r.jesus_buffer, r.lava_swim_sword)) #TODO: update to swordless - boots bonk around the top left corner at vire, get on top of the wall to bonk to the left, and transition while slashing sword
            lava_left_corridor.connect(pre_center_zamboni, r.jesus_buffer, one_way=True)
            after_e_passage.connect(pre_center_zamboni, r.jesus_buffer, one_way=True)
            pre_center_keyblock.connect(pre_center_zamboni, r.jesus_buffer, one_way=True)
            pre_center_keyblock.connect(before_b_passage, r.jesus_buffer, one_way=True)
            before_c_passage.connect(before_b_passage, r.jesus_buffer)
            before_b_passage.connect(pre_center_zamboni, r.jesus_buffer, one_way=True)
            #TODO: loop_ledge.connect(heart_vire, r.hookshot_clip_block, one_way=True) #new logic
            #dark
            before_f_stairs.connect(dark_west, AND(AND(BOMB, OR(r.jesus_buffer, BOW)), r.lava_swim)) # hell - bomb the wall with bomb arrow of jesus buffer to get close enough and pause buffer the bomb on the splash, return with lava swim
            dark_west.connect(before_f_stairs, AND(BOMB, HOOKSHOT, r.jesus_buffer)) # hell - use hookshot when splashing to grab spark's block
            before_f_stairs.connect(dark_west, AND(BOW, BOMB, r.lava_swim, r.jesus_buffer), one_way=True)
            dark_west.connect(peahat_area, AND(BOMB, r.jesus_buffer))
            dark_center.connect(peahat_area, AND(BOMB, r.jesus_buffer))
            dark_east_zol.connect(dark_east_spark, OR(r.hookshot_clip, r.boots_bonk))
            dark_center.connect(before_d_passage, AND(r.super_jump_feather, r.ledge_super_bump), one_way=True)
            dark_center_pre_keyblock.connect(before_d_passage, r.zoomerang_buffer, one_way=True)
            #miniboss
            before_d_passage.connect(after_d_passage, r.boots_bonk_2d_hell) # get through 2d section with boots bonks
            loop_ledge.connect(before_b_passage, r.jesus_buffer, one_way=True)
            peahat_area.connect(before_f_stairs, AND(r.jesus_buffer, r.lava_swim))
            #miniboss rewars without feather: (1) power bracelet and boots through E passage (2) jesus buffers and magic rod through B passage
            switch_room.connect(rod_ledge_chest7, AND(BOMB, OR(AND(r.jesus_buffer, MAGIC_ROD), AND(POWER_BRACELET, r.boots_bonk_2d_hell, r.sideways_block_push)), FOUND(KEY8, 7), r.enemy_requirements["PEAHAT"], r.enemy_requirements["SNAKE"], HOOKSHOT, r.miniboss_requirements[world_setup.miniboss_mapping[7]]), one_way=True)
            #dodongo
            dodongo_area.connect(dodongo_area_drop3, AND(FEATHER, SHIELD)) # lock gibdos into pits and crack the tile they stand on, then use shield to bump them into the pit
            dodongo_area.connect(pre_lava_ledge, r.boots_bonk) # bonk over 1 block of lava, no buffer
            dodongo_area.connect(after_f_stairs_chest9, AND(r.miniboss_requirements["DODONGO"], r.boots_bonk, r.lava_swim), one_way=True) # hell
            pre_lava_ledge.connect(lava_ledge, r.super_jump_feather) # walk off ledge and pause buffer to get in position
            slime_corridor.connect(before_f_stairs, r.lava_swim) # hell
            #northwest
            before_b_passage.connect(after_b_passage, AND(r.boots_bonk_2d_hell, MAGIC_ROD)) # boots bonk in 2d to use magic rod on upper ice blocks
            before_f_stairs.connect(peahat_area, r.jesus_buffer, one_way=True) # hell - from refill room push block and boots bonk into jesus buffer then bonk again
            before_f_stairs.connect(peahat_area, r.lava_swim) #hell can be troublesome, if having issues, exit to tal tal and try again or use sword to guarantee it
            before_f_stairs.connect(peahat_area, AND(r.jesus_buffer, r.lava_swim)) # use boots bonk next to 3x peahats to get on top of lava, and transition left while slashing sword
            miniboss4_room.connect(nw_zamboni_room, AND(r.boots_bonk, r.miniboss_requirements["CUE_BALL"])) # use a boots bonk to cross the lava in cueball room
            #boss
            before_c_passage.connect(after_c_passage, AND(r.boots_bonk_2d_hell, MAGIC_ROD)) # boots bonk through 2d section
            after_c_passage.connect(before_f_stairs, AND(r.jesus_jump, r.zoomerang))
            boss_room.connect(instrument, AND(r.boots_bonk, r.boss_requirements[world_setup.boss_mapping[7]]))
            
        self.entrance = entrance
        self.final_room = instrument


class NoDungeon8:
    def __init__(self, options, world_setup, r):
        entrance = Location("D8 Entrance", dungeon=8)
        boss = Location(dungeon=8).add(HeartContainer(0x234)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[7]])
        instrument = Location(dungeon=8).add(Instrument(0x230)).connect(boss, FEATHER) # jump over the lava to get to the instrument

        self.entrance = entrance
