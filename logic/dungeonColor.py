from .requirements import *
from .location import Location
from locations import *


class DungeonColor:
    def __init__(self):
        entrance = Location(9)
        room2 = Location(9).connect(entrance, OR(attack, HOOKSHOT))
        room2.add(DungeonChest(0x30F))  # compass chest
        room2.add(DungeonChest(0x311))  # stone beak
        room2.add(DungeonChest(0x314))  # key
        room2.add(DroppedKey(0x308))

        Location(9).connect(room2, AND(KEY9, SWORD)).add(DungeonChest(0x302))  # nightmare key after slime mini boss
        room3 = Location(9).connect(room2, KEY9) # After the miniboss
        room4 = Location(9).connect(room3, POWER_BRACELET)  # need to lift a pot to reveal button
        room4.add(DungeonChest(0x306))  # map
        room4.add(DroppedKey(0x307))
        room5 = Location(9).connect(room4, KEY9)  # before the boss
        boss = Location(9).connect(room5, NIGHTMARE_KEY9)
        boss.add(TunicFairy())

        self.entrance = entrance
