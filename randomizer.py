import explorer
import random
import os
import logic
from locations.items import *
import binascii
import generator


DEFAULT_ITEM_POOL = {
    "SWORD": 1,
    "FEATHER": 1,
    "HOOKSHOT": 1,
    "BOW": 1,
    "BOMB": 2,
    "MAGIC_POWDER": 1,
    "MAGIC_ROD": 1,
    "OCARINA": 1,
    "PEGASUS_BOOTS": 1,
    "POWER_BRACELET": 2,
    "SHIELD": 2,
    "SHOVEL": 1,

    "TOADSTOOL": 1,

    "SEASHELL": 24,

    "SLIME_KEY": 1,
    "TAIL_KEY": 1,
    "ANGLER_KEY": 1,
    "BIRD_KEY": 1,
    "FACE_KEY": 1,

    "GOLD_LEAF": 5,

    "FLIPPERS": 1,
    "BOWWOW": 1,
    "SONG1": 1,
    "SONG2": 1,
    "SONG3": 1,

    "BLUE_TUNIC": 1,
    "RED_TUNIC": 1,
    "MAX_ARROWS_UPGRADE": 1,
    "MAX_BOMBS_UPGRADE": 1,
    "MAX_POWDER_UPGRADE": 1,

    "HEART_CONTAINER": 8,
    "HEART_PIECE": 11,

    "RUPEES_100": 3,
    "RUPEES_20": 39,
    "RUPEES_200": 3,
    "RUPEES_50": 19,

    "MEDICINE": 2,
    "MESSAGE": 1,
    "GEL": 4,

    "COMPASS1": 1,
    "COMPASS2": 1,
    "COMPASS3": 1,
    "COMPASS4": 1,
    "COMPASS5": 1,
    "COMPASS6": 1,
    "COMPASS7": 1,
    "COMPASS8": 1,
    "COMPASS9": 1,
    "KEY1": 3,
    "KEY2": 5,
    "KEY3": 9,
    "KEY4": 5,
    "KEY5": 3,
    "KEY6": 3,
    "KEY7": 3,
    "KEY8": 7,
    "KEY9": 3,
    "MAP1": 1,
    "MAP2": 1,
    "MAP3": 1,
    "MAP4": 1,
    "MAP5": 1,
    "MAP6": 1,
    "MAP7": 1,
    "MAP8": 1,
    "MAP9": 1,
    "NIGHTMARE_KEY1": 1,
    "NIGHTMARE_KEY2": 1,
    "NIGHTMARE_KEY3": 1,
    "NIGHTMARE_KEY4": 1,
    "NIGHTMARE_KEY5": 1,
    "NIGHTMARE_KEY6": 1,
    "NIGHTMARE_KEY7": 1,
    "NIGHTMARE_KEY8": 1,
    "NIGHTMARE_KEY9": 1,
    "STONE_BEAK1": 1,
    "STONE_BEAK2": 1,
    "STONE_BEAK3": 1,
    "STONE_BEAK4": 1,
    "STONE_BEAK5": 1,
    "STONE_BEAK6": 1,
    "STONE_BEAK7": 1,
    "STONE_BEAK8": 1,
    "STONE_BEAK9": 1,
}


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
        self.item_pool = {}
        self.spots = []
        self.forward_placement = not options.keysanity

        self.readItemPool(options)
        self.modifyDefaultItemPool(options)
        assert self.logicStillValid(), "Sanity check failed: %s" % (self.logicStillValid(verbose=True))

        bail_counter = 0
        while self.item_pool:
            if not self.placeItem():
                bail_counter += 1
                if bail_counter > 100:
                    print(sum(self.item_pool.values()), self.item_pool)
                    print(self.spots)
                    raise Error("Failed to place an item for a bunch of retries")
            else:
                bail_counter = 0

        if options.goal == "random":
            options.goal = self.rnd.randint(-1, 8)

        if options.multiworld:
            for n in range(options.multiworld):
                rom = generator.generateRom(options, self.seed, self.__logic, multiworld=n)
                rom.save("LADXR_Multiworld_%d_%d.gbc" % (options.multiworld, n + 1), name="LADXR")
        else:
            rom = generator.generateRom(options, self.seed, self.__logic)
            filename = options.output_filename
            if filename is None:
                filename = "LADXR_%s.gbc" % (binascii.hexlify(self.seed).decode("ascii").upper())
            rom.save(filename, name="LADXR")

    def addItem(self, item, count=1):
        self.item_pool[item] = self.item_pool.get(item, 0) + count

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

    def readItemPool(self, options):
        # Collect the item pool from the rom to see which items we can randomize.
        if options.multiworld is None:
            self.item_pool = DEFAULT_ITEM_POOL.copy()
        else:
            for world in range(options.multiworld):
                for item, count in DEFAULT_ITEM_POOL.items():
                    self.addItem("%s_W%d" % (item, world), count)

        for spot in self.__logic.iteminfo_list:
            if spot.forced_item is not None:
                self.removeItem(spot.forced_item)
                spot.item = spot.forced_item
            elif len(spot.getOptions()) == 1:
                # If a spot has no other placement options, just ignore this spot.
                self.removeItem(spot.getOptions()[0])
                spot.item = spot.getOptions()[0]
            else:
                self.addSpot(spot)
                spot.item = None

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
            if "_W" in remove_item:
                new_item += remove_item[remove_item.rfind("_W"):]
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
