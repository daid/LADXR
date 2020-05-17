from .itemInfo import ItemInfo


class Chest(ItemInfo):
    OPTIONS = ["POWER_BRACELET", "MIRROR_SHIELD", "BOW", "HOOKSHOT", "MAGIC_ROD", "PEGASUS_BOOTS", "OCARINA",
        "FEATHER", "SHOVEL", "MAGIC_POWDER", "BOMB", "SWORD", "FLIPPERS", "MAGNIFYING_LENS", "MEDICINE",
        "TAIL_KEY", "ANGLER_KEY", "FACE_KEY", "BIRD_KEY", "GOLD_LEAF",
        "RUPEES_50", "RUPEES_20", "RUPEES_100", "RUPEES_200", "RUPEES_500",
        "SEASHELL", "MESSAGE", "GEL"]
        #BOW, ANGLER_KEY, RUPEES_500, FACE_KEY, BIRD_KEY, GOLD_LEAF shows wrong message
        #500 rupees show 200 rupees message
        #not sure if we should se MAGIC_POWDER, as it overrules the toadstool
        #no idea what happens if we get MEDICINE when we have it already, most likely, nothing.
    MAPPING = {"POWER_BRACELET": 0, "MIRROR_SHIELD": 1, "BOW": 2, "HOOKSHOT": 3, "MAGIC_ROD": 4, "PEGASUS_BOOTS": 5, "OCARINA": 6,
        "FEATHER": 7, "SHOVEL": 8, "MAGIC_POWDER": 9, "BOMB": 10, "SWORD": 11, "FLIPPERS": 12, "MAGNIFYING_LENS": 13, "MEDICINE": 0x10,
        "TAIL_KEY": 0x11, "ANGLER_KEY": 0x12, "FACE_KEY": 0x13, "BIRD_KEY": 0x14, "GOLD_LEAF": 0x15,
        "RUPEES_50": 0x1B, "RUPEES_20": 0x1C, "RUPEES_100": 0x1D, "RUPEES_200": 0x1E, "RUPEES_500": 0x1F,
        "SEASHELL": 0x20, "MESSAGE": 0x21, "GEL": 0x22,
        "MAP": 0x16, "COMPASS": 0x17, "STONE_BEAK": 0x18, "NIGHTMARE_KEY": 0x19, "KEY": 0x1A}

    def __init__(self, room):
        super().__init__()
        self.addr = room + 0x560

    def patch(self, rom, option):
        rom.banks[0x14][self.addr] = self.MAPPING[option]

    def read(self, rom):
        value = rom.banks[0x14][self.addr]
        for k, v in self.MAPPING.items():
            if v == value:
                return k
        raise ValueError("Could not find chest contents in ROM (0x%02x)" % (value))


class DungeonChest(Chest):
    def setLocation(self, location):
        self._location = location
        assert location.dungeon is not None
        d = location.dungeon
        self.OPTIONS = Chest.OPTIONS + ["MAP%d" % (d), "COMPASS%d" % (d), "STONE_BEAK%d" % (d), "NIGHTMARE_KEY%d" % (d), "KEY%d" % (d)]

    def patch(self, rom, option):
        if option.startswith("MAP") or option.startswith("COMPASS") or option.startswith("STONE_BEAK") or option.startswith("NIGHTMARE_KEY") or option.startswith("KEY"):
            option = option[:-1]
        super().patch(rom, option)

    def read(self, rom):
        result = super().read(rom)
        if result in ["MAP", "COMPASS", "STONE_BEAK", "NIGHTMARE_KEY", "KEY"]:
            return "%s%d" % (result, self._location.dungeon)
        return result
