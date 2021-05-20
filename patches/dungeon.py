from roomEditor import RoomEditor


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
                obj.type_id = re.floor_object
                update = True
        if update:
            re.store(rom)
