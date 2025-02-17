from .requirements import *
from .location import Location
from locations.all import *


class Dungeon7:
    def __init__(self, options, world_setup, r):
        entrance = Location("D7 Entrance", dungeon=7)
        first_key = Location(dungeon=7).add(DroppedKey(0x210)).connect(entrance, r.enemy_requirements["LIKE_LIKE"], id="ij")
        topright_pillar_area = Location("D7 Ball Room", dungeon=7).connect(entrance, KEY7, id="ik")
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=7).add(OwlStatue(0x216)).connect(topright_pillar_area, STONE_BEAK7, id="il")
        topright_pillar = Location(dungeon=7).add(DungeonChest(0x212)).connect(topright_pillar_area, POWER_BRACELET, id="im")  # map chest
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=7).add(OwlStatue(0x204)).connect(topright_pillar_area, STONE_BEAK7, id="in")
        topright_pillar_area.add(DungeonChest(0x209))  # stone slab chest can be reached by dropping down a hole
        three_of_a_kind_north = Location(dungeon=7).add(DungeonChest(0x211)).connect(topright_pillar_area, AND(OR(FEATHER, r.hit_switch), r.enemy_requirements["THREE_OF_A_KIND"]), id="io")  # compass chest; either hit the switch, or have feather to fall on top of raised blocks. No bracelet because ball does not reset
        bottomleftF2_area = Location("D7 Hinox Area", dungeon=7).connect(topright_pillar_area, r.hit_switch, id="ip")  # area with hinox, be able to hit a switch to reach that area
        topleftF1_chest = Location(dungeon=7).add(DungeonChest(0x201)) # top left chest on F1
        bottomleftF2_area.connect(topleftF1_chest, None, one_way = True, id="iq")  # drop down in left most holes of hinox room or tile room
        Location(dungeon=7).add(DroppedKey(0x21B)).connect(bottomleftF2_area, r.miniboss_requirements["HINOX"], id="ir") # hinox drop key
        # Most of the dungeon can be accessed at this point.
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            bottomleft_owl = Location(dungeon=7).add(OwlStatue(0x21C)).connect(bottomleftF2_area, AND(BOMB, STONE_BEAK7), id="is")
        nightmare_key = Location(dungeon=7).add(DungeonChest(0x224)).connect(bottomleftF2_area, r.miniboss_requirements[world_setup.miniboss_mapping[6]], id="it") # nightmare key after the miniboss
        mirror_shield_chest = Location(dungeon=7).add(DungeonChest(0x21A)).connect(bottomleftF2_area, r.hit_switch, id="iu")  # mirror shield chest, need to be able to hit a switch to reach or
        bottomleftF2_area.connect(mirror_shield_chest, AND(KEY7, FOUND(KEY7, 3)), one_way = True, id="iv") # reach mirror shield chest from hinox area by opening keyblock
        toprightF1_chest = Location(dungeon=7).add(DungeonChest(0x204)).connect(bottomleftF2_area, r.hit_switch, id="iw")  # chest on the F1 right ledge. Added attack_hookshot since switch needs to be hit to get back up
        final_pillar_area = Location(dungeon=7).add(DungeonChest(0x21C)).connect(bottomleftF2_area, AND(BOMB, HOOKSHOT, r.enemy_requirements["THREE_OF_A_KIND"]), id="ix")  # chest that needs to spawn to get to the last pillar
        final_pillar = Location("D7 Final Pillar", dungeon=7).connect(final_pillar_area, POWER_BRACELET, id="iy") # decouple chest from pillar

        beamos_horseheads_area = Location("D7 After Boss Door", dungeon=7).connect(final_pillar, NIGHTMARE_KEY7, id="iz") # area behind boss door
        beamos_horseheads = Location(dungeon=7).add(DungeonChest(0x220)).connect(beamos_horseheads_area, POWER_BRACELET, id="j0") # 100 rupee chest / medicine chest (DX) behind boss door
        pre_boss = Location("D7 Before Boss", dungeon=7).connect(beamos_horseheads_area, HOOKSHOT, id="j1") # raised plateau before boss staircase
        boss = Location(dungeon=7).add(HeartContainer(0x223), Instrument(0x22c)).connect(pre_boss, r.boss_requirements[world_setup.boss_mapping[6]], id="j2")

        if options.dungeon_items not in {'localnightmarekey', 'keysanity', 'keysy', 'smallkeys'}:
            first_key.items[0].forced_item = KEY7
            
        if options.logic == 'glitched' or options.logic == 'hell':
            topright_pillar_area.connect(entrance, r.super_jump_sword, id="j4") # superjump in the center to get on raised blocks, superjump in switch room to right side to walk down. center superjump has to be low so sword added
            toprightF1_chest.connect(topright_pillar_area, r.super_jump_feather, id="j5") # superjump from F1 switch room
            topleftF2_area = Location("D7 Tile Room", dungeon=7).connect(topright_pillar_area, r.super_jump_feather, id="j6") # superjump in top left pillar room over the blocks from right to left, to reach tile room
            topleftF2_area.connect(topleftF1_chest, None, one_way = True, id="j7") # fall down tile room holes on left side to reach top left chest on ground floor
            topleftF1_chest.connect(bottomleftF2_area, r.boots_jump, one_way = True, id="j8") # without hitting the switch, jump on raised blocks at f1 pegs chest (0x209), and boots jump to stairs to reach hinox area
            final_pillar_area.connect(bottomleftF2_area, AND(r.sideways_block_push, OR(r.enemy_requirements["THREE_OF_A_KIND"], POWER_BRACELET)), id="j9") # sideways block push to get to the chest and pillar, kill requirement for 3 of a kind enemies to access chest. Assumes you do not get ball stuck on raised pegs for bracelet path
            if options.owlstatues == "both" or options.owlstatues == "dungeon":
                bottomleft_owl.connect(bottomleftF2_area, AND(r.sideways_block_push, STONE_BEAK7), id="ja") # sideways block push to get to the owl statue
            final_pillar.connect(bottomleftF2_area, r.bomb_trigger, id="jb") # bomb trigger pillar
            pre_boss.connect(final_pillar, r.super_jump_feather, id="jc") # superjump on top of goomba to extend superjump to boss door plateau
            pre_boss.connect(beamos_horseheads_area, None, one_way=True, id="jd") # can drop down from raised plateau to beamos horseheads area
            
        if options.logic == 'hell':
            topright_pillar_area.connect(entrance, r.super_jump_feather, id="je") # superjump in the center to get on raised blocks, has to be low
            topright_pillar_area.connect(entrance, r.boots_superhop, id="jf") # boots superhop in the center to get on raised blocks
            toprightF1_chest.connect(topright_pillar_area, r.boots_superhop, id="jg") # boots superhop from F1 switch room
            pre_boss.connect(final_pillar, r.boots_superhop, id="jh") # boots superhop on top of goomba to extend superhop to boss door plateau
        
        self.entrance = entrance
        self.final_room = boss


class NoDungeon7:
    def __init__(self, options, world_setup, r):
        entrance = Location("D7 Entrance", dungeon=7)
        boss = Location(dungeon=7).add(HeartContainer(0x223), Instrument(0x22c)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[6]])

        self.entrance = entrance
