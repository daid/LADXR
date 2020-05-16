from . import overworld
from . import dungeon1
from . import dungeon2
from . import dungeon3
from location import AND, OR

dungeon1.entrance.connect(overworld.start, "TAIL_KEY")
dungeon2.entrance.connect(overworld.swamp, "FEATHER")  # TODO: requires saving chomp
dungeon3.entrance.connect(overworld.center_area, AND("SLIME_KEY", OR("FLIPPERS", "FEATHER")))
start = overworld.start
