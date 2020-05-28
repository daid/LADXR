from roomEditor import RoomEditor


def tweakMap(rom):
    # 5 holes at the castle, reduces to 3
    re = RoomEditor(rom, 0x078)
    re.objects[-1].count = 3
    re.store(rom)
