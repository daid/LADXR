from .requirements import *

entrance = Location(7)
Location(7).add(DroppedKey(0x210)).connect(entrance, attack)
post_first_door = Location(7).connect(entrance, KEY7)
topright_pillar = Location(7).add(DungeonChest(0x212)).connect(post_first_door, POWER_BRACELET)  # map chest
topright_pillar.add(DungeonChest(0x209))  # stone slab chest can be reached by dropping down a hole
bottomright_pillar = Location(7).add(DungeonChest(0x211)).connect(topright_pillar, FEATHER)  # compass chest
# Most of the dungeon can be accessed at this point.
bottomright_pillar.add(DroppedKey(0x21B))
bottomright_pillar.add(DungeonChest(0x224))  # nightmare key after the miniboss
bottomright_pillar.add(DungeonChest(0x21A))  # mirror shield chest

final_pillar = Location(7).add(DroppedKey(0x21C)).connect(bottomright_pillar, HOOKSHOT)  # chest that needs to spawn to get to the last pillar
final_pillar.add(DungeonChest(0x220))  # 100 rupee chest

boss = Location(7).connect(final_pillar, NIGHTMARE_KEY7)
