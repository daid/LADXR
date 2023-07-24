from roomEditor import RoomEditor, Object, ObjectHorizontal, ObjectWarp
from assembler import ASM


KEY_DOORS = {
    0xEC: 0xF4,
    0xED: 0xF5,
    0xEE: 0xF6,
    0xEF: 0xF7,
    0xF8: 0xF4,
}

def removeKeyDoors(rom):
    for n in range(0x100, 0x316):
        if n == 0x2FF:
            continue
        update = False
        re = RoomEditor(rom, n)
        for obj in re.objects:
            if obj.type_id in KEY_DOORS:
                obj.type_id = KEY_DOORS[obj.type_id]
                update = True
            if obj.type_id == 0xDE: # Keyblocks
                obj.type_id = re.floor_object & 0x0F
                update = True
        if update:
            re.store(rom)


def patchNoDungeons(rom):
    def setMinimap(dungeon_nr, x, y, room):
        for n in range(64):
            if rom.banks[0x14][0x0220 + 64 * dungeon_nr + n] == room:
                rom.banks[0x14][0x0220 + 64 * dungeon_nr + n] = 0xFF
        rom.banks[0x14][0x0220 + 64 * dungeon_nr + x + y * 8] = room
    #D1
    setMinimap(0, 3, 6, 0x06)
    setMinimap(0, 3, 5, 0x02)
    re = RoomEditor(rom, 0x117)
    for n in range(1, 7):
        re.removeObject(n, 0)
        re.removeObject(0, n)
        re.removeObject(9, n)
    re.objects += [Object(4, 0, 0xf0)]
    re.store(rom)
    re = RoomEditor(rom, 0x11A)
    re.getWarps()[0].room = 0x117
    re.store(rom)
    re = RoomEditor(rom, 0x11B)
    re.getWarps()[0].room = 0x117
    re.store(rom)

    #D2
    setMinimap(1, 2, 6, 0x2B)
    setMinimap(1, 1, 6, 0x2A)
    re = RoomEditor(rom, 0x136)
    for n in range(1, 7):
        re.removeObject(n, 0)
    re.objects += [Object(4, 0, 0xf0)]
    re.store(rom)

    #D3
    setMinimap(2, 1, 6, 0x5A)
    setMinimap(2, 1, 5, 0x59)
    re = RoomEditor(rom, 0x152)
    for n in range(2, 7):
        re.removeObject(9, n)
    re.store(rom)

    #D4
    setMinimap(3, 3, 6, 0x66)
    setMinimap(3, 3, 5, 0x62)
    re = RoomEditor(rom, 0x17A)
    for n in range(3, 7):
        re.removeObject(n, 0)
    re.objects += [Object(4, 0, 0xf0)]
    re.store(rom)

    #D5
    setMinimap(4, 7, 6, 0x85)
    setMinimap(4, 7, 5, 0x82)
    re = RoomEditor(rom, 0x1A1)
    for n in range(3, 8):
        re.removeObject(n, 0)
        re.removeObject(0, n)
    for n in range(4, 6):
        re.removeObject(n, 1)
        re.removeObject(n, 2)
    re.objects += [Object(4, 0, 0xf0)]
    re.store(rom)

    #D6
    setMinimap(5, 3, 6, 0xBC)
    setMinimap(5, 3, 5, 0xB5)
    re = RoomEditor(rom, 0x1D4)
    for n in range(2, 8):
        re.removeObject(0, n)
        re.removeObject(9, n)
    re.objects += [Object(4, 0, 0xf0)]
    re.store(rom)

    #D7
    setMinimap(6, 1, 6, 0x2E)
    setMinimap(6, 1, 5, 0x2C)
    re = RoomEditor(rom, 0x20E)
    for n in range(1, 8):
        re.removeObject(0, n)
        re.removeObject(9, n)
    re.objects += [Object(3, 0, 0x29), ObjectHorizontal(4, 0, 0x0D, 2), Object(6, 0, 0x2A)]
    re.store(rom)
    re = RoomEditor(rom, 0x22E)
    re.objects = [Object(4, 0, 0xf0), Object(3, 7, 0x2B), ObjectHorizontal(4, 7, 0x0D, 2), Object(6, 7, 0x2C), Object(1, 0, 0xA8)] + re.getWarps()
    re.floor_object = 13
    re.store(rom)
    re = RoomEditor(rom, 0x22C)
    re.removeObject(0, 7)
    re.removeObject(2, 7)
    re.objects.append(ObjectHorizontal(0, 7, 0x03, 3))
    re.store(rom)

    #D8
    setMinimap(7, 3, 6, 0x34)
    setMinimap(7, 3, 5, 0x30)
    re = RoomEditor(rom, 0x25D)
    re.objects += [Object(3, 0, 0x25), Object(4, 0, 0xf0), Object(6, 0, 0x26)]
    re.store(rom)

    #D0
    setMinimap(11, 2, 6, 0x00)
    setMinimap(11, 3, 6, 0x01)


def patchDungeonChain(rom, world_setup):
    entrance_rooms = [0x117, 0x136, 0x152, 0x17A, 0x1A1, 0x1D4, 0x20E, 0x25D, 0x312, 0x274]
    maps = [0, 1, 2, 3, 4, 5, 6, 7, 0xFF, 8]
    exit_rooms = [0x102, 0x12A, 0x159, 0x162, 0x182, 0x1B5, 0x22C, 0x230, 0x301, 0x272]
    order = world_setup.dungeon_chain + [9]  # Add 9 as egg, which always will be the final link in the chain.

    last_exit_map = 0x10
    last_exit_room = 0x2A3  # Start house

    for n in range(len(order)):
        re = RoomEditor(rom, last_exit_room)
        re.objects = [o for o in re.objects if not isinstance(o, ObjectWarp)]
        re.objects.append(ObjectWarp(1, maps[order[n]], entrance_rooms[order[n]], 80, 124))
        if last_exit_map != 0x10:
            re.entities = []
            re.objects.append(ObjectHorizontal(4, 2, 0x1D, 2))
            if last_exit_room == 0x301:  # Remove the border in color dungeon room
                re.removeObject(2, 1)
                re.removeObject(7, 1)
                re.removeObject(2, 4)
                re.removeObject(3, 4)
                re.removeObject(7, 4)
        re.store(rom)

        re = RoomEditor(rom, entrance_rooms[order[n]] if order[n] != 9 else 0x270)
        re.objects = [o for o in re.objects if not isinstance(o, ObjectWarp)]
        re.objects.append(ObjectWarp(1, last_exit_map, last_exit_room, 80, 124 if last_exit_map == 0x10 else 64))
        if order[n] == 9:  # For the egg, don't give an option to enter the maze
            re.removeObject(3, 0)
            re.removeObject(4, 0)
            re.removeObject(6, 0)
        re.store(rom)

        last_exit_map = maps[order[n]]
        last_exit_room = exit_rooms[order[n]]

    # Do not lock the color dungeon final room door.
    rom.patch(0x14, 0x0201, "24", "00")
    # Fix that the music stays on boss defeated after killing the boss and switching map.
    rom.patch(0x03, 0x23B9, ASM("ld [$D46C], a"), "", fill_nop=True)
