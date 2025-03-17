from .requirements import *
from .location import Location
from locations.all import *


class Dungeon8:
    def __init__(self, options, world_setup, r, *, back_entrance_heartpiece=0x000):

        # locations
        entrance = Location("D8 Entrance", dungeon=8)
        lava_beamos_room = Location("D8 Lava Beamos Room", dungeon=8)
        miniboss1_room = Location("D8 Hinox Room", dungeon=8)
        sw_zamboni_area = Location("D8 Zamboni Intersection", dungeon=8)
        sw_zamboni_area_chest1 = Location(dungeon=8).add(DungeonChest(0x24D)) # 20 rupees
        sw_zamboni_area_chest2 = Location(dungeon=8).add(DungeonChest(0x246)) # small key
        spark_pit_room = Location("D8 Southwest Spark & Pit Room", dungeon=8)
        spark_pit_room_chest2 = Location(dungeon=8).add(DungeonChest(0x255)) # 50 rupees
        miniboss2_room = Location("D8 Rolling Bones Room", dungeon=8)
        sw_vire_room = Location("D8 Southwest Vire Room", dungeon=8)
        sw_vire_room_drop1 = Location(dungeon=8).add(DroppedKey(0x24C)) # small key
        vacuum_room = Location("D8 Vacuum Room", dungeon=8)
        vacuum_room_chest3 = Location(dungeon=8).add(DungeonChest(0x25C)) # compass
        spark_pot_room = Location("D8 Sparks Hidden Button Room", dungeon=8)
        slime_trap_room = Location("D8 Lava Chest Room", dungeon=8)
        slime_trap_room_chest4 = Location(dungeon=8).add(DungeonChest(0x259)) # slime trap
        zamboni_pit_west = Location("D8 West of Chasm Zamboni", dungeon=8)
        zamboni_pit_east = Location("D8 East of Chasm Zamboni", dungeon=8)
        zamboni_pit_east_drop2 = Location(dungeon=8).add(DroppedKey(0x25A)) # small key
        miniboss3_room = Location("D8 Smasher Room", dungeon=8)
        mimic_room = Location("D8 Mimic Room", dungeon=8)
        before_a_passage = Location("D8 Mimic Passageway Spawned", dungeon=8)
        after_a_passage = Location("D8 Beamos Hidden Button Room", dungeon=8)
        pot_pit_room = Location("D8 Pots & Pits Room", dungeon=8)
        pot_pit_room_doorway = Location("D8 Pots & Pits Room Door", dungeon=8)
        pot_pit_room_chest5 = Location(dungeon=8).add(DungeonChest(0x25F)) # beak
        before_e_passage = Location("D8 Pots, & Pits Room Stairs", dungeon=8)
        after_e_passage = Location("D8 Staircase Below Three Peahats", dungeon=8)
        pre_center_zamboni = Location("D8 North of Entrance", dungeon=8)
        before_b_passage = Location("D8 Staircase by Center Zamboni", dungeon=8)
        after_b_passage = Location("D8 Before Cueball", dungeon=8)
        before_c_passage = Location("D8 Before Passage to Boss", dungeon=8)
        switch_room = Location("D8 Switch Room", dungeon=8)
        pushblock_room = Location("D8 Pushblock Chest Area", dungeon=8)
        pushblock_room_chest6 = Location(dungeon=8).add(DungeonChest(0x24F)) # map
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
        after_d_passage = Location("D8 Staircase by Blaino", dungeon=8)
        miniboss_room = Location("D8 Blaino Room", dungeon=8)
        miniboss_cubby = Location("D8 Post Blaino Before Pegs", dungeon=8)
        rod_ledge = Location("D8 Blaino Reward Ledge", dungeon=8)
        rod_ledge_chest7 = Location(dungeon=8).add(DungeonChest(0x237)) # magic rod
        dodongo_area = Location("D8 Dodongo Area", dungeon=8)
        dodongo_area_drop3 = Location(dungeon=8).add(DroppedKey(0x23E)) # small key
        pre_lava_ledge = Location("D8 Ledge West of Dodongos", dungeon=8)
        lava_ledge = Location("D8 Lava Ledge", dungeon=8)
        lava_ledge_chest8 = Location(dungeon=8).add(DungeonChest(0x235)) # medicine
        slime_corridor = Location("D8 Corridor by Lava Ledge Chest", dungeon=8)
        after_g_passage = Location("D8 North Refill Room", dungeon=8)
        after_f_stairs = Location("D8 Ledge Above Dodongos", dungeon=8)
        after_f_stairs_chest9 = Location(dungeon=8).add(DungeonChest(0x23D)) # small key
        before_f_stairs = Location("D8 Northwest Area", dungeon=8)
        miniboss4_cubby = Location("D8 Cubby After Northwest Vire", dungeon=8)
        before_f_stairs_chest10 = Location(dungeon=8).add(DungeonChest(0x240)) # small key
        before_f_stairs_drop4 = Location(dungeon=8).add(DroppedKey(0x241)) # small key
        ledge_west_boss = Location("D8 West of Boss Door Ledge", dungeon=8)
        ledge_west_boss_chest11 = Location(dungeon=8).add(DungeonChest(0x23A)) # 50 rupees
        miniboss4_room = Location("D8 Cueball Room", dungeon=8)
        nw_zamboni_room = Location("D8 Two Torch Zamboni Puzzle", dungeon=8)
        nw_zamboni_room_chest12 = Location(dungeon=8).add(DungeonChest(0x232)) # nightmare key
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
        # west   
        entrance.connect(lava_beamos_room, r.enemy_requirements["VIRE"]) # Entrance <--> Lava Beamos Room
        lava_beamos_room.connect(miniboss1_room, r.enemy_requirements["SNAKE"]) # Lava Beamos Room <--> Hinox Room
        lava_beamos_room.connect(entrance, None, one_way=True) # Lava Beamos Room --> Entrance
        miniboss1_room.connect(sw_zamboni_area, r.miniboss_requirements["HINOX"]) # Hinox Room <--> Zamboni Intersection
        miniboss1_room.connect(lava_beamos_room, None, one_way=True) # Hinox Room --> Lava Beamos Room
        sw_zamboni_area.connect(sw_zamboni_area_chest1, None) # Zamboni Intersection <--> Left of Hinox Zamboni Chest
        sw_zamboni_area.connect(sw_zamboni_area_chest2, MAGIC_ROD) # Zamboni Intersection <--> Two Torches Room Chest 
        sw_zamboni_area.connect(spark_pit_room, OR(HOOKSHOT, FEATHER)) # Zamboni Intersection <--> Southwest Spark & Pit Room
        spark_pit_room.connect(spark_pit_room_chest2, None) # Southwest Spark & Pit Room <--> Spark, Pit Chest
        sw_zamboni_area.connect(miniboss1_room, None, one_way=True) # Zamboni Intersection --> Hinox Room
        sw_zamboni_area.connect(miniboss2_room, None, one_way=True) # Zamboni Intersection --> Rolling Bones Room
        miniboss2_room.connect(sw_vire_room, r.miniboss_requirements["ROLLING_BONES"]) # Rolling Bones Room <--> Southwest Vire Room
        sw_vire_room.connect(sw_vire_room_drop1, r.attack_hookshot_no_bomb) #  <-->  # takes 11 bombs minimum to get this from entrance, so bombs are excluded
        miniboss2_room.connect(vacuum_room, r.miniboss_requirements["ROLLING_BONES"]) # Rolling Bones Room <--> Vacuum Room
        vacuum_room.connect(vacuum_room_chest3, None) # Vacuum Room <--> Vacuum Mouth Chest
        vacuum_room.connect(entrance, None, one_way=True) # Vacuum Room --> Entrance
        # east
        entrance.connect(spark_pot_room, r.enemy_requirements["VIRE"], one_way=True) # Entrance <--> Sparks Hidden Button Room
        spark_pot_room.connect(entrance, POWER_BRACELET, one_way=True) # Sparks Hidden Button Roome --> Entrance
        spark_pot_room.connect(slime_trap_room, POWER_BRACELET) # Sparks Hidden Button Room <--> Lava Chest Room
        slime_trap_room.connect(slime_trap_room_chest4, None) # Lava Chest Room <--> Right Lava Chest
        slime_trap_room.connect(spark_pot_room, None, one_way=True) # Lava Chest Room --> Sparks Hidden Button Room
        slime_trap_room.connect(zamboni_pit_west, FEATHER) # Lava Chest Room <--> West of Chasm Zamboni
        zamboni_pit_west.connect(slime_trap_room, HOOKSHOT, one_way=True)
        spark_pot_room.connect(mimic_room, POWER_BRACELET) # Sparks Hidden Button Room <--> Mimic Room
        mimic_room.connect(spark_pot_room, None, one_way=True) # Mimic Room --> Sparks Hidden Button Room
        mimic_room.connect(before_a_passage, r.enemy_requirements["MIMIC"]) # Mimic Room <--> Mimic Passageway Spawned
        before_a_passage.connect(mimic_room, None, one_way=True) # Mimic Passageway Spawned <--> Mimic Room
        before_a_passage.connect(after_a_passage, FEATHER) # Lava Chest Room <--> Mimic Passageway Spawned
        zamboni_pit_east.connect(zamboni_pit_west, None, one_way=True) # East of Chasm Zamboni <--> West of Chasm Zamboni
        zamboni_pit_east.connect(zamboni_pit_east_drop2, None) # East of Chasm Zamboni <--> Zamboni, Two Zol Key
        zamboni_pit_east.connect(switch_room, BOMB) # East of Chasm Zamboni <--> Switch Room
        switch_room.connect(before_c_passage, BOMB) # Switch Room <--> Before Passage to Boss
        zamboni_pit_east.connect(miniboss3_room, None, one_way=True) # East of Chasm Zamboni --> Smasher Room
        miniboss3_room.connect(zamboni_pit_east, r.miniboss_requirements["SMASHER"], one_way=True) # Smasher Room --> East of Chasm Zamboni
        miniboss3_room.connect(after_a_passage, r.miniboss_requirements["SMASHER"], one_way=True) # Smasher Room --> Beamos Hidden Button Room
        after_a_passage.connect(miniboss3_room, POWER_BRACELET, one_way=True) # Beamos Hidden Button Room --> Smasher Room
        miniboss3_room.connect(pot_pit_room_doorway, r.miniboss_requirements["SMASHER"], one_way=True) # Smasher Room <--> Pots & Pits Room Door
        pot_pit_room_doorway.connect(miniboss3_room, AND(OR(FEATHER, POWER_BRACELET), r.enemy_requirements["SNAKE"]), one_way=True) # Pots & Pits Room Door --> Smasher Room #TODO: is there a way to clear this room and get to smasher for higher logic levels? (like boomerang or )
        pot_pit_room_doorway.connect(pot_pit_room, OR(FEATHER, POWER_BRACELET)) # Pots & Pits Room Door <--> Pots & Pits Room
        pot_pit_room.connect(pot_pit_room_chest5, None) # Pots & Pits Room <--> Four Ropes Pot Chest
        pot_pit_room.connect(before_e_passage, POWER_BRACELET) # Pots & Pits Room <--> Pots, & Pits Room Stairs
        before_e_passage.connect(after_e_passage, FEATHER) # Pots, & Pits Room Stairs <--> Staircase Below Three Peahats
        # north
        entrance.connect(pre_center_zamboni, FEATHER) # Entrance <--> North of Entrance
        pre_center_zamboni.connect(before_b_passage, None, one_way=True) # North of Entrance --> Staircase by Center Zamboni
        before_b_passage.connect(spark_pot_room, None, one_way=True) # Staircase by Center Zamboni --> Sparks Hidden Button Room
        pre_center_zamboni.connect(before_c_passage, None, one_way=True) # North of Entrance --> Before Passage to Boss # new logic
        before_c_passage.connect(slime_trap_room, None, one_way=True) # Before Passage to Boss --> Lava Chest Room
        pre_center_zamboni.connect(after_e_passage, None, one_way=True) # North of Entrance --> Staircase Below Three Peahats
        pre_center_zamboni.connect(lava_left_corridor, None) # North of Entrance --> 'L' Shaped Corridor # two way due to pushblock
        pre_center_zamboni.connect(loop_ledge, None, one_way=True) # North of Entrance --> Useless Ledge
        pre_center_zamboni.connect(pre_center_keyblock, None, one_way=True) # North of Entrance --> Before Central Keyblock
        lava_left_corridor.connect(after_e_passage, BOMB) # 'L' Shaped Corridor <--> Staircase Below Three Peahats
        lava_left_corridor.connect(pushblock_room, None) # 'L' Shaped Corridor <--> Pushblock Chest Area
        pushblock_room.connect(pushblock_room_chest6, None) # Pushblock Chest Area <--> Push Block Chest
        loop_ledge.connect(before_c_passage, None, one_way=True) # Useless Ledge --> Before Passage to Boss
        pre_center_keyblock.connect(heart_vire, FOUND(KEY8, 1)) # Before Central Keyblock <--> Floating Heart & Vire Area
        pre_center_keyblock.connect(peahat_area, FOUND(KEY8, 1)) # Before Central Keyblock <--> Peahat Area
        pre_center_keyblock.connect(loop_ledge, FEATHER, one_way=True) # Before Central Keyblock --> Useless Ledge
        peahat_area.connect(heart_vire, FOUND(KEY8, 1)) # Peahat Area <--> Floating Heart & Vire Area
        peahat_area.connect(after_e_passage, None, one_way=True) # Peahat Area --> Staircase Below Three Peahats
        heart_vire.connect(before_g_passage, FOUND(KEY8, 2)) # Floating Heart & Vire Area <--> Blade Room
        before_g_passage.connect(hidden_arrow_room, None, one_way=True) # Blade Room --> Hidden Arrow Room
        before_g_passage.connect(after_g_passage, AND(FEATHER, HOOKSHOT)) # Blade Room <--> North Refill Room
        hidden_arrow_room.connect(dodongo_area, r.enemy_requirements["HIDING_ZOL"]) # Hidden Arrow Room <--> Dodongo Area
        hidden_arrow_room.connect(dark_east_spark, BOMB) # Hidden Arrow Room <--> Dark East (Spark Side)
        # dark
        dark_east_spark.connect(dark_east_zol, FEATHER) # Dark East (Spark Side) <--> Dark East (Zol Side)
        dark_east_zol.connect(dark_center, FOUND(KEY8, 4)) # Dark East (Zol Side) <--> Dark Center
        dark_center.connect(peahat_area, AND(BOMB, FEATHER), one_way=True) # Dark Center --> Peahat Area # coming form peahat area could be hard due to obscurity
        dark_center.connect(dark_west, r.enemy_requirements["SNAKE"], one_way=True) # Dark Center <--> Dark West
        dark_west.connect(peahat_area, AND(BOMB, FEATHER), one_way=True) # Dark West --> Peahat Area # coming form peahat area could be hard due to obscurity
        dark_west.connect(before_f_stairs, AND(BOMB, FEATHER), one_way=True) # Dark West --> Northwest Area
        dark_west.connect(dark_center, AND(r.enemy_requirements["SNAKE"], r.enemy_requirements["PEAHAT"])) # Dark West <--> Dark Center
        dark_west.connect(dark_center_torches, FOUND(KEY8, 3)) # Dark West <--> Dark Center Between Torches # ???
        dark_center_torches.connect(dark_center, None, one_way=True) # Dark Center Between Torches --> Dark Center
        dark_center_torches.connect(dark_center_pre_keyblock, HOOKSHOT) # Dark Center Between Torches <--> Dark Center Before Keyblock
        dark_center_pre_keyblock.connect(dark_center, None, one_way=True) # Dark Center Before Keyblock --> Dark Center
        dark_center_pre_keyblock.connect(before_d_passage, FOUND(KEY8, 7)) # Dark Center Before Keyblock <--> Dark Room Staircase
        # miniboss
        before_d_passage.connect(after_d_passage, FEATHER) # Dark Room Staircase <--> Staircase by Blaino
        after_d_passage.connect(miniboss_room, None, one_way=True) # Staircase by Blaino <--> Blaino Room
        miniboss_room.connect(miniboss_cubby, r.miniboss_requirements[world_setup.miniboss_mapping[7]]) # Blaino Room <--> Post Blaino Before Pegs
        miniboss_room.connect(entrance, None, one_way=True) # Blaino Room <--> Entrance # Blaino punches you back to entrance
        rod_ledge.connect(rod_ledge_chest7, None) # Blaino Reward Ledge <--> Magic Rod Chest
        rod_ledge.connect(after_d_passage, None, one_way=True) # Blaino Reward Ledge <--> Staircase by Blaino
        switch_room.connect(rod_ledge_chest7, AND(BOMB, FEATHER, POWER_BRACELET, HOOKSHOT, FOUND(KEY8, 7), r.enemy_requirements["SNAKE"], r.miniboss_requirements[world_setup.miniboss_mapping[7]]), one_way=True) # Switch Room <--> Magic Rod Chest # explicitly include normal logic from switch room to rod chest
        # dodongo
        hidden_arrow_room.connect(dodongo_area, None, one_way=True) # Hidden Arrow Room <--> Dodongo Area
        dodongo_area.connect(dodongo_area_drop3, r.enemy_requirements["GIBDO"]) # Dodongo Area <--> Gibdos on Cracked Floor Key # 2 gibdos cracked floor; technically possible to use pits to kill but dumb
        dodongo_area.connect(pre_lava_ledge, FEATHER) # Dodongo Area <--> Ledge West of Dodongos
        pre_lava_ledge.connect(slime_corridor, None, one_way=True) # Ledge West of Dodongos <--> Corridor by Lava Ledge Chest
        pre_lava_ledge.connect(lava_ledge, HOOKSHOT) # Ledge West of Dodongos <--> Lava Ledge
        pre_lava_ledge.connect(after_g_passage, None, one_way=True) # Ledge West of Dodongos <--> North Refill Room
        lava_ledge.connect(lava_ledge_chest8, None) # Lava Ledge <--> Lava Ledge Chest
        lava_ledge.connect(after_g_passage, None, one_way=True) # Lava Ledge <--> North Refill Room
        dodongo_area.connect(after_f_stairs_chest9, AND(FEATHER, FOUND(KEY8, 4), r.miniboss_requirements["DODONGO"]), one_way=True) # Dodongo Area <-->  #TODO: assumes vanilla tal tal exits
        after_f_stairs.connect(dodongo_area, None, one_way=True) # Ledge Above Dodongos <--> Dodongo Area
        before_f_stairs.connect(after_f_stairs, None) # Northwest Area <--> Ledge Above Dodongos # assumes vanilla tal tal exits
        # northwest
        slime_corridor.connect(before_f_stairs, FOUND(KEY8, 4)) # Corridor by Lava Ledge Chest <--> Northwest Area
        before_f_stairs.connect(before_f_stairs_chest10, None) # Northwest Area <--> Beamos Blocked Chest
        before_f_stairs.connect(before_f_stairs_drop4, BOW) # Northwest Area <--> Lava Arrow Statue Key
        miniboss4_cubby.connect(ledge_west_boss, HOOKSHOT) # Cubby After Northwest Vire <--> West of Boss Door Ledge
        ledge_west_boss.connect(ledge_west_boss_chest11, None) # West of Boss Door Ledge <--> West of Boss Door Ledge Chest
        ledge_west_boss.connect(before_f_stairs, None, one_way=True) # West of Boss Door Ledge --> Northwest Area
        before_f_stairs.connect(sw_zamboni_area, None, one_way=True) # Northwest Area --> Zamboni Intersection 
        # tal tal
        if back_entrance_heartpiece is not None:
            Location().add(HeartPiece(back_entrance_heartpiece)).connect(before_f_stairs, None) # heart piece
        # cueball
        before_b_passage.connect(after_b_passage, AND(FEATHER, MAGIC_ROD)) # Staircase by Center Zamboni <--> Before Cueball
        after_b_passage.connect(before_b_passage, MAGIC_ROD, one_way=True) # Before Cueball <--> Staircase by Center Zamboni
        after_b_passage.connect(miniboss4_cubby, None, one_way=True) # Before Cueball <--> Cubby After Northwest Vire
        before_f_stairs.connect(miniboss4_cubby, AND(r.enemy_requirements["VIRE"], AND(r.enemy_requirements["SNAKE"]))) # Northwest Area <--> Cubby After Northwest Vire
        miniboss4_cubby.connect(before_f_stairs, None, one_way=True) # Cubby After Northwest Vire <--> Northwest Area
        after_b_passage.connect(miniboss4_room, FOUND(KEY8, 7)) # Before Cueball <--> Cueball Room
        miniboss4_room.connect(nw_zamboni_room, AND(FEATHER, r.miniboss_requirements["CUE_BALL"])) # Cueball Room <--> Two Torch Zamboni Puzzle
        nw_zamboni_room.connect(nw_zamboni_room_chest12, None) # Two Torch Zamboni Puzzle <--> Nightmare Key
        # boss
        before_c_passage.connect(after_c_passage, AND(FEATHER, MAGIC_ROD)) # Before Passage to Boss <--> Outside Boss Door
        after_c_passage.connect(boss_room, NIGHTMARE_KEY8) # Outside Boss Door <--> Boss Room
        boss_room.connect(boss_room_drop5, r.boss_requirements[world_setup.boss_mapping[7]]) # Boss Room <--> Hot Head Heart Container
        boss_room.connect(instrument, AND(FEATHER, r.boss_requirements[world_setup.boss_mapping[7]])) # Boss Room <--> Instrument Room

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            #south
            zamboni_pit_west.connect(zamboni_pit_east, r.tight_jump) # diagonal jump over the pits to reach zamboni
            after_a_passage.connect(before_a_passage, None, one_way=True) # take some damage but itemless
            pot_pit_room_doorway.connect(miniboss3_room, r.throw_pot, one_way=True) # 4 pots to kill 4 ropes
            #center
            peahat_area.connect(heart_vire, r.tight_jump) # around keyblock
            peahat_area.connect(dark_center, AND(BOMB, FEATHER)) # pixel perfect bomb placement
            peahat_area.connect(dark_west, AND(BOMB, FEATHER)) # pixel perfect bomb placement
            before_f_stairs.connect(dark_west, AND(BOMB, FEATHER)) # pixel perfect bomb placement
            #north
            dodongo_area.connect(dodongo_area_drop3, OR(HOOKSHOT, MAGIC_ROD)) # crack one of the floor tiles and hookshot the gibdos in, or burn the gibdos and make them jump into pit
            before_f_stairs.connect(miniboss4_cubby, r.throw_pot) # throw 4 of the 5 pots to kill 2 ropes and vire
            before_f_stairs.connect(sw_vire_room_drop1, AND(r.miniboss_requirements["ROLLING_BONES"], r.enemy_requirements["VIRE"]), one_way=True) # allows bombs to kill vire but only from dropdown in unlit torch room
            after_f_stairs.connect(after_f_stairs_chest9, BOMB) # throw bombs from ledge to defeat dodongos

        if options.logic == 'glitched' or options.logic == 'hell':
            #south
            sw_zamboni_area.connect(spark_pit_room, r.pit_buffer_itemless) # pit buffer down across the pit then walk diagonally between pits
            before_e_passage.connect(pot_pit_room, AND(r.hookshot_clip_block, r.super_jump_feather), one_way=True) # new logic
            #center
            after_e_passage.connect(peahat_area, r.sideways_block_push) # sideways block push in peahat room to get past keyblock
            after_e_passage.connect(lava_left_corridor, AND(r.wall_clip, r.super_jump_feather), one_way=True)
            lava_left_corridor.connect(pre_center_zamboni, r.jesus_jump) # jesus jump through center lava to get back to zamboni
            after_e_passage.connect(pre_center_zamboni, r.jesus_jump) # jesus jump through center lava to get back to zamboni
            pre_center_keyblock.connect(pre_center_zamboni, r.jesus_jump) # jesus jump through center lava to get back to zamboni
            loop_ledge.connect(pre_center_zamboni, r.jesus_jump) # jesus jump through center lava to get back to zamboni
            before_c_passage.connect(pre_center_zamboni, r.jesus_jump) # jesus jump through center lava to get back to zamboni
            peahat_area.connect(before_f_stairs, r.jesus_jump) # use jesus jump in refill room left of peahats to clip bottom wall and push bottom block left, to get a place to super jump
            before_c_passage.connect(loop_ledge, AND(r.wall_clip, r.super_jump_feather)) # wall clip on stairs, superjump over blocks
            loop_ledge.connect(pre_center_keyblock, AND(r.wall_clip, r.super_jump_feather)) # wall clip on useless ledge, and superjump over blocks
            pre_center_keyblock.connect(heart_vire, r.super_jump_feather) # push block into lava, get wall clipped on left wall and superjump right then up to skip keyblock
            #dark
            dark_center.connect(dark_center_torches, r.super_jump_feather) # wall clip and super jump
            dark_center.connect(dark_center_pre_keyblock, r.super_jump_feather) # wall clip and super jump
            dark_center.connect(dark_east_zol, r.hookshot_clip, one_way=True) # hookshot clip off the zols to get through without spending key
            dark_center_torches.connect(before_d_passage, r.bookshot) # skip keyblock to blaino
            #miniboss
            miniboss_cubby.connect(rod_ledge, r.super_jump_feather) # superjump to skip over pegs after blaino
            #north
            before_f_stairs.connect(slime_corridor, r.jesus_jump) # from up left you can jesus jump / lava swim around the key door next to the boss.
            after_g_passage.connect(slime_corridor, r.jesus_jump) # jesus jump through lava ledges
            slime_corridor.connect(before_f_stairs, r.jesus_jump) # jesus jump below key door through screen transision to skip key requirement
            miniboss4_cubby.connect(after_b_passage, r.super_jump_feather) # superjump to get to cueball doorway
            after_g_passage.connect(lava_ledge, AND(r.jesus_jump, r.super_jump_feather)) # jesus jump and use any way to wall clip / super jump to reach lava ledge chest
            slime_corridor.connect(lava_ledge, AND(r.jesus_jump, r.super_jump_feather)) # jesus jump and use any way to wall clip / super jump to reach lava ledge chest
            dodongo_area.connect(after_f_stairs, r.super_jump_feather) # wall clip and superjump to dojongo ledge
            dodongo_area.connect(after_f_stairs_chest9, AND(r.miniboss_requirements["DODONGO"], r.super_jump_feather)) # kill dodongos and superjump to immediately get chest
            before_f_stairs.connect(after_c_passage, r.super_jump_feather, one_way=True) # superjump off the bottom or right wall to jump over to the boss door

        if options.logic == 'hell':
            #south
            sw_zamboni_area.connect(before_f_stairs, r.zoomerang_buffer) # pixel perfect left-facing zoomerang followed up by another zoomerang to get un-stuck. unreliable without shovel
            before_a_passage.connect(after_a_passage, r.boots_bonk_2d_hell) #TODO: replace with row below, also consider moving this to hard
            #TODO: before_a_passage.connect(after_a_passage, OR(r.boots_bonk_2d_hell, r.bracelet_bounce_2d_spikepit, r.toadstool_bounce_2d_spikepit)) # 
            pot_pit_room_doorway.connect(pot_pit_room_chest5, r.pit_buffer_itemless, one_way=True) # pit buffer from south smasher doorway to the SE room chest
            pot_pit_room.connect(pot_pit_room_doorway, AND(r.hookshot_clip_block, r.hookshot_spam_pit)) # can get to SE room doorway with just hookshot spam
            pot_pit_room.connect(before_e_passage, r.zoomerang_buffer, one_way=True) # new logic, zoomerang gets you to SE room passage without bracelet. unreliable without shovel #TODO: check if possible in reverse with pot dislodge method
            before_e_passage.connect(pot_pit_room, r.shaq_jump, one_way=True) #TODO: this is wild, attempt shaq jump in lower right corner of staircase area until it works
            before_e_passage.connect(after_e_passage, r.boots_bonk, one_way=True) # boots bonking from rope room to below peahats through passage
            zamboni_pit_west.connect(slime_trap_room, r.boots_bonk, one_way=True) # boots bonk to hop over 1 tile of lava
            #center
            entrance.connect(pre_center_zamboni, AND(r.jesus_buffer, r.lava_swim_sword)) #TODO: update to swordless probably - boots bonk around the top left corner at vire, get on top of the wall to bonk to the left, and transition while slashing sword
            peahat_area.connect(before_f_stairs, AND(r.jesus_buffer, r.lava_swim)) # bonk to set up lava swim on the screen transition
            lava_left_corridor.connect(pre_center_zamboni, r.jesus_buffer, one_way=True) # jesus buffer through center lava to get back to zamboni
            after_e_passage.connect(pre_center_zamboni, r.jesus_buffer, one_way=True) # jesus buffer through center lava to get back to zamboni
            pre_center_keyblock.connect(pre_center_zamboni, r.jesus_buffer, one_way=True) # jesus buffer through center lava to get back to zamboni
            pre_center_keyblock.connect(before_b_passage, r.jesus_buffer, one_way=True) # jesus buffer through center lava to get to staircase
            loop_ledge.connect(before_b_passage, r.jesus_buffer, one_way=True) # jesus buffer through center lava to get to staircase
            before_b_passage.connect(loop_ledge, HOOKSHOT, one_way=True) # while standing on staircase, hookshot up, then hookshot right on the frame that you splash the lava - pausing on the splash frame to buffer is OK
            before_c_passage.connect(before_b_passage, r.jesus_buffer) # jesus buffer between staircase to cueball and staircase to boss
            before_b_passage.connect(pre_center_zamboni, r.jesus_buffer, one_way=True) # hop off ledge from staircase to cueball and then jesus buffer
            loop_ledge.connect(heart_vire, r.hookshot_clip_block, one_way=True) # get in block walk-off-ledge and pause buffering, then walk-jump into block. hoookshot clip off vire to get out and skip key requirement
            #TODO: before_g_passage.connect(after_g_passage, AND(HOOKSHOT, r.damage_boost_special, "TOADSTOOL2"), one_way=True) # new logic - use toadstool after hurt by goomba, and bouncing off goomba to freeze after gaining height. Hold "A" button during the damage boost to get extra boost
            #dark
            before_f_stairs.connect(dark_west, AND(BOMB, r.lava_swim), one_way=True) # pixel perfect bomb placement to open door, return with lava swim
            dark_west.connect(before_f_stairs, AND(BOMB, HOOKSHOT, r.jesus_buffer), one_way=True) # boots bonk then use hookshot when splashing to grab spark's block, will respawn near spark block
            dark_west.connect(peahat_area, AND(BOMB, r.jesus_buffer), one_way=True) # bomb the wall and boots bonk + pause buffer until on land
            dark_center.connect(peahat_area, AND(BOMB, r.jesus_buffer), one_way=True) # bomb the wall and boots bonk + pause buffer until on land
            dark_east_zol.connect(dark_east_spark, OR(r.hookshot_spam_pit, r.boots_bonk)) # spam hookshot or simply boots bonk to get over 1 block pit
            dark_center.connect(before_d_passage, AND(r.super_jump_feather, r.ledge_super_bump), one_way=True) # wall clip then superjump to spot 2-tiles left of staircase. once rope is closeby, shield-backflip to staircase
            dark_center_pre_keyblock.connect(before_d_passage, r.zoomerang_buffer, one_way=True) # right-facing zoomerang to geth through keyblock. unreliable without shovel
            #miniboss
            before_d_passage.connect(after_d_passage, r.boots_bonk_2d_hell) # get through 2d section with boots bonks
            switch_room.connect(rod_ledge_chest7, AND(BOMB, OR(AND(r.jesus_buffer, MAGIC_ROD), AND(POWER_BRACELET, r.boots_bonk_2d_hell, r.sideways_block_push)), FOUND(KEY8, 7), r.enemy_requirements["PEAHAT"], r.enemy_requirements["SNAKE"], HOOKSHOT, r.miniboss_requirements[world_setup.miniboss_mapping[7]]), one_way=True) # hell logic for getting rod chest without feather
            #dodongo
            dodongo_area.connect(dodongo_area_drop3, AND(FEATHER, SHIELD)) # lock gibdos into pits and crack the tile they stand on, then use shield to bump them into the pit
            dodongo_area.connect(pre_lava_ledge, r.boots_bonk) # bonk over 1 block of lava, no buffer
            dodongo_area.connect(after_f_stairs_chest9, AND(r.miniboss_requirements["DODONGO"], r.boots_bonk, r.lava_swim), one_way=True) # kill dodongos and lava swim to get through tal tal connector to chest
            pre_lava_ledge.connect(lava_ledge, r.super_jump_feather) # walk off ledge and pause buffer to get in position
            slime_corridor.connect(before_f_stairs, AND(r.jesus_buffer, r.lava_swim)) # boots bonk and lava swim around small key door near boss
            #northwest
            before_b_passage.connect(after_b_passage, AND(r.boots_bonk_2d_hell, MAGIC_ROD)) # boots bonk in 2d to use magic rod on upper ice blocks
            before_f_stairs.connect(peahat_area, r.jesus_buffer, one_way=True) # hell - from refill room push block and boots bonk into jesus buffer then bonk again
            before_f_stairs.connect(peahat_area, AND(r.jesus_buffer, r.lava_swim)) #hell can be troublesome, if having issues, exit to tal tal and try again or use sword to guarantee it
            before_f_stairs.connect(peahat_area, AND(r.jesus_buffer, r.lava_swim)) # use boots bonk next to 3x peahats to get on top of lava, and transition left while slashing sword
            #TODO: before_f_stairs.connect(ledge_west_boss, r.super_bump) # super bump while wall clipped on stairs to tal tal
            #TODO: before_f_stairs.connect(miniboss4_cubby, r.super_bump) # super bump while wall clipped on stairs to tal tal
            miniboss4_room.connect(nw_zamboni_room, AND(r.boots_bonk, r.miniboss_requirements["CUE_BALL"])) # use a boots bonk to cross the lava in cueball room
            #boss
            before_c_passage.connect(after_c_passage, AND(r.boots_bonk_2d_hell, MAGIC_ROD)) # boots bonk through 2d ice section
            after_c_passage.connect(before_f_stairs, AND(r.jesus_jump, r.zoomerang)) # jj across lava uand then a few dozen consecutive buffers to get lodged lower left corner of rain, the right-facing zoomerang to escape
            boss_room.connect(instrument, AND(r.boots_bonk, r.boss_requirements[world_setup.boss_mapping[7]])) # boots bonk in boss room to collect instrument
            
        self.entrance = entrance
        self.final_room = instrument


class NoDungeon8:
    def __init__(self, options, world_setup, r):
        entrance = Location("D8 Entrance", dungeon=8)
        boss = Location(dungeon=8).add(HeartContainer(0x234)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[7]])
        instrument = Location(dungeon=8).add(Instrument(0x230)).connect(boss, FEATHER) # jump over the lava to get to the instrument

        self.entrance = entrance
