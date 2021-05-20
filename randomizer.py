import random
import zipfile
import os
import binascii
from datetime import datetime

import explorer
import logic
from locations.items import *
import generator
import spoilerLog
import itempool
from plan import Plan
from worldSetup import WorldSetup


class Error(Exception):
    pass


class Randomizer:
    def __init__(self, options, *, seed=None):
        self.seed = seed
        self.plan = None
        if self.seed is None:
            self.seed = os.urandom(16)
        self.rnd = random.Random(self.seed)
        if options.race:
            self.rnd.random()  # Just pull 1 random number so race seeds are different then from normal seeds but still stable.
        if isinstance(options.goal, range):
            options.goal = self.rnd.randint(min(options.goal), max(options.goal))
        if options.plan:
            assert options.multiworld is None
            self.plan = Plan(options.plan)

        if options.multiworld:
            self.__logic = logic.MultiworldLogic(options, self.rnd)
        else:
            for n in range(1000):  # Try the world setup in case entrance randomization generates unsolvable logic
                world_setup = WorldSetup()
                world_setup.randomize(options, self.rnd)
                self.__logic = logic.Logic(options, world_setup=world_setup)
                if options.entranceshuffle not in ("advanced", "expert", "insanity") or len(self.__logic.iteminfo_list) == sum(itempool.ItemPool(options, self.rnd).toDict().values()):
                    break

        if self.plan:
            for ii in self.__logic.iteminfo_list:
                item = self.plan.forced_items.get(ii.nameId.upper(), None)
                if isinstance(item, list):
                    ii.OPTIONS = item
                else:
                    ii.forced_item = item

        if options.dungeon_items in ('standard', 'localkeys') or options.forwardfactor:
            item_placer = ForwardItemPlacer(self.__logic, options.forwardfactor, options.accessibility_rule)
        else:
            item_placer = RandomItemPlacer(self.__logic, options.accessibility_rule)
        for item, count in self.readItemPool(options, item_placer).items():
            if count > 0:
                item_placer.addItem(item, count)
        item_placer.run(self.rnd)

        if options.multiworld:
            z = None
            if options.output_filename is not None:
                z = zipfile.ZipFile(options.output_filename, "w")
                z.write(os.path.join(os.path.dirname(__file__), "multiworld/bizhawkConnector.lua"), "bizhawkConnector.lua")
                z.write(os.path.join(os.path.dirname(__file__), "multiworld/socket.dll"), "socket.dll")
            roms = []
            for n in range(options.multiworld):
                rom = generator.generateRom(options.multiworld_options[n], self.seed, self.__logic, rnd=self.rnd, multiworld=n)
                fname = "LADXR_Multiworld_%d_%d.gbc" % (options.multiworld, n + 1)
                if z:
                    handle = z.open(fname, "w")
                    rom.save(handle, name="LADXR")
                    handle.close()
                else:
                    rom.save(fname, name="LADXR")
                roms.append(rom)
            if (options.spoilerformat != "none" or options.log_directory) and not options.race:
                log = spoilerLog.SpoilerLog(options, roms)
                if options.log_directory:
                    filename = "LADXR_Multiworld_%d_%s_%s.json" % (options.multiworld, datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), log.seed)
                    log_path = os.path.join(options.log_directory, filename)
                    log.outputJson(log_path)
                if options.spoilerformat != "none":
                    extension = "json" if options.spoilerformat == "json" else "txt"
                    sfname = "LADXR_Multiworld_%d.%s" % (options.multiworld, extension)
                    log.output(sfname, z)
        else:
            rom = generator.generateRom(options, self.seed, self.__logic, rnd=self.rnd)
            filename = options.output_filename
            if filename is None:
                filename = "LADXR_%s.gbc" % (binascii.hexlify(self.seed).decode("ascii").upper())
            rom.save(filename, name="LADXR")

            if (options.spoilerformat != "none" or options.log_directory) and not options.race:
                log = spoilerLog.SpoilerLog(options, [rom])
                if options.log_directory:
                    filename = "LADXR_%s_%s.json" % (datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), log.seed)
                    log_path = os.path.join(options.log_directory, filename)
                    log.outputJson(log_path)
                if options.spoilerformat != "none":
                    log.output(options.spoiler_filename)

    def readItemPool(self, options, item_placer):
        item_pool = {}
        # Collect the item pool from the rom to see which items we can randomize.
        if options.multiworld is None:
            item_pool = itempool.ItemPool(options, self.rnd).toDict()
        else:
            for world in range(options.multiworld):
                world_item_pool = itempool.ItemPool(options.multiworld_options[world], self.rnd).toDict()
                for item, count in world_item_pool.items():
                    item_pool["%s_W%d" % (item, world)] = count

        for spot in self.__logic.iteminfo_list:
            if spot.forced_item is not None:
                item_pool[spot.forced_item] = item_pool.get(spot.forced_item, 0) - 1
                spot.item = spot.forced_item
            elif len(spot.getOptions()) == 1:
                # If a spot has no other placement options, just ignore this spot.
                item_pool[spot.getOptions()[0]] -= 1
                spot.item = spot.getOptions()[0]
            else:
                item_placer.addSpot(spot)
                spot.item = None

        if self.plan:
            for item, count in self.plan.item_pool.items():
                item_pool[item] = item_pool.get(item, 0) + count

        # The plandomizer might cause an item pool item to go negative, and we need to correct for that.
        need_to_remove = 0
        for item, count in item_pool.items():
            if count < 0:
                need_to_remove -= count
        for item in (RUPEES_50, RUPEES_20, RUPEES_200, MESSAGE, MEDICINE, GEL, SEASHELL):
            remove = min(need_to_remove, item_pool.get(item, 0))
            if remove:
                item_pool[item] -= remove
                need_to_remove -= remove
        return item_pool


