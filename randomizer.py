import explorer
import random
import os
import logic
import copy
import patches.dungeonEntrances
import patches.goal
from locations.items import *
import hints


class Error(Exception):
    pass


class Randomizer:
    def __init__(self, rom, options, *, seed=None):
        self.seed = seed
        if self.seed is None:
            self.seed = os.urandom(16)
        self.rnd = random.Random(self.seed)
        if options.race:
            self.rnd.random()  # Just pull 1 random number so race seeds are different then from normal seeds but still stable.
        if options.multiworld:
            assert not options.dungeonshuffle, "Cannot use dungeonshuffle in multiworld at the moment"
            self.__logic = logic.MultiworldLogic(options, self.rnd)
        else:
            self.__logic = logic.Logic(options, self.rnd)
        self.item_pool = {}
        self.spots = []
        self.forward_placement = not options.keysanity

        self.readItemPool(rom)
        self.modifyDefaultItemPool(options)
        assert self.logicStillValid(), "Sanity check failed: %s" % (self.logicStillValid(verbose=True))

        bail_counter = 0
        while self.item_pool:
            if not self.placeItem():
                bail_counter += 1
                if bail_counter > 100:
                    raise Error("Failed to place an item for a bunch of retries")
            else:
                bail_counter = 0

        # Apply patches to rom
        if options.goal == "random":
            patches.goal.setRequiredInstrumentCount(rom, self.rnd.randint(-1, 8))

        if self.__logic.entranceMapping:
            patches.dungeonEntrances.changeEntrances(rom, self.__logic.entranceMapping)
        hints.addHints(rom, self.rnd, self.__logic.iteminfo_list)
        if options.multiworld:
            for n in range(2):
                result_rom = copy.deepcopy(rom)
                for spot in self.__logic.iteminfo_list:
                    if spot.world == n:
                        spot.patch(result_rom, spot.item)
                result_rom.save("Multiworld_%d.gbc" % (n + 1))
        else:
            for spot in self.__logic.iteminfo_list:
                spot.patch(rom, spot.item)

    def addItem(self, item):
        self.item_pool[item] = self.item_pool.get(item, 0) + 1

    def removeItem(self, item):
        self.item_pool[item] -= 1
        if self.item_pool[item] == 0:
            del self.item_pool[item]

    def addSpot(self, spot):
        while len(self.spots) <= spot.priority:
            self.spots.append([])
        self.spots[spot.priority].append(spot)

    def removeSpot(self, spot):
        self.spots[spot.priority].remove(spot)
        while len(self.spots) > 0 and len(self.spots[-1]) == 0:
            self.spots.pop()

    def readItemPool(self, rom):
        # Collect the item pool from the rom to see which items we can randomize.
        for spot in self.__logic.iteminfo_list:
            item = spot.read(rom)
            self.item_pool[item] = self.item_pool.get(item, 0) + 1

        for spot in self.__logic.iteminfo_list:
            # If a spot has no other placement options, just ignore this spot.
            if len(spot.getOptions()) > 1:
                self.addSpot(spot)
                spot.item = None
            else:
                self.removeItem(spot.getOptions()[0])
                spot.item = spot.getOptions()[0]

    def modifyDefaultItemPool(self, options):
        if options.bowwow == 'always':
            # Bowwow mode takes a sword from the pool to give as bowwow. So we need to fix that.
            self.addItem(SWORD)
            self.removeItem(BOWWOW)
        if options.bowwow == 'swordless':
            # Bowwow mode takes a sword from the pool to give as bowwow.
            self.removeItem(BOWWOW)
            self.addItem(RUPEES_20)
        if options.hpmode == 'inverted':
            self.item_pool[BAD_HEART_CONTAINER] = self.item_pool[HEART_CONTAINER]
            del self.item_pool[HEART_CONTAINER]

        # Remove rupees from the item pool and replace them with other items to create more variety
        rupee_item = []
        rupee_item_count = []
        for k, v in self.item_pool.items():
            if k.startswith("RUPEES_"):
                rupee_item.append(k)
                rupee_item_count.append(v)
        rupee_chests = sum(v for k, v in self.item_pool.items() if k.startswith("RUPEES_"))
        for n in range(rupee_chests // 5):
            new_item = self._rndChoices((BOMB, SINGLE_ARROW, ARROWS_10, MAGIC_POWDER, MEDICINE), (10, 5, 10, 10, 1))
            while True:
                remove_item = self._rndChoices(rupee_item, rupee_item_count)
                if remove_item in self.item_pool:
                    break
            self.addItem(new_item)
            self.removeItem(remove_item)

    def _rndChoices(self, population, weights):
        import bisect
        import itertools
        cum_weights = list(itertools.accumulate(weights))
        return population[bisect.bisect(cum_weights, self.rnd.random() * cum_weights[-1], 0, len(cum_weights) - 1)]

    def placeItem(self):
        # Find a random spot and item to place
        if self.forward_placement:
            # Forward placement
            e = explorer.Explorer()
            e.addItem("RUPEES_2000")
            e.visit(self.__logic.start)
            spots = [spot for loc in e.getAccessableLocations() for spot in loc.items if spot.item is None]
            spot = self.rnd.choice(spots)
            options = list(filter(lambda i: i in self.item_pool, spot.getOptions()))
            req_items = e.getRequiredItemsForNextLocations()
            if req_items:
                options = list(filter(lambda i: i in req_items, options))
        else:
            # Random placement
            spot = self.rnd.choice(self.spots[-1])
            options = list(filter(lambda i: i in self.item_pool, spot.getOptions()))

        if not options:
            return False
        item = self.rnd.choice(sorted(options))

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
        if self.spots:
            e = explorer.Explorer()
            e.visit(self.__logic.start)
            valid = False
            for loc in e.getAccessableLocations():
                for ii in loc.items:
                    for spots in self.spots:
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
        for item_pool_item, count in self.item_pool.items():
            for n in range(count):
                e.addItem(item_pool_item)
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
        for spots in self.spots:
            for spot in spots:
                for option in spot.getOptions():
                    if option not in item_spots:
                        item_spots[option] = set()
                    item_spots[option].add(spot)
        for item in sorted(self.item_pool.keys(), key=lambda item: len(item_spots.get(item, set()))):
            spots = item_spots.get(item, set())
            for n in range(self.item_pool.get(item, 0)):
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
