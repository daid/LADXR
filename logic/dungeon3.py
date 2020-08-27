from .requirements import *
from .location import Location
from locations import *


class Dungeon3:
    def __init__(self, options, boss_requirement):
        entrance = Location(3)
        dungeon3_reverse_eye = Location(3).add(DungeonChest(0x153)).connect(entrance, PEGASUS_BOOTS) # Right side reverse eye
        area2 = Location(3).connect(entrance, POWER_BRACELET)
        Location(3).add(DungeonChest(0x151)).connect(area2, attack_hookshot_powder)  # First chest with key
        area2.add(DungeonChest(0x14F))  # Second chest with slime
        area3 = Location(3).connect(area2, OR(attack_hookshot_powder, PEGASUS_BOOTS)) # need to kill slimes to continue or pass through left path
        dungeon3_zol_stalfos = Location(3).add(DungeonChest(0x14E)).connect(area3, AND(PEGASUS_BOOTS, attack_skeleton))  # 3th chest requires killing the slime behind the crystal pillars

        # now we can go 4 directions,
        area_up = Location(3).connect(area3, AND(KEY3, FOUND(KEY3, 8)))
        dungeon3_north_key_drop = Location(3).add(DroppedKey(0x154)).connect(area_up, attack_skeleton) # north key drop
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(3).add(OwlStatue(0x154)).connect(area_up, STONE_BEAK3)
        dungeon3_raised_blocks_north = Location(3).add(DungeonChest(0x14C)) # chest locked behind raised blocks near staircase
        dungeon3_raised_blocks_east = Location(3).add(DungeonChest(0x150)) # chest locked behind raised blocks next to slime chest
        area_up.connect(dungeon3_raised_blocks_north, attack_hookshot, one_way=True) # hit switch to reach north chest
        area_up.connect(dungeon3_raised_blocks_east, attack_hookshot, one_way=True) # hit switch to reach east chest
        
        area_left = Location(3).connect(area3, AND(KEY3, FOUND(KEY3, 8)))
        area_left_key_drop = Location(3).add(DroppedKey(0x155)).connect(area_left, attack_no_boomerang) # west key drop (no longer requires feather to get across hole)

        area_down = Location(3).connect(area3, AND(KEY3, FOUND(KEY3, 8)))
        dungeon3_south_key_drop = Location(3).add(DroppedKey(0x158)).connect(area_down, attack_no_boomerang) # south keydrop

        area_right = Location(3).connect(area3, AND(KEY3, FOUND(KEY3, 4)))  # We enter the top part of the map here.
        Location(3).add(DroppedKey(0x14D)).connect(area_right, attack_hookshot_powder)  # key after the stairs.

        dungeon3_nightmare_key_chest = Location(3).add(DungeonChest(0x147)).connect(area_right, AND(BOMB, FEATHER, PEGASUS_BOOTS))  # nightmare key chest
        dungeon3_post_dodongo_chest = Location(3).add(DungeonChest(0x146)).connect(area_right, BOMB)  # boots after the miniboss
        compass_chest = Location(3).add(DungeonChest(0x142)).connect(area_right, OR(SWORD, BOMB, AND(SHIELD, attack_hookshot_powder))) # bomb only activates with sword, bomb or shield
        dungeon3_3_bombite_room = Location(3).add(DroppedKey(0x141)).connect(compass_chest, BOMB) # 3 bombite room
        dungeon3_3_bombite_room.connect(area_right, BOOMERANG) # 3 bombite room from the left side, grab item with boomerang
        Location(3).add(DroppedKey(0x148)).connect(area_right, attack_no_boomerang) # 2 zol 2 owl drop key
        Location(3).add(DungeonChest(0x144)).connect(area_right, attack_skeleton)  # map chest
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(3).add(OwlStatue(0x140), OwlStatue(0x147)).connect(area_right, STONE_BEAK3)

        towards_boss1 = Location(3).connect(area_right, AND(KEY3, FOUND(KEY3, 5)))
        towards_boss2 = Location(3).connect(towards_boss1, AND(KEY3, FOUND(KEY3, 6)))
        towards_boss3 = Location(3).connect(towards_boss2, AND(KEY3, FOUND(KEY3, 7)))
        towards_boss4 = Location(3).connect(towards_boss3, AND(KEY3, FOUND(KEY3, 8)))

        # Just the whole area before the boss, requirements for the boss itself and the rooms before it are the same.
        pre_boss = Location(3).connect(towards_boss4, AND(attack_no_boomerang, FEATHER, PEGASUS_BOOTS))
        pre_boss.add(DroppedKey(0x15B))

        boss = Location(3).add(HeartContainer(0x15A)).connect(pre_boss, AND(NIGHTMARE_KEY3, boss_requirement))
        # TODO Set as target

        if not options.keysanity:
            # Without keysanity we need to fix the keylogic here, else we can never generate proper placement.
            area_left.connect(area3, KEY3)
            dungeon3_north_key_drop.items[0].forced_item = KEY3
            area_down.connect(area3, KEY3)
            area_left_key_drop.items[0].forced_item = KEY3
            area_up.connect(area3, KEY3)
            dungeon3_south_key_drop.items[0].forced_item = KEY3

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            dungeon3_reverse_eye.connect(entrance, HOOKSHOT) # hookshot the chest to get to the right side
            dungeon3_north_key_drop.connect(area_up, POWER_BRACELET) # use pots to kill the enemies
            dungeon3_south_key_drop.connect(area_down, POWER_BRACELET) # use pots to kill enemies
        
        if options.logic == 'glitched' or options.logic == 'hell':
            area3.connect(dungeon3_raised_blocks_east, FEATHER, one_way=True) # use superjump to get over the bottom left block
            area3.connect(dungeon3_raised_blocks_north, AND(PEGASUS_BOOTS, FEATHER), one_way=True) # use shagjump (unclipped superjump next to movable block) from north wall to get on the blocks
            dungeon3_nightmare_key_chest.connect(area_right, AND(FEATHER, BOMB)) # superjump to right side 3 gap via top wall and jump the 2 gap
            dungeon3_post_dodongo_chest.connect(area_right, AND(FEATHER, OR(FOUND(KEY3, 5), SWORD))) # superjump from keyblock path. use 1 key to open first block + text clip 2nd or dodongo superjump to negate all extra keys which needs sword to turn
        
        if options.logic == 'hell':
            area3.connect(dungeon3_raised_blocks_north, AND(PEGASUS_BOOTS, BOW), one_way=True) # use boots superjump off top wall
            dungeon3_zol_stalfos.connect(area_up, AND(FEATHER, SWORD)) # use superjump near top blocks chest to get to zol without boots. TODO: Nag messages removes sword req
            area_left_key_drop.connect(area_left, SHIELD) # knock everything into the pit including the teleporting owls
            dungeon3_south_key_drop.connect(area_down, SHIELD) # knock everything into the pit including the teleporting owls
            dungeon3_nightmare_key_chest.connect(area_right, AND(FEATHER, SHIELD)) # superjump into jumping stalfos and shield bump to right ledge
            dungeon3_nightmare_key_chest.connect(area_right, AND(BOMB, PEGASUS_BOOTS, HOOKSHOT)) # boots bonk across the pits with pit buffering and hookshot to the chest
            pre_boss.connect(towards_boss4, AND(attack_no_boomerang, FEATHER, POWER_BRACELET)) # use bracelet super bounce glitch to pass through first part underground section
            #pre_boss.connect(towards_boss4, AND(attack_no_boomerang, PEGASUS_BOOTS, MEDICINE)) # use medicine invulnerability to pass through the 2d section with a boots bonk to reach the staircase
            
        self.entrance = entrance
