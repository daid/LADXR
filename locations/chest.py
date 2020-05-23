from .itemInfo import ItemInfo
from .constants import *
from assembler import ASM


class Chest(ItemInfo):
    OPTIONS = [POWER_BRACELET, SHIELD, BOW, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS, OCARINA,
        FEATHER, SHOVEL, MAGIC_POWDER, BOMB, SWORD, FLIPPERS, MAGNIFYING_LENS, MEDICINE,
        TAIL_KEY, ANGLER_KEY, FACE_KEY, BIRD_KEY, GOLD_LEAF,
        RUPEES_50, RUPEES_20, RUPEES_100, RUPEES_200, RUPEES_500,
        SEASHELL, MESSAGE, GEL, BOOMERANG]
        #500 rupees show 200 rupees message
        #not sure if we should se MAGIC_POWDER, as it overrules the toadstool

    def __init__(self, room):
        super().__init__()
        self.room = room
        self.addr = room + 0x560

    def patch(self, rom, option):
        rom.banks[0x14][self.addr] = CHEST_ITEMS[option]

        if self.room == 0x1B6:
            # Patch the code that gives the nightmare key when you throw the pot at the chest in dungeon 6
            # As this is hardcoded for a specific chest type
            rom.patch(3, 0x145D, ASM("ld a, $19"), ASM("ld a, $%02x" % (CHEST_ITEMS[option])))

    def read(self, rom):
        value = rom.banks[0x14][self.addr]
        for k, v in CHEST_ITEMS.items():
            if v == value:
                return k
        raise ValueError("Could not find chest contents in ROM (0x%02x)" % (value))

    def __repr__(self):
        return "%s:%03x" % (self.__class__.__name__, self.room)


class DungeonChest(Chest):
    def setLocation(self, location):
        self._location = location
        assert location.dungeon is not None
        d = location.dungeon
        self.OPTIONS = Chest.OPTIONS + ["MAP%d" % (d), "COMPASS%d" % (d), "STONE_BEAK%d" % (d), "NIGHTMARE_KEY%d" % (d), "KEY%d" % (d)]

    def patch(self, rom, option):
        if option.startswith(MAP) or option.startswith(COMPASS) or option.startswith(STONE_BEAK) or option.startswith(NIGHTMARE_KEY) or option.startswith(KEY):
            option = option[:-1]
        super().patch(rom, option)

    def read(self, rom):
        result = super().read(rom)
        if result in [MAP, COMPASS, STONE_BEAK, NIGHTMARE_KEY, KEY]:
            return "%s%d" % (result, self._location.dungeon)
        return result

    def __repr__(self):
        return "%s:%03x:%d" % (self.__class__.__name__, self.room, self._location.dungeon)
