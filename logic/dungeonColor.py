from .requirements import *
from .location import Location
from locations.all import *


class DungeonColor:
    def __init__(self, options, world_setup, r):
        
        #locations
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
        boss = Location("D0 Fairy Room", dungeon=0).add(TunicFairy(0), TunicFairy(1)) # tunics

        #owl statues
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=0).add(OwlStatue(0x30F)).connect(main_room, STONE_BEAK0, id="lg") # Main Area <--> Entrance owl
            Location(dungeon=0).add(OwlStatue(0x308)).connect(main_room, STONE_BEAK0, id="") # Main Area <--> Upper Key owl
            Location(dungeon=0).add(OwlStatue(0x30A)).connect(west_room, STONE_BEAK0, id="lp") # 3x3 Puzzle Room <--> Puzzowl

        #connections
        main_room.connect(entrance, AND(r.enemy_requirements["COLOR_GHOUL_GREEN"], r.enemy_requirements["COLOR_GHOUL_RED"]), id="") # Entrance <--> Main Area
        main_room_chest1.connect(main_room, OR(r.hit_switch, SHIELD), id="li") # Main Area <--> Entrance Chest
        main_room_chest2.connect(main_room, AND(POWER_BRACELET, r.attack_hookshot), id="lh") # Main Area <--> Two Socket Chest
        main_room_chest3.connect(main_room, AND(r.enemy_requirements["COLOR_GHOUL_GREEN"], r.enemy_requirements["COLOR_GHOUL_RED"]), id="lf") # Main Area <--> Lower Small Key
        main_room_drop1.connect(main_room, OR(r.hit_switch, SHIELD), id="") # Main Area <--> Upper Small Key
        rupee_room.connect(main_room, BOMB, id="") # Main Area <--> Secret Rupee Room
        miniboss1_room.connect(main_room, AND(KEY0, FOUND(KEY0, 3)), id="lj") # Main Area <--> Miniboss 1
        miniboss1_room_chest4.connect(miniboss1_room, r.miniboss_requirements[world_setup.miniboss_mapping["c2"]], id="lk") # Miniboss 1 <--> Nightmare Key Chest
        miniboss2_room.connect(main_room, AND(KEY0, FOUND(KEY0, 2)), id="ll") # Main Area <--> Miniboss 2
        button_room.connect(miniboss2_room, r.miniboss_requirements[world_setup.miniboss_mapping["c1"]], id="lm") # Miniboss 2 <--> Hidden Button Room
        north_room.connect(button_room, POWER_BRACELET, id="")  # Hidden Button Room <--> North Area
        north_room_chest5.connect(north_room, AND(r.enemy_requirements["ZOL"], r.enemy_requirements["HIDING_ZOL"]), id="") # North Area <--> Zol Chest
        north_room_drop2.connect(north_room, AND(r.attack_hookshot, POWER_BRACELET), id="lo") # North Area <--> Bullshit Room
        west_room.connect(button_room, POWER_BRACELET, id="ln") # Hidden Button Room <--> 3x3 Puzzle Room
        fourzol_room.connect(west_room, OR(r.hit_switch, SHIELD), id="lq") # 3x3 Puzzle Room <--> Four Zol Room
        switch_room.connect(fourzol_room, AND(KEY0, FOUND(KEY0, 3)), id="lr") # Four Zol Room <--> Room Before Boss
        pre_boss.connect(switch_room, OR(r.hit_switch, AND(PEGASUS_BOOTS, FEATHER)), id="ls") # Room Before Boss <--> Outside Boss Door
        boss_room.connect(pre_boss, NIGHTMARE_KEY0, id="lt") # Outside Boss Door <--> Boss Room
        boss.connect(boss_room, r.boss_requirements[world_setup.boss_mapping[8]], id="lu") # Boss Room <--> Fairy Room

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            main_room.connect(entrance, r.throw_pot, id="lv") # throw pots to kill karakoro
            main_room_chest3.connect(main_room, r.throw_pot, id="") # throw pots to kill camo goblin
            north_room_chest5.connect(north_room, r.throw_pot, id="") # throw pots to kill zols
            main_room_chest2.connect(main_room, r.attack_hookshot_no_bomb, id="lw") # knock the karakoro into the pit without picking them up
            pre_boss.connect(switch_room, r.tight_jump, id="lx") # before the boss, jump past raised blocks with only feather

        if options.logic == 'hell':
            main_room_chest3.connect(main_room, r.shield_bump, id="") # shield bump camo goblins into pit
            main_room_chest2.connect(main_room, OR(BOMB, r.shield_bump), id="lz") # shield bump or bomb two socket karakoro into the holes
            north_room_drop2.connect(north_room, OR(BOMB, r.shield_bump), id="m0") # shield bump or bomb four socket karakoro into the holes
            
        self.entrance = entrance
        self.final_room = boss


class NoDungeonColor:
    def __init__(self, options, world_setup, r):
        entrance = Location(dungeon=0)
        boss = Location(dungeon=0).connect(entrance, r.boss_requirements[world_setup.boss_mapping[8]])
        boss.add(TunicFairy(0), TunicFairy(1))

        self.entrance = entrance
