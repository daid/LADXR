import binascii
import struct
b2h = binascii.hexlify
h2b = binascii.unhexlify

class ROM:
    def __init__(self, filename):
        data = open(filename, "rb").read()
        assert len(data) == 1024 * 1024
        self.banks = []
        for n in range(0x40):
            self.banks.append(bytearray(data[n*16*1024:(n+1)*16*1024]))

    def patch(self, bank_nr, addr, old, new):
        old = h2b(old)
        new = h2b(new)
        assert len(old) == len(new)
        assert addr >= 0 and addr + len(old) <= 16*1024
        bank = self.banks[bank_nr]
        if bank[addr:addr+len(old)] != old:
            print("Bank data:")
            print(b2h(bank))
            loc = bank.find(old)
            while loc > -1:
                print("Possible at:", hex(loc))
                loc = bank.find(old, loc+1)
            assert False, "Patch mismatch: %s != %s" % (b2h(bank[addr:addr+len(old)]), b2h(old))
        bank[addr:addr+len(old)] = new

    def save(self, filename):
        f = open(filename, "wb")
        self.banks[0][0x14E] = 0
        self.banks[0][0x14F] = 0
        checksum = 0
        for bank in self.banks:
            checksum = (checksum + sum(bank)) & 0xFFFF
        self.banks[0][0x14E] = checksum >> 8
        self.banks[0][0x14F] = checksum & 0xFF
        for bank in self.banks:
            f.write(bank)
        f.close()
        print("Saved:", filename)

class Texts:
    def __init__(self, rom):
        count = 0x2B0
        pointers = rom.banks[0x1C][1:1+count*2]
        banks = rom.banks[0x1C][0x741:0x741+count]

        self.strings = []
        self.storage = {}
        self.banks = []

        for n in range(count):
            bank = banks[n] & 0x3f
            pointer = pointers[n*2] | pointers[n*2+1] << 8
            pointer &= 0x3fff
            self.strings.append(self._readString(rom, bank, pointer))
            self.banks.append(bank)

        # I think it is safe to expand the storage to the end of the bank for each of the storage areas,
        # as the rest of the bank seems unused.
        # However, as we reduce the amount of text, this is not really needed.
        #for bank in self.storage:
        #    rom.banks[bank] = (self.storage[bank][1], 0x4000)

    def __setitem__(self, key, value):
        self.strings[key] = value

    def store(self, rom):
        pointers = []
        storage = self.storage.copy()

        done = {}
        for n, s in enumerate(self.strings):
            bank = self.banks[n]
            if (bank, s) in done:
                pointer = pointers[done[(bank, s)]]
            else:
                assert storage[bank][1] - storage[bank][0] >= len(s), "Not enough room in bank %s" % (bank)
                pointer = storage[bank][0]
                storage[bank] = (pointer + len(s), storage[bank][1])
                rom.banks[bank][pointer:pointer+len(s)] = s
                done[(bank, s)] = n

            pointers.append(pointer)
            rom.banks[0x1C][0x741+n] = bank | (rom.banks[0x1C][0x741+n] & 0x80)
            rom.banks[0x1C][1+n*2] = pointer & 0xff
            rom.banks[0x1C][2+n*2] = ((pointer >> 8) & 0xff) | 0x40

    def _readString(self, rom, bank_nr, pointer):
        bank = rom.banks[bank_nr]
        start = pointer
        while bank[pointer] not in (0xfe, 0xff):
            pointer += 1
        pointer += 1
        self._addStorage(bank_nr, start, pointer)
        return bytes(bank[start:pointer])

    def _addStorage(self, bank, start, end):
        if bank not in self.storage:
            self.storage[bank] = (start, end)
        else:
            if self.storage[bank][0] <= start and self.storage[bank][1] == end:
                return
            assert self.storage[bank][1] == start or self.storage[bank][1] == start - 1
            self.storage[bank] = (self.storage[bank][0], end)

if __name__ == "__main__":
    import sys
    rom = ROM(sys.argv[1])

    # Ability to patch any text in the game with different text
    texts = Texts(rom)

    # Skip no-sword music override (replace specific jump calls with nops)
    rom.patch(2, 0x155, "CAA241", "000000")
    rom.patch(2, 0x3B46, "2841", "0000")

    # Remove the owl, just do not run its event (this might break something)
    # Note, this gives quite a bit of room for possible custom code to be located instead of the owl code.
    rom.patch(6, 0x27F7, "79EA01C5", "C9C9C9C9")

    # Never allow stealing (always acts as if you do not have a sword)
    rom.patch(4, 0x36F9, "FA4EDB", "3E0000")
    # Always allow stealing (even without a sword)
    #rom.patch(4, 0x36F9, "FA4EDB", "3E0100")

    # Change which item you get at the start.
    # (NOTE: This also sets the shield level to 1)
    # Giving a sword here, gives a lvl0 sword. Which... does no damage.
    rom.patch(5, 0xCD1, "04", "03")
    rom.patch(5, 0xCC6, "86", "82") # patch shield that icon that is shown.
    # Patch the text that Tarin uses to give your shield back.
    texts[0x54] = b"#####, is it    " \
                + b"dangerous to go " \
                + b"alone, take this\xff"
    texts[0x91] = b"Got the         " \
                + b"Power Bracelet!\xff"

    # Into text from Marin. Gota go fast, so less text.
    texts[0x01] = b"Let^sa go!\xff"

    texts.store(rom)
    rom.save(sys.argv[2])
