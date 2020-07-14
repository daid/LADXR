import random
import zipfile
import os
import binascii

import explorer
import logic
from locations.items import *
import generator
import itempool


class Error(Exception):
    pass


class Randomizer:
    def __init__(self, options, *, seed=None):
        self.seed = seed
        if self.seed is None:
            self.seed = os.urandom(16)
        self.rnd = random.Random(self.seed)
        if options.race:
            self.rnd.random()  # Just pull 1 random number so race seeds are different then from normal seeds but still stable.
        if options.multiworld:
            self.__logic = logic.MultiworldLogic(options, self.rnd)
        else:
            self.__logic = logic.Logic(options, self.rnd)

        if not options.keysanity or options.forwardfactor:
            item_placer = ForwardItemPlacer(self.__logic, options.forwardfactor)
        else:
            item_placer = RandomItemPlacer(self.__logic)

        if options.plan:
            assert options.multiworld is None
            self.readPlan(options.plan)

        for item, count in self.readItemPool(options, item_placer).items():
            if count > 0:
                item_placer.addItem(item, count)
        item_placer.run(self.rnd)

        if options.goal == "random":
            options.goal = self.rnd.randint(-1, 8)

        if options.multiworld:
            z = None
            if options.output_filename is not None:
                z = zipfile.ZipFile(options.output_filename, "w")
            for n in range(options.multiworld):
                rom = generator.generateRom(options.multiworld_options[n], self.seed, self.__logic, multiworld=n)
                fname = "LADXR_Multiworld_%d_%d.gbc" % (options.multiworld, n + 1)
                if z:
                    rom.save(z.open(fname, "w"), name="LADXR")
                else:
                    rom.save(fname, name="LADXR")
        else:
            rom = generator.generateRom(options, self.seed, self.__logic)
            filename = options.output_filename
            if filename is None:
                filename = "LADXR_%s.gbc" % (binascii.hexlify(self.seed).decode("ascii").upper())
            rom.save(filename, name="LADXR")

    def readPlan(self, filename):
        for line in open(filename, "rt"):
            line = line.strip()
            if ";" in line:
                line = line[:line.find(";")]
            if "#" in line:
                line = line[:line.find("#")]
            if ":" not in line:
                continue
            location, item = map(str.strip, line.upper().split(":", 1))
            if item == "":
                continue
            found = False
            for ii in self.__logic.iteminfo_list:
                if ii.nameId.upper() == location:
                    ii.forced_item = item.upper()
                    found = True
            if not found:
                print("Plandomizer warning, spot not found:", location, item)

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

        # The plandomizer might cause an item pool item to go negative, and we need to correct for that.
        need_to_remove = 0
        for item, count in item_pool.items():
            if count < 0:
                need_to_remove -= count
        if need_to_remove > 0:
            item_pool[RUPEES_50] -= need_to_remove
        return item_pool


class ItemPlacer:
    def __init__(self):
        pass

    def addItem(self, item, count=1):
        raise NotImplementedError()

    def removeItem(self, item):
        raise NotImplementedError()

    def addSpot(self, spot):
        raise NotImplementedError()

    def removeSpot(self, spot):
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()


class RandomItemPlacer:
    def __init__(self, logic):
        self.__logic = logic
        self.__item_pool = {}
        self.__spots = []

    def addItem(self, item, count=1):
        self.__item_pool[item] = self.__item_pool.get(item, 0) + count

    def removeItem(self, item):
        self.__item_pool[item] -= 1
        if self.__item_pool[item] == 0:
            del self.__item_pool[item]

    def addSpot(self, spot):
        while len(self.__spots) <= spot.priority:
            self.__spots.append([])
        self.__spots[spot.priority].append(spot)

    def removeSpot(self, spot):
        self.__spots[spot.priority].remove(spot)
        while len(self.__spots) > 0 and len(self.__spots[-1]) == 0:
            self.__spots.pop()

    def run(self, rnd):
        assert sum(self.__item_pool.values()) == sum([len(spots) for spots in self.__spots]), "%d != %d" % (sum(self.__item_pool.values()), sum([len(spots) for spots in self.__spots]))
        assert self.logicStillValid(), "Sanity check failed: %s" % (self.logicStillValid(verbose=True))

        bail_counter = 0
        while self.__item_pool:
            assert sum(self.__item_pool.values()) == sum(map(lambda n: len(n), self.__spots))
            if not self.__placeItem(rnd):
                bail_counter += 1
                if bail_counter > 10:
                    raise Error("Failed to place an item for a bunch of retries")
            else:
                bail_counter = 0

    def __placeItem(self, rnd):
        # Random placement
        spot = rnd.choice(self.__spots[-1])
        options = list(filter(lambda i: i in self.__item_pool, spot.getOptions()))

        if not options:
            return False
        item = rnd.choice(sorted(options))

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
        if self.__spots:
            e = explorer.Explorer()
            e.visit(self.__logic.start)
            valid = False
            for loc in e.getAccessableLocations():
                for ii in loc.items:
                    for spots in self.__spots:
                        if ii in spots:
                            valid = True
            if not valid:
                if verbose:
                    print("Can no longer find new locations to explore")
                return False

        # Check if we can still place all our items
        if not self.canStillPlaceItemPool(verbose):
            if verbose:
                print("Can no longer place our item pool")
            return False

        # Finally, check if the logic still makes everything accessible when we have all the items.
        e = explorer.Explorer()
        for item_pool_item, count in self.__item_pool.items():
            e.addItem(item_pool_item, count)
        e.visit(self.__logic.start)

        if len(e.getAccessableLocations()) != len(self.__logic.location_list):
            if verbose:
                for loc in self.__logic.location_list:
                    if loc not in e.getAccessableLocations():
                        print("Cannot access: ", loc.items)
                print("Not all locations are accessible anymore with the full item pool")
            return False
        return True

    def canStillPlaceItemPool(self, verbose=False):
        # For each item in the pool, find which spots are available.
        # Then, from the hardest to place item to the easy stuff strip the availability pool
        item_spots = {}
        for spots in self.__spots:
            for spot in spots:
                for option in spot.getOptions():
                    if option not in item_spots:
                        item_spots[option] = set()
                    item_spots[option].add(spot)
        for item in sorted(self.__item_pool.keys(), key=lambda item: len(item_spots.get(item, set()))):
            spots = item_spots.get(item, set())
            for n in range(self.__item_pool.get(item, 0)):
                if verbose:
                    print(n, item, spots)
                if not spots:
                    if verbose:
                        print(item_spots)
                    return False
                spot = next(iter(spots))
                for spot_set in item_spots.values():
                    if spot in spot_set:
                        spot_set.remove(spot)
        return True


