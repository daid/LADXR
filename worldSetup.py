import patches.enemies
import patches.dungeonEntrances
import patches.startLocation
from locations.items import *


MULTI_CHEST_OPTIONS = [MAGIC_POWDER, BOMB, MEDICINE, RUPEES_50, RUPEES_20, RUPEES_100, RUPEES_200, RUPEES_500, SEASHELL, GEL, ARROWS_10, SINGLE_ARROW]
MULTI_CHEST_WEIGHTS = [20,           20,   20,       50,        50,        20,         10,         5,          5,        20,  10,        10]

class WorldSetup:
    def __init__(self):
        self.start_house_index = 0
        self.dungeon_entrance_mapping = list(range(9))
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
        if options.randomstartlocation:
            self.start_house_index = rnd.randint(0, 7)
        if options.dungeonshuffle:
            rnd.shuffle(self.dungeon_entrance_mapping)
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
                self.miniboss_mapping[key] = "GIANT_BUZZ_BLOB" # rnd.choice(values)
                if options.miniboss == 'shuffle':
                    values.remove(self.miniboss_mapping[key])
        self.multichest = rnd.choices(MULTI_CHEST_OPTIONS, MULTI_CHEST_WEIGHTS)[0]

    def loadFromRom(self, rom):
        self.start_house_index = patches.startLocation.readStartLocation(rom)
        self.dungeon_entrance_mapping = patches.dungeonEntrances.readEntrances(rom)
        self.boss_mapping = patches.enemies.readBossMapping(rom)
        self.miniboss_mapping = patches.enemies.readMiniBossMapping(rom)
