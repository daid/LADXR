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
        camo_pit_room = Location("D0 Camo Pit Room", dungeon=0)
        bone_putter_room = Location("D0 Bone Putter Room", dungeon=0)
        bone_putter_room_chest3 = Location(dungeon=0).add(DungeonChest(0x314)) # small key
        main_room_drop1 = Location(dungeon=0).add(DroppedKey(0x308)) # small key
        main_room_owl1 = Location(dungeon=0).add(OwlStatue(0x30F)) # hint
        main_room_owl2 = Location(dungeon=0).add(OwlStatue(0x308)) # hint
        #TODO: rupee_room = Location("D0 Secret Rupee Room", dungeon=0)
        #TODO: rupee_room_jackpot = Location("D0 Rupee Jackpot", dungeon=0) # 140 rupees
        ne_miniboss = Location("D0 NE Miniboss", dungeon=0)
        ne_miniboss_chest4 = Location(dungeon=0).add(DungeonChest(0x302)) # nightmare key
        center_miniboss = Location("D0 Center Miniboss", dungeon=0)
        button_room = Location("D0 Hidden Button Room", dungeon=0)
        button_north = Location("D0 Bullshit Room", dungeon=0)
        north_room_chest5 = Location(dungeon=0).add(DungeonChest(0x306)) # map
        north_room_drop2 = Location(dungeon=0).add(DroppedKey(0x307)) # small key
        button_west = Location("D0 3x3 Puzzle Room", dungeon=0)
        west_room_owl3 = Location(dungeon=0).add(OwlStatue(0x30A)) # hint
        fourzol_room = Location("D0 Four Zol Room", dungeon=0)
        switch_room = Location("D0 Room Before Boss", dungeon=0)
        pre_boss = Location("D0 Outside Boss Door", dungeon=0)
        boss_room = Location("D0 Boss Room", dungeon=0)
        fairy_rewards = Location("D0 Fairy Room", dungeon=0).add(TunicFairy(0), TunicFairy(1)) # red tunic, blue tunic

        # owl statues
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            main_room.connect(main_room_owl1, STONE_BEAK0, back=False)
            main_room.connect(main_room_owl2, STONE_BEAK0, back=False)
            button_west.connect(west_room_owl3, STONE_BEAK0, back=False)

        # connections
        entrance.connect(main_room, AND(r.enemy_requirements["COLOR_GHOUL_GREEN"], r.enemy_requirements["COLOR_GHOUL_RED"]), back=False)
        main_room.connect((main_room_chest1, main_room_drop1), r.hit_switch_color, back=False)
        main_room.connect(main_room_chest2, AND(POWER_BRACELET, r.attack_hookshot), back=False) #NOTE: not using enemy requirements here
        main_room.connect(camo_pit_room, back=False)
        main_room.connect(ne_miniboss, FOUND(KEY0, 3), back=False)
        main_room.connect(center_miniboss, FOUND(KEY0, 2), back=False)
        #TODO: main_room.connect(rupee_room, BOMB, back=False)
        #TODO: rupee_room.connect(rupee_room_jackpot, back=False)
        camo_pit_room.connect(bone_putter_room, AND(r.enemy_requirements["COLOR_GHOUL_GREEN"], r.enemy_requirements["COLOR_GHOUL_RED"]), back=False) #NOTE: can also shield bump, but no implication to logic - would be hell
        bone_putter_room.connect((main_room, bone_putter_room_chest3), back=False)
        ne_miniboss.connect(ne_miniboss_chest4, r.miniboss_requirements[world_setup.miniboss_mapping["c2"]], back=False)
        center_miniboss.connect(button_room, r.miniboss_requirements[world_setup.miniboss_mapping["c1"]], back=False)
        button_room.connect((button_north, button_west), POWER_BRACELET, back=False)
        button_north.connect(north_room_chest5, AND(r.enemy_requirements["ZOL"], r.enemy_requirements["HIDING_ZOL"]), back=False)
        button_north.connect(north_room_drop2, AND(r.attack_hookshot, POWER_BRACELET), back=False) #NOTE: not using enemy requirements here
        button_west.connect(fourzol_room, r.hit_switch_color, back=False)
        fourzol_room.connect(switch_room, FOUND(KEY0, 3), back=False)
        switch_room.connect(pre_boss, OR(r.hit_switch, AND(PEGASUS_BOOTS, FEATHER)), back=False)
        pre_boss.connect(boss_room, NIGHTMARE_KEY0, back=False)
        boss_room.connect(fairy_rewards, r.boss_requirements[world_setup.boss_mapping[8]], back=False)

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            entrance.connect(main_room, r.throw_pot, back=False) # throw pots to kill camo goblin
            main_room.connect(main_room_chest2, r.attack_hookshot_no_bomb, back=False) # knock the karakoro into the pit without picking them up
            camo_pit_room.connect(bone_putter_room, r.throw_pot, back=False) # throw pots to kill camo goblin
            button_north.connect(north_room_chest5, r.throw_pot, back=False) # throw pots to kill zols
            switch_room.connect(pre_boss, r.tight_jump, back=False) # before the boss, jump past raised blocks with only feather

        if options.logic == 'hell':
            main_room.connect(main_room_chest2, OR(BOMB, r.shield_bump), back=False) # shield bump or bomb two socket karakoro into the holes
            button_north.connect(north_room_drop2, OR(BOMB, r.shield_bump), back=False) # shield bump or bomb four socket karakoro into the holes
            
        self.entrance = entrance
        self.final_room = fairy_rewards

class NoDungeonColor:
    def __init__(self, options, world_setup, r):

        # locations
        entrance = Location("D0 Entrance", dungeon=0)
        boss_room = Location("D0 Boss Room", dungeon=0)
        fairy_rewards = Location("D0 Fairy Room", dungeon=0).add(TunicFairy(0), TunicFairy(1))
        # connections
        entrance.connect(boss_room, back=r.boss_requirements[world_setup.boss_mapping[8]])
        boss_room.connect(fairy_rewards, r.boss_requirements[world_setup.boss_mapping[8]], back=False)

        self.entrance = entrance
