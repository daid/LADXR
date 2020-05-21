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

dungeon1.entrance.connect(overworld.start, TAIL_KEY)
dungeon2.entrance.connect(overworld.swamp, FEATHER)  # TODO: requires saving chomp
dungeon3.entrance.connect(overworld.center_area, AND(COUNT(GOLD_LEAF, 6), OR(FLIPPERS, FEATHER)))
dungeon4.entrance.connect(overworld.right_mountains_1, ANGLER_KEY)
dungeon4.entrance.connect(overworld.center_area, AND(ANGLER_KEY, FLIPPERS))
dungeon5.entrance.connect(overworld.center_area, FLIPPERS)
dungeon6.entrance.connect(overworld.dungeon6_entrance, FACE_KEY)
dungeon7.entrance.connect(overworld.right_mountains_3, BIRD_KEY)
dungeon8.entrance.connect(overworld.left_side_mountain, AND(COUNT(SHIELD, 2), OCARINA, SWORD))  # TODO: Requires song3
start = overworld.start
