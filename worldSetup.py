import patches.enemies
import logic
from locations.items import *
from entranceInfo import ENTRANCE_INFO
from patches import bingo
from patches import maze


class Error(Exception):
    pass


MULTI_CHEST_OPTIONS = [MAGIC_POWDER, BOMB, MEDICINE, RUPEES_50, RUPEES_20, RUPEES_100, RUPEES_200, RUPEES_500, SEASHELL, GEL, ARROWS_10, SINGLE_ARROW]
MULTI_CHEST_WEIGHTS = [20,           20,   20,       50,        50,        20,         10,         5,          5,        20,  10,        10]

# List of all the possible locations where we can place our starting house
start_locations = [
    "phone_d8",
    "rooster_house",
    "writes_phone",
    "castle_phone",
    "photo_house",
    "start_house",
    "prairie_right_phone",
    "banana_seller",
    "prairie_low_phone",
    "animal_phone",
]


class WorldSetup:
    def __init__(self):
        self.entrance_mapping = {k: k for k in ENTRANCE_INFO.keys()}
        self.boss_mapping = list(range(9))
        self.miniboss_mapping = {
            # Main minibosses
            0: "ROLLING_BONES", 1: "HINOX", 2: "DODONGO", 3: "CUE_BALL", 4: "GHOMA", 5: "SMASHER", 6: "GRIM_CREEPER", 7: "BLAINO",
            # Color dungeon needs to be special, as always.
            "c1": "AVALAUNCH", "c2": "GIANT_BUZZ_BLOB",
            # Overworld
            "moblin_cave": "MOBLIN_KING",
            "armos_temple": "ARMOS_KNIGHT",
        }
        self.goal = None
        self.bingo_goals = None
        self.sign_maze = None
        self.multichest = RUPEES_20
        self.map = None  # Randomly generated map data

    def getEntrancePool(self, settings, connectorsOnly=False):
        entrances = []

        if connectorsOnly:
            if settings.entranceshuffle in ("split", "mixed"):
                entrances = [k for k, v in ENTRANCE_INFO.items() if v.type == "connector"]
            
            return entrances

        if settings.dungeonshuffle and settings.entranceshuffle == "none":
            entrances = [k for k, v in ENTRANCE_INFO.items() if v.type == "dungeon"]
        if settings.entranceshuffle in ("simple", "split", "mixed"):
            types = {"single"}
            if settings.tradequest:
                types.add("trade")
            if settings.shufflejunk:
                types.update(["dummy", "trade"])
            if settings.shuffleannoying:
                types.add("insanity")
            if settings.shufflewater:
                types.add("water")
            if settings.randomstartlocation:
                types.add("start")
            if settings.dungeonshuffle:
                types.add("dungeon")
            if settings.entranceshuffle in ("mixed"):
                types.add("connector")
            entrances = [k for k, v in ENTRANCE_INFO.items() if v.type in types]

        return entrances
    
    def swapEntrances(self, a, b):
        temp = self.entrance_mapping[a]
        self.entrance_mapping[a] = self.entrance_mapping[b]
        self.entrance_mapping[b] = temp
    
    def inaccessibleEntrances(self, settings, entrancePool):
        log = logic.Logic(settings, world_setup=self)
        return [x for x in entrancePool if log.world.overworld_entrance[x].location not in log.location_list]

    def pickEntrances(self, settings, rnd):
        if settings.overworld == "random":
            return
        if settings.overworld == "dungeondive":
            self.entrance_mapping = {"d%d" % (n): "d%d" % (n) for n in range(9)}
        if settings.randomstartlocation and settings.entranceshuffle == "none":
            start_location = start_locations[rnd.randrange(len(start_locations))]
            if start_location != "start_house":
                self.entrance_mapping[start_location] = "start_house"
                self.entrance_mapping["start_house"] = start_location

        entrancePool = self.getEntrancePool(settings)
        unmappedEntrances = list(entrancePool)

        for entrance in [x for x in entrancePool]:
            self.entrance_mapping[entrance] = unmappedEntrances.pop(rnd.randrange(len(unmappedEntrances)))

        if settings.entranceshuffle == 'split':
            # Shuffle connectors among themselves
            # entrancePool is intentionally overwritten so we're only swapping connectors
            entrancePool = self.getEntrancePool(settings, connectorsOnly=True)
            unmappedEntrances = list(entrancePool)

            for entrance in entrancePool.copy():
                self.entrance_mapping[entrance] = unmappedEntrances.pop(rnd.randrange(len(unmappedEntrances)))

        # Make sure all entrances in the pool are accessible
        for _ in range(1000):
            islands = self.inaccessibleEntrances(settings, entrancePool)

            if not islands:
                break

            island = rnd.choice(islands)
            main = rnd.choice([x for x in entrancePool if x not in islands])

            self.swapEntrances(island, main)
        
        if self.inaccessibleEntrances(settings, entrancePool):
            raise Error("Failed to make all entrances accessible after a bunch of retries")


    def randomize(self, settings, rnd):
        if settings.boss != "default":
            values = list(range(9))
            if settings.heartcontainers:
                # Color dungeon boss does not drop a heart container so we cannot shuffle him when we
                # have heart container shuffling
                values.remove(8)
            self.boss_mapping = []
            for n in range(8 if settings.heartcontainers else 9):
                value = rnd.choice(values)
                self.boss_mapping.append(value)
                if value in (3, 6) or settings.boss == "shuffle":
                    values.remove(value)
            if settings.heartcontainers:
                self.boss_mapping += [8]
        if settings.miniboss != "default":
            values = [name for name in self.miniboss_mapping.values()]
            for key in self.miniboss_mapping.keys():
                self.miniboss_mapping[key] = rnd.choice(values)
                if settings.miniboss == 'shuffle':
                    values.remove(self.miniboss_mapping[key])

        if settings.goal == 'random':
            self.goal = rnd.randint(-1, 8)
        elif settings.goal == 'open':
            self.goal = -1
        elif settings.goal in {"seashells", "bingo", "bingo-full"}:
            self.goal = settings.goal
        elif settings.goal in {"maze"}:
            self.goal = settings.goal
            self.sign_maze = maze.buildMaze(rnd)
        elif settings.goal == "specific":
            instruments = [c for c in "12345678"]
            rnd.shuffle(instruments)
            self.goal = "=" + "".join(instruments[:4])
        elif "-" in settings.goal:
            a, b = settings.goal.split("-")
            if a == "open":
                a = -1
            self.goal = rnd.randint(int(a), int(b))
        else:
            self.goal = int(settings.goal)
        if self.goal in {"bingo", "bingo-full"}:
            self.bingo_goals = bingo.randomizeGoals(rnd, settings)

        self.multichest = rnd.choices(MULTI_CHEST_OPTIONS, MULTI_CHEST_WEIGHTS)[0]

        self.pickEntrances(settings, rnd)

    def loadFromRom(self, rom):
        import patches.overworld
        if patches.overworld.isNormalOverworld(rom):
            import patches.entrances
            self.entrance_mapping = patches.entrances.readEntrances(rom)
        else:
            self.entrance_mapping = {"d%d" % (n): "d%d" % (n) for n in range(9)}
        self.boss_mapping = patches.enemies.readBossMapping(rom)
        self.miniboss_mapping = patches.enemies.readMiniBossMapping(rom)
        self.goal = 8 # Better then nothing