class ItemPlacer:
    def __init__(self, logic, accessibility_rule):
        self._logic = logic
        self._item_pool = {}
        self._spots = []
        self._accessibility_rule = accessibility_rule

    def addItem(self, item, count=1):
        self._item_pool[item] = self._item_pool.get(item, 0) + count

    def removeItem(self, item):
        self._item_pool[item] -= 1
        if self._item_pool[item] == 0:
            del self._item_pool[item]

    def addSpot(self, spot):
        self._spots.append(spot)

    def removeSpot(self, spot):
        self._spots.remove(spot)

    def run(self, rnd):
        raise NotImplementedError()

    def hasNewPlacesToExplore(self):
        e = explorer.Explorer()
        e.visit(self._logic.start)
        for loc in e.getAccessableLocations():
            for spot in loc.items:
                if spot.item is None:
                    return True
        return False

    def canStillPlaceItemPool(self):
        item_pool = self._item_pool.copy()
        spots = self._spots.copy()
        def scoreSpot(s):
            if s.location.dungeon:
                return 0, s.nameId
            return len(s.getOptions()), s.nameId
        item_spot_count = {}
        spots.sort(key=scoreSpot)
        for spot in spots:
            for option in spot.getOptions():
                item_spot_count[option] = item_spot_count.get(option, 0) + 1
        for spot in spots:
            done = False
            for option in sorted(spot.getOptions(), key=lambda opt: (item_spot_count[opt], opt)):
                if option in item_pool:
                    item_pool[option] -= 1
                    if item_pool[option] == 0:
                        del item_pool[option]
                    done = True
                    break
            if not done:
                return False
        return True


class RandomItemPlacer(ItemPlacer):
    def run(self, rnd):
        assert sum(self._item_pool.values()) == len(self._spots), "%d != %d" % (sum(self._item_pool.values()), len(self._spots))
        assert self.logicStillValid(), "Sanity check failed: %s" % (self.logicStillValid(verbose=True))

        bail_counter = 0
        while self._item_pool:
            assert sum(self._item_pool.values()) == len(self._spots)
            if not self.__placeItem(rnd):
                bail_counter += 1
                if bail_counter > 10:
                    raise Error("Failed to place an item for a bunch of retries")
            else:
                bail_counter = 0

    def __placeItem(self, rnd):
        # Random placement
        spot = rnd.choice(self._spots)
        options = [i for i in spot.getOptions() if i in self._item_pool]

        if not options:
            return False
        item = rnd.choice(options)

        spot.item = item
        self.removeItem(item)
        self.removeSpot(spot)

        if not self.logicStillValid():
            spot.item = None
            self.addItem(item)
            self.addSpot(spot)
            #print("Failed to place:", item)
            return False
        #print("Placed:", item)
        return True

    def logicStillValid(self, verbose=False):
        # Check if we still have new places to explore
        if self._spots:
            if not self.hasNewPlacesToExplore():
                if verbose:
                    print("Can no longer find new locations to explore")
                return False

        # Check if we can still place all our items
        if not self.canStillPlaceItemPool():
            if verbose:
                print("Can no longer place our item pool")
            return False

        # Finally, check if the logic still makes everything accessible when we have all the items.
        e = explorer.Explorer()
        for item_pool_item, count in self._item_pool.items():
            e.addItem(item_pool_item, count)
        e.visit(self._logic.start)

        if self._accessibility_rule == "goal":
            return self._logic.windfish in e.getAccessableLocations()
        else:
            if len(e.getAccessableLocations()) != len(self._logic.location_list):
                if verbose:
                    for loc in self._logic.location_list:
                        if loc not in e.getAccessableLocations():
                            print("Cannot access: ", loc.items)
                    print("Not all locations are accessible anymore with the full item pool")
                return False
        return True


