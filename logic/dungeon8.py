from .requirements import *
from .location import Location
from locations import *


class Dungeon8:
    def __init__(self, options):
        entrance = Location(8)
        entrance_up = Location(8).connect(entrance, FEATHER)
        entrance_left = Location(8).connect(entrance, attack_hookshot) # past hinox

        # left side
        entrance_left.add(DungeonChest(0x24D)) # zamboni room chest
        entrance_left.add(DungeonChest(0x25C)) # eye magnet chest
        entrance_left.add(DroppedKey(0x24C)) # vire drop key
        Location(8).add(DungeonChest(0x255)).connect(entrance_left, OR(HOOKSHOT, FEATHER))  # chest before lvl1 miniboss
        Location(8).add(DungeonChest(0x246)).connect(entrance_left, MAGIC_ROD)  # key chest that spawns after creating fire
        
        # right side
        bottomright_owl = Location(8).add(OwlStatue(0x253)).connect(entrance, AND(STONE_BEAK8, FEATHER, POWER_BRACELET)) # Two ways to reach this owl statue, but both require the same (except that one route requires bombs as well)
        Location(8).add(DungeonChest(0x259)).connect(entrance, OR(FEATHER, AND(attack_hookshot, POWER_BRACELET)))  # chest with slime
        bottom_right = Location(8).add(DroppedKey(0x25A)).connect(entrance, AND(FEATHER, OR(BOMB, AND(SWORD, POWER_BRACELET)))) # zamboni key drop; bombs for entrance up, sword + bracelet for entrance right through mimic room
        bottomright_pot_chest = Location(8).add(DungeonChest(0x25F)).connect(bottom_right, POWER_BRACELET) # 4 ropes pot room chest

        map_chest = Location(8).add(DungeonChest(0x24F)).connect(entrance, FEATHER)
        lower_center = Location(8).connect(entrance_up, KEY8)
        upper_center = Location(8).connect(lower_center, KEY8)
        Location(8).add(OwlStatue(0x245)).connect(upper_center, STONE_BEAK8)
        Location(8).add(DroppedKey(0x23E)).connect(upper_center, attack_skeleton) # 2 gibdos cracked floor; technically possible to use pits to kill but dumb
        medicine_chest = Location(8).add(DungeonChest(0x235)).connect(upper_center, HOOKSHOT)  # medicine chest
                                                                  
        middle_center_1 = Location(8).connect(upper_center, BOMB)
        middle_center_2 = Location(8).connect(middle_center_1, KEY8)
        middle_center_3 = Location(8).connect(middle_center_2, KEY8)
        miniboss_entrance = Location(8).connect(middle_center_3, KEY8)
        miniboss = Location(8).connect(miniboss_entrance, AND(HOOKSHOT, SWORD))  # hookshot to get to the miniboss, sword to kill
        miniboss.add(DungeonChest(0x237)) # fire rod chest

        up_left = Location(8).connect(upper_center, AND(attack_hookshot_powder, KEY8)) #TODO alternate path with fire rod through 2d section to nightmare key
        #up_left.connect(entrance_up, MAGIC_ROD, one_way=True)
        up_left.add(DungeonChest(0x240)) # beamos blocked chest
        Location(8).add(DungeonChest(0x23D)).connect(up_left, BOMB) # dodongo chest
        Location().add(HeartPiece(0x000)).connect(up_left, FEATHER)  # Outside the dungeon on the platform (feather is a requirement as it needs at least 1 requirement, and feather is always required to get here)
        Location(8).add(DroppedKey(0x241)).connect(up_left, BOW) # lava statue
        Location(8).add(OwlStatue(0x241)).connect(up_left, STONE_BEAK8)
        Location(8).add(DungeonChest(0x23A)).connect(up_left, HOOKSHOT) # ledge chest left of boss door

        cueball_req = Location(8).connect(entrance_up, AND(FEATHER, SWORD, MAGIC_ROD))
        nightmare_key = Location(8).add(DungeonChest(0x232)).connect(cueball_req, KEY8)

        # Bombing from the center dark rooms to the left so you can access more keys.
        # The south walls of center dark room can be bombed from lower_center too with bomb and feather for center dark room access from the south, allowing even more access. Not sure if this should be logic since "obscure"
        middle_center_2.connect(up_left, AND(BOMB, FEATHER), one_way=True) # does this even skip a key? both middle_center_2 and up_left come from upper_center with 1 extra key

        boss = Location(8).add(HeartContainer(0x234)).connect(entrance_up, AND(NIGHTMARE_KEY8, MAGIC_ROD))
        
        if options.logic == 'hard' or options.logic == 'glitched':
            #bottomright_owl.connect(entrance, AND(SWORD, POWER_BRACELET, PEGASUS_BOOTS)) # underground section past mimics, boots bonking across the gap to the ladder
            #bottom_right.connect(entrance, AND(SWORD, POWER_BRACELET, PEGASUS_BOOTS)) # underground section past mimics, boots bonking across the gap to the ladder
            #map_chest.connect(bottom_right, AND(POWER_BRACELET, PEGASUS_BOOTS, BOMB)) # underground section south of smasher, use pegasus boots to cross lava pillars
            #entrance_left.connect(up_left, FEATHER, one_way=True) # not hard, but only useful in hard/glitched. One way. Needs a requirement so added feather 
            up_left.connect(lower_center, AND(BOMB, FEATHER)) # blow up hidden walls from peahat room -> dark room -> eye statue room
            
        if options.logic == 'glitched':
            #bottomright_pot_chest.connect(entrance, AND(FEATHER, SWORD)) # use staircase backwards, subpixel manip for superjump past the pots
            lower_center.connect(entrance_up, FEATHER) # sideways block push / superjump in peahat room to get past keyblock
            miniboss.connect(lower_center, AND(BOMB, FEATHER, HOOKSHOT, SWORD)) # blow up hidden wall for darkroom, use feather + hookshot to clip past keyblock in front of stairs
            up_left.connect(lower_center, FEATHER) # use jesus jump in refill room left of peahats to clip bottom wall and push bottom block left, to get a place to super jump
            upper_center.connect(lower_center, FEATHER) # from up left you can jesus jump / lava swim around the key door next to the boss. Avoid circle referencing up_left + upper_center
            cueball_req.connect(up_left, AND(FEATHER, SWORD)) # superjump
            #cueball_req.connect(map_chest, AND(BOMB, PEGASUS_BOOTS, SWORD, MAGIC_ROD)) # bomb trigger lava filler to stairs, use boots bonk to cross 2d
            medicine_chest.connect(upper_center, FEATHER) # jesus super jump
            #boss.connect(map_chest, AND(NIGHTMARE_KEY8, BOMB, PEGASUS_BOOTS, MAGIC_ROD)) # bomb trigger lava filler to stairs, use boots bonk to cross 2d

        self.entrance = entrance
