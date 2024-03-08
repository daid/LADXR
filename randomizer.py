import argparse
import random
import zipfile
import os
import binascii
from datetime import datetime
from typing import Optional, List, Dict, Tuple

import explorer
import locations.itemInfo
import logic
from locations.items import *
import generator
import spoilerLog
import itempool
import mapgen
from plan import Plan
from worldSetup import WorldSetup
from settings import Settings


class Error(Exception):
    pass


class Randomizer:
    def __init__(self, args: argparse.Namespace, settings: Settings, *, seed: Optional[bytes] = None) -> None:
        self.seed = seed
        self.plan = None
        if self.seed is None:
            self.seed = os.urandom(16)
        self.rnd = random.Random(self.seed)
        if settings.race:
            self.rnd.random()  # Just pull 1 random number so race seeds are different then from normal seeds but still stable.
        if args.plan:
            assert settings.multiworld is None
            self.plan = Plan(args.plan)

        if settings.multiworld:
            self.__logic = logic.MultiworldLogic(settings, self.rnd)
        else:
            for n in range(1000):  # Try the world setup in case entrance randomization generates unsolvable logic
                world_setup = WorldSetup()
                world_setup.randomize(settings, self.rnd)
                if settings.overworld == "random":
                    world_setup.map = mapgen.generate(args.input_filename, 8, 8)
                    if world_setup.map is None:
                        continue
                random.setstate(self.rnd.getstate())
                self.__logic = logic.Logic(settings, world_setup=world_setup)
                if settings.entranceshuffle not in ("split", "mixed", "wild", "chaos", "insane", "madness") or len(self.__logic.iteminfo_list) == sum(itempool.ItemPool(self.__logic, settings, self.rnd, self.plan != None).toDict().values()):
                    break

        if self.plan:
            for ii in self.__logic.iteminfo_list:
                item = self.plan.forced_items.get(ii.nameId.upper(), None)
                if isinstance(item, list):
                    ii.OPTIONS = item
                elif item is not None:
                    ii.forced_item = item

        if settings.multiworld:
            item_placer = MultiworldItemPlacer(self.__logic, settings.forwardfactor if settings.forwardfactor > 0.0 else 0.5, settings.accessibility, settings.multiworld)
        elif settings.forwardfactor > 0.0 or settings.overworld in {'dungeonchain'}:
            item_placer = ForwardItemPlacer(self.__logic, settings.forwardfactor, settings.accessibility)
        else:
            item_placer = RandomItemPlacer(self.__logic, settings.dungeon_items, settings.owlstatues, settings.accessibility)
        for item, count in self.readItemPool(settings, item_placer).items():
            if count > 0:
                item_placer.addItem(item, count)
        item_placer.run(self.rnd)

        if settings.multiworld:
            z = None
            if args.output_filename is not None:
                z = zipfile.ZipFile(args.output_filename, "w")
                z.write(os.path.join(os.path.dirname(__file__), "multiworld/bizhawkConnector.lua"), "bizhawkConnector.lua")
                z.write(os.path.join(os.path.dirname(__file__), "multiworld/socket.dll"), "socket.dll")
            roms = []
            for n in range(settings.multiworld):
                rom = generator.generateRom(args, settings.multiworld_settings[n], self.seed, self.__logic, rnd=self.rnd, multiworld=n)
                fname = "LADXR_Multiworld_%d_%d.gbc" % (settings.multiworld, n + 1)
                if z:
                    handle = z.open(fname, "w")
                    rom.save(handle, name="LADXR")
                    handle.close()
                else:
                    rom.save(fname, name="LADXR")
                roms.append(rom)
            if (args.spoilerformat != "none" or args.log_directory) and not settings.race:
                log = spoilerLog.SpoilerLog(settings, args, roms)
                if args.log_directory:
                    filename = "LADXR_Multiworld_%d_%s_%s.json" % (settings.multiworld, datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), log.seed)
                    log_path = os.path.join(args.log_directory, filename)
                    log.outputJson(log_path)
                if args.spoilerformat != "none":
                    extension = "json" if args.spoilerformat == "json" else "txt"
                    sfname = "LADXR_Multiworld_%d.%s" % (settings.multiworld, extension)
                    log.output(sfname, z)
        else:
            rom = generator.generateRom(args, settings, self.seed, self.__logic, rnd=self.rnd)
            filename = args.output_filename
            if filename is None:
                filename = "LADXR_%s.gbc" % (binascii.hexlify(self.seed).decode("ascii").upper())
            rom.save(filename, name="LADXR")

            if (args.spoilerformat != "none" or args.log_directory) and not settings.race:
                log = spoilerLog.SpoilerLog(settings, args, [rom])
                if args.log_directory:
                    filename = "LADXR_%s_%s.json" % (datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), log.seed)
                    log_path = os.path.join(args.log_directory, filename)
                    log.outputJson(log_path)
                if args.spoilerformat != "none":
                    log.output(args.spoiler_filename)

    def readItemPool(self, settings: Settings, item_placer: "ItemPlacer") -> Dict[str, int]:
        item_pool = {}
        # Build the item pool to see which items we can randomize.
        if settings.multiworld is None:
            item_pool = itempool.ItemPool(self.__logic, settings, self.rnd, self.plan != None).toDict()
        else:
            for world in range(settings.multiworld):
                world_item_pool = itempool.ItemPool(self.__logic.worlds[world], settings.multiworld_settings[world], self.rnd, self.plan != None).toDict()
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
    def __init__(self, logic: logic.Logic, accessibility: str) -> None:
        self._logic = logic
        self._item_pool: Dict[str, int] = {}
        self._spots: List[locations.itemInfo.ItemInfo] = []
        self._accessibility: str = accessibility

    def addItem(self, item: str, count: int = 1) -> None:
        self._item_pool[item] = self._item_pool.get(item, 0) + count

    def removeItem(self, item: str) -> None:
        self._item_pool[item] -= 1
        if self._item_pool[item] == 0:
            del self._item_pool[item]

    def getItemListWithMultiplicity(self) -> List[str]:
        item_list = []
        for item, count in self._item_pool.items():
            item_list += [item for _ in range(count)]
        return item_list

    def addSpot(self, spot: locations.itemInfo.ItemInfo) -> None:
        self._spots.append(spot)

    def removeSpot(self, spot: locations.itemInfo.ItemInfo) -> None:
        self._spots.remove(spot)

    def run(self, rnd: random.Random) -> None:
        raise NotImplementedError()

    def hasNewPlacesToExplore(self) -> bool:
        e = explorer.Explorer()
        e.visit(self._logic.start)
        for loc in e.getAccessableLocations():
            for spot in loc.items:
                if spot.item is None:
                    return True
        return False

    def canStillPlaceItemPool(self) -> bool:
        item_pool = self._item_pool.copy()
        spots = self._spots.copy()
        def scoreSpot(s: locations.itemInfo.ItemInfo) -> Tuple[int, str]:
            if s.location.dungeon is not None:
                return 0, s.nameId
            return len(s.getOptions()), s.nameId
        spots.sort(key=scoreSpot)

        item_spot_count: Dict[str, int] = {}
        for spot in spots:
            for option in spot.getOptions():
                item_spot_count[option] = item_spot_count.get(option, 0) + 1

        item_priority_order = [item for item in item_pool.keys()]
        item_priority_order.sort(key=lambda item: item_spot_count.get(item, 0))

        for spot in spots:
            options = set(spot.getOptions())
            done = False
            for item in item_priority_order:
                if item in options:
                    item_pool[item] -= 1
                    if item_pool[item] == 0:
                        del item_pool[item]
                        item_priority_order.remove(item)
                        # Check if we can stop because all remaining items can be placed everywhere. (performance optimization)
                        if item_priority_order and item_spot_count.get(item_priority_order[0], 0) == len(spots):
                            return True
                    done = True
                    break
            if not done:
                return False
        return True


