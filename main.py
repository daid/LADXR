import binascii
from rom import ROM
from pointerTable import PointerTable
from assembler import ASM
import randomizer
import patches.core
import patches.bowwow
import patches.desert
import patches.owl
import patches.titleScreen
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


class BackgroundTable(PointerTable):
    def _readData(self, rom, bank_nr, pointer):
        # Ignore 2 invalid pointers.
        if pointer in (0, 0x1651):
            return bytearray()

        mem = {}
        bank = rom.banks[bank_nr]
        start = pointer
        while bank[pointer] != 0x00:
            addr = bank[pointer] << 8 | bank[pointer + 1]
            amount = (bank[pointer + 2] & 0x3F) + 1
            repeat = (bank[pointer + 2] & 0x40) == 0x40
            vertical = (bank[pointer + 2] & 0x80) == 0x80
            pointer += 3
            for n in range(amount):
                mem[addr] = bank[pointer]
                if not repeat:
                    pointer += 1
                addr += 0x20 if vertical else 0x01
            if repeat:
                pointer += 1
        pointer += 1
        self._addStorage(bank_nr, start, pointer)

        if mem:
            low = min(mem.keys()) & 0xFFE0
            high = (max(mem.keys()) | 0x001F) + 1
            print(hex(start))
            for addr in range(low, high, 0x20):
                print("".join(map(lambda n: ("%02X" % (mem[addr + n])) if addr + n in mem else "  ", range(0x20))))
        return bank[start:pointer]


class BackgroundTilesTable(BackgroundTable):
    def __init__(self, rom):
        super().__init__(rom, {
            "count": 0x25,
            "pointers_addr": 0x052D,
            "pointers_bank": 0x20,
            "data_bank": 0x08,
            "expand_to_end_of_bank": True
        })


class BackgroundAttributeTable(BackgroundTable):
    def __init__(self, rom):
        super().__init__(rom, {
            "count": 0x25,
            "pointers_addr": 0x1C4D,
            "pointers_bank": 0x24,
            "data_bank": 0x24,
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
    #rom.background_tiles = BackgroundTilesTable(rom)
    #rom.background_attributes = BackgroundAttributeTable(rom)

    patches.core.noSwordMusic(rom)
    patches.core.chestForSword(rom)
    patches.core.removeGhost(rom)
    patches.core.removeBirdKeyHoleDrop(rom)
    patches.core.alwaysAllowSecretBook(rom)
    patches.core.cleanup(rom)
    patches.bowwow.neverGetBowwow(rom)
    patches.desert.desertAccess(rom)
    patches.owl.removeOwlEvents(rom)

    # Show marin outside, even without a sword.
    rom.patch(0x05, 0x0E78, ASM("ld a, [$DB4E]"), ASM("ld a, $01"), fill_nop=True)
    # Make marin ignore the fact that you did not save the racoon
    rom.patch(0x05, 0x0E87, ASM("ld a, [$D808]"), ASM("ld a, $10"), fill_nop=True)
    rom.patch(0x05, 0x0F73, ASM("ld a, [$D808]"), ASM("ld a, $10"), fill_nop=True)
    rom.patch(0x05, 0x0FB0, ASM("ld a, [$DB48]"), ASM("ld a, $01"), fill_nop=True)
    # Show marin in the animal village
    rom.patch(0x03, 0x0a84, ASM("ld a, [$DB74]"), ASM("ld a, $01"), fill_nop=True)

    ## Monkey bridge patch, always have the bridge there.
    rom.patch(0x00, 0x3334, ASM("bit 4, e\njr Z, $05"), b"", fill_nop=True)

    # Remove "this object is heavy, bla bla", and other nag messages when touching an object
    rom.patch(0x02, 0x2ba6, ASM("ld a, [$C5A6]\nand a"), ASM("ld a, $01\nand a"), fill_nop=True)
    rom.patch(0x02, 0x3314, ASM("ld a, [$C5A6]\nand a"), ASM("ld a, $01\nand a"), fill_nop=True)

    # Low health beep patches
    rom.patch(2,  0x2359, ASM("ld a, $30"), ASM("ld a, $60")) # slow slow hp beep
    #rom.patch(2,  0x235b, ASM("ld hl, $FFF3\nld [hl], $04"), b"", fill_nop=True) # Remove health beep

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
        seed = "DEFAULT"
        for ii in locations.itemInfo.ItemInfo.all:
            ii.item = ii.read(rom)
            ii.patch(rom, ii.item)
        e = explorer.Explorer()
        e.visit(logic.start)
        e.dump()

        from locations import Chest
        Chest(0x2F2).patch(rom, "GOLD_LEAF")
        print(hex(rom.banks[0x14][0x1D2]))
        rom.banks[0x14][0x1D2] = 0x61
        from roomEditor import RoomEditor, Object
        re = RoomEditor(rom, 0x2D2)
        re.objects.append(Object(8, 2, 0xA1))
        re.store(rom)
        re = RoomEditor(rom, 0x114)
        for obj in re.objects:
            print(obj)
    else:
        retry_count = 0
        while True:
            try:
                seed = randomizer.Randomizer(rom).seed
                seed = binascii.hexlify(seed).decode("ascii").upper()
                break
            except randomizer.Error:
                retry_count += 1
                print("Failed, trying again: %d" % (retry_count))

    rom.patch(0, 0x0003, "00", "01")  # DEBUG SAVE PATCH

    rom.texts.store(rom)
    rom.entities.store(rom)
    rom.rooms_overworld_top.store(rom)
    rom.rooms_overworld_bottom.store(rom)
    rom.rooms_indoor_a.store(rom)
    rom.rooms_indoor_b.store(rom)

    import binascii
    print("Seed: %s" % (seed))
    patches.titleScreen.setRomInfo(rom, seed[16:], seed[:16])

    #rom.background_tiles.store(rom)
    #rom.background_attributes.store(rom)
    rom.save(sys.argv[2], name=seed)
