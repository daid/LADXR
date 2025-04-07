from .requirements import *
from .location import Location
from locations.all import *

class Dungeon2:
    def __init__(self, options, world_setup, r):

        # locations
        entrance = Location("D2 Entrance", dungeon=2)
        entrance_chest1 = Location(dungeon=2).add(DungeonChest(0x136)) # 50 rupees
        blade_room = Location("D2 West of Torches", dungeon=2)
        pitbeetle_room = Location("D2 Hardhat Beetle Room", dungeon=2)
        pitbeetle_room_chest2 = Location(dungeon=2).add(DungeonChest(0x12E)) # beak
        stalfos_room = Location("D2 East of Torches", dungeon=2)
        stalfos_room_drop1 = Location(dungeon=2).add(DroppedKey(0x132)) # small key
        mimic_room = Location("D2 Mimic Room", dungeon=2)
        mimic_room_chest3 = Location(dungeon=2).add(DungeonChest(0x137)) # compass
        statue_switch_room = Location("D2 1st Switch Room", dungeon=2)
        statue_switch_room_drop2 = Location(dungeon=2).add(DroppedKey(0x134)) # small key
        statue_switch_room_owl1 = Location(dungeon=2).add(OwlStatue(0x133)) # hint
        locked_switch_room = Location("D2 Locked Switch Room", dungeon=2)
        locked_switch_room_chest4 = Location(dungeon=2).add(DungeonChest(0x138)) # small key
        pit_peg_room = Location("D2 Pits & Pegs Room", dungeon=2)
        pit_peg_room_chest5 = Location(dungeon=2).add(DungeonChest(0x139)) # small key
        mimic_beetle_room = Location("D2 Mimic & Beetle Area", dungeon=2)
        pushblock_room = Location("D2 Pushblock Room", dungeon=2)
        pushblock_room_owl2 = Location(dungeon=2).add(OwlStatue(0x12F)) # hint
        before_a_passage = Location("D2 Pushblock Room Passage Spawn", dungeon=2)
        after_a_passage = Location("D2 Before Miniboss", dungeon=2)
        miniboss_room = Location("D2 Miniboss Room", dungeon=2)
        after_miniboss = Location("D2 After Miniboss", dungeon=2)
        between_pits = Location("D2 After Miniboss Between Pits", dungeon=2)
        between_pits_owl3 = Location(dungeon=2).add(OwlStatue(0x129)) # hint
        before_b_passage = Location("D2 Blocked Staircase", dungeon=2)
        vacuum_room = Location("D2 Vacuum Mouth Area", dungeon=2)
        vacuum_room_chest6 = Location(dungeon=2).add(DungeonChest(0x126)) # map
        vacuum_room_chest7 = Location(dungeon=2).add(DungeonChest(0x121)) # 20 rupees
        boo_room = Location("D2 Boo Buddies Room", dungeon=2)
        boo_room_chest8 = Location(dungeon=2).add(DungeonChest(0x120)) # bracelet
        final_switch_west = Location("D2 Left of North Switch", dungeon=2)
        final_switch_east = Location("D2 Right of North Switch", dungeon=2)
        final_switch_east_chest9 = Location(dungeon=2).add(DungeonChest(0x122)) # small key
        after_b_passage = Location("D2 Enemy Order Room", dungeon=2)
        after_b_passage_chest10 = Location(dungeon=2).add(DungeonChest(0x127)) # nightmare key
        pot_pol_room_doorway = Location("D2 20 Pots Room Doorway", dungeon=2)
        pot_pol_room = Location("D2 20 Pots Room", dungeon=2)
        before_c_passage = Location("D2 Boss Passageway Spawn", dungeon=2)
        pre_boss_room = Location("D2 Room Before Boss", dungeon=2)
        pre_boss = Location("D2 Outside Boss Door", dungeon=2)
        boss_room = Location("D2 Boss Room", dungeon=2)
        boss_room_drop3 = Location(dungeon=2).add(HeartContainer(0x12B)) # heart container
        instrument = Location("D2 Instrument Room", dungeon=2).add(Instrument(0x12a)) # conch horn
        
        # owl statues
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            statue_switch_room.connect(statue_switch_room_owl1, STONE_BEAK2, back=False)
            pushblock_room.connect(pushblock_room_owl2, STONE_BEAK2, back=False)
            between_pits.connect(between_pits_owl3, STONE_BEAK2, back=False)

        # connections
        # entrance
        entrance.connect(entrance_chest1, POWER_BRACELET, back=False)
        entrance.connect(blade_room, FOUND(KEY2, 5), back=False)
        blade_room.connect(pitbeetle_room, r.enemy_requirements["KEESE"], back=False)
        pitbeetle_room.connect(pitbeetle_room_chest2, OR(FEATHER, HOOKSHOT), back=False)
        entrance.connect(stalfos_room, r.fire, back=None)
        stalfos_room.connect(stalfos_room_drop1, AND(r.enemy_requirements["STALFOS_EVASIVE"], r.enemy_requirements["STALFOS_AGGRESSIVE"]), back=False)
        stalfos_room.connect(mimic_room, FOUND(KEY2, 5), back=False)
        stalfos_room.connect(statue_switch_room, back=r.hit_switch) #NOTE: r.hit_switch would have to be dropped here if a skip is found to get from mimic_beetle_room to statue_switch_room
        mimic_room.connect(mimic_room_chest3, r.enemy_requirements["MASKED_MIMIC_GORIYA"], back=False)
        locked_switch_room.connect((statue_switch_room, locked_switch_room_chest4), r.hit_switch)
        locked_switch_room.connect(pit_peg_room, r.hit_switch, back=None) #NOTE: r.hit_switch would have to be dropped here if a skip is found to get from statue_switch_room to locked_switch_room
        pit_peg_room.connect(mimic_beetle_room, FEATHER)
        pit_peg_room_chest5.connect((mimic_beetle_room, pit_peg_room), False, back=FEATHER)
        mimic_beetle_room.connect(statue_switch_room_drop2, AND(r.enemy_requirements["MASKED_MIMIC_GORIYA"], FEATHER, r.hit_switch), back=False)
        mimic_beetle_room.connect(pushblock_room, FOUND(KEY2, 3))
        pushblock_room.connect(before_a_passage)
        # main
        before_a_passage.connect(after_a_passage, FEATHER)
        after_a_passage.connect(miniboss_room, back=False)
        miniboss_room.connect(entrance, r.miniboss_requirements[world_setup.miniboss_mapping[1]], back=False) # miniboss portal
        miniboss_room.connect(after_miniboss, r.miniboss_requirements[world_setup.miniboss_mapping[1]], back=None)
        between_pits.connect((after_miniboss, vacuum_room), FEATHER)
        before_b_passage.connect((after_miniboss, between_pits), POWER_BRACELET)
        before_b_passage.connect(after_b_passage, FEATHER)
        vacuum_room.connect((vacuum_room_chest6, vacuum_room_chest7), back=False)
        vacuum_room.connect(entrance, FEATHER, back=False) # jump over pits and warp let vacuum warp you to entrance
        vacuum_room.connect(boo_room, FOUND(KEY2, 5), back=False)
        boo_room.connect(boo_room_chest8, OR(r.fire, r.enemy_requirements["BOO_BUDDY"]), back=False)
        vacuum_room.connect(final_switch_west, POWER_BRACELET)
        final_switch_west.connect(final_switch_east, r.hit_switch)
        final_switch_east.connect(final_switch_east_chest9, back=False)
        final_switch_east.connect(after_b_passage, r.hit_switch, back=False)
        after_b_passage.connect(after_b_passage_chest10, AND(r.enemy_requirements["KEESE"], r.enemy_requirements["MOBLIN"], OR(r.enemy_requirements["POLS_VOICE"], POWER_BRACELET)), back=False)
        after_b_passage.connect((vacuum_room, final_switch_west, final_switch_east), AND(r.hit_switch, FEATHER, POWER_BRACELET), back=False)

        # boss
        after_b_passage.connect(pot_pol_room_doorway, FOUND(KEY2, 5))
        pot_pol_room_doorway.connect(pot_pol_room, POWER_BRACELET)
        pot_pol_room.connect(before_c_passage, AND(OR(POWER_BRACELET, r.enemy_requirements["POLS_VOICE"]), r.enemy_requirements["ZOL"]), back=None) #TODO: REMOVE, it's now in casual logic. Normal logic will be OR(enemy reqs, bracelet)
        before_c_passage.connect(pre_boss_room, POWER_BRACELET, back=None)
        pre_boss_room.connect(pre_boss, FEATHER, back=False)
        pre_boss.connect(boss_room, NIGHTMARE_KEY2, back=False)
        boss_room.connect((boss_room_drop3, instrument), r.boss_requirements[world_setup.boss_mapping[1]], back=False)

        
        #TODO: if options.logic == "casual":
            #TODO: pot_pol_room.connect(before_c_passage, AND(OR(POWER_BRACELET, r.enemy_requirements["POLS_VOICE"]), r.enemy_requirements["ZOL"]), back=None) # intended to kill pols with pots since in vanilla there's no other way
        if options.logic != "casual": #TODO: change to else
            statue_switch_room.connect(statue_switch_room_drop2, r.rear_attack, back=False) # defeat mimics from where key drops
            #TODO: pot_pol_room.connect(before_c_passage, OR(POWER_BRACELET, AND(r.enemy_requirements["POLS_VOICE"], r.enemy_requirements["ZOL"])), back=None) # clear while room with pots

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            #TODO: before_b_passage.connect(vacuum_room, AND(POWER_BRACELET, r.corner_walk), back=False) # lift pot and corner walk over pit [stair shuffle prep]
            #TODO: final_switch_west.connect(final_switch_east, r.tight_jump) # jump around the single peg blocking the switch [stair shuffle prep]
            after_b_passage.connect((final_switch_west, final_switch_east), AND(r.hit_switch, r.tight_jump), back=False) # hit 4-keese switch, then jump to south hallway, and tight jump around 4 pots to get to the next switch, hit is and go left or right
            #TODO: after_b_passage.connect(vacuum_room, AND(BOOMERANG, POWER_BRACELET)) # diagonal boomerang throw from south wall to hit north wall switch [stair shuffle prep]
            #TODO: after_b_passage.connect((final_switch_west, final_switch_east), AND(BOOMERANG, OR(HOOKSHOT, FEATHER)), back=False) # diagonal boomerang throw from south wall to hit switch, then cross to chest [stair shuffle prep]

        if options.logic == 'glitched' or options.logic == 'hell':
            boo_room.connect(boo_room_chest8, SWORD, back=False) # use sword to spawn ghosts on other side of the room so they run away (logically irrelevant because player will have fire)
            after_miniboss.connect(before_b_passage, r.super_jump_feather, back=False) # superjump after hinox to access stairs
            #TODO: after_b_passage.connect((vacuum_room, final_switch_west, final_switch_east), r.super_jump_feather, back=False) # starting from enemy order room, wall clip on bottom wall and low superjump onto pegs, jump pit or setup wall clips/superjumps in SW to get over to vacuum ares [stair shuffle prep]
            #TODO: before_c_passage.connect(pot_pol_room, AND(r.hookshot_clip, r.super_jump_feather), back=False) #hookshot top center pot while touching north wall several times until wall clipped, superjump over pots to key door [stair shuffle prep]
            before_c_passage.connect(pre_boss_room, BOMB, back=False) # use a bomb to lower the second platform

        if options.logic == 'hell':    
            pitbeetle_room.connect(pitbeetle_room_chest2, r.boots_bonk_pit, back=False) # use boots bonk on torch to jump over the pits
            pit_peg_room.connect(mimic_beetle_room, OR(r.boots_bonk_pit, r.hookshot_spam_pit)) # can use both pegasus boots bonks or hookshot spam to cross the pit room
            mimic_beetle_room.connect(statue_switch_room_drop2, AND(r.enemy_requirements["MASKED_MIMIC_GORIYA"], OR(r.boots_bonk_pit, r.hookshot_spam_pit), r.hit_switch), back=False)
            pit_peg_room_chest5.connect((pit_peg_room, mimic_beetle_room), False, back=OR(r.boots_bonk_pit, r.hookshot_spam_pit)) # can use both pegasus boots bonks or hookshot spam to cross the pit room
            before_a_passage.connect(after_a_passage, r.boots_dash_2d) # TODO: Move to HARD logic - # use boots to dash over the spikes in the 2d section
            #TODO: before_a_passage.connect(after_a_passage, OR(r.bracelet_bounce_2d_spikepit, r.toadstool_bounce_2d_spikepit)) # bracelet or toadstool to get damage boost from 2d spikes to get through passage
            between_pits.connect((after_miniboss, vacuum_room), r.boots_bonk_pit) # boots bonk to get over 1 tile pits to or from owl statue
            vacuum_room.connect(entrance, back=False) # let vacuum pull you over pits and warp you to entrance
            #TODO: after_miniboss.connect(vacuum_room, r.hookshot_spam_pit) # hookshot spam to cross single tile pits by owl statue
            #TODO: before_b_passage.connect(after_b_passage, r.boots_bonk_2d_hell) # boots bonk through pirahna passage either way [stair shuffle prep]
            #TODO: after_b_passage.connect(final_switch_east, AND(r.boots_superhop, r.boots_bonk_pit), back=False) # boots superhop up on peg, then boots bonk on pot or wall to cross to chest [stair shuffle prep]
            #TODO: final_switch_west.connect(final_switch_east, r.pit_buffer_boots) # pit buffer onto one of the pots and boots bonk upwards go get to the other side of the peg [stair shuffle prep]
            #TODO: final_switch_east.connect(after_b_passage, r.pit_buffer_itemless, back=False) # pit buffer on pits below chest to get on pegs and leave from lower right exit [stair shuffle prep]
            pot_pol_room_doorway.connect(pot_pol_room, AND(r.hookshot_clip_block), back=False) # hookshot clip through the pots using both pol's voice
            before_c_passage.connect(pre_boss_room, r.boots_jump, back=False) # boots + feather to cross over top and skip the lowering platform
            pre_boss_room.connect(pre_boss, AND(r.boots_bonk_pit, r.hookshot_spam_pit), back=False) # TODO: enclose in OR statement

        self.entrance = entrance
        self.final_room = instrument


class NoDungeon2:
    def __init__(self, options, world_setup, r):
        entrance = Location("D2 Entrance", dungeon=2)
        Location(dungeon=2).add(DungeonChest(0x136)).connect(entrance, POWER_BRACELET)  # chest at entrance
        Location(dungeon=2).add(HeartContainer(0x12B), Instrument(0x12a)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[1]])
        self.entrance = entrance
