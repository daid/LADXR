from .requirements import *
from .location import Location
from locations.all import *


class Dungeon1:
    def __init__(self, options, world_setup, r):

        # locations
        entrance = Location("D1 Entrance", dungeon=1)
        entrance_drop1 = Location(dungeon=1).add(DroppedKey(0x116)) # small key
        entrance_chest1 = Location(dungeon=1).add(DungeonChest(0x115)) # compass
        entrance_chest2 = Location(dungeon=1).add(DungeonChest(0x113)) # small key
        entrance_chest3 = Location(dungeon=1).add(DungeonChest(0x114)) # map
        cracked_pit_room = Location("D1 Cracked Pit Room", dungeon=1)
        main_room = Location("D1 Main Area", dungeon=1)
        main_room_chest4 = Location(dungeon=1).add(DungeonChest(0x10E)) # small key
        main_room_chest5 = Location(dungeon=1).add(DungeonChest(0x10D)) # 20 rupees
        pre_keyblock = Location("D1 Before Key Block", dungeon=1)
        fenced_walkway = Location("D1 Fenced Area", dungeon=1)
        fenced_walkway_chest6 = Location(dungeon=1).add(DungeonChest(0x108)) # nightmare key
        bombable_room = Location("Bombable Wall Room", dungeon=1)
        bombable_room_chest7 = Location(dungeon=1).add(DungeonChest(0x10C)) # seashell
        north_room = Location("D1 North Room", dungeon=1)
        north_room_owl1 = Location(dungeon=1).add(OwlStatue(0x104)) # hint
        northwest_room = Location("D1 Spiked Beetle Room", dungeon=1)
        northwest_room_owl2 = Location(dungeon=1).add(OwlStatue(0x103)) # hint
        before_a_passage = Location("D1 Passage Spawn", dungeon=1)
        after_a_passage = Location("D1 Feather Room", dungeon=1)
        after_a_passage_chest8 = Location(dungeon=1).add(DungeonChest(0x11D)) # feather
        east_room = Location("D1 East Area", dungeon=1)
        east_room_chest7 = Location(dungeon=1).add(DungeonChest(0x10A)) # stone beak
        east_room_owl3 = Location(dungeon=1).add(OwlStatue(0x10A)) # hint
        miniboss_room = Location("D1 Miniboss", dungeon=1)
        fourblade_room = Location("D1 After Miniboss", dungeon=1)
        boss_room = Location("D1 Boss Room", dungeon=1)
        boss_basement = Location("D1 Boss Basement", dungeon=1)
        boss_room_drop2 = Location(dungeon=1).add(HeartContainer(0x106)) # heart container
        instrument = Location("D1 Instrument Room", dungeon=1).add(Instrument(0x102)) # full moon cello

        # owl statues
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            north_room.connect(north_room_owl1, STONE_BEAK1, back=False)
            northwest_room.connect(northwest_room_owl2, STONE_BEAK1, back=False)
            east_room.connect(east_room_owl3, STONE_BEAK1, back=False)

        # connections
        # entrance
        entrance.connect(entrance_drop1, OR(r.enemy_requirements["HARDHAT_BEETLE"], r.push_hardhat), back=False)
        entrance.connect(entrance_chest1, back=False)
        entrance.connect(entrance_chest2, back=False)
        entrance.connect(entrance_chest3, AND(OR(r.enemy_requirements["STALFOS_EVASIVE"], SHIELD), r.enemy_requirements["KEESE"]), back=False) #TODO: REMOVE, replace with casual logic statement
        entrance.connect(main_room, back=False)
        entrance.connect(cracked_pit_room, back=r.enemy_requirements["KEESE"])

        # main area
        main_room.connect(main_room_chest4, back=False)
        main_room.connect(main_room_chest5, OR(r.enemy_requirements["MINI_MOLDORM"], SHIELD), back=False)
        main_room.connect(pre_keyblock, FEATHER)
        main_room.connect(north_room, FOUND(KEY1, 3))
        main_room.connect(east_room, FOUND(KEY1, 3))
        pre_keyblock.connect(fenced_walkway, FOUND(KEY1, 3))
        fenced_walkway.connect(fenced_walkway_chest6, back=False)
        main_room.connect(bombable_room, BOMB)
        bombable_room.connect(bombable_room_chest7, back=False)
        # northwest
        north_room.connect(northwest_room)
        northwest_room.connect(before_a_passage, OR(r.enemy_requirements["SPIKED_BEETLE"], SHIELD), back=None) #TODO: REMOVE, replace with casual logic statement
        before_a_passage.connect(after_a_passage)
        after_a_passage.connect(after_a_passage_chest8, back=False)
        # boss
        east_room.connect(east_room_chest7, r.enemy_requirements["THREE_OF_A_KIND"], back=False)
        east_room.connect(miniboss_room, FEATHER, back=AND(FEATHER, r.miniboss_requirements[world_setup.miniboss_mapping[0]]))
        miniboss_room.connect(entrance, r.miniboss_requirements[world_setup.miniboss_mapping[0]], back=False) # miniboss portal
        miniboss_room.connect(fourblade_room, r.miniboss_requirements[world_setup.miniboss_mapping[0]], back=None)
        fourblade_room.connect(boss_room, NIGHTMARE_KEY1, back=r.boss_requirements[world_setup.boss_mapping[0]])
        #TODO: boss_room.connect(boss_basement, back=False) # [no relevance until stairs shuffle]
        #TODO: boss_basement.connect(fourblade_room) # [no relevance until stairs shuffle]
        boss_room.connect((boss_room_drop2, instrument), r.boss_requirements[world_setup.boss_mapping[0]], back=False)

        #TODO: if options.logic == "casual":
            #TODO: entrance.connect(entrance_chest3, AND(r.enemy_requirements["STALFOS_EVASIVE"], r.enemy_requirements["KEESE"]), back=False)
            #TODO: northwest_room.connect(before_a_passage, r.enemy_requirements["SPIKED_BEETLE"], back=None)
        #TODO: else:
            #TODO: entrance.connect(entrance_chest3, AND(OR(r.enemy_requirements["STALFOS_EVASIVE"], SHIELD), r.enemy_requirements["KEESE"]), back=False)
            #TODO: northwest_room.connect(before_a_passage, OR(r.enemy_requirements["SPIKED_BEETLE"], SHIELD), back=None)

        if options.bowwow != "normal":
            cracked_pit_room.connect(main_room, AND(r.enemy_requirements["KEESE"], FEATHER), back=FEATHER) # crystals in main room are pits in good boy mode
        else:
            cracked_pit_room.connect(main_room, AND(r.enemy_requirements["KEESE"], SWORD), back=SWORD)

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            entrance.connect(entrance_chest3, r.enemy_requirements["KEESE"], back=False) # make stalfos jump into when you press A or B button
            if options.bowwow == "swordless":
                cracked_pit_room.connect(main_room, r.boots_bonk, back=False) # crystals in main room are pits in swordless good boy mode

        if options.logic == 'glitched' or options.logic == 'hell':
            if options.bowwow == "swordless":
                main_room.connect(cracked_pit_room, r.pit_buffer_itemless, back=False) # crystals in main room are pits in swordless good boy mode
            main_room.connect(fenced_walkway, r.super_jump_feather) # super jump, works both ways, connected from main room since the wall clip must be maintained
            east_room.connect(miniboss_room, OR(r.damage_boost, r.pit_buffer_itemless), back=AND(r.pit_buffer_itemless, r.miniboss_requirements[world_setup.miniboss_mapping[0]])) # itemless pit buffer to/from miniboss door
        
        if options.logic == 'hell':
            main_room.connect(pre_keyblock, r.damage_boost, back=False) # damage boost off the hardhat to cross the pit NOTE: boots bonk also
            northwest_room.connect(before_a_passage, SWORD, back=None) # keep slashing the spiked beetles until 1 pixel at a time they move into the pit and fall
            
        self.entrance = entrance
        self.final_room = instrument


class NoDungeon1:
    def __init__(self, options, world_setup, r):
        entrance = Location("D1 Entrance", dungeon=1)
        Location(dungeon=1).add(HeartContainer(0x106), Instrument(0x102)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[0]])
        self.entrance = entrance