class RandomItemPlacer(ItemPlacer):
    def __init__(self, logic: logic.Logic, dungeon_item_setting: str, owl_statue_setting: str, accessibility: str) -> None:
        super().__init__(logic, accessibility)
        self.dungeon_item_setting = dungeon_item_setting
        self.owl_statue_setting = owl_statue_setting

    def run(self, rnd: random.Random) -> None:
        assert sum(self._item_pool.values()) == len(self._spots), "%d != %d" % (sum(self._item_pool.values()), len(self._spots))
        assert self.logicStillValid(), "Sanity check failed: %s" % (self.logicStillValid(verbose=True))

        # Place keys that are restricted to their dungeon first to avoid running out of valid spots
        dungeon_keys = []
        if self.owl_statue_setting in {'both', 'dungeon'} and self.dungeon_item_setting in {'', 'keysy', 'smallkeys', 'nightmarekeys'}:
            dungeon_keys += [item for item in self.getItemListWithMultiplicity() if item.startswith("STONE_BEAK")]
        if self.dungeon_item_setting in {'', 'localkeys', 'nightmarekeys'}:
            dungeon_keys += [item for item in self.getItemListWithMultiplicity() if item.startswith("KEY")]
        if self.dungeon_item_setting in {'', 'localkeys', 'localnightmarekey', 'smallkeys'}:
            dungeon_keys += [item for item in self.getItemListWithMultiplicity() if item.startswith("NIGHTMARE_KEY")]
        rnd.shuffle(dungeon_keys)

        bail_counter = 0
        while self._item_pool:
            assert sum(self._item_pool.values()) == len(self._spots)
            if dungeon_keys:
                success = self.placeSpecificItem(dungeon_keys[0], rnd)
                if success:
                    dungeon_keys.pop(0)
            else:
                success = self.__placeItem(rnd)
            if not success:
                bail_counter += 1
                if bail_counter > 10:
                    raise Error("Failed to place an item for a bunch of retries")
            else:
                bail_counter = 0

    def __placeItem(self, rnd: random.Random) -> bool:
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

    def placeSpecificItem(self, item: str, rnd: random.Random) -> bool:
        # Random placement of a given item
        spot_options = [spot for spot in self._spots if item in spot.getOptions()]
        spot = rnd.choice(spot_options)

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

    def logicStillValid(self, verbose: bool = False) -> bool:
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

        if self._accessibility == "goal":
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
        COMPASS1, COMPASS2, COMPASS3, COMPASS4, COMPASS5, COMPASS6, COMPASS7, COMPASS8, COMPASS0,
        MAP1, MAP2, MAP3, MAP4, MAP5, MAP6, MAP7, MAP8, MAP0,
        STONE_BEAK1, STONE_BEAK2, STONE_BEAK3, STONE_BEAK4, STONE_BEAK5, STONE_BEAK6, STONE_BEAK7, STONE_BEAK8, STONE_BEAK0
    ]

    def __init__(self, logic: logic.Logic, forwardfactor: float, accessibility: str, *, verbose: bool = False) -> None:
        super().__init__(logic, accessibility)
        for ii in logic.iteminfo_list:
            ii.weight = 1.0
        self.__forwardfactor = forwardfactor if forwardfactor > 0.0 else 0.5
        self.__start_spots_filled = False
        self.__verbose = verbose

    def run(self, rnd: random.Random) -> None:
        assert self.canStillPlaceItemPool(), "Sanity check failed %s" % (self.canStillPlaceItemPool())
        if sum(self._item_pool.values()) != len(self._spots):
            for k, v in sorted(self._item_pool.items()):
                print(k, v)
        assert sum(self._item_pool.values()) == len(self._spots), "%d != %d" % (sum(self._item_pool.values()), len(self._spots))
        bail_counter = 0
        while self._item_pool:
            if not self._placeItem(rnd):
                bail_counter += 1
                if bail_counter > 30:
                    raise Error("Failed to place an item for a bunch of retries")
            else:
                bail_counter = 0

    def _placeItem(self, rnd: random.Random) -> bool:
        e = explorer.Explorer()
        e.visit(self._logic.start)
        if self._accessibility == "goal" and self._logic.windfish in e.getAccessableLocations():
            spots = self._spots
            req_items = []
        else:
            if not self.__start_spots_filled:
                spots = [spot for spot in self._spots if "StartItem" in str(spot)]
                if not spots:
                    self.__start_spots_filled = True
            else:
                spots = [spot for loc in e.getAccessableLocations() for spot in loc.items if spot.item is None]
            req_items = [item for item in e.getRequiredItemsForNextLocations() if item in self._item_pool or item == "RUPEES"]
            req_items.sort()
        if not req_items:
            for di in self.DUNGEON_ITEMS:
                if di in self._item_pool:
                    req_items = [item for item in self.DUNGEON_ITEMS if item in self._item_pool]
                    break
        if req_items:
            if "RUPEES" in req_items:
                req_items.remove("RUPEES")
                for rup in [RUPEES_20, RUPEES_50, RUPEES_100, RUPEES_200, RUPEES_500]:
                    if rup in self._item_pool:
                        req_items.append(rup)
        if not req_items:
            req_items = [item for item in sorted(self._item_pool.keys())]

        if self.__verbose:
            print("Locations left: %d Considering now %d for %d items" % (len(self._spots), len(spots), len(req_items)))
        item = self._chooseItem(rnd, req_items)
        spots = [spot for spot in spots if item in spot.getOptions()]
        spots.sort(key=lambda spot: spot.nameId)
        if not spots:
            return False
        spot = rnd.choices(spots, [spot.weight for spot in spots])[0]

        spot.item = item
        if self._accessibility != "goal" or self._logic.windfish not in e.getAccessableLocations():
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
            if spot.weight > 0.001:
                spot.weight *= self.__forwardfactor
        return True

    def _chooseItem(self, rnd: random.Random, req_items: List[str]) -> str:
        return rnd.choice(req_items)


