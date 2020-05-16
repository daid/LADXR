import binascii

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
        assert len(old) == len(new), "Length mismatch: %d != %d" % (len(old), len(new))
        assert addr >= 0 and addr + len(old) <= 16*1024
        bank = self.banks[bank_nr]
        if bank[addr:addr+len(old)] != old:
            print("Bank data:")
            print(b2h(bank))
            loc = bank.find(old)
            while loc > -1:
                print("Possible at:", hex(loc))
                loc = bank.find(old, loc+1)
            assert False, "Patch mismatch: %s != %s at 0x%04x" % (b2h(bank[addr:addr+len(old)]), b2h(old), addr)
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
