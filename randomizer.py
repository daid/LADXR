import location
import explorer
import locations
import random


class Error(Exception):
    pass


class Randomizer:
    def __init__(self, rom):
        self.rnd = random.Random()
        self.item_pool = {}
        self.spots = []

        self.readItemPool(rom)

        bail_counter = 0
        while self.item_pool:
            if not self.placeItem():
                bail_counter += 1
                if bail_counter > 50:
                    raise Error("Failed to place an item for a 100 retries")
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
        item_spots = {}
        for spot in location.ItemInfo.all:
            item = spot.read(rom)
            # If a spot has no other placement options, just ignore this spot.
            #  We still marked to spots so we can later patch them to allow more options.
            if len(spot.getOptions()) > 1:
                self.item_pool[item] = self.item_pool.get(item, 0) + 1
                self.addSpot(spot)
            else:
                spot.item = item

        #print("Item pool:")
        #for k, v in sorted(self.item_pool.items()):
        #    print("    ", k, v)
        #print("Spot count: %d" % (len(self.spots)))
        #print(item_spots)

    def placeItem(self):
        spot = self.rnd.choice(self.spots)

        options = list(filter(lambda i: i in self.item_pool.keys(), spot.getOptions()))
        if not options:
            raise Error("Placement failure")
        item = self.rnd.choice(sorted(options))

        spot.item = item
        self.removeItem(item)
        self.removeSpot(spot)

        e = explorer.Explorer()
        for item_pool_item, count in self.item_pool.items():
            for n in range(count):
                e.addItem(item_pool_item)
        e.visit(locations.start)

        if len(e.getAvailableLocations()) != len(location.Location.all) or not self.canStillPlaceItemPool():
            spot.item = None
            self.addItem(item)
            self.addSpot(spot)
            #print("Failed to place:", item)
            return False
        #print("Placed:", item)
        return True

    def canStillPlaceItemPool(self):
        # For each item in the pool, find which spots are available.
        # Then, from the hardest to place item to the easy stuff strip the availability pool
        item_spots = {}
        for spot in self.spots:
            for option in spot.getOptions():
                if option not in item_spots:
                    item_spots[option] = set()
                item_spots[option].add(spot)
        for item, spots in sorted(item_spots.items(), key=lambda n: len(n[1])):
            for n in range(self.item_pool.get(item, 0)):
                if not spots:
                    return False
                spot = next(iter(spots))
                for spot_set in item_spots.values():
                    if spot in spot_set:
                        spot_set.remove(spot)
        return True
