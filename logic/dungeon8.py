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
        spark_pit_room_chest3 = Location(dungeon=8).add(DungeonChest(0x255)) # 50 rupees
        miniboss2_room = Location("D8 Rolling Bones Room", dungeon=8)
        sw_vire_room = Location("D8 Southwest Vire Room", dungeon=8)
        sw_vire_room_drop1 = Location(dungeon=8).add(DroppedKey(0x24C)) # small key
        vacuum_room = Location("D8 Vacuum Room", dungeon=8)
        vacuum_room_chest4 = Location(dungeon=8).add(DungeonChest(0x25C)) # compass
        spark_pot_room = Location("D8 Sparks Hidden Button Room", dungeon=8)
        slime_trap_room = Location("D8 Lava Chest Room", dungeon=8)
        slime_trap_room_chest5 = Location(dungeon=8).add(DungeonChest(0x259)) # slime trap
        zamboni_pit_west = Location("D8 West of Chasm Zamboni", dungeon=8)
        zamboni_pit_east = Location("D8 East of Chasm Zamboni", dungeon=8)
        zamboni_pit_east_drop2 = Location(dungeon=8).add(DroppedKey(0x25A)) # small key
        miniboss3_room = Location("D8 Smasher Room", dungeon=8)
        mimic_room = Location("D8 Mimic Room", dungeon=8)
        before_a_passage = Location("D8 Mimic Passageway Spawned", dungeon=8)
        after_a_passage = Location("D8 Beamos Hidden Button Room", dungeon=8)
        after_a_passage_owl1 = Location(dungeon=8).add(OwlStatue(0x253)) # hint
        pot_pit_room = Location("D8 Pots & Pits Room", dungeon=8)
        pot_pit_room_doorway = Location("D8 Pots & Pits Room Door", dungeon=8)
        pot_pit_room_chest6 = Location(dungeon=8).add(DungeonChest(0x25F)) # beak
        after_e_passage = Location("D8 Pots & Pits Room Stairs", dungeon=8)
        before_e_passage = Location("D8 Staircase Below Three Peahats", dungeon=8)
        pre_center_zamboni = Location("D8 North of Entrance", dungeon=8)
        before_b_passage = Location("D8 Staircase by Center Zamboni", dungeon=8)
        after_b_passage = Location("D8 Before Cueball", dungeon=8)
        before_c_passage = Location("D8 Before Passage to Boss", dungeon=8)
        switch_room = Location("D8 Switch Room", dungeon=8)
        switch_room_switch = Location("D8 Switch", dungeon=8).add(KeyLocation("SWITCH8"))
        pushblock_room = Location("D8 Pushblock Chest Area", dungeon=8)
        pushblock_room_chest7 = Location(dungeon=8).add(DungeonChest(0x24F)) # map
        bombwall_corridor = Location("D8 Bombwall Corridor", dungeon=8)
        pre_center_keyblock = Location("D8 Before Central Keyblock", dungeon=8)
        loop_ledge = Location("D8 Useless Ledge", dungeon=8)
        peahat_area = Location("D8 Peahat Area", dungeon=8)
        heart_vire = Location("D8 Floating Heart & Vire Area", dungeon=8)
        before_g_passage = Location("D8 Blade Room", dungeon=8)
        hidden_arrow_room = Location("Hidden Arrow Room", dungeon=8)
        hidden_arrow_room_owl2 = Location(dungeon=8).add(OwlStatue(0x245)) # hint
        dark_east_zol = Location("D8 Dark East (Zol Side)", dungeon=8)
        dark_east_spark = Location("D8 Dark East (Spark Side)", dungeon=8)
        dark_center = Location("D8 Dark Center", dungeon=8)
        dark_center_torches = Location("D8 Dark Between Torches", dungeon=8)
        dark_center_pre_keyblock = Location("D8 Dark CBefore Keyblock", dungeon=8)
        dark_west = Location("D8 Dark West", dungeon=8)
        before_d_passage = Location("D8 Dark Room Staircase", dungeon=8)
        after_d_passage = Location("D8 Staircase by Blaino", dungeon=8)
        miniboss_room = Location("D8 Blaino Room", dungeon=8)
        miniboss_cubby = Location("D8 Before Pegs After Blaino", dungeon=8)
        rod_ledge = Location("D8 Blaino Reward Ledge", dungeon=8)
        rod_ledge_chest8 = Location(dungeon=8).add(DungeonChest(0x237)) # magic rod
        dodongo_area = Location("D8 Dodongo Area", dungeon=8)
        dodongo_area_drop3 = Location(dungeon=8).add(DroppedKey(0x23E)) # small key
        pre_lava_ledge = Location("D8 Ledge West of Dodongos", dungeon=8)
        lava_ledge = Location("D8 Lava Ledge", dungeon=8)
        lava_ledge_chest9 = Location(dungeon=8).add(DungeonChest(0x235)) # medicine
        slime_corridor = Location("D8 Corridor by Lava Ledge Chest", dungeon=8)
        after_g_passage = Location("D8 North Refill Room", dungeon=8)
        after_f_stairs = Location("D8 Ledge Above Dodongos", dungeon=8)
        after_f_stairs_chest10 = Location(dungeon=8).add(DungeonChest(0x23D)) # small key
        before_f_stairs = Location("D8 Northwest Area", dungeon=8)
        taltal_passage = Location("D8 Tal Tal Connector")
        before_f_stairs_owl3 = Location(dungeon=8).add(OwlStatue(0x241)) # hint
        miniboss4_cubby = Location("D8 Cubby Before Cueball", dungeon=8)
        before_f_stairs_chest11 = Location(dungeon=8).add(DungeonChest(0x240)) # small key
        before_f_stairs_drop4 = Location(dungeon=8).add(DroppedKey(0x241)) # small key
        ledge_west_boss = Location("D8 Ledge by NW Exit", dungeon=8)
        ledge_west_boss_chest12 = Location(dungeon=8).add(DungeonChest(0x23A)) # 50 rupees
        miniboss4_room = Location("D8 Cueball Room", dungeon=8)
        nw_zamboni_room = Location("D8 Two Torch Zamboni Puzzle", dungeon=8)
        nw_zamboni_room_chest13 = Location(dungeon=8).add(DungeonChest(0x232)) # nightmare key
        after_c_passage = Location("Outside Boss Door", dungeon=8)
        boss_room = Location("D8 Boss Room", dungeon=8)
        boss_room_drop5 = Location(dungeon=8).add(HeartContainer(0x234)) # heart container
        instrument = Location("D8 Instrument Room", dungeon=8).add(Instrument(0x230)) # instrument

        # back exits
        taltal_passage.connect((before_f_stairs, after_f_stairs))
        if back_entrance_heartpiece is not None:
            taltal_chest = Location().add(HeartPiece(back_entrance_heartpiece))
            taltal_passage.connect(taltal_chest, back=False) # heart piece
        
        # connections
        # west   
        entrance.connect((lava_beamos_room, spark_pot_room), r.enemy_requirements["VIRE"], back=False)
        lava_beamos_room.connect(entrance, back=False)
        lava_beamos_room.connect(miniboss1_room, r.enemy_requirements["SNAKE"], back=None)
        miniboss1_room.connect(sw_zamboni_area, r.miniboss_requirements["HINOX"], back=None)
        sw_zamboni_area.connect((sw_zamboni_area_chest1, miniboss2_room), back=False)
        sw_zamboni_area.connect(sw_zamboni_area_chest2, MAGIC_ROD, back=False)
        sw_zamboni_area.connect(spark_pit_room, OR(HOOKSHOT, FEATHER), back=False)
        spark_pit_room.connect(spark_pit_room_chest3, back=False)
        miniboss2_room.connect((sw_vire_room, vacuum_room, sw_zamboni_area), r.miniboss_requirements["ROLLING_BONES"], back=False)
        sw_vire_room.connect(sw_vire_room_drop1, r.attack_hookshot_no_bomb, back=False) # takes 11 bombs minimum to get this from entrance, so bombs are excluded
        vacuum_room.connect((vacuum_room_chest4, entrance), back=False) # let vacuum warp you to entrance
        # east
        spark_pot_room.connect((entrance, slime_trap_room, mimic_room), POWER_BRACELET, back=False)
        slime_trap_room.connect((slime_trap_room_chest5, spark_pot_room), back=False)
        slime_trap_room.connect(zamboni_pit_west, FEATHER, back=OR(FEATHER, HOOKSHOT))
        mimic_room.connect(spark_pot_room, back=False)
        mimic_room.connect(before_a_passage, r.enemy_requirements["MIMIC"], back=None)
        before_a_passage.connect(after_a_passage, FEATHER)
        zamboni_pit_east.connect((zamboni_pit_east_drop2, zamboni_pit_west, miniboss3_room), back=False)
        switch_room.connect((zamboni_pit_east, before_c_passage), BOMB)
        switch_room.connect(switch_room_switch, r.hit_switch, back=False)
        miniboss3_room.connect((zamboni_pit_east, after_a_passage, pot_pit_room_doorway), r.miniboss_requirements["SMASHER"], back=False)
        after_a_passage.connect(miniboss3_room, POWER_BRACELET, back=False)
        pot_pit_room_doorway.connect(miniboss3_room, AND(OR(FEATHER, POWER_BRACELET), r.enemy_requirements["SNAKE"]), back=False)
        pot_pit_room_doorway.connect(pot_pit_room, OR(FEATHER, POWER_BRACELET))
        pot_pit_room.connect(pot_pit_room_chest6, back=False)
        pot_pit_room.connect(after_e_passage, POWER_BRACELET)
        # center
        entrance.connect(pre_center_zamboni, FEATHER)
        pre_center_zamboni.connect((bombwall_corridor, before_e_passage, pre_center_keyblock, loop_ledge, before_c_passage, before_b_passage), back=False)
        before_b_passage.connect(spark_pot_room, back=False)
        before_c_passage.connect(slime_trap_room, back=False)
        bombwall_corridor.connect(pre_center_zamboni, FEATHER, back=False)
        bombwall_corridor.connect(before_e_passage, BOMB)
        bombwall_corridor.connect(pushblock_room, back=False)
        pushblock_room.connect(pushblock_room_chest7, back=False)
        pre_center_keyblock.connect(loop_ledge, FEATHER, back=False)
        loop_ledge.connect(before_c_passage, back=False)
        pre_center_keyblock.connect((heart_vire, peahat_area), FOUND(KEY8, 1))
        peahat_area.connect(before_e_passage, back=False)
        before_e_passage.connect(after_e_passage, FEATHER)
        # east
        heart_vire.connect(before_g_passage, FOUND(KEY8, 2))
        before_g_passage.connect(hidden_arrow_room, back=False)
        before_g_passage.connect(after_g_passage, AND(FEATHER, HOOKSHOT))
        hidden_arrow_room.connect(dodongo_area, r.enemy_requirements["HIDING_ZOL"], back=None)
        hidden_arrow_room.connect(dark_east_spark, BOMB)
        # dark
        dark_east_spark.connect(dark_east_zol, FEATHER)
        dark_east_zol.connect(dark_center, FOUND(KEY8, 4))
        peahat_area.connect((dark_center, dark_west), AND(BOW, BOMB, FEATHER), back=AND(BOMB, FEATHER))
        dark_center.connect(dark_west, r.enemy_requirements["SNAKE"], back=AND(r.enemy_requirements["SNAKE"], r.enemy_requirements["PEAHAT"]))
        dark_west.connect(dark_center_torches, FOUND(KEY8, 3))
        for location in (dark_center_torches, dark_center_pre_keyblock):
            location.connect(dark_center, None, back=False)
        dark_west.connect(before_f_stairs, AND(BOMB, FEATHER), back=AND(BOW, BOMB, FEATHER))
        dark_center_torches.connect(dark_center_pre_keyblock, HOOKSHOT)
        dark_center_pre_keyblock.connect(before_d_passage, FOUND(KEY8, 7))
        # miniboss
        before_d_passage.connect(after_d_passage, FEATHER)
        after_d_passage.connect(miniboss_room)
        miniboss_room.connect((miniboss_cubby, entrance), r.miniboss_requirements[world_setup.miniboss_mapping[7]], back=False) # miniboss portal
        miniboss_cubby.connect(rod_ledge, "SWITCH8", back=False)
        rod_ledge.connect(rod_ledge_chest8, back=False)
        # northeast
        dodongo_area.connect(dodongo_area_drop3, r.enemy_requirements["GIBDO"], back=False)
        dodongo_area.connect(pre_lava_ledge, FEATHER)
        pre_lava_ledge.connect((slime_corridor, after_g_passage), back=False)
        pre_lava_ledge.connect(lava_ledge, HOOKSHOT, back=False)
        lava_ledge.connect((lava_ledge_chest9, after_g_passage), back=False)
        after_f_stairs.connect(after_f_stairs_chest10, r.miniboss_requirements["DODONGO"], back=False)
        after_f_stairs.connect(dodongo_area, back=False)
        # northwest
        slime_corridor.connect(before_f_stairs, FOUND(KEY8, 4))
        before_f_stairs.connect((before_f_stairs_chest11, sw_zamboni_area), back=False)
        before_f_stairs.connect(before_f_stairs_drop4, BOW, back=False)
        before_f_stairs.connect(miniboss4_cubby, AND(r.enemy_requirements["VIRE"], AND(r.enemy_requirements["SNAKE"])), back=None)
        before_f_stairs.connect(peahat_area, FEATHER, back=False)
        miniboss4_cubby.connect(ledge_west_boss, HOOKSHOT, back=False)
        ledge_west_boss.connect(ledge_west_boss_chest12, back=False)
        # cueball
        before_b_passage.connect(after_b_passage, AND(FEATHER, MAGIC_ROD), back=MAGIC_ROD)
        after_b_passage.connect(miniboss4_cubby, back=False)
        after_b_passage.connect(miniboss4_room, FOUND(KEY8, 7), back=False)
        miniboss4_room.connect(nw_zamboni_room, AND(FEATHER, r.miniboss_requirements["CUE_BALL"]), back=False)
        nw_zamboni_room.connect(nw_zamboni_room_chest13, back=False)
        # boss
        before_c_passage.connect(after_c_passage, AND(FEATHER, MAGIC_ROD), back=MAGIC_ROD)
        after_c_passage.connect(boss_room, NIGHTMARE_KEY8, back=False)
        boss_room.connect(boss_room_drop5, r.boss_requirements[world_setup.boss_mapping[7]], back=False)
        boss_room.connect(instrument, AND(FEATHER, r.boss_requirements[world_setup.boss_mapping[7]]), back=False)
        # owl statues
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            after_a_passage.connect(after_a_passage_owl1, STONE_BEAK8)
            hidden_arrow_room.connect(hidden_arrow_room_owl2, STONE_BEAK8)
            before_f_stairs.connect(before_f_stairs_owl3, STONE_BEAK8)
        # hard
        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            #south
            zamboni_pit_west.connect(zamboni_pit_east, r.tight_jump, back=False) # diagonal jump to cross zamboni pit from left side
            after_a_passage.connect(before_a_passage, r.damage_boost, back=False) # take some damage but itemless
            pot_pit_room_doorway.connect(pot_pit_room, r.boots_bonk_pit) # bonk off wall or pot to cross 1-tile pit
            pot_pit_room_doorway.connect(miniboss3_room, OR(r.throw_pot, AND(FEATHER, r.shield_bump)), back=False) # use 4 pots to kill 4 ropes, or bump them into pits with shield
            #center
            peahat_area.connect(heart_vire, r.tight_jump) # tight jump around keyblock
            peahat_area.connect((dark_center, dark_west), AND(BOMB, FEATHER), back=False) # pixel perfect bomb placement
            #north
            dodongo_area.connect(dodongo_area_drop3, OR(HOOKSHOT, MAGIC_ROD), back=False) # crack one of the floor tiles and hookshot the gibdos in, or burn the gibdos and make them jump into pit
            before_f_stairs.connect(dark_west, AND(BOMB, FEATHER), back=False) # pixel perfect bomb placement
            before_f_stairs.connect(miniboss4_cubby, r.throw_pot, back=False) # throw 4 of the 5 pots to kill 2 ropes and vire
            before_f_stairs.connect(sw_vire_room_drop1, AND(r.miniboss_requirements["ROLLING_BONES"], r.enemy_requirements["VIRE"]), back=False) # allows bombs to kill vire but only from dropdown in unlit torch room
        # glitched
        if options.logic == 'glitched' or options.logic == 'hell':
            #south
            sw_zamboni_area.connect(spark_pit_room, AND(r.pit_buffer_itemless, r.diagonal_walk), back=False) # pit buffer down across the pit then walk diagonally between pits
            after_e_passage.connect(pot_pit_room, AND(r.hookshot_clip_wall, r.super_jump_feather), back=False) # hookshot the pot to get wall clipped, then you can superjump down then up to get in rope room
            #center
            before_e_passage.connect(peahat_area, r.sideways_block_push, back=False) # sideways block push in peahat room to get past keyblock
            before_e_passage.connect(bombwall_corridor, r.super_jump_feather, back=False)
            for location in (before_e_passage, pre_center_keyblock, loop_ledge, before_c_passage, before_b_passage):
                location.connect(pre_center_zamboni, r.jesus_jump, back=False) # allows jesus jump to any connection near center zamboni
            peahat_area.connect(before_f_stairs, r.jesus_jump, back=False) # use jesus jump in refill room left of peahats to clip bottom wall and push bottom block left, to get a place to super jump
            before_c_passage.connect(loop_ledge, r.super_jump_feather, back=False) # wall clip on stairs, superjump over blocks
            loop_ledge.connect((heart_vire, pre_center_keyblock), r.super_jump_feather, back=False) # wall clip on loop ledge or ledge left of keyblock, and superjump over blocks
            pre_center_keyblock.connect((loop_ledge, heart_vire), r.super_jump_feather, back=False) # push block into lava, get wall clipped on left wall and superjump right to skip keyblock | or superjump by stairs over blocks
            dark_center.connect((dark_center_torches, dark_center_pre_keyblock), r.super_jump_feather, back=False) # wall clip and super jump to either ledge
            dark_center.connect(dark_east_zol, r.hookshot_clip_block, back=False) # hookshot clip off the zols to get through without spending key
            dark_center_torches.connect(before_d_passage, r.bookshot, back=False) # skip keyblock to blaino's passageway
            miniboss_cubby.connect(rod_ledge, r.super_jump_feather, back=False) # superjump to skip over pegs after blaino
            #north
            slime_corridor.connect((before_f_stairs, after_g_passage), r.jesus_jump) # jesus jump through lava to reach northmost staircase or go around key door
            miniboss4_cubby.connect(after_b_passage, r.super_jump_feather) # superjump to get to cueball doorway
            for location in (after_g_passage, slime_corridor):
                location.connect(lava_ledge, AND(r.jesus_jump, r.super_jump_feather), back=False) # jesus jump and buffer into bottom ledge to wall clip / super jump to reach chest
            dodongo_area.connect(after_f_stairs, r.super_jump_feather, back=False) # wall clip and superjump to dodongo ledge
            dodongo_area.connect(after_f_stairs_chest10, AND(r.miniboss_requirements["DODONGO"], r.super_jump_feather), back=False) # wall clip and superjump to dodongo ledge chest after killing dodongo
            before_f_stairs.connect(after_c_passage, r.super_jump_feather, back=False) # superjump off the bottom or right wall to jump over to the boss door
        # hell
        if options.logic == 'hell':
            #south
            entrance.connect((lava_beamos_room, pre_center_zamboni), AND(r.jesus_buffer, r.lava_swim_sword), back=False) # boots bonk around the top left corner at vire, get on top of the wall to bonk to the left, and transition while slashing sword #TODO: look into consistency of swordless
            entrance.connect(lava_beamos_room, r.jesus_jump, back=False) # jesus jump around the key door
            before_a_passage.connect(after_a_passage, OR(r.bracelet_bounce_2d_spikepit, r.boots_bonk_2d_hell), back=False) # bracelet to get damage boost from 2d spikes to get through passage
            after_e_passage.connect(pot_pit_room, OR(r.shaq_jump, AND(r.hookshot_clip_wall, r.hookshot_clip_block, r.hookshot_over_pit)), back=r.zoomerang) # repeatedly hookshot the pot from 1 tile away, once fully wall clipped face down > kill rope > face right > spam hookshot > clip through from lucky rupee drop. back is right-facing zoomerang
            pot_pit_room_doorway.connect(pot_pit_room, r.pit_buffer_itemless, back=r.hookshot_spam_pit) # pit buffer from south smasher doorway to the SE room chest
            pot_pit_room_doorway.connect(miniboss3_room, OR(AND(r.hookshot_spam_pit, r.enemy_requirements["SNAKE"]), AND(r.boots_bonk_pit, r.shield_bump)), back=False) # boots bonk to navigate room, or bump them into pits with shield
            after_e_passage.connect(before_e_passage, r.boots_bonk, back=False) # boots bonking from rope room to below peahats through passage
            zamboni_pit_west.connect(slime_trap_room, r.boots_bonk, back=False) # boots bonk to hop over 1 tile of lava
            #center
            before_f_stairs.connect(peahat_area, AND(r.boots_bonk, r.jesus_buffer), back=False) # from refill room push block into lava and boots bonk over the 1-tile of lava
            #TODO: make connections for starting a jesus buffer assisted by hookshot hookshot to stop drowning in water or lava
            peahat_area.connect(before_f_stairs, AND(r.jesus_buffer, r.lava_swim), back=False) # bonk to set up lava swim on the screen transition
            for location in (before_e_passage, pre_center_keyblock, loop_ledge, before_c_passage, before_b_passage):
                location.connect(pre_center_zamboni, r.jesus_buffer, back=False) # allows jesus buffer to any connection near center zamboni
            before_b_passage.connect(loop_ledge, HOOKSHOT, back=False) # while standing on staircase, hookshot up, then hookshot right on the frame that you splash the lava - pausing on the splash frame to buffer seems easier
            loop_ledge.connect(heart_vire, r.hookshot_clip_block, back=False) # get in block walk-off-ledge and pause buffering, then walk-jump into block. hoookshot clip off vire to get out and skip key requirement
            before_g_passage.connect(after_g_passage, AND(HOOKSHOT, r.damage_boost_special, "TOADSTOOL2"), back=False) # new logic - use toadstool after hurt by goomba, and bouncing off goomba to freeze after gaining height. Hold "A" button during the damage boost to get extra boost
            #dark
            before_f_stairs.connect(dark_west, AND(BOMB, r.jesus_buffer, r.lava_swim), back=False) # pixel perfect bomb placement to open door, return with lava swim
            for location in (dark_west, dark_center):
                location.connect(peahat_area, AND(BOMB, r.jesus_buffer), back=False) # bomb the wall and boots bonk to start jesus buffer
            dark_west.connect(before_f_stairs, AND(BOMB, r.hookshot_wrap, r.jesus_buffer), back=False) # boots bonk then use hookshot when splashing to grab spark's block, will respawn near spark block
            dark_east_zol.connect(dark_east_spark, OR(r.hookshot_spam_pit, r.boots_bonk)) # spam hookshot or simply boots bonk to get over 1 block pit
            dark_center.connect(before_d_passage, AND(r.super_jump_feather, r.shield_bump), back=False) # wall clip then superjump to the spot 2-tiles left of staircase - when rope is in front of link, shield-backflip to staircase
            dark_center_pre_keyblock.connect(before_d_passage, r.zoomerang_shovel, back=False) # right-facing zoomerang to get through keyblock. unreliable without shovel
            #miniboss
            before_d_passage.connect(after_d_passage, r.boots_bonk_2d_hell) # get through 2d section with boots bonks
            dodongo_area.connect(dodongo_area_drop3, AND(FEATHER, SHIELD), back=False) # lock gibdos into pits and crack the tile below them, then use shield to bump them into the pit
            dodongo_area.connect(pre_lava_ledge, r.boots_bonk) # bonk over 1 block of lava, no buffer
            pre_lava_ledge.connect(lava_ledge, r.super_jump_feather) # walk off ledge and pause buffer to get in position
            slime_corridor.connect(before_f_stairs, AND(r.jesus_buffer, r.lava_swim)) # boots bonk and lava swim around small key door near boss
            #northwest
            before_b_passage.connect(after_b_passage, AND(r.boots_bonk_2d_hell, MAGIC_ROD), back=False) # boots bonk in 2d to use magic rod on upper ice blocks
            before_f_stairs.connect(ledge_west_boss, r.super_bump, back=False) # super bump while wall clipped on stairs to tal tal
            miniboss4_room.connect(nw_zamboni_room, AND(r.boots_bonk, r.jesus_buffer, r.miniboss_requirements["CUE_BALL"]), back=False) # use a boots bonk to cross the lava in cueball room
            #boss
            before_c_passage.connect(after_c_passage, AND(r.boots_bonk_2d_hell, MAGIC_ROD), back=False) # boots bonk through 2d ice section
            after_c_passage.connect(before_f_stairs, AND(r.jesus_jump, r.zoomerang), back=False) # jesus jump across lava and then a few dozen consecutive buffers to get lodged lower left corner of rail, the right-facing zoomerang to escape
            boss_room.connect(instrument, AND(r.boots_bonk, r.jesus_buffer, r.boss_requirements[world_setup.boss_mapping[7]]), back=False) # boots bonk in boss room to collect instrument
            # connections that require overworld-only replenishable items such as "TOADSTOOL2" and "MEDICINE2"
            if options.overworld != 'alttp' and options.overworld != 'dungeondive':
                before_a_passage.connect(after_a_passage, r.toadstool_bounce_2d_spikepit, back=False) # toadstool to get damage boost from 2d spikes to get through passage

        self.entrance = entrance
        self.final_room = instrument


class NoDungeon8:
    def __init__(self, options, world_setup, r):

        # locations
        entrance = Location("D8 Entrance", dungeon=8)
        boss_room = Location("D8 Boss Room", dungeon=8)
        boss_room_drop5 = Location(dungeon=8).add(HeartContainer(0x234)) # heart container
        instrument = Location("D8 Instrument Room", dungeon=8).add(Instrument(0x230)) # instrument
        # connections
        entrance.connect(boss_room, back=r.boss_requirements[world_setup.boss_mapping[7]])
        boss_room.connect(boss_room_drop5, r.boss_requirements[world_setup.boss_mapping[7]], back=False)
        boss_room.connect(instrument, AND(FEATHER, r.boss_requirements[world_setup.boss_mapping[7]]), back=False)

        self.entrance = entrance
