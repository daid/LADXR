from roomEditor import RoomEditor, Object, ObjectWarp, ObjectHorizontal
from assembler import ASM


BOSS_ROOMS = [
    (0x106, 0x10b),
    (0x12b, 0x12d),
    (0x15a, 0x15b),
    (0x166, 0x16c),
    (0x185, 0x18b),
    (0x1bc, 0x1c4),
    (0x223, ),
    (0x234, 0x23a),
    (0x300, 0x304),
]
SPRITE_DATA = [
    b'\xff\xff\xb0\xb1',
    b'\xff\xff\xb6\xb7',
    b'\xff\xff\xb4\xb5',
    None,
    b'\xff\xff\xb8\xb9',  # (Needs $06 in IndoorsTilesetsTable boss room)
    b'\xff\xff\xb2\xb3',  # (flying tiles are in first graphics set)
    None,
    b'\xff\xff\xba\xbb',
    b'\x90\xff\x94\xff',
]
BOSS_ENTITIES = [
    (3, 2, 0x59),
    (4, 2, 0x5C),
    (4, 3, 0x5B),
    None,
    (4, 3, 0x5D),
    (4, 3, 0x5A),
    None,
    (4, 3, 0x62),
    (5, 2, 0xF9),
]


def getCleanBossRoom(rom, dungeon_nr):
    re = RoomEditor(rom, BOSS_ROOMS[dungeon_nr][0])
    new_objects = []
    for obj in re.objects:
        if isinstance(obj, ObjectWarp):
            continue
        if obj.type_id == 0xBE:  # Remove staircases
            continue
        if obj.type_id == 0x06:  # Remove lava
            continue
        if obj.type_id == 0x1c:  # Change D1 pits into normal pits
            obj.type_id = 0x01
        if obj.type_id == 0x1e:  # Change D1 pits into normal pits
            obj.type_id = 0xaf
        if obj.type_id == 0x1f:  # Change D1 pits into normal pits
            obj.type_id = 0xb0
        if obj.type_id == 0xF5:  # Change open doors into closing doors.
            obj.type_id = 0xF1
        new_objects.append(obj)


    # Make D4 room a valid fighting room by removing most content.
    if dungeon_nr == 3:
        new_objects = new_objects[:2] + [Object(1, 1, 0xAC), Object(8, 1, 0xAC), Object(1, 6, 0xAC), Object(8, 6, 0xAC)]

    # D7 has an empty room we use for most bosses, but it needs some adjustments.
    if dungeon_nr == 6:
        # Move around the unused and instrument room.
        rom.banks[0x14][0x03a0 + 6 + 1 * 8] = 0x00
        rom.banks[0x14][0x03a0 + 7 + 2 * 8] = 0x2C
        rom.banks[0x14][0x03a0 + 7 + 3 * 8] = 0x23
        rom.banks[0x14][0x03a0 + 6 + 5 * 8] = 0x00

        rom.banks[0x14][0x0520 + 7 + 2 * 8] = 0x2C
        rom.banks[0x14][0x0520 + 7 + 3 * 8] = 0x23
        rom.banks[0x14][0x0520 + 6 + 5 * 8] = 0x00

        re.floor_object &= 0x0F
        new_objects += [
            Object(4, 0, 0xF0),
            Object(1, 6, 0xBE),
            ObjectWarp(1, dungeon_nr, 0x22E, 24, 16)
        ]

        # Set the stairs towards the eagle tower top to our new room.
        r = RoomEditor(rom, 0x22E)
        r.objects[-1] = ObjectWarp(1, dungeon_nr, re.room, 24, 112)
        r.store(rom)

        # Remove the normal door to the instrument room
        r = RoomEditor(rom, 0x22e)
        r.removeObject(4, 0)
        r.store(rom)
        rom.banks[0x14][0x22e - 0x100] = 0x00

        r = RoomEditor(rom, 0x22c)
        r.changeObject(0, 7, 0x03)
        r.changeObject(2, 7, 0x03)
        r.store(rom)

    re.objects = new_objects
    re.entities = []
    return re