class ForwardItemPlacer(ItemPlacer):
    DUNGEON_ITEMS = [
        COMPASS1, COMPASS2, COMPASS3, COMPASS4, COMPASS5, COMPASS6, COMPASS7, COMPASS8, COMPASS9,
        MAP1, MAP2, MAP3, MAP4, MAP5, MAP6, MAP7, MAP8, MAP9,
        STONE_BEAK1, STONE_BEAK2, STONE_BEAK3, STONE_BEAK4, STONE_BEAK5, STONE_BEAK6, STONE_BEAK7, STONE_BEAK8, STONE_BEAK9
    ]

    def __init__(self, logic, forwardfactor, accessibility_rule):
        super().__init__(logic, accessibility_rule)
        for ii in logic.iteminfo_list:
            ii.weight = 1.0
        self.__forwardfactor = forwardfactor if forwardfactor else 0.5

    def run(self, rnd):
        assert self.canStillPlaceItemPool(), "Sanity check failed %s" % (self.canStillPlaceItemPool())
        if sum(self._item_pool.values()) != len(self._spots):
            for k, v in sorted(self._item_pool.items()):
                print(k, v)
        assert sum(self._item_pool.values()) == len(self._spots), "%d != %d" % (sum(self._item_pool.values()), len(self._spots))
        bail_counter = 0
        while self._item_pool:
            if not self.__placeItem(rnd):
                bail_counter += 1
                if bail_counter > 100:
                    raise Error("Failed to place an item for a bunch of retries")
            else:
                bail_counter = 0

    def __placeItem(self, rnd):
        e = explorer.Explorer()
        e.visit(self._logic.start)
        if self._accessibility_rule == "goal" and self._logic.windfish in e.getAccessableLocations():
            spots = self._spots
            req_items = []
        else:
            spots = [spot for loc in e.getAccessableLocations() for spot in loc.items if spot.item is None]
            req_items = [item for item in sorted(e.getRequiredItemsForNextLocations()) if item in self._item_pool]
        if not req_items:
            for di in self.DUNGEON_ITEMS:
                if di in self._item_pool:
                    req_items = [item for item in self.DUNGEON_ITEMS if item in self._item_pool]
                    break
        if req_items:
            if "RUPEES" in req_items:
                req_items += [RUPEES_20, RUPEES_50, RUPEES_100, RUPEES_200, RUPEES_500]
        else:
            req_items = [item for item in sorted(self._item_pool.keys())]

        item = rnd.choice(req_items)
        spots = list(sorted([spot for spot in spots if item in spot.getOptions()], key=lambda spot: spot.nameId))
        if not spots:
            return False
        spot = rnd.choices(spots, [spot.weight for spot in spots])[0]

        spot.item = item
        if self._accessibility_rule != "goal" or self._logic.windfish not in e.getAccessableLocations():
            if e.getRequiredItemsForNextLocations() and not self.hasNewPlacesToExplore():
                spot.item = None
                return False
        self.removeItem(spot.item)
        self.removeSpot(spot)
        if not self.canStillPlaceItemPool():
            self.addItem(spot.item)
            self.addSpot(spot)
            spot.item = None
            return False
        # For each item placed, make all accessible locations less likely to be picked
        for spot in spots:
            spot.weight *= self.__forwardfactor
        return True
