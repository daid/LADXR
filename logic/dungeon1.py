from .requirements import *
from .location import Location
from locations.all import *


class Dungeon1:
    def __init__(self, options, world_setup, r):
        entrance = Location(1)
        entrance.add(DungeonChest(0x113), DungeonChest(0x115), DungeonChest(0x10E))
        Location(1).add(DroppedKey(0x116)).connect(entrance, OR(BOMB, r.push_hardhat)) # hardhat beetles (can kill with bomb)
        Location(1).add(DungeonChest(0x10D)).connect(entrance, OR(r.attack_hookshot_powder, SHIELD)) # moldorm spawn chest
        stalfos_keese_room = Location(1).add(DungeonChest(0x114)).connect(entrance, r.attack_hookshot) # 2 stalfos 2 keese room
        Location(1).add(DungeonChest(0x10C)).connect(entrance, BOMB) # hidden seashell room
        dungeon1_upper_left = Location(1).connect(entrance, AND(KEY1, FOUND(KEY1, 3)))
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(1).add(OwlStatue(0x103), OwlStatue(0x104)).connect(dungeon1_upper_left, STONE_BEAK1)
        feather_chest = Location(1).add(DungeonChest(0x11D)).connect(dungeon1_upper_left, SHIELD)  # feather location, behind spike enemies. can shield bump into pit (only shield works)
        boss_key = Location(1).add(DungeonChest(0x108)).connect(entrance, AND(FEATHER, KEY1, FOUND(KEY1, 3))) # boss key
        dungeon1_right_side = Location(1).connect(entrance, AND(KEY1, FOUND(KEY1, 3)))
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(1).add(OwlStatue(0x10A)).connect(dungeon1_right_side, STONE_BEAK1)
        Location(1).add(DungeonChest(0x10A)).connect(dungeon1_right_side, OR(r.attack_hookshot, SHIELD)) # three of a kind, shield stops the suit from changing
        dungeon1_miniboss = Location(1).connect(dungeon1_right_side, AND(r.miniboss_requirements[world_setup.miniboss_mapping[0]], FEATHER))
        dungeon1_boss = Location(1).connect(dungeon1_miniboss, NIGHTMARE_KEY1)
        Location(1).add(HeartContainer(0x106), Instrument(0x102)).connect(dungeon1_boss, r.boss_requirements[world_setup.boss_mapping[0]])

        if options.logic not in ('normal', 'casual'):
            stalfos_keese_room.connect(entrance, r.attack_hookshot_powder) # stalfos jump away when you press a button.

        if options.logic == 'glitched' or options.logic == 'hell':
            boss_key.connect(entrance, FEATHER)  # super jump
            dungeon1_miniboss.connect(dungeon1_right_side, r.miniboss_requirements[world_setup.miniboss_mapping[0]]) # damage boost or buffer pause over the pit to cross or mushroom
        
        if options.logic == 'hell':
            feather_chest.connect(dungeon1_upper_left, SWORD)  # keep slashing the spiked beetles until they keep moving 1 pixel close towards you and the pit, to get them to fall
            boss_key.connect(entrance, FOUND(KEY1,3)) # damage boost off the hardhat to cross the pit
            
        self.entrance = entrance