def changeBosses(rom, mapping):
    for dungeon_nr in range(9):
        target = mapping[dungeon_nr]
        if target == dungeon_nr:
            continue

        if target == 3:  # D4 fish boss
            # If dungeon_nr == 6: use normal eagle door towards fish.
            if dungeon_nr == 6:
                # Add the staircase to the boss, and fix the warp back.
                re = RoomEditor(rom, 0x22E)
                for obj in re.objects:
                    if isinstance(obj, ObjectWarp):
                        obj.type_id = 2
                        obj.map_nr = 3
                        obj.room = 0x1EF
                        obj.target_x = 24
                        obj.target_y = 16
                re.store(rom)
                re = RoomEditor(rom, 0x1EF)
                re.objects[-1] = ObjectWarp(1, dungeon_nr if dungeon_nr < 8 else 0xff, 0x22E, 72, 80)
                re.store(rom)
            else:
                # Set the proper room event flags
                rom.banks[0x14][BOSS_ROOMS[dungeon_nr][0] - 0x100] = 0x2A

                # Patch the fish heart container to open up the right room.
                rom.patch(0x03, 0x1A0F, ASM("ld hl, $D966"), ASM("ld hl, $%04x" % (0xD800 + BOSS_ROOMS[dungeon_nr][0])))

                # Add the staircase to the boss, and fix the warp back.
                re = getCleanBossRoom(rom, dungeon_nr)
                re.objects += [Object(4, 4, 0xBE), ObjectWarp(2, 3, 0x1EF, 24, 16)]
                re.store(rom)
                re = RoomEditor(rom, 0x1EF)
                re.objects[-1] = ObjectWarp(1, dungeon_nr if dungeon_nr < 8 else 0xff, BOSS_ROOMS[dungeon_nr][0], 72, 80)
                re.store(rom)
            # Patch the proper item towards the D4 boss
            rom.banks[0x3E][0x3800 + 0x01ff] = rom.banks[0x3E][0x3800 + BOSS_ROOMS[dungeon_nr][0]]
            rom.banks[0x3E][0x3300 + 0x01ff] = rom.banks[0x3E][0x3300 + BOSS_ROOMS[dungeon_nr][0]]
        elif target == 6:  # Evil eagle
            rom.banks[0x14][BOSS_ROOMS[dungeon_nr][0] - 0x100] = 0x2A

            # Patch the eagle heart container to open up the right room.
            rom.patch(0x03, 0x1A04, ASM("ld hl, $DA2E"), ASM("ld hl, $%04x" % (0xD800 + BOSS_ROOMS[dungeon_nr][0])))
            rom.patch(0x02, 0x1FC8, ASM("cp $06"), ASM("cp $%02x" % (dungeon_nr if dungeon_nr < 8 else 0xff)))

            # Add the staircase to the boss, and fix the warp back.
            re = getCleanBossRoom(rom, dungeon_nr)
            re.objects += [Object(4, 4, 0xBE), ObjectWarp(2, 6, 0x2F8, 72, 80)]
            re.store(rom)
            re = RoomEditor(rom, 0x2F8)
            re.objects[-1] = ObjectWarp(1, dungeon_nr if dungeon_nr < 8 else 0xff, BOSS_ROOMS[dungeon_nr][0], 72, 80)
            re.store(rom)

            # Patch the proper item towards the D7 boss
            rom.banks[0x3E][0x3800 + 0x0223] = rom.banks[0x3E][0x3800 + BOSS_ROOMS[dungeon_nr][0]]
            rom.banks[0x3E][0x3300 + 0x0223] = rom.banks[0x3E][0x3300 + BOSS_ROOMS[dungeon_nr][0]]
        else:
            rom.banks[0x14][BOSS_ROOMS[dungeon_nr][0] - 0x100] = 0x21
            rom.room_sprite_data_indoor[BOSS_ROOMS[dungeon_nr][0] - 0x100] = SPRITE_DATA[target]
            for room in BOSS_ROOMS[dungeon_nr][1:]:
                rom.room_sprite_data_indoor[room - 0x100] = b'\xff\xff\xff\xff'
            re = getCleanBossRoom(rom, dungeon_nr)
            re.entities = [BOSS_ENTITIES[target]]

            if target == 4:
                # For slime eel, we need to setup the right wall tiles.
                rom.banks[0x20][0x2EB3 + BOSS_ROOMS[dungeon_nr][0] - 0x100] = 0x06
            if target == 5:
                # Patch facade so he doesn't use the spinning tiles, which is a problem for the sprites.
                rom.patch(0x04, 0x121D, ASM("cp $14"), ASM("cp $00"))
                rom.patch(0x04, 0x1226, ASM("cp $04"), ASM("cp $00"))
                rom.patch(0x04, 0x127F, ASM("cp $14"), ASM("cp $00"))
            if target == 7:
                pass
                # For hot head, add some lava (causes graphical glitches)
                # re.animation_id = 0x06
                # re.objects += [
                #     ObjectHorizontal(3, 2, 0x06, 4),
                #     ObjectHorizontal(2, 3, 0x06, 6),
                #     ObjectHorizontal(2, 4, 0x06, 6),
                #     ObjectHorizontal(3, 5, 0x06, 4),
                # ]

            re.store(rom)
