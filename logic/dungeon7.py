from .requirements import *
from .location import Location
from locations.all import *


class Dungeon7:
    def __init__(self, options, world_setup, r):

        # locations
        entrance = Location("D7 Entrance", dungeon=7)
        entrance_drop1 = Location(dungeon=7).add(DroppedKey(0x210)) # small key
        before_a_stairs = Location("D7 Key Locked Staircase", dungeon=7)
        after_a_stairs = Location("D7 Ball Room", dungeon=7)
        after_a_stairs_switch = Location("D7 Pit Switch", dungeon=7).add(KeyLocation("SWITCH7B"))
        #TODO: after_a_stairs_switch_range = Location("D7 Pit Switch (Range)", dungeon=7).add(KeyLocation("SWITCH7B_RANGE")) NOTE: enable this when new switch logic is uncommented
        after_a_stairs_owl1 = Location(dungeon=7).add(OwlStatue(0x216))
        ball_access = Location("D7 Ball Access", dungeon=7).add(KeyLocation("D7_BALL"))
        before_b_stairs = Location("D7 1st Floor North Area", dungeon=7)
        before_b_stairs_owl2 = Location(dungeon=7).add(OwlStatue(0x204))
        before_b_stairs_chest1 = Location(dungeon=7).add(DungeonChest(0x209)) # stone beak
        before_b_stairs_switch = Location("D7 1st Floor Switch", dungeon=7).add(KeyLocation("SWITCH7A"))
        before_b_stairs_switch_range = Location("D7 1st Floor Switch (From Pegs)", dungeon=7).add(KeyLocation("SWITCH7A_RANGE"))
        after_b_stairs = Location("D7 Upstairs Locked Staircase", dungeon=7)
        before_c_stairs = Location("D7 1st Floor NW Staircase", dungeon=7)
        after_c_stairs = Location("D7 North Three-of-a-Kind", dungeon=7)
        after_c_stairs_chest2 = Location(dungeon=7).add(DungeonChest(0x211)) # compass
        before_d_stairs = Location("D7 1st Floor SW Staircase", dungeon=7)
        after_d_stairs = Location("D7 Hinox Area", dungeon=7)
        after_d_stairs_drop2 = Location(dungeon=7).add(DroppedKey(0x21B)) # small key
        east_ledge = Location("D7 East Ledge", dungeon=7)
        east_ledge_chest3 = Location(dungeon=7).add(DungeonChest(0x204))
        west_ledge = Location("D7 West Ledge", dungeon=7)
        west_ledge_chest4 = Location(dungeon=7).add(DungeonChest(0x201)) # seashell
        ne_pillar = Location("D7 NE Pillar Area", dungeon=7)
        ne_pillar_fall = Location("D7 NE Pillar Fallen", dungeon=7).add(KeyLocation("D7_PILLAR"))
        ne_pillar_chest5 = Location(dungeon=7).add(DungeonChest(0x212)) # map chest
        se_pillar = Location("D7 SE Pillar Area", dungeon=7)
        se_pillar_fall = Location("D7 SE Pillar Fallen", dungeon=7).add(KeyLocation("D7_PILLAR"))
        se_pillar_switch = Location("D7 Fenced Switch", dungeon=7).add(KeyLocation("SWITCH7C"))
        #TODO: se_pillar_switch_midrange = Location("D7 Fenced Switch (From Below)", dungeon=7).add(KeyLocation("SWITCH7C_MIDRANGE")) NOTE: enable this when new switch logic is uncommented
        se_pillar_switch_range = Location("D7 Fenced Switch (From Pegs)", dungeon=7).add(KeyLocation("SWITCH7C_RANGE"))
        nw_pillar = Location("D7 NW Pillar Area", dungeon=7)
        nw_pillar_fall = Location("D7 NW Pillar Fallen", dungeon=7).add(KeyLocation("D7_PILLAR"))
        sw_pillar = Location("D7 SW Pillar Area", dungeon=7)
        sw_pillar_fall = Location("D7 SW Pillar Fallen", dungeon=7).add(KeyLocation("D7_PILLAR"))
        sw_pillar_toak = Location("D7 South Three-of-a-Kind Clear", dungeon=7).add(KeyLocation("D7_TOAK_CLEAR"))
        sw_pillar_chest6 = Location(dungeon=7).add(DungeonChest(0x21C))
        tile_room = Location("D7 Floating Tile Fight", dungeon=7)
        spike_corridor = Location("D7 Corridor Between Pillars", dungeon=7)
        bombwall_corridor = Location("D7 Bombable Wall Corridor", dungeon=7)
        bombwall_pit = Location("D7 Near Bombable Wall Owl", dungeon=7)
        bombwall_pit_owl3 = Location(dungeon=7).add(OwlStatue(0x21C))
        keylock_ledge = Location("D7 Key Locked Ledge", dungeon=7)
        pegs_before_ball = Location("D7 On Pegs Around Chest", dungeon=7)
        pegs_before_ball_chest7 = Location(dungeon=7).add(DungeonChest(0x21A))
        before_e_stairs = Location("D7 Staircase by Fenced Switch", dungeon=7)
        after_e_stairs = Location("D7 3rd Floor Staircase", dungeon=7)
        floor3_pre_cutscene = Location("D7 3rd Floor", dungeon=7)
        floor3_post_cutscene = Location("D7 3rd Floor (After Cutscene)", dungeon=7)
        miniboss = Location("D7 Miniboss Room", dungeon=7)
        after_miniboss = Location("D7 After Miniboss Room", dungeon=7)
        after_miniboss_chest8 = Location(dungeon=7).add(DungeonChest(0x224)) # nightmare key
        #TODO: after_miniboss_switch = Location("D7 Switch After Miniboss").add(KeyLocation("SWITCH7D")) NOTE: enable this if switch is found to be logical
        boss_backdoor = Location("D7 Boss Backdoor Room", dungeon=7)
        conveyor_room = Location("D7 Conveyor Horseheads Room", dungeon=7)
        after_boss_door = Location("D7 After Boss Door", dungeon=7)
        after_boss_door_chest9 = Location(dungeon=7).add(DungeonChest(0x220)) # medicine
        pre_boss_ledge = Location("D7 Before Boss", dungeon=7)
        boss_room = Location("D7 Boss Room", dungeon=7)
        boss_room_drop3 = Location(dungeon=7).add(HeartContainer(0x223)).add(KeyLocation("D7_BOSS_CLEAR")) # heart container & instrument room door flag
        instrument = Location("D7 Instrument Room", dungeon=7).add(Instrument(0x22c)) # organ of evening calm

        # owl statues
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            after_a_stairs.connect(after_a_stairs_owl1, STONE_BEAK7, back=False)
            before_b_stairs.connect(before_b_stairs_owl2, STONE_BEAK7, back=False)
            bombwall_pit.connect(bombwall_pit_owl3, STONE_BEAK7, back=False)

        # connections
        # floor 1
        entrance.connect(entrance_drop1, r.enemy_requirements["LIKE_LIKE"], back=False)
        entrance.connect(before_a_stairs, FOUND(KEY7, 1))
        before_b_stairs.connect(before_b_stairs_chest1, back=False)
        before_b_stairs.connect(before_b_stairs_switch, r.hit_switch, back=False)
        before_b_stairs.connect(before_b_stairs_switch_range, OR(OR(BOOMERANG, BOW, BOMB, HOOKSHOT, MAGIC_ROD)), back=False)
        before_b_stairs.connect(before_c_stairs, AND(FEATHER, "SWITCH7A_RANGE"))
        before_b_stairs.connect(before_d_stairs, OR("SWITCH7A", "SWITCH7C", "SWITCH7C_RANGE"), back=OR("SWITCH7A", "SWITCH7C", "SWITCH7C_RANGE")) #TODO: replace with line below when enable SWITCH7B_RANGE
        #TODO: before_b_stairs.connect(before_d_stairs, OR("SWITCH7A", "SWITCH7B_RANGE", "SWITCH7C", "SWITCH7C_RANGE"), back=OR("SWITCH7A", "SWITCH7B_RANGE", "SWITCH7C", "SWITCH7C_RANGE"))
        before_b_stairs.connect(entrance, OR("SWITCH7A", "SWITCH7C", "SWITCH7C_RANGE"), back=False) #TODO: replace with line below when enable SWITCH7B_RANGE
        #TODO: before_b_stairs.connect(entrance, OR("SWITCH7A", "SWITCH7B_RANGE", "SWITCH7C", "SWITCH7C_RANGE"), back=False)
        west_ledge.connect((entrance, before_b_stairs, west_ledge_chest4), back=False)
        east_ledge.connect((entrance, before_a_stairs, before_a_stairs, east_ledge_chest3), back=False)
        # connect floor 1 & 2
        entrance.connect((bombwall_pit, sw_pillar), False, back=None) # pit
        before_a_stairs.connect(after_a_stairs) # stairs
        before_b_stairs.connect(after_b_stairs) # stairs
        before_c_stairs.connect(after_c_stairs) # stairs
        before_d_stairs.connect(after_d_stairs) # stairs
        ne_pillar.connect((entrance, before_b_stairs), back=False) # pit
        nw_pillar.connect((before_b_stairs, before_c_stairs), back=False) # pit
        se_pillar.connect((entrance, before_b_stairs), back=False) # pit
        spike_corridor.connect(before_b_stairs, back=False) # pit
        tile_room.connect((before_b_stairs, west_ledge), back=False) # pit
        after_d_stairs.connect(west_ledge, back=False) # pit
        pegs_before_ball.connect(east_ledge, back=False) # pit
        # floor 2 north
        after_a_stairs.connect(ball_access, POWER_BRACELET)
        #TODO: after_a_stairs.connect((pegs_before_ball, after_d_stairs), "SWITCH7B_RANGE", back=False) # enable when casual logic statement is uncommented
        after_a_stairs.connect(ne_pillar) #TODO: REMOVE in favor of casual logic for pulling lever
        after_b_stairs.connect(ne_pillar, "SWITCH7A", back="SWITCH7C") #TODO: replace with line below when enable SWITCH7B_RANGE
        #TODO: after_b_stairs.connect(ne_pillar, "SWITCH7A", back=OR("SWITCH7B_RANGE", "SWITCH7C"))
        ne_pillar.connect(ne_pillar_chest5, POWER_BRACELET, back=False)
        ne_pillar.connect(ne_pillar_fall, "D7_BALL", back=False)
        ne_pillar.connect(se_pillar, FEATHER)
        ne_pillar.connect(spike_corridor, "SWITCH7A", back="SWITCH7C") #TODO: replace with line below when enable SWITCH7B_RANGE or SWITCH7C_MIDRANGE
        #TODO: ne_pillar.connect(spike_corridor, OR("SWITCH7A", "SWITCH7B_RANGE"), back=OR("SWITCH7C", "SWITCH7C_MIDRANGE"))
        se_pillar.connect(se_pillar_fall, "D7_BALL", back=False)
        se_pillar.connect(se_pillar_switch, r.hit_switch) #NOTE: add bracelet method if rom patched
        se_pillar.connect(spike_corridor, "SWITCH7C", back=OR("SWITCH7A", FEATHER)) #TODO: replace with line below when enable SWITCH7B_RANGE
        #TODO: se_pillar.connect(spike_corridor, OR(FEATHER, "SWITCH7C"), back=OR("SWITCH7A", "SWITCH7B_RANGE", FEATHER))
        se_pillar.connect(before_c_stairs, FEATHER, back=False)
        spike_corridor.connect(after_c_stairs, FEATHER) # jump over spikes
        spike_corridor.connect(before_c_stairs, "SWITCH7A", back=False) #TODO: replace with line below when enable SWITCH7B_RANGE
        #TODO: spike_corridor.connect(before_c_stairs, OR("SWITCH7A", "SWITCH7B_RANGE"), back=False)
        after_c_stairs.connect(after_c_stairs_chest2, r.enemy_requirements["THREE_OF_A_KIND"], back=False) #NOTE: add bracelet method if rom patched
        nw_pillar.connect(spike_corridor, FEATHER, back=False)
        nw_pillar.connect(nw_pillar_fall, "D7_BALL", back=False)
        nw_pillar.connect(tile_room)
        # floor 2 south
        after_d_stairs.connect((entrance, west_ledge, tile_room), back=False) # fall down pits in hinox room or walk into tile fight room
        after_d_stairs.connect(after_d_stairs_drop2, r.miniboss_requirements["HINOX"], back=False)
        after_d_stairs.connect(sw_pillar_toak, r.enemy_requirements["THREE_OF_A_KIND"], back=False)
        after_d_stairs.connect((se_pillar_switch_range, se_pillar_switch_range), OR(BOOMERANG, BOW, BOMB, MAGIC_ROD), back=False)
        after_d_stairs.connect(pegs_before_ball, OR(HOOKSHOT, SWORD), back=False) #TODO: REMOVE this line, upstream logic was too broad with switch requirements
        after_d_stairs.connect(pegs_before_ball, "SWITCH7C_RANGE", back=None) # stand on pegs and hit switch
        after_d_stairs.connect(keylock_ledge, FOUND(KEY7, 3))
        keylock_ledge.connect((se_pillar, pegs_before_ball, after_d_stairs), back=False)
        pegs_before_ball.connect(after_a_stairs_switch, r.hit_switch, back=False)
        pegs_before_ball.connect((after_a_stairs, pegs_before_ball_chest7), back=False)
        # floor 2 center
        bombwall_corridor.connect((bombwall_pit, nw_pillar), BOMB)
        bombwall_corridor.connect(after_d_stairs, back=False) # push blocks from inside corridor to get to hinox area
        bombwall_pit.connect(sw_pillar, AND(HOOKSHOT, "D7_TOAK_CLEAR"), back=False) #NOTE: add bracelet method if rom patched
        sw_pillar.connect(sw_pillar_fall, "D7_BALL", back=False)
        sw_pillar.connect(sw_pillar_chest6, "D7_TOAK_CLEAR", back=False) #NOTE: add bracelet method if rom patched
        # connect floor 2 & 3
        after_d_stairs.connect(before_e_stairs)
        before_e_stairs.connect(after_e_stairs)
        after_e_stairs.connect(floor3_pre_cutscene, back=False)
        after_e_stairs.connect(floor3_post_cutscene, FOUND("D7_PILLAR", 4), back=False)
        # floor 3 before cutscene NOTE: these connections work before or after cutscene
        floor3_pre_cutscene.connect(miniboss, back=False)
        miniboss.connect(entrance, r.miniboss_requirements[world_setup.miniboss_mapping[6]], back=False) # miniboss portal
        miniboss.connect((floor3_pre_cutscene, after_miniboss), r.miniboss_requirements[world_setup.miniboss_mapping[6]], back=None)
        after_miniboss.connect(after_miniboss_chest8, back=False)
        #TODO: after_miniboss.connect(after_miniboss_switch, r.hit_switch, back=False) NOTE: enable this if switch is found to be logical
        #TODO: floor3_pre_cutscene.connect(boss_backdoor, FOUND(KEY7, 3))
        #TODO: conveyor_room.connect(after_boss_door_chest9, POWER_BRACELET, back=False)
        conveyor_room.connect((before_b_stairs, before_c_stairs), back=False) # fall down near boss door to floor 1
        # floor 3 after cutscene NOTE: shouldn't put miniboss, boss_backdoor, or conveyor_room in here else logic will leak
        floor3_post_cutscene.connect(after_boss_door, NIGHTMARE_KEY7)
        after_boss_door.connect(after_boss_door_chest9, POWER_BRACELET, back=False)
        after_boss_door.connect(pre_boss_ledge, HOOKSHOT, back=None)
        pre_boss_ledge.connect(boss_room)
        boss_room.connect(boss_room_drop3, r.boss_requirements[world_setup.boss_mapping[6]], back=False)
        boss_room.connect(instrument, "D7_BOSS_CLEAR", back=False)

        # key logic patch
        if options.dungeon_items not in {'localnightmarekey', 'keysanity', 'keysy', 'smallkeys'}:
            entrance_drop1.items[0].forced_item = KEY7

        #TODO: if options.logic == "casual":
            #TODO: after_a_stairs.connect(ne_pillar, POWER_BRACELET, back=None) # intended method is to pull lever
        #TODO: else:
            #TODO: after_a_stairs.connect(ne_pillar) # Ball Room <--> NE Pillar Area
            #TODO: after_a_stairs.connect(after_a_stairs_switch_range, BOOMERANG, back=False)

        #TODO if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            #TODO: after_c_stairs.connect(spike_corridor, r.damage_boost) # [logic prep for stairs shuffle] # forced damage so cannot be in normal logic
            #TODO: after_d_stairs.connect(se_pillar_switch_midrange, OR(BOOMERANG, BOW, BOMB, MAGIC_ROD, AND(FEATHER, SWORD)), back=False) # very difficult or obscure ways to hit switch from behind rail NOTE: add bracelet method if rom patched
            #TODO: after_d_stairs.connect(se_pillar_switch_range, OR(BOOMERANG, BOW, BOMB, MAGIC_ROD), back=False) # hit switch and get on pegs by east exit

        if options.logic == 'glitched' or options.logic == 'hell':
            ne_pillar.connect(ne_pillar_fall, r.bomb_trigger, back=False) # trigger pillar cutscene by placing a bomb during the screen transition
            se_pillar.connect(se_pillar_fall, r.bomb_trigger, back=False) # trigger pillar cutscene by placing a bomb during the screen transition)
            spike_corridor.connect((nw_pillar_fall, ne_pillar_fall, se_pillar_fall), r.bomb_trigger, back=False) # trigger pillar cutscene by placing a bomb during the screen transition
            nw_pillar.connect(nw_pillar_fall, r.bomb_trigger, back=False) # trigger pillar cutscene by placing a bomb during the screen transition
            sw_pillar.connect(sw_pillar_fall, r.bomb_trigger, back=False) # trigger pillar cutscene by placing a bomb during the screen transition
            entrance.connect((before_b_stairs, before_c_stairs), r.super_jump_sword, back=False) # superjump in the center to get on raised blocks sword added to help with low jump
            before_b_stairs.connect((entrance, before_c_stairs, east_ledge), r.super_jump_feather, back=False) # superjump in spike switch room to right ledge
            spike_corridor.connect(nw_pillar, OR(r.shaq_jump, r.super_jump_feather), back=False) # superjump from right wall or shaq jump off pushblock
            west_ledge.connect(before_d_stairs, r.boots_jump, back=False) # without hitting the switch, drop off ledge onto peg wall, and boots jump to pegs blocking stairs
            after_d_stairs.connect(bombwall_corridor, r.sideways_block_push, back=False) # sideways block push to get to owl statue by bomb wall
            after_d_stairs.connect(sw_pillar_toak, "D7_BALL", back=False) #TODO: MOVE to hard logic, no glitch here, but with the kill saved as a variable, it is possible to collect chest without sideways block push
            after_d_stairs.connect((bombwall_pit, sw_pillar), r.sideways_block_push, back=False) # sideways block push to get to SW pillar area
            after_d_stairs.connect(se_pillar, r.super_jump_feather, back=False) # sideways block push to get to SW pillar area
            after_d_stairs.connect(bombwall_corridor, r.shaq_jump, back=False)
            floor3_post_cutscene.connect(pre_boss_ledge, r.super_jump_feather, back=False) # superjump on top of goomba to bounce across to boss door plateau
            #TODO: boss_backdoor.connect(conveyor_room, AND(r.hookshot_clip_block, r.super_jump_feather), back=False) # hookshot clip pot in upper right repeatedly until wall clipped, then superjump onto pegs
            
        if options.logic == 'hell':
            #TODO: entrance.connect(before_a_stairs, AND(r.boots_superhop, r.shield_bump), back=AND(super_jump_boots, r.zoomerang_buffer)) # boots superbump off blade to cross, or boots jump, midair turn to land in block and then zoomernag to un-stuck
            #TODO: entrance.connect(west_ledge, r.super_bump, back=False) # enter SW room wall clipped, line up with wizrobes, and repeat super bumps to move up onto the ledge (very precise, relevant in stairs shuffle)
            entrance.connect(east_ledge, AND(OR(r.super_jump_boots, r.zoomerang), r.shield_bump), back=False) # along bottom wall in first key room, setup boots super jump, but hold shield after the jump to bump down to ledge
            entrance.connect((before_b_stairs, before_c_stairs), r.super_jump_feather) # superjump in the center to get on raised blocks, hell because the jump has to be very low
            entrance.connect(before_b_stairs, r.boots_superhop, back=True) # boots superhop in the center to get on raised blocks
            before_b_stairs.connect(east_ledge, r.boots_superhop, back=False) # boots superhop from room with spike switch
            #TODO: before_c_stairs.connect((before_b_stairs, west_ledge), r.super_bump, back=False) # super bump wall clipped from the stairs off peahat to cross pegs, then again into kirby mouth to get spit onto ledge
            spike_corridor.connect(ne_pillar, r.pit_buffer_boots, back=AND(r.pit_buffer_itemless, r.super_jump_feather)) # pit buffer to go around pegs to ne pillar reverse: pit buffer and super jump off south wall to land on pegs
            #TODO: spike_corridor.connect(ne_pillar, r.boots_bonk_pit, back=OR(AND(r.boots_superhop, r.sword_poke), AND(r.pit_buffer_itemless, r.super_jump_feather))) # boots bonk off pegs to se pillar reverse: pit buffer and super jump off south wall to land on pegs
            #TODO: after_d_stairs.connect(after_d_stairs_drop2, "D7_BALL", back=False) # kill hinox with ball (don't drop it!)
            after_d_stairs.connect(sw_pillar, r.super_jump_boots, back=False) # boots jump into wall by puzzle buddies to super jump into sw pillar area
            #TODO: sw_pillar_toak.connect((bombwall_pit, sw_pillar), False, back=AND(r.pit_buffer_boots, BOMB)) # pit buffer into rail and defeat puzzle buddies with bomb NOTE: probably some other items too
            #TODO: after_d_stairs.connect(se_pillar, r.boots_superhop, back=False) #[logic prep for stairs shuffle]
            #TODO: after_d_stairs.connect(se_pillar_switch_midrange, OR(AND(PEGASUS_BOOTS, SWORD), AND(r.super_jump_feather, HOOKSHOT),COUNT(SWORD, 2)), back=False) # 1) boots bonk and slash 2) superjump & 6 pause buffers to land on rail, hookshot the switch, and walk back off rail 3) L2 sword beam
            #TODO: after_d_stairs.connect(keylock_ledge, AND(r.boots_superhop, r.shield_bump), back=False) # running super bump off antifairy to get on ledge without key
            #TODO: after_d_stairs.connect((bombwall_pit, sw_pillar), False, back=r.zoomerang_buffer) # push block and perform right-facing zoomerang to escapt where blocks meet at corner
            #TODO: bombwall_pit.connect(sw_pillar, r.pit_buffer_boots) # two way pit buffer across pit
            #TODO: sw_pillar.connect(sw_pillar_toak, back=False) # push blocks to stun suit buddies and spawn chest - quite difficult, should we include this?
            #TODO: floor3_pre_cutscene.connect((conveyor_area, after_boss_door), OR(r.super_bump, r.super_poke), back=False)
            #TODO: boss_backdoor.connect((conveyor_area, after_boss_door), OR(r.shaq_jump, r.boots_superhop), back=False) # all forms of sueprjumps and rebound off peahat onto pegs
            floor3_post_cutscene.connect(pre_boss_ledge, r.boots_superhop, back=False) # boots superhop on top of goomba to extend superhop to boss door plateau
        
        self.entrance = entrance
        self.final_room = instrument


class NoDungeon7:
    def __init__(self, options, world_setup, r):
        entrance = Location("D7 Entrance", dungeon=7)
        boss = Location(dungeon=7).add(HeartContainer(0x223), Instrument(0x22c)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[6]])

        self.entrance = entrance
