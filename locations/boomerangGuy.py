from .itemInfo import ItemInfo
from .constants import *
from assembler import ASM


class BoomerangGuy(ItemInfo):
    OPTIONS = [BOOMERANG]

    # Cannot trade:
    # SWORD, BOMB, SHIELD, POWER_BRACELET, OCARINA, MAGIC_POWDER, BOW
    # Checks for these are at $46A2, and potentially we could remove those.
    # But SHIELD, BOMB and MAGIC_POWDER would most likely break things.
    # SWORD and POWER_BRACELET would most likely introduce the lv0 shield/bracelet issue

    def __init__(self):
        super().__init__()
        self.enabled = False

    def configure(self, options):
        if options.boomerangtrade:
            self.OPTIONS = [BOOMERANG, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS, FEATHER, SHOVEL]
            self.enabled = True

    def patch(self, rom, option, *, cross_world=False):
        assert not cross_world
        if not self.enabled:
            return

        # Always have the boomerang trade guy enabled (normally you need the magnifier)
        rom.patch(0x19, 0x05EC, "FA0EDBFE0E", "3E0E00FE0E")  # show the guy
        rom.patch(0x00, 0x3199, "FA0EDBFE0E", "3E0E00FE0E")  # load the proper room layout

        inv = INVENTORY_MAP[option]
        # Patch the check if you traded back the boomerang (so traded twice)
        rom.patch(0x19, 0x063F, ASM("cp $0D"), ASM("cp $%s" % (inv)))
        # Item to give by "default" (aka, boomerang)
        rom.patch(0x19, 0x06C1, ASM("ld a, $0D"), ASM("ld a, $%s" % (inv)))
        # Check if inventory slot is boomerang to give back item in this slot
        rom.patch(0x19, 0x06FC, ASM("cp $0D"), ASM("cp $%s" % (inv)))
        # Put the boomerang ID in the inventory of the boomerang guy (aka, traded back)
        rom.patch(0x19, 0x0710, ASM("ld a, $0D"), ASM("ld a, $%s" % (inv)))

        rom.texts[0x222] = b"Okay, let's do  "\
                           b"it!\xff"
        rom.texts[0x224] = b"You got the a   "\
                           b"new item in     "\
                           b"exchange for the"\
                           b"item you had.\xff"
        rom.texts[0x225] = b"Give me back my "\
                           b"item, I beg you!"\
                           b"I'll return the "\
                           b"item you gave me"\
                           b"    Okay Not Now"\
                           b"\xfe"
        rom.texts[0x226] = b"The item came   "\
                           b"back to you. You"\
                           b"returned the    "\
                           b"other item.\xff"

    def read(self, rom):
        for k, v in INVENTORY_MAP.items():
            if int(v, 16) == rom.banks[0x19][0x0640]:
                return k
        raise ValueError()
