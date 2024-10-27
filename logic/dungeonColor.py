from .requirements import *
from .location import Location
from locations.all import *


class DungeonColor:
    def __init__(self, options, world_setup, r):
        entrance = Location("D0 Entrance", dungeon=0)
        room2 = Location(dungeon=0).connect(entrance, AND(r.enemy_requirements["GREEN_CAMO_MOBLIN"], r.enemy_requirements["RED_CAMO_MOBLIN"]))
        room2.add(DungeonChest(0x314))  # key
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=0).add(OwlStatue(0x308), OwlStatue(0x30F)).connect(room2, STONE_BEAK0)
        room2_weapon = Location(dungeon=0).connect(room2, AND(r.attack_hookshot, POWER_BRACELET)) # throw karakoro in holes
        room2_weapon.add(DungeonChest(0x311))  # stone beak
        room2_lights = Location(dungeon=0).connect(room2, OR(r.hit_switch, SHIELD))
        room2_lights.add(DungeonChest(0x30F))  # compass chest
        room2_lights.add(DroppedKey(0x308))

        miniboss_room1 = Location("D0 Miniboss Room 1", dungeon=0).connect(room2, AND(KEY0, FOUND(KEY0, 3)))
        Location(dungeon=0).connect(miniboss_room1, r.miniboss_requirements[world_setup.miniboss_mapping["c2"]]).add(DungeonChest(0x302))  # nightmare key after slime mini boss
        miniboss_room2 = Location("D0 Miniboss Room 2", dungeon=0).connect(room2, AND(KEY0, FOUND(KEY0, 2)))
        room3 = Location("D0 After Miniboss 2", dungeon=0).connect(miniboss_room2, r.miniboss_requirements[world_setup.miniboss_mapping["c1"]]) # After the miniboss
        room4 = Location(dungeon=0).connect(room3, POWER_BRACELET)  # need to lift a pot to reveal button
        room4_map_chest = Location(dungeon=0).add(DungeonChest(0x306)).connect(room4, AND(r.enemy_requirements["RED_ZOL"], r.enemy_requirements["GREEN_ZOL"]))
        room4karakoro = Location(dungeon=0).add(DroppedKey(0x307)).connect(room4, AND(r.attack_hookshot, POWER_BRACELET))  # require item to knock Karakoro enemies into shell
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=0).add(OwlStatue(0x30A)).connect(room4, STONE_BEAK0)
        room5 = Location("D0 After 3x3", dungeon=0).connect(room4, OR(r.hit_switch, SHIELD)) # lights room
        room6 = Location("D0 Room Before Boss", dungeon=0).connect(room5, AND(KEY0, FOUND(KEY0, 3))) # room with switch and nightmare door
        pre_boss = Location("D0 Outside Boss Door", dungeon=0).connect(room6, OR(r.hit_switch, AND(PEGASUS_BOOTS, FEATHER)))  # before the boss, require item to hit switch or jump past raised blocks
        boss_room = Location("D0 Boss Room", dungeon=0).connect(pre_boss, NIGHTMARE_KEY0)
        boss = Location(dungeon=0).connect(boss_room, r.boss_requirements[world_setup.boss_mapping[8]])
        boss.add(TunicFairy(0), TunicFairy(1))

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            room2.connect(entrance, r.throw_pot) # throw pots at enemies
            room2_weapon.connect(room2, r.attack_hookshot_no_bomb) # knock the karakoro into the pit without picking them up. 
            pre_boss.connect(room6, r.tight_jump) # before the boss, jump past raised blocks without boots

        if options.logic == 'hell':
            room2_weapon.connect(room2, r.attack_hookshot) # also have a bomb as option to knock the karakoro into the pit without bracelet 
            room2_weapon.connect(room2, r.shield_bump) # shield bump karakoro into the holes
            room4karakoro.connect(room4, r.shield_bump) # shield bump karakoro into the holes
            
        self.entrance = entrance
        self.final_room = boss


class NoDungeonColor:
    def __init__(self, options, world_setup, r):
        entrance = Location(dungeon=0)
        boss = Location(dungeon=0).connect(entrance, r.boss_requirements[world_setup.boss_mapping[8]])
        boss.add(TunicFairy(0), TunicFairy(1))

        self.entrance = entrance
