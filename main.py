from rom import ROM
from pointerTable import PointerTable
from assembler import ASM
import randomizer
import patches.core
import patches.bowwow
import patches.desert
import patches.owl
import locations.itemInfo
import explorer
import logic


class Texts(PointerTable):
    END_OF_DATA = (0xfe, 0xff)

    def __init__(self, rom):
        super().__init__(rom, {
            "count": 0x2B0,
            "pointers_addr": 1,
            "pointers_bank": 0x1C,
            "banks_addr": 0x741,
            "banks_bank": 0x1C,
        })

        # I think it is safe to expand the storage to the end of the bank for each of the storage areas,
        # as the rest of the bank seems unused.
        # However, as we reduce the amount of text, this is not really needed.
        #for bank in self.storage:
        #    rom.banks[bank] = (self.storage[bank][1], 0x4000)


class Entities(PointerTable):
    def __init__(self, rom):
        super().__init__(rom, {
            "count": 0x320,
            "pointers_addr": 0,
            "pointers_bank": 0x16,
            "data_bank": 0x16,
        })

class RoomsTable(PointerTable):
    HEADER = 2

    def _readData(self, rom, bank_nr, pointer):
        bank = rom.banks[bank_nr]
        start = pointer
        pointer += self.HEADER
        while bank[pointer] != 0xFE:
            obj_type = (bank[pointer] & 0xF0)
            if obj_type == 0xE0:
                pointer += 5
            elif obj_type == 0xC0 or obj_type == 0x80:
                pointer += 3
            else:
                pointer += 2
        pointer += 1
        self._addStorage(bank_nr, start, pointer)
        return bank[start:pointer]


class RoomsOverworldTop(RoomsTable):
    def __init__(self, rom):
        super().__init__(rom, {
            "count": 0x080,
            "pointers_addr": 0x000,
            "pointers_bank": 0x09,
            "data_bank": 0x09,
        })


class RoomsOverworldBottom(RoomsTable):
    def __init__(self, rom):
        super().__init__(rom, {
            "count": 0x080,
            "pointers_addr": 0x100,
            "pointers_bank": 0x09,
            "data_bank": 0x1A,
        })


class RoomsIndoorA(RoomsTable):
    # TODO: The color dungeon tables are in the same bank, but the pointer table is after the room data.
    def __init__(self, rom):
        super().__init__(rom, {
            "count": 0x100,
            "pointers_addr": 0x000,
            "pointers_bank": 0x0A,
            "data_bank": 0x0A,
        })


class RoomsIndoorB(RoomsTable):
    # Most likely, this table can be expanded all the way to the end of the bank,
    # giving a few 100 extra bytes to work with.
    def __init__(self, rom):
        super().__init__(rom, {
            "count": 0x0FF,
            "pointers_addr": 0x000,
            "pointers_bank": 0x0B,
            "data_bank": 0x0B,
        })


if __name__ == "__main__":
    import sys
    assert sys.argv[1] != sys.argv[2]
    rom = ROM(sys.argv[1])

    # Ability to patch any text in the game with different text
    rom.texts = Texts(rom)
    rom.entities = Entities(rom)
    rom.rooms_overworld_top = RoomsOverworldTop(rom)
    rom.rooms_overworld_bottom = RoomsOverworldBottom(rom)
    rom.rooms_indoor_a = RoomsIndoorA(rom)
    rom.rooms_indoor_b = RoomsIndoorB(rom)

    patches.core.noSwordMusic(rom)
    patches.core.chestForSword(rom)
    patches.core.removeGhost(rom)
    patches.core.removeBirdKeyDrop(rom)
    patches.bowwow.neverGetBowwow(rom)
    patches.desert.desertAccess(rom)
    patches.owl.removeOwlEvents(rom)

    ## Monkey bridge patch
    rom.patch(0x00, 0x3334, ASM("bit 4, e\njr Z, $05"), ASM("nop\nnop\nnop\nnop"))

    # Remove low health beep (remove loading the SFX)
    rom.patch(2,  0x235b, ASM("ld hl, $FFF3\nld [hl], $04"), ASM("nop\nnop\nnop\nnop\nnop"))

    # Never allow stealing (always acts as if you do not have a sword)
    #rom.patch(4, 0x36F9, "FA4EDB", "3E0000")
    # Always allow stealing (even without a sword)
    rom.patch(4, 0x36F9, "FA4EDB", "3E0100")

    # Into text from Marin. Got to go fast, so less text. (This intro text is very long)
    rom.texts[0x01] = b"Let^sa go!\xff"

    # Reduce length of a bunch of common texts
    rom.texts[0xEA] = b"You've got a    " + b"Guardian Acorn!\xff"
    rom.texts[0xEB] = rom.texts[0xEA]
    rom.texts[0xEC] = rom.texts[0xEA]
    rom.texts[0x08] = b"You got a Piece " + b"of Power!\xff"
    rom.texts[0xEF] = b"You found a     " + b"Secret Seashell!\xff"
    rom.texts[0xA7] = b"You've got the  " + b"Compass!\xff"

    test_logic = True
    if test_logic:
        for ii in locations.itemInfo.ItemInfo.all:
            ii.item = ii.read(rom)
            ii.patch(rom, ii.item)
        e = explorer.Explorer()
        e.visit(logic.start)
        e.dump()
    else:
        while True:
            try:
                randomizer.Randomizer(rom)
                break
            except randomizer.Error:
                print("Failed, trying again.")

    #rom.patch(0, 0x0003, "00", "01") # DEBUG SAVE PATCH

    rom.texts.store(rom)
    rom.entities.store(rom)
    # Note: Changing the overworld also requires updating the GBC overlays.
    rom.rooms_overworld_top.store(rom)
    rom.rooms_overworld_bottom.store(rom)
    rom.rooms_indoor_a.store(rom)
    rom.rooms_indoor_b.store(rom)
    rom.save(sys.argv[2], name="TEST")
