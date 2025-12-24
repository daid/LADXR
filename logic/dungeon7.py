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
        after_a_stairs_switch_range = Location("D7 Pit Switch (Range)", dungeon=7).add(KeyLocation("SWITCH7B_RANGE")) #NOTE: This switch is not used in casual logic (diagonal boomerang), so it's been omitted from casual in itempool.py
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
        se_pillar_switch_midrange = Location("D7 Fenced Switch (From Below)", dungeon=7).add(KeyLocation("SWITCH7C_MIDRANGE")) #NOTE: This switch variant is only accessible via hard or higher logic tricks
        se_pillar_switch_range = Location("D7 Fenced Switch (From Pegs)", dungeon=7).add(KeyLocation("SWITCH7C_RANGE"))
        nw_pillar = Location("D7 NW Pillar Area", dungeon=7)
        nw_pillar_fall = Location("D7 NW Pillar Fallen", dungeon=7).add(KeyLocation("D7_PILLAR"))
        sw_pillar = Location("D7 SW Pillar Area", dungeon=7)
        sw_pillar_fall = Location("D7 SW Pillar Fallen", dungeon=7).add(KeyLocation("D7_PILLAR"))
        sw_pillar_toak_clear = Location("D7 South Three-of-a-Kind Clear", dungeon=7).add(KeyLocation("D7_TOAK_CLEAR")) #NOTE: unopened chest despawns after 6 screen transitions or enter stairs, but never despawns if opened
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
        pre_cut_floor3 = Location("D7 3rd Floor (Before Cutscene)", dungeon=7)
        post_cut_floor3 = Location("D7 3rd Floor (After Cutscene)", dungeon=7)
        miniboss = Location("D7 Miniboss Room", dungeon=7)
        after_miniboss = Location("D7 After Miniboss Room", dungeon=7)
        after_miniboss_chest8 = Location(dungeon=7).add(DungeonChest(0x224)) # nightmare key
        #TODO: after_miniboss_switch = Location("D7 Switch After Miniboss").add(KeyLocation("SWITCH7D")) #NOTE: enable this if miniboss switch is found to be logically relevant
        pre_cut_boss_backdoor = Location("D7 Boss Backdoor Room", dungeon=7)
        pre_cut_conveyor_area = Location("D7 Conveyor Horseheads Area (Before Cutscene)", dungeon=7)
        post_cut_conveyor_area = Location("D7 After Boss Door", dungeon=7)
        conveyor_area_chest9 = Location(dungeon=7).add(DungeonChest(0x220)) # medicine
        pre_boss_stairs = Location("D7 Before Boss", dungeon=7)
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
        before_b_stairs.connect(before_b_stairs_switch_range, OR(BOOMERANG, BOW, BOMB, HOOKSHOT, MAGIC_ROD), back=False)
        before_b_stairs.connect(before_c_stairs, AND("SWITCH7A_RANGE", FEATHER), back=False)
        before_b_stairs.connect(before_d_stairs, "SWITCH7A", back=False)
        before_b_stairs.connect(entrance, "SWITCH7A", back=False)
        west_ledge.connect((entrance, before_b_stairs, west_ledge_chest4), back=False)
        east_ledge.connect((entrance, before_a_stairs, before_b_stairs, east_ledge_chest3), back=False)
        # connect floor 1 & 2
        before_a_stairs.connect(after_a_stairs) # se stairs
        before_b_stairs.connect(after_b_stairs) # ne stairs
        before_c_stairs.connect(after_c_stairs) # nw stairs
        before_d_stairs.connect(after_d_stairs) # sw stairs
        ne_pillar.connect((entrance, before_b_stairs), back=False) # pit
        se_pillar.connect((entrance, before_b_stairs), back=False) # pit
        spike_corridor.connect(before_b_stairs, back=False) # pit
        nw_pillar.connect(before_b_stairs, back=False) # pit
        entrance.connect((bombwall_pit, sw_pillar), False, back=None) # pit
        tile_room.connect((before_b_stairs, west_ledge), back=False) # pit
        after_d_stairs.connect((entrance, west_ledge), back=False) # pits in hinox room
        pegs_before_ball.connect(east_ledge, back=False) # pit
        # floor 2 north
        after_a_stairs.connect(ball_access, POWER_BRACELET)
        after_a_stairs.connect(pegs_before_ball, "SWITCH7B_RANGE", back=False)
        after_b_stairs.connect(ne_pillar, "SWITCH7A", back=OR("SWITCH7B_RANGE", "SWITCH7C"))
        ne_pillar.connect(ne_pillar_chest5, POWER_BRACELET, back=False)
        ne_pillar.connect(ne_pillar_fall, "D7_BALL", back=False)
        ne_pillar.connect(se_pillar, FEATHER)
        ne_pillar.connect(spike_corridor, OR("SWITCH7A", "SWITCH7B_RANGE"), back=OR("SWITCH7C", "SWITCH7C_MIDRANGE"))
        se_pillar.connect(se_pillar_fall, "D7_BALL", back=False)
        se_pillar.connect(se_pillar_switch, r.hit_switch) #NOTE: add bracelet method if rom patched
        se_pillar.connect(spike_corridor, OR(FEATHER, "SWITCH7C"), back=OR("SWITCH7A", "SWITCH7B_RANGE", FEATHER))
        se_pillar.connect(before_c_stairs, FEATHER, back=False)
        spike_corridor.connect(after_c_stairs, FEATHER) # jump over spikes
        spike_corridor.connect(before_c_stairs, OR("SWITCH7A", "SWITCH7B_RANGE"), back=False)
        after_c_stairs.connect(after_c_stairs_chest2, r.enemy_requirements["THREE_OF_A_KIND"], back=False) #NOTE: add bracelet method if rom patched
        nw_pillar.connect(spike_corridor, FEATHER, back=False)
        nw_pillar.connect(nw_pillar_fall, "D7_BALL", back=False)
        nw_pillar.connect(tile_room)
        # floor 2 south
        after_d_stairs.connect(tile_room, back=False)
        after_d_stairs.connect(after_d_stairs_drop2, r.miniboss_requirements["HINOX"], back=False)
        after_d_stairs.connect(sw_pillar_toak_clear, r.enemy_requirements["THREE_OF_A_KIND"], back=False) #NOTE: add bracelet method if rom patched
        after_d_stairs.connect((se_pillar_switch_midrange, se_pillar_switch_range), OR(BOOMERANG, BOW, BOMB, MAGIC_ROD), back=False)
        after_d_stairs.connect(pegs_before_ball, "SWITCH7C_RANGE", back=None)
        after_d_stairs.connect(keylock_ledge, FOUND(KEY7, 3))
        keylock_ledge.connect((se_pillar, pegs_before_ball, after_d_stairs), back=False)
        pegs_before_ball.connect(after_a_stairs_switch, r.hit_switch, back=False)
        pegs_before_ball.connect((after_a_stairs, pegs_before_ball_chest7, after_d_stairs), back=False)
        # floor 2 center
        bombwall_corridor.connect((bombwall_pit, nw_pillar), BOMB)
        bombwall_corridor.connect(after_d_stairs, back=False) # push blocks from inside corridor to get to hinox area
        bombwall_pit.connect(sw_pillar, AND(HOOKSHOT, "D7_TOAK_CLEAR"), back=False) #NOTE: chest despawns after 6 room transisions, must walke through tile fight room and bombwall coridor
        sw_pillar.connect(sw_pillar_chest6, "D7_TOAK_CLEAR", back=False)
        sw_pillar.connect(sw_pillar_fall, "D7_BALL", back=False)
        # connect floor 2 & 3
        after_d_stairs.connect(before_e_stairs)
        before_e_stairs.connect(after_e_stairs)
        after_e_stairs.connect(pre_cut_floor3, back=False)
        after_e_stairs.connect(post_cut_floor3, FOUND("D7_PILLAR", 4), back=False)
        # floor 3 before cutscene NOTE: these connections work before or after cutscene
        pre_cut_floor3.connect(miniboss, back=False)
        miniboss.connect(entrance, r.miniboss_requirements[world_setup.miniboss_mapping[6]], back=False) # miniboss portal
        miniboss.connect((pre_cut_floor3, after_miniboss), r.miniboss_requirements[world_setup.miniboss_mapping[6]], back=None)
        after_miniboss.connect(after_miniboss_chest8, back=False)
        #TODO: after_miniboss.connect(after_miniboss_switch, r.hit_switch, back=False) NOTE: enable this if switch is found to be logical
        pre_cut_floor3.connect(pre_cut_boss_backdoor, FOUND(KEY7, 3))
        for location in (pre_cut_conveyor_area, post_cut_conveyor_area):
            location.connect(conveyor_area_chest9, POWER_BRACELET, back=False)
        pre_cut_conveyor_area.connect((nw_pillar, before_b_stairs, before_c_stairs), back=False) # fall down from floor 3 big pit
        # floor 3 after cutscene 
        post_cut_floor3.connect(post_cut_conveyor_area, NIGHTMARE_KEY7)
        post_cut_conveyor_area.connect((before_b_stairs, before_c_stairs), back=False) # fall down from floor 3 1-tile pit
        post_cut_conveyor_area.connect(pre_boss_stairs, HOOKSHOT, back=None)
        pre_boss_stairs.connect(boss_room)
        boss_room.connect(boss_room_drop3, r.boss_requirements[world_setup.boss_mapping[6]], back=False)
        boss_room.connect(instrument, "D7_BOSS_CLEAR", back=False)

        # key logic patch
        if options.dungeon_keys == '':
            entrance_drop1.items[0].forced_item = KEY7

        if options.logic == "casual":
            after_a_stairs.connect(ne_pillar, POWER_BRACELET, back=None) # intended method is to pull lever
        else:
            after_a_stairs.connect(ne_pillar) # Ball Room <--> NE Pillar Area
            after_a_stairs.connect(after_a_stairs_switch_range, BOOMERANG, back=False)
            before_b_stairs.connect(before_c_stairs, "SWITCH7A", back=False) # have to walk through kirby corridor, it's too easy to take damage, so it's excluded from casual

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            after_c_stairs.connect(spike_corridor, r.damage_boost) # forced damage so this cannot be in normal logic
            after_d_stairs.connect(se_pillar_switch_midrange, OR(BOOMERANG, BOW, BOMB, MAGIC_ROD, AND(FEATHER, SWORD)), back=False) # jump and swing sword from below rail NOTE: add bracelet method if rom patched
            after_d_stairs.connect(se_pillar_switch_range, OR(BOOMERANG, BOW, BOMB, MAGIC_ROD), back=False) # hit switch and get on pegs by east exit
            after_d_stairs.connect(sw_pillar_toak_clear, "D7_BALL", back=False) # throw the ball to solve three-of-a-kind and spawn the chest

        if options.logic == 'glitched' or options.logic == 'hell':
            ne_pillar.connect(ne_pillar_fall, AND(r.bomb_trigger, r.enemy_requirements["HIDING_ZOL"]), back=False) # trigger pillar cutscene by placing a bomb during the screen transition
            se_pillar.connect(se_pillar_fall, AND(r.bomb_trigger, r.enemy_requirements["HIDING_ZOL"]), back=False) # trigger pillar cutscene by placing a bomb during the screen transition
            spike_corridor.connect((nw_pillar_fall, ne_pillar_fall, se_pillar_fall), AND(r.bomb_trigger, r.enemy_requirements["HIDING_ZOL"]), back=False) # trigger pillar cutscene by placing a bomb during the screen transition
            nw_pillar.connect(nw_pillar_fall, r.bomb_trigger, back=False) # trigger pillar cutscene by placing a bomb during the screen transition
            sw_pillar.connect(sw_pillar_fall, r.bomb_trigger, back=False) # trigger pillar cutscene by placing a bomb during the screen transition
            entrance.connect((before_b_stairs, before_c_stairs), r.super_jump_sword, back=False) # superjump in the center to get on raised blocks sword added to help with low jump
            before_b_stairs.connect((entrance, before_c_stairs, east_ledge), r.super_jump_feather, back=False) # superjump in spike switch room to right ledge
            before_b_stairs.connect((west_ledge, east_ledge), PEGASUS_BOOTS, back=False) # dash downwards while kirby is near top ledge, after inhaled, kirby spits you out it will cause a sideways superjump
            spike_corridor.connect(nw_pillar, OR(r.shaq_jump, r.super_jump_feather), back=False) # superjump from right wall or shaq jump off pushblock
            west_ledge.connect(before_d_stairs, r.boots_jump, back=False) # without hitting the switch, drop off ledge onto peg wall, and boots jump to pegs blocking stairs
            after_d_stairs.connect(bombwall_corridor, r.sideways_block_push, back=False) # sideways block push to get to owl statue by bomb wall
            after_d_stairs.connect((bombwall_pit, sw_pillar), r.sideways_block_push, back=False) # sideways block push to get to SW pillar area
            after_d_stairs.connect(se_pillar, r.super_jump_feather, back=False) # wall clip by torch or stairs and superjump into fenced switch area
            after_d_stairs.connect(bombwall_corridor, r.shaq_jump, back=False)
            post_cut_floor3.connect(pre_boss_stairs, r.super_jump_feather, back=False) # superjump on top of goomba to bounce across to boss door plateau
            pre_cut_boss_backdoor.connect(pre_cut_conveyor_area, AND(r.hookshot_clip_block, r.super_jump_feather), back=False) # hookshot clip pot in upper right repeatedly until wall clipped, then superjump onto pegs
            
        if options.logic == 'hell':
            entrance.connect(before_a_stairs, AND(r.boots_superhop, r.shield_bump), back=AND(r.super_jump_boots, r.zoomerang_shovel)) # boots superbump off blade to cross, or boots jump, midair turn to land in block and then zoomernag to un-stuck
            entrance.connect(west_ledge, r.super_bump, back=False) # enter SW room wall clipped, line up with wizrobes, and repeat super bumps to move up onto the ledge
            entrance.connect(east_ledge, AND(OR(r.super_jump_boots, r.zoomerang), r.shield_bump), back=False) # along bottom wall in first key room, setup boots super jump, but hold shield after the jump to bump down to ledge
            entrance.connect((before_b_stairs, before_c_stairs), r.super_jump_feather) # superjump in the center to get on raised blocks, hell because the jump has to be very low
            entrance.connect(before_b_stairs, r.boots_superhop, back=True) # boots superhop in the center to get on raised blocks
            before_b_stairs.connect(before_b_stairs_switch_range, r.sword_beam, back=False) # standing on pegs to the left of ground floor switch, shoot a sword laser at the switch
            before_b_stairs.connect(east_ledge, r.boots_superhop, back=False) # boots superhop from room with spike switch
            before_c_stairs.connect((before_b_stairs, west_ledge), r.super_bump, back=False) # super bump wall clipped from the stairs off peahat to cross pegs, then again into kirby mouth to get spit onto ledge
            ne_pillar.connect(se_pillar, r.hookshot_spam_pit) # hookshot spam to cross pit between the two east pillars
            se_pillar.connect(spike_corridor, AND(BOOMERANG, r.hookshot_clip_block), back=False) # get a rupee from enemy kill and deliver it with boomerang while spamming hookshot to clip through the pushblock in reverse
            #TODO: se_pillar.connect(spike_corridor, r.damage_boost_special) #NOTE: [can't add this until the ledge between the east pillars is given a unique location variable due to pushblock] walk partly into the pit and quickly turn around to take spike knockback which causes you to hop over pit
            spike_corridor.connect(ne_pillar, r.pit_buffer_boots, back=AND(r.pit_buffer_itemless, r.super_jump_feather)) # pit buffer to go around pegs to ne pillar reverse: pit buffer and super jump off south wall to land on pegs
            ne_pillar.connect(after_b_stairs, r.super_bump, back=False) # super bump off anti-fairy to get on the single peg blocking the stairs
            spike_corridor.connect(ne_pillar, r.boots_bonk_pit, back=OR(AND(r.boots_superhop, r.sword_poke), AND(r.pit_buffer_itemless, r.super_jump_feather))) # boots bonk off pegs to se pillar reverse: pit buffer and super jump off south wall to land on pegs
            after_d_stairs.connect(after_d_stairs_drop2, "D7_BALL", back=False) # kill hinox with ball (don't drop it!)
            after_d_stairs.connect(sw_pillar, r.super_jump_boots, back=False) # boots jump into wall by puzzle buddies to super jump into sw pillar area
            for location in (bombwall_pit, sw_pillar):
                location.connect(sw_pillar_toak_clear, AND(r.pit_buffer_boots, BOMB), back=False) # pit buffer into rail and solve the three-of-a-kind puzzle with bombs
            after_d_stairs.connect(se_pillar, r.boots_superhop, back=False)
            after_d_stairs.connect(se_pillar_switch_midrange, OR(AND(r.boots_bonk, SWORD), AND(r.super_jump_feather, HOOKSHOT), r.sword_beam), back=False) # 1) boots bonk and slash 2) superjump & 6 pause buffers to land on rail, hookshot the switch, and walk back off rail 3) L2 sword beam
            after_d_stairs.connect(se_pillar_switch_range, r.sword_beam, back=False)
            after_d_stairs.connect(keylock_ledge, AND(r.boots_superhop, r.shield_bump), back=False) # running super bump off antifairy to get on ledge without key
            for location in (bombwall_pit, sw_pillar):
                location.connect(after_d_stairs, r.zoomerang_shovel, back=False) # push block and perform right-facing zoomerang to escape at the point where two blocks touch corners
            bombwall_pit.connect(sw_pillar, r.pit_buffer_boots) # pit buffer across the 4-block wide pit
            sw_pillar.connect(sw_pillar_toak_clear, back=False) # push blocks to stun suit buddies and spawn chest
            post_cut_floor3.connect(pre_boss_stairs, r.boots_superhop, back=False) # boots superhop on top of goomba to extend superhop to boss door plateau
            pre_cut_floor3.connect((pre_cut_conveyor_area, post_cut_conveyor_area), OR(r.super_bump, r.super_poke), back=False)
            pre_cut_boss_backdoor.connect((pre_cut_conveyor_area, post_cut_conveyor_area), OR(r.shaq_jump, r.boots_superhop), back=False) # superhop or shaw jump followed by shield bumping off peahat onto pegs

        
        self.entrance = entrance
        self.final_room = instrument


class NoDungeon7:
    def __init__(self, options, world_setup, r):
        entrance = Location("D7 Entrance", dungeon=7)
        boss = Location(dungeon=7).add(HeartContainer(0x223), Instrument(0x22c)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[6]])

        self.entrance = entrance
