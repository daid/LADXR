from .requirements import *
from .location import Location
from locations import *


class Dungeon7:
    def __init__(self):
        entrance = Location(7)
        Location(7).add(DroppedKey(0x210)).connect(entrance, attack)
        topright_pillar_area = Location(7).connect(entrance, KEY7)
        topright_pillar = Location(7).add(DungeonChest(0x212)).connect(topright_pillar_area, POWER_BRACELET)  # map chest
        topright_pillar_area.add(DungeonChest(0x209))  # stone slab chest can be reached by dropping down a hole
        bottomright_pillar = Location(7).add(DungeonChest(0x211)).connect(topright_pillar_area, OR(FEATHER, attack_hookshot), OR(SHIELD, POWER_BRACELET, attack_hookshot))  # compass chest; bracelet can be used in combination with ball; path without feather with hitting switch by falling on the raised blocks
        # Most of the dungeon can be accessed at this point.
        bottomleftF2_area = Location(7).add(DungeonChest(0x212)).connect(topright_pillar_area, attack_hookshot)  # area with hinox
        bottomleftF2_area.add(DungeonChest(0x224))  # nightmare key after the miniboss
        bottomleftF2_area.add(DungeonChest(0x21A))  # mirror shield chest

        final_pillar_area = Location(7).add(DungeonChest(0x21C)).connect(bottomleftF2_area, BOMB, HOOKSHOT)  # chest that needs to spawn to get to the last pillar
        final_pillar = Location(7).connect(final_pillar_area, POWER_BRACELET) # decouple chest from pillar

        boss = Location(7).add(DungeonChest(0x220)).connect(final_pillar, NIGHTMARE_KEY7) # 100 rupee chest / medicine chest (DX) behind boss door

        self.entrance = entrance
