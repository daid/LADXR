from roomEditor import RoomEditor, ObjectWarp


def changeEntrances(rom, mapping):
    dungeon_entrance_rooms = [0x117, 0x136, 0x152, 0x17a, 0x1a1, 0x1d4, 0x20e, 0x25d, 0x312]
    instrument_rooms = [0x102, 0x12A, 0x159, 0x162, 0x182, 0x1B5, 0x22C, 0x230, 0x301]

    alt_rooms = {0x02B: (0x09, 0x109A), 0x08C: (0x1A, 0x034E), 0x00E: (0x09, 0x07EC)}

    world_entrance_rooms = []
    enter_warps = []
    exit_warps = []

    for room in dungeon_entrance_rooms:
        world_entrance_rooms.append(RoomEditor(rom, room).getWarps()[0].room)

    for idx, room in enumerate(world_entrance_rooms):
        if alt_rooms.get(room, None) is not None:
            re = RoomEditor(rom, bank_nr=alt_rooms[room][0], address=alt_rooms[room][1])
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

        re = RoomEditor(rom, instrument_rooms[idx])
        for obj in re.objects:
            if isinstance(obj, ObjectWarp):
                assert obj.room == world_entrance_rooms[idx]

    for a, b in enumerate(mapping):
        re = RoomEditor(rom, world_entrance_rooms[a])
        re.changeWarpTarget(enter_warps[a].room, enter_warps[b].room, enter_warps[b].map_nr, enter_warps[b].target_x, enter_warps[b].target_y)
        re.store(rom)
        if alt_rooms.get(world_entrance_rooms[a], None) is not None:
            re = RoomEditor(rom, bank_nr=alt_rooms[world_entrance_rooms[a]][0], address=alt_rooms[world_entrance_rooms[a]][1])
            re.changeWarpTarget(enter_warps[a].room, enter_warps[b].room, enter_warps[b].map_nr, enter_warps[b].target_x, enter_warps[b].target_y)
            re.store(rom)
        re = RoomEditor(rom, enter_warps[b].room)
        re.changeWarpTarget(world_entrance_rooms[b], exit_warps[a].room, exit_warps[a].map_nr, exit_warps[a].target_x, exit_warps[a].target_y)
        re.store(rom)
        re = RoomEditor(rom, instrument_rooms[b])
        re.changeWarpTarget(world_entrance_rooms[b], exit_warps[a].room, exit_warps[a].map_nr, exit_warps[a].target_x, exit_warps[a].target_y)
        re.store(rom)


def readEntrances(rom):
    result = []
    entrance_rooms = [0x0D3, 0x024, 0x0B5, (0x09, 0x109A), 0x0D9, (0x1A, 0x034E), (0x09, 0x07EC), 0x010, 0x077]

    for idx, room in enumerate(entrance_rooms):
        if isinstance(room, tuple):
            re = RoomEditor(rom, bank_nr=room[0], address=room[1])
        else:
            re = RoomEditor(rom, room)
        warp = None
        for obj in re.objects:
            if isinstance(obj, ObjectWarp) and (obj.map_nr < 9 or obj.map_nr == 0xff):
                warp = obj
        if not warp:
            # TODO: This indicates a different map setup...
            result.append(idx)
        elif warp.map_nr == 0xFF:
            result.append(8)
        else:
            result.append(warp.map_nr)
    return result
