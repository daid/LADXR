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
from .requirements import AND, OR, COUNT, FOUND, boss_requirements
from .location import Location
from locations.items import *


class Logic:
    def __init__(self, configuration_options, *, start_house_index=None, entranceMapping=None, bossMapping=None):
        self.start_house_index = start_house_index
        self.entranceMapping = entranceMapping
        self.bossMapping = bossMapping

        if configuration_options.overworld == "dungeondive":
            world = overworld.DungeonDiveOverworld(configuration_options)
        else:
            world = overworld.World(configuration_options)

        world.start.connect(world.start_locations[start_house_index], None)

        dungeons = [
            dungeon1.Dungeon1(configuration_options, boss_requirements[bossMapping[0]]),
            dungeon2.Dungeon2(configuration_options, boss_requirements[bossMapping[1]]),
            dungeon3.Dungeon3(configuration_options, boss_requirements[bossMapping[2]]),
            dungeon4.Dungeon4(configuration_options, boss_requirements[bossMapping[3]]),
            dungeon5.Dungeon5(configuration_options, boss_requirements[bossMapping[4]]),
            dungeon6.Dungeon6(configuration_options, boss_requirements[bossMapping[5]]),
            dungeon7.Dungeon7(configuration_options, boss_requirements[bossMapping[6]]),
            dungeon8.Dungeon8(configuration_options, boss_requirements[bossMapping[7]]),
            dungeonColor.DungeonColor(configuration_options, boss_requirements[bossMapping[8]])
        ]

        dungeons[entranceMapping[0]].entrance.connect(world.dungeon1_entrance, None)
        dungeons[entranceMapping[1]].entrance.connect(world.dungeon2_entrance, None)
        dungeons[entranceMapping[2]].entrance.connect(world.dungeon3_entrance, None)
        dungeons[entranceMapping[3]].entrance.connect(world.dungeon4_entrance, None)
        dungeons[entranceMapping[4]].entrance.connect(world.dungeon5_entrance, None)
        dungeons[entranceMapping[5]].entrance.connect(world.dungeon6_entrance, None)
        dungeons[entranceMapping[6]].entrance.connect(world.dungeon7_entrance, None)
        dungeons[entranceMapping[7]].entrance.connect(world.dungeon8_entrance, None)
        dungeons[entranceMapping[8]].entrance.connect(world.dungeon9_entrance, None)

        self.start = world.start
        self.windfish = world.windfish
        self.location_list = []
        self.iteminfo_list = []

        self.__location_set = set()
        self.__recursiveFindAll(self.start)
        del self.__location_set

        if configuration_options.bowwow != 'normal':
            # We cheat in bowwow mode, we pretend we have the sword, as bowwow can pretty much do all what the sword can do.
            # Except for taking out bushes (and crystal pillars are removed)
            if SWORD in requirements.bush:
                requirements.bush.remove(SWORD)

        for ii in self.iteminfo_list:
            ii.configure(configuration_options)

    def dumpFlatRequirements(self):
        def __rec(location, req):
            if hasattr(location, "flat_requirements"):
                new_flat_requirements = requirements.mergeFlat(location.flat_requirements, requirements.flatten(req))
                if new_flat_requirements == location.flat_requirements:
                    return
                location.flat_requirements = new_flat_requirements
            else:
                location.flat_requirements = requirements.flatten(req)
            for connection, requirement in location.simple_connections:
                __rec(connection, AND(req, requirement) if req else requirement)
            for connection, requirement in location.gated_connections:
                __rec(connection, AND(req, requirement) if req else requirement)
        __rec(self.start, None)
        for ii in self.iteminfo_list:
            print(ii)
            for fr in ii._location.flat_requirements:
                print("    " + ", ".join(sorted(map(str, fr))))

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


class MultiworldLogic:
    def __init__(self, configuration_options, rnd):
        self.worlds = []
        self.start = Location()
        self.location_list = [self.start]
        self.iteminfo_list = []

        for n in range(configuration_options.multiworld):
            entranceMapping = list(range(9))
            bossMapping = list(range(8))
            if configuration_options.dungeonshuffle:
                rnd.shuffle(entranceMapping)
            if configuration_options.bossshuffle:
                rnd.shuffle(bossMapping)
            bossMapping += [8]  # Shuffling the color dungeon boss does not work properly, so we ignore that one.
            start_house_index = 0

            world = Logic(configuration_options.multiworld_options[n], start_house_index=start_house_index, entranceMapping=entranceMapping, bossMapping=bossMapping)
            for ii in world.iteminfo_list:
                ii.world = n

            for loc in world.location_list:
                loc.simple_connections = [(target, addWorldIdToRequirements(n, req)) for target, req in loc.simple_connections]
                loc.gated_connections = [(target, addWorldIdToRequirements(n, req)) for target, req in loc.gated_connections]
                loc.items = [MultiworldItemInfoWrapper(n, configuration_options.multiworld, ii) for ii in loc.items]
                self.iteminfo_list += loc.items

            self.worlds.append(world)
            self.start.simple_connections += world.start.simple_connections
            self.start.gated_connections += world.start.gated_connections
            self.start.items += world.start.items
            world.start.items.clear()
            self.location_list += world.location_list

        self.entranceMapping = None


class MultiworldItemInfoWrapper:
    def __init__(self, world, world_count, target):
        self.world = world
        self.world_count = world_count
        self.target = target
        self.MULTIWORLD_OPTIONS = None

    @property
    def priority(self):
        return self.target.priority

    @property
    def forced_item(self):
        if self.target.forced_item is None:
            return None
        if "_W" in self.target.forced_item:
            return self.target.forced_item
        return "%s_W%d" % (self.target.forced_item, self.world)

    def read(self, rom):
        return "%s_W%d" % (self.target.read(rom), self.world)

    def getOptions(self):
        if self.MULTIWORLD_OPTIONS is None:
            options = self.target.getOptions()
            if self.target.MULTIWORLD and len(options) > 1:
                self.MULTIWORLD_OPTIONS = []
                for n in range(self.world_count):
                    self.MULTIWORLD_OPTIONS += ["%s_W%d" % (t, n) for t in options]
            else:
                self.MULTIWORLD_OPTIONS = ["%s_W%d" % (t, self.world) for t in options]
        return self.MULTIWORLD_OPTIONS

    def patch(self, rom, option):
        idx = option.rfind("_W")
        world = int(option[idx+2:])
        option = option[:idx]
        if not self.target.MULTIWORLD:
            assert self.world == world
            self.target.patch(rom, option)
        else:
            self.target.patch(rom, option, multiworld=world)

    def __repr__(self):
        return "W%d:%s" % (self.world, repr(self.target))


def addWorldIdToRequirements(world, req):
    if req is None:
        return None
    if isinstance(req, str):
        return "%s_W%d" % (req, world)
    if isinstance(req, COUNT):
        return COUNT(addWorldIdToRequirements(world, req.item), req.amount)
    if isinstance(req, FOUND):
        return FOUND(addWorldIdToRequirements(world, req.item), req.amount)
    if isinstance(req, AND):
        return AND(*(addWorldIdToRequirements(world, r) for r in req))
    if isinstance(req, OR):
        return OR(*(addWorldIdToRequirements(world, r) for r in req))
    raise RuntimeError("Unknown requirement type: %s" % (req))
