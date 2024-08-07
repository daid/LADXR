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
    entrance_rooms = {
        1: 0x117, 2: 0x136, 3: 0x152, 4: 0x17A, 5: 0x1A1, 6: 0x1D4, 7: 0x20E, 8: 0x25D, 0: 0x312, "egg": 0x274,
        "shop": 0x2A1, "mamu": 0x2FB, "trendy": 0x2A0, "dream": 0x2AA, "chestcave": 0x2CD,
    }
    maps = {
        1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 0: 0xFF, "egg": 8,
        "shop": 0x0E, "mamu": 0x11, "trendy": 0x0F, "dream": 0x13, "chestcave": 0x11,
        "cavegen": 0x0A,
    }
    exit_rooms = {
        1: 0x102, 2: 0x12A, 3: 0x159, 4: 0x162, 5: 0x182, 6: 0x1B5, 7: 0x22C, 8: 0x230, 0: 0x301, "egg": 0x272,
        "shop": 0x2A1, "mamu": 0x2FB, "trendy": 0x2A0, "dream": 0x2AA, "chestcave": 0x2CD,
    }
    single_rooms = {"shop", "mamu", "trendy", "dream", "chestcave"}
    order = world_setup.dungeon_chain + ["egg"]

    if world_setup.cavegen:
        for ri in [0x2B6, 0x2B7, 0x2B8, 0x2B9, 0x285, 0x286, 0x2F3, 0x2ED, 0x2EE, 0x2EA, 0x2EB, 0x2EC, 0x287, 0x2F1, 0x2F2, 0x2EF, 0x2BA, 0x2BB, 0x2BC, 0x28D, 0x2F9, 0x2FA, 0x280, 0x281, 0x282, 0x283, 0x284, 0x28C, 0x288, 0x28A, 0x290, 0x291, 0x292, 0x28E, 0x29A, 0x289, 0x28B]:
            re = RoomEditor(rom, ri)
            re.entities = []
            re.objects = []
            re.store(rom)
        for xy in range(8 * 8):
            rom.banks[0x14][0x0220 + 10 * 8 * 8 + xy] = 0
        for room in world_setup.cavegen.all_rooms:
            rom.banks[0x14][0x0220 + 10 * 8 * 8 + room.x + room.y * 8] = room.room_id & 0xFF
            rom.banks[0x14][0x0000 + room.room_id - 0x100] = room.event
            re = RoomEditor(rom, room.room_id)
            re.entities = room.entities
            re.buildObjectList(room.tiles)
            if re.hasEntity(0xBE):
                re.objects.append(ObjectWarp(1, 0x0A, world_setup.cavegen.start.room_id, 80, 80))
            re.store(rom)
            if room.type == "start":
                entrance_rooms["cavegen"] = room.room_id
            if room.type == "end":
                exit_rooms["cavegen"] = room.room_id
        # Fix tile attributes for bombable walls
        rom.patch(0x24, 0x0400 + 0x3F * 4, "00000000040404040000000000000000", "04040404040404040404040404040404")

    last_exit_map = 0x10
    last_exit_room = 0x2A3  # Start house
    last_exit_chain = "start"

    for chain_step in order:
        # Patch the exit of the previous map to warp the next chain step.
        re = RoomEditor(rom, last_exit_room)
        if last_exit_chain in single_rooms:
            # Duplicate the return-to-previous warp, and add a warp to the next one.
            # Then add two doors and an entity that controls the door warps
            re.objects += re.getWarps()
            re.objects.append(ObjectWarp(1, maps[chain_step], entrance_rooms[chain_step], 80, 96 if chain_step == 0 else 124))
            re.objects = [obj for obj in re.objects if obj.type_id not in {0xFD, 0xCB}]
            if last_exit_chain == "mamu":
                re.objects += [Object(2, 7, 0xF5), Object(6, 7, 0xF5)]
                re.entities.append((1, 0, 0x44))  # yarna bones entity
            else:
                re.objects += [Object(2, 7, 0xFD), Object(6, 7, 0xFD)]
                re.entities.append((0, 0, 0x44))  # yarna bones entity
        else:
            re.objects = [o for o in re.objects if not isinstance(o, ObjectWarp)]
            if chain_step == "cavegen":
                re.objects.append(ObjectWarp(1, maps[chain_step], entrance_rooms[chain_step], 80, 80))
            else:
                re.objects.append(ObjectWarp(1, maps[chain_step], entrance_rooms[chain_step], 80, 124))
            if last_exit_chain != "start":
                re.entities = []
                re.objects.append(ObjectHorizontal(4, 2, 0x1D, 2))
            if last_exit_chain == 0:  # Remove the border in color dungeon room
                re.removeObject(2, 1)
                re.removeObject(7, 1)
                re.removeObject(2, 4)
                re.removeObject(3, 4)
                re.removeObject(7, 4)
        re.store(rom)

        # Patch the entrance of this chain step to goto the previous step.
        re = RoomEditor(rom, entrance_rooms[chain_step] if chain_step != "egg" else 0x270)
        re.objects = [o for o in re.objects if not isinstance(o, ObjectWarp)]
        if last_exit_chain == "start":
            re.objects.append(ObjectWarp(1, last_exit_map, last_exit_room, 80, 124))
        elif last_exit_chain in single_rooms:
            re.objects.append(ObjectWarp(1, last_exit_map, last_exit_room, 112, 124))
        else:
            re.objects.append(ObjectWarp(1, last_exit_map, last_exit_room, 80, 64))
        if chain_step == "egg":  # For the egg, don't give an option to enter the maze
            re.removeObject(3, 0)
            re.removeObject(4, 0)
            re.removeObject(6, 0)
        re.store(rom)

        last_exit_map = maps[chain_step]
        last_exit_room = exit_rooms[chain_step]
        last_exit_chain = chain_step

    # Do not lock the color dungeon final room door.
    rom.patch(0x14, 0x0201, "24", "00")
    # Fix that the music stays on boss defeated after killing the boss and switching map.
    rom.patch(0x03, 0x23B9, ASM("ld [wBossDefeated], a"), "", fill_nop=True)

    # Patch the yarna bones code into an entity that handles the two doors in a single room for us
    rom.patch(0x15, 0x043F, 0x0492, ASM("""
    ; Prevent changing the warp when we are entering the dream bed
    ld  a, [wLinkMotionState]
    cp  3 ; LINK_MOTION_MAP_FADE_OUT
    ret z
    
    ldh a, [hLinkPositionZ] ; linkZ
    cp  $70
    jr  nz, linkNotFallingIn
    ld  a, $30
    ldh [hLinkPositionX], a ; linkX
    ld  a, $78
    ldh [hLinkPositionY], a ; linkY
linkNotFallingIn:

    ldh a, [hLinkPositionX] ; linkX
    cp  $50
    ld  de, $D401 ; warp0 data
    jr  nc, rightSide
leftSide:
    ld  hl, $D406 ; warp1 data
    jr  copyWarpData
rightSide:
    ld  hl, $D40B ; warp2 data

copyWarpData:
    push bc
    ld  c, 5
.loop:
    ld  a, [hl+]
    ld  [de], a
    inc de
    dec c
    jr  nz, .loop
    pop bc
    
    ldh a, [hActiveEntityPosX] ; active entity X
    cp  $10
    ret c
    ; If we use fake exit tiles, make sure the tiles are proper exits
    ld  hl, $D783
    ld  a, $C1
    ld  [hl+], a
    ld  a, $C2
    ld  [hl+], a
    inc hl
    inc hl
    ld  a, $C1
    ld  [hl+], a
    ld  a, $C2
    ld  [hl+], a
    ret
""", 0x443F), fill_nop=True)
    # For the color ghouls, they normally wait till the door is locked before attacking, remove that check.
    rom.patch(0x36, 0x23E1, ASM("ret z"), "", fill_nop=True)