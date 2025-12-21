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
from . import dungeonChain
from .requirements import AND, OR, COUNT, COUNTS, FOUND, RequirementsSettings
from .location import Location
from locations.items import *
from locations.keyLocation import KeyLocation
import worldSetup
import itempool
import mapgen


class Logic:
    def __init__(self, configuration_options, *, world_setup, requirements_settings=None):
        self.world_setup = world_setup

        if requirements_settings == None:
            requirements_settings = RequirementsSettings(configuration_options)

        r = requirements_settings
        self.requirements_settings = requirements_settings

        if configuration_options.overworld == "dungeondive":
            world = overworld.DungeonDiveOverworld(configuration_options, r)
        elif configuration_options.overworld == "random":
            world = mapgen.LogicGenerator(configuration_options, world_setup, r, world_setup.map)
        elif configuration_options.overworld == "dungeonchain":
            world = overworld.DungeonChain(configuration_options, r)
        elif configuration_options.overworld == "alttp":
            world = overworld.ALttP(configuration_options, world_setup, r)
        else:
            world = overworld.World(configuration_options, world_setup, r)

        if configuration_options.overworld == "nodungeons":
            world.updateIndoorLocation("d1", dungeon1.NoDungeon1(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d2", dungeon2.NoDungeon2(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d3", dungeon3.NoDungeon3(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d4", dungeon4.NoDungeon4(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d5", dungeon5.NoDungeon5(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d6", dungeon6.NoDungeon6(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d7", dungeon7.NoDungeon7(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d8", dungeon8.NoDungeon8(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d0", dungeonColor.NoDungeonColor(configuration_options, world_setup, r).entrance)
        elif configuration_options.overworld == "dungeonchain":
            dungeonChain.construct(configuration_options, world_setup=world_setup, world=world, requirements_settings=r)
        elif configuration_options.overworld != "random":
            world.updateIndoorLocation("d1", dungeon1.Dungeon1(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d2", dungeon2.Dungeon2(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d3", dungeon3.Dungeon3(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d4", dungeon4.Dungeon4(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d5", dungeon5.Dungeon5(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d6", dungeon6.Dungeon6(configuration_options, world_setup, r).entrance)
            world.updateIndoorLocation("d7", dungeon7.Dungeon7(configuration_options, world_setup, r).entrance)
            if configuration_options.overworld != "alttp":
                world.updateIndoorLocation("d8", dungeon8.Dungeon8(configuration_options, world_setup, r).entrance)
                world.updateIndoorLocation("d0", dungeonColor.DungeonColor(configuration_options, world_setup, r).entrance)
            else:
                world.updateIndoorLocation("d8", dungeon8.Dungeon8(configuration_options, world_setup, r, back_entrance_heartpiece=0x0E0).entrance)

        if configuration_options.overworld in {"alttp"}:
            world_setup.entrance_mapping = {}
            for k, v in world.entrances.items():
                if k.endswith(":inside"):
                    world_setup.entrance_mapping[k] = k[:-7]
                else:
                    world_setup.entrance_mapping[k] = f"{k}:inside"
        if configuration_options.overworld not in {"dungeonchain", "random"}:
            for k in world.entrances.keys():
                assert k in world_setup.entrance_mapping, k
            for k in world_setup.entrance_mapping.keys():
                assert k in world.entrances, k

            for source, target in world_setup.entrance_mapping.items():
                se = world.entrances[source]
                if not se.location:
                    continue
                te = world.entrances[target]
                empty_cycle_targets = {target}
                while te.location is None:
                    # If the target is empty, we need to check if we can get from that empty location to somewhere else.
                    assert te.requirement is None
                    assert not te.enterIsSet()
                    assert not te.exitIsSet()
                    target = world_setup.entrance_mapping[target]
                    if target in empty_cycle_targets:
                        break
                    empty_cycle_targets.add(target)
                    te = world.entrances[target]
                if te.location and te.location != se.location:
                    if se.requirement is not None and te.requirement is not None:
                        se.location.connect(te.location, AND(se.requirement, te.requirement), back=False)
                    elif se.requirement is not None:
                        se.location.connect(te.location, se.requirement, back=False)
                    else:
                        se.location.connect(te.location, te.requirement, back=False)
                    if se.enterIsSet():
                        se.location.connect(te.location, se.one_way_enter_requirement, back=False)
                    if te.exitIsSet():
                        se.location.connect(te.location, te.one_way_exit_requirement, back=False)

        egg_trigger = AND(OCARINA, SONG1)
        if configuration_options.logic == 'glitched' or configuration_options.logic == 'hell':
            egg_trigger = OR(AND(OCARINA, SONG1), BOMB)

        if configuration_options.overworld == "dungeonchain":
            pass  # Dungeon chain has no egg, so no egg requirement.
        elif world_setup.goal == "seashells":
            world.nightmare.connect(world.egg, COUNT(SEASHELL, 20))
        elif world_setup.goal in ("raft", "bingo", "bingo-double", "bingo-triple", "bingo-full", "maze"):
            world.nightmare.connect(world.egg, egg_trigger)
        elif isinstance(world_setup.goal, str) and world_setup.goal.startswith("="):
            world.nightmare.connect(world.egg, AND(egg_trigger, *["INSTRUMENT%s" % c for c in world_setup.goal[1:]]))
        elif world_setup.goal == 'open':
            world.nightmare.connect(world.egg, None)
        elif world_setup.goal_count == 0:
            world.nightmare.connect(world.egg, egg_trigger)
        elif world_setup.goal_count == 8:
            world.nightmare.connect(world.egg, AND(egg_trigger, INSTRUMENT1, INSTRUMENT2, INSTRUMENT3, INSTRUMENT4, INSTRUMENT5, INSTRUMENT6, INSTRUMENT7, INSTRUMENT8))
        else:
            world.nightmare.connect(world.egg, AND(egg_trigger, COUNTS([INSTRUMENT1, INSTRUMENT2, INSTRUMENT3, INSTRUMENT4, INSTRUMENT5, INSTRUMENT6, INSTRUMENT7, INSTRUMENT8], world_setup.goal_count)))

        if configuration_options.dungeon_keys == 'removed':
            for n in range(9):
                for count in range(9):
                    world.start.add(KeyLocation("KEY%d" % (n)))
        if configuration_options.nightmare_keys == 'removed':
            for n in range(9):
                world.start.add(KeyLocation("NIGHTMARE_KEY%d" % (n)))
        if configuration_options.dungeon_beaks == 'removed':
            for n in range(9):
                world.start.add(KeyLocation("STONE_BEAK%d" % (n)))

        self.world = world
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
            for connection, requirement in location.connections:
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
        for connection, requirement in location.connections:
            self.__recursiveFindAll(connection)
