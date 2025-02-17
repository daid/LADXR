from .requirements import *
from .location import Location
from locations.all import *


class Dungeon5:
    def __init__(self, options, world_setup, r):
        entrance = Location("D5 Entrance", dungeon=5)
        start_hookshot_chest = Location(dungeon=5).add(DungeonChest(0x1A0)).connect(entrance, HOOKSHOT, id="fu")
        compass = Location(dungeon=5).add(DungeonChest(0x19E)).connect(entrance, AND(r.enemy_requirements["KEESE"], r.enemy_requirements["IRON_MASK"]), id="fv")
        fourth_stalfos_area = Location(dungeon=5).add(DroppedKey(0x181)).connect(compass, AND(SWORD, FEATHER), id="fw") # crystal rocks can only be broken by sword

        area2 = Location("D5 After First Key", dungeon=5).connect(entrance, KEY5, id="fx")
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=5).add(OwlStatue(0x19A)).connect(area2, STONE_BEAK5, id="fy")
        area2_past_iron_masks = Location(dungeon=5).add(DungeonChest(0x19B)).connect(area2, r.enemy_requirements["IRON_MASK"], id="fz")  # map chest
        blade_trap_chest = Location(dungeon=5).add(DungeonChest(0x197)).connect(area2_past_iron_masks, HOOKSHOT, id="g0")  # key chest on the left
        pre_gohma = Location("D5 Before Miniboss", dungeon=5).connect(area2_past_iron_masks, HOOKSHOT, id="g1") # area top left before keyblock gohma
        gohma = Location("D5 Miniboss Room", dungeon=5).connect(pre_gohma, AND(KEY5, FOUND(KEY5,2)), id="g2")
        post_gohma = Location("D5 After Miniboss", dungeon=5).connect(gohma, r.miniboss_requirements[world_setup.miniboss_mapping[4]], id="g3") # staircase after gohma
        staircase_before_boss = Location("D5 Before Boss Keyblock", dungeon=5).connect(post_gohma, AND(HOOKSHOT, FEATHER), id="g4") # bottom right section pits room before boss door. Path via gohma
        after_keyblock_boss = Location("D5 After Boss Keyblock", dungeon=5).connect(staircase_before_boss, AND(KEY5, FOUND(KEY5, 3)), id="g5") # top right section pits room before boss door
        after_stalfos = Location(dungeon=5).add(DungeonChest(0x196)).connect(area2, AND(r.enemy_requirements["STALFOS_AGGRESSIVE"], r.enemy_requirements["STALFOS_EVASIVE"], r.enemy_requirements["MASTER_STALFOS"]), id="g7") # Need to defeat master stalfos once for this empty chest; l2 sword beams kill but obscure
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            butterfly_owl = Location(dungeon=5).add(OwlStatue(0x18A)).connect(after_stalfos, AND(FEATHER, STONE_BEAK5), id="g7")
        else:
            butterfly_owl = None
        after_stalfos.connect(staircase_before_boss, AND(FEATHER, r.enemy_requirements["STAR"]), one_way=True, id="g8") # pathway from stalfos to staircase: past butterfly room and push the block
        north_of_crossroads = Location("D5 Crossroads North", dungeon=5).connect(after_stalfos, FEATHER, id="g9")
        first_bridge_chest = Location(dungeon=5).add(DungeonChest(0x18E)).connect(north_of_crossroads, OR(HOOKSHOT, AND(FEATHER, PEGASUS_BOOTS)), id="ga") # south of bridge
        north_bridge_chest = Location(dungeon=5).add(DungeonChest(0x188)).connect(north_of_crossroads, HOOKSHOT, id="gb") # north bridge chest 50 rupees
        east_bridge_chest = Location(dungeon=5).add(DungeonChest(0x18F)).connect(north_of_crossroads, HOOKSHOT, id="gc") # east bridge chest small key
        third_arena = Location("D5 Master Stalfos 3", dungeon=5).connect(north_of_crossroads, AND(r.enemy_requirements["HIDING_ZOL"], r.enemy_requirements["MASTER_STALFOS"]), id="gd") # can beat 3rd m.stalfos
        stone_tablet = Location(dungeon=5).add(DungeonChest(0x183)).connect(north_of_crossroads, AND(POWER_BRACELET, AND(r.enemy_requirements["HIDING_ZOL"], r.enemy_requirements["STALFOS_AGGRESSIVE"], r.enemy_requirements["STALFOS_EVASIVE"])), id="ge")  # stone tablet
        boss_key = Location(dungeon=5).add(DungeonChest(0x186)).connect(after_stalfos, AND(FLIPPERS, HOOKSHOT), id="gf")  # nightmare key
        before_boss = Location("D5 Before Boss", dungeon=5).connect(after_keyblock_boss, HOOKSHOT, id="gg") 
        boss_room = Location("D5 Boss Room", dungeon=5).connect(before_boss, NIGHTMARE_KEY5, id="gh")
        boss = Location(dungeon=5).add(HeartContainer(0x185), Instrument(0x182)).connect(boss_room, r.boss_requirements[world_setup.boss_mapping[4]], id="gi")

        # When we can reach the stone tablet chest, we can also reach the final location of master stalfos
        m_stalfos_drop = Location(dungeon=5).add(HookshotDrop()).connect(third_arena, AND(FEATHER, SWORD, BOMB), id="gj") # can reach fourth arena from entrance with feather and sword

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            blade_trap_chest.connect(area2, AND(FEATHER, r.attack_hookshot_powder), id="gk") # jump past the blade traps
            boss_key.connect(after_stalfos, AND(FLIPPERS, r.boots_jump), id="gl") # boots jump across
            after_stalfos.connect(after_keyblock_boss, AND(FEATHER, r.enemy_requirements["STAR"]), id="gm") # circumvent stalfos by going past gohma and backwards from boss door
            if butterfly_owl:
                butterfly_owl.connect(after_stalfos, AND(r.boots_bonk, STONE_BEAK5), id="gn") # boots charge + bonk to cross 2d bridge
            after_stalfos.connect(staircase_before_boss, AND(r.boots_bonk, r.enemy_requirements["STAR"]), one_way=True, id="go") # pathway from stalfos to staircase: boots charge + bonk to cross bridge, past butterfly room and push the block
            staircase_before_boss.connect(post_gohma, AND(r.boots_bonk, HOOKSHOT), id="gp") # boots bonk in 2d section to skip feather
            north_of_crossroads.connect(after_stalfos, r.hookshot_over_pit, id="gq") # hookshot to the right block to cross pits
            first_bridge_chest.connect(north_of_crossroads, AND(r.wall_clip, r.tight_jump), id="gr") # tight jump from bottom wall clipped to make it over the pits
            after_keyblock_boss.connect(after_stalfos, AND(FEATHER, r.enemy_requirements["STAR"]), id="gs") # jump from bottom left to top right, skipping the keyblock 
            before_boss.connect(after_stalfos, AND(r.boots_jump, r.enemy_requirements["STAR"]), id="gt") # cross pits room from bottom left to top left with boots jump
            
        if options.logic == 'glitched' or options.logic == 'hell':
            start_hookshot_chest.connect(entrance, r.pit_buffer, id="gu") # 1 pit buffer to clip bottom wall and jump across the pits
            post_gohma.connect(pre_gohma, r.hookshot_clip_block, id="gv") # glitch through the blocks/pots with hookshot.
            north_bridge_chest.connect(north_of_crossroads, r.pit_buffer, id="gw") # 1 pit buffer to clip bottom wall and jump across the pits
            east_bridge_chest.connect(first_bridge_chest, r.pit_buffer, id="gx") # 1 pit buffer to clip bottom wall and jump across the pits
            #after_stalfos.connect(staircase_before_boss, AND(r.text_clip, r.super_jump), id="gy") # use the keyblock to get a wall clip in right wall to perform a superjump over the pushable block
            after_stalfos.connect(staircase_before_boss, AND(r.enemy_requirements["STAR"], r.super_jump_boots), id="gz") # charge a boots dash in bottom right corner to the right, jump before hitting the wall and use weapon to the left side before hitting the wall
         
        if  options.logic == 'hell':
            start_hookshot_chest.connect(entrance, r.pit_buffer_boots, id="h0") # use pit buffer to clip into the bottom wall and boots bonk off the wall again
            fourth_stalfos_area.connect(compass, AND(r.boots_bonk_2d_hell, SWORD), id="h1") # do an incredibly hard boots bonk setup to get across the hanging platforms in the 2d section
            blade_trap_chest.connect(area2, AND(r.pit_buffer_boots, r.attack_hookshot_powder), id="h2") # boots bonk + pit buffer past the blade traps
            pre_gohma.connect(area2, AND(r.boots_jump, r.pit_buffer, r.attack_hookshot_powder), id="h3") # use boots jump in room with 2 zols + flying arrows to pit buffer above pot, then jump across.
            post_gohma.connect(pre_gohma, AND(r.sideways_block_push, POWER_BRACELET), id="h4") # Sideways block push + pick up pots to reach post_gohma
            staircase_before_boss.connect(post_gohma, r.boots_jump, id="h5") # to pass 2d section, tight jump on left screen: hug left wall on little platform, then dash right off platform and jump while in midair to bonk against right wall
            after_stalfos.connect(staircase_before_boss, AND(r.enemy_requirements["STAR"], r.super_jump_sword), id="h6") # unclipped superjump in bottom right corner of staircase before boss room, jumping left over the pushable block. reverse is push block
            after_stalfos.connect(staircase_before_boss, AND(r.enemy_requirements["STAR"], r.zoomerang), id="h7") # use zoomerang dashing left to get an unclipped boots superjump off the right wall over the block. reverse is push block
            after_stalfos.connect(area2, SWORD, id="h8") # knock master stalfos down 255 times (about 23 minutes)
            north_bridge_chest.connect(north_of_crossroads, r.boots_bonk_pit, id="h9") # boots bonk across the pits with pit buffering
            first_bridge_chest.connect(north_of_crossroads, r.boots_bonk_pit, id="ha") # get to first chest via the north chest with pit buffering
            east_bridge_chest.connect(first_bridge_chest, r.boots_bonk_pit, id="hb") # boots bonk across the pits with pit buffering
            third_arena.connect(north_of_crossroads, SWORD, id="hc") # can beat 3rd m.stalfos with 255 sword spins
            m_stalfos_drop.connect(third_arena, AND(FEATHER, SWORD), id="hd") # beat master stalfos by knocking it down 255 times x 4 (takes about 1.5h total)
            m_stalfos_drop.connect(third_arena, AND(r.boots_bonk_2d_hell, SWORD), id="he") # can reach fourth arena from entrance with pegasus boots and sword
            boss_key.connect(after_stalfos, AND(r.pit_buffer_itemless, FLIPPERS), id="hf") # pit buffer across
            if butterfly_owl:
                after_keyblock_boss.connect(butterfly_owl, AND(r.pit_buffer_itemless, STONE_BEAK5), one_way=True, id="hg") # pit buffer from top right to bottom in right pits room
            before_boss.connect(after_stalfos, AND(r.enemy_requirements["STAR"], r.super_jump_sword), id="hh") # cross pits room from bottom left to top left by unclipped superjump on bottom wall on top of side wall, then jump across            

        self.entrance = entrance
        self.final_room = boss


class NoDungeon5:
    def __init__(self, options, world_setup, r):
        entrance = Location("D5 Entrance", dungeon=5)
        Location(dungeon=5).add(HeartContainer(0x185), Instrument(0x182)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[4]])

        self.entrance = entrance
