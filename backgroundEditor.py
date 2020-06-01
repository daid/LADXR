
class BackgroundEditor:
    def __init__(self, rom, index, *, attributes=False):
        self.__index = index
        self.__is_attributes = attributes

        self.tiles = {}
        if attributes:
            data = rom.background_attributes[index]
        else:
            data = rom.background_tiles[index]
        idx = 0
        while data[idx] != 0x00:
            addr = data[idx] << 8 | data[idx + 1]
            amount = (data[idx + 2] & 0x3F) + 1
            repeat = (data[idx + 2] & 0x40) == 0x40
            vertical = (data[idx + 2] & 0x80) == 0x80
            idx += 3
            for n in range(amount):
                self.tiles[addr] = data[idx]
                if not repeat:
                    idx += 1
                addr += 0x20 if vertical else 0x01
            if repeat:
                idx += 1

    def dump(self):
        if not self.tiles:
            return
        low = min(self.tiles.keys()) & 0xFFE0
        high = (max(self.tiles.keys()) | 0x001F) + 1
        print(hex(self.__index))
        for addr in range(low, high, 0x20):
            print("%04x " % (addr) + "".join(map(lambda n: ("%02X" % (self.tiles[addr + n])) if addr + n in self.tiles else "  ", range(0x20))))

    def store(self, rom):
        # NOTE: This is not a very good encoder, but the background back has so much free space that we really don't care.
        # Improvements can be done to find long sequences of bytes and store those as repeated.
        result = bytearray()
        low = min(self.tiles.keys())
        high = max(self.tiles.keys()) + 1
        while low < high:
            if low not in self.tiles:
                low += 1
                continue
            count = 1
            while low + count in self.tiles and count < 255:
                count += 1
            result.append(low >> 8)
            result.append(low & 0xFF)
            result.append(count - 1)
            for n in range(count):
                result.append(self.tiles[low + n])
            low += count
        result.append(0x00)
        if self.__is_attributes:
            rom.background_attributes[self.__index] = result
        else:
            rom.background_tiles[self.__index] = result
