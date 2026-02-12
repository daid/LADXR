import random
import re
import struct
import binascii
from typing import Optional, List, Dict, Tuple, Any

OP_END = 0x00
OP_REST = 0x01
OP_NOTE_MIN = 0x02
OP_NOTE_MAX = 0x90
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
OP_NOTELEN_0 = 0xA0
OP_NOTELEN_F = 0xAF
OP_NOISE_SPECIAL = 0xFF
OP_COMMENT = 0x100  # virtual opcode


def noteToString(channel_idx, note):
    if note is None:
        return "   "
    if channel_idx == 3:
        if note == OP_NOISE_SPECIAL:
            return "NFF"
        assert note >= 6, f"Odd noise note: {note:02x}"
        assert ((note - 1) % 5) == 0, f"Odd noise note: {note:02x}"
        return f"N{(note-1)//5:02}"
    assert 2 <= note <= OP_NOTE_MAX
    assert (note & 1) == 0
    octave = (note - 2) // 24
    note = ["C_",  "C#", "D_", "D#", "E_", "F_", "F#", "G_", "G#", "A_", "A#", "B_"][((note - 2) // 2) % 12]
    return f"{note}{octave+1}"


def noteFromString(channel_idx, data):
    assert len(data) == 3
    if channel_idx == 3:
        assert data[0] == "N"
        if data == "NFF":
            return OP_NOISE_SPECIAL
        return 1 + int(data[1:]) * 5
    else:
        octave = int(data[2]) - 1
        match data[:2]:
            case "C_": return 2 + octave * 24
            case "C#": return 4 + octave * 24
            case "D_": return 6 + octave * 24
            case "D#": return 8 + octave * 24
            case "E_": return 10 + octave * 24
            case "F_": return 12 + octave * 24
            case "F#": return 14 + octave * 24
            case "G_": return 16 + octave * 24
            case "G#": return 18 + octave * 24
            case "A_": return 20 + octave * 24
            case "A#": return 22 + octave * 24
            case "B_": return 24 + octave * 24
        raise ValueError(f"Cannot parse note: {data}")


def songOpsEqual(ops_a, ops_b) -> bool:
    if len(ops_a) != len(ops_b):
        return False
    for a, b in zip(ops_a, ops_b):
        if a != b:
            return False
    return True


def songOpsSize(ops):
    return sum(len(op) for op in ops)


def songPseudoOpsSize(ops):
    current_len = -1
    size = 0
    for op in ops:
        if op[0] < OP_NOTE_MAX:
            if op[1] == current_len:
                size += 1
            else:
                current_len = op[1]
                size += 2
        else:
            size += len(op)
    return size


def songOpsHasUnclosedLoop(ops):
    open_loop_count = 0
    for op in ops:
        if op[0] == OP_LOOP_START:
            open_loop_count += 1
        elif op[0] == OP_LOOP_END:
            open_loop_count -= 1
            if open_loop_count < 0:
                return True
    return open_loop_count != 0


class SongBlock:
    def __init__(self, addr):
        self.addr = addr
        self.ops = []
    
    def oopsAllRest(self):
        for op in self.ops:
            if op[0] not in {OP_REST, OP_LOOP_START, OP_LOOP_END, OP_SET_INSTRUMENT} and (op[0] < OP_NOTELEN_0 or op[0] > OP_NOTELEN_F):
                return False
        return True

    def dump(self):
        for op in self.ops:
            if op[0] == OP_REST:
                print(f"   REST")
            elif op[0] == OP_END:
                print(f"   END")
            elif op[0] == OP_LOOP_START:
                print(f"   LOOP {op[1]}")
            elif op[0] == OP_LOOP_END:
                print(f"   LOOPEND")
            elif OP_NOTELEN_0 <= op[0] <= OP_NOTELEN_F:
                print(f"   NoteLen: {op[0] & 0x0F}")
            elif op[0] < OP_NOTE_MAX and (op[0] & 1) == 0:
                print(f"   {noteToString(0, op[0])}")
            else:
                print(f"   {op}")


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

    def dump(self):
        print(f"  Loop: {self.loop}")
        for idx, block in enumerate(self.blocks):
            print(f"  Block: {idx}")
            block.dump()


class Song:
    def __init__(self):
        self.initial_transpose = 0
        self.speed_data = b''
        self.channels: List[Optional[SongChannel]] = []
    
    def dump(self):
        print("Song:")
        for idx, channel in enumerate(self.channels):
            print(f" Channel {idx}:")
            if channel:
                channel.dump()

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
                if op[0] not in {OP_SET_SPEED_DATA, OP_LOOP_START, OP_LOOP_END, OP_SET_TRANSPOSE} and (op[0] < OP_NOTELEN_0 or op[0] > OP_NOTELEN_F):
                    if OP_NOTE_MIN <= op[0] <= OP_NOTE_MAX and channel_idx != 3: # A note or rest, apply transpose
                        op = (op[0] + self.transpose, )
                        assert OP_NOTE_MIN <= op[0] <= OP_NOTE_MAX, "Note out of range after transpose?"
                    callback(channel_idx, self.speed[channel_idx], op)
                self.block_offset[channel_idx] += 1
                if OP_REST <= op[0] <= OP_NOTE_MAX: # A note or rest
                    self.delay[channel_idx] = self.speed[channel_idx]
                elif OP_NOTELEN_0 <= op[0] <= OP_NOTELEN_F: # notlen
                    self.speed[channel_idx] = self.speed_data[op[0] & 0x0F]
                elif op[0] == OP_NOISE_SPECIAL and channel_idx == 3:
                    self.delay[channel_idx] = self.speed[channel_idx]
                elif op[0] == OP_SET_INSTRUMENT:
                    pass
                elif op[0] == OP_SET_SPEED_DATA:
                    self.speed_data = op[1]
                elif op[0] == OP_SET_TRANSPOSE:
                    self.transpose = op[1]
                    if self.transpose & 0x80:
                        self.transpose = -(0x100 - self.transpose)
                elif op[0] in {OP_ENABLE_UNKNOWN1, OP_DISABLE_UNKNOWN1, OP_ENABLE_UNKNOWN2, OP_DISABLE_UNKNOWN2, OP_ENABLE_UNKNOWN3, OP_DISABLE_UNKNOWN3}:
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
        while not sp.isFinished() and timestep < 10000:
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
            assert (instrument[3] & 0x3F) in (0, 1, 3), f"Unexpected setting for pulse channel vibrato: {instrument[3] & 0x3F:02x}"
            vibrato = instrument[3] & 0x3F
            duty = instrument[3] >> 6
            volume = instrument[1] >> 4
            env_dir_inc = "-" if (instrument[1] & 0x08) == 0 else "+"
            env_pace = instrument[1] & 0x07
            f.write(f"pulse_instrument: vibrato: {vibrato} duty: {duty} volume: {volume} vol_change: {env_dir_inc}{env_pace} unk1: 0x{instrument[2]:02x}\n")
        for instrument_index, instrument in enumerate(wave_instruments):
            f.write(f"wave_instrument: {binascii.hexlify(instrument[2]).decode('ascii')} volume: {(instrument[1] >> 5) & 0x03} effect: 0x{instrument[1] & 0x9F:02x}\n")
        f.write("sequence:\n")
        f.write("  intro\n")
        f.write("  main\n")
        f.write("pattern: intro\n")
        f.write("pattern: main\n")
        pattern.sort(key=lambda p: (p[0], p[1], -p[3][0]))
        for timestep, channel_idx, length, op in pattern:
            if OP_NOTE_MIN <= op[0] <= OP_NOTE_MAX: # A note to play
                f.write(f"  {timestep:04} {channel_idx+1} {noteToString(channel_idx, op[0])} {length}\n")
            elif op[0] == OP_REST:
                pass # Ignore rests
            else:
                f.write(f"  {timestep:04} {channel_idx+1} ")
                if op[0] == OP_SET_INSTRUMENT:
                    if channel_idx == 2:
                        f.write(f"={wave_instruments.index(op):02}")
                    else:
                        f.write(f"={pulse_instruments.index(op):02}")
                elif op[0] == OP_ENABLE_UNKNOWN1:
                    f.write(f"+U1")
                elif op[0] == OP_DISABLE_UNKNOWN1:
                    f.write(f"-U1")
                elif op[0] == OP_ENABLE_UNKNOWN2:
                    f.write(f"+U2")
                elif op[0] == OP_DISABLE_UNKNOWN2:
                    f.write(f"-U2")
                elif op[0] == OP_ENABLE_UNKNOWN3:
                    f.write(f"+U3")
                elif op[0] == OP_DISABLE_UNKNOWN3:
                    f.write(f"-U3")
                elif op[0] == OP_COMMENT:
                    f.write(op[1])
                elif op[0] == OP_END:
                    f.write("END")
                elif op[0] == OP_NOISE_SPECIAL and channel_idx == 3:
                    f.write(f"NFF {length}")
                else:
                    raise NotImplementedError(f"Unknown opcode in export: {op[0]:02x}")
                f.write("\n")
        f.close()


class MusicData:
    def __init__(self, rom, bank: int, table_addr: int, count: int):
        self._rb = rom.banks[bank]
        self.__bank = bank
        self.__table_addr = table_addr
        if bank == 0x1B:
            self.__free_blocks = [(0x4ED6, 0x8000 - 0x4ED6)]
        elif bank == 0x1E:
            self.__free_blocks = [(0x4DA9, 0x8000 - 0x4DA9)]
        else:
            self.__free_blocks = [(0x5000, 0x3000)]
        self.songs = []
        for n in range(count):
            ptr = self._rb[table_addr + n * 2]
            ptr |= self._rb[table_addr + n * 2 + 1] << 8
            #print(f"Song {n} {bank:x} {ptr:x}")
            self.songs.append(self._read_song(ptr))
        self._rb = None
        self.__free_blocks.sort()
        idx = 0
        while idx < len(self.__free_blocks) - 1:
            a0, s0 = self.__free_blocks[idx]
            a1, s1 = self.__free_blocks[idx+1]
            if a1 <= a0 + s0:
                self.__free_blocks[idx] = (a0, max(a0 + s0, a1 + s1) - a0)
                self.__free_blocks.pop(idx + 1)
            else:
                idx += 1
        # for a, s in self.__free_blocks:
        #     print(f"{a:04x} {a+s:04x} ({s})")
        self.__over_spend_size = 0

    def free_space(self):
        return sum(size for start, size in self.__free_blocks)

    def _get_block(self, addr, size):
        assert addr >= 0x4000
        self.__free_blocks.append((addr, size))
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
        for idx, (addr, bsize) in enumerate(self.__free_blocks):
            if size <= bsize:
                self.__free_blocks[idx] = (addr + size, bsize - size)
                return addr
        addr = 0x4000 + self.__over_spend_size
        self.__over_spend_size += size
        return addr

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
        print(f"Song space total: {self.free_space()}")
        for sidx, song in enumerate(self.songs):
            before_store_space = self.free_space()
            speed_ptr = store_block(song.speed_data)
            ptr1 = store_channel(song.channels[0], 1)
            ptr2 = store_channel(song.channels[1], 2)
            ptr3 = store_channel(song.channels[2], 3)
            ptr4 = store_channel(song.channels[3], 4)
            baddr = store_block(struct.pack("<BHHHHH", song.initial_transpose, speed_ptr, ptr1, ptr2, ptr3, ptr4))
            rb[self.__table_addr + sidx * 2:self.__table_addr + sidx * 2+2] = struct.pack("<H", baddr)
            print(f"Song: 0x{sidx:02x}: ~size: {before_store_space - self.free_space()}")
        print(f"Song space left: {self.free_space()}")

        if self.__over_spend_size > 0:
            raise RuntimeError(f"Not enough space for song data in bank: 0x{self.__bank:02x}. Needed {self.__over_spend_size} more bytes.")


class LADXMImporter:
    def __init__(self):
        self._speed_table: List[int] = []
        # Store per channel/pattern name a list of blocks containing pseudo-song-ops
        self._patterns: Dict[Tuple[int, str], List[List[Any]]] = {}
        self._sequence: List[str] = []

    def _create_pattern(self, name: str):
        assert (0, name) not in self._patterns
        self._current_block = ([], [], [], [])
        self._current_time = [0, 0, 0, 0]
        for n in range(4):
            self._patterns[(n, name)] = [self._current_block[n]]

    def _rest_till(self, channel: int, frame_nr: int):
        time_delta = frame_nr - self._current_time[channel]
        while time_delta > 0:
            best_idx = -1
            for idx in range(16):
                if self._speed_table[idx] <= time_delta and (best_idx == -1 or self._speed_table[best_idx] < self._speed_table[idx]):
                    best_idx = idx
            self._current_block[channel].append((OP_REST, best_idx))
            time_delta -= self._speed_table[best_idx]
        self._current_time[channel] = frame_nr

    def _add(self, channel: int, frame_nr: int, opcode: Any):
        self._rest_till(channel, frame_nr)
        self._current_block[channel].append(opcode)

    def _is_all_rest(self, channel: int) -> bool:
        for (channel_idx, name), blocks in self._patterns.items():
            if channel != channel_idx:
                continue
            for block in blocks:
                for op in block:
                    if op[0] not in {OP_REST, OP_LOOP_START, OP_LOOP_END, OP_SET_INSTRUMENT}:
                        return False
        return True

    def load_ladxm(self, filename):
        assert not self._speed_table and not self._patterns
        # First load the ladxm file raw
        pulse_instruments = []
        wave_instruments = []
        patterns = {}

        lines = open(filename, "rt").readlines()
        while lines:
            line = lines.pop(0).rstrip()
            key, _, data = line.partition(":")
            data = data.strip()
            match key:
                case "version":
                    assert data == "1"
                case "pulse_instrument":
                    data = dict(re.findall(r"(\w+):\s+([\w\-]+)", data))
                    b1 = (int(data['volume']) << 4) | (abs(int(data['vol_change'])))
                    if int(data['vol_change']) > 0:
                        b1 |= 0x08
                    b3 = int(data['vibrato']) | (int(data['duty']) << 6)
                    pulse_instruments.append((OP_SET_INSTRUMENT, b1, int(data['unk1'], 0), b3))
                case "wave_instrument":
                    wave_data = data[:32]
                    data = dict(re.findall(r"(\w+):\s+([\w\-]+)", data[32:]))
                    b1 = (int(data['volume'], 0) << 5) | int(data['effect'], 0)
                    wave_instruments.append((OP_SET_INSTRUMENT, b1, binascii.unhexlify(wave_data)))
                case "sequence":
                    while lines and lines[0].startswith(" "):
                        self._sequence.append(lines.pop(0).strip())
                case "pattern":
                    pattern = []
                    patterns[data] = pattern
                    while lines and lines[0].startswith(" "):
                        line = lines.pop(0).strip().split()
                        frame_nr = int(line[0])
                        channel_nr = int(line[1])
                        if channel_nr < 1:  # ignore comments
                            continue
                        if len(line) > 3:
                            pattern.append((frame_nr, channel_nr - 1, line[2], int(line[3])))
                        else:
                            pattern.append((frame_nr, channel_nr - 1, line[2], 0))
                case _:
                    print(f"? {key}={data}")

        # Figure out our speed table.
        self._speed_table = []
        for pattern in patterns.values():
            for frame_nr, channel_nr, data, length in pattern:
                if length > 0 and length not in self._speed_table:
                    self._speed_table.append(length)
        while len(self._speed_table) < 16:
            add_value = 1
            while add_value in self._speed_table:
                add_value *= 2
                if add_value == 0x100:
                    add_value = 3
                if add_value == 0x180:
                    add_value = 5
            self._speed_table.append(add_value)
        assert len(self._speed_table) <= 16, "Too many entries in speed table."

        # Build patterns of blocks with pseudo ops
        for key, pattern in patterns.items():
            self._create_pattern(key)
            for frame_nr, channel_nr, data, length in pattern:
                if channel_nr < 0:
                    continue
                elif channel_nr == 4:
                    for n in range(4):
                        self._rest_till(n, frame_nr)
                elif data == "END":
                    pass
                elif data == "+U1":
                    self._add(channel_nr, frame_nr, (OP_ENABLE_UNKNOWN1,))
                elif data == "-U1":
                    self._add(channel_nr, frame_nr, (OP_DISABLE_UNKNOWN1,))
                elif data == "+U2":
                    self._add(channel_nr, frame_nr, (OP_ENABLE_UNKNOWN2,))
                elif data == "-U2":
                    self._add(channel_nr, frame_nr, (OP_DISABLE_UNKNOWN2,))
                elif data == "+U3":
                    self._add(channel_nr, frame_nr, (OP_ENABLE_UNKNOWN3,))
                elif data == "-U3":
                    self._add(channel_nr, frame_nr, (OP_DISABLE_UNKNOWN3,))
                elif data.startswith("="):
                    if channel_nr < 2:
                        self._add(channel_nr, frame_nr, pulse_instruments[int(data[1:])])
                    elif channel_nr == 2:
                        self._add(channel_nr, frame_nr, wave_instruments[int(data[1:])])
                else:
                    self._add(channel_nr, frame_nr, (noteFromString(channel_nr, data), self._speed_table.index(length)))
                    self._current_time[channel_nr] += length

    def _optimize_with_loops(self, block):
        while True:
            best_loop = None
            loop_counter = 0
            for start in range(len(block)):
                if block[start][0] == OP_LOOP_START:
                    loop_counter += 1
                elif block[start][0] == OP_LOOP_END:
                    loop_counter -= 1
                if loop_counter > 0:
                    continue
                for length in range(1, min(32, len(block) - start)):
                    base_list = block[start:start + length]
                    skip = False
                    for op in base_list:
                        if op[0] == OP_LOOP_START:
                            skip = True
                            break
                    if skip:
                        continue
                    repeat_count = 1
                    while songOpsEqual(block[start + repeat_count * length:start + repeat_count * length + length], base_list):
                        repeat_count += 1
                    if repeat_count > 1:
                        saved_size = songPseudoOpsSize(base_list) * (repeat_count - 1)
                        if saved_size > 3 and (best_loop is None or best_loop[0] < saved_size):
                            best_loop = (saved_size, start, length, repeat_count)
            if best_loop is None:
                break
            saved_size, start, length, repeat_count = best_loop
            base_list = block[start:start + length]
            block = block[:start] + [(OP_LOOP_START, repeat_count)] + base_list + [(OP_LOOP_END,)] + block[start + length * repeat_count:]
        return block

    def _find_block_to_split(self):
        best_block = None
        for blocks in self._patterns.values():
            for block_idx, block in enumerate(blocks):
                in_loop_counter = 0
                for start in range(len(block) // 2):
                    if block[start][0] == OP_LOOP_START:
                        in_loop_counter += 1
                    elif block[start][0] == OP_LOOP_END:
                        in_loop_counter -= 1
                    if in_loop_counter > 0:
                        continue
                    for length in range(2, (len(block) - start) // 2):
                        base_list = block[start:start+length]
                        if songOpsHasUnclosedLoop(base_list):
                            continue
                        overlap_positions = [start]
                        check_start = start + length
                        while check_start < len(block) - length:
                            if songOpsEqual(base_list, block[check_start:check_start+length]):
                                overlap_positions.append(check_start)
                                check_start += length
                            else:
                                check_start += 1
                        if len(overlap_positions) > 1:
                            space_saved = songOpsSize(base_list) * (len(overlap_positions) - 1) - len(overlap_positions) * 4
                            if space_saved > 0:
                                if best_block is None or best_block[0] < space_saved:
                                    best_block = (space_saved, overlap_positions, length, blocks, block_idx)
        if best_block:
            space_saved, overlap_positions, length, blocks, block_idx = best_block
            input_ops = blocks.pop(block_idx)
            new_blocks = []
            start = 0
            for position in overlap_positions:
                if position > start:
                    new_blocks.append(input_ops[start:position])
                new_blocks.append(input_ops[position:position+length])
                start = position + length
            if start < len(input_ops):
                new_blocks.append(input_ops[start:])
            for new_block in new_blocks:
                blocks.insert(block_idx, new_block)
                block_idx += 1
            return True
        return False

    def optimize(self):
        # Remove channels that are just all rest.
        for n in range(4):
            if self._is_all_rest(n):
                self._patterns = {k: v for k, v in self._patterns.items() if k[0] != n}
        # Optimize blocks by searching and adding loops
        for channel, name in self._patterns:
            self._patterns[(channel, name)] = [self._optimize_with_loops(block) for block in self._patterns[(channel, name)]]
        # Find blocks to split to save space
        split_count = 0
        while self._find_block_to_split():
            split_count += 1
        print(f"Optimized with {split_count} splits, using {sum(len(blocks) for blocks in self._patterns.values())} blocks.")

    def to_song(self) -> Song:
        song = Song()
        song.initial_transpose = 0
        song.speed_data = bytes(self._speed_table)
        song.channels = [None, None, None, None]
        for channel_idx in range(4):
            for sequence in self._sequence:
                pattern = self._patterns.get((channel_idx, sequence))
                if pattern is None:
                    continue
                if song.channels[channel_idx] is None:
                    song.channels[channel_idx] = SongChannel()
                    song.channels[channel_idx].loop = len(pattern)
                for block in pattern:
                    song_block = SongBlock(random.randint(0, 0x40) * 0x100)
                    song.channels[channel_idx].blocks.append(song_block)
                    current_notelen = -1
                    for op in block:
                        if op[0] < OP_NOTE_MAX:
                            if current_notelen != op[1]:
                                current_notelen = op[1]
                                song_block.ops.append((OP_NOTELEN_0 + current_notelen, ))
                            song_block.ops.append((op[0],))
                        else:
                            song_block.ops.append(op)
                            if op[0] in {OP_LOOP_START, OP_SET_INSTRUMENT}:
                                current_notelen = -1
        return song

def main():
    i = LADXMImporter()
    i.load_ladxm("music/ffa/overworld_12.ladxm")
    i.optimize()
    song = i.to_song()
    song.dump()


if __name__ == "__main__":
    main()
