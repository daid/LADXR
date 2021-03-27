from roomEditor import RoomEditor
from worldSetup import ENTRANCE_INFO


def changeEntrances(rom, mapping):
    warp_to_indoor = {}
    warp_to_outdoor = {}
    for key in mapping.keys():
        info = ENTRANCE_INFO[key]
        re = RoomEditor(rom, info.alt_room if info.alt_room is not None else info.room)
        warp = re.getWarps()[info.index if info.index not in (None, "all") else 0]
        warp_to_indoor[key] = warp
        assert info.target == warp.room, "%s != %03x" % (key, warp.room)

        re = RoomEditor(rom, warp.room)
        for warp in re.getWarps():
            if warp.room == info.room:
                warp_to_outdoor[key] = warp
        assert key in warp_to_outdoor, "Missing warp to outdoor on %s" % (key)

    for key, target in mapping.items():
        if key == target:
            continue
        info = ENTRANCE_INFO[key]
        # Change the entrance to point to the new indoor room
        re = RoomEditor(rom, info.room)
        re.changeWarp(warp_to_indoor[key].room, warp_to_indoor[target])
        re.store(rom)
        if info.alt_room:
            re = RoomEditor(rom, info.alt_room)
            re.changeWarp(warp_to_indoor[key].room, warp_to_indoor[target])
            re.store(rom)

        # Change the exit to point to the right outside
        re = RoomEditor(rom, warp_to_indoor[target].room)
        re.changeWarp(ENTRANCE_INFO[target].room, warp_to_outdoor[key])
        re.store(rom)
        if ENTRANCE_INFO[target].instrument_room is not None:
            re = RoomEditor(rom, ENTRANCE_INFO[target].instrument_room)
            re.changeWarp(ENTRANCE_INFO[target].room, warp_to_outdoor[key])
            re.store(rom)


def readEntrances(rom):
    result = {}
    for key, info in ENTRANCE_INFO.items():
        re = RoomEditor(rom, info.alt_room if info.alt_room is not None else info.room)
        warp = re.getWarps()[info.index if info.index not in (None, "all") else 0]
        for other_key, other_info in ENTRANCE_INFO.items():
            if warp.room == other_info.target:
                result[key] = other_key
    return result
