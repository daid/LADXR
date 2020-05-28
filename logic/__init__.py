from . import overworld
from . import dungeon1
from . import dungeon2
from . import dungeon3
from . import dungeon4
from . import dungeon5
from . import dungeon6
from . import dungeon7
from . import dungeon8
from . import dungeonColor
from .requirements import AND, OR, COUNT
from locations.items import *


class Logic:
    def __init__(self, configuration_options):
        world = overworld.World()
        d1 = dungeon1.Dungeon1()
        d2 = dungeon2.Dungeon2()
        d3 = dungeon3.Dungeon3()
        d4 = dungeon4.Dungeon4()
        d5 = dungeon5.Dungeon5()
        d6 = dungeon6.Dungeon6()
        d7 = dungeon7.Dungeon7()
        d8 = dungeon8.Dungeon8()
        dColor = dungeonColor.DungeonColor()

        d1.entrance.connect(world.start, TAIL_KEY)
        d2.entrance.connect(world.swamp, FEATHER)  # TODO: requires saving chomp
        d3.entrance.connect(world.center_area, AND(SLIME_KEY, OR(FLIPPERS, FEATHER)))
        d4.entrance.connect(world.right_mountains_1, ANGLER_KEY)
        d4.entrance.connect(world.center_area, AND(ANGLER_KEY, FLIPPERS))
        d5.entrance.connect(world.center_area, FLIPPERS)
        d6.entrance.connect(world.dungeon6_entrance, FACE_KEY)
        d7.entrance.connect(world.right_mountains_3, BIRD_KEY)
        d8.entrance.connect(world.left_side_mountain, AND(COUNT(SHIELD, 2), OCARINA, SWORD))  # TODO: Requires song3
        dColor.entrance.connect(world.graveyard, POWER_BRACELET)

        self.start = world.start
        self.location_list = []
        self.iteminfo_list = []

        self.__location_set = set()
        self.__recursiveFindAll(self.start)
        del self.__location_set

        for ii in self.iteminfo_list:
            ii.configure(configuration_options)

    def __recursiveFindAll(self, location):
        if location in self.__location_set:
            return
        self.location_list.append(location)
        self.__location_set.add(location)
        for ii in location.items:
            self.iteminfo_list.append(ii)
        for connection, requirement in location.simple_connections:
            self.__recursiveFindAll(connection)
        for connection, requirement in location.gated_connections:
            self.__recursiveFindAll(connection)
