from .itemInfo import ItemInfo
from .constants import *
from assembler import ASM


class KeyHole(ItemInfo):
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
        TRADING_ITEM_FISHING_HOOK, TRADING_ITEM_NECKLACE, TRADING_ITEM_SCALE, TRADING_ITEM_MAGNIFYING_GLASS,
        TAIL_CAVE_OPENED, KEY_CAVERN_OPENED, ANGLER_TUNNEL_OPENED, FACE_SHRINE_OPENED, CASTLE_GATE_OPENED, EAGLE_TOWER_OPENED
    ]
    MULTIWORLD = False

    def __init__(self, room, default_reward):
        super().__init__(room)
        self.__default_reward = default_reward

    def configure(self, options):
        if options.keyholesanity:
            super().configure(options)
        else:
            self.OPTIONS = [self.__default_reward]

    def patch(self, rom, option, *, multiworld=None):
        item_id = CHEST_ITEMS[option]
        if option == GEL:
            randomnumber = self.room  # TODO: We need some way to get some seed depended randomness in here.
            item_id = GEL_DISGUISE_MIN + (randomnumber % (GEL_DISGUISE_MAX - GEL_DISGUISE_MIN))
        rom.banks[0x3E][self.room + 0x3B16] = item_id

        if option == self.__default_reward:  # Keyhole is not changed, no patch required.
            return

        if rom.banks[0x02][0x2FA9] == 0xF0:
            rom.patch(0x02, 0x2FA9, ASM("ldh a, [hRoomStatus]\nbit 4, a"), ASM("call $8000-5"), fill_nop=True)
            rom.patch(0x02, 0x4000-5, "00" * 5, ASM("ldh a, [hRoomStatus]\nbit 4, a\nret"), fill_nop=True)
            rom.patch(0x02, 0x3D00, "00" * 9, ASM("""
                and a
                jr  z, skip  
                ld a, $09 ; give "owl statue" item and message
                rst 8
            skip:
                or 1 ; Return with "nothing to do"
                ret
            """))

        if self.room == 0x0D3:
            self.__addKeyholePatch(rom, 0x0D3, 0xDB11)
        elif self.room == 0x0B5:
            self.__addKeyholePatch(rom, 0x0B5, 0xDB15)
        elif self.room == 0x02B:
            self.__addKeyholePatch(rom, 0x02B, 0xDB12)
        elif self.room == 0x08C:
            self.__addKeyholePatch(rom, 0x08C, 0xDB13)
        elif self.room == 0x00E:
            self.__addKeyholePatch(rom, 0x00E, 0xDB14)
        elif self.room == 0x2C3:
            # Do not open the castle with the button
            rom.patch(0x02, 0x3831, ASM("set 4, [hl]"), "", fill_nop=True)
            # Give the item on the button press
            rom.patch(0x15, 0x00E9, ASM("call $7CDB"), ASM("ld a, 9\nrst 8"))
        else:
            raise RuntimeError(f"Don't know how to patch keyhole at {self.room:03x}:{self.__default_reward}")

    def __addKeyholePatch(self, rom, room_nr, key_addr):
        target_addr = rom.banks[0x02][0x2FAA] | rom.banks[0x02][0x2FAB] << 8
        code = ASM(f"""
            ldh a, [hMapRoom]
            cp  ${room_nr:02x}
            jr  nz, skip
            ld  a, [${key_addr:04x}]
            jp  $7D00
        skip:""")
        cs = len(code) // 2
        rom.patch(0x02, target_addr - cs - 0x4000, "00" * cs, code)
        rom.patch(0x02, 0x2FAA, ASM(f"dw ${target_addr:04x}"), ASM(f"dw ${target_addr-cs:04x}"))

    def read(self, rom):
        assert self._location is not None, hex(self.room)
        value = rom.banks[0x3E][self.room + 0x3B16]
        if GEL_DISGUISE_MIN <= value < GEL_DISGUISE_MAX:
            return GEL
        for k, v in CHEST_ITEMS.items():
            if v == value:
                return k
        raise ValueError("Could not find chest contents in ROM (0x%02x)" % (value))

    def __repr__(self):
        return "%s:%03x" % (self.__class__.__name__, self.room)
