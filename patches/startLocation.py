from roomEditor import RoomEditor, ObjectWarp

# Make sure this list matches the logic list!
START_EXITS = [
    0x0A2,
    0x0E3,
    0x088,
    0x031,
    0x037,
    0x011,
    0x0DB,
    0x00A,
]


def setStartLocation(rom, index):
    if index == 0:
        return

    def swapWarps(r0, r1):
        r0warps = list(filter(lambda obj: isinstance(obj, ObjectWarp), r0.objects))
        r1warps = list(filter(lambda obj: isinstance(obj, ObjectWarp), r1.objects))
        r0.objects = list(filter(lambda obj: not isinstance(obj, ObjectWarp), r0.objects)) + r0warps[:-1] + r1warps[-1:]
        r1.objects = list(filter(lambda obj: not isinstance(obj, ObjectWarp), r1.objects)) + r1warps[:-1] + r0warps[-1:]
        return r0warps[-1].room, r1warps[-1].room

    old_room = RoomEditor(rom, START_EXITS[0])
    new_room = RoomEditor(rom, START_EXITS[index])
    old_indoor_room_id, new_indoor_room_id = swapWarps(old_room, new_room)
    old_room.store(rom)
    new_room.store(rom)

    old_room = RoomEditor(rom, old_indoor_room_id)
    new_room = RoomEditor(rom, new_indoor_room_id)
    swapWarps(old_room, new_room)
    old_room.store(rom)
    new_room.store(rom)


def readStartLocation(rom):
    for index, room in enumerate(START_EXITS):
        re = RoomEditor(rom, room)
        for obj in re.objects:
            if isinstance(obj, ObjectWarp) and obj.room == 0x2a3:
                return index
    assert False, "Failed to find starting house exit..."
