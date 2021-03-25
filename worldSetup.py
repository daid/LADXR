import patches.enemies
import patches.dungeonEntrances
import patches.startLocation
from locations.items import *


MULTI_CHEST_OPTIONS = [MAGIC_POWDER, BOMB, MEDICINE, RUPEES_50, RUPEES_20, RUPEES_100, RUPEES_200, RUPEES_500, SEASHELL, GEL, ARROWS_10, SINGLE_ARROW]
MULTI_CHEST_WEIGHTS = [20,           20,   20,       50,        50,        20,         10,         5,          5,        20,  10,        10]

class EntranceInfo:
    def __init__(self, room, *, dungeon=None, index=None):
        pass

ENTRANCE_INFO = {
    # Row0-1
    "d8":                           EntranceInfo(0x10, dungeon=8),
    "phone_d8":                     EntranceInfo(0x11),
    "fire_cave_exit":               EntranceInfo(0x03),
    "fire_cave_entrance":           EntranceInfo(0x13),
    "madbatter_taltal":             EntranceInfo(0x04),
    "left_taltal_entrance":         EntranceInfo(0x15),
    "right_taltal_entrance":        EntranceInfo(0x17),
    "left_to_right_taltalentrance": EntranceInfo(0x07),
    "left_taltal_exit1":            EntranceInfo(0x18, index=0),
    "left_taltal_exit2":            EntranceInfo(0x18, index=1),
    "papahl_entrance":              EntranceInfo(0x19),
    "papahl_exit":                  EntranceInfo(0x0A, index=1),
    "rooster_house":                EntranceInfo(0x0A, index=0),
    "bird_cave":                    EntranceInfo(0x0A, index=2),
    "multichest_left":              EntranceInfo(0x1D, index=0),
    "multichest_right":             EntranceInfo(0x1D, index=1),
    "multichest_top":               EntranceInfo(0x0D),
    "right_taltal_connector1":      EntranceInfo(0x1E, index=0),
    "right_taltal_connector2":      EntranceInfo(0x1F, index=0),
    "right_taltal_connector3":      EntranceInfo(0x1E, index=1),
    "right_taltal_connector4":      EntranceInfo(0x1F, index=2),
    "right_taltal_connector5":      EntranceInfo(0x1F, index=1),
    "right_taltal_connector6":      EntranceInfo(0x0F),
    "right_fairy":                  EntranceInfo(0x1F, index=3),
    "d7":                           EntranceInfo(0x0E, dungeon=7),
    # Row 2-3
    "writes_cave_left":             EntranceInfo(0x20),
    "writes_cave_right":            EntranceInfo(0x21),
    "writes_house":                 EntranceInfo(0x30),
    "writes_phone":                 EntranceInfo(0x31),
    "d2":                           EntranceInfo(0x24, dungeon=2),
    "moblin_cave":                  EntranceInfo(0x35),
    "photo_house":                  EntranceInfo(0x37),
    "mambo":                        EntranceInfo(0x2A),
    "d4":                           EntranceInfo(0x2B, dungeon=4, index=0),
    "d4_exit":                      EntranceInfo(0x2B, dungeon=4, index=1),
    "d4_exit_exit":                 EntranceInfo(0x2D),
    "heartpiece_swim_cave":         EntranceInfo(0x2E),
    "raft_return_exit":             EntranceInfo(0x2F),
    "raft_house":                   EntranceInfo(0x3F),
    "raft_return_enter":            EntranceInfo(0x8F),
    # Forest and everything right of it
    "hookshot_cave":                EntranceInfo(0x42),
    "toadstool_exit":               EntranceInfo(0x50),
    "forest_madbatter":             EntranceInfo(0x52),
    "toadstool_entrance":           EntranceInfo(0x62),
    "crazy_tracy":                  EntranceInfo(0x45),
    "witch":                        EntranceInfo(0x65),
    "graveyard_cave_left":          EntranceInfo(0x75),
    "graveyard_cave_right":         EntranceInfo(0x76),
    "d0":                           EntranceInfo(0x77, dungeon=9),
    #Castle
    "castle_jump_cave":             EntranceInfo(0x78),
    "castle_main_entrance":         EntranceInfo(0x69),
    "castle_upper_left":            EntranceInfo(0x59, index=0),
    "castle_upper_right":           EntranceInfo(0x59, index=1),
    "castle_secret_exit":           EntranceInfo(0x49),
    "castle_secret_entrance":       EntranceInfo(0x4A),
    "castle_phone":                 EntranceInfo(0x4B),
    #Mabe village
    "papahl_house_left":            EntranceInfo(0x82, index=0),
    "papahl_house_right":           EntranceInfo(0x82, index=1),
    "dream_hut":                    EntranceInfo(0x83),
    "rooster_grave":                EntranceInfo(0x92),
    "shop":                         EntranceInfo(0x93),
    "madambowwow":                  EntranceInfo(0xA1, index=0),
    "kennel":                       EntranceInfo(0xA1, index=1),
    "start_house":                  EntranceInfo(0xA2),
    "library":                      EntranceInfo(0xB0),
    "ulrira":                       EntranceInfo(0xB1),
    "mabe_phone":                   EntranceInfo(0xB2),
    "trendy_shop":                  EntranceInfo(0xB3),
    # Ukuku Prairie
    "prairie_left_phone":           EntranceInfo(0xA4),
    "prairie_left_cave1":           EntranceInfo(0x84),
    "prairie_left_cave2":           EntranceInfo(0x86),
    "prairie_left_fairy":           EntranceInfo(0x87),
    "d3":                           EntranceInfo(0xB5, dungeon=3),
    "prairie_right_phone":          EntranceInfo(0x88),
    "seashell_mansion":             EntranceInfo(0x8A),
    "prairie_right_cave_top":       EntranceInfo(0xB8, index=1),
    "prairie_right_cave_bottom":    EntranceInfo(0xC8),
    "prairie_right_cave_high":      EntranceInfo(0xB8, index=0),
    "prairie_to_animal_connector":  EntranceInfo(0xAA),
    "animal_to_prairie_connector":  EntranceInfo(0xAB),
    
    "d6":                           EntranceInfo(0x8C, dungeon=6),
    "d6_connector_exit":            EntranceInfo(0x9C),
    "d6_connector_entrance":        EntranceInfo(0x9D),
    "armos_maze_cave":              EntranceInfo(0xAE),
    "armos_temple":                 EntranceInfo(0xAC),
    # Beach area
    "d1":                           EntranceInfo(0xD3, dungeon=1),
    "boomerang_cave":               EntranceInfo(0xF4),
    "banana_seller":                EntranceInfo(0xE3),
    "ghost_house":                  EntranceInfo(0xF6),

    #Lower prairie
    "prairie_low_phone":            EntranceInfo(0xE8),
    "prairie_madbatter_connector_entrance": EntranceInfo(0xF9),
    "prairie_madbatter_connector_exit": EntranceInfo(0xE7),
    "prairie_madbatter":            EntranceInfo(0xE6),

    "d5":                           EntranceInfo(0xD9),
    # Animal village
    "animal_phone":                 EntranceInfo(0xDB),
    "animal_house1":                EntranceInfo(0xCC, index=0),
    "animal_house2":                EntranceInfo(0xCC, index=1),
    "animal_house3":                EntranceInfo(0xCD, index=1),
    "animal_house4":                EntranceInfo(0xCD, index=2),
    "animal_house5":                EntranceInfo(0xDD),
    "animal_cave":                  EntranceInfo(0xCD, index=0),
    "desert_cave":                  EntranceInfo(0xCF),
}

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
                self.miniboss_mapping[key] = rnd.choice(values)
                if options.miniboss == 'shuffle':
                    values.remove(self.miniboss_mapping[key])
        self.multichest = rnd.choices(MULTI_CHEST_OPTIONS, MULTI_CHEST_WEIGHTS)[0]

    def loadFromRom(self, rom):
        self.start_house_index = patches.startLocation.readStartLocation(rom)
        self.dungeon_entrance_mapping = patches.dungeonEntrances.readEntrances(rom)
        self.boss_mapping = patches.enemies.readBossMapping(rom)
        self.miniboss_mapping = patches.enemies.readMiniBossMapping(rom)
