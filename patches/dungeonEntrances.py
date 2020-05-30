from roomEditor import RoomEditor, ObjectWarp


def changeEntrances(rom, mapping):
    entrance_rooms = [0x0D3, 0x024, 0x0B5, 0x02B, 0x0D9, 0x08C, 0x00E, 0x010, 0x077]
    alt_rooms = [None, None, None, (0x09, 0x109A), None, (0x1A, 0x034E), (0x09, 0x07EC), None, None]
    enter_warps = []
    exit_warps = []

    for idx, room in enumerate(entrance_rooms):
        if alt_rooms[idx] is not None:
            re = RoomEditor(rom, bank_nr=alt_rooms[idx][0], address=alt_rooms[idx][1])
        else:
            re = RoomEditor(rom, room)
        warp = None
        for obj in re.objects:
            if isinstance(obj, ObjectWarp) and (obj.map_nr < 9 or obj.map_nr == 0xff):
                warp = obj
        enter_warps.append(warp)
        if warp:
            re = RoomEditor(rom, warp.room)
            warp = None
            for obj in re.objects:
                if isinstance(obj, ObjectWarp) and obj.room == room:
                    warp = obj
        exit_warps.append(warp)

    for a, b in enumerate(mapping):
        re = RoomEditor(rom, entrance_rooms[a])
        re.changeWarpTarget(enter_warps[a].room, enter_warps[b].room, enter_warps[b].map_nr, enter_warps[b].target_x, enter_warps[b].target_y)
        re.store(rom)
        if alt_rooms[a] is not None:
            re = RoomEditor(rom, bank_nr=alt_rooms[a][0], address=alt_rooms[a][1])
            re.changeWarpTarget(enter_warps[a].room, enter_warps[b].room, enter_warps[b].map_nr, enter_warps[b].target_x, enter_warps[b].target_y)
            re.store(rom)
        re = RoomEditor(rom, enter_warps[b].room)
        re.changeWarpTarget(entrance_rooms[b], exit_warps[a].room, exit_warps[a].map_nr, exit_warps[a].target_x, exit_warps[a].target_y)
        re.store(rom)
