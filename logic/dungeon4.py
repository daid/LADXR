from .requirements import *
from .location import Location
from locations.all import *


class Dungeon4:
    def __init__(self, options, world_setup, r):

        # locations
        entrance = Location("D4 Entrance", dungeon=4)
        entrance_chest1 = Location(dungeon=4).add(DungeonChest(0x179)) # beak
        entrance_chest2 = Location(dungeon=4).add(DungeonChest(0x16A)) # map
        east_of_entrance = Location("D4 East of Entrance", dungeon=4)
        east_of_entrance_chest3 = Location(dungeon=4).add(DungeonChest(0x178)) # compass
        crystal_room = Location("D4 Crystal Room", dungeon=4)
        crystal_room_chest4 = Location(dungeon=4).add(DungeonChest(0x17B)) # small key
        east_crossroads = Location("D4 East of Crossroads", dungeon=4)
        east_crossroads_chest5 = Location(dungeon=4).add(DungeonChest(0x171)) # small key
        east_crossroads_chest6 = Location(dungeon=4).add(DungeonChest(0x165)) # small key
        west_statue_room = Location("D4 Statue Room West Door", dungeon=4)
        north_statue_room = Location("D4 Statue Room North Door", dungeon=4)
        south_crossroads = Location("D4 South of Crossroads", dungeon=4)
        south_crossroads_chest7 = Location(dungeon=4).add(DungeonChest(0x175)) # 50 rupees
        north_crossroads = Location("D4 North of Crossroads", dungeon=4)
        before_miniboss = Location("D4 Before Miniboss", dungeon=4)
        sidescroller_drop1 = Location(dungeon=4).add(DroppedKey(0x169)) # small key
        before_miniboss_chest8 = Location(dungeon=4).add(DungeonChest(0x16E)) # 50 rupees
        south_tile_puzzle = Location("D4 Lower Tile Puzzle Area", dungeon=4)
        south_tile_puzzle_chest9 = Location(dungeon=4).add(DungeonChest(0x16D)) # gel chest
        south_tile_puzzle_chest10 = Location(dungeon=4).add(DungeonChest(0x168)) # key chest near the puzzle
        miniboss_room = Location("D4 Miniboss Room", dungeon=4)
        after_miniboss = Location("D4 After Miniboss", dungeon=4)
        flippers_room = Location("D4 Flippers Room", dungeon=4)
        north_tile_puzzle = Location("D4 Upper Tile Puzzle", dungeon=4)
        flippers_room_chest11 = Location(dungeon=4).add(DungeonChest(0x160)) # flippers
        before_a_passage = Location("D4 Puzzle Stairs Spawn", dungeon=4)
        after_a_passage = Location("D4 Boss Key Ledge", dungeon=4)
        after_a_passage_chest12 = Location(dungeon=4).add(DungeonChest(0x176)) # nightmare key
        before_b_passage = Location("D4 Before Boss Passageway", dungeon=4)
        outside_b_passage_keyblock = Location("D4 Outside Boss Passageway Keyblock", dungeon=4)
        outside_b_passage_shallows = Location("D4 Shallow Water By Boss Passageway", dungeon=4)
        after_b_passage = Location("D4 After Boss Passageway", dungeon=4)
        pre_boss_room = Location("D4 Before Boss Door", dungeon=4)
        pre_boss = Location("D4 Before Boss Stairs", dungeon=4)
        boss_room = Location("D4 Boss Room", dungeon=4).add(HeartContainer(0x166)) # heart container
        instrument = Location("D4 Instrument Room", dungeon=4).add(Instrument(0x162)) # surf harp

        # owl statues

        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=4).add(OwlStatue(0x16F)).connect(before_miniboss, STONE_BEAK4) # Before Miniboss <--> Spiked Beetle Owl

        # connections
        entrance.connect(entrance_chest1, None) # Entrance <--> Watery Statue Chest
        entrance.connect(entrance_chest2, None) # Entrance <--> NW of Boots Pit Ledge Chest
        entrance.connect(east_of_entrance, AND(r.enemy_requirements["SPIKED_BEETLE"], r.enemy_requirements["ZOL"])) # Entrance <--> East of Entrance
        east_of_entrance.connect(east_of_entrance_chest3, None) # East of Entrance <--> Two Spiked Beetle, Zol Chest
        east_of_entrance.connect(crystal_room, AND(r.enemy_requirements["SPIKED_BEETLE"], r.enemy_requirements["ZOL"])) # East of Entrance <--> Crystal Room
        crystal_room.connect(crystal_room_chest4, SWORD) # Crystal Room <--> Crystal Chest
        entrance.connect(east_crossroads, AND(FEATHER, PEGASUS_BOOTS)) # Entrance <--> East of Crossroads
        east_crossroads.connect(east_crossroads_chest5, BOMB) # East of Crossroads <--> Lower Bomb Locked Watery Chest
        east_crossroads.connect(east_crossroads_chest6, OR(BOMB, FLIPPERS)) # East of Crossroads <--> Upper Bomb Locked Watery Chest
        east_of_entrance.connect(west_statue_room, KEY4, one_way=True) # East of Entrance <--> Statue Room West Door
        west_statue_room.connect(east_of_entrance, AND(KEY4, FOUND(KEY4, 5)), one_way=True) # Statue Room West Door <--> East of Entrance
        west_statue_room.connect(north_statue_room, OR(FEATHER, FLIPPERS)) # Statue Room West Door <--> Statue Room North Door
        south_crossroads.connect(north_statue_room, AND(KEY4, FOUND(KEY4, 4)), one_way=True) # South of Crossroads <--> Statue Room North Door
        north_statue_room.connect(south_crossroads, AND(KEY4, FOUND(KEY4, 2)), one_way=True) # Statue Room North Door <--> South of Crossroads
        south_crossroads.connect(south_crossroads_chest7, FLIPPERS) # South of Crossroads <--> Peahat's Chest <--> South of Crossroads
        south_crossroads.connect(north_crossroads, AND(FEATHER, PEGASUS_BOOTS)) # South of Crossroads <--> North of Crossroads
        north_crossroads.connect(before_miniboss, AND(KEY4, FOUND(KEY4, 3))) # North of Crossroads <--> Before Miniboss
        before_miniboss.connect(sidescroller_drop1, AND(r.enemy_requirements["ZOL"], FLIPPERS)) # Before Miniboss <--> Pit Key
        before_miniboss.connect(before_miniboss_chest8, FLIPPERS) # Before Miniboss <--> Flipper Locked After Boots Pit Chest
        before_miniboss.connect(south_tile_puzzle, OR(FEATHER, FLIPPERS)) # Before Miniboss <--> Lower Tile Puzzle Area
        south_tile_puzzle.connect(south_tile_puzzle_chest9, None) # Lower Tile Puzzle Area <--> Spark Chest
        south_tile_puzzle.connect(south_tile_puzzle_chest10, None) # Lower Tile Puzzle Area <--> Blob Chest
        before_miniboss.connect(north_tile_puzzle, FLIPPERS) # Before Miniboss <--> Upper Tile Puzzle
        before_miniboss.connect(miniboss_room, AND(KEY4, FOUND(KEY4, 5))) # Before Miniboss <--> Miniboss Room - #TODO: change to one_way
        miniboss_room.connect(after_miniboss, r.miniboss_requirements[world_setup.miniboss_mapping[3]]) # Miniboss Room <--> After Miniboss #TODO: change to one_way
        after_miniboss.connect(flippers_room, POWER_BRACELET, one_way=True) # After Miniboss <--> Flippers Room
        flippers_room.connect(north_tile_puzzle, r.enemy_requirements["ZOL"]) # Flippers Room <--> Before Miniboss Room #TODO: change to one_way
        north_tile_puzzle.connect(flippers_room, None, one_way=True) # Flippers Room <--> Before Miniboss Room
        before_miniboss.connect(north_tile_puzzle, FLIPPERS) # Before Miniboss Room <--> Flippers Room
        #TODO: flippers_room.connect(after_miniboss, r.enemy_requirements["ZOL"], one_way=True) # [logic prep for staircase rando]
        #TODO: after_miniboss.connect(miniboss_room, POWER_BRACELET, one_way=True) # [logic prep for staircase rando]
        #TODO: miniboss_room.connect(before_miniboss, r.miniboss_requirements[world_setup.miniboss_mapping[3]], one_way=True) # [logic prep for staircase rando]
        flippers_room.connect(flippers_room_chest11, None) # Flippers Room <--> Flippers Chest
        north_tile_puzzle.connect(south_tile_puzzle, None, one_way=True)# Upper Tile Puzzle <--> Lower Tile Puzzle
        south_tile_puzzle.connect(before_a_passage, OR(AND(FEATHER, PEGASUS_BOOTS), FLIPPERS), one_way=True) # Lower Tile Puzzle Area <--> Puzzle Stairs Spawn
        before_a_passage.connect(after_a_passage, FEATHER, one_way=True) # Puzzle Stairs Spawn --> Boss Key Ledge
        after_a_passage.connect(after_a_passage_chest12, None) # Boss Key Ledge <--> Nightmare Key Ledge Chest
        after_a_passage.connect(south_tile_puzzle, None, one_way=True) # Boss Key Ledge <--> Lower Tile Puzzle Area
        south_tile_puzzle.connect(outside_b_passage_keyblock, FLIPPERS) # Lower Tile Puzzle Area <--> Outside Boss Passageway Keyblock
        outside_b_passage_keyblock.connect(before_b_passage, AND(KEY4, FOUND(KEY4, 5))) # Outside Boss Passageway Keyblock <--> Before Boss Passageway
        before_miniboss.connect(outside_b_passage_shallows, OR(FLIPPERS, HOOKSHOT, AND(FEATHER, PEGASUS_BOOTS))) # Before Miniboss Room <--> Outside Boss Passageway Pushblock
        before_b_passage.connect(after_b_passage, AND(r.attack_hookshot, FLIPPERS)) # Before Boss Passageway <--> After Boss Passageway #TODO: r.attack_hookshot not required. Move it to casual  or move flippers only method to hard
        after_b_passage.connect(pre_boss_room, None) # After Boss Passageway <--> Before Boss Door
        pre_boss_room.connect(pre_boss, NIGHTMARE_KEY4) # Before Boss Door <--> Boss Room
        pre_boss.connect(boss_room, None) # logic prep for staircase rando
        boss_room.connect(instrument, r.boss_requirements[world_setup.boss_mapping[3]]) # Boss Room <--> Instrument Room

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            entrance.connect(north_crossroads, r.tight_jump) # jump across the corners
            entrance.connect(south_crossroads, r.tight_jump) # jump across the corners
            north_crossroads.connect(east_crossroads, r.tight_jump) # jump across the corners
            south_crossroads.connect(east_crossroads, r.tight_jump) # jump across the corners
            east_crossroads.connect(east_crossroads_chest6, r.tight_jump) # jump around the bombable block
            south_crossroads.connect(south_crossroads_chest7, r.tight_jump) # With a tight jump feather is enough to cross the puddle without flippers
            before_miniboss.connect(sidescroller_drop1, AND(r.enemy_requirements["ZOL"], BOOMERANG)) # fall off the bridge and boomerang downwards before hitting the water to grab the item
            before_miniboss.connect(sidescroller_drop1, AND(r.throw_pot, FLIPPERS)) #TODO: replace with below
            #TODO: before_miniboss.connect(sidescroller_drop1, FLIPPERS) # let zols drown to spawn key
            before_miniboss.connect(before_miniboss_chest8, r.tight_jump) # With a tight jump feather is enough to cross the puddle without flippers
            after_miniboss.connect(flippers_room, None, one_way=True) # walk directly without pulling lever
            #TODO: after_miniboss.connect(miniboss_room, None, one_way=True) # [logic prep for auto-key logic] walk directly without pulling lever
            south_tile_puzzle.connect(before_a_passage, r.tight_jump) # With a tight jump feather is enough to reach the top left switch without flippers, or use flippers for puzzle and boots to get through 2d section
            south_tile_puzzle.connect(pre_boss_room, r.tight_jump) # jump from bottom right corner of boss door room
            
        if options.logic == 'glitched' or options.logic == 'hell':
            #TODO: entrance.connect(west_statue_room, r.super_jump_feather, one_way=True) # [logic prep for auto-key logic]
            east_crossroads.connect(east_crossroads_chest5, AND(r.sideways_block_push, FLIPPERS)) # sideways block push to skip bombs
            #TODO: before_miniboss.connect(north_crossroads, r.super_jump_feather, one_way=True) # [logic prep for staircase rando] - push block down and superjump to the right
            before_miniboss.connect(sidescroller_drop1, AND(r.super_jump_feather, OR(r.enemy_requirements["ZOL"], r.throw_pot))) #TODO: replace with below
            #TODO: before_miniboss.connect(sidescroller_drop1, r.super_jump_feather) # let zols drown to spawn key, superjump into pit, and press left get item
            before_miniboss.connect(north_tile_puzzle, r.jesus_jump) # use jesus jump to transition over the water left of miniboss #TODO: more granular connection
            #TODO: before_miniboss.connect(outside_b_passage_shallows, r.jesus_jump) # [logic prep for staircase rando] jesus jump
            #TODO: south_tile_puzzle.connect(outside_b_passage_keyblock, r.jesus_jump) # [logic prep for staircase rando] jesus jump
            #TODO: before_a_passage.connect(after_a_passage, AND(BRACELET, r.super_poke)) # [logic prep for staircase rando] lift pots, then superjump and knockback off the peahat twice to get on ledge
            #TODO: outside_b_passage_shallows.connect(before_b_passage, r.super_jump_feather) # [logic prep for staircase rando]

        if options.logic == 'hell':
            #TODO: entrance.connect(after_a_passage, AND(wall_clip, r.super_bump), one_way=True) # wall clip and super bump off tektite to land on boss key ledge
            entrance.connect(east_crossroads, AND(r.pit_buffer_boots, r.hookshot_spam_pit)) # pit buffer into block, bonk/jump across gap, and hookshot spam to get across
            entrance.connect(north_crossroads, AND(r.pit_buffer_boots, r.hookshot_spam_pit)) # pit buffer into block, bonk/jump up, and hookshot spam to get across (easier with Piece of Power)
            entrance.connect(south_crossroads, OR(r.pit_buffer_boots, AND(r.pit_buffer, r.hookshot_spam_pit))) # #TODO: change to AND(r.pit_buffer, OR(r.pit_buffer_boots, r.hookshot_spam_pit))
            #TODO: north_crossroads.connect(entrance, AND(r.pit_buffer, r.hookshot_spam_pit)) #logic prep for staircase rando
            #TODO: north_crossroads.connect(east_crossroads, AND(r.pit_buffer, r.hookshot_spam_pit)) #logic prep for staircase rando
            south_crossroads.connect(east_crossroads, AND(OR(BOMB, BOW), r.hookshot_clip_block), one_way=True) # split zols for more entities, and clip through the block against the right wall
            east_crossroads.connect(east_crossroads_chest5, AND(r.sideways_block_push, OR(r.jesus_buffer, r.jesus_jump))) # use feather to water clip into the top right corner of the bombable block, and sideways block push to gain access. Can boots bonk of top right wall, then water buffer to top of chest and boots bonk to water buffer next to chest
            west_statue_room.connect(north_statue_room, r.boots_bonk) # two boots bonks to cross the water gaps
            south_crossroads.connect(south_crossroads_chest7, AND(r.pit_buffer_boots, HOOKSHOT)) # boots bonk across the water bottom wall to the bottom left corner, then hookshot up
            north_crossroads.connect(before_miniboss, AND(r.shaq_jump, r.hookshot_clip_block), one_way=True) # push block left of keyblock up, then shaq jump off the left wall and pause buffer to land on keyblock and push up on the block above it then hookshot to clip through
            north_crossroads.connect(before_miniboss, AND(OR(BOMB, BOW), r.hookshot_clip_block), one_way=True) # split zol for more entities, and clip through the block left of keyblock by hookshot spam
            #TODO: south_tile_puzzle.connect(north_tile_puzzle, r.hookshot_clip_block, one_way=True) # [logic prep for staircase rando] facing downwards at the pushblock in statue+spark room, spam hookshot while spark passes you by
            #TODO: before_miniboss.connect(entrance, OR(r.super_poke, r.super_bump), one_way=True) # [logic prep for staircase rando] rebound off peahat to entrance
            #TODO: outside_b_passage_shallows.connect(before_b_passage, r.hookshot_clip_block) # logic prep for staircase rando
            #TODO: outside_b_passage_shallows.connect(before_miniboss_chest8, AND(r.jesus_buffer, TOADSTOOL)) # boots bonk to upper right of chest, buffer down, then hold left+toadstool to land on shallow water
            before_a_passage.connect(after_a_passage, AND(r.boots_bonk_2d_hell)) # Use flippers for puzzle and boots bonk to get through 2d section #TODO: move to hard, change to boots_bonk
            #TODO: before_a_passage.connect(after_a_passage, r.super_poke) # [logic prep for staircase rando] braceletless superjump and knockback off the peahat twice to get on ledge
            #TODO: before_a_passage.connect(entrance, OR(r.super_poke, r.super_bump), one_way=True) # [logic prep for staircase rando] rebound off peahat to entrance
            south_tile_puzzle.connect(pre_boss_room, r.pit_buffer_boots) # boots bonk across bottom wall then boots bonk to the platform before boss door
            
        self.entrance = entrance
        self.final_room = instrument


class NoDungeon4:
    def __init__(self, options, world_setup, r):
        entrance = Location("D4 Entrance", dungeon=4)
        Location(dungeon=4).add(HeartContainer(0x166), Instrument(0x162)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[3]])

        self.entrance = entrance
