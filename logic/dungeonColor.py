from .requirements import *
from .location import Location
from locations.all import *


class DungeonColor:
    def __init__(self, options, world_setup, r):
        entrance = Location("D0 Entrance", dungeon=0)
        room2 = Location(dungeon=0).connect(entrance, r.attack_hookshot_powder, id="lf")
        room2.add(DungeonChest(0x314))  # key
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=0).add(OwlStatue(0x308), OwlStatue(0x30F)).connect(room2, STONE_BEAK0, id="lg")
        room2_weapon = Location(dungeon=0).connect(room2, AND(r.attack_hookshot, POWER_BRACELET), id="lh")
        room2_weapon.add(DungeonChest(0x311))  # stone beak
        room2_lights = Location(dungeon=0).connect(room2, OR(r.attack_hookshot, SHIELD), id="li")
        room2_lights.add(DungeonChest(0x30F))  # compass chest
        room2_lights.add(DroppedKey(0x308))

        miniboss_room1 = Location("D0 Miniboss Room 1", dungeon=0).connect(room2, AND(KEY0, FOUND(KEY0, 3)), id="lj")
        Location(dungeon=0).connect(miniboss_room1, r.miniboss_requirements[world_setup.miniboss_mapping["c2"]], id="lk").add(DungeonChest(0x302))  # nightmare key after slime mini boss
        miniboss_room2 = Location("D0 Miniboss Room 2", dungeon=0).connect(room2, AND(KEY0, FOUND(KEY0, 2)), id="ll")
        room3 = Location("D0 After Miniboss 2", dungeon=0).connect(miniboss_room2, r.miniboss_requirements[world_setup.miniboss_mapping["c1"]], id="lm") # After the miniboss
        room4 = Location(dungeon=0).connect(room3, POWER_BRACELET, id="ln")  # need to lift a pot to reveal button
        room4.add(DungeonChest(0x306))  # map
        room4karakoro = Location(dungeon=0).add(DroppedKey(0x307)).connect(room4, AND(r.attack_hookshot, POWER_BRACELET), id="lo")  # require item to knock Karakoro enemies into shell
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=0).add(OwlStatue(0x30A)).connect(room4, STONE_BEAK0, id="lp")
        room5 = Location("D0 After 3x3", dungeon=0).connect(room4, OR(r.attack_hookshot, SHIELD), id="lq") # lights room
        room6 = Location("D0 Room Before Boss", dungeon=0).connect(room5, AND(KEY0, FOUND(KEY0, 3)), id="lr") # room with switch and nightmare door
        pre_boss = Location("D0 Outside Boss Door", dungeon=0).connect(room6, OR(r.hit_switch, AND(PEGASUS_BOOTS, FEATHER)), id="ls")  # before the boss, require item to hit switch or jump past raised blocks
        boss_room = Location("D0 Boss Room", dungeon=0).connect(pre_boss, NIGHTMARE_KEY0, id="lt")
        boss = Location(dungeon=0).connect(boss_room, r.boss_requirements[world_setup.boss_mapping[8]], id="lu")
        boss.add(TunicFairy(0), TunicFairy(1))

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            room2.connect(entrance, r.throw_pot, id="lv") # throw pots at enemies
            room2_weapon.connect(room2, r.attack_hookshot_no_bomb, id="lw") # knock the karakoro into the pit without picking them up. 
            pre_boss.connect(room6, r.tight_jump, id="lx") # before the boss, jump past raised blocks without boots

        if options.logic == 'hell':
            room2_weapon.connect(room2, r.attack_hookshot, id="ly") # also have a bomb as option to knock the karakoro into the pit without bracelet 
            room2_weapon.connect(room2, r.shield_bump, id="lz") # shield bump karakoro into the holes
            room4karakoro.connect(room4, r.shield_bump, id="m0") # shield bump karakoro into the holes
            
        self.entrance = entrance
        self.final_room = boss


class NoDungeonColor:
    def __init__(self, options, world_setup, r):
        entrance = Location(dungeon=0)
        boss = Location(dungeon=0).connect(entrance, r.boss_requirements[world_setup.boss_mapping[8]], id="m1")
        boss.add(TunicFairy(0), TunicFairy(1))

        self.entrance = entrance
