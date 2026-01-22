import struct
import binascii
from typing import Optional, List

OP_END = 0x00
OP_REST = 0x01
OP_LOOP_START = 0x9B
OP_LOOP_END = 0x9C
OP_ENABLE_UNKNOWN1 = 0x95
OP_DISABLE_UNKNOWN1 = 0x96
OP_ENABLE_UNKNOWN2 = 0x97
OP_DISABLE_UNKNOWN2 = 0x98
OP_ENABLE_UNKNOWN3 = 0x99
OP_DISABLE_UNKNOWN3 = 0x9A
OP_SET_INSTRUMENT = 0x9D
OP_SET_SPEED_DATA = 0x9E
OP_SET_TRANSPOSE = 0x9F
OP_COMMENT = 0x100  # virtual opcode

def noteToString(channel_idx, note):
    if note is None:
        return "   "
    if channel_idx == 3:
        return f"N{note:02x}"
    assert 2 <= note <= 0x90
    assert (note & 1) == 0
    octave = note // 24
    note = ["C_",  "C#", "D_", "D#", "E_", "F_", "F#", "G_", "G#", "A_", "A#", "B_"][(note // 2) % 12]
    return f"{note}{octave+1}"


class SongBlock:
    def __init__(self, addr):
        self.addr = addr
        self.ops = []
    
    def oopsAllRest(self):
        for op in self.ops:
            if op[0] not in {OP_REST, OP_LOOP_START, OP_LOOP_END, OP_SET_INSTRUMENT} and (op[0] < 0xA0 or op[0] > 0xAF):
                return False
        return True


class SongChannel:
    def __init__(self):
        self.blocks = []
        self.loop = None
        self.next = None
        self.addr = None

    def oopsAllRest(self):
        for block in self.blocks:
            if not block.oopsAllRest():
                return False
        return True


class Song:
    def __init__(self):
        self.initial_transpose = 0
        self.speed_data = b''
        self.channels = []


class SongPlayback:
    def __init__(self, song: Song):
        self.transpose = song.initial_transpose
        self.delay = [0, 0, 0, 0]
        self.speed_data = song.speed_data
        self.channel = [None if channel is None or channel.oopsAllRest() else channel for channel in song.channels]
        self.speed = [0, 0, 0, 0]
        self.block_index = [0, 0, 0, 0]
        self.block_offset = [0, 0, 0, 0]
        self.loop_start: List[Optional[int]] = [None, None, None, None]
        self.loop_count: List[Optional[int]] = [None, None, None, None]

        if self.transpose:
            raise NotImplementedError("Transpose not implemented")
        if self.channel[3]:
            raise NotImplementedError("Channel 4 not implemented")

    def step(self, callback) -> int:
        for channel_idx in range(4):
            if self.channel[channel_idx] is None:
                self.delay[channel_idx] = 256
            while self.delay[channel_idx] == 0:
                if self.block_offset[channel_idx] == len(self.channel[channel_idx].blocks[self.block_index[channel_idx]].ops):
                    callback(-1, 0, (OP_COMMENT, f"End of block for channel {channel_idx+1} ({self.channel[channel_idx].blocks[self.block_index[channel_idx]].addr:04x})"))
                    self.block_index[channel_idx] += 1
                    self.block_offset[channel_idx] = 0
                    if self.block_index[channel_idx] == len(self.channel[channel_idx].blocks):
                        if self.channel[channel_idx].next is not None:
                            raise NotImplementedError("Move to next not implemented")
                        if self.channel[channel_idx].loop is not None:
                            callback(-1, 0, (OP_COMMENT, f"Channel {channel_idx+1} loop to: {self.channel[channel_idx].blocks[self.channel[channel_idx].loop].addr:04x}"))
                        self.channel[channel_idx] = None
                        break
                op = self.channel[channel_idx].blocks[self.block_index[channel_idx]].ops[self.block_offset[channel_idx]]
                if op[0] not in {OP_SET_SPEED_DATA, OP_LOOP_START, OP_LOOP_END} and (op[0] < 0xA0 or op[0] > 0xAF):
                    callback(channel_idx, self.speed[channel_idx], op)
                self.block_offset[channel_idx] += 1
                if 0x01 <= op[0] <= 0x90: # A note or rest
                    self.delay[channel_idx] = self.speed[channel_idx]
                elif 0xA0 <= op[0] <= 0xAF: # notlen
                    self.speed[channel_idx] = self.speed_data[op[0] & 0x0F]
                elif op[0] == OP_SET_INSTRUMENT:
                    pass
                elif op[0] == OP_SET_SPEED_DATA:
                    self.speed_data = op[1]
                elif op[0] in {0x99, 0x9A}:
                    pass
                elif op[0] == OP_LOOP_START:
                    self.loop_start[channel_idx] = self.block_offset[channel_idx]
                    self.loop_count[channel_idx] = op[1]
                elif op[0] == OP_LOOP_END:
                    self.loop_count[channel_idx] -= 1
                    if self.loop_count[channel_idx] != 0:
                        self.block_offset[channel_idx] = self.loop_start[channel_idx]
                else:
                    raise NotImplementedError(f"Not implemented opcode: {channel_idx}: {op[0]:02x}: {op}")
        time_pass = min(self.delay)
        self.delay = [d - time_pass for d in self.delay]
        return time_pass

    def isFinished(self):
        for channel in self.channel:
            if channel is not None:
                return False
        return True


class LADXMExporter:
    def __init__(self, song: Song, filename: str):
        sp = SongPlayback(song)
        pattern = []
        pulse_instruments = []
        wave_instruments = []
        timestep = 0
        while not sp.isFinished():
            def f(channel_idx, length, op):
                if op[0] == OP_SET_INSTRUMENT:
                    if channel_idx == 2:
                        if op not in wave_instruments:
                            wave_instruments.append(op)
                    elif op not in pulse_instruments:
                        pulse_instruments.append(op)
                pattern.append((timestep, channel_idx, length, op))
            timestep += sp.step(f)
        pattern.append((timestep, 4, 0, (OP_END, )))

        f = open(filename, "wt")
        f.write("version: 1\n")
        for instrument_index, instrument in enumerate(pulse_instruments):
            length = 0x3F - instrument[3] & 0x3F
            duty = instrument[3] >> 6
            volume = instrument[1] >> 4
            env_dir_inc = "-" if (instrument[1] & 0x08) == 0 else "+"
            env_pace = instrument[1] & 0x07
            f.write(f"pulse_instrument: length: {length} duty: {duty} volume: {volume} vol_change: {env_dir_inc}{env_pace} unk1: {instrument[2]}\n")
        for instrument_index, instrument in enumerate(wave_instruments):
            f.write(f"wave_instrument: {binascii.hexlify(instrument[2]).decode('ascii')} unk1: {instrument[1]}\n")
        f.write("sequence:\n")
        f.write("  intro\n")
        f.write("  main\n")
        f.write("pattern: intro\n")
        f.write("pattern: main\n")
        pattern.sort(key=lambda p: (p[0], p[1], -p[3][0]))
        for timestep, channel_idx, length, op in pattern:
            if 0x02 <= op[0] <= 0x90 or (op[0] == 0x01 and channel_idx == 3): # A note to play
                f.write(f"  {timestep:04} {channel_idx+1} {noteToString(channel_idx, op[0])} {length}\n")
            elif op[0] == 0x01:
                pass # Ignore rests
            else:
                f.write(f"  {timestep:04} {channel_idx+1} ")
                if op[0] == OP_SET_INSTRUMENT:
                    if channel_idx == 2:
                        f.write(f"={wave_instruments.index(op):02}")
                    else:
                        f.write(f"={pulse_instruments.index(op):02}")
                elif op[0] == OP_ENABLE_UNKNOWN3:
                    f.write(f"+U3")
                elif op[0] == OP_DISABLE_UNKNOWN3:
                    f.write(f"-U3")
                elif op[0] == OP_COMMENT:
                    f.write(op[1])
                elif op[0] == OP_END:
                    f.write("END")
                else:
                    raise NotImplementedError(hex(op[0]))
                f.write("\n")
        f.close()


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
        #     print(f"{a:04x} {a+s:04x} ({s})")

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

    def _read_channel_block(self, base_addr, channel_type) -> SongBlock:
        block = SongBlock(base_addr)
        addr = base_addr
        while self._rb[addr-0x4000] != 0:
            if self._rb[addr-0x4000] == OP_LOOP_START: # Loop
                addr += 1
                block.ops.append((OP_LOOP_START, self._rb[addr-0x4000]))
            elif self._rb[addr-0x4000] == OP_SET_INSTRUMENT and channel_type == 3: # Set waveform (channel 3)
                wave_ptr = self._get_ptr(addr + 1)
                wave_data = self._get_block(wave_ptr, 16)
                addr += 3
                block.ops.append((OP_SET_INSTRUMENT, self._rb[addr-0x4000], wave_data))
            elif self._rb[addr-0x4000] == OP_SET_INSTRUMENT: # Set envelope duty (channel 1/2)
                addr += 3
                block.ops.append((OP_SET_INSTRUMENT, self._rb[addr-0x4000-2], self._rb[addr-0x4000-1], self._rb[addr-0x4000]))
            elif self._rb[addr-0x4000] == OP_SET_SPEED_DATA: # Set speed
                speed_ptr = self._get_ptr(addr + 1)
                speed_data = self._get_block(speed_ptr, 16)
                addr += 2
                block.ops.append((OP_SET_SPEED_DATA, speed_data))
            elif self._rb[addr-0x4000] == OP_SET_TRANSPOSE: # Set transpose
                addr += 1
                block.ops.append((OP_SET_TRANSPOSE, self._rb[addr-0x4000]))
            else:
                block.ops.append((self._rb[addr-0x4000],))
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
                for op in block.ops:
                    if op[0] == OP_SET_INSTRUMENT and channel_type == 3: # Waveform special case which has a pointer
                        addr = store_block(op[2])
                        bin_block += struct.pack("<BHB", OP_SET_INSTRUMENT, addr, op[1])
                    elif op[0] == OP_SET_SPEED_DATA:
                        addr = store_block(op[1])
                        bin_block += struct.pack("<BH", OP_SET_SPEED_DATA, addr)
                    else:
                        for c in op:
                            bin_block.append(c)
                bin_block.append(0)
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


def main():
    import rom
    r = rom.ROM(open("input.gbc", "rb"))
    a = MusicData(r, 0x1B, 0x0077, 0x30)
    b = MusicData(r, 0x1E, 0x007F, 0x40)
    a.store(r)
    b.store(r)

    for name, md in [("a", a), ("b", b)]:
        for song_idx, song in enumerate(md.songs):
            try:
                LADXMExporter(song, f"music/{name}_{song_idx:02}.ladxm")
            except NotImplementedError as e:
                print(f"NotImplementedError on song {name}_{song_idx}: {e}")


if __name__ == "__main__":
    main()
