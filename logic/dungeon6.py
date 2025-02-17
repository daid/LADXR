from .requirements import *
from .location import Location
from locations.all import *


class Dungeon6:
    def __init__(self, options, world_setup, r, *, raft_game_chest=True):
        entrance = Location("D6 Entrance", dungeon=6)
        Location(dungeon=6).add(DungeonChest(0x1CF)).connect(entrance, OR(r.enemy_requirements["WIZROBE"], COUNT(POWER_BRACELET, 2)), id="hj") # 50 rupees
        elephants_heart_chest = Location(dungeon=6).add(DungeonChest(0x1C9)).connect(entrance, COUNT(POWER_BRACELET, 2), id="hk") # 100 rupees start
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=6).add(OwlStatue(0x1BB)).connect(entrance, STONE_BEAK6, id="hl")

        # Power bracelet chest
        bracelet_chest = Location(dungeon=6).add(DungeonChest(0x1CE)).connect(entrance, AND(BOMB, FEATHER, r.enemy_requirements["HIDING_ZOL"], r.enemy_requirements["MINI_MOLDORM"], r.enemy_requirements["WIZROBE"]), id="hm")

        # left side
        Location(dungeon=6).add(DungeonChest(0x1C0)).connect(entrance, AND(POWER_BRACELET, r.enemy_requirements["WIZROBE"]), id="hn") # 3 wizrobes raised blocks don't need to hit the switch
        left_side = Location(dungeon=6).add(DungeonChest(0x1B9)).add(DungeonChest(0x1B3)).connect(entrance, AND(POWER_BRACELET, OR(BOMB, BOOMERANG)), id="ho")
        Location(dungeon=6).add(DroppedKey(0x1B4)).connect(left_side, OR(r.enemy_requirements["WIZROBE"], BOW), id="hp") # 2 wizrobe drop key, allow bow as only 2
        top_left = Location(dungeon=6).add(DungeonChest(0x1B0)).connect(left_side, COUNT(POWER_BRACELET, 2), id="hq") # top left chest horseheads
        if raft_game_chest:
            Location().add(Chest(0x06C)).connect(top_left, POWER_BRACELET, id="hr")  # seashell chest in raft game

        # right side
        to_miniboss = Location("D6 Before Miniboss", dungeon=6).connect(entrance, KEY6, id="hs")
        miniboss_room = Location("D6 Miniboss Room", dungeon=6).connect(to_miniboss, BOMB, id="ht")
        miniboss = Location("D6 After Miniboss", dungeon=6).connect(miniboss_room, r.miniboss_requirements[world_setup.miniboss_mapping[5]], id="hu")
        lower_right_side = Location(dungeon=6).add(DungeonChest(0x1BE)).connect(entrance, AND(r.enemy_requirements["WIZROBE"], COUNT(POWER_BRACELET, 2)), id="hv") # waterway key
        medicine_chest = Location(dungeon=6).add(DungeonChest(0x1D1)).connect(lower_right_side, FEATHER, id="hw") # ledge chest medicine
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            lower_right_owl = Location(dungeon=6).add(OwlStatue(0x1D7)).connect(lower_right_side, AND(POWER_BRACELET, STONE_BEAK6), id="hx")

        center_1 = Location(dungeon=6).add(DroppedKey(0x1C3)).connect(miniboss, AND(COUNT(POWER_BRACELET, 2), FEATHER), id="hy") # tile room key drop
        center_2_and_upper_right_side = Location(dungeon=6).add(DungeonChest(0x1B1)).connect(center_1, AND(COUNT(POWER_BRACELET, 2), PEGASUS_BOOTS, r.enemy_requirements["POLS_VOICE"], KEY6, FOUND(KEY6, 2)), id="hz") # top right chest horseheads
        boss_key = Location(dungeon=6).add(DungeonChest(0x1B6))
        center_2_and_upper_right_side.connect(boss_key, AND(HOOKSHOT, POWER_BRACELET, r.miniboss_requirements["DODONGO"], KEY6, FOUND(KEY6, 3)), one_way=True, id="i0")
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=6).add(OwlStatue(0x1B6)).connect(boss_key, STONE_BEAK6, id="i1")

        boss_room = Location("D6 Boss Room", dungeon=6).connect(center_1, AND(NIGHTMARE_KEY6, OR(AND(r.enemy_requirements["HIDING_ZOL"], r.enemy_requirements["WIZROBE"]), SHIELD)), id="i2")
        boss = Location(dungeon=6).add(HeartContainer(0x1BC), Instrument(0x1b5)).connect(boss_room, r.boss_requirements[world_setup.boss_mapping[5]], id="i3")

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            bracelet_chest.connect(entrance, AND(BOMB, r.enemy_requirements["HIDING_ZOL"], r.enemy_requirements["MINI_MOLDORM"], r.enemy_requirements["WIZROBE"]), id="i4") # get through 2d section by "fake" jumping to the ladders
            center_1.connect(miniboss, AND(COUNT(POWER_BRACELET, 2), r.boots_dash_2d), id="i5") # use a boots dash to get over the platforms
            center_2_and_upper_right_side.connect(center_1, AND(COUNT(POWER_BRACELET, 2), r.damage_boost, r.enemy_requirements["POLS_VOICE"], FOUND(KEY6, 2)), id="i6") # damage_boost past the mini_thwomps
            
        if options.logic == 'glitched' or options.logic == 'hell':
            elephants_heart_chest.connect(entrance, BOMB, id="i7") # kill moldorm on screen above wizrobes, then bomb trigger on the right side to break elephant statue to get to the second chest
            entrance.connect(left_side, AND(POWER_BRACELET, r.super_jump_feather), one_way=True, id="i8") # path from entrance to left_side: use superjumps to pass raised blocks
            lower_right_side.connect(center_2_and_upper_right_side, r.super_jump, one_way=True, id="i9") # path from lower_right_side to center_2:  superjump from waterway towards dodongos. superjump next to corner block, so weapons added
            center_1.connect(miniboss, AND(r.bomb_trigger, OR(r.boots_dash_2d, FEATHER)), id="ia") # bomb trigger the elephant statue after the miniboss
            center_2_and_upper_right_side.connect(center_1, AND(POWER_BRACELET, r.shaq_jump), one_way=True, id="ib") # going backwards from dodongos, use a shaq jump to pass by keyblock at tile room
            boss_key.connect(lower_right_side, AND(POWER_BRACELET, r.super_jump_feather), id="ic") # superjump from waterway to the left.

        if options.logic == 'hell':
            entrance.connect(left_side, AND(POWER_BRACELET, r.boots_superhop), one_way=True, id="id") # can boots superhop off the top right corner in 3 wizrobe raised blocks room
            entrance.connect(left_side, AND(POWER_BRACELET, r.stun_mask_mimic, r.throw_enemy), one_way=True, id="ie") # stun mask mimic, then pick it up and throw it against the top wall so it lands on top of the switch with enough delay to get past the top raised blocks
            medicine_chest.connect(lower_right_side, r.boots_superhop, id="if") # can boots superhop off the top wall with bow or magic rod
            center_1.connect(miniboss, AND(r.damage_boost_special, OR(r.bomb_trigger, COUNT(POWER_BRACELET, 2))), id="ig") # use a double damage boost from the sparks to get across (first one is free, second one needs to buffer while in midair for spark to get close enough)
            lower_right_side.connect(center_2_and_upper_right_side, r.super_jump_feather, one_way=True, id="ih") # path from lower_right_side to center_2:  superjump from waterway towards dodongos. superjump next to corner block is super tight to get enough horizontal distance
            
        self.entrance = entrance
        self.final_room = boss


class NoDungeon6:
    def __init__(self, options, world_setup, r):
        entrance = Location("D6 Entrance", dungeon=6)
        Location(dungeon=6).add(HeartContainer(0x1BC), Instrument(0x1b5)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[5]])
        self.entrance = entrance
