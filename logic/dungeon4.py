from .requirements import *
from .location import Location
from locations import *


class Dungeon4:
    def __init__(self, options):
        entrance = Location(4)
        entrance.add(DungeonChest(0x179))  # stone slab chest
        entrance.add(DungeonChest(0x16A))  # map chest
        right_of_entrance = Location(4).add(DungeonChest(0x178)).connect(entrance, AND(SHIELD, attack_hookshot)) # 2 zol 1 spike enemy
        Location(4).add(DungeonChest(0x17B)).connect(right_of_entrance, SWORD) # room with key chest
        rightside_crossroads = Location(4).connect(entrance, AND(FEATHER, PEGASUS_BOOTS))  # 2 key chests on the right.
        pushable_block_chest = Location(4).add(DungeonChest(0x171)).connect(rightside_crossroads, BOMB) # lower chest
        puddle_crack_block_chest = Location(4).add(DungeonChest(0x165)).connect(rightside_crossroads, OR(BOMB, FLIPPERS)) # top right chest
        double_locked_room = Location(4).connect(right_of_entrance, KEY4)
        after_double_lock = Location(4).connect(double_locked_room, AND(KEY4, OR(FEATHER, FLIPPERS)))
        dungeon4_puddle_before_crossroads = Location(4).add(DungeonChest(0x175)).connect(after_double_lock, FLIPPERS)
        north_crossroads = Location(4).connect(after_double_lock, AND(FEATHER, PEGASUS_BOOTS))
        before_miniboss = Location(4).connect(north_crossroads, AND(KEY4, FOUND(KEY4, 3)))
        if options.owlstatues == "both" or options.owlstatues == "dungeon":
            Location(4).add(OwlStatue(0x16F)).connect(before_miniboss, STONE_BEAK4)
        sidescroller_key = Location(4).add(DroppedKey(0x169)).connect(before_miniboss, AND(attack_hookshot_powder, FLIPPERS))  # key that drops in the hole and needs swim to get
        Location(4).add(DungeonChest(0x16E)).connect(before_miniboss, FLIPPERS)  # chest with 50 rupees
        before_miniboss.add(DungeonChest(0x16D))  # gel chest
        before_miniboss.add(DungeonChest(0x168))  # key chest near the puzzle
        miniboss = Location(4).connect(before_miniboss, OR(FLIPPERS, AND(KEY4, FOUND(KEY4, 5), POWER_BRACELET, SWORD))) # flippers to move around miniboss through 5 tile room
        miniboss.add(DungeonChest(0x160))  # flippers chest

        to_the_nightmare_key = Location(4).connect(before_miniboss, AND(FEATHER, OR(FLIPPERS, PEGASUS_BOOTS)))  # 5 symbol puzzle (does not need flippers with boots + feather)
        to_the_nightmare_key.add(DungeonChest(0x176))

        before_boss = Location(4).connect(before_miniboss, AND(attack_hookshot, FLIPPERS, KEY4, FOUND(KEY4, 5)))
        boss = Location(4).add(HeartContainer(0x1FF)).connect(before_boss, AND(NIGHTMARE_KEY4, FLIPPERS, OR(SWORD, MAGIC_ROD, BOW, BOMB)))

        if options.logic == 'hard' or options.logic == 'glitched' or options.logic == 'hell':
            sidescroller_key.connect(before_miniboss, AND(FEATHER, BOOMERANG)) # grab the key jumping over the water and boomerang downwards
            sidescroller_key.connect(before_miniboss, AND(POWER_BRACELET, FLIPPERS)) # kill the zols with the pots in the room to spawn the key
            rightside_crossroads.connect(entrance, FEATHER) # jump across the corners
            puddle_crack_block_chest.connect(rightside_crossroads, FEATHER) # jump around the bombable block
            north_crossroads.connect(entrance, FEATHER) # jump across the corners
            after_double_lock.connect(entrance, FEATHER) # jump across the corners
            dungeon4_puddle_before_crossroads.connect(after_double_lock, FEATHER) # With a tight jump feather is enough to cross the puddle without flippers
            to_the_nightmare_key.connect(before_miniboss, OR(FEATHER, AND(FLIPPERS, PEGASUS_BOOTS))) # With a tight jump feather is enough to reach the top left switch without flippers
            before_boss.connect(before_miniboss, FEATHER) # jump to the bottom right corner of boss door room
            
        if options.logic == 'glitched' or options.logic == 'hell':    
            pushable_block_chest.connect(rightside_crossroads, FLIPPERS) # sideways block push to skip bombs
            sidescroller_key.connect(before_miniboss, AND(FEATHER, OR(attack_hookshot_powder, POWER_BRACELET))) # superjump into the hole to grab the key while falling into the water
            miniboss.connect(before_miniboss, FEATHER) # use jesus jump to transition over the water left of miniboss
        
        if options.logic == 'hell':
            rightside_crossroads.connect(entrance, AND(PEGASUS_BOOTS, HOOKSHOT)) # pit buffer into the wall of the first pit, then boots bonk across the center, hookshot to get to the rightmost pit to a second villa buffer on the rightmost pit
            pushable_block_chest.connect(rightside_crossroads, OR(PEGASUS_BOOTS, FEATHER)) # use feather to water clip into the top right corner of the bombable block, and sideways block push to gain access. Can boots bonk of top right wall, then water buffer to top of chest and boots bonk to water buffer next to chest
            north_crossroads.connect(entrance, AND(PEGASUS_BOOTS, HOOKSHOT)) # pit buffer into wall of the first pit, then boots bonk towards the top and hookshot spam to get across (easier with Piece of Power)
            after_double_lock.connect(entrance, PEGASUS_BOOTS) # boots bonk + pit buffer to the bottom
            dungeon4_puddle_before_crossroads.connect(after_double_lock, AND(PEGASUS_BOOTS, HOOKSHOT)) # boots bonk across the water bottom wall to the bottom left corner, then hookshot up
            miniboss.connect(before_miniboss, PEGASUS_BOOTS) # use boots bonk + water buffer to get on the bottom wall of the water transition south of miniboss, and transition left bonking of the wall
            before_boss.connect(before_miniboss, PEGASUS_BOOTS) # boots bonk across bottom wall then boots bonk to the platform before boss door
            
        self.entrance = entrance

