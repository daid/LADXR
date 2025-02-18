from .requirements import *
from .location import Location
from locations.all import *


class DungeonColor:
    def __init__(self, options, world_setup, r):

        entrance = Location("D0 Entrance", dungeon=0)
        main_room = Location("D0 Lower Right Area", dungeon=0).connect(entrance, AND(r.enemy_requirements["COLOR_GHOUL_GREEN"], r.enemy_requirements["COLOR_GHOUL_RED"])) # connect D0 Entrance to D0 Lower Right Area
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=0).add(OwlStatue(0x30F)).connect(main_room, STONE_BEAK0) # lower owl statue
            Location(dungeon=0).add(OwlStatue(0x308)).connect(main_room, STONE_BEAK0) # upper owl statue
        Location(dungeon=0).add(DungeonChest(0x30F)).connect(main_room, OR(r.hit_switch, SHIELD)) # compass chest
        Location(dungeon=0).add(DungeonChest(0x314)).connect(main_room, AND(r.enemy_requirements["COLOR_GHOUL_GREEN"], r.enemy_requirements["COLOR_GHOUL_RED"])) # lower small key chest
        Location(dungeon=0).add(DroppedKey(0x308)).connect(main_room, OR(r.hit_switch, SHIELD)) # upper small key drop
        Location(dungeon=0).add(DungeonChest(0x311)).connect(main_room, AND(POWER_BRACELET, r.attack_hookshot)) # stone beak chest
        miniboss_room1 = Location("D0 Miniboss 1 Room", dungeon=0).connect(main_room, AND(KEY0, FOUND(KEY0, 3))) # miniboss 1 key requirement
        miniboss1 = Location("D0 Nightmare Key Room", dungeon=0).connect(miniboss_room1, r.miniboss_requirements[world_setup.miniboss_mapping["c2"]])
        miniboss1.add(DungeonChest(0x302)) # nightmare key after miniboss 1
        miniboss_room2 = Location("D0 Miniboss 2 Room", dungeon=0).connect(main_room, AND(KEY0, FOUND(KEY0, 2))) # miniboss 2 room key requirement
        potbutton_room = Location("D0 Hidden Button Room", dungeon=0).connect(miniboss_room2, r.miniboss_requirements[world_setup.miniboss_mapping["c1"]]) # import miniboss 2 rewuirements and connect to potbutton room
        north_potbutton_room = Location("D0 North of Hidden Button Room", dungeon=0).connect(potbutton_room, POWER_BRACELET)  # need to lift a pot to reveal button
        Location(dungeon=0).add(DungeonChest(0x306)).connect(north_potbutton_room, AND(r.enemy_requirements["ZOL"], r.enemy_requirements["HIDING_ZOL"])) # map
        Location(dungeon=0).add(DungeonChest(0x307)).connect(north_potbutton_room, AND(r.attack_hookshot, POWER_BRACELET))  # require item to knock Karakoro enemies into shell
        west_potbutton_room = Location("D0 West of Hidden Button Room", dungeon=0).connect(potbutton_room, POWER_BRACELET) # 3x3 room
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=0).add(OwlStatue(0x30A)).connect(west_potbutton_room, STONE_BEAK0) # west owl statue
        fourzol_room = Location("D0 Four Zol Room", dungeon=0).connect(west_potbutton_room, OR(r.hit_switch, SHIELD)) # room after 3x3
        switch_room = Location("D0 Room Before Boss", dungeon=0).connect(fourzol_room, AND(KEY0, FOUND(KEY0, 3))) # room with switch and nightmare door
        pre_boss = Location("D0 Outside Boss Door", dungeon=0).connect(switch_room, OR(r.hit_switch, AND(PEGASUS_BOOTS, FEATHER)))  # before the boss, require item to hit switch or jump past raised blocks
        boss_room = Location("D0 Boss Room", dungeon=0).connect(pre_boss, NIGHTMARE_KEY0) # boss nightmare key requirement
        boss = Location("D0 Fairy Room", dungeon=0).connect(boss_room, r.boss_requirements[world_setup.boss_mapping[8]]) # import boss requirements
        boss.add(TunicFairy(0), TunicFairy(1)) # tunic rewards after boss

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            main_room.connect(entrance, r.throw_pot) # throw pots to kill karakoro
            Location(dungeon=0).add(DungeonChest(0x314)).connect(main_room, r.throw_pot) # throw pots to kill camo goblin
            Location(dungeon=0).add(DungeonChest(0x306)).connect(north_potbutton_room, r.throw_pot) # throw pots to kill zols
            Location(dungeon=0).add(DungeonChest(0x311)).connect(main_room, r.attack_hookshot_no_bomb) # knock the karakoro into the pit without picking them up
            pre_boss.connect(switch_room, r.tight_jump) # before the boss, jump past raised blocks with only feather

        if options.logic == 'hell':
            Location(dungeon=0).add(DungeonChest(0x314)).connect(main_room, r.shield_bump) # shield bump camo goblins into pit
            Location(dungeon=0).add(DungeonChest(0x311)).connect(main_room, OR(BOMB, r.shield_bump)) # shield bump or bomb two socket karakoro into the holes
            Location(dungeon=0).add(DungeonChest(0x307)).connect(north_potbutton_room, OR(BOMB, r.shield_bump)) # shield bump or bomb four socket karakoro into the holes
            
        self.entrance = entrance
        self.final_room = boss


class NoDungeonColor:
    def __init__(self, options, world_setup, r):
        entrance = Location(dungeon=0)
        boss = Location(dungeon=0).connect(entrance, r.boss_requirements[world_setup.boss_mapping[8]])
        boss.add(TunicFairy(0), TunicFairy(1))

        self.entrance = entrance
