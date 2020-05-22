from .itemInfo import ItemInfo
from .items import *
from assembler import ASM


class Chest(ItemInfo):
    OPTIONS = [POWER_BRACELET, SHIELD, BOW, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS, OCARINA,
        FEATHER, SHOVEL, MAGIC_POWDER, BOMB, SWORD, FLIPPERS, MAGNIFYING_LENS, MEDICINE,
        TAIL_KEY, ANGLER_KEY, FACE_KEY, BIRD_KEY, GOLD_LEAF,
        RUPEES_50, RUPEES_20, RUPEES_100, RUPEES_200, RUPEES_500,
        SEASHELL, MESSAGE, GEL, BOOMERANG]
        #500 rupees show 200 rupees message
        #not sure if we should se MAGIC_POWDER, as it overrules the toadstool
        #no idea what happens if we get MEDICINE when we have it already, most likely, nothing.
    MAPPING = {POWER_BRACELET: 0x00, SHIELD: 0x01, BOW: 0x02, HOOKSHOT: 0x03, MAGIC_ROD: 0x04, PEGASUS_BOOTS: 0x05, OCARINA: 0x06,
        FEATHER: 0x07, SHOVEL: 0x08, MAGIC_POWDER: 0x09, BOMB: 0x0A, SWORD: 0x0B, FLIPPERS: 0x0C, MAGNIFYING_LENS: 0x0D, MEDICINE: 0x10,
        TAIL_KEY: 0x11, ANGLER_KEY: 0x12, FACE_KEY: 0x13, BIRD_KEY: 0x14, GOLD_LEAF: 0x15,
        RUPEES_50: 0x1B, RUPEES_20: 0x1C, RUPEES_100: 0x1D, RUPEES_200: 0x1E, RUPEES_500: 0x1F,
        SEASHELL: 0x20, MESSAGE: 0x21, GEL: 0x22,
        MAP: 0x16, COMPASS: 0x17, STONE_BEAK: 0x18, NIGHTMARE_KEY: 0x19, KEY: 0x1A,
        BOOMERANG: 0x0E}

    def __init__(self, room):
        super().__init__()
        self.room = room
        self.addr = room + 0x560

    def patch(self, rom, option):
        rom.banks[0x14][self.addr] = self.MAPPING[option]

        if self.room == 0x1B6:
            # Patch the code that gives the nightmare key when you throw the pot at the chest in dungeon 6
            # As this is hardcoded for a specific chest type
            rom.patch(3, 0x145D, ASM("ld a, $19"), ASM("ld a, $%02x" % (self.MAPPING[option])))

    def read(self, rom):
        value = rom.banks[0x14][self.addr]
        for k, v in self.MAPPING.items():
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
