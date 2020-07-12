from .requirements import *
from .location import Location
from locations import *


class Dungeon1:
    def __init__(self, options):
        entrance = Location(1)
        entrance.add(DungeonChest(0x113), DungeonChest(0x115), DungeonChest(0x10E))
        Location(1).add(DroppedKey(0x116)).connect(entrance, OR(BOMB, push_hardhat)) # hardhat beetles (can kill with bomb)
        Location(1).add(DungeonChest(0x10D)).connect(entrance, OR(attack_hookshot_powder, SHIELD)) # moldorm spawn chest
        Location(1).add(DungeonChest(0x114)).connect(entrance, attack_hookshot_powder) # 2 stalfos 2 keese room, stalfos jump away when you press a button. 
        Location(1).add(DungeonChest(0x10C)).connect(entrance, BOMB) # hidden seashell room
        dungeon1_upper_left = Location(1).connect(entrance, AND(KEY1, FOUND(KEY1, 3)))
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(1).add(OwlStatue(0x103), OwlStatue(0x104)).connect(dungeon1_upper_left, STONE_BEAK1)
        Location(1).add(DungeonChest(0x11D)).connect(dungeon1_upper_left, SHIELD)  # feather location, behind spike enemies. can shield bump into pit (only shield works)
        boss_key = Location(1).add(DungeonChest(0x108)).connect(entrance, AND(FEATHER, KEY1, FOUND(KEY1, 3))) # boss key
        dungeon1_right_side = Location(1).connect(entrance, AND(KEY1, FOUND(KEY1, 3)))
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(1).add(OwlStatue(0x10A)).connect(dungeon1_right_side, STONE_BEAK1)
        Location(1).add(DungeonChest(0x10A)).connect(dungeon1_right_side, OR(attack_hookshot, SHIELD)) # three of a kind, shield stops the suit from changing
        dungeon1_miniboss = Location(1).connect(dungeon1_right_side, AND(attack_hookshot, FEATHER))
        dungeon1_boss = Location(1).connect(dungeon1_miniboss, NIGHTMARE_KEY1)
        Location(1).add(HeartContainer(0x106)).connect(dungeon1_boss, SWORD)

        if options.logic == 'glitched' or options.logic == 'hell':
            boss_key.connect(entrance, FEATHER)  # super jump
            dungeon1_miniboss.connect(dungeon1_right_side, attack_hookshot) # damage boost or buffer pause over the pit to cross or mushroom
        
        if options.logic == 'hell':
            boss_key.connect(entrance, AND(KEY1, FOUND(KEY1,3))) # damage boost off the hardhat to cross the pit
            
        self.entrance = entrance
