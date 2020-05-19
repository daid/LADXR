

class RoomEditor:
    def __init__(self, rom, room):
        self.room = room
        self.entities = []
        self.objects = []

        entities_raw = rom.entities[room]
        idx = 0
        while entities_raw[idx] != 0xFF:
            x = entities_raw[idx] & 0x0F
            y = entities_raw[idx] >> 4
            id = entities_raw[idx + 1]
            self.entities.append((x, y, id))
            idx += 2
        assert idx == len(entities_raw) - 1

        if room < 0x080:
            objects_raw = rom.rooms_overworld_top[room]
        elif room < 0x100:
            objects_raw = rom.rooms_overworld_bottom[room - 0x80]
        elif room < 0x200:
            objects_raw = rom.rooms_indoor_a[room - 0x100]
        elif room < 0x300:
            objects_raw = rom.rooms_indoor_b[room - 0x200]
        else:
            assert False, "Color dungeon not added yet"

        self.animation_id = objects_raw[0]
        self.floor_tile = objects_raw[1]
        idx = 2
        while objects_raw[idx] != 0xFE:
            x = objects_raw[idx] & 0x0F
            y = objects_raw[idx] >> 4
            if y == 0x08:  # horizontal
                count = x
                x = objects_raw[idx + 1] & 0x0F
                y = objects_raw[idx + 1] >> 4
                self.objects.append(ObjectHorizontal(x, y, objects_raw[idx + 2], count))
                idx += 3
            elif y == 0x0C: # vertical
                count = x
                x = objects_raw[idx + 1] & 0x0F
                y = objects_raw[idx + 1] >> 4
                self.objects.append(ObjectVertical(x, y, objects_raw[idx + 2], count))
                idx += 3
            elif y == 0x0E:  # warp
                # TODO: Figure out warp format. idx+2 seems target room, idx+3/idx+4 destination pixel location
                self.objects.append(ObjectWarp(objects_raw[idx:idx+5]))
                idx += 5
            else:
                self.objects.append(Object(x, y, objects_raw[idx + 1]))
                idx += 2
        assert idx == len(objects_raw) - 1

        if room < 0x0CC:
            self.overlay = rom.banks[0x26][room * 80:room * 80+80]
        elif room < 0x100:
            self.overlay = rom.banks[0x27][(room - 0xCC) * 80:(room - 0xCC) * 80 + 80]
        else:
            self.overlay = None

    def store(self, rom):
        objects_raw = bytearray([self.animation_id, self.floor_tile])
        for obj in self.objects:
            objects_raw += obj.export()
        objects_raw += bytearray([0xFE])

        if self.room < 0x080:
            rom.rooms_overworld_top[self.room] = objects_raw
        elif self.room < 0x100:
            rom.rooms_overworld_bottom[self.room - 0x80] = objects_raw
        elif self.room < 0x200:
            rom.rooms_indoor_a[self.room - 0x100] = objects_raw
        elif self.room < 0x300:
            rom.rooms_indoor_b[self.room - 0x200] = objects_raw
        else:
            assert False, "Color dungeon not added yet"

        entities_raw = bytearray()
        for entity in self.entities:
            entities_raw += bytearray([entity[0] | entity[1] << 4, entity[2]])
        entities_raw += bytearray([0xFF])
        rom.entities[self.room] = entities_raw

        if self.room < 0x0CC:
            rom.banks[0x26][self.room * 80:self.room * 80 + 80] = self.overlay
        elif self.room < 0x100:
            rom.banks[0x27][(self.room - 0xCC) * 80:(self.room - 0xCC) * 80 + 80] = self.overlay

    def addEntity(self, x, y, type_id):
        self.entities.append((x, y, type_id))

    def removeEntities(self, type_id):
        self.entities = list(filter(lambda e: e[2] != type_id, self.entities))

    def hasEntity(self, type_id):
        return any(map(lambda e: e[2] == type_id, self.entities))

    def changeObject(self, x, y, new_type):
        for obj in self.objects:
            if obj.x == x and obj.y == y:
                obj.type_id = new_type
                if self.overlay is not None:
                    self.overlay[x + y * 10] = new_type

    def removeObject(self, x, y):
        self.objects = list(filter(lambda obj: obj.x != x or obj.y != y, self.objects))

    def moveObject(self, x, y, new_x, new_y):
        for obj in self.objects:
            if obj.x == x and obj.y == y:
                if self.overlay is not None:
                    self.overlay[x + y * 10] = self.floor_tile
                    self.overlay[new_x + new_y * 10] = obj.type_id
                obj.x = new_x
                obj.y = new_y

class Object:
    def __init__(self, x, y, type_id):
        self.x = x
        self.y = y
        self.type_id = type_id

    def export(self):
        return bytearray([self.x | (self.y << 4), self.type_id])

    def __repr__(self):
        return "%s:%d,%d:%02X" % (self.__class__.__name__, self.x, self.y, self.type_id)


class ObjectHorizontal(Object):
    def __init__(self, x, y, type_id, count):
        super().__init__(x, y, type_id)
        self.count = count

    def export(self):
        return bytearray([0x80 | self.count, self.x | (self.y << 4), self.type_id])


class ObjectVertical(Object):
    def __init__(self, x, y, type_id, count):
        super().__init__(x, y, type_id)
        self.count = count

    def export(self):
        return bytearray([0xC0 | self.count, self.x | (self.y << 4), self.type_id])


class ObjectWarp(Object):
    def __init__(self, data):
        super().__init__(None, None, None)
        self.data = data

    def export(self):
        return self.data
