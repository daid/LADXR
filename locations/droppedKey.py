from .itemInfo import ItemInfo
from .constants import *


class DroppedKey(ItemInfo):
    OPTIONS = [POWER_BRACELET, SHIELD, BOW, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS, OCARINA,
        FEATHER, SHOVEL, MAGIC_POWDER, BOMB, SWORD, FLIPPERS, MAGNIFYING_LENS, MEDICINE,
        TAIL_KEY, ANGLER_KEY, FACE_KEY, BIRD_KEY, GOLD_LEAF, SLIME_KEY, ROOSTER, HAMMER,
        RUPEES_50, RUPEES_20, RUPEES_100, RUPEES_200, RUPEES_500,
        SEASHELL, GEL, BOOMERANG, HEART_PIECE, ARROWS_10, SINGLE_ARROW,
        MAX_POWDER_UPGRADE, MAX_BOMBS_UPGRADE, MAX_ARROWS_UPGRADE, RED_TUNIC, BLUE_TUNIC,
        HEART_CONTAINER, BAD_HEART_CONTAINER, TOADSTOOL, SONG1, SONG2, SONG3,
        INSTRUMENT1, INSTRUMENT2, INSTRUMENT3, INSTRUMENT4, INSTRUMENT5, INSTRUMENT6, INSTRUMENT7, INSTRUMENT8,
        TRADING_ITEM_YOSHI_DOLL, TRADING_ITEM_RIBBON, TRADING_ITEM_DOG_FOOD, TRADING_ITEM_BANANAS, TRADING_ITEM_STICK,
        TRADING_ITEM_HONEYCOMB, TRADING_ITEM_PINEAPPLE, TRADING_ITEM_HIBISCUS, TRADING_ITEM_LETTER, TRADING_ITEM_BROOM,
        TRADING_ITEM_FISHING_HOOK, TRADING_ITEM_NECKLACE, TRADING_ITEM_SCALE, TRADING_ITEM_MAGNIFYING_GLASS
    ]
    MULTIWORLD = True

    def patch(self, rom, option, *, multiworld=None):
        if option.startswith(MAP) or option.startswith(COMPASS) or option.startswith(STONE_BEAK) or option.startswith(NIGHTMARE_KEY) or option.startswith(KEY):
            if self._location.dungeon == int(option[-1]) and multiworld is None and self.room not in {0x166, 0x223}:
                option = option[:-1]
        item_id = CHEST_ITEMS[option]
        if option == GEL:
            randomnumber = self.room  # TODO: We need some way to get some seed depended randomness in here.
            item_id = GEL_DISGUISE_MIN + (randomnumber % (GEL_DISGUISE_MAX - GEL_DISGUISE_MIN))
        rom.banks[0x3E][self.room + 0x3800] = item_id
        if self.room == 0x169:  # Room in D4 where the key drops down the hole into the sidescroller
            rom.banks[0x3E][0x017C + 0x3800] = item_id
        elif self.room == 0x166:  # D4 boss, also place the item in out real boss room.
            rom.banks[0x3E][0x01ff + 0x3800] = item_id
        elif self.room == 0x223:  # D7 boss, also place the item in our real boss room.
            rom.banks[0x3E][0x02E8 + 0x3800] = item_id
        elif self.room == 0x092:  # Marins song
            rom.banks[0x3E][0x00DC + 0x3800] = item_id

        if multiworld is not None:
            rom.banks[0x3E][0x3300 + self.room] = multiworld
            if self.room == 0x169:  # Room in D4 where the key drops down the hole into the sidescroller
                rom.banks[0x3E][0x3300 + 0x017C] = multiworld
            elif self.room == 0x166:  # D4 boss, also place the item in out real boss room.
                rom.banks[0x3E][0x3300 + 0x01ff] = multiworld
            elif self.room == 0x223:  # D7 boss, also place the item in our real boss room.
                rom.banks[0x3E][0x3300 + 0x02E8] = multiworld
            elif self.room == 0x092:  # Marins song
                rom.banks[0x3E][0x3300 + 0x00DC] = multiworld

    def read(self, rom):
        assert self._location is not None, hex(self.room)
        value = rom.banks[0x3E][self.room + 0x3800]
        if GEL_DISGUISE_MIN <= value < GEL_DISGUISE_MAX:
            return GEL
        for k, v in CHEST_ITEMS.items():
            if v == value:
                if k in [MAP, COMPASS, STONE_BEAK, NIGHTMARE_KEY, KEY]:
                    assert self._location.dungeon is not None, "Dungeon item outside of dungeon? %r" % (self)
                    return "%s%d" % (k, self._location.dungeon)
                return k
        raise ValueError("Could not find chest contents in ROM (0x%02x)" % (value))

    def __repr__(self):
        if self._location and self._location.dungeon is not None:
            return "%s:%03x:%d" % (self.__class__.__name__, self.room, self._location.dungeon)
        else:
            return "%s:%03x" % (self.__class__.__name__, self.room)
