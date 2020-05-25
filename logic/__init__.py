from . import overworld
from . import dungeon1
from . import dungeon2
from . import dungeon3
from . import dungeon4
from . import dungeon5
from . import dungeon6
from . import dungeon7
from . import dungeon8
from .requirements import AND, OR, COUNT
from locations.items import *

def construct():
    world = overworld.World()
    d1 = dungeon1.Dungeon1()
    d2 = dungeon2.Dungeon2()
    d3 = dungeon3.Dungeon3()
    d4 = dungeon4.Dungeon4()
    d5 = dungeon5.Dungeon5()
    d6 = dungeon6.Dungeon6()
    d7 = dungeon7.Dungeon7()
    d8 = dungeon8.Dungeon8()

    d1.entrance.connect(world.start, TAIL_KEY)
    d2.entrance.connect(world.swamp, FEATHER)  # TODO: requires saving chomp
    d3.entrance.connect(world.center_area, AND(SLIME_KEY, OR(FLIPPERS, FEATHER)))
    d4.entrance.connect(world.right_mountains_1, ANGLER_KEY)
    d4.entrance.connect(world.center_area, AND(ANGLER_KEY, FLIPPERS))
    d5.entrance.connect(world.center_area, FLIPPERS)
    d6.entrance.connect(world.dungeon6_entrance, FACE_KEY)
    d7.entrance.connect(world.right_mountains_3, BIRD_KEY)
    d8.entrance.connect(world.left_side_mountain, AND(COUNT(SHIELD, 2), OCARINA, SWORD))  # TODO: Requires song3
    return world.start
