from .requirements import *
from .location import Location
from locations.all import *


class Dungeon3:
    def __init__(self, options, world_setup, r):
        entrance = Location("D3 Entrance", dungeon=3)
        dungeon3_reverse_eye = Location(dungeon=3).add(DungeonChest(0x153)).connect(entrance, PEGASUS_BOOTS, id="cv") # Right side reverse eye
        area2 = Location("D3 After Pot Door", dungeon=3).connect(entrance, POWER_BRACELET, id="cw")
        Location(dungeon=3).add(DungeonChest(0x151)).connect(area2, r.attack_hookshot_powder, id="cx")  # First chest with key
        area2.add(DungeonChest(0x14F))  # Second chest with slime
        area3 = Location("D3 After Zol Chest", dungeon=3).connect(area2, OR(r.attack_hookshot_powder, PEGASUS_BOOTS), id="cy") # need to kill slimes to continue or pass through left path
        dungeon3_zol_stalfos = Location(dungeon=3).add(DungeonChest(0x14E)).connect(area3, AND(PEGASUS_BOOTS, r.attack_skeleton), id="cz")  # 3th chest requires killing the slime behind the crystal pillars

        # now we can go 4 directions,
        area_up = Location("D3 North Room", dungeon=3).connect(area3, AND(KEY3, FOUND(KEY3, 8)), id="d0")
        dungeon3_north_key_drop = Location(dungeon=3).add(DroppedKey(0x154)).connect(area_up, r.attack_skeleton, id="d1") # north key drop
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=3).add(OwlStatue(0x154)).connect(area_up, STONE_BEAK3, id="d2")
        dungeon3_raised_blocks_north = Location(dungeon=3).add(DungeonChest(0x14C)) # chest locked behind raised blocks near staircase
        dungeon3_raised_blocks_east = Location(dungeon=3).add(DungeonChest(0x150)) # chest locked behind raised blocks next to slime chest
        area_up.connect(dungeon3_raised_blocks_north, r.hit_switch, one_way=True, id="d3") # hit switch to reach north chest
        area_up.connect(dungeon3_raised_blocks_east, r.hit_switch, one_way=True, id="d4") # hit switch to reach east chest
        
        area_left = Location("D3 West Room", dungeon=3).connect(area3, AND(KEY3, FOUND(KEY3, 8)), id="d5")
        area_left_key_drop = Location(dungeon=3).add(DroppedKey(0x155)).connect(area_left, r.attack_hookshot, id="d6") # west key drop (no longer requires feather to get across hole), can use boomerang to knock owls into pit

        area_down = Location("D3 South Room", dungeon=3).connect(area3, AND(KEY3, FOUND(KEY3, 8)), id="d7")
        dungeon3_south_key_drop = Location(dungeon=3).add(DroppedKey(0x158)).connect(area_down, r.attack_hookshot, id="d8") # south keydrop, can use boomerang to knock owls into pit

        area_right = Location("D3 East Room", dungeon=3).connect(area3, AND(KEY3, FOUND(KEY3, 4)), id="d9")  # We enter the top part of the map here.
        Location(dungeon=3).add(DroppedKey(0x14D)).connect(area_right, r.attack_hookshot_powder, id="da")  # key after the stairs.

        dungeon3_nightmare_key_chest = Location(dungeon=3).add(DungeonChest(0x147)).connect(area_right, AND(BOMB, FEATHER, PEGASUS_BOOTS), id="db")  # nightmare key chest
        dungeon3_miniboss_room = Location("D3 Miniboss Room", dungeon=3).connect(area_right, r.attack_hookshot_powder, id="dc")
        dungeon3_post_dodongo_chest = Location(dungeon=3).add(DungeonChest(0x146)).connect(dungeon3_miniboss_room, r.miniboss_requirements[world_setup.miniboss_mapping[2]], id="dd")  # boots after the miniboss
        compass_chest = Location(dungeon=3).add(DungeonChest(0x142)).connect(area_right, OR(SWORD, BOMB, AND(SHIELD, r.attack_hookshot_powder)), id="de") # bomb only activates with sword, bomb or shield
        dungeon3_3_bombite_room = Location(dungeon=3).add(DroppedKey(0x141)).connect(compass_chest, BOMB, id="df") # 3 bombite room
        Location(dungeon=3).add(DroppedKey(0x148)).connect(area_right, r.attack_no_boomerang, id="dg") # 2 zol 2 owl drop key
        Location(dungeon=3).add(DungeonChest(0x144)).connect(area_right, r.attack_skeleton, id="dh")  # map chest
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=3).add(OwlStatue(0x140), OwlStatue(0x147)).connect(area_right, STONE_BEAK3, id="di")

        towards_boss1 = Location("D3 Boss Path 1", dungeon=3).connect(area_right, AND(KEY3, FOUND(KEY3, 5)), id="dj")
        towards_boss2 = Location("D3 Boss Path 2", dungeon=3).connect(towards_boss1, AND(KEY3, FOUND(KEY3, 6)), id="dk")
        towards_boss3 = Location("D3 Boss Path 3", dungeon=3).connect(towards_boss2, AND(KEY3, FOUND(KEY3, 7)), id="dl")
        towards_boss4 = Location("D3 Boss Path 4", dungeon=3).connect(towards_boss3, AND(KEY3, FOUND(KEY3, 8)), id="dm")

        # Just the whole area before the boss, requirements for the boss itself and the rooms before it are the same.
        pre_boss = Location(dungeon=3).connect(towards_boss4, AND(r.attack_no_boomerang, FEATHER, PEGASUS_BOOTS), id="dn")
        pre_boss.add(DroppedKey(0x15B))

        boss_room = Location("D3 Boss Room", dungeon=3).connect(pre_boss, NIGHTMARE_KEY3, id="do")
        boss = Location(dungeon=3).add(HeartContainer(0x15A), Instrument(0x159)).connect(boss_room, r.boss_requirements[world_setup.boss_mapping[2]], id="dp")

        if options.dungeon_items not in {'localnightmarekey', 'keysanity', 'keysy', 'smallkeys'}:
            # Without keysanity we need to fix the keylogic here, else we can never generate proper placement.
            area_left.connect(area3, KEY3, id="dq")
            area_left_key_drop.items[0].forced_item = KEY3
            area_down.connect(area3, KEY3, id="dr")
            dungeon3_south_key_drop.items[0].forced_item = KEY3

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            dungeon3_3_bombite_room.connect(area_right, BOOMERANG, id="ds") # 3 bombite room from the left side, grab item with boomerang
            dungeon3_reverse_eye.connect(entrance, r.hookshot_over_pit, id="dt") # hookshot the chest to get to the right side
            dungeon3_north_key_drop.connect(area_up, r.throw_pot, id="du") # use pots to kill the enemies
            dungeon3_south_key_drop.connect(area_down, r.throw_pot, id="dv") # use pots to kill enemies
            area_up.connect(dungeon3_raised_blocks_north, r.throw_pot, one_way=True, id="dw") # use pots to hit the switch
            area_up.connect(dungeon3_raised_blocks_east, AND(r.throw_pot, r.attack_hookshot_powder), one_way=True, id="dx") # use pots to hit the switch

        if options.logic == 'glitched' or options.logic == 'hell':
            area2.connect(dungeon3_raised_blocks_east, AND(r.attack_hookshot_powder, r.super_jump_feather), one_way=True, id="dy") # use superjump to get over the bottom left block
            area3.connect(dungeon3_raised_blocks_north, AND(OR(PEGASUS_BOOTS, r.hookshot_clip_block), r.shaq_jump), one_way=True, id="dz") # use shagjump (unclipped superjump next to movable block) from north wall to get on the blocks. Instead of boots can also get to that area with a hookshot clip past the movable block
            area3.connect(dungeon3_zol_stalfos, r.hookshot_clip_block, one_way=True, id="e0") # hookshot clip through the northern push block next to raised blocks chest to get to the zol
            dungeon3_nightmare_key_chest.connect(area_right, AND(r.super_jump_feather, BOMB), id="e1") # superjump to right side 3 gap via top wall and jump the 2 gap
            dungeon3_post_dodongo_chest.connect(area_right, AND(r.super_jump_feather, FOUND(KEY3, 6)), id="e2") # superjump from keyblock path. use 2 keys to open enough blocks TODO: text skip skips 1 key
        
        if options.logic == 'hell':
            area2.connect(dungeon3_raised_blocks_east, r.boots_superhop, one_way=True, id="e3") # use boots superhop to get over the bottom left block
            area3.connect(dungeon3_raised_blocks_north, r.boots_superhop, one_way=True, id="e4") # use boots superhop off top wall or left wall to get on raised blocks
            area_up.connect(dungeon3_zol_stalfos, AND(r.super_jump_feather, r.attack_skeleton), one_way=True, id="e5") # use superjump near top blocks chest to get to zol without boots, keep wall clip on right wall to get a clip on left wall or use obstacles
            area_left_key_drop.connect(area_left, r.shield_bump, id="e6") # knock everything into the pit including the teleporting owls
            dungeon3_south_key_drop.connect(area_down, r.shield_bump, id="e7") # knock everything into the pit including the teleporting owls
            dungeon3_nightmare_key_chest.connect(area_right, AND(r.super_jump_feather, r.shield_bump), id="e8") # superjump into jumping stalfos and shield bump to right ledge
            dungeon3_nightmare_key_chest.connect(area_right, AND(BOMB, r.pit_buffer_boots, HOOKSHOT), id="e9") # boots bonk across the pits with pit buffering and hookshot to the chest
            compass_chest.connect(dungeon3_3_bombite_room, OR(BOW, MAGIC_ROD, AND(OR(FEATHER, PEGASUS_BOOTS), OR(SWORD, MAGIC_POWDER))), one_way=True, id="ea") # 3 bombite room from the left side, use a bombite to blow open the wall without bombs
            pre_boss.connect(towards_boss4, AND(r.attack_no_boomerang, FEATHER, POWER_BRACELET), id="eb") # use bracelet super bounce glitch to pass through first part underground section
            pre_boss.connect(towards_boss4, AND(r.attack_no_boomerang, r.boots_bonk_2d_spikepit), id="ec") # use medicine invulnerability to pass through the 2d section with a boots bonk to reach the staircase
            
        self.entrance = entrance
        self.final_room = boss


class NoDungeon3:
    def __init__(self, options, world_setup, r):
        entrance = Location("D3 Entrance", dungeon=3)
        Location(dungeon=3).add(HeartContainer(0x15A), Instrument(0x159)).connect(entrance, AND(POWER_BRACELET, r.boss_requirements[
            world_setup.boss_mapping[2]]))

        self.entrance = entrance
