from .requirements import *
from .location import Location
from locations.all import *


class DungeonColor:
    def __init__(self, options, world_setup, r):

        # locations
        entrance = Location("D0 Entrance", dungeon=0)
        main_room = Location("D0 Main Area", dungeon=0)
        main_room_chest1 = Location(dungeon=0).add(DungeonChest(0x30F)) # compass
        main_room_chest2 = Location(dungeon=0).add(DungeonChest(0x311)) # beak
        main_room_chest3 = Location(dungeon=0).add(DungeonChest(0x314)) # small key
        main_room_drop1 = Location(dungeon=0).add(DroppedKey(0x308)) # small key
        rupee_room = Location("D0 Secret Rupee Room", dungeon=0)
        miniboss1_room = Location("D0 Miniboss 1", dungeon=0)
        miniboss1_room_chest4 = Location(dungeon=0).add(DungeonChest(0x302)) # nightmare key
        miniboss2_room = Location("D0 Miniboss 2", dungeon=0)
        button_room = Location("D0 Hidden Button Room", dungeon=0)
        north_room = Location("D0 North Area", dungeon=0)
        north_room_chest5 = Location(dungeon=0).add(DungeonChest(0x306)) # map
        north_room_drop2 = Location(dungeon=0).add(DroppedKey(0x307)) # small key
        west_room = Location("D0 3x3 Puzzle Room", dungeon=0)
        fourzol_room = Location("D0 Four Zol Room", dungeon=0)
        switch_room = Location("D0 Room Before Boss", dungeon=0)
        pre_boss = Location("D0 Outside Boss Door", dungeon=0)
        boss_room = Location("D0 Boss Room", dungeon=0)
        instrument = Location("D0 Fairy Room", dungeon=0).add(TunicFairy(0), TunicFairy(1)) # red tunic, blue tunic

        # owl statues
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=0).add(OwlStatue(0x30F)).connect(main_room, STONE_BEAK0) # Main Area <--> Entrance owl
            Location(dungeon=0).add(OwlStatue(0x308)).connect(main_room, STONE_BEAK0) # Main Area <--> Upper Key owl
            Location(dungeon=0).add(OwlStatue(0x30A)).connect(west_room, STONE_BEAK0) # 3x3 Puzzle Room <--> Puzzowl

        # connections
        entrance.connect(main_room, AND(r.enemy_requirements["COLOR_GHOUL_GREEN"], r.enemy_requirements["COLOR_GHOUL_RED"])) # Entrance <--> Main Area
        main_room.connect(main_room_chest1, OR(r.hit_switch, SHIELD)) # Main Area <--> Entrance Chest
        main_room.connect(main_room_chest2, AND(POWER_BRACELET, r.attack_hookshot)) # Main Area <--> Two Socket Chest
        main_room.connect(main_room_chest3, AND(r.enemy_requirements["COLOR_GHOUL_GREEN"], r.enemy_requirements["COLOR_GHOUL_RED"])) # Main Area <--> Lower Small Key
        main_room.connect(main_room_drop1, OR(r.hit_switch, SHIELD)) # Main Area <--> Upper Small Key
        main_room.connect(rupee_room, BOMB) # Main Area <--> Secret Rupee Room
        main_room.connect(miniboss1_room, AND(KEY0, FOUND(KEY0, 3))) # Main Area <--> Miniboss 1
        miniboss1_room.connect(miniboss1_room_chest4, r.miniboss_requirements[world_setup.miniboss_mapping["c2"]]) # Miniboss 1 <--> Nightmare Key Chest
        main_room.connect(miniboss2_room, AND(KEY0, FOUND(KEY0, 2))) # Main Area <--> Miniboss 2
        miniboss2_room.connect(button_room, r.miniboss_requirements[world_setup.miniboss_mapping["c1"]]) # Miniboss 2 <--> Hidden Button Room
        button_room.connect(north_room, POWER_BRACELET)  # Hidden Button Room <--> North Area
        north_room.connect(north_room_chest5, AND(r.enemy_requirements["ZOL"], r.enemy_requirements["HIDING_ZOL"])) # North Area <--> Zol Chest
        north_room.connect(north_room_drop2, AND(r.attack_hookshot, POWER_BRACELET)) # North Area <--> Bullshit Room
        button_room.connect(west_room, POWER_BRACELET) # Hidden Button Room <--> 3x3 Puzzle Room
        west_room.connect(fourzol_room, OR(r.hit_switch, SHIELD)) # 3x3 Puzzle Room <--> Four Zol Room
        fourzol_room.connect(switch_room, AND(KEY0, FOUND(KEY0, 3))) # Four Zol Room <--> Room Before Boss
        switch_room.connect(pre_boss, OR(r.hit_switch, AND(PEGASUS_BOOTS, FEATHER))) # Room Before Boss <--> Outside Boss Door
        pre_boss.connect(boss_room, NIGHTMARE_KEY0) # Outside Boss Door <--> Boss Room
        boss_room.connect(instrument, r.boss_requirements[world_setup.boss_mapping[8]]) # Boss Room <--> Fairy Room

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            entrance.connect(main_room, r.throw_pot) # throw pots to kill karakoro
            main_room.connect(main_room_chest3, r.throw_pot) # throw pots to kill camo goblin
            north_room.connect(north_room_chest5, r.throw_pot) # throw pots to kill zols
            main_room.connect(main_room_chest2, r.attack_hookshot_no_bomb) # knock the karakoro into the pit without picking them up
            switch_room.connect(pre_boss, r.tight_jump) # before the boss, jump past raised blocks with only feather

        if options.logic == 'hell':
            main_room.connect(main_room_chest3, r.shield_bump) # shield bump camo goblins into pit
            main_room.connect(main_room_chest2, OR(BOMB, r.shield_bump)) # shield bump or bomb two socket karakoro into the holes
            north_room.connect(north_room_drop2, OR(BOMB, r.shield_bump)) # shield bump or bomb four socket karakoro into the holes
            
        self.entrance = entrance
        self.final_room = instrument


class NoDungeonColor:
    def __init__(self, options, world_setup, r):
        entrance = Location(dungeon=0)
        boss = Location(dungeon=0)
        entrance.connect(boss, r.boss_requirements[world_setup.boss_mapping[8]])
        boss.add(TunicFairy(0), TunicFairy(1))

        self.entrance = entrance
