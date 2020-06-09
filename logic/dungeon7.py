from .requirements import *
from .location import Location
from locations import *


class Dungeon7:
    def __init__(self, options):
        entrance = Location(7)
        Location(7).add(DroppedKey(0x210)).connect(entrance, attack)
        topright_pillar_area = Location(7).connect(entrance, KEY7)
        Location(7).add(OwlStatue(0x216)).connect(topright_pillar_area, STONE_BEAK7)
        topright_pillar = Location(7).add(DungeonChest(0x212)).connect(topright_pillar_area, POWER_BRACELET)  # map chest
        Location(7).add(OwlStatue(0x204)).connect(topright_pillar, STONE_BEAK7)
        topright_pillar_area.add(DungeonChest(0x209))  # stone slab chest can be reached by dropping down a hole
        bottomright_pillar = Location(7).add(DungeonChest(0x211)).connect(topright_pillar_area, AND(OR(FEATHER, attack_hookshot), OR(SHIELD, POWER_BRACELET, attack_hookshot)))  # compass chest; bracelet can be used in combination with ball; path without feather with hitting switch by falling on the raised blocks
        bottomright_pillar.add(DroppedKey(0x21B), DungeonChest(0x201))  # key at the hinox, and seashell chest on left F1 ledge
        # Most of the dungeon can be accessed at this point.
        bottomleftF2_area = Location(7).connect(topright_pillar_area, attack_hookshot)  # area with hinox
        Location(7).add(OwlStatue(0x21C)).connect(bottomleftF2_area, STONE_BEAK7)
        bottomleftF2_area.add(DungeonChest(0x224))  # nightmare key after the miniboss
        bottomleftF2_area.add(DungeonChest(0x21A), DungeonChest(0x204))  # mirror shield chest, and chest on the F1 right ledge

        final_pillar_area = Location(7).add(DungeonChest(0x21C)).connect(bottomleftF2_area, AND(BOMB, HOOKSHOT))  # chest that needs to spawn to get to the last pillar
        final_pillar = Location(7).connect(final_pillar_area, POWER_BRACELET) # decouple chest from pillar

        boss = Location(7).add(DungeonChest(0x220)).connect(final_pillar, NIGHTMARE_KEY7) # 100 rupee chest / medicine chest (DX) behind boss door

        self.entrance = entrance
