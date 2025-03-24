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
        east_torches = Location("D2 East of Torches", dungeon=2)
        east_torches_drop1 = Location(dungeon=2).add(DroppedKey(0x132)) # small key
        east_torches_drop2 = Location(dungeon=2).add(DroppedKey(0x134)) # small key
        east_torches_chest3 = Location(dungeon=2).add(DungeonChest(0x137)) # compass
        pitplatform_room = Location("D2 Platforms & Pits Area", dungeon=2)
        pitplatform_chest4 = Location(dungeon=2).add(DungeonChest(0x138)) # small key
        pitplatform_chest5 = Location(dungeon=2).add(DungeonChest(0x139)) # small key
        mimic_beetle_room = Location("D2 Mimic & Beetle Area", dungeon=2) 
        before_a_passage = Location("D2 Pushblock Room", dungeon=2)
        after_a_passage = Location("D2 Dark Spark Room", dungeon=2)
        miniboss_room = Location("D2 Miniboss Room", dungeon=2)
        after_miniboss = Location("D2 After Miniboss", dungeon=2) # need to return to this and break it into logical sections
        before_b_passage = Location("D2 Blocked Staircase", dungeon=2) # need to return to this and break it into logical sections
        after_b_passage = Location("D2 Enemy Order Room", dungeon=2)
        after_b_passage_chest10 = Location(dungeon=2).add(DungeonChest(0x127)) # nightmare key
        vacuum_room = Location("D2 Vacuum Mouth Area", dungeon=2)
        vacuum_room_chest6 = Location(dungeon=2).add(DungeonChest(0x126)) # map
        vacuum_room_chest7 = Location(dungeon=2).add(DungeonChest(0x121)) # 20 rupees
        boo_room = Location("D2 Boo Buddies Room", dungeon=2)
        boo_room_chest8 = Location(dungeon=2).add(DungeonChest(0x120)) # bracelet
        northwest_switch_room = Location("D2 Left of North Trapped Switch", dungeon=2)
        northeast_switch_room = Location("D2 Right of North Trapped Switch", dungeon=2)
        northeast_switch_room_chest9 = Location(dungeon=2).add(DungeonChest(0x122)) # small key
        pot_pol_room_doorway = Location("D2 Pots & Pols Room Doorway", dungeon=2)
        pot_pol_room = Location("D2 Pots & Pols Room", dungeon=2)
        before_c_passage = Location("D2 Boss Passageway Spawn", dungeon=2)
        pre_boss_room = Location("D2 Room Before Boss", dungeon=2)
        pre_boss = Location("D2 Outside Boss Door", dungeon=2)
        boss_room = Location("D2 Boss Room", dungeon=2)
        boss_room_drop3 = Location(dungeon=2).add(HeartContainer(0x12B)) # heart container
        instrument = Location("D2 Instrument Room", dungeon=2).add(Instrument(0x12a)) # conch horn
        
        # owl statues
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=2).add(OwlStatue(0x133)).connect(east_torches, STONE_BEAK2) # East of Torches <--> Switch Owl
            Location(dungeon=2).add(OwlStatue(0x12F)).connect(before_a_passage, STONE_BEAK2) # Pushblock Room <--> Before First Staircase Owl
            Location(dungeon=2).add(OwlStatue(0x129)).connect(vacuum_room, STONE_BEAK2) # Vacuum Mouth Area <--> After Hinox Owl

        entrance.connect(entrance_chest1, POWER_BRACELET) # Entrance <--> Entrance Chest
        entrance.connect(blade_room, FOUND(KEY2, 5)) # Entrance <--> West of Torches
        pitbeetle_room.connect(blade_room, r.enemy_requirements["KEESE"]) # West of Torches <--> Hardhat Beetle Room
        pitbeetle_room.connect(pitbeetle_room_chest2, OR(FEATHER, HOOKSHOT)) # Beetle Room <--> Hardhat Beetle Pit Chest
        entrance.connect(east_torches, r.fire) # Entrance <--> East of Torches
        east_torches.connect(east_torches_drop1, AND(r.enemy_requirements["STALFOS_EVASIVE"], r.enemy_requirements["STALFOS_AGGRESSIVE"])) # East of Torches <--> Two Stalfos Key
        east_torches.connect(east_torches_chest3, AND(FOUND(KEY2, 5), r.enemy_requirements["MASKED_MIMIC_GORIYA"])) # East of Torches <--> Mask-Mimic Chest
        east_torches.connect(pitplatform_room, r.hit_switch) # East of Torches <--> Platforms & Pits Area
        pitplatform_room.connect(pitplatform_chest4, r.hit_switch) # Platforms & Pits Area <--> First Switch Locked Chest
        pitplatform_room.connect(pitplatform_chest5, FEATHER) # Platforms & Pits Area <--> Button Spawn Chest
        pitplatform_room.connect(mimic_beetle_room, FEATHER) # Platforms & Pits Area <--> Mimic & Beetle Area
        mimic_beetle_room.connect(before_a_passage, FOUND(KEY2, 3)) # Mimic & Beetle Area <--> Pushblock Room
        before_a_passage.connect(after_a_passage, FEATHER) # Pushblock Room <--> Dark Spark Room
        after_a_passage.connect(miniboss_room, None) # Dark Spark Room <--> Miniboss Room
        miniboss_room.connect(after_miniboss, r.miniboss_requirements[world_setup.miniboss_mapping[1]]) # Miniboss Room <--> After Miniboss
        after_miniboss.connect(before_b_passage, POWER_BRACELET) # After Miniboss <--> Blocked Staircase
        before_b_passage.connect(after_b_passage, FEATHER) # Blocked Staircase <--> Enemy Order Room
        after_b_passage.connect(after_b_passage_chest10, AND(r.enemy_requirements["KEESE"], r.enemy_requirements["MOBLIN"], OR(r.enemy_requirements["POLS_VOICE"], POWER_BRACELET))) # Enemy Order Room <--> Enemy Order Room Chest
        after_miniboss.connect(vacuum_room, FEATHER) # After Miniboss <--> Vacuum Mouth Area
        vacuum_room.connect(vacuum_room_chest6, None) # Vacuum Mouth Area <--> Vacuum Mouth Chest
        vacuum_room.connect(vacuum_room_chest7, None) # Vacuum Mouth Area <--> Outside Boo Buddies Room Chest
        vacuum_room.connect(boo_room, FOUND(KEY2, 5)) # Vacuum Mouth Area <--> Boo Buddies Room
        boo_room.connect(boo_room_chest8, OR(r.fire, r.enemy_requirements["BOO_BUDDY"])) # Boo Buddies Room <--> Boo Buddies Room Chest
        vacuum_room.connect(northwest_switch_room, POWER_BRACELET) # Vacuum Mouth Area <--> Left of North Trapped Switch
        northwest_switch_room.connect(northeast_switch_room, r.hit_switch) # Left of North Trapped Switch <--> Right of North Trapped Switch
        northeast_switch_room.connect(northeast_switch_room_chest9, None) # Right of North Trapped Switch <--> Second Switch Locked Chest
        northeast_switch_room.connect(after_b_passage, r.hit_switch, one_way=True) # Right of North Trapped Switch <--> Enemy Order Room
        after_b_passage.connect(pot_pol_room_doorway, FOUND(KEY2, 5)) # Enemy Order Room <--> Pots & Pols Room Doorway
        pot_pol_room_doorway.connect(pot_pol_room, POWER_BRACELET) # Pots & Pols Room Doorway <--> Pots & Pols Room
        pot_pol_room.connect(before_c_passage, AND(OR(POWER_BRACELET, r.enemy_requirements["POLS_VOICE"]), r.enemy_requirements["ZOL"])) # Pots & Pols Room --> Boss Passageway Spawn #TODO: enemy randomizer would make this pot kill requirement inaccurate. Also, technically you can kill zols with pots too, given 20 available, consider for normal logic
        #TODO: before_c_passage.connect(pot_pol_room, None, one_way=True) # Boss Passageway Spawn --> Pots & Pols Room [logic prep for staircase rando]
        before_c_passage.connect(pre_boss_room, POWER_BRACELET) # Boss Passageway <--> Room Before Boss
        pre_boss_room.connect(pre_boss, FEATHER) # Room Before Boss <--> Outside Boss Door
        pre_boss.connect(boss_room, NIGHTMARE_KEY2) # Outside Boss Door <--> Boss Room
        boss_room.connect(boss_room_drop3, r.boss_requirements[world_setup.boss_mapping[1]]) # Boss Room <--> Heart Container
        boss_room.connect(instrument, r.boss_requirements[world_setup.boss_mapping[1]]) # Boss Room <--> Instrument Room

        # connections
        if options.logic == "casual":
            mimic_beetle_room.connect(east_torches_drop2, AND(FEATHER, r.enemy_requirements["MASKED_MIMIC_GORIYA"])) # exclude killing mimics from Spark room
        else:
            east_torches.connect(east_torches_drop2, OR(r.rear_attack, AND(FEATHER, r.enemy_requirements["MASKED_MIMIC_GORIYA"]))) # East of Torches <--> Mask Mimic Key

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            #outside_passage_b.connect(vacuum_room, POWER_BRACELET, one_way=True) # exit passage b stairs by lifting pot and also r.corner_walk if it were in requirements.py
            #TODO: northwest_switch_room.connect(northeast_switch_room, r.tight_jump) # jump around the single peg blocking the switch [logic prep for stairs rando]
            after_b_passage.connect(northeast_switch_room, AND(r.hit_switch, r.tight_jump)) # 

        if options.logic == 'glitched' or options.logic == 'hell':
            boo_room.connect(boo_room_chest8, SWORD) # use sword to spawn ghosts on other side of the room so they run away (logically irrelevant because player will have fire)
            after_miniboss.connect(before_b_passage, r.super_jump_feather, one_way=True) # superjump after hinox to access passage B
            #TODO: vacuum_room.connect(northeast_switch_room, AND(POWER_BRACELET, r.super_jump_feather), one_way=True) # lift pots, wall clip on bottom wall, and low superjump onto pegs. then you can jump to either side of the locked switch [logic prep for stairs rando]
            #TODO: vacuum_room.connect(northwest_switch_room, AND(POWER_BRACELET, r.super_jump_feather), one_way=True) # lift pots, wall clip on bottom wall, and low superjump onto pegs. then you can jump to either side of the locked switch [logic prep for stairs rando]
            #TODO: after_b_passage.connect(northeast_switch_room, r.super_jump_feather, one_way=True) # wall clip on bottom wall, and low superjump onto pegs. then you can jump to either side of the locked switch [logic prep for stairs rando]
            #TODO: after_b_passage.connect(northwest_switch_room, r.super_jump_feather, one_way=True) # wall clip on bottom wall, and low superjump onto pegs. then you can jump to either side of the locked switch [logic prep for stairs rando]
            #TODO: after_b_passage.connect(vacuum_room, r.super_jump_feather, one_way=True) # starting from enemy order room, wall clip and walk all the way to switch room, superjump onto pegs, two diagonal jumps to leafe lower lefe wall clipped, then multiple superjumps to escape past pots [logic prep for stairs rando]
            #TODO: before_c_passage.connect(pot_pol_room, AND(r.hookshot_clip, r.super_jump_feather), one_way=True) # [logic prep for staircase rando] - hookshot top center pot while touching north wall several times until wall clipped, superjump over pots to key door [logic prep for stairs rando]
            
        if options.logic == 'hell':    
            pitbeetle_room.connect(pitbeetle_room_chest2, r.boots_bonk_pit) # use boots bonk on torch to jump over the pits
            pitplatform_room.connect(pitplatform_chest5, OR(r.boots_bonk_pit, r.hookshot_spam_pit)) # can use both pegasus boots bonks or hookshot spam to cross the pit room
            pitplatform_room.connect(mimic_beetle_room, OR(r.boots_bonk_pit, r.hookshot_spam_pit)) # can use both pegasus boots bonks or hookshot spam to cross the pit room
            mimic_beetle_room.connect(east_torches_drop2, AND(r.rear_attack_range, OR(r.boots_bonk_pit, r.hookshot_spam_pit))) # defeat mimics and then travel back to grab the key with hell tricks to get back through pit/peg room
            before_a_passage.connect(after_a_passage, r.boots_dash_2d) # TODO: Move to HARD logic -  use boots to dash over the spikes in the 2d section
            #TODO: before_a_passage.connect(after_a_passage, OR(r.bracelet_bounce_2d_spikepit, r.toadstool_bounce_2d_spikepit)) # bracelet or toadstool to get damage boost from 2d spikes to get through passage [logic prep for stairs rando]
            after_miniboss.connect(vacuum_room, r.boots_bonk_pit) # boots bonk to get over 1 tile pits by owl statue
            #TODO: after_miniboss.connect(vacuum_room, r.hookshot_spam_pit) # hookshot spam to cross single tile pits by owl statue [logic prep for stairs rando]
            #TODO: before_b_passage.connect(after_b_passage, r.boots_bonk_2d_hell) # boots bonk through pirahna passage either way [logic prep for stairs rando]
            #TODO: northwest_switch_room.connect(northeast_switch_room, r.pit_buffer_boots) # pit buffer onto one of the pots and boots bonk diagonally upwards go get to the other side of the peg [logic prep for stairs rando]
            #TODO: northeast_switch_room.connect(after_b_passage, None, one_way=True) # pit buffer on pits below chest to get on pegs and leave from lower right exit [logic prep for stairs rando]
            pot_pol_room_doorway.connect(before_c_passage, AND(r.hookshot_clip_block, r.enemy_requirements["ZOL"], r.enemy_requirements["POLS_VOICE"])) # hookshot clip through the pot using both pol's voice 
            before_c_passage.connect(pre_boss_room, OR(BOMB, r.boots_jump)) # use a bomb to lower the last platform, or boots + feather to cross over top (only relevant in hell logic)
            pre_boss_room.connect(pre_boss, AND(r.boots_bonk_pit, r.hookshot_spam_pit)) # TODO: enclose in OR statement to allow boots only method

            #TODO: consider fake "SWITCH_2" item for conciseness and preparedness for stair shuffle

        self.entrance = entrance
        self.final_room = instrument


class NoDungeon2:
    def __init__(self, options, world_setup, r):
        entrance = Location("D2 Entrance", dungeon=2)
        Location(dungeon=2).add(DungeonChest(0x136)).connect(entrance, POWER_BRACELET)  # chest at entrance
        Location(dungeon=2).add(HeartContainer(0x12B), Instrument(0x12a)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[1]])
        self.entrance = entrance
