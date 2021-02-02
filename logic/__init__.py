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
from worldSetup import WorldSetup


class Logic:
    def __init__(self, configuration_options, *, world_setup):
        self.world_setup = world_setup

        if configuration_options.overworld == "dungeondive":
            world = overworld.DungeonDiveOverworld(configuration_options)
        else:
            world = overworld.World(configuration_options, world_setup)

        world.start.connect(world.start_locations[world_setup.start_house_index], None)

        dungeons = [
            dungeon1.Dungeon1(configuration_options, world_setup),
            dungeon2.Dungeon2(configuration_options, world_setup),
            dungeon3.Dungeon3(configuration_options, world_setup),
            dungeon4.Dungeon4(configuration_options, world_setup),
            dungeon5.Dungeon5(configuration_options, world_setup),
            dungeon6.Dungeon6(configuration_options, world_setup),
            dungeon7.Dungeon7(configuration_options, world_setup),
            dungeon8.Dungeon8(configuration_options, world_setup),
            dungeonColor.DungeonColor(configuration_options, world_setup)
        ]

        dungeons[world_setup.dungeon_entrance_mapping[0]].entrance.connect(world.dungeon1_entrance, None)
        dungeons[world_setup.dungeon_entrance_mapping[1]].entrance.connect(world.dungeon2_entrance, None)
        dungeons[world_setup.dungeon_entrance_mapping[2]].entrance.connect(world.dungeon3_entrance, None)
        dungeons[world_setup.dungeon_entrance_mapping[3]].entrance.connect(world.dungeon4_entrance, None)
        dungeons[world_setup.dungeon_entrance_mapping[4]].entrance.connect(world.dungeon5_entrance, None)
        dungeons[world_setup.dungeon_entrance_mapping[5]].entrance.connect(world.dungeon6_entrance, None)
        dungeons[world_setup.dungeon_entrance_mapping[6]].entrance.connect(world.dungeon7_entrance, None)
        dungeons[world_setup.dungeon_entrance_mapping[7]].entrance.connect(world.dungeon8_entrance, None)
        dungeons[world_setup.dungeon_entrance_mapping[8]].entrance.connect(world.dungeon9_entrance, None)

        egg_trigger = AND(OCARINA, SONG1)
        if configuration_options.logic == 'glitched' or configuration_options.logic == 'hell':
            egg_trigger = OR(AND(OCARINA, SONG1), BOMB)

        if configuration_options.goal == "seashells":
            world.nightmare.connect(world.egg, COUNT(SEASHELL, 20))
        elif configuration_options.goal == "raft":
            world.nightmare.connect(world.egg, egg_trigger)
        else:
            goal = int(configuration_options.goal)
            if goal < 0:
                world.nightmare.connect(world.egg, None)
            elif goal == 0:
                world.nightmare.connect(world.egg, egg_trigger)
            elif goal == 8:
                world.nightmare.connect(world.egg, AND(egg_trigger, INSTRUMENT1, INSTRUMENT2, INSTRUMENT3, INSTRUMENT4, INSTRUMENT5, INSTRUMENT6, INSTRUMENT7, INSTRUMENT8))
            else:
                world.nightmare.connect(world.egg, AND(egg_trigger, COUNT([INSTRUMENT1, INSTRUMENT2, INSTRUMENT3, INSTRUMENT4, INSTRUMENT5, INSTRUMENT6, INSTRUMENT7, INSTRUMENT8], goal)))

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
            world_setup = WorldSetup()
            world_setup.randomize(configuration_options, rnd)
            world = Logic(configuration_options.multiworld_options[n], world_setup=world_setup)
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
    def nameId(self):
        return self.target.nameId

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
        if isinstance(req.item, list):
            return COUNT([addWorldIdToRequirements(world, item) for item in req.item], req.amount)
        return COUNT(addWorldIdToRequirements(world, req.item), req.amount)
    if isinstance(req, FOUND):
        return FOUND(addWorldIdToRequirements(world, req.item), req.amount)
    if isinstance(req, AND):
        return AND(*(addWorldIdToRequirements(world, r) for r in req))
    if isinstance(req, OR):
        return OR(*(addWorldIdToRequirements(world, r) for r in req))
    raise RuntimeError("Unknown requirement type: %s" % (req))
