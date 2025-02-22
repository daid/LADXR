from .requirements import *
from .location import Location
from locations.all import *


class Dungeon1:
    def __init__(self, options, world_setup, r):

        #locations
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
        north_room = Location("D1 North Area", dungeon=1)
        feather_room = Location("D1 Feather Room", dungeon=1).add(DungeonChest(0x11D)) # feather
        east_room = Location("D1 Right Area", dungeon=1)
        east_room_chest6 = Location(dungeon=1).add(DungeonChest(0x10A)) # stone beak
        miniboss_room = Location("D1 Miniboss", dungeon=1)
        fourblade_room = Location("D1 After Miniboss", dungeon=1)
        boss_room = Location("D1 Boss Room", dungeon=1)
        boss = Location("D1 Boss Rewards", dungeon=1).add(HeartContainer(0x106), Instrument(0x102)) # heart container, instrument

        #owl statues
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=1).add(OwlStatue(0x103)).connect(north_room, STONE_BEAK1)
            Location(dungeon=1).add(OwlStatue(0x104)).connect(north_room, STONE_BEAK1)
            Location(dungeon=1).add(OwlStatue(0x10A)).connect(east_room, STONE_BEAK1)

        #connections
        entrance_drop1.connect(entrance, OR(r.enemy_requirements["HARDHAT_BEETLE"], r.push_hardhat)) # Entrance <--> Hardhat Beetles Key
        entrance_chest1.connect(entrance, None) # Entrance <--> Four Zol Chest
        entrance_chest2.connect(entrance, None) # Entrance <--> Pit Button Chest
        entrance_chest3.connect(entrance, AND(OR(r.enemy_requirements["STALFOS_EVASIVE"], SHIELD), r.enemy_requirements["KEESE"])) # Entrance <--> Two Stalfos, Two Key Chest
        main_room.connect(entrance, None) # Entrance <--> Main Area
        main_room_chest3.connect(main_room, None) # Main Area <--> Spark, Mini-Moldorm Chest
        main_room_chest4.connect(main_room, OR(r.enemy_requirements["MINI_MOLDORM"], SHIELD)) # Main Area <--> Mini-Moldorn Spawn Chest
        main_room_chest5.connect(entrance, AND(FEATHER, KEY1, FOUND(KEY1, 3))) # Main Area <--> Nightmare Key Chest
        seashell_room.connect(main_room, BOMB) # Main Area <--> Hidden Bombable Wall Room
        north_room.connect(main_room, AND(KEY1, FOUND(KEY1, 3))) # Main Area <--> North Area
        feather_room.connect(north_room, OR(r.enemy_requirements["SPIKED_BEETLE"], SHIELD)) # North Area <--> Feather Room
        east_room.connect(main_room, AND(KEY1, FOUND(KEY1, 3))) # Main Area <--> East Area
        east_room_chest6.connect(east_room, r.enemy_requirements["THREE_OF_A_KIND"]) # Right Area <--> Three of a Kind Chest
        miniboss_room.connect(east_room, FEATHER) # East Area <--> Miniboss Room
        fourblade_room.connect(miniboss_room, r.miniboss_requirements[world_setup.miniboss_mapping[0]]) # Miniboss <--> After Miniboss
        boss_room.connect(fourblade_room, NIGHTMARE_KEY1) # After Miniboss <--> Boss Room
        boss.connect(boss_room, r.boss_requirements[world_setup.boss_mapping[0]]) # Boss Room <--> Boss Rewards

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            entrance_chest3.connect(entrance, r.enemy_requirements["KEESE"]) # stalfos jump away when you press a button.

        if options.logic == 'glitched' or options.logic == 'hell':
            main_room_chest5.connect(entrance, r.super_jump_feather)  # super jump
            miniboss_room.connect(east_room, OR(r.damage_boost, r.pit_buffer_itemless)) # damage boost or buffer or mushroom pause over the pit to cross 
        
        if options.logic == 'hell':
            feather_room.connect(north_room, SWORD) # keep slashing the spiked beetles until they keep moving 1 pixel close towards you and the pit, to get them to fall
            main_room_chest5.connect(entrance, AND(r.damage_boost, FOUND(KEY1,3))) # damage boost off the hardhat to cross the pit
            
        self.entrance = entrance
        self.final_room = boss


class NoDungeon1:
    def __init__(self, options, world_setup, r):
        entrance = Location("D1 Entrance", dungeon=1)
        Location(dungeon=1).add(HeartContainer(0x106), Instrument(0x102)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[0]])
        self.entrance = entrance
