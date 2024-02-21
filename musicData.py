import struct


class SongChannel:
    def __init__(self):
        self.blocks = []
        self.loop = None
        self.next = None
        self.addr = None


class Song:
    def __init__(self):
        self.initial_transpose = 0
        self.speed_data = b''
        self.channels = []


class MusicData:
    def __init__(self, rom, bank: int, table_addr: int, count: int):
        self._rb = rom.banks[bank]
        self.__bank = bank
        self.__table_addr = table_addr
        if bank == 0x1B:
            self.__blocks = [(0x4ED6, 0x8000 - 0x4ED6)]
        elif bank == 0x1E:
            self.__blocks = [(0x4DA9, 0x8000 - 0x4DA9)]
        else:
            self.__blocks = [(0x5000, 0x3000)]
        self.songs = []
        for n in range(count):
            ptr = self._rb[table_addr + n * 2]
            ptr |= self._rb[table_addr + n * 2 + 1] << 8
            #print(f"Song {n} {bank:x} {ptr:x}")
            self.songs.append(self._read_song(ptr))
        self._rb = None
        self.__blocks.sort()
        idx = 0
        while idx < len(self.__blocks) - 1:
            a0, s0 = self.__blocks[idx]
            a1, s1 = self.__blocks[idx+1]
            if a1 <= a0 + s0:
                self.__blocks[idx] = (a0, max(a0 + s0, a1 + s1) - a0)
                self.__blocks.pop(idx + 1)
            else:
                idx += 1
        # for a, s in self.__blocks:
        #     print(f"{a:04x} {a+s:04x}")

    def _get_block(self, addr, size):
        assert addr >= 0x4000
        self.__blocks.append((addr, size))
        return bytes(self._rb[addr-0x4000:addr-0x4000+size])

    def _get_ptr(self, addr):
        return struct.unpack("<H", self._get_block(addr, 2))[0]

    def _read_song(self, addr):
        block = self._get_block(addr, 11)
        initial_transpose, speeddata_ptr, channel_ptr1, channel_ptr2, channel_ptr3, channel_ptr4 = struct.unpack("<BHHHHH", block)
        song = Song()
        song.initial_transpose = initial_transpose
        song.speed_data = self._get_block(speeddata_ptr, 15)
        song.channels.append(self._read_channel_blocks(channel_ptr1, 1, {}))
        song.channels.append(self._read_channel_blocks(channel_ptr2, 2, {}))
        song.channels.append(self._read_channel_blocks(channel_ptr3, 3, {}))
        song.channels.append(self._read_channel_blocks(channel_ptr4, 4, {}))
        return song

    def _read_channel_blocks(self, base_addr, channel_type, done):
        if base_addr == 0:
            return None
        sc = SongChannel()
        addr = base_addr
        done[addr] = sc
        while True:
            data_ptr = self._get_ptr(addr)
            addr += 2
            if data_ptr == 0xFFFF:
                loop_ptr = self._get_ptr(addr)
                # This might loop into another song... (or loop to a loop that loops back to this)
                if loop_ptr < base_addr or loop_ptr > addr:
                    if loop_ptr not in done:
                        self._read_channel_blocks(loop_ptr, channel_type, done)
                    sc.next = done[loop_ptr]
                else:
                    sc.loop = (loop_ptr - base_addr) // 2
                break
            if data_ptr == 0x0000:
                break
            sc.blocks.append(self._read_channel_block(data_ptr, channel_type))
        return sc

    def _read_channel_block(self, base_addr, channel_type):
        block = []
        addr = base_addr
        while self._rb[addr-0x4000] != 0:
            if self._rb[addr-0x4000] == 0x9B: # Loop
                addr += 1
                block.append((0x9B, self._rb[addr-0x4000]))
            elif self._rb[addr-0x4000] == 0x9D and channel_type == 3: # Set waveform (channel 3)
                wave_ptr = self._get_ptr(addr + 1)
                wave_data = self._get_block(wave_ptr, 16)
                addr += 3
                block.append((0x9D, self._rb[addr-0x4000], wave_data))
            elif self._rb[addr-0x4000] == 0x9D: # Set envelope duty (channel 1/2)
                addr += 3
                block.append((0x9D, self._rb[addr-0x4000-2], self._rb[addr-0x4000-1], self._rb[addr-0x4000]))
            elif self._rb[addr-0x4000] == 0x9E: # Set speed
                addr += 2
                block.append((0x9E, self._rb[addr-0x4000-1], self._rb[addr-0x4000]))
            elif self._rb[addr-0x4000] == 0x9F: # Set transpose
                addr += 1
                block.append((0x9F, self._rb[addr-0x4000]))
            else:
                block.append((self._rb[addr-0x4000],))
            addr += 1
        self._get_block(base_addr, addr - base_addr + 1)
        return block

    def _alloc(self, size: int) -> int:
        for idx, (addr, bsize) in enumerate(self.__blocks):
            if size <= bsize:
                self.__blocks[idx] = (addr + size, bsize - size)
                return addr
        raise RuntimeError("Not enough space for song data")

    def store(self, rom):
        rb = rom.banks[self.__bank]
        _block_storage = {}
        def store_block(block: bytes) -> int:
            if block in _block_storage:
                return _block_storage[block]
            addr = self._alloc(len(block))
            rb[addr-0x4000:addr-0x4000+len(block)] = block
            _block_storage[block] = addr
            return addr
        def store_channel(channel, channel_type):
            if channel is None:
                return 0
            if channel.addr is not None:
                return channel.addr
            assert channel.loop is None or channel.next is None
            channel_data = b''
            for block in channel.blocks:
                bin_block = bytearray()
                for op in block:
                    if op[0] == 0x9D and channel_type == 3:
                        addr = store_block(op[2])
                        bin_block += struct.pack("<BHB", 0x9D, addr, op[1])
                    else:
                        for c in op:
                            bin_block.append(c)
                addr = store_block(bytes(bin_block))
                channel_data += struct.pack("<H", addr)
            if channel.loop is not None:
                channel_data += struct.pack('<HH', 0xFFFF, len(channel.blocks) - channel.loop)
                addr = store_block(channel_data)
                assert rb[addr+len(channel_data)-2-0x4000:addr+len(channel_data)-0x4000] in (struct.pack("<H", len(channel.blocks) - channel.loop), struct.pack("<H", addr + channel.loop * 2))
                rb[addr+len(channel_data)-2-0x4000:addr+len(channel_data)-0x4000] = struct.pack("<H", addr + channel.loop * 2)
            elif channel.next is not None:
                if channel.next.addr is not None:
                    channel_data += struct.pack('<HH', 0xFFFF, channel.next.addr)
                else:
                    channel_data += struct.pack('<HH', 0xFFFF, 0xFFFF)
                addr = store_block(channel_data)
                channel.addr = addr
                loop_addr = store_channel(channel.next, channel_type)
                assert rb[addr+len(channel_data)-2-0x4000:addr+len(channel_data)-0x4000] in (b'\xFF\xFF', struct.pack("<H", loop_addr)), rb[addr+len(channel_data)-2-0x4000:addr+len(channel_data)-0x4000]
                rb[addr+len(channel_data)-2-0x4000:addr+len(channel_data)-0x4000] = struct.pack("<H", loop_addr)
            else:
                channel_data += b'\x00\x00'
                addr = store_block(channel_data)
            channel.addr = addr
            return addr
        for sidx, song in enumerate(self.songs):
            speed_ptr = store_block(song.speed_data)
            ptr1 = store_channel(song.channels[0], 1)
            ptr2 = store_channel(song.channels[1], 2)
            ptr3 = store_channel(song.channels[2], 3)
            ptr4 = store_channel(song.channels[3], 4)
            baddr = store_block(struct.pack("<BHHHHH", song.initial_transpose, speed_ptr, ptr1, ptr2, ptr3, ptr4))
            rb[self.__table_addr + sidx * 2:self.__table_addr + sidx * 2+2] = struct.pack("<H", baddr)
        # for a, s in self.__blocks:
        #     print(f"{a:04x} {a+s:04x} ({s})")


if __name__ == "__main__":
    import rom
    r = rom.ROM(open("input.gbc", "rb"))
    a = MusicData(r, 0x1B, 0x0077, 0x30)
    b = MusicData(r, 0x1E, 0x007F, 0x40)
    a.store(r)
    b.store(r)
