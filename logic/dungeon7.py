from .requirements import *
from .location import Location
from locations import *


class Dungeon7:
    def __init__(self, options):
        entrance = Location(7)
        first_key = Location(7).add(DroppedKey(0x210)).connect(entrance, attack_hookshot_powder)
        topright_pillar_area = Location(7).connect(entrance, KEY7)
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(7).add(OwlStatue(0x216)).connect(topright_pillar_area, STONE_BEAK7)
        topright_pillar = Location(7).add(DungeonChest(0x212)).connect(topright_pillar_area, POWER_BRACELET)  # map chest
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(7).add(OwlStatue(0x204)).connect(topright_pillar_area, STONE_BEAK7)
        topright_pillar_area.add(DungeonChest(0x209))  # stone slab chest can be reached by dropping down a hole
        three_of_a_kind_north = Location(7).add(DungeonChest(0x211)).connect(topright_pillar_area, OR(attack_hookshot, AND(FEATHER, SHIELD)))  # compass chest; path without feather with hitting switch by falling on the raised blocks. No bracelet because ball does not reset
        bottomleftF2_area = Location(7).add(DungeonChest(0x201)).connect(topright_pillar_area, attack_hookshot)  # area with hinox
        Location(7).add(DroppedKey(0x21B)).connect(bottomleftF2_area, attack_hookshot) # hinox drop key
        # Most of the dungeon can be accessed at this point.
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            bottomleft_owl = Location(7).add(OwlStatue(0x21C)).connect(bottomleftF2_area, AND(BOMB, STONE_BEAK7))
        nightmare_key = Location(7).add(DungeonChest(0x224)).connect(bottomleftF2_area, attack_no_bomb) # nightmare key after the miniboss
        bottomleftF2_area.add(DungeonChest(0x21A))  # mirror shield chest
        toprightF1_chest = Location(7).add(DungeonChest(0x204)).connect(bottomleftF2_area, attack_hookshot)  # chest on the F1 right ledge. Added attack_hookshot since 1 requirement is needed
        final_pillar_area = Location(7).add(DungeonChest(0x21C)).connect(bottomleftF2_area, AND(BOMB, HOOKSHOT))  # chest that needs to spawn to get to the last pillar
        final_pillar = Location(7).connect(final_pillar_area, POWER_BRACELET) # decouple chest from pillar

        pre_boss = Location(7).connect(final_pillar, NIGHTMARE_KEY7) 
        beamos_horseheads = Location(7).connect(pre_boss, POWER_BRACELET) # 100 rupee chest / medicine chest (DX) behind boss door
        boss = Location(7).add(HeartContainer(0x2E8)).connect(pre_boss, AND(OR(MAGIC_ROD, SWORD, HOOKSHOT), SHIELD))

        if not options.keysanity:
            first_key.items[0].forced_item = KEY7
            
        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            boss.connect(pre_boss, OR(MAGIC_ROD, AND(BOMB, BOW))) # magic rod and bomb arrows allow a 3 cycle which avoids the feather wind attack
            boss.connect(pre_boss, AND(BOW, SHIELD)) # limited arrow amount is rough
            
        if options.logic == 'glitched' or options.logic == 'hell':
            topright_pillar_area.connect(entrance, AND(FEATHER, SWORD)) # superjump in the center to get on raised blocks, superjump in switch room to right side to walk down. center superjump has to be low so sword added
            toprightF1_chest.connect(topright_pillar_area, FEATHER) # superjump from F1 switch room
            final_pillar_area.connect(bottomleftF2_area, attack_hookshot) # sideways block push to get to the chest and pillar
            if options.owlstatues == "both" or options.owlstatues == "dungeon":
                bottomleft_owl.connect(bottomleftF2_area, AND(attack_hookshot, STONE_BEAK7)) # sideways block push to get to the owl statue (attack_hookshot is already implied from bottomleftF2_area)
            final_pillar.connect(bottomleftF2_area, BOMB) # bomb trigger pillar
            pre_boss.connect(final_pillar, FEATHER) # superjump on top of goomba to extend superjump to boss door plateau
            boss.connect(pre_boss, OR(BOMB, BOW, HOOKSHOT, MAGIC_ROD)) # use bombs while on staircase to time when evil eagle flies by. Or hit the boss straight above staircase, then use ranged (bow/hookshot/magic rod (l2sword??)) straight down to kill evil eagle offscreen
            
            
        if options.logic == 'hell':
            topright_pillar_area.connect(entrance, FEATHER) # superjump in the center to get on raised blocks, has to be low
        
        self.entrance = entrance
