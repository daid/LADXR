from .itemInfo import ItemInfo
from .constants import *


class StartItem(ItemInfo):
    # We need to give something here that we can use to progress.
    #   Anything but a shield currently bugs out the logic, as it cannot place the shield somewhere else.
    # FUTURE: Giving a TAIL_KEY here could potentially be done by patching the code, this would open up the
    #   first dungeon, which has chests available without fighting.
    OPTIONS = [SHIELD] #, "POWER_BRACELET", "FEATHER", "BOOMERANG"]

    def patch(self, rom, option):
        # Change which item you get at the start.
        # (NOTE: This also sets the shield level to 1, which is fine, even if we do not get the shield)
        # Giving a sword here, gives a lv0 sword. Which does no damage?
        # Giving the power bracelet here gives a lv0 bracelet, most likely making lv2 inaccessible
        rom.patch(5, 0xCD1, "04", INVENTORY_MAP[option])
        rom.patch(5, 0xCC6, "86", INVENTORY_ICON[option]) # patch shield that icon that is shown.
        # Patch the text that Tarin uses to give your shield back.
        rom.texts[0x54] = b"#####, is it    " \
                        + b"dangerous to go " \
                        + b"alone!          " \
                        + b"take this!\xff"
        rom.texts[0x91] = b"Got the ...     " \
                        + b"something!\xff"

    def read(self, rom):
        value = rom.banks[5][0xCD1]
        for k, v in INVENTORY_MAP.items():
            if int(v, 16) == value:
                return k
        raise ValueError("Could not find start item contents in ROM (0x%02x)" % (value))
