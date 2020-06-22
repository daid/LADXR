from .requirements import *
from .location import Location
from locations import *


class Dungeon7:
    def __init__(self, options):
        entrance = Location(7)
        Location(7).add(DroppedKey(0x210)).connect(entrance, attack_hookshot_powder)
        topright_pillar_area = Location(7).connect(entrance, KEY7)
        Location(7).add(OwlStatue(0x216)).connect(topright_pillar_area, STONE_BEAK7)
        topright_pillar = Location(7).add(DungeonChest(0x212)).connect(topright_pillar_area, POWER_BRACELET)  # map chest
        Location(7).add(OwlStatue(0x204)).connect(topright_pillar_area, STONE_BEAK7)
        topright_pillar_area.add(DungeonChest(0x209))  # stone slab chest can be reached by dropping down a hole
        three_of_a_kind_north = Location(7).add(DungeonChest(0x211)).connect(topright_pillar_area, OR(attack_hookshot, AND(FEATHER, SHIELD)))  # compass chest; path without feather with hitting switch by falling on the raised blocks. No bracelet because ball does not reset
        bottomleftF2_area = Location(7).add(DungeonChest(0x201)).connect(topright_pillar_area, attack_hookshot)  # area with hinox
        Location(7).add(DroppedKey(0x21B)).connect(bottomleftF2_area, attack_hookshot) # hinox drop key
        # Most of the dungeon can be accessed at this point.
        bottomleft_owl = Location(7).add(OwlStatue(0x21C)).connect(bottomleftF2_area, AND(BOMB, STONE_BEAK7))
        nightmare_key = Location(7).add(DungeonChest(0x224)).connect(bottomleftF2_area, attack_no_bomb) # nightmare key after the miniboss
        bottomleftF2_area.add(DungeonChest(0x21A))  # mirror shield chest
        toprightF1_chest = Location(7).add(DungeonChest(0x204)).connect(bottomleftF2_area, attack_hookshot)  # chest on the F1 right ledge. Added attack_hookshot since 1 requirement is needed
        final_pillar_area = Location(7).add(DungeonChest(0x21C)).connect(bottomleftF2_area, AND(BOMB, HOOKSHOT))  # chest that needs to spawn to get to the last pillar
        final_pillar = Location(7).connect(final_pillar_area, POWER_BRACELET) # decouple chest from pillar

        pre_boss = Location(7).connect(final_pillar, NIGHTMARE_KEY7) 
        beamos_horseheads = Location(7).connect(pre_boss, POWER_BRACELET) # 100 rupee chest / medicine chest (DX) behind boss door
        boss = Location(7).add(HeartContainer(0x2E8)).connect(pre_boss, AND(OR(MAGIC_ROD, SWORD, HOOKSHOT), SHIELD))
            
        if options.logic == 'glitched':
            topright_pillar_area.connect(entrance, FEATHER) # superjump in the center to get on raised blocks, superjump in switch room to right side to walk down
            toprightF1_chest.connect(entrance, FEATHER) # superjump through center and from F1 switch room
            final_pillar_area.connect(bottomleftF2_area, attack_hookshot) # sideways block push to get to the chest and pillar
            bottomleft_owl.connect(bottomleftF2_area, attack_hookshot) # sideways block push to get to the owl statue (attack_hookshot is already implied from bottomleftF2_area)
            final_pillar.connect(bottomleftF2_area, BOMB) # bomb trigger pillar
            pre_boss.connect(final_pillar, FEATHER) # superjump on top of goomba to extend superjump to boss door plateau
            
        self.entrance = entrance
