from .itemInfo import ItemInfo
from .constants import *
from assembler import ASM


class BoomerangGuy(ItemInfo):
    OPTIONS = [BOOMERANG, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS, FEATHER, SHOVEL]

    # Cannot trade:
    # SWORD, BOMB, SHIELD, POWER_BRACELET, OCARINA, MAGIC_POWDER, BOW
    # Checks for these are at $46A2, and potentially we could remove those.
    # But SHIELD, BOMB and MAGIC_POWDER would most likely break things.

    def patch(self, rom, option):
        inv = INVENTORY_MAP[option]
        # Patch the check if you traded back the boomerang (so traded twice)
        rom.patch(0x19, 0x063F, ASM("cp $0D"), ASM("cp $%s" % (inv)))
        # Item to give by "default" (aka, boomerang)
        rom.patch(0x19, 0x06C1, ASM("ld a, $0D"), ASM("ld a, $%s" % (inv)))
        # Check if inventory slot is boomerang to give back item in this slot
        rom.patch(0x19, 0x06FC, ASM("cp $0D"), ASM("cp $%s" % (inv)))
        # Put the boomerang ID in the inventory of the boomerang guy (aka, traded back)
        rom.patch(0x19, 0x0710, ASM("ld a, $0D"), ASM("ld a, $%s" % (inv)))

    def read(self, rom):
        for k, v in INVENTORY_MAP.items():
            if int(v, 16) == rom.banks[0x19][0x0640]:
                return k
        raise ValueError()
