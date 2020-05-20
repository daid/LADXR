from locations import location
import explorer
import logic
import random
import os


class Error(Exception):
    pass


class Randomizer:
    def __init__(self, rom, *, seed=None):
        self.seed = seed
        if self.seed is None:
            self.seed = os.urandom(16)
        self.rnd = random.Random(self.seed)
        self.item_pool = {}
        self.spots = []

        self.readItemPool(rom)

        bail_counter = 0
        while self.item_pool:
            if not self.placeItem():
                bail_counter += 1
                if bail_counter > 50:
                    raise Error("Failed to place an item for a bunch of retries")
            else:
                bail_counter = 0

        for spot in location.ItemInfo.all:
            spot.patch(rom, spot.item)

    def addItem(self, item):
        self.item_pool[item] = self.item_pool.get(item, 0) + 1

    def removeItem(self, item):
        self.item_pool[item] -= 1
        if self.item_pool[item] == 0:
            del self.item_pool[item]

    def addSpot(self, spot):
        self.spots.append(spot)

    def removeSpot(self, spot):
        self.spots.remove(spot)

    def readItemPool(self, rom):
        # Collect the item pool from the rom to see which items we can randomize.
        for spot in location.ItemInfo.all:
            item = spot.read(rom)
            # If a spot has no other placement options, just ignore this spot.
            #  We still marked to spots so we can later patch them to allow more options.
            if len(spot.getOptions()) > 1:
                self.item_pool[item] = self.item_pool.get(item, 0) + 1
                self.addSpot(spot)
                spot.item = None
            else:
                spot.item = item

    def placeItem(self):
        # Find a random spot and item to place
        spot = self.rnd.choice(self.spots)
        options = list(filter(lambda i: i in self.item_pool.keys(), spot.getOptions()))

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
            e.visit(logic.start)
            valid = False
            for loc in e.getAccessableLocations():
                for ii in loc.items:
                    if ii in self.spots:
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
        e.visit(logic.start)

        if len(e.getAccessableLocations()) != len(location.Location.all):
            if verbose:
                print("Not all locations are accessible anymore with the full item pool")
            return False
        return True


    def canStillPlaceItemPool(self, verbose=False):
        # For each item in the pool, find which spots are available.
        # Then, from the hardest to place item to the easy stuff strip the availability pool
        item_spots = {}
        for spot in self.spots:
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
                    return False
                spot = next(iter(spots))
                for spot_set in item_spots.values():
                    if spot in spot_set:
                        spot_set.remove(spot)
        return True
