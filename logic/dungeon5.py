from .requirements import *
from .location import Location
from locations import *

#TODO: In this dungeon you can waste a key by going to the miniboss, which is useless and can be bypassed.
#       Logic does not account for you wasting this key (maybe remove the keyblock?)

class Dungeon5:
    def __init__(self, options):
        entrance = Location(5)
        Location(5).add(DungeonChest(0x1A0)).connect(entrance, HOOKSHOT)
        compass = Location(5).add(DungeonChest(0x19E)).connect(entrance, attack_hookshot)
        Location(5).add(DroppedKey(0x181)).connect(compass, AND(SWORD, FEATHER))

        area2 = Location(5).connect(entrance, KEY5)  
        Location(5).add(OwlStatue(0x19A)).connect(area2, STONE_BEAK5)
        Location(5).add(DungeonChest(0x19B)).connect(area2, attack_hookshot)  # map chest
        blade_trap_chest = Location(5).add(DungeonChest(0x197)).connect(area2, HOOKSHOT)  # key chest on the left
        post_gohma = Location(5).connect(area2, AND(HOOKSHOT, KEY5)) # staircase after gohma
        staircase_before_boss = Location(5).connect(post_gohma, AND(HOOKSHOT, FEATHER)) # bottom right section pits room before boss door. Path via gohma
        after_keyblock_boss = Location(5).connect(staircase_before_boss, AND(KEY5, FOUND(KEY5, 3))) # top right section pits room before boss door
        after_stalfos = Location(5).add(DungeonChest(0x196)).connect(area2, AND(SWORD, BOMB)) # Need to defeat master stalfos once for this empty chest; l2 sword beams kill but obscure
        butterfly_owl = Location(5).add(OwlStatue(0x18A)).connect(after_stalfos, AND(FEATHER, STONE_BEAK5))
        after_stalfos.connect(staircase_before_boss, AND(FEATHER, attack_hookshot_powder), one_way=True) # pathway from stalfos to staircase: past butterfly room and push the block
        north_of_crossroads = Location(5).connect(after_stalfos, FEATHER)
        Location(5).add(DungeonChest(0x18E)).connect(north_of_crossroads, OR(HOOKSHOT, AND(FEATHER, PEGASUS_BOOTS))) # south of bridge
        north_bridge_chest = Location(5).add(DungeonChest(0x188)).connect(north_of_crossroads, HOOKSHOT) # north bridge chest 50 rupees
        east_bridge_chest = Location(5).add(DungeonChest(0x18F)).connect(north_of_crossroads, HOOKSHOT) # east bridge chest small key
        stone_tablet = Location(5).add(DungeonChest(0x183)).connect(north_of_crossroads, POWER_BRACELET)  # stone tablet
        boss_key = Location(5).add(DungeonChest(0x186)).connect(after_stalfos, AND(FLIPPERS, HOOKSHOT))  # nightmare key
        before_boss = Location(5).connect(after_keyblock_boss, HOOKSHOT) 
        boss = Location(5).add(HeartContainer(0x185)).connect(before_boss, AND(HOOKSHOT, SWORD, NIGHTMARE_KEY5))

        # When we can reach the stone tablet chest, we can also reach the final location of master stalfos
        stone_tablet.add(HookshotDrop())

        if options.logic == 'hard' or options.logic == 'glitched':
            blade_trap_chest.connect(area2, AND(FEATHER, attack_hookshot_powder))
            boss_key.connect(after_stalfos, AND(FLIPPERS, FEATHER, PEGASUS_BOOTS)) # boots jump across
            after_stalfos.connect(after_keyblock_boss, AND(FEATHER, attack_hookshot_powder)) # circumvent stalfos by going past gohma and backwards from boss door
            butterfly_owl.connect(after_stalfos, AND(PEGASUS_BOOTS, STONE_BEAK5)) # boots charge + bonk to cross 2d bridge
            staircase_before_boss.connect(post_gohma, AND(PEGASUS_BOOTS, HOOKSHOT)) # boots bonk in 2d section to skip feather
            north_of_crossroads.connect(after_stalfos, HOOKSHOT) # hookshot to the right block to cross pits
            after_keyblock_boss.connect(after_stalfos, AND(FEATHER, attack_hookshot_powder)) # jump from bottom left to top right, skipping the keyblock 
            before_boss.connect(after_stalfos, AND(FEATHER, PEGASUS_BOOTS, attack_hookshot_powder)) # cross pits room from bottom left to top left with boots jump
            
        if options.logic == 'glitched':
            post_gohma.connect(area2, HOOKSHOT) # glitch through the blocks/pots with hookshot. Zoomerang can be used but has no logical implications because of 2d section requiring hookshot
            north_bridge_chest.connect(north_of_crossroads, AND(PEGASUS_BOOTS, FEATHER, BOOMERANG)) # use zoomerang to cross pits from the bottom
            #after_stalfos.connect(post_gohma, AND(FEATHER, HOOKSHOT, OR(SWORD, BOW, MAGIC_ROD))) # TODO: requires nag messages from key block before boss
            
        self.entrance = entrance
