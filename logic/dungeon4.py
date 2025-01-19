from .requirements import *
from .location import Location
from locations.all import *


class Dungeon4:
    def __init__(self, options, world_setup, r):
        entrance = Location("D4 Entrance", dungeon=4)
        entrance.add(DungeonChest(0x179))  # stone slab chest
        entrance.add(DungeonChest(0x16A))  # map chest
        right_of_entrance = Location(dungeon=4).add(DungeonChest(0x178)).connect(entrance, AND(SHIELD, r.attack_hookshot_powder), id="ee") # 1 zol 2 spike beetles 1 spark chest
        Location(dungeon=4).add(DungeonChest(0x17B)).connect(right_of_entrance, AND(SHIELD, SWORD), id="ef") # room with key chest
        rightside_crossroads = Location("D4 Crossroads East", dungeon=4).connect(entrance, AND(FEATHER, PEGASUS_BOOTS), id="eg")  # 2 key chests on the right.
        pushable_block_chest = Location(dungeon=4).add(DungeonChest(0x171)).connect(rightside_crossroads, BOMB, id="eh") # lower chest
        puddle_crack_block_chest = Location(dungeon=4).add(DungeonChest(0x165)).connect(rightside_crossroads, OR(BOMB, FLIPPERS), id="ei") # top right chest
        
        double_locked_room = Location("D4 Double Locked Room", dungeon=4).connect(right_of_entrance, AND(KEY4, FOUND(KEY4, 5)), one_way=True, id="ej")
        right_of_entrance.connect(double_locked_room, KEY4, one_way=True, id="ek")
        after_double_lock = Location("D4 Crossroads South", dungeon=4).connect(double_locked_room, AND(KEY4, FOUND(KEY4, 4), OR(FEATHER, FLIPPERS)), one_way=True, id="el")
        double_locked_room.connect(after_double_lock, AND(KEY4, FOUND(KEY4, 2), OR(FEATHER, FLIPPERS)), one_way=True, id="em")
        
        dungeon4_puddle_before_crossroads = Location(dungeon=4).add(DungeonChest(0x175)).connect(after_double_lock, FLIPPERS, id="en")
        north_crossroads = Location("D4 Crossroads North", dungeon=4).connect(after_double_lock, AND(FEATHER, PEGASUS_BOOTS), id="eo")
        before_miniboss = Location("D4 Before Miniboss", dungeon=4).connect(north_crossroads, AND(KEY4, FOUND(KEY4, 3)), id="ep")
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=4).add(OwlStatue(0x16F)).connect(before_miniboss, STONE_BEAK4, id="eq")
        sidescroller_key = Location(dungeon=4).add(DroppedKey(0x169)).connect(before_miniboss, AND(r.attack_hookshot_powder, FLIPPERS), id="er")  # key that drops in the hole and needs swim to get
        center_puddle_chest = Location(dungeon=4).add(DungeonChest(0x16E)).connect(before_miniboss, FLIPPERS, id="es")  # chest with 50 rupees
        left_water_area = Location("D4 Tile Puzzle", dungeon=4).connect(before_miniboss, OR(FEATHER, FLIPPERS), id="et") # area left with zol chest and 5 symbol puzzle (water area)
        left_water_area.add(DungeonChest(0x16D))  # gel chest
        left_water_area.add(DungeonChest(0x168))  # key chest near the puzzle
        miniboss_room = Location("D4 Miniboss Room", dungeon=4).connect(before_miniboss, AND(KEY4, FOUND(KEY4, 5)), id="eu")
        miniboss = Location("D4 After Miniboss", dungeon=4).connect(miniboss_room, r.miniboss_requirements[world_setup.miniboss_mapping[3]], id="ev") 
        terrace_zols_chest = Location("D4 After Flippers", dungeon=4).connect(before_miniboss, FLIPPERS, id="ew") # flippers to move around miniboss through 5 tile room
        miniboss.connect(terrace_zols_chest, POWER_BRACELET, one_way=True, id="ex") # reach flippers chest through the miniboss room
        terrace_zols_chest.add(DungeonChest(0x160))  # flippers chest
        terrace_zols_chest.connect(left_water_area, r.attack_hookshot_powder, one_way=True, id="ey") # can move from flippers chest south to push the block to left area
        
        to_the_nightmare_key = Location(dungeon=4).connect(left_water_area, AND(FEATHER, OR(FLIPPERS, PEGASUS_BOOTS)), id="ez")  # 5 symbol puzzle (does not need flippers with boots + feather)
        to_the_nightmare_key.add(DungeonChest(0x176))

        before_boss = Location("D4 Before Boss", dungeon=4).connect(before_miniboss, AND(r.attack_hookshot, FLIPPERS, KEY4, FOUND(KEY4, 5)), id="f0")
        boss_room = Location("D4 Boss Room", dungeon=4).connect(before_boss, NIGHTMARE_KEY4, id="f1")
        boss = Location(dungeon=4).add(HeartContainer(0x166), Instrument(0x162)).connect(boss_room, r.boss_requirements[world_setup.boss_mapping[3]], id="f2")

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            sidescroller_key.connect(before_miniboss, BOOMERANG, id="f3") # fall off the bridge and boomerang downwards before hitting the water to grab the item
            sidescroller_key.connect(before_miniboss, AND(r.throw_pot, FLIPPERS), id="f4") # kill the zols with the pots in the room to spawn the key
            rightside_crossroads.connect(entrance, r.tight_jump, id="f5") # jump across the corners
            puddle_crack_block_chest.connect(rightside_crossroads, r.tight_jump, id="f6") # jump around the bombable block
            north_crossroads.connect(entrance, r.tight_jump, id="f7") # jump across the corners
            after_double_lock.connect(entrance, r.tight_jump, id="f8") # jump across the corners
            dungeon4_puddle_before_crossroads.connect(after_double_lock, r.tight_jump, id="f9") # With a tight jump feather is enough to cross the puddle without flippers
            center_puddle_chest.connect(before_miniboss, r.tight_jump, id="fa") # With a tight jump feather is enough to cross the puddle without flippers
            miniboss.connect(terrace_zols_chest, None, one_way=True, id="fb") # reach flippers chest through the miniboss room without pulling the lever
            to_the_nightmare_key.connect(left_water_area, r.tight_jump, id="fc") # With a tight jump feather is enough to reach the top left switch without flippers, or use flippers for puzzle and boots to get through 2d section
            before_boss.connect(left_water_area, r.tight_jump, id="fd") # jump to the bottom right corner of boss door room
            
        if options.logic == 'glitched' or options.logic == 'hell':    
            pushable_block_chest.connect(rightside_crossroads, AND(r.sideways_block_push, FLIPPERS), id="fe") # sideways block push to skip bombs
            sidescroller_key.connect(before_miniboss, AND(r.super_jump_feather, OR(r.attack_hookshot_powder, r.throw_pot)), id="ff") # superjump into the hole to grab the key while falling into the water
            miniboss.connect(before_miniboss, r.jesus_jump, id="fg") # use jesus jump to transition over the water left of miniboss
        
        if options.logic == 'hell':
            rightside_crossroads.connect(entrance, AND(r.pit_buffer_boots, r.hookshot_spam_pit), id="fh") # pit buffer into the wall of the first pit, then boots bonk across the center, hookshot to get to the rightmost pit to a second villa buffer on the rightmost pit
            rightside_crossroads.connect(after_double_lock, AND(OR(BOMB, BOW), r.hookshot_clip_block), id="fi") # split zols for more entities, and clip through the block against the right wall
            pushable_block_chest.connect(rightside_crossroads, AND(r.sideways_block_push, OR(r.jesus_buffer, r.jesus_jump)), id="fj") # use feather to water clip into the top right corner of the bombable block, and sideways block push to gain access. Can boots bonk of top right wall, then water buffer to top of chest and boots bonk to water buffer next to chest
            after_double_lock.connect(double_locked_room, AND(FOUND(KEY4, 4), r.pit_buffer_boots), one_way=True, id="fk") # use boots bonks to cross the water gaps
            after_double_lock.connect(entrance, r.pit_buffer_boots, id="fl") # boots bonk + pit buffer to the bottom
            after_double_lock.connect(entrance, AND(r.pit_buffer, r.hookshot_spam_pit), id="fm") # hookshot spam over the first pit of crossroads, then buffer down
            dungeon4_puddle_before_crossroads.connect(after_double_lock, AND(r.pit_buffer_boots, HOOKSHOT), id="fn") # boots bonk across the water bottom wall to the bottom left corner, then hookshot up
            north_crossroads.connect(entrance, AND(r.pit_buffer_boots, r.hookshot_spam_pit), id="fo") # pit buffer into wall of the first pit, then boots bonk towards the top and hookshot spam to get across (easier with Piece of Power)
            before_miniboss.connect(north_crossroads, AND(r.shaq_jump, r.hookshot_clip_block), id="fp") # push block left of keyblock up, then shaq jump off the left wall and pause buffer to land on keyblock. 
            before_miniboss.connect(north_crossroads, AND(OR(BOMB, BOW), r.hookshot_clip_block), id="fq") # split zol for more entities, and clip through the block left of keyblock by hookshot spam
            to_the_nightmare_key.connect(left_water_area, AND(FLIPPERS, r.boots_bonk), id="fr") # Use flippers for puzzle and boots bonk to get through 2d section
            before_boss.connect(left_water_area, r.pit_buffer_boots, id="fs") # boots bonk across bottom wall then boots bonk to the platform before boss door
            
        self.entrance = entrance
        self.final_room = boss


class NoDungeon4:
    def __init__(self, options, world_setup, r):
        entrance = Location("D4 Entrance", dungeon=4)
        Location(dungeon=4).add(HeartContainer(0x166), Instrument(0x162)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[3]])

        self.entrance = entrance