class MultiworldItemPlacer(ForwardItemPlacer):
    def __init__(self, logic: logic.Logic, forwardfactor: float, accessibility: str, world_count: int) -> None:
        super().__init__(logic, forwardfactor, accessibility, verbose=True)
        self.__world_count = world_count
        self.__initial_spot_count = 0
        self.DUNGEON_ITEMS = ["%s_W%d" % (item, w) for item in self.DUNGEON_ITEMS for w in range(world_count)]

    def run(self, rnd: random.Random) -> None:
        self.__initial_spot_count = len(self._spots)
        super().run(rnd)

    def _placeItem(self, rnd: random.Random) -> bool:
        result = super()._placeItem(rnd)
        if result:
            return True
        if len(self._spots) < self.__initial_spot_count / 10:
            # At this point we assume the failure is because we can no longer place items across worlds.
            # And that the items are not really important, so cheat, and change which players the items belong to.
            spot_options = set()
            for spot in self._spots:
                for item in spot.getOptions():
                    spot_options.add(item)
            new_item_pool = {}
            for item, amount in self._item_pool.items():
                if item.startswith(BAD_HEART_CONTAINER):
                    item = RUPEES_50 + item[item.rfind("_"):]
                for n in range(self.__world_count):
                    new_item = "%s%d" % (item[:-1], n)
                    if new_item in spot_options:
                        new_item_pool[new_item] = amount
            print("Deploying cheat: %s -> %s" % (self._item_pool, new_item_pool))
            self._item_pool = new_item_pool
        return False

    # def canStillPlaceItemPool(self) -> bool:
    #     return True

    def _chooseItem(self, rnd: random.Random, req_items: List[str]) -> str:
        per_world: Dict[int, int] = {}
        worlds = []
        for item in req_items:
            world = int(item[item.rfind("_W")+2:])
            per_world[world] = per_world.get(world, 0) + 1
            worlds.append(world)
        if len(per_world) == 1:
            return rnd.choice(req_items)

        total = len(req_items)
        weights = []
        for item, world in zip(req_items, worlds):
            weights.append(total / per_world[world])
        return rnd.choices(req_items, weights)[0]
