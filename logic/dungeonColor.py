from .requirements import *
from .location import Location
from locations import *


class DungeonColor:
    def __init__(self, options):
        entrance = Location(9)
        room2 = Location(9).connect(entrance, attack_hookshot_powder)
        room2.add(DungeonChest(0x314))  # key
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(9).add(OwlStatue(0x308), OwlStatue(0x30F)).connect(room2, STONE_BEAK9)
        room2_weapon = Location(9).connect(room2, attack_hookshot)
        room2_weapon.add(DungeonChest(0x311))  # stone beak
        room2_lights = Location(9).connect(room2, OR(attack_hookshot, SHIELD))
        room2_lights.add(DungeonChest(0x30F))  # compass chest
        room2_lights.add(DroppedKey(0x308))

        Location(9).connect(room2, AND(KEY9, FOUND(KEY9, 3), MAGIC_POWDER)).add(DungeonChest(0x302))  # nightmare key after slime mini boss
        room3 = Location(9).connect(room2_weapon, AND(KEY9, FOUND(KEY9, 2))) # After the miniboss
        room4 = Location(9).connect(room3, POWER_BRACELET)  # need to lift a pot to reveal button
        room4.add(DungeonChest(0x306))  # map
        room4.add(DroppedKey(0x307))
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(9).add(OwlStatue(0x30A)).connect(room4, STONE_BEAK9)
        room5 = Location(9).connect(room4, AND(KEY9, FOUND(KEY9, 3)))  # before the boss
        boss = Location(9).connect(room5, AND(NIGHTMARE_KEY9, attack_no_bomb))
        boss.add(TunicFairy(0), TunicFairy(1))
        
        if options.logic == 'hard' or options.logic == 'glitched':
            room2.connect(entrance, POWER_BRACELET) # throw pots at enemies
                        
        self.entrance = entrance
