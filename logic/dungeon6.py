from .requirements import *

entrance = Location(6)
Location(6).add(DungeonChest(0x1CF)).connect(entrance, BOMB, BOW)
Location(6).add(DungeonChest(0x1C9)).connect(entrance, COUNT(POWER_BRACELET, 2))

# Power bracelet chest
Location(6).add(DungeonChest(0x1CE)).connect(entrance, AND(BOMB, FEATHER))

# left side
left_side = Location(6).add(DungeonChest(0x1C0)).add(DungeonChest(0x1B9)).connect(entrance, BOMB)
left_side2 = Location(6).add(DungeonChest(0x1B3), DroppedKey(0x1B4)).connect(left_side, POWER_BRACELET)
top_left = Location(6).add(DungeonChest(0x1B0)).connect(left_side2, COUNT(POWER_BRACELET, 2))
top_left.add(Chest(0x06C))  # seashell chest in raft game

# right side
to_miniboss = Location(6).connect(entrance, KEY6)
miniboss = Location(6).connect(to_miniboss, BOMB)
lower_right_side = Location(6).add(DungeonChest(0x1D1), DungeonChest(0x1BE)).connect(to_miniboss, POWER_BRACELET)

center_1 = Location(6).add(DroppedKey(0x1C3)).connect(miniboss, AND(COUNT(POWER_BRACELET, 2), FEATHER))
center_2_and_upper_right_side = Location(6).add(DungeonChest(0x1B1)).connect(center_1, KEY6)
boss_key = Location(6).add(DungeonChest(0x1B6)).connect(center_2_and_upper_right_side, AND(KEY6, HOOKSHOT))

boss = Location(6).connect(center_1, NIGHTMARE_KEY6)