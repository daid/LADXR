from .requirements import *

entrance = Location(1)
entrance.add(DungeonChest(0x113), DungeonChest(0x115), DungeonChest(0x10E))
Location(1).add(DroppedKey(0x116), DungeonChest(0x10D)).connect(entrance, attack)
Location(1).add(DungeonChest(0x114)).connect(entrance, attack_skeleton)
Location(1).add(DungeonChest(0x10C)).connect(entrance, BOMB)
dungeon1_upper_left = Location(1).connect(entrance, KEY1)
Location(1).add(DungeonChest(0x11D)).connect(dungeon1_upper_left, AND(SHIELD, attack))  # feather location, behind spike enemies
Location(1).add(DungeonChest(0x108)).connect(entrance, AND(FEATHER, KEY1)) # boss key
dungeon1_right_side = Location(1).connect(entrance, KEY1)
Location(1).add(DungeonChest(0x10A)).connect(dungeon1_right_side, attack) # three of a kind
dungeon1_miniboss = Location(1).connect(dungeon1_right_side, FEATHER)
dungeon1_boss = Location(1).connect(dungeon1_miniboss, NIGHTMARE_KEY1)
Location(1).connect(dungeon1_boss, attack) #TODO: goal room
