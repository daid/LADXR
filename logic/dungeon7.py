from .requirements import *
from .location import Location
from locations.all import *


class Dungeon7:
    def __init__(self, options, world_setup, r):

        # locations
        entrance = Location("D7 Entrance", dungeon=7)
        entrance_drop1 = Location(dungeon=7).add(DroppedKey(0x210)) # small key
        before_a_stairs = Location("D7 Before Locked Staircase", dungeon=7)
        after_a_stairs = Location("D7 Ball Room", dungeon=7)
        before_b_stairs = Location("D7 First Floor Main Area", dungeon=7)
        before_b_stairs_chest1 = Location(dungeon=7).add(DungeonChest(0x209)) # stone beak
        after_b_stairs = Location("D7 Horseheads Staircase", dungeon=7)
        before_c_stairs = Location("D7 Two Peahat, Moldorm Room", dungeon=7)
        after_c_stairs = Location("D7 North Three-of-a-Kind Puzzle", dungeon=7)
        after_c_stairs_chest2 = Location(dungeon=7).add(DungeonChest(0x211)) # compass
        before_d_stairs = Location("D7 Peg Locked Staircase", dungeon=7)
        after_d_stairs = Location("D7 Hinox Area", dungeon=7)
        after_d_stairs_drop2 = Location(dungeon=7).add(DroppedKey(0x21B)) # small key
        east_ledge = Location("D7 East Beamos Ledge", dungeon=7)
        east_ledge_chest3 = Location(dungeon=7).add(DungeonChest(0x204))
        west_ledge = Location("D7 West Kirby Ledge", dungeon=7)
        west_ledge_chest4 = Location(dungeon=7).add(DungeonChest(0x201)) # seashell
        ne_pillar = Location("D7 Northeast Pillar Area")
        ne_pillar_chest5 = Location(dungeon=7).add(DungeonChest(0x212)) # map chest
        se_pillar = Location("D7 Southeast Pillar Area", dungeon=7)
        nw_pillar = Location("D7 Northwest Pillar Area", dungeon=7)
        sw_pillar = Location("D7 Southwest Pillar Area", dungeon=7)
        sw_pillar_chest6 = Location(dungeon=7).add(DungeonChest(0x21C))
        tile_room = Location("D7 Floating Tile Fight", dungeon=7)
        spike_corridor = Location("D7 Between Pillar Pushbocks", dungeon=7)
        bomb_corridor = Location("D7 Bombable Wall Corridor", dungeon=7)
        bombwall_owl = Location("D7 By Pit Owl", dungeon=7)
        keylock_ledge = Location("D7 Key Locked Ledge", dungeon=7)
        pegs_after_a_stairs = Location("D7 On Pegs Around Chest", dungeon=7)
        pegs_after_a_stairs_chest7 = Location(dungeon=7).add(DungeonChest(0x21A))
        final_pillar_fallen = Location("D7 Final Pillar Destroyed", dungeon=7)
        before_e_stairs = Location("D7 Stairs Leading to 3rd Floor", dungeon=7)
        after_e_stairs = Location("D7 Third Floor Entry", dungeon=7)
        miniboss_room = Location("D7 Miniboss Room", dungeon=7)
        after_miniboss_room = Location("D7 After Miniboss Room", dungeon=7)
        after_miniboss_room_chest8 = Location(dungeon=7).add(DungeonChest(0x224)) # nightmare key
        boss_backdoor = Location("D7 Boss Backdoor Room", dungeon=7)
        after_boss_door = Location("D7 After Boss Door", dungeon=7)
        conveyor_room = Location("D7 Conveyor Horseheads Room", dungeon=7)
        conveyor_room_chest9 = Location(dungeon=7).add(DungeonChest(0x220)) # medicine
        pre_boss_room = Location("D7 Before Boss", dungeon=7)
        boss_room = Location("D7 Boss Room", dungeon=7)
        boss_room_drop3 = Location(dungeon=7).add(HeartContainer(0x223)) # heart container
        instrument = Location("D7 Instrument Room", dungeon=7).add(Instrument(0x22c)) # organ of evening calm

        # owl statues
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(dungeon=7).add(OwlStatue(0x216)).connect(after_a_stairs, STONE_BEAK7)
            Location(dungeon=7).add(OwlStatue(0x204)).connect(before_b_stairs, STONE_BEAK7)
            Location(dungeon=7).add(OwlStatue(0x21C)).connect(bombwall_owl, STONE_BEAK7)

        # connections
        # floor 1
        entrance.connect(entrance_drop1, r.enemy_requirements["LIKE_LIKE"]) # Entrance <--> Entrance Key
        entrance.connect(before_a_stairs, FOUND(KEY7, 1)) # Entrance <--> Before First Staircase
        before_b_stairs.connect(before_b_stairs_chest1, None) # First Floor Main Area <--> Switch Wrapped Chest
        before_b_stairs.connect(before_d_stairs, r.hit_switch) # First Floor Main Area <--> Peg Locked Staircase
        west_ledge.connect(west_ledge_chest4, None) # West Kirby Ledge <--> Kirby Ledge Chest
        #TODO: west_ledge.connect(before_b_stairs, None, one_way=True) # West Kirby Ledge --> First Floor Main Area #[logic prep for staircase rando]
        #TODO: west_ledge.connect(entrance, None, one_way=True) # West Kirby Ledge --> Entrance #[logic prep for staircase rando]
        east_ledge.connect(east_ledge_chest3, None) # East Beamos Ledge <--> Beamos Ledge Chest
        #TODO: east_ledge.connect(before_a_stairs, None, one_way=True) # East Beamos Ledge --> Before Locked Staircase #[logic prep for staircase rando]
        #TODO: east_ledge.connect(entrance, None, one_way=True) # East Beamos Ledge --> Entrance #[logic prep for staircase rando]

        # connect floor 1 & 2
        before_a_stairs.connect(after_a_stairs, None) # Before Locked Staircase <--> Ball Room
        before_b_stairs.connect(after_b_stairs, None) # First Floor Main Area <--> Horseheads Staircase
        before_c_stairs.connect(after_c_stairs, None) # Two Peahat, Moldorm Room <--> North Three-of-a-Kind Puzzle
        before_d_stairs.connect(after_d_stairs, None) # Peg Locked Staircase <--> Hinox Area
        ne_pillar.connect(before_b_stairs, None, one_way=True) # Northeast Pillar Area --> First Floor Main Area
        se_pillar.connect(before_b_stairs, None) # Southeast Pillar Area <--> First Floor Main Area
        se_pillar.connect(before_c_stairs, OR(r.hit_switch, FEATHER)) # Southeast Pillar Area <--> Two Peahat, Moldorm Room
        tile_room.connect(west_ledge, None, one_way=True) # Floating Tile Fight --> West Kirby Ledge
        after_d_stairs.connect(west_ledge, None, one_way=True) # Hinox Area --> West Kirby Ledge
        pegs_after_a_stairs.connect(east_ledge, None, one_way=True) # On Pegs Around Chest --> East Beamos Ledge

        # floor 2
        after_a_stairs.connect(ne_pillar, None) # Ball Room <--> Northeast Pillar Area #TODO: delete in favor of casual logic commented out below
        ne_pillar.connect(ne_pillar_chest5, POWER_BRACELET) # Northeast Pillar Area <--> Horse Head, Bubble Chest
        after_b_stairs.connect(ne_pillar, r.hit_switch) # Horseheads Staircase <--> Northeast Pillar Area
        ne_pillar.connect(se_pillar, FEATHER) # Northeast Pillar Area <--> Southeast Pillar Area
        after_c_stairs.connect(after_c_stairs_chest2, r.enemy_requirements["THREE_OF_A_KIND"]) # North Three-of-a-Kind Puzzle <-->  #TODO: When ROM patched to reset ball on S&Q in ROM, then add bracelet method
        after_c_stairs.connect(spike_corridor, FEATHER) # [logic prep for staircase rando]
        spike_corridor.connect(se_pillar, FEATHER, one_way=True) # Between Pillar Pushbocks --> Southeast Pillar Area
        nw_pillar.connect(spike_corridor, FEATHER, one_way=True) # Northwest Pillar Area --> Between Pillar Pushbocks
        after_d_stairs.connect(tile_room, None, one_way=True) # Hinox Area --> Floating Tile Fight
        tile_room.connect(nw_pillar, None) # Floating Tile Fight <--> Northwest Pillar Area
        after_d_stairs.connect(after_d_stairs_drop2, r.miniboss_requirements["HINOX"]) # Hinox Area <--> Kinox Key
        after_d_stairs.connect(keylock_ledge, FOUND(KEY7, 3)) # Hinox Area <--> Key Locked Ledge
        after_d_stairs.connect(pegs_after_a_stairs, OR(r.hit_switch)) # Hinox Area <--> On Pegs Around Chest #TODO: REPLACE with below
        #TODO: after_a_stairs.connect(pegs_after_a_stairs, BOOMERANG) # Ball Room <--> On Pegs Around Ches # NEW VERSION
        #TODO: before_b_stairs.connect(pegs_after_a_stairs, OR(BOOMERANG, BOW, BOMB, MAGIC_ROD, COUNT(SWORD,2))) # Hinox Area <--> On Pegs Around Ches # NEW VERSION
        keylock_ledge.connect(pegs_after_a_stairs, None, one_way=True) # Key Locked Ledge --> On Pegs Around Chest
        keylock_ledge.connect(se_pillar, None, one_way=True) # Key Locked Ledge --> Southeast Pillar Area
        keylock_ledge.connect(after_d_stairs, None, one_way=True) # Key Locked Ledge --> Hinox Area
        pegs_after_a_stairs.connect(after_d_stairs, None, one_way=True) # On Pegs Around Chest --> Hinox Area
        pegs_after_a_stairs.connect(pegs_after_a_stairs_chest7, None) # On Pegs Around Chest --> Mirror Shield Chest
        nw_pillar.connect(bomb_corridor, BOMB) # Northwest Pillar Area <--> Bombable Wall Corridor
        bomb_corridor.connect(bombwall_owl, BOMB) # Bombable Wall Corridor <--> By Pit Owl
        #TODO: bomb_corridor.connect(after_d_stairs, None, one_way=True) # Bombable Wall Corridor --> Hinox Area # push blocks #[logic prep for staircase rando]
        bombwall_owl.connect(sw_pillar, HOOKSHOT) # By Pit Owl <--> Southwest Pillar Area
        sw_pillar.connect(sw_pillar_chest6, r.enemy_requirements["THREE_OF_A_KIND"]) # Southwest Pillar Area <--> Three of a Kind, Pit Chest #TODO: you can't really use any kill requirement pillar side of pushblocks
        sw_pillar.connect(final_pillar_fallen, POWER_BRACELET) # Southwest Pillar Area <--> Final Pillar Destroyed
        after_d_stairs.connect(before_e_stairs, None) # Hinox Area <--> Stairs Leading to 3rd Floor

        # connect floor 2 & 3
        before_e_stairs.connect(after_e_stairs, None) # Stairs Leading to 3rd Floor <--> Third Floor Entry
        final_pillar_fallen.connect(after_boss_door, NIGHTMARE_KEY7) # Final Pillar Destroyed <--> After Boss Door
        final_pillar_fallen.connect(boss_backdoor, None) # Final Pillar Destroyed <--> Boss Backdoor Room

        # floor 3
        after_e_stairs.connect(miniboss_room, None) # Third Floor Entry <--> Miniboss Room
        miniboss_room.connect(after_miniboss_room, r.miniboss_requirements[world_setup.miniboss_mapping[6]]) # Miniboss Room <--> After Miniboss Room
        after_miniboss_room.connect(after_miniboss_room_chest8, None) # After Miniboss Room <--> Nightmare Key/After Grim Creeper Chest

        # floor 3 after cutscene
        #TODO: boss_backdoor.connect(after_boss_door, AND(r.attack_hookshot_no_bomb, FOUND(KEY7, 3)))
        after_boss_door.connect(conveyor_room, None) # After Boss Door <--> Conveyor Horseheads Room
        conveyor_room.connect(conveyor_room_chest9, POWER_BRACELET) # Conveyor Horseheads Room <--> Conveyor Beamos Chest
        after_boss_door.connect(pre_boss_room, HOOKSHOT) # After Boss Door <--> Before Boss
        pre_boss_room.connect(after_boss_door, None, one_way=True) # Before Boss --> After Boss Door
        pre_boss_room.connect(boss_room, None) # Before Boss <--> Boss Room
        boss_room.connect(boss_room_drop3, r.boss_requirements[world_setup.boss_mapping[6]]) # Boss Room <--> Heart Container
        boss_room.connect(instrument, r.boss_requirements[world_setup.boss_mapping[6]]) # Boss Room <--> Instrument Room

        # key logic patch
        if options.dungeon_items not in {'localnightmarekey', 'keysanity', 'keysy', 'smallkeys'}:
            entrance_drop1.items[0].forced_item = KEY7

        #TODO: if options.logic == "casual":
            #TODO: after_a_stairs.connect(ne_pillar, POWER_BRACELET) # intended method is to pull lever
        #TODO: else:
            #TODO: after_a_stairs.connect(ne_pillar, None) # Ball Room <--> Northeast Pillar Area
            #TODO: after_a_stairs.connect(after_d_stairs, BOOMERANG) # Ball Room <--> Hinox Area

        #TODO if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            #TODO: after_c_stairs.connect(spike_corridor, None) # [logic prep for staircase rando] # forced damage so cannot be in normal logic

        if options.logic == 'glitched' or options.logic == 'hell':
            entrance.connect(before_b_stairs, r.super_jump_sword) # superjump in the center to get on raised blocks sword added to help since it has to be a low jump
            before_b_stairs.connect(east_ledge, r.super_jump_feather) # superjump in spike switch room to right ledge
            spike_corridor.connect(nw_pillar, OR(r.shaq_jump, r.super_jump_feather)) # superjump from right wall or shaq jump off pushblock
            west_ledge.connect(before_d_stairs, r.boots_jump, one_way = True) # without hitting the switch, drop off ledge onto peg wall, and boots jump to pegs blocking stairs
            after_d_stairs.connect(bombwall_owl, r.sideways_block_push) # sideways block push to get to owl statue by bomb wall
            after_d_stairs.connect(sw_pillar, r.sideways_block_push) # sideways block push to get to SW pillar area
            #TODO: after_d_stairs.connect(bomb_corridor, AND(r.wall_clip, r.shaq_jump)) #[logic prep for staircase rando]
            #TODO: bombwall_owl.connect(after_d_stairs, r.zoomerang_buffer) #[logic prep for staircase rando]
            #TODO: sw_pillar.connect(after_d_stairs, r.zoomerang_buffer) #[logic prep for staircase rando]
            sw_pillar.connect(sw_pillar_chest6, POWER_BRACELET) #TODO: Not really an accurate statement, as you can't do the block push from the north side. evaluate moving to hard logic, or even connecting from hinox area?
            #TODO: after_e_stairs.connect(conveyor_room_chest9, AND(FOUND(KEY7, 3), r.hookshot_clip_block, r.super_jump_feather)) # hookshot clip pot in upper right while 2 blocks to the left of it repeatedly until wall clipped, then superjump onto pegs
            #TODO: boss_backdoor.connect(conveyor_room_chest9, AND(FOUND(KEY7, 3), r.hookshot_clip_block, r.super_jump_feather)) # hookshot clip pot in upper right while 2 blocks to the left of it repeatedly until wall clipped, then superjump onto pegs
            after_d_stairs.connect(final_pillar_fallen, r.bomb_trigger) # bomb trigger pillar
            final_pillar_fallen.connect(pre_boss_room, r.super_jump_feather) # superjump on top of goomba to extend superjump to boss door plateau
            
        if options.logic == 'hell':
            #TODO: entrance.connect(before_a_stairs, r.boots_superbump) # boots to run, then bow or rod to run backwards, then hold shield so blade bumps you over wall #[logic prep for staircase rando]
            #TODO: entrance.connect(west_ledge, r.super_bump) # enter SW room wall clipped, line up with wizrobes, and repeat super bumps to move up onto the ledge (very precise)
            entrance.connect(east_ledge, AND(r.super_jump_boots, r.shield_bump)) # along bottom wall in first key room, setup boots super jump, but hold shield after the jump to bump down to ledge
            #TODO: after_b_stairs.connect(ne_pillar, r.zoomerang_buffer) # zoomerang gets you out of saircase in horsehead room if the entrance was randomized and you couldn't hit a switch  #[logic prep for staircase rando]
            entrance.connect(before_b_stairs, r.super_jump_feather) # superjump in the center to get on raised blocks, hell because the jump has to be very low
            entrance.connect(before_b_stairs, r.boots_superhop) # boots superhop in the center to get on raised blocks
            before_b_stairs.connect(east_ledge, r.boots_superhop) # boots superhop from room with spike switch
            before_c_stairs.connect(before_b_stairs, r.super_bump) #[logic prep for staircase rando]
            before_c_stairs.connect(west_ledge, r.super_bump) # super bump but into kirby mouth, it can spit you out with no-clip and land on ledge (need wall clip from c staircase) #[logic prep for staircase rando]
            spike_corridor.connect(ne_pillar, r.pit_buffer_boots, one_way=True) #[logic prep for staircase rando]
            #TODO: after_d_stairs.connect(se_pillar, r.boots_superhop, one_way = True) #[logic prep for staircase rando]
            #TODO: after_d_stairs.connect(se_pillar, r.super_bump, one_way = True) #[logic prep for staircase rando]
            #TODO: after_d_stairs.connect(keylock_ledge, r.boots_superbump) # running super bump off antifairy to get on ledge without key
            #TODO: bombwall_owl.connect(sw_pillar, r.pit_buffer_boots) 
            #TODO: sw_pillar.connect(sw_pillar_chest7, None) # push blocks to stun suit buddies and spawn chest #quite difficult, should we include this?
            final_pillar_fallen.connect(pre_boss_room, r.boots_superhop) # boots superhop on top of goomba to extend superhop to boss door plateau
            #TODO: after_e_stairs.connect(conveyor_room_chest9, OR(r.super_bump, r.super_poke)) # superjump and rebound off peahat onto pegs
            #TODO: boss_backdoor.connect(after_boss_door, OR(r.super_bump, r.super_poke)) # superjump and rebound off peahat onto pegs
            #TODO: final_pillar_fallen.connect(pre_boss, r.super_jump_feather) #[logic prep for staircase rando]
            #TODO: pre_boss_room.connect(instrument, AND(PEGASUS_BOOTS, r.shield_bump)) # walk off ledge holding shield, then use shield to backflip and goomba surf to instrument #TODO: boots helps if the landing is poor, maybe tracker only without boots?
            

        
        self.entrance = entrance
        self.final_room = instrument


class NoDungeon7:
    def __init__(self, options, world_setup, r):
        entrance = Location("D7 Entrance", dungeon=7)
        boss = Location(dungeon=7).add(HeartContainer(0x223), Instrument(0x22c)).connect(entrance, r.boss_requirements[
            world_setup.boss_mapping[6]])

        self.entrance = entrance
