from .requirements import *

#TODO: In this dungeon you can waste a key by going to the miniboss, which is useless and can be bypassed.
#       Logic does not account for you wasting this key (maybe remove the keyblock?)

entrance = Location(5)
Location(5).add(DungeonChest(0x1A0)).connect(entrance, HOOKSHOT)
compass = Location(5).add(DungeonChest(0x19E)).connect(entrance, OR(attack, HOOKSHOT))
Location(5).add(DroppedKey(0x181)).connect(compass, AND(SWORD, FEATHER))

area2 = Location(5).add(DungeonChest(0x198)).connect(entrance, KEY5)  # map chest
Location(5).add(DungeonChest(0x197)).connect(area2, HOOKSHOT)  # key chest on the left
after_stalfos = Location(5).add(DungeonChest(0x196)).connect(area2, AND(SWORD, BOMB)) # Need to defeat master stalfos once for this empty chest
Location(5).add(DungeonChest(0x18E), DungeonChest(0x188), DungeonChest(0x18F)).connect(after_stalfos, AND(FEATHER, HOOKSHOT))
stone_tablet = Location(5).add(DungeonChest(0x183)).connect(after_stalfos, AND(FEATHER, POWER_BRACELET))  # stone tablet
Location(5).add(DungeonChest(0x186)).connect(after_stalfos, AND(FLIPPERS, HOOKSHOT))  # nightmare key
boss = Location(5).connect(after_stalfos, AND(FEATHER, HOOKSHOT))

# When we can reach the stone tablet chest, we can also reach the final location of master stalfos
stone_tablet.add(HookshotDrop())
