from .requirements import *
from .location import Location
from locations import *


class Dungeon8:
    def __init__(self):
        entrance = Location(8)
        entrance_up = Location(8).add(DungeonChest(0x24F)).connect(entrance, FEATHER)
        entrance_left_right = Location(8).connect(entrance, attack)

        # left side
        entrance_left_right.add(DungeonChest(0x24D))
        Location(8).add(DungeonChest(0x255), DungeonChest(0x25C), DroppedKey(0x24C)).connect(entrance_left_right, FEATHER)  # stuff around lvl1 miniboss
        Location(8).add(DungeonChest(0x246)).connect(entrance_left_right, MAGIC_ROD)  # key chest that spawns after creating fire
        # right side
        Location(8).add(DungeonChest(0x259)).connect(entrance_left_right, POWER_BRACELET)  # chest with slime
        bottom_right = Location(8).add(DroppedKey(0x25A), DungeonChest(0x25F)).connect(entrance_up, BOMB)

        lower_center = Location(8).connect(entrance_up, KEY8)
        upper_center = Location(8).connect(lower_center, KEY8)
        upper_center.add(DroppedKey(0x23E))
        middle_center_1 = Location(8).connect(upper_center, BOMB)
        middle_center_2 = Location(8).connect(middle_center_1, KEY8)
        middle_center_3 = Location(8).connect(middle_center_2, KEY8)
        miniboss = Location(8).connect(middle_center_3, KEY8)
        miniboss.add(DungeonChest(0x237))

        up_left = Location(8).connect(upper_center, KEY8)
        up_left.add(DungeonChest(0x240))
        up_left.add(DungeonChest(0x23D))
        up_left.add(HeartPiece(0x000))  # Outside the dungeon on the platform
        Location(8).add(DroppedKey(0x241)).connect(up_left, BOW)
        Location(8).add(DungeonChest(0x23A)).connect(up_left, HOOKSHOT)

        nightmare_key = Location(8).add(DungeonChest(0x232)).connect(entrance_up, MAGIC_ROD)

        # Bombing from the center dark rooms to the left so you can access more keys.
        middle_center_2.connect(up_left, AND(BOMB, FEATHER), one_way=True)

        self.entrance = entrance
