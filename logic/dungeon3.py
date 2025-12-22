from .requirements import *
from .location import Location
from locations.all import *


class Dungeon3:
    def __init__(self, options, world_setup, r):

        # locations
        entrance = Location("D3 Entrance", dungeon=3)
        entrance_chest1 = Location(dungeon=3).add(DungeonChest(0x153)) #small key
        after_pot_door = Location("D3 After Pot Door", dungeon=3)
        after_pot_door_chest2 = Location(dungeon=3).add(DungeonChest(0x151)) # small key
        slime_room = Location("D3 Slime Room", dungeon=3)
        slime_room_chest3 = Location(dungeon=3).add(DungeonChest(0x14F)) # slime
        swordstalfos_room = Location("D3 Stalfos Pedestal Room", dungeon=3)
        swordstalfos_room_chest4 = Location(dungeon=3).add(DungeonChest(0x150)) # map
        before_a_stairs = Location("D3 Near 1st Staircase", dungeon=3)
        before_a_stairs_chest5 = Location(dungeon=3).add(DungeonChest(0x14E)) # 200 rupees
        before_a_stairs_chest6 = Location(dungeon=3).add(DungeonChest(0x14C)) # beak
        west_hallway = Location("D3 Long Hallway", dungeon=3)
        west_hallway_clear = Location("D3 Hallway Gel Defeated", dungeon=3).add(KeyLocation("D3_GEL_CLEAR"))
        after_a_stairs = Location("D3 Key Door Crossroads", dungeon=3)
        north_4way = Location("D3 North Key Room", dungeon=3)
        north_4way_drop3 = Location(dungeon=3).add(DroppedKey(0x154)) # small key
        north_4way_owl1 = Location(dungeon=3).add(OwlStatue(0x154)) # hint
        north_4way_switch = Location("D3 North Key Room Switch", dungeon=3).add(KeyLocation("SWITCH3"))
        south_4way = Location("D3 South Key Room", dungeon=3)
        south_4way_drop1 = Location(dungeon=3).add(DroppedKey(0x158)) # small key
        west_4way = Location("D3 West Key Room", dungeon=3)
        west_4way_drop2 = Location(dungeon=3).add(DroppedKey(0x155)) # small key
        before_b_stairs = Location("D3 East Key Room", dungeon=3)
        after_b_stairs = Location("D3 Main Area", dungeon=3)
        after_b_stairs_drop4 = Location(dungeon=3).add(DroppedKey(0x14D)) # small key
        after_b_stairs_owl2 = Location(dungeon=3).add(OwlStatue(0x147)) # hint
        miniboss_room = Location("D3 Miniboss Room", dungeon=3)
        after_miniboss_room = Location("D3 Miniboss Reward Room", dungeon=3)
        after_miniboss_room_chest10 = Location(dungeon=3).add(DungeonChest(0x146)) # pegasus boots
        two_pairodd_room = Location("D3 Two Zol, Two Pairodd Room", dungeon=3)
        two_pairodd_room_drop5 = Location(dungeon=3).add(DroppedKey(0x148)) # small key
        two_zol_stalfos_room = Location("D3 Two Zol, Stalfos Room", dungeon=3)
        two_zol_stalfos_room_clear = Location("D3 Two Zols & Stalfos Defeated", dungeon=3).add(KeyLocation("D3_ZOLS_CLEAR")).add(KeyLocation("D3_STALFOS_CLEAR"))
        fenced_walkway = Location("D3 Fenced Walkway", dungeon=3)
        fenced_walkway_owl3 = Location("Flying Bomb Owl", dungeon=3).add(OwlStatue(0x140)) # hint
        fenced_walkway_chest7 = Location(dungeon=3).add(DungeonChest(0x144)) # 50 rupees
        north_bombwall = Location("North Bombable Wall Open", dungeon=3).add(KeyLocation("D3_BOMBWALL"))
        timer_bombite_room = Location("D3 Timer Bombite Room", dungeon=3)
        three_zol_stalfos_room = Location("D3 Three Zol, Stalfos Room", dungeon=3)
        three_zol_stalfos_room_chest8 = Location(dungeon=3).add(DungeonChest(0x142)) # compass
        bouncing_bombite_room = Location("D3 Bouncing Bombite Room", dungeon=3)
        bouncing_bombite_room_drop_6 = Location(dungeon=3).add(DroppedKey(0x141)) # small key
        big_pit_room = Location("D3 Bombable Wall Room", dungeon=3)
        ledge_pre_pit = Location("D3 East Ledge Before Pit", dungeon=3)
        ledge_post_pit = Location("D3 East Ledge After Pit", dungeon=3)
        ledge_post_pit_chest_9 = Location(dungeon=3).add(DungeonChest(0x147)) # nightmare key
        towards_boss1 = Location("D3 Boss Path 1", dungeon=3)
        towards_boss2 = Location("D3 Boss Path 2", dungeon=3)
        towards_boss3 = Location("D3 Boss Path 3", dungeon=3)
        before_c_passage = Location("D3 Boss Path 4", dungeon=3)
        after_c_passage = Location("D3 Three Pairodd Room", dungeon=3)
        pre_boss_room = Location("D3 Room Before Boss", dungeon=3)
        pre_boss_room_drop7 = Location(dungeon=3).add(DroppedKey(0x15B)) # small key
        boss_room = Location("D3 Boss Room", dungeon=3)
        boss_room_drop8 = Location(dungeon=3).add(HeartContainer(0x15A)) # heart container
        instrument = Location("D3 Instrument Room", dungeon=3).add(Instrument(0x159)) # sea lily's bell

        # owl statues
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            north_4way.connect(north_4way_owl1, STONE_BEAK3, back=False)
            after_b_stairs.connect(after_b_stairs_owl2, STONE_BEAK3, back=False)
            fenced_walkway.connect(fenced_walkway_owl3, STONE_BEAK3, back=False)
            
        # connections
        # entrance
        entrance.connect(entrance_chest1, PEGASUS_BOOTS, back=False)
        entrance.connect(after_pot_door, POWER_BRACELET, back=None)
        after_pot_door.connect(after_pot_door_chest2, AND(r.enemy_requirements["GEL"], r.enemy_requirements["MOBLIN_SWORD"], r.enemy_requirements["BOUNCING_BOMBITE"]), back=False)
        after_pot_door.connect(west_hallway, PEGASUS_BOOTS)
        slime_room.connect((after_pot_door, swordstalfos_room, before_a_stairs), r.enemy_requirements["HIDING_ZOL"], back=None)
        slime_room.connect(slime_room_chest3, back=False)
        west_hallway.connect(west_hallway_clear, r.enemy_requirements["GEL"], back=False)
        west_hallway.connect(before_a_stairs, back=False)
        before_a_stairs.connect(before_a_stairs_chest5, AND("D3_GEL_CLEAR", r.enemy_requirements["STALFOS_EVASIVE"]), back=False)
        swordstalfos_room.connect(swordstalfos_room_chest4, "SWITCH3", back=False)
        before_a_stairs.connect(before_a_stairs_chest6, "SWITCH3", back=False)
        before_a_stairs.connect(after_a_stairs)
        # 4 way
        after_a_stairs.connect((north_4way, south_4way, west_4way), FOUND(KEY3, 8), back=False)
        north_4way.connect(north_4way_drop3, AND(r.enemy_requirements["STALFOS_AGGRESSIVE"], r.enemy_requirements["MOBLIN"]), back=False)
        north_4way.connect(north_4way_switch, r.hit_switch, back=False)
        south_4way.connect(south_4way_drop1, AND(r.enemy_requirements["HIDING_ZOL"], r.enemy_requirements["MOBLIN"], OR(r.enemy_requirements["PAIRODD"], BOOMERANG)), back=False)
        west_4way.connect(west_4way_drop2, AND(r.enemy_requirements["HIDING_ZOL"], OR(r.enemy_requirements["PAIRODD"], BOOMERANG)), back=False)
        after_a_stairs.connect(before_b_stairs, FOUND(KEY3, 4))
        # main area
        before_b_stairs.connect(after_b_stairs)
        after_b_stairs.connect(after_b_stairs_drop4, r.enemy_requirements["HIDING_ZOL"], back=False)
        after_b_stairs.connect(two_pairodd_room, AND(r.enemy_requirements["ZOL"], r.enemy_requirements["GEL"]), back=None) #NOTE: requires 11 arrows/powder if forced to go through slime_room if 1-kill per use
        after_b_stairs.connect(miniboss_room, AND(r.enemy_requirements["ZOL"], r.enemy_requirements["GEL"]), back=None) #NOTE: requires 11 arrows/powder if forced to go through slime_room if 1-kill per use
        miniboss_room.connect(entrance, r.miniboss_requirements[world_setup.miniboss_mapping[2]], back=False) # miniboss portal
        miniboss_room.connect(after_miniboss_room, r.miniboss_requirements[world_setup.miniboss_mapping[2]], back=None)
        after_miniboss_room.connect((after_miniboss_room_chest10, after_b_stairs), back=False)
        # main west
        two_pairodd_room.connect(two_pairodd_room_drop5, AND(r.enemy_requirements["HIDING_ZOL"], r.enemy_requirements["PAIRODD"]), back=False)
        two_pairodd_room.connect(two_zol_stalfos_room, back=False)
        two_zol_stalfos_room.connect(two_zol_stalfos_room_clear, AND(r.enemy_requirements["ZOL"], r.enemy_requirements["STALFOS_AGGRESSIVE"]), back=False) #NOTE: requires 7 arrows to clear room, exceeds 10 from entrance with some itemsets
        two_zol_stalfos_room.connect(fenced_walkway, back=False)
        fenced_walkway.connect(fenced_walkway_chest7, AND("D3_ZOLS_CLEAR", "D3_STALFOS_CLEAR"), back=False)
        fenced_walkway.connect(north_bombwall, BOMB, back=False)
        # main north
        timer_bombite_room.connect((after_b_stairs, three_zol_stalfos_room), AND(r.enemy_requirements["HIDING_ZOL"], r.enemy_requirements["TIMER_BOMBITE"]), back=None)
        three_zol_stalfos_room.connect(three_zol_stalfos_room_chest8, back=False)
        three_zol_stalfos_room.connect(north_bombwall, BOMB, back=False)
        three_zol_stalfos_room.connect(bouncing_bombite_room, "D3_BOMBWALL")
        bouncing_bombite_room.connect(bouncing_bombite_room_drop_6, r.enemy_requirements["BOUNCING_BOMBITE"], back=False)
        # main east
        after_b_stairs.connect(big_pit_room, BOMB)
        big_pit_room.connect(ledge_pre_pit, AND(FEATHER, PEGASUS_BOOTS))
        ledge_pre_pit.connect((after_b_stairs, big_pit_room), back=False)
        ledge_pre_pit.connect(ledge_post_pit, OR(HOOKSHOT, FEATHER), back=False) #NOTE: should two-block feather jump be hard?
        ledge_post_pit.connect((after_b_stairs, ledge_post_pit_chest_9), back=False)
        # boss
        after_b_stairs.connect(towards_boss1, FOUND(KEY3, 5))
        towards_boss1.connect(towards_boss2, FOUND(KEY3, 6))
        towards_boss2.connect(towards_boss3, FOUND(KEY3, 7))
        towards_boss3.connect(before_c_passage, FOUND(KEY3, 8))
        before_c_passage.connect(after_c_passage, AND(FEATHER, PEGASUS_BOOTS))
        after_c_passage.connect(pre_boss_room, r.enemy_requirements["PAIRODD"], back=False)
        pre_boss_room.connect(pre_boss_room_drop7, r.enemy_requirements["KEESE"], back=False)
        pre_boss_room.connect(boss_room, NIGHTMARE_KEY3, back=False)
        boss_room.connect((boss_room_drop8, instrument), r.boss_requirements[world_setup.boss_mapping[2]], back=False)

        if options.dungeon_keys == '':
            # Without keysanity we need to fix the keylogic here, else we can never generate proper placement.
            after_a_stairs.connect(west_4way, FOUND(KEY3, 1), back=False)
            west_4way_drop2.items[0].forced_item = KEY3
            after_a_stairs.connect(south_4way, FOUND(KEY3, 1), back=False)
            south_4way_drop1.items[0].forced_item = KEY3

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            entrance.connect(entrance_chest1, r.hookshot_over_pit, back=False) # hookshot the chest to get past vacuum trap
            north_4way.connect(north_4way_switch, r.throw_pot, back=False) # use pots to hit switch
            south_4way.connect(south_4way_drop1, r.throw_pot, back=False) # use pots to kill enemies
            north_4way.connect(north_4way_drop3, r.throw_pot, back=False) # use pots to kill the enemies
            fenced_walkway.connect(bouncing_bombite_room_drop_6, BOOMERANG, back=False) # 3 bombite room from the walkway, grab item with boomerang
            fenced_walkway.connect(two_zol_stalfos_room_clear, OR(BOOMERANG, BOMB, BOW), back=False) #NOTE: requires 7 arrows to clear room, exceeds 10 from entrance with some itemsets
            fenced_walkway.connect(north_bombwall, OR(AND(FEATHER, OR(SWORD, MAGIC_POWDER)), BOW, MAGIC_ROD, BOOMERANG), back=False) # feather and close range weapon to trigger bouncing bombite to blow up the wall

        if options.logic == 'glitched' or options.logic == 'hell':
            before_a_stairs.connect(west_hallway, OR(AND("SWITCH3", r.super_jump_feather), r.hookshot_clip_block), back=False) # hookshot clip through the pushblock using zols and their rupees, or hit the switch and superjump to pegs
            west_hallway.connect((before_a_stairs, before_a_stairs_chest6), OR(r.super_jump_feather, r.shaq_jump), back=False) # shaq jump off pushblock to land on pegs and grab the chest, or wall clip in hallway and super jump a few times to get on pegs #NOTE: shouldn't connect tricks to items
            swordstalfos_room.connect(swordstalfos_room_chest4, r.super_jump_feather, back=False) # use superjump to get over the bottom left block
            big_pit_room.connect(ledge_pre_pit, AND(r.corner_walk, r.super_jump_feather), back=False) # superjump to right side 3 of the big pit
            towards_boss1.connect(miniboss_room, r.super_jump_feather, back=False) # superjump out between keyblock 1 & 2
            towards_boss2.connect(after_miniboss_room, r.super_jump_feather, back=False) # superjump out between keyblock 2 & 3 - key requirement for wall clip
            towards_boss3.connect((after_miniboss_room, after_b_stairs), r.super_jump_feather, back=False) # superjump out between keyblock 3 & 4
        
        if options.logic == 'hell':
            entrance.connect(entrance_chest1, SWORD, back=False) # hold right for ~2:00 and kill vacuum with sword
            west_hallway.connect((before_a_stairs, before_a_stairs_chest6), r.boots_superhop, back=False) # use boots superhop off top wall or left wall to get on raised blocks
            swordstalfos_room.connect(swordstalfos_room_chest4, OR(r.boots_superhop, r.hookshot_clip_block), back=False) # boots superhop to get over the bottom left block, OR spam hookshot while a keese passes by to clip through pushblock
            before_a_stairs.connect((west_hallway, before_a_stairs_chest6), OR(AND(r.boots_superhop, r.shield_bump), r.super_bump), back=False) # setup shaq jump or boots superhop above staircase and shield bump on zol to hop over pushblock
            west_4way.connect(west_4way_drop2, r.shield_bump, back=False) # knock everything into the pit including the teleporting owls
            south_4way.connect(south_4way_drop1, r.shield_bump, back=False) # knock everything into the pit including the teleporting owls
            after_b_stairs.connect(fenced_walkway, r.super_bump, back=False) # super bump off zols to go past pushblock to the fenced walkway
            fenced_walkway.connect(north_bombwall, OR(r.sword_beam, AND(r.boots_bonk, OR(SWORD, MAGIC_POWDER))), back=False) # set off bouncing bombite to blow up the bombwall from the fenced walkway
            after_b_stairs.connect(ledge_pre_pit, AND(r.super_jump_feather, r.shield_bump), back=False) # superjump into jumping stalfos and shield bump to right ledge
            big_pit_room.connect(ledge_pre_pit, r.pit_buffer_boots) # boots bonk across the pits with pit buffering and then hookshot or shield bump to the chest
            after_b_stairs.connect(towards_boss3, r.super_bump, back=False) # super bump off stalfos to get in between boss key block 3 and 4
            before_c_passage.connect(after_c_passage, OR(r.toadstool_bounce_2d_spikepit, r.bracelet_bounce_2d_spikepit, r.boots_bonk_2d_spikepit), back=OR(r.toadstool_bounce_2d_spikepit, r.bracelet_bounce_2d_spikepit, r.boots_bonk_2d_hell)) # bracelet or toadstool to bounce off spikes (no medicine) or boots bonk with medicine invulnerability. holding the "A" button while airborne in sidescroller makes you lighter


        self.entrance = entrance
        self.final_room = instrument


class NoDungeon3:
    def __init__(self, options, world_setup, r):
        entrance = Location("D3 Entrance", dungeon=3)
        Location(dungeon=3).add(HeartContainer(0x15A), Instrument(0x159)).connect(entrance, AND(POWER_BRACELET, r.boss_requirements[
            world_setup.boss_mapping[2]]))

        self.entrance = entrance
