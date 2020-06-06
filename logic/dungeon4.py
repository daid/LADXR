from .requirements import *
from .location import Location
from locations import *


class Dungeon4:
    def __init__(self):
        entrance = Location(4)
        entrance.add(DungeonChest(0x179))  # stone slab chest
        entrance.add(DungeonChest(0x16A))  # map chest
        right_of_entrance = Location(4).add(DungeonChest(0x178)).connect(entrance, AND(SHIELD, attack_hookshot)) # 2 zol 1 spike enemy
        Location(4).add(DungeonChest(0x17B)).connect(right_of_entrance, SWORD) # room with key chest
        Location(4).add(DungeonChest(0x171)).add(DungeonChest(0x165)).connect(entrance, AND(FEATHER, PEGASUS_BOOTS, BOMB))  # 2 key chests on the right.

        double_locked_room = Location(4).connect(right_of_entrance, KEY4)
        after_double_lock = Location(4).connect(double_locked_room, AND(KEY4, OR(FEATHER, FLIPPERS)))
        Location(4).add(DungeonChest(0x175)).connect(after_double_lock, FLIPPERS)
        before_miniboss = Location(4).connect(after_double_lock, AND(FEATHER, PEGASUS_BOOTS, KEY4))
        Location(4).add(DroppedKey(0x169)).connect(before_miniboss, FLIPPERS)  # key that drops in the hole and needs swim to get
        Location(4).add(DungeonChest(0x16E)).connect(before_miniboss, FLIPPERS)  # chest with 50 rupees
        before_miniboss.add(DungeonChest(0x16D))  # gel chest
        before_miniboss.add(DungeonChest(0x168))  # key chest near the puzzle
        miniboss = Location(4).connect(before_miniboss, AND(KEY4, POWER_BRACELET))
        miniboss.add(DungeonChest(0x160))  # flippers chest

        to_the_nightmare_key = Location(4).connect(before_miniboss, FLIPPERS)  # 5 symbol puzzle
        to_the_nightmare_key.add(DungeonChest(0x176))

        boss = Location(4).connect(before_miniboss, AND(attack_hookshot, FLIPPERS, KEY4))

        self.entrance = entrance

