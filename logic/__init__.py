from . import overworld
from . import dungeon1
from . import dungeon2
from . import dungeon3
from . import dungeon4
from . import dungeon5
from . import dungeon6
from .requirements import AND, OR, COUNT
from locations.items import *

dungeon1.entrance.connect(overworld.start, TAIL_KEY)
dungeon2.entrance.connect(overworld.swamp, FEATHER)  # TODO: requires saving chomp
dungeon3.entrance.connect(overworld.center_area, AND("SLIME_KEY", OR(FLIPPERS, FEATHER)))
dungeon4.entrance.connect(overworld.right_mountains_1, ANGLER_KEY)
dungeon5.entrance.connect(overworld.center_area, FLIPPERS)
dungeon6.entrance.connect(overworld.dungeon6_entrance, FACE_KEY)
start = overworld.start
