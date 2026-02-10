from assembler import ASM
import musicData
import os


_LOOPING_MUSIC = (1, 2, 3, 4, 5, 6, 7, 8, 9, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
                  0x18, 0x19, 0x1C, 0x1D, 0x1F, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x2F, 0x31, 0x32, 0x33, 0x37,
                  0x39, 0x3A, 0x3C, 0x3E, 0x40, 0x48, 0x49, 0x4A, 0x4B, 0x4E, 0x50, 0x53, 0x54, 0x55, 0x57, 0x58, 0x59,
                  0x5A, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F, 0x60, 0x61)


def randomizeMusic(rom, rnd):
    # Randomize overworld
    for x in range(0, 16, 2):
        for y in range(0, 16, 2):
            idx = x + y * 16
            result = rnd.choice(_LOOPING_MUSIC)
            rom.banks[0x02][idx] = result
            rom.banks[0x02][idx+1] = result
            rom.banks[0x02][idx+16] = result
            rom.banks[0x02][idx+17] = result
    # Random music in dungeons/caves
    for n in range(0x20):
        rom.banks[0x02][0x100 + n] = rnd.choice(_LOOPING_MUSIC)


def noMusic(rom):
    rom.patch(0x1B, 0x001E, ASM("ld hl, $D368\nldi a, [hl]"), ASM("xor a"), fill_nop=True)
    rom.patch(0x1E, 0x001E, ASM("ld hl, $D368\nldi a, [hl]"), ASM("xor a"), fill_nop=True)

def shiftedMusic(rom):
    for n in range(18 * 4 + 2):
        freq = rom.banks[0x1B][0x09C2 + n * 2] | (rom.banks[0x1B][0x09C3 + n * 2] << 8)
        freq = max(0x20, min(int((freq - 8) * 0.95), 0x7FF))
        rom.banks[0x1B][0x09C2 + n * 2] = freq & 0xFF
        rom.banks[0x1B][0x09C3 + n * 2] = (freq >> 8) & 0xFF

        freq = rom.banks[0x1E][0x09BF + n * 2] | (rom.banks[0x1E][0x09C0 + n * 2] << 8)
        freq = max(0x20, min(int((freq - 8) * 0.95), 0x7FF))
        rom.banks[0x1E][0x09BF + n * 2] = freq & 0xFF
        rom.banks[0x1E][0x09C0 + n * 2] = (freq >> 8) & 0xFF

def importMusic(rom, rnd, music_directory):
    directory = os.path.join(os.path.dirname(__file__), "..", "music", music_directory)
    song_files = os.listdir(directory)
    rnd.shuffle(song_files)
    songs_a = musicData.MusicData(rom, 0x1B, 0x0077, 0x30)
    songs_b = musicData.MusicData(rom, 0x1E, 0x007F, 0x40)

    song_spots = {
        "dungeon": [
            (songs_b, 0x03, "D1"),
            (songs_b, 0x04, "D2"),
            (songs_b, 0x05, "D3"),
            (songs_b, 0x06, "D4"),
            (songs_b, 0x2A, "D5"),
            (songs_b, 0x37, "D6"),
            (songs_b, 0x3A, "D7"),
            (songs_b, 0x39, "D8"),
            (songs_a, 0x20, "D0"),
        ],
        "town": [
            (songs_a, 0x03, "Mabe"),
            (songs_a, 0x0A, "Animal"),
            (songs_a, 0x11, "MrWriteHouse"),
            (songs_a, 0x12, "Ulrira"),
            (songs_a, 0x16, "ChristineHouse"),
            (songs_a, 0x2F, "RichardHouse"),
        ],
        "overworld": [
            (songs_a, 0x04, "Overworld"),
            (songs_a, 0x05, "TalTalRange"),
            (songs_a, 0x07, "RaftRideRapids"),
            (songs_a, 0x08, "MysteriousForest"),
        ],
        "battle": [
            (songs_a, 0x1D, "MoblinHideout"),
            (songs_b, 0x08, "Boss"),
            (songs_b, 0x12, "FinalBoss"),
            (songs_b, 0x2F, "Miniboss"),
        ],
    }

    for song_file in song_files:
        song = musicData.import_ladxm(os.path.join(directory, song_file))
        song.optimize()
        if song_file == "battle_0e.ladxm":
            song.channels[0], song.channels[1] = song.channels[1], song.channels[0]
            song.dump()
        song_type, _, _ = song_file.partition("_")
        if song_type in song_spots and song_spots[song_type]:
            list_idx = rnd.randrange(0, len(song_spots[song_type]))
            songs, idx, name = song_spots[song_type].pop(list_idx)
            print(f"Replaced song {name} with {song_file}")
            songs.songs[idx] = song
        else:
            print(f"??? {song_type}")

    # TMP hack to save some space until we can compress song data better
    for n in range(6):
        songs_b.songs[0x20 + n] = songs_b.songs[0x26]
    songs_b.songs[0x3F] = songs_b.songs[0x00]

    songs_a.store(rom)
    songs_b.store(rom)