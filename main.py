import location
from rom import ROM
from pointerTable import PointerTable
import randomizer
from roomEditor import RoomEditor
import patches.core


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

    # Always have the boomerang trade guy enabled.
    rom.patch(0x19, 0x05EC, "FA0EDBFE0E", "3E0E00FE0E")  # show the guy
    rom.patch(0x00, 0x3190, "FA0EDBFE0E", "3E0E00FE0E")  # load the proper room loyout

    # Remove the owl, just do not run its event (this might break something)
    # Note, this gives quite a bit of room for possible custom code to be located instead of the owl code.
    rom.patch(6, 0x27F7, "79EA01C5", "C9000000")

    ### BowWow patches
    rom.patch(0x03, 0x1DFE, "EA56DB", "000000") # Do not mark BowWow as kidnapped after we complete dungeon 1.
    rom.patch(0x15, 0x06B6, "FA56DBFE80C2", "FA56DBFE80CA")  # always load the moblin boss
    rom.patch(0x03, 0x1824, "FA56DBFE80C2", "FA56DBFE80CA")  # always load the cave moblins
    rom.patch(0x07, 0x3983, "FA56DBFE80C2", "FA56DBFE80CA")  # always load the cave moblin with sword
    # TODO: Do something at the end of the bowwow cave, maybe place a chest there?

    # Basic patch to have the swamp flowers delete themselves directly.
    #  Could also patch to jump to the code area of the owl, and have some custom condition coded there.
    #  Which is why we didn't just delete the entities from the rooms.
    rom.patch(0x20, 0x7C * 3, "B56206", "843f00")
    rom.patch(0x20, 0x7e * 3, "FE6306", "843f00")

    ## Ghost patch
    rom.patch(0x03, 0x1E0A, "EA79DB", "000000")  # Do not have the ghost follow you after dungeon 4

    ## Monkey bridge patch
    rom.patch(0x00, 0x3334, "CB632805", "00000000")  # Do not have the ghost follow you after dungeon 4

    # Remove low health beep
    #rom.patch(2,  0x233D, "3604", "0000")

    # Never allow stealing (always acts as if you do not have a sword)
    #rom.patch(4, 0x36F9, "FA4EDB", "3E0000")
    # Always allow stealing (even without a sword)
    rom.patch(4, 0x36F9, "FA4EDB", "3E0100")

    # Into text from Marin. Gota go fast, so less text.
    rom.texts[0x01] = b"Let^sa go!\xff"

    # Reduce length of a bunch of common texts
    rom.texts[0xEA] = b"You've got a    " + b"Guardian Acorn!\xff"
    rom.texts[0xEB] = rom.texts[0xEA]
    rom.texts[0xEC] = rom.texts[0xEA]
    rom.texts[0x08] = b"You got a Piece " + b"of Power!\xff"
    rom.texts[0xEF] = b"You found a     " + b"Secret Seashell!\xff"

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
    rom.save(sys.argv[2])
