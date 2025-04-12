from .requirements import *
from .location import Location
from locations.all import *


class Dungeon4:
    def __init__(self, options, world_setup, r):

        # locations
        entrance = Location("D4 Entrance", dungeon=4)
        entrance_chest1 = Location(dungeon=4).add(DungeonChest(0x179)) # beak
        entrance_chest2 = Location(dungeon=4).add(DungeonChest(0x16A)) # map
        spark_beetle_room = Location("D4 Room East of Entrance", dungeon=4)
        spark_beetle_room_chest3 = Location(dungeon=4).add(DungeonChest(0x178)) # compass
        crystal_room = Location("D4 Crystal Room", dungeon=4)
        crystal_room_chest4 = Location(dungeon=4).add(DungeonChest(0x17B)) # small key
        east_crossroads = Location("D4 East of Crossroads", dungeon=4)
        east_crossroads_chest5 = Location(dungeon=4).add(DungeonChest(0x171)) # small key
        east_crossroads_chest6 = Location(dungeon=4).add(DungeonChest(0x165)) # small key
        west_statue_room = Location("D4 Statue Room SW", dungeon=4)
        north_statue_room = Location("D4 Statue Room NE", dungeon=4)
        south_crossroads = Location("D4 South of Crossroads", dungeon=4)
        south_crossroads_chest7 = Location(dungeon=4).add(DungeonChest(0x175)) # 50 rupees
        north_crossroads = Location("D4 North of Crossroads", dungeon=4)
        before_miniboss = Location("D4 Before Miniboss", dungeon=4)
        before_miniboss_owl1 = Location(dungeon=4).add(OwlStatue(0x16F)) # hint
        before_miniboss_zol_clear = Location("D4 Pit Drop Spawned", dungeon=4).add(KeyLocation("D4_PITKEY"))
        before_miniboss_pit = Location("D4 Pit Before Miniboss", dungeon=4)
        before_miniboss_stairs = Location("D4 Stairs Before Miniboss", dungeon=4)
        sidescroller_pit = Location("D4 Sidescroller Pit Entrance", dungeon=4)
        sidescroller_stairs = Location("D4 Sidescroller Ladder Entrance", dungeon=4)
        sidescroller_drop1 = Location(dungeon=4).add(DroppedKey(0x169)) # small key
        before_miniboss_chest8 = Location(dungeon=4).add(DungeonChest(0x16E)) # 50 rupees
        south_tile_puzzle = Location("D4 Water Tektite Area", dungeon=4)
        south_tile_puzzle_chest9 = Location(dungeon=4).add(DungeonChest(0x16D)) # gel chest
        south_tile_puzzle_chest10 = Location(dungeon=4).add(DungeonChest(0x168)) # small key
        miniboss_room = Location("D4 Miniboss Room", dungeon=4)
        after_miniboss = Location("D4 After Miniboss", dungeon=4)
        flippers_room = Location("D4 Fireball Statue Room", dungeon=4)
        north_tile_puzzle = Location("D4 North Tile Puzzle", dungeon=4)
        #TODO: tile_puzzle_clue = Location("D4 Tile Puzzle Cluee", dungeon=4).add(KeyLocation("D4_PUZZLE_CLUE"))
        flippers_room_chest11 = Location(dungeon=4).add(DungeonChest(0x160)) # flippers
        before_a_passage = Location("D4 Puzzle Stairs Spawn", dungeon=4)
        after_a_passage = Location("D4 Boss Key Ledge", dungeon=4)
        after_a_passage_chest12 = Location(dungeon=4).add(DungeonChest(0x176)) # nightmare key
        before_b_passage = Location("D4 Before Boss Passageway", dungeon=4)
        outside_b_passage_keyblock = Location("D4 Flying Heart Room", dungeon=4)
        outside_b_passage_shallows = Location("D4 Shallow Water By Keyblock", dungeon=4)
        after_b_passage = Location("D4 Before Boss Door", dungeon=4)
        pre_boss = Location("D4 Before Boss Staircase", dungeon=4)
        boss_room = Location("D4 Boss Room", dungeon=4)
        boss_room_drop2 = Location(dungeon=4).add(HeartContainer(0x166)).add(KeyLocation("D4_BOSS_CLEAR")) # heart container & instrument room door flag
        instrument = Location("D4 Instrument Room", dungeon=4).add(Instrument(0x162)) # surf harp

        # owl statues
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            before_miniboss.connect(before_miniboss_owl1, STONE_BEAK4)

        # connections
        # entrance
        entrance.connect((entrance_chest1, entrance_chest2), back=False)
        entrance.connect(spark_beetle_room, AND(r.enemy_requirements["SPIKED_BEETLE"], r.enemy_requirements["ZOL"]))
        spark_beetle_room.connect(spark_beetle_room_chest3, back=False)
        spark_beetle_room.connect(crystal_room, AND(r.enemy_requirements["SPIKED_BEETLE"], r.enemy_requirements["ZOL"]), back=False)
        crystal_room.connect(crystal_room_chest4, SWORD, back=False)
        # crossroads
        entrance.connect(east_crossroads, AND(FEATHER, PEGASUS_BOOTS))
        east_crossroads.connect(east_crossroads_chest5, BOMB, back=False)
        east_crossroads.connect(east_crossroads_chest6, OR(BOMB, FLIPPERS), back=False)
        spark_beetle_room.connect(west_statue_room, FOUND(KEY4, 1), back=FOUND(KEY4, 5))
        west_statue_room.connect(north_statue_room, OR(FEATHER, FLIPPERS))
        north_statue_room.connect(south_crossroads, FOUND(KEY4, 2), back=FOUND(KEY4, 4))
        south_crossroads.connect(south_crossroads_chest7, FLIPPERS, back=False)
        south_crossroads.connect(north_crossroads, AND(FEATHER, PEGASUS_BOOTS))
        north_crossroads.connect(before_miniboss, FOUND(KEY4, 3))
        # miniboss
        before_miniboss.connect(before_miniboss_zol_clear, r.enemy_requirements["ZOL"], back=False) # kill zol to get key drop in logic
        before_miniboss.connect(outside_b_passage_shallows, OR(FLIPPERS, HOOKSHOT, AND(FEATHER, PEGASUS_BOOTS)), back=OR(FLIPPERS, AND(FEATHER, PEGASUS_BOOTS)))
        before_miniboss.connect(before_miniboss_chest8, FLIPPERS, back=False)
        before_miniboss.connect(south_tile_puzzle, OR(FEATHER, FLIPPERS))
        before_miniboss.connect(north_tile_puzzle, FLIPPERS)
        before_miniboss.connect(miniboss_room, FOUND(KEY4, 5), back=False)
        before_miniboss.connect(before_miniboss_stairs)
        before_miniboss_stairs.connect(sidescroller_stairs)
        sidescroller_stairs.connect(sidescroller_drop1, AND("D4_PITKEY", FLIPPERS), back=False)
        before_miniboss_pit.connect(sidescroller_pit, back=False) # connects pit to sidescroller, the superjump remains in glitched logic
        sidescroller_pit.connect(sidescroller_stairs, FLIPPERS, back=False) # be able to fall into sidescroller and logically exit ladder
        miniboss_room.connect((entrance, before_miniboss, after_miniboss), r.miniboss_requirements[world_setup.miniboss_mapping[3]], back=False) # miniboss portal and both exits
        after_miniboss.connect((miniboss_room, flippers_room), POWER_BRACELET, back=False) #TODO: REMOVE and it's in casual logic statement
        flippers_room.connect((after_miniboss, north_tile_puzzle), r.enemy_requirements["ZOL"], back=False)
        flippers_room.connect(flippers_room_chest11, back=False)
        north_tile_puzzle.connect((flippers_room, south_tile_puzzle), back=False) #TODO: REPLACE with below
        #TODO: north_tile_puzzle.connect((tile_puzzle_clue, flippers_room, south_tile_puzzle), back=False)
        # west
        south_tile_puzzle.connect((south_tile_puzzle_chest9, south_tile_puzzle_chest10), back=False)
        south_tile_puzzle.connect(before_a_passage, OR(AND(FEATHER, PEGASUS_BOOTS), FLIPPERS), back=False) #TODO: REMOVE and it's in casual logic statement
        before_a_passage.connect(after_a_passage, FEATHER)
        after_a_passage.connect((south_tile_puzzle, after_a_passage_chest12), back=False)
        south_tile_puzzle.connect(outside_b_passage_keyblock, FLIPPERS)
        outside_b_passage_keyblock.connect(before_b_passage, FOUND(KEY4, 5))
        # boss
        after_b_passage.connect(pre_boss, NIGHTMARE_KEY4) #NOTE: in stairs shuffle if you didn't have nightmare key you could wall clip in the doorway and get out without nightmare key - undecided
        pre_boss.connect(boss_room) # stairs to boss
        boss_room.connect(boss_room_drop2, r.boss_requirements[world_setup.boss_mapping[3]], back=False)
        pre_boss.connect(instrument, "D4_BOSS_CLEAR", back=False)

        if options.logic == "casual":
            #TODO: after_miniboss.connect((miniboss_room, flippers_room), POWER_BRACELET, back=False)
            before_b_passage.connect(after_b_passage, AND(r.attack_hookshot, FLIPPERS)) #TODO: CHANGE to AND(r.enemy_requirements["CHEEP_CHEEP_HORIZONTAL"], r.enemy_requirements["CHEEP_CHEEP_VERTICAL"])
            #TODO: south_tile_puzzle.connect(before_a_passage, AND("D4_PUZZLE_CLUE", OR(AND(FEATHER, PEGASUS_BOOTS), FLIPPERS)), back=False)
        else:
            #TODO: after_miniboss.connect((miniboss_room, flippers_room), back=False)
            before_b_passage.connect(after_b_passage, AND(r.attack_hookshot, FLIPPERS)) #TODO: REMOVE r.attack_hookshot under normal logic since you can just swim past
            #TODO: south_tile_puzzle.connect(before_a_passage, OR(AND(FEATHER, PEGASUS_BOOTS), FLIPPERS), back=False)

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            for location in (entrance, east_crossroads):
                location.connect((north_crossroads, south_crossroads), r.tight_jump) # jump diagonally over crossroads
            east_crossroads.connect(east_crossroads_chest6, r.tight_jump, back=False) # jump around the bombable block
            south_crossroads.connect(south_crossroads_chest7, r.tight_jump, back=False) # precise feather jump is enough to cross the water without flippers
            before_miniboss.connect(before_miniboss_zol_clear, r.throw_pot, back=False) #TODO: REMOVE and replace with below
            #TODO: before_miniboss.connect(before_miniboss_zol_clear, back=False) # bait zols to drown to spawn key
            before_miniboss.connect(before_miniboss_chest8, r.tight_jump) # precise feather jump is enough to cross the water without flippers
            after_miniboss.connect(flippers_room, back=False) #TODO: REMOVE and let it be in casual/normal statement
            sidescroller_drop1.connect((before_miniboss, sidescroller_stairs), False, back=AND("D4_PITKEY", BOOMERANG)) # boomerang item before falls in pit or from the sidescroller by walking off ledge and throwing the boomerang
            sidescroller_pit.connect(sidescroller_drop1, "D4_PITKEY", back=False) # hold left after falling in pit to grab the drop before it touches the water #NOTE: this particular connection shows up in magpie as glitched still for some reason?
            south_tile_puzzle.connect(before_a_passage, r.tight_jump, back=False) # precise feather jump is enough to reach the top left puzzle tile without flippers
            south_tile_puzzle.connect(after_b_passage, r.tight_jump) # tight diagonal feather jump in or out of pre boss door room
            #TODO: after_a_passage.connect(before_a_passage, back=False) # diagonal walk off the stairs in to fake jump over the little ledge then bait and walk past thwomps
            
        if options.logic == 'glitched' or options.logic == 'hell':
            #TODO: entrance.connect(west_statue_room, r.super_jump_feather, back=False) # super jump off the tile to the right of the staircase to below statues [stair shuffle prep]
            east_crossroads.connect(east_crossroads_chest5, AND(r.sideways_block_push, FLIPPERS), back=False) # sideways block push while swimming to skip bombs
            #TODO: before_miniboss.connect(north_crossroads, r.super_jump_feather, back=False) # push block down and superjump to the right [stair shuffle prep]
            before_miniboss.connect(before_miniboss_pit, r.super_jump_feather, back=False) # superjump into pits outside miniboss
            before_miniboss.connect(north_tile_puzzle, r.jesus_jump) # use jesus jump to transition over the water left of miniboss
            #TODO: before_miniboss.connect(outside_b_passage_shallows, r.jesus_jump) # jesus jump to shallow water to the right of the boss passage staircase
            #TODO: south_tile_puzzle.connect(outside_b_passage_keyblock, r.jesus_jump) # jesus jump to get to the button [stair shuffle prep]
            #TODO: south_tile_puzzle.connect(after_a_passage, AND(POWER_BRACELET, r.super_poke), back=False) # wall clip in the two stalfos room, lift pots, then superjump and knockback off the peahat to get on ledge [stair shuffle prep]
            #TODO: outside_b_passage_shallows.connect(before_b_passage, r.shaq_jump, back=AND(r.hookshot_clip, r.super_jump_feather)) # to get out, hookshot clip into the top wall, then superjump down. to get in, it's precise shaq jump, but usually have to chain a few together

        if options.logic == 'hell':
            #TODO: entrance.connect(after_a_passage, r.super_bump, back=False) # wall clip and super bump off tektite to land on boss key ledge
            #TODO: entrance.connect((south_tile_puzzle, before_miniboss), False, back=OR(r.super_poke, r.super_bump)) # super jump and rebound off peahat to entrance
            north_crossroads.connect((entrance, east_crossroads), AND(r.pit_buffer_itemless, r.hookshot_spam_pit), back=AND(r.pit_buffer_boots, r.hookshot_spam_pit)) # left <> right: pit buffer, bonk across gap, hookshot spam to finish | sides > top: pit buffer, bonk to center, hookshot spam up | top > sides: pit buffer down, hookshot spam across
            north_crossroads.connect(south_crossroads, r.pit_buffer_itemless, back=False) #logic prep for staircase rando
            south_crossroads.connect((entrance, east_crossroads), AND(OR(BOMB, BOW), r.hookshot_clip_block), back=AND(r.pit_buffer_itemless, r.pit_buffer_boots)) #TODO: REPLACE with below
            #TODO:south_crossroads.connect((entrance, east_crossroads), AND(OR(BOMB, BOW), r.hookshot_clip_block), back=AND(r.pit_buffer_itemless, OR(r.pit_buffer_boots, r.hookshot_spam_pit))) # boots buffer or hookshot spam to center of pit and buffer down, return with splitting zols and hookshot clipping through block
            east_crossroads.connect(east_crossroads_chest5, AND(r.sideways_block_push, OR(r.jesus_buffer, r.jesus_jump)), back=False) # use feather to water clip into the top right corner of the bombable block, and sideways block push to gain access. Can boots bonk of top right wall, then water buffer to top of chest and boots bonk to water buffer next to chest
            west_statue_room.connect(north_statue_room, r.boots_bonk) # two boots bonks to cross the water tiles
            south_crossroads.connect(south_crossroads_chest7, AND(r.pit_buffer_boots, HOOKSHOT), back=False) # boots bonk across the water bottom wall to the bottom left corner, then hookshot up #TODO: investigate hookshot wrap method
            north_crossroads.connect(before_miniboss, AND(OR(AND(r.shaq_jump, BOMB, BOW), r.hookshot_clip_block), AND(r.shaq_jump, r.super_bump)), back=False) # push block left of keyblock up, then shaq jump off the left wall, push another block up, and hookshot clip through | split zol for more entities, and clip through the block left of keyblock by hookshot spam | shaq jump off pushblock, then shield bump/ pause buffer in such a way to land in push block
            #TODO: before_miniboss.connect(north_tile_puzzle, AND(r.boots_bonk, r.jesus_buffer, r.hookshot_buffer), back=False) # boots bonk and jesus buffer to screen transision, then hookshot across to stop drowning
            #TODO: before_miniboss.connect(south_tile_puzzle, AND(r.boots_bonk, r.jesus_buffer, r.hookshot_buffer) # bonk on wall above puddle chest, buffer all the way to screen transition, hookshot can get you above water after screen transition to restart buffer [stair shuffle prep]
            #TODO: south_tile_puzzle.connect(north_tile_puzzle, r.hookshot_clip_block, back=False) # facing downwards at the pushblock in statue+spark room, spam hookshot while spark passes you by [stair shuffle prep]
            #TODO: outside_b_passage_shallows.connect(before_b_passage, r.hookshot_clip_block, back=False) # clip into the block, then hookshot clip off a tektite [stair shuffle prep]
            #TODO: outside_b_passage_shallows.connect(before_miniboss_chest8, AND(r.boots_bonk, r.jesus_buffer), back=False) # boots bonk to one pixel right of the chest, pause buffer until you are below the chest, and hold left as you unpause to step onto shallow water
            #TODO: outside_b_passage_keyblock.connect(south_tile_puzzle, AND(r.jesus_buffer, r.hookshot_buffer), back=False) # start a buffer by the button to get to the shallow water below [stair shuffle prep]
            #TODO: south_tile_puzzle.connect(after_a_passage, r.super_poke, back=False) # superjump and knockback off the peahat twice to get on ledge
            before_a_passage.connect(after_a_passage, r.boots_bonk_2d_hell, back=False) # boots bonk to get through 2d section
            south_tile_puzzle.connect(after_b_passage, r.pit_buffer_boots) # boots bonk across bottom wall then boots bonk to the platform before boss door
            
        self.entrance = entrance
        self.final_room = instrument


class NoDungeon4:
    def __init__(self, options, world_setup, r):
        entrance = Location("D4 Entrance", dungeon=4)
        Location(dungeon=4).add(HeartContainer(0x166), Instrument(0x162)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[3]])

        self.entrance = entrance
