from .requirements import *
from .location import Location
from locations import *


class Dungeon3:
    def __init__(self):
        entrance = Location(3)
        Location(3).add(DungeonChest(0x153)).connect(entrance, PEGASUS_BOOTS) # Right side reverse eye
        area2 = Location(3).connect(entrance, POWER_BRACELET)
        Location(3).add(DungeonChest(0x151)).connect(area2, attack_hookshot)  # First chest with key
        area2.add(DungeonChest(0x14F))  # Second chest with slime
        area3 = Location(3).connect(area2, OR(attack_powder, PEGASUS_BOOTS)) # need to kill slimes to continue or pass through left path
        Location(3).add(DungeonChest(0x14E)).connect(area3, AND(PEGASUS_BOOTS, attack_skeleton))  # 3th chest requires killing the slime behind the crystal pillars

        # now we can go 4 directions,
        area_up = Location(3).connect(area3, KEY3)
        Location(3).add(DroppedKey(0x154)).connect(area_up, attack_skeleton) # north key drop

        area_left = Location(3).connect(area3, KEY3)
        Location(3).add(FlyingKey(0x155)).connect(area_left, AND(attack_hookshot, FEATHER)) # west key drop

        area_down = Location(3).connect(area3, KEY3)
        Location(3).add(DroppedKey(0x155)).connect(area_down, attack_no_boomerang) # south keydrop

        area_right = Location(3).connect(area3, KEY3)  # We enter the top part of the map here.
        Location(3).add(DroppedKey(0x14D)).connect(area_right, attack)  # key after the stairs.

        Location(3).add(DungeonChest(0x147)).connect(area_right, AND(BOMB, FEATHER, PEGASUS_BOOTS))  # nightmare key chest
        Location(3).add(DungeonChest(0x146)).connect(area_right, BOMB)  # boots after the miniboss
        compass_chest = Location(3).add(DungeonChest(0x142)).connect(area_right, OR(SWORD, BOMB, AND(SHIELD, attack_powder))) # bomb only activates with sword, bomb or shield
        Location(3).add(DroppedKey(0x141)).connect(compass_chest, BOMB) # 3 bombite room
        Location(3).add(DroppedKey(0x148)).connect(area_right, attack_no_boomerang) # 2 zol 2 owl drop key
        Location(3).add(DungeonChest(0x144)).connect(area_right, attack_skeleton)  # map chest

        towards_boss1 = Location(3).connect(area_right, KEY3)
        towards_boss2 = Location(3).connect(towards_boss1, KEY3)
        towards_boss3 = Location(3).connect(towards_boss2, KEY3)
        towards_boss4 = Location(3).connect(towards_boss3, KEY3)

        # Just the whole area before the boss, requirements for the boss itself and the rooms before it are the same.
        pre_boss = Location(3).connect(towards_boss4, AND(attack_no_boomerang, FEATHER, PEGASUS_BOOTS))
        pre_boss.add(DroppedKey(0x15B))

        boss = Location(3).connect(pre_boss, NIGHTMARE_KEY3)
        # TODO Set as target
        # TODO Check two raised blocks chests (Should be 0x150 and 0x14C? Req are similar to 0x154)

        self.entrance = entrance
