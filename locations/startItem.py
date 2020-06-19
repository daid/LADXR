from .itemInfo import ItemInfo
from .constants import *
from assembler import ASM
from utils import formatText


class StartItem(ItemInfo):
    # We need to give something here that we can use to progress.
    # FUTURE: Giving a TAIL_KEY here could potentially be done by patching the code, this would open up the
    #   first dungeon, which has chests available without fighting.
    OPTIONS = [SWORD, SHIELD, POWER_BRACELET, FEATHER, BOOMERANG, MAGIC_ROD]
    MESSAGE = {SWORD: 0x9B, SHIELD: 0x91, POWER_BRACELET: 0x90, FEATHER: 0x97, BOOMERANG: 0xD9, MAGIC_ROD: 0x94, BOWWOW: 0xC8}

    def __init__(self):
        super().__init__()
        self.give_bowwow = False

    def configure(self, options):
        if options.bowwow != 'normal':
            # When we have bowwow mode, we pretend to be a sword for logic reasons
            self.OPTIONS = [SWORD]
            self.give_bowwow = True

    def patch(self, rom, option, *, cross_world=False):
        assert not cross_world
        # TODO: Seems walking back into the house with certain options causes the initial event to repeat.

        if self.give_bowwow:
            option = BOWWOW
            rom.texts[0xC8] = formatText(b"Got BowWow!")
            rom.patch(0x05, 0x0CD0, 0x0CDA, ASM("""
                ld   a, $01
                ld   [$DB56], a
            """), fill_nop=True)
            rom.patch(0x05, 0x0CF3, ASM("ld de, $4CC6\ncall $3C77"), ASM("ld de, $401C\ncall $3BC0"))
            rom.patch(5, 0x0CDA, ASM("ld a, $22"), ASM("ld a, $00"))  # do not change links sprite into the one with a shield
        else:
            # Change which item you get at the start.
            rom.patch(5, 0x0CD1, "04", INVENTORY_MAP[option])
            rom.patch(5, 0x0CC6, "8617", INVENTORY_ICON[option]) # patch shield that icon that is shown.
            if option != SHIELD:
                rom.patch(5, 0x0CDA, ASM("ld a, $22"), ASM("ld a, $00"))  # do not change links sprite into the one with a shield
                #   Do not set the shield level to 1, but potentially set another item level if needed.
                if option == SWORD:
                    # TOFIX: This directly hides marin and tarin
                    rom.patch(5, 0x0CD7, ASM("ld [$DB44], a"), ASM("ld [$DB4E], a"), fill_nop=True)
                elif option == POWER_BRACELET:
                    rom.patch(5, 0x0CD7, ASM("ld [$DB44], a"), ASM("ld [$DB43], a"), fill_nop=True)
                else:
                    rom.patch(5, 0x0CD7, ASM("ld [$DB44], a"), "", fill_nop=True)

        # Patch the text that Tarin uses to give your shield back.
        rom.texts[0x54] = formatText(b"#####, it is dangerous to go alone!\nTake this!")
        rom.patch(5, 0x0CDE, ASM("ld a, $91"), ASM("ld a, $%02x" % (self.MESSAGE[option])))

        rom.patch(0x05, 0x0CAB, 0x0CB0, ASM("""
            ; Set the room status to finished.
            ld a, $20
            call $36C4
        """), fill_nop=True)

        # Instead of checking for the shield level to put you in the bed, check the room flag.
        rom.patch(0x05, 0x1202, ASM("ld a, [$DB44]\nand a"), ASM("ldh a, [$F8]\nand $20"))
        rom.patch(0x05, 0x0C6D, ASM("ld a, [$DB44]\nand a"), ASM("ldh a, [$F8]\nand $20"))

    def read(self, rom):
        value = rom.banks[5][0xCD1]
        for k, v in INVENTORY_MAP.items():
            if int(v, 16) == value:
                return k
        raise ValueError("Could not find start item contents in ROM (0x%02x)" % (value))
