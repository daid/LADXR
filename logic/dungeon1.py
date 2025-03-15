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
        main_room = Location("D1 Main Area", dungeon=1)
        main_room_chest3 = Location(dungeon=1).add(DungeonChest(0x10E)) # small key
        main_room_chest4 = Location(dungeon=1).add(DungeonChest(0x10D)) # 20 rupees
        main_room_chest5 = Location(dungeon=1).add(DungeonChest(0x108)) # nightmare key
        seashell_room = Location("Hidden Bombable Wall Room", dungeon=1).add(DungeonChest(0x10C)) # seashell
        north_room = Location("D1 North Room", dungeon=1)
        northwest_room = Location("D1 Spiked Beetle Room", dungeon=1)
        feather_room = Location("D1 Feather Room", dungeon=1).add(DungeonChest(0x11D)) # feather
        east_room = Location("D1 East Area", dungeon=1)
        east_room_chest6 = Location(dungeon=1).add(DungeonChest(0x10A)) # stone beak
        miniboss_room = Location("D1 Miniboss", dungeon=1)
        fourblade_room = Location("D1 After Miniboss", dungeon=1)
        boss_room = Location("D1 Boss Room", dungeon=1)
        boss_room_drop2 = Location(dungeon=1).add(HeartContainer(0x106)) # heart container
        instrument = Location("D1 Instrument Room", dungeon=1).add(Instrument(0x102)) # full moon cello

        # owl statues
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=1).add(OwlStatue(0x104)).connect(north_room, STONE_BEAK1) # North Room <--> Movable Block Owl
            Location(dungeon=1).add(OwlStatue(0x103)).connect(northwest_room, STONE_BEAK1) # North Room <--> Spiked Beetle Owl
            Location(dungeon=1).add(OwlStatue(0x10A)).connect(east_room, STONE_BEAK1) # East Area <--> Three of a Kind Owl

        # connections
        entrance.connect(entrance_drop1, OR(r.enemy_requirements["HARDHAT_BEETLE"], r.push_hardhat)) # Entrance <--> Hardhat Beetles Key
        entrance.connect(entrance_chest1, None) # Entrance <--> Four Zol Chest
        entrance.connect(entrance_chest2, None) # Entrance <--> Pit Button Chest
        entrance.connect(entrance_chest3, AND(OR(r.enemy_requirements["STALFOS_EVASIVE"], SHIELD), r.enemy_requirements["KEESE"])) # Entrance <--> Two Stalfos, Two Key Chest
        entrance.connect(main_room, None) # Entrance <--> Main Area
        main_room.connect(main_room_chest3, None) # Main Area <--> Spark, Mini-Moldorm Chest
        main_room.connect(main_room_chest4, OR(r.enemy_requirements["MINI_MOLDORM"], SHIELD)) # Main Area <--> Mini-Moldorn Spawn Chest
        entrance.connect(main_room_chest5, AND(FEATHER, FOUND(KEY1, 3))) # Main Area <--> Nightmare Key Chest
        main_room.connect(seashell_room, BOMB) # Main Area <--> Hidden Bombable Wall Room
        main_room.connect(north_room, FOUND(KEY1, 3)) # Main Area <--> North Area
        north_room.connect(northwest_room, None) # North Room <--> Spiked Beetle Room
        northwest_room.connect(feather_room, OR(r.enemy_requirements["SPIKED_BEETLE"], SHIELD)) # North Area <--> Feather Room
        main_room.connect(east_room, FOUND(KEY1, 3)) # Main Area <--> East Area
        east_room.connect(east_room_chest6, r.enemy_requirements["THREE_OF_A_KIND"]) # East Area <--> Three of a Kind Chest
        east_room.connect(miniboss_room, FEATHER) # East Area <--> Miniboss Room
        miniboss_room.connect(fourblade_room, r.miniboss_requirements[world_setup.miniboss_mapping[0]]) # Miniboss <--> After Miniboss
        fourblade_room.connect(boss_room, NIGHTMARE_KEY1) # After Miniboss <--> Boss Room
        boss_room.connect(boss_room_drop2, r.boss_requirements[world_setup.boss_mapping[0]]) # Boss Room <--> Moldorm Heart Container
        boss_room.connect(instrument, r.boss_requirements[world_setup.boss_mapping[0]]) # Boss Room <--> Instrument Room

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            entrance.connect(entrance_chest3, r.enemy_requirements["KEESE"]) # stalfos jump away when you press a button.

        if options.logic == 'glitched' or options.logic == 'hell':
            entrance.connect(main_room_chest5, r.super_jump_feather) # super jump
            east_room.connect(miniboss_room, OR(r.damage_boost, r.pit_buffer_itemless)) # itemless pit buffer to miniboss door 
        
        if options.logic == 'hell':
            main_room.connect(main_room_chest5, AND(r.damage_boost, FOUND(KEY1, 3))) # damage boost off the hardhat to cross the pit
            north_room.connect(feather_room, SWORD) # keep slashing the spiked beetles until they keep moving 1 pixel close towards you and the pit, to get them to fall
            
        self.entrance = entrance
        self.final_room = instrument


class NoDungeon1:
    def __init__(self, options, world_setup, r):
        entrance = Location("D1 Entrance", dungeon=1)
        Location(dungeon=1).add(HeartContainer(0x106), Instrument(0x102)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[0]])
        self.entrance = entrance