class ForwardItemPlacer:
    DUNGEON_ITEMS = [
        COMPASS1, COMPASS2, COMPASS3, COMPASS4, COMPASS5, COMPASS6, COMPASS7, COMPASS8, COMPASS9,
        MAP1, MAP2, MAP3, MAP4, MAP5, MAP6, MAP7, MAP8, MAP9,
        STONE_BEAK1, STONE_BEAK2, STONE_BEAK3, STONE_BEAK4, STONE_BEAK5, STONE_BEAK6, STONE_BEAK7, STONE_BEAK8, STONE_BEAK9
    ]

    def __init__(self, logic, forwardfactor):
        self.__logic = logic
        self.__item_pool = {}
        self.__spots = []
        for ii in logic.iteminfo_list:
            ii.weight = 1.0
        self.__forwardfactor = forwardfactor if forwardfactor else 0.5

    def addItem(self, item, count=1):
        self.__item_pool[item] = self.__item_pool.get(item, 0) + count

    def removeItem(self, item):
        self.__item_pool[item] -= 1
        if self.__item_pool[item] == 0:
            del self.__item_pool[item]

    def addSpot(self, spot):
        self.__spots.append(spot)

    def removeSpot(self, spot):
        self.__spots.remove(spot)

    def run(self, rnd):
        if sum(self.__item_pool.values()) != len(self.__spots):
            for k, v in sorted(self.__item_pool.items()):
                print(k, v)
        assert sum(self.__item_pool.values()) == len(self.__spots), "%d != %d" % (sum(self.__item_pool.values()), len(self.__spots))
        bail_counter = 0
        while self.__item_pool:
            if not self.__placeItem(rnd):
                bail_counter += 1
                if bail_counter > 100:
                    raise Error("Failed to place an item for a bunch of retries")
            else:
                bail_counter = 0

    def __placeItem(self, rnd):
        e = explorer.Explorer()
        e.visit(self.__logic.start)
        spots = [spot for loc in e.getAccessableLocations() for spot in loc.items if spot.item is None]
        req_items = [item for item in sorted(e.getRequiredItemsForNextLocations()) if item in self.__item_pool]
        if not req_items:
            for di in self.DUNGEON_ITEMS:
                if di in self.__item_pool:
                    req_items = [item for item in self.DUNGEON_ITEMS if item in self.__item_pool]
                    break
        if req_items:
            if "RUPEES" in req_items:
                req_items += [RUPEES_20, RUPEES_50, RUPEES_100, RUPEES_200, RUPEES_500]
        else:
            req_items = [item for item in sorted(self.__item_pool.keys())]

        item = rnd.choice(req_items)
        spots = [spot for spot in spots if item in spot.getOptions()]
        if not spots:
            return False
        spot = rnd.choices(spots, [spot.weight for spot in spots])[0]

        spot.item = item
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

    def hasNewPlacesToExplore(self):
        e = explorer.Explorer()
        e.visit(self.__logic.start)
        for loc in e.getAccessableLocations():
            for spot in loc.items:
                if spot.item is None:
                    return True
        return False

    def canStillPlaceItemPool(self, verbose=False):
        # For each item in the pool, find which spots are available.
        # Then, from the hardest to place item to the easy stuff strip the availability pool
        item_spots = {}
        for spot in self.__spots:
            for option in spot.getOptions():
                if option not in item_spots:
                    item_spots[option] = set()
                item_spots[option].add(spot)
        for item in sorted(self.__item_pool.keys(), key=lambda item: len(item_spots.get(item, set()))):
            spots = item_spots.get(item, set())
            for n in range(self.__item_pool.get(item, 0)):
                if verbose:
                    print(n, item, spots)
                if not spots:
                    if verbose:
                        print(item_spots)
                    return False
                spot = next(iter(spots))
                for spot_set in item_spots.values():
                    if spot in spot_set:
                        spot_set.remove(spot)
        return True
