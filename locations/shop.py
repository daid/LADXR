from .itemInfo import ItemInfo
from .constants import *
from utils import formatText


class ShopItem(ItemInfo):
    OPTIONS = [POWER_BRACELET, SHIELD, BOW, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS, OCARINA,
        FEATHER, SHOVEL, MAGIC_POWDER, BOMB, SWORD, FLIPPERS, MAGNIFYING_LENS, MEDICINE,
        TAIL_KEY, ANGLER_KEY, FACE_KEY, BIRD_KEY, GOLD_LEAF, SLIME_KEY, ROOSTER, HAMMER,
        RUPEES_50, RUPEES_20, RUPEES_100, RUPEES_200, RUPEES_500,
        SEASHELL, BOOMERANG, HEART_PIECE, BOWWOW, ARROWS_10, SINGLE_ARROW,
        MAX_POWDER_UPGRADE, MAX_BOMBS_UPGRADE, MAX_ARROWS_UPGRADE, RED_TUNIC, BLUE_TUNIC,
        HEART_CONTAINER, BAD_HEART_CONTAINER, TOADSTOOL, SONG1, SONG2, SONG3,
        INSTRUMENT1, INSTRUMENT2, INSTRUMENT3, INSTRUMENT4, INSTRUMENT5, INSTRUMENT6, INSTRUMENT7, INSTRUMENT8,
        TRADING_ITEM_YOSHI_DOLL, TRADING_ITEM_RIBBON, TRADING_ITEM_DOG_FOOD, TRADING_ITEM_BANANAS, TRADING_ITEM_STICK,
        TRADING_ITEM_HONEYCOMB,TRADING_ITEM_PINEAPPLE, TRADING_ITEM_HIBISCUS, TRADING_ITEM_LETTER, TRADING_ITEM_BROOM,
        TRADING_ITEM_FISHING_HOOK,TRADING_ITEM_NECKLACE,TRADING_ITEM_SCALE,TRADING_ITEM_MAGNIFYING_GLASS,
        TAIL_CAVE_OPENED, KEY_CAVERN_OPENED, ANGLER_TUNNEL_OPENED, FACE_SHRINE_OPENED, CASTLE_GATE_OPENED, EAGLE_TOWER_OPENED
    ]

    def __init__(self, index, *, price=None, room=0x2A1):
        self.__index = index
        self.__price = price if price is not None else [200, 980][index]
        self.__shopsanity = False
        assert 0x200 <= room < 0x2FF, "Shops needs to be in underworld 2"
        super().__init__(room)

    def configure(self, options):
        super().configure(options)
        self.__shopsanity = options.shopsanity != ''
        if options.shopsanity == 'important':
            self.OPTIONS = [opt for opt in self.OPTIONS if opt not in [
                MAGNIFYING_LENS, MEDICINE, GOLD_LEAF,
                MAGIC_POWDER, BOMB,
                RUPEES_50, RUPEES_20, RUPEES_100, RUPEES_200, RUPEES_500,
                SEASHELL, HEART_PIECE, BOWWOW, ARROWS_10, SINGLE_ARROW,
                MAX_POWDER_UPGRADE, MAX_BOMBS_UPGRADE, MAX_ARROWS_UPGRADE, RED_TUNIC, BLUE_TUNIC,
                HEART_CONTAINER, BAD_HEART_CONTAINER, TOADSTOOL, SONG1, SONG2, SONG3,
                TRADING_ITEM_YOSHI_DOLL, TRADING_ITEM_RIBBON, TRADING_ITEM_DOG_FOOD, TRADING_ITEM_BANANAS, TRADING_ITEM_STICK,
                TRADING_ITEM_HONEYCOMB,TRADING_ITEM_PINEAPPLE, TRADING_ITEM_HIBISCUS, TRADING_ITEM_LETTER, TRADING_ITEM_BROOM,
                TRADING_ITEM_FISHING_HOOK,TRADING_ITEM_NECKLACE,TRADING_ITEM_SCALE,TRADING_ITEM_MAGNIFYING_GLASS,
                TAIL_CAVE_OPENED, KEY_CAVERN_OPENED, ANGLER_TUNNEL_OPENED, FACE_SHRINE_OPENED, CASTLE_GATE_OPENED, EAGLE_TOWER_OPENED,
                KEY0, KEY1, KEY2, KEY3, KEY4, KEY5, KEY6, KEY7, KEY8,
                MAP0, MAP1, MAP2, MAP3, MAP4, MAP5, MAP6, MAP7, MAP8,
                COMPASS0, COMPASS1, COMPASS2, COMPASS3, COMPASS4, COMPASS5, COMPASS6, COMPASS7, COMPASS8,
                STONE_BEAK0, STONE_BEAK1, STONE_BEAK2, STONE_BEAK3, STONE_BEAK4, STONE_BEAK5, STONE_BEAK6, STONE_BEAK7, STONE_BEAK8,
            ]]

    def patch(self, rom, option, *, multiworld=None):
        assert multiworld is None
        if self.__index == 0:
            # First item goes into the drop key table
            rom.banks[0x3E][self.room + 0x3800] = CHEST_ITEMS[option]
            if not self.__shopsanity:
                rom.texts[0x030] = formatText("Deluxe {%s} %d {RUPEES}!" % (option, self.__price), ask="Buy  No Way")
        elif self.__index == 1:
            # Second item goes into the chest table
            rom.banks[0x14][self.room + 0x560] = CHEST_ITEMS[option]
            if not self.__shopsanity:
                rom.texts[0x02C] = formatText("{%s} Only %d {RUPEES}!" % (option, self.__price), ask="Buy  No Way")

    def read(self, rom):
        value = rom.banks[0x3E][self.room + 0x3800]
        if self.__index == 1:
            value = rom.banks[0x14][self.room + 0x560]
        for k, v in CHEST_ITEMS.items():
            if v == value:
                return k
        raise ValueError("Could not find shop item contents in ROM (0x%02x)" % (value))

    @property
    def nameId(self):
        return "0x%03X-%s" % (self.room, self.__index)

    def __repr__(self):
        return "%s(%d)" % (self.__class__.__name__, self.__index)
