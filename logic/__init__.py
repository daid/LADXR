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
from .requirements import AND, OR, COUNT, FOUND
from .location import Location
from locations.items import *


class Logic:
    def __init__(self, configuration_options, rnd, *, entranceMapping=None):
        world = overworld.World(configuration_options)

        dungeons = [
            dungeon1.Dungeon1(configuration_options),
            dungeon2.Dungeon2(configuration_options),
            dungeon3.Dungeon3(configuration_options),
            dungeon4.Dungeon4(configuration_options),
            dungeon5.Dungeon5(configuration_options),
            dungeon6.Dungeon6(configuration_options),
            dungeon7.Dungeon7(configuration_options),
            dungeon8.Dungeon8(configuration_options),
            dungeonColor.DungeonColor(configuration_options)
        ]

        if entranceMapping is None:
            entranceMapping = list(range(9))
            if configuration_options.dungeonshuffle:
                rnd.shuffle(entranceMapping)
        self.entranceMapping = entranceMapping

        dungeons[entranceMapping[0]].entrance.connect(world.start, TAIL_KEY)
        dungeons[entranceMapping[1]].entrance.connect(world.swamp, OR(BOWWOW, MAGIC_ROD, HOOKSHOT))
        dungeons[entranceMapping[2]].entrance.connect(world.center_area, AND(SLIME_KEY, OR(FLIPPERS, FEATHER)))
        dungeons[entranceMapping[3]].entrance.connect(world.center_area, AND(ANGLER_KEY, OR(FLIPPERS, AND(POWER_BRACELET, SWORD, PEGASUS_BOOTS))))
        dungeons[entranceMapping[4]].entrance.connect(world.center_area, FLIPPERS)
        dungeons[entranceMapping[5]].entrance.connect(world.dungeon6_entrance, FACE_KEY)
        dungeons[entranceMapping[6]].entrance.connect(world.right_mountains_3, BIRD_KEY)
        dungeons[entranceMapping[7]].entrance.connect(world.dungeon8_entrance, AND(OCARINA, SWORD))  # TODO: Requires song3
        dungeons[entranceMapping[8]].entrance.connect(world.graveyard, POWER_BRACELET)
            
        self.start = world.start
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

        for n in range(2):
            world = Logic(configuration_options, rnd)
            for ii in world.iteminfo_list:
                ii.world = n

            for loc in world.location_list:
                loc.simple_connections = [(target, addWorldIdToRequirements(n, req)) for target, req in loc.simple_connections]
                loc.gated_connections = [(target, addWorldIdToRequirements(n, req)) for target, req in loc.gated_connections]
                loc.items = [MultiworldItemInfoWrapper(n, ii) for ii in loc.items]
                self.iteminfo_list += loc.items

            self.worlds.append(world)
            self.start.simple_connections += world.start.simple_connections
            self.start.gated_connections += world.start.gated_connections
            self.start.items += world.start.items
            world.start.items.clear()
            self.location_list += world.location_list

        self.entranceMapping = None


class MultiworldItemInfoWrapper:
    def __init__(self, world, target):
        self.world = world
        self.target = target
        self.MULTIWORLD_OPTIONS = None

    @property
    def priority(self):
        return self.target.priority

    def read(self, rom):
        return "%s_W%d" % (self.target.read(rom), self.world)

    def getOptions(self):
        if self.MULTIWORLD_OPTIONS is None:
            options = self.target.getOptions()
            if self.target.MULTIWORLD and len(options) > 1:
                self.MULTIWORLD_OPTIONS = []
                for n in range(2):
                    self.MULTIWORLD_OPTIONS += ["%s_W%d" % (t, n) for t in options]
            else:
                self.MULTIWORLD_OPTIONS = ["%s_W%d" % (t, self.world) for t in options]
        return self.MULTIWORLD_OPTIONS

    def patch(self, rom, option):
        world = int(option[option.rfind("_W") + 2:])
        rom.banks[0x3E][0x3300 + self.target.room] = world
        self.target.patch(rom, option[3:], cross_world=self.world != world)

    def __repr__(self):
        return "W%d:%s" % (self.world, repr(self.target))


def addWorldIdToRequirements(world, req):
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
