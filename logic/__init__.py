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
from .requirements import AND, OR, COUNT, FOUND, RequirementsSettings
from .location import Location
from locations.items import *
from worldSetup import WorldSetup
import itempool


class Logic:
    def __init__(self, configuration_options, *, world_setup):
        self.world_setup = world_setup
        r = RequirementsSettings(configuration_options)

        if configuration_options.overworld == "dungeondive":
            world = overworld.DungeonDiveOverworld(configuration_options, r)
        else:
            world = overworld.World(configuration_options, world_setup, r)

        world.updateIndoorLocation("d1", dungeon1.Dungeon1(configuration_options, world_setup, r).entrance)
        world.updateIndoorLocation("d2", dungeon2.Dungeon2(configuration_options, world_setup, r).entrance)
        world.updateIndoorLocation("d3", dungeon3.Dungeon3(configuration_options, world_setup, r).entrance)
        world.updateIndoorLocation("d4", dungeon4.Dungeon4(configuration_options, world_setup, r).entrance)
        world.updateIndoorLocation("d5", dungeon5.Dungeon5(configuration_options, world_setup, r).entrance)
        world.updateIndoorLocation("d6", dungeon6.Dungeon6(configuration_options, world_setup, r).entrance)
        world.updateIndoorLocation("d7", dungeon7.Dungeon7(configuration_options, world_setup, r).entrance)
        world.updateIndoorLocation("d8", dungeon8.Dungeon8(configuration_options, world_setup, r).entrance)
        world.updateIndoorLocation("d0", dungeonColor.DungeonColor(configuration_options, world_setup, r).entrance)

        for k in world.overworld_entrance.keys():
            assert k in world_setup.entrance_mapping, k
        for k in world_setup.entrance_mapping.keys():
            assert k in world.overworld_entrance, k

        for entrance, indoor in world_setup.entrance_mapping.items():
            location, requirement, one_way_enter_requirement, one_way_exit_requirement = world.overworld_entrance[entrance]
            if world.indoor_location[indoor] is not None:
                location.connect(world.indoor_location[indoor], requirement)
                if one_way_enter_requirement is not None:
                    location.connect(world.indoor_location[indoor], one_way_enter_requirement, one_way=True)
                if one_way_exit_requirement is not None:
                    world.indoor_location[indoor].connect(location, one_way_exit_requirement, one_way=True)

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
    def __init__(self, configuration_options, rnd=None, *, world_setups=None):
        assert rnd or world_setups
        self.worlds = []
        self.start = Location()
        self.location_list = [self.start]
        self.iteminfo_list = []

        for n in range(configuration_options.multiworld):
            options = configuration_options.multiworld_options[n]
            world = None
            if world_setups:
                world = Logic(options, world_setup=world_setups[n])
            else:
                for cnt in range(1000):  # Try the world setup in case entrance randomization generates unsolvable logic
                    world_setup = WorldSetup()
                    world_setup.randomize(options, rnd)
                    world = Logic(options, world_setup=world_setup)
                    if options.entranceshuffle not in ("advanced", "expert", "insanity") or len(world.iteminfo_list) == sum(itempool.ItemPool(options, rnd).toDict().values()):
                        break

            for ii in world.iteminfo_list:
                ii.world = n

            for loc in world.location_list:
                loc.simple_connections = [(target, addWorldIdToRequirements(n, req)) for target, req in loc.simple_connections]
                loc.gated_connections = [(target, addWorldIdToRequirements(n, req)) for target, req in loc.gated_connections]
                loc.items = [MultiworldItemInfoWrapper(n, options, ii) for ii in loc.items]
                self.iteminfo_list += loc.items

            self.worlds.append(world)
            self.start.simple_connections += world.start.simple_connections
            self.start.gated_connections += world.start.gated_connections
            self.start.items += world.start.items
            world.start.items.clear()
            self.location_list += world.location_list

        self.entranceMapping = None


class MultiworldMetadataWrapper:
    def __init__(self, world, metadata):
        self.world = world
        self.metadata = metadata

    @property
    def name(self):
        return self.metadata.name

    @property
    def area(self):
        return "P%d %s" % (self.world + 1, self.metadata.area)

    @property
    def sphere(self):
        return self.metadata.sphere

    @sphere.setter
    def sphere(self, value):
        self.metadata.sphere = value


class MultiworldItemInfoWrapper:
    def __init__(self, world, configuration_options, target):
        self.world = world
        self.world_count = configuration_options.multiworld
        self.target = target
        self.dungeon_items = configuration_options.dungeon_items
        self.MULTIWORLD_OPTIONS = None
        self.item = None

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

    @property
    def room(self):
        return self.target.room

    @property
    def metadata(self):
        return MultiworldMetadataWrapper(self.world, self.target.metadata)

    @property
    def MULTIWORLD(self):
        return self.target.MULTIWORLD

    def read(self, rom):
        world = rom.banks[0x3E][0x3300 + self.target.room] if self.target.MULTIWORLD else self.world
        return "%s_W%d" % (self.target.read(rom), world)

    def getOptions(self):
        if self.MULTIWORLD_OPTIONS is None:
            options = self.target.getOptions()
            if self.target.MULTIWORLD and len(options) > 1:
                self.MULTIWORLD_OPTIONS = []
                for n in range(self.world_count):
                    self.MULTIWORLD_OPTIONS += ["%s_W%d" % (t, n) for t in options if n == self.world or self.canMultiworld(t)]
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

    # Return true if the item is allowed to be placed in any world, or false if it is
    # world specific for this check.
    def canMultiworld(self, option):
        if self.dungeon_items == 'standard':
            if option.startswith("MAP"):
                return False
            if option.startswith("COMPASS"):
                return False
            if option.startswith("STONE_BEAK"):
                return False
        if self.dungeon_items in ('standard', 'localkeys'):
            if option.startswith("KEY"):
                return False
        if self.dungeon_items in ('standard', 'localkeys', 'localnightmarekey'):
            if option.startswith("NIGHTMARE_KEY"):
                return False
        return True

    @property
    def location(self):
        return self.target.location

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
