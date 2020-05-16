import typing

from roomEditor import RoomEditor


class ItemInfo:
    OPTIONS = []
    all = []  # type: typing.List[ItemInfo]

    def __init__(self):
        self.item = None
        self._location = None
        ItemInfo.all.append(self)

    def setLocation(self, location):
        self._location = location

    def getOptions(self):
        return self.OPTIONS

    def patch(self, rom, option):
        raise NotImplementedError()

    def read(self, rom):
        raise NotImplementedError()


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


class StartItem(ItemInfo):
    OPTIONS = ["SHIELD"] #, "POWER_BRACELET", "FEATHER"]
    MAPPING = {"SWORD": "01", "BOMB": "02", "POWER_BRACELET": "03", "SHIELD": "04", "BOW": "05", "HOOKSHOT": "06",
               "MAGIC_ROD": "07", "PEGASUS_BOOTS": "08", "OCARINA": "09", "FEATHER": "0A", "SHOVEL": "0B",
               "MAGIC_POWDER": "0C", "BOOMERANG": "0D"}
    ICON = {"SWORD": "84", "BOMB": "80", "POWER_BRACELET": "82", "SHIELD": "86", "BOW": "88", "HOOKSHOT": "8A",
            "MAGIC_ROD": "8C", "PEGASUS_BOOTS": "98", "OCARINA": "90", "FEATHER": "92", "SHOVEL": "96",
            "MAGIC_POWDER": "8E", "BOOMERANG": "A4"}

    def patch(self, rom, option):
        # Change which item you get at the start.
        # (NOTE: This also sets the shield level to 1, which is fine, even if we do not get the shield)
        # Giving a sword here, gives a lvl0 sword. Which... does no damage.
        rom.patch(5, 0xCD1, "04", self.MAPPING[option])
        rom.patch(5, 0xCC6, "86", self.ICON[option]) # patch shield that icon that is shown.
        # Patch the text that Tarin uses to give your shield back.
        rom.texts[0x54] = b"#####, is it    " \
                        + b"dangerous to go " \
                        + b"alone, take this\xff"
        rom.texts[0x91] = b"Got the ...     " \
                        + b"something!\xff"

    def read(self, rom):
        value = rom.banks[5][0xCD1]
        for k, v in self.MAPPING.items():
            if int(v, 16) == value:
                return k
        raise ValueError("Could not find start item contents in ROM (0x%02x)" % (value))


class DroppedKey(ItemInfo):
    OPTIONS = ["KEY"]

    def __init__(self, room):
        super().__init__()
        self.room = room

    def setLocation(self, location):
        self.OPTIONS = ["KEY%d" % (location.dungeon)]

    def patch(self, rom, option):
        pass

    def read(self, rom):
        return self.OPTIONS[0]


class FlyingKey(ItemInfo):
    OPTIONS = ["KEY"]

    def __init__(self, room):
        super().__init__()
        self.room = room

    def setLocation(self, location):
        self.OPTIONS = ["KEY%d" % (location.dungeon)]

    def patch(self, rom, option):
        pass

    def read(self, rom):
        return self.OPTIONS[0]


class BeachSword(Chest):
    def __init__(self):
        super().__init__(0x0F2)
        self.room = 0x0F2

    def patch(self, rom, option):
        if option != "SWORD":
            # Set the chest data
            super().patch(rom, option)
            # Patch the room to contain a chest instead of the sword on the beach
            re = RoomEditor(rom, 0x0F2)
            re.changeObject(7, 4, 0xA0)
            re.moveObject(7, 4, 5, 4)
            re.removeEntities(0x31)  # remove sword
            re.removeEntities(0x41)  # remove owl
            re.store(rom)

    def read(self, rom):
        re = RoomEditor(rom, 0x0F2)
        if re.hasEntity(0x31):
            return "SWORD"
        return super().read(rom)


class Toadstool(ItemInfo):
    OPTIONS = ["TOADSTOOL"]

    def patch(self, rom, option):
        pass

    def read(self, rom):
        return "TOADSTOOL"


class BoomerangGuy(ItemInfo):
    OPTIONS = ["BOOMERANG"]

    def patch(self, rom, option):
        pass

    def read(self, rom):
        return "BOOMERANG"


class Witch(ItemInfo):
    OPTIONS = ["MAGIC_POWDER"]

    def patch(self, rom, option):
        pass

    def read(self, rom):
        return "MAGIC_POWDER"


class ShopShovel(ItemInfo):
    OPTIONS = ["SHOVEL"]

    def patch(self, rom, option):
        pass

    def read(self, rom):
        return "SHOVEL"


class ShopBow(ItemInfo):
    OPTIONS = ["BOW"]

    def patch(self, rom, option):
        pass

    def read(self, rom):
        return "BOW"


class ShopBombs(ItemInfo):
    OPTIONS = ["BOMB"]

    def patch(self, rom, option):
        pass

    def read(self, rom):
        return "BOMB"


class GoldLeaf(ItemInfo):
    OPTIONS = ["GOLD_LEAF"]

    def __init__(self, room):
        super().__init__()
        self.room = room

    def patch(self, rom, option):
        pass

    def read(self, rom):
        return "GOLD_LEAF"


class SlimeKey(ItemInfo):
    OPTIONS = ["SLIME_KEY"]

    def patch(self, rom, option):
        pass

    def read(self, rom):
        return "SLIME_KEY"


class Location:
    all = []

    def __init__(self, dungeon=None):
        self.items = []  # type: typing.List[ItemInfo]
        self.dungeon = dungeon
        self.connections = {}
        Location.all.append(self)

    def add(self, *item_infos):
        for ii in item_infos:
            assert isinstance(ii, ItemInfo)
            ii.setLocation(self)
            self.items.append(ii)
        return self

    def connect(self, other, *args, one_way=False):
        assert isinstance(other, Location)

        if other not in self.connections:
            self.connections[other] = []
        self.connections[other] += list(args)
        if not one_way:
            other.connect(self, *args, one_way=True)
        return self


class OR(list):
    def __init__(self, *args):
        super().__init__(args)

    def __repr__(self):
        return "or%s" % (super().__repr__())


class AND(list):
    def __init__(self, *args):
        super().__init__(args)

    def __repr__(self):
        return "and%s" % (super().__repr__())


class COUNT:
    def __init__(self, item, amount):
        self.item = item
        self.amount = amount

    def __repr__(self):
        return "%dx%s" % (self.amount, self.item)
