class OverworldSection:
    def __init__(self, name, corner_room, size):
        self.name = name
        self.corner_room = corner_room
        self.size = size

    def hasRoom(self, room):
        return (self.corner_room & 0x0F) <= (room & 0x0F) < (self.corner_room & 0x0F) + self.size[0] and \
               ((self.corner_room & 0xF0) >> 4) <= ((room & 0xF0) >> 4) < (((self.corner_room & 0xF0) >> 4) + self.size[1])

    def __repr__(self):
        return "<Section:%s %dx%d>" % (self.name, *self.size)


def createAll():
    return [
        OverworldSection("beach1", 0xE0, (2, 2)),
        OverworldSection("beach2", 0xE2, (2, 2)),
        OverworldSection("beach2", 0xE4, (2, 2)),
        OverworldSection("ghost_house", 0xE6, (2, 2)),
        OverworldSection("dungeon1", 0xC2, (2, 2)),
        OverworldSection("manu", 0xC4, (2, 2)),
        OverworldSection("pothole_field", 0xC6, (2, 2)),
        OverworldSection("town1", 0xA0, (2, 2)),
        OverworldSection("town2", 0xA2, (2, 2)),
        OverworldSection("town3", 0x82, (2, 2)),
        OverworldSection("fishing", 0x81, (1, 1)),
        OverworldSection("forest1", 0x40, (2, 2)),
        OverworldSection("forest2", 0x42, (2, 2)),
        OverworldSection("forest3", 0x60, (2, 2)),
        OverworldSection("forest4", 0x62, (2, 2)),
        OverworldSection("writes_cave", 0x20, (2, 2)),
        OverworldSection("swamp", 0x22, (3, 2)),
        OverworldSection("deadforest", 0x46, (2, 2)),
        OverworldSection("graveyard", 0x66, (2, 2)),
        OverworldSection("castle", 0x48, (4, 4)),
        OverworldSection("egg", 0x06, (1, 2)),
        OverworldSection("animal_village", 0xCC, (2, 2)),
        OverworldSection("desert", 0xCE, (2, 4)),
        OverworldSection("armos", 0xAC, (4, 2)),
        OverworldSection("dungeon3", 0xA5, (3, 2)),
        OverworldSection("dungeon7", 0x0E, (2, 2)),
        OverworldSection("dungeon8", 0x00, (3, 2)),
        OverworldSection("taltal1", 0x03, (1, 2)),
        OverworldSection("taltal2", 0x04, (2, 2)),
        OverworldSection("rapids", 0x4C, (4, 4)),
        OverworldSection("rafting_house", 0x2E, (2, 2)),
        OverworldSection("bay", 0xC8, (3, 3)),
        OverworldSection("donut", 0xA8, (2, 2)),
        OverworldSection("seashell_mansion", 0x8A, (2, 2)),
        OverworldSection("dungeon6", 0x8C, (2, 2)),
        OverworldSection("rivercrossing", 0xAA, (2, 1)),
        OverworldSection("moblincave", 0x25, (2, 2)),
        OverworldSection("trixy", 0x45, (1, 1)),
        OverworldSection("zombie", 0x74, (2, 1)),
        OverworldSection("witch", 0x65, (1, 1)),
        OverworldSection("mambo", 0x29, (2, 2)),
        OverworldSection("dungeon4", 0x1B, (1, 2)),
        OverworldSection("taltal3", 0x07, (2, 2)),
        OverworldSection("taltal4", 0x09, (2, 2)),
        OverworldSection("taltal5", 0x0C, (2, 2)),

        OverworldSection("warp0", 0x95, (1, 1)),
        OverworldSection("warp1", 0xEC, (2, 2)),
        OverworldSection("warp2", 0x2C, (2, 2)),
        OverworldSection("rapids_exit", 0x8E, (2, 2)),

        OverworldSection("filler1", 0xC0, (2, 2)),
        OverworldSection("filler2", 0x80, (1, 1)),
        OverworldSection("filler3", 0x90, (1, 1)),
        OverworldSection("filler4", 0x91, (1, 1)),
        OverworldSection("filler5", 0x44, (1, 1)),
        OverworldSection("filler6", 0x54, (1, 1)),
        OverworldSection("filler7", 0x55, (1, 1)),
        OverworldSection("filler8", 0x64, (1, 1)),
        OverworldSection("filler9", 0xA4, (1, 1)),
        OverworldSection("filler10", 0xB4, (1, 1)),
        OverworldSection("filler11", 0x84, (1, 2)),
        OverworldSection("filler12", 0x85, (1, 1)),
        OverworldSection("filler13", 0x86, (1, 1)),
        OverworldSection("filler14", 0x87, (1, 1)),
        OverworldSection("filler15", 0x96, (1, 1)),
        OverworldSection("filler16", 0x97, (2, 1)),
        OverworldSection("filler17", 0x88, (1, 1)),
        OverworldSection("filler18", 0x89, (1, 1)),
        OverworldSection("filler19", 0x99, (1, 1)),
        OverworldSection("filler20", 0xCB, (1, 1)),
        OverworldSection("filler21", 0xDB, (1, 1)),
        OverworldSection("filler22", 0x27, (2, 2)),
        OverworldSection("filler23", 0xEB, (1, 1)),
        OverworldSection("filler24", 0xF8, (1, 1)),
        OverworldSection("filler25", 0xFA, (1, 1)),
        OverworldSection("filler26", 0xFB, (1, 1)),
        OverworldSection("filler27", 0xF9, (1, 1)),
        OverworldSection("filler28", 0x3B, (1, 1)),
        OverworldSection("filler29", 0x0B, (1, 1)),

        OverworldSection("damn1", 0xBA, (1, 1)),
        OverworldSection("damn2", 0xBB, (1, 1)),
    ]