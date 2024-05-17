from .itemInfo import ItemInfo
from .constants import *
import utils


class TradeSequenceItem(ItemInfo):
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

    def __init__(self, room, default_item):
        super().__init__(room)
        self.__default_item = default_item

    def configure(self, options):
        if not options.tradequest:
            self.OPTIONS = [self.__default_item]

    def patch(self, rom, option, *, multiworld=None):
        rom.banks[0x3E][self.room + 0x3B16] = CHEST_ITEMS[option]

        if option == self.__default_item:
            return
        if self.__default_item == TRADING_ITEM_DOG_FOOD:
            rom.texts[0x181] = utils.formatText("Make-up! Jewels! Dresses! I want it all! Sigh... And some new accessories would be nice... Oh! That Ribbon! I need it! Will you trade for my {%s}?" % option, ask="Yes  No!")
            rom.texts[0x182] = b'\xff'
            rom.texts[0x183] = utils.formatText("Lucky! Thanks! Well, here's your {%s}!" % option)
        elif self.__default_item == TRADING_ITEM_BANANAS:
            rom.texts[0x1CA] = utils.formatText("MUNCH MUNCH!! ... ... ... ... That was great! I know it's not a fair trade, but here's some {%s}! YUM..." % option)
        elif self.__default_item == TRADING_ITEM_PINEAPPLE:
            rom.texts[0x1CF] = utils.formatText("Hi ho! Hey you! Is that possibly a <honeycomb> you have? I just ran out! Will you swap it for a {%s}?" % option, ask="Yes  No")
        elif self.__default_item == TRADING_ITEM_HIBISCUS:
            rom.texts[0x173] = utils.formatText("AH! This isn't meant to be a reward... Here, take this {%s}!" % option)
        elif self.__default_item == TRADING_ITEM_LETTER:
            rom.texts[0x168] = utils.formatText("I would like you to take this {%s}, please!" % option)
        elif self.__default_item == TRADING_ITEM_BROOM:
            rom.texts[0x135] = utils.formatText("Mmm... She's so beautiful... I must give you something for your trouble... Hmm...  Well, it looks like all I have is this {%s}... how'll that be?" % option, ask="Fine No...")
        elif self.__default_item == TRADING_ITEM_FISHING_HOOK:
            rom.texts[0x15D] = utils.formatText("Okay! In return you can have this {%s} I found when I swept by the river bank!" % option)

    def read(self, rom):
        assert self._location is not None, hex(self.room)
        value = rom.banks[0x3E][self.room + 0x3B16]
        for k, v in CHEST_ITEMS.items():
            if v == value:
                return k
        raise ValueError("Could not find owl statue contents in ROM (0x%02x)" % (value))

    def __repr__(self):
        return "%s:%03x" % (self.__class__.__name__, self.room)

    @property
    def nameId(self):
        return "0x%03X-Trade" % self.room
