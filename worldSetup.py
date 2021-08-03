import patches.enemies
from locations.items import *
from entranceInfo import ENTRANCE_INFO


MULTI_CHEST_OPTIONS = [MAGIC_POWDER, BOMB, MEDICINE, RUPEES_50, RUPEES_20, RUPEES_100, RUPEES_200, RUPEES_500, SEASHELL, GEL, ARROWS_10, SINGLE_ARROW]
MULTI_CHEST_WEIGHTS = [20,           20,   20,       50,        50,        20,         10,         5,          5,        20,  10,        10]


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
        }
        self.multichest = RUPEES_20

    def randomize(self, options, rnd):
        if options.overworld == "dungeondive":
            self.entrance_mapping = {"d%d" % (n): "d%d" % (n) for n in range(9)}
        if options.randomstartlocation and options.entranceshuffle == "none":
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
            start_location = start_locations.pop(rnd.randrange(len(start_locations)))
            if start_location != "start_house":
                self.entrance_mapping[start_location] = "start_house"
                self.entrance_mapping["start_house"] = start_location
        if options.dungeonshuffle and options.entranceshuffle == "none":
            entrances = [k for k, v in ENTRANCE_INFO.items() if v.type == "dungeon"]
            for entrance in entrances.copy():
                self.entrance_mapping[entrance] = entrances.pop(rnd.randrange(len(entrances)))
        if options.entranceshuffle in ("simple", "advanced", "expert", "insanity"):
            types = {"single"}
            if options.entranceshuffle in ("expert", "insanity"):
                types.add("dummy")
            if options.entranceshuffle in ("insanity",):
                types.add("insanity")
            if options.randomstartlocation:
                types.add("start")
            if options.dungeonshuffle:
                types.add("dungeon")
            entrances = [k for k, v in ENTRANCE_INFO.items() if v.type in types]
            for entrance in entrances.copy():
                self.entrance_mapping[entrance] = entrances.pop(rnd.randrange(len(entrances)))

        if options.entranceshuffle in ("advanced", "expert", "insanity"):
            entrances = [k for k, v in ENTRANCE_INFO.items() if v.type == "connector"]
            for entrance in entrances.copy():
                self.entrance_mapping[entrance] = entrances.pop(rnd.randrange(len(entrances)))

        if options.boss != "default":
            values = list(range(9))
            if options.heartcontainers:
                # Color dungeon boss does not drop a heart container so we cannot shuffle him when we
                # have heart container shuffling
                values.remove(8)
            self.boss_mapping = []
            for n in range(8 if options.heartcontainers else 9):
                value = rnd.choice(values)
                self.boss_mapping.append(value)
                if value in (3, 6) or options.boss == "shuffle":
                    values.remove(value)
            if options.heartcontainers:
                self.boss_mapping += [8]
        if options.miniboss != "default":
            values = [name for name in self.miniboss_mapping.values()]
            for key in self.miniboss_mapping.keys():
                self.miniboss_mapping[key] = rnd.choice(values)
                if options.miniboss == 'shuffle':
                    values.remove(self.miniboss_mapping[key])
        self.multichest = rnd.choices(MULTI_CHEST_OPTIONS, MULTI_CHEST_WEIGHTS)[0]

    def loadFromRom(self, rom):
        import patches.overworld
        if patches.overworld.isNormalOverworld(rom):
            import patches.entrances
            self.entrance_mapping = patches.entrances.readEntrances(rom)
        else:
            self.entrance_mapping = {"d%d" % (n): "d%d" % (n) for n in range(9)}
        self.boss_mapping = patches.enemies.readBossMapping(rom)
        self.miniboss_mapping = patches.enemies.readMiniBossMapping(rom)
