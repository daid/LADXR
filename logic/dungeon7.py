from .requirements import *
from .location import Location
from locations.all import *


class Dungeon7:
    def __init__(self, options, world_setup, r):
        entrance = Location(7)
        first_key = Location(7).add(DroppedKey(0x210)).connect(entrance, r.attack_hookshot_powder)
        topright_pillar_area = Location(7).connect(entrance, KEY7)
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(7).add(OwlStatue(0x216)).connect(topright_pillar_area, STONE_BEAK7)
        topright_pillar = Location(7).add(DungeonChest(0x212)).connect(topright_pillar_area, POWER_BRACELET)  # map chest
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(7).add(OwlStatue(0x204)).connect(topright_pillar_area, STONE_BEAK7)
        topright_pillar_area.add(DungeonChest(0x209))  # stone slab chest can be reached by dropping down a hole
        three_of_a_kind_north = Location(7).add(DungeonChest(0x211)).connect(topright_pillar_area, OR(r.attack_hookshot, AND(FEATHER, SHIELD)))  # compass chest; path without feather with hitting switch by falling on the raised blocks. No bracelet because ball does not reset
        bottomleftF2_area = Location(7).add(DungeonChest(0x201)).connect(topright_pillar_area, r.attack_hookshot)  # area with hinox
        Location(7).add(DroppedKey(0x21B)).connect(bottomleftF2_area, r.attack_hookshot) # hinox drop key
        # Most of the dungeon can be accessed at this point.
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            bottomleft_owl = Location(7).add(OwlStatue(0x21C)).connect(bottomleftF2_area, AND(BOMB, STONE_BEAK7))
        nightmare_key = Location(7).add(DungeonChest(0x224)).connect(bottomleftF2_area, r.miniboss_requirements[world_setup.miniboss_mapping[6]]) # nightmare key after the miniboss
        bottomleftF2_area.add(DungeonChest(0x21A))  # mirror shield chest
        toprightF1_chest = Location(7).add(DungeonChest(0x204)).connect(bottomleftF2_area, r.attack_hookshot)  # chest on the F1 right ledge. Added attack_hookshot since 1 requirement is needed
        final_pillar_area = Location(7).add(DungeonChest(0x21C)).connect(bottomleftF2_area, AND(BOMB, HOOKSHOT))  # chest that needs to spawn to get to the last pillar
        final_pillar = Location(7).connect(final_pillar_area, POWER_BRACELET) # decouple chest from pillar

        pre_boss = Location(7).connect(final_pillar, NIGHTMARE_KEY7) 
        beamos_horseheads = Location(7).add(DungeonChest(0x220)).connect(pre_boss, POWER_BRACELET) # 100 rupee chest / medicine chest (DX) behind boss door
        boss = Location(7).add(HeartContainer(0x223), Instrument(0x22c)).connect(pre_boss, r.boss_requirements[world_setup.boss_mapping[6]])

        if options.dungeon_items not in {'localnightmarekey', 'keysanity', 'keysy'}:
            first_key.items[0].forced_item = KEY7
            
        if options.logic == 'glitched' or options.logic == 'hell':
            topright_pillar_area.connect(entrance, AND(FEATHER, SWORD)) # superjump in the center to get on raised blocks, superjump in switch room to right side to walk down. center superjump has to be low so sword added
            toprightF1_chest.connect(topright_pillar_area, FEATHER) # superjump from F1 switch room
            topright_pillar_area.connect(bottomleftF2_area, FEATHER) # superjump in top left pillar room over the blocks from right to left
            final_pillar_area.connect(bottomleftF2_area, r.attack_hookshot) # sideways block push to get to the chest and pillar
            if options.owlstatues == "both" or options.owlstatues == "dungeon":
                bottomleft_owl.connect(bottomleftF2_area, STONE_BEAK7) # sideways block push to get to the owl statue (attack_hookshot is already implied from bottomleftF2_area)
            final_pillar.connect(bottomleftF2_area, BOMB) # bomb trigger pillar
            pre_boss.connect(final_pillar, FEATHER) # superjump on top of goomba to extend superjump to boss door plateau
            
        if options.logic == 'hell':
            topright_pillar_area.connect(entrance, FEATHER) # superjump in the center to get on raised blocks, has to be low
        
        self.entrance = entrance
