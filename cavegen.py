
DIR_X = {"up": 0, "down": 0, "left": -1, "right": 1}
DIR_Y = {"up": -1, "down": 1, "left": 0, "right": 0}
DIR_MIRROR = {"up": "down", "down": "up", "left": "right", "right": "left"}
TILE_FLOOR = 0x0D
TILE_UPPER = 0x0D
TILE_WALL_L = 0x23
TILE_WALL_R = 0x24
TILE_WALL_U = 0x21
TILE_WALL_D = 0x22
TILE_WALL_UL = 0x25
TILE_WALL_UR = 0x26
TILE_WALL_DL = 0x27
TILE_WALL_DR = 0x28
TILE_CONNECTIONS = {
    "big": {
        "up": {1: 0x29, 2: 0x0D, 3: 0x0D, 4: 0x0D, 5: 0x0D, 6: 0x0D, 7: 0x0D, 8: 0x2A},
        "down": {7*10+1: 0x02B, 7*10+2: 0x0D, 7*10+3: 0x0D, 7*10+4: 0x0D, 7*10+5: 0x0D, 7*10+6: 0x0D, 7*10+7: 0x0D, 7*10+8: 0x2C},
        "left": {1*10: 0x29, 2*10: 0x0D, 3*10: 0x0D, 4*10: 0x0D, 5*10: 0x0D, 6*10: 0x2B},
        "right": {1*10+9: 0x2A, 2*10+9: 0x0D, 3*10+9: 0x0D, 4*10+9: 0x0D, 5*10+9: 0x0D, 6*10+9: 0x2C},
    },
    "small": {
        "up": {3: 0x29, 4: 0x0D, 5: 0x0D, 6: 0x2A},
        "down": {7*10+3: 0x2B, 7*10+4: 0x0D, 7*10+5: 0x0D, 7*10+6: 0x2C},
        "left": {2*10: 0x29, 3*10: 0x0D, 4*10: 0x0D, 5*10: 0x2B},
        "right": {2*10+9: 0x2A, 3*10+9: 0x0D, 4*10+9: 0x0D, 5*10+9: 0x2C},
    },
    "door": {
        "up": {4: 0x43, 5: 0x44},
        "down": {7*10+4: 0x8C, 7*10+5: 0x08},
        "left": {3*10: 0x09, 4*10: 0x0A},
        "right": {3*10+9: 0x0B, 4*10+9: 0x0C},
    },
    "door-closed": {
        "up": {4: 0x35, 5: 0x36},
        "down": {7*10+4: 0x37, 7*10+5: 0x38},
        "left": {3*10: 0x39, 4*10: 0x3A},
        "right": {3*10+9: 0x3B, 4*10+9: 0x3C},
    },
    "bomb": {
        "up": {5: 0x3F},
        "down": {7*10+5: 0x40},
        "left": {4*10: 0x41},
        "right": {4*10+9: 0x42},
    },
}
ENEMY_TYPES = [
    "MOBLIN", "KEESE", "TEKTITE", "GHINI", "STALFOS", "GEL", "GIBDO", "LIKE_LIKE", "IRON_MASK",
    "MIMIC", "MINI_MOLDORM", "SPIKED_BEETLE", "TIMER_BOMBITE", "PAIRODD", "ANTI_KIRBY", "WATER_TEKTITE",
    "STAR", "GOOMBA", "PEAHAT", "SNAKE", "WINGED_OCTOROCK", "BOMBER", "VIRE", "SAND_CRAB", "POKEY",
    "COLOR_GHOUL",
]
MINIBOSS_TYPES = ["ROLLING_BONES", "HINOX", "DODONGO", "CUE_BALL", "GHOMA", "SMASHER", "GRIM_CREEPER", "BLAINO",
                  "AVALAUNCH", "GIANT_BUZZ_BLOB", "MOBLIN_KING", "ARMOS_KNIGHT"]

HAZARD_ENTITIES = {
    "MOBLIN": [(-1, -1, 0x0B), (-1, -1, 0x0B), (-1, -1, 0x0B), (-1, -1, 0x14)],
    "KEESE": [(-1, -1, 0x19), (-1, -1, 0x19), (-1, -1, 0x19), (-1, -1, 0x19)],
    "TEKTITE": [(-1, -1, 0x0D), (-1, -1, 0x0D), (-1, -1, 0x0D)],
    "GHINI": [(-1, -1, 0x12), (-1, -1, 0x12)],
    "STALFOS": [(-1, -1, 0x1A), (-1, -1, 0x1A), (-1, -1, 0x1E), (-1, -1, 0x1E)],
    "GEL": [(-1, -1, 0x1B), (-1, -1, 0x1B), (-1, -1, 0x1B), (-1, -1, 0x9B), (-1, -1, 0x9B)],
    "GIBDO": [(-1, -1, 0x1F), (-1, -1, 0x1F)],
    "WIZROBE": [(-1, -1, 0x21), (-1, -1, 0x21), (-1, -1, 0x21)],
    "LIKE_LIKE": [(-1, -1, 0x23), (-1, -1, 0x23)],
    "IRON_MASK": [(-1, -1, 0x24), (-1, -1, 0x24), (-1, -1, 0x24)],
    "MIMIC": [(-1, -1, 0x28), (-1, -1, 0x28)],
    "MINI_MOLDORM": [(-1, -1, 0x29)],
    "SPIKED_BEETLE": [(-1, -1, 0x2C), (-1, -1, 0x2C)],
    "BOUNCING_BOMBITE": [(-1, -1, 0x55), (-1, -1, 0x55), (-1, -1, 0x55)],
    "TIMER_BOMBITE": [(-1, -1, 0x56), (-1, -1, 0x56), (-1, -1, 0x56)],
    "PAIRODD": [(-1, -1, 0x57), (-1, -1, 0x57)],
    "ANTI_KIRBY": [(-1, -1, 0x91)],
    "WATER_TEKTITE": [(-1, -1, 0x99), (-1, -1, 0x99), (-1, -1, 0x99)],
    "STAR": [(-1, -1, 0x9C)],
    "GOOMBA": [(-1, -1, 0x9F), (-1, -1, 0x9F), (-1, -1, 0x9F)],
    "PEAHAT": [(-1, -1, 0xA0), (-1, -1, 0xA0)],
    "SNAKE": [(-1, -1, 0xA1), (-1, -1, 0xA1), (-1, -1, 0xA1)],
    "WINGED_OCTOROCK": [(-1, -1, 0xAE), (-1, -1, 0xAE)],
    "BOMBER": [(-1, -1, 0xBA)],
    "VIRE": [(-1, -1, 0xBD)],
    "SAND_CRAB": [(-1, -1, 0xC6), (-1, -1, 0xC6), (-1, -1, 0xC6)],
    "POKEY": [(-1, -1, 0xE3), (-1, -1, 0xE3)],
    "COLOR_GHOUL": [(-1, -1, 0xEC), (-1, -1, 0xED), (-1, -1, 0xEE)],

    "ROLLING_BONES": [(8, 3, 0x81), (6, 3, 0x82)],
    "HINOX": [(5, 2, 0x89)],
    "DODONGO": [(3, 2, 0x60), (5, 2, 0x60)],
    "CUE_BALL": [(1, 1, 0x8e)],
    "GHOMA": [(2, 1, 0x5e), (2, 4, 0x5e)],
    "SMASHER": [(5, 2, 0x92)],
    "GRIM_CREEPER": [(4, 0, 0xbc)],
    "BLAINO": [(5, 3, 0xbe)],
    "AVALAUNCH": [(5, 1, 0xf4)],
    "GIANT_BUZZ_BLOB": [(4, 2, 0xf8)],
    "MOBLIN_KING": [(5, 5, 0xe4)],
    "ARMOS_KNIGHT": [(4, 3, 0x88)],
}

class RoomConnection:
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.direction = None
        self.type = None

    def __repr__(self):
        return f"RC<:{self.source}->{self.target}:{self.direction}:{self.type}>"


class Room:
    def __init__(self, *, type="normal"):
        self.connections = []
        self.hazard = None
        self.type = type
        self.x = None
        self.y = None
        self.source = None
        self.tiles = []
        self.entities = []
        self.event = 0
        self.room_id = None

    def add_room(self, type="normal"):
        if len(self.connections) == 3:
            return None
        r = Room(type=type)
        self.connections.append(RoomConnection(self, r))
        r.source = self.connections[-1]
        return r

    @property
    def xy(self):
        return (self.x, self.y)

    def __repr__(self):
        return f"ROOM{{{self.x},{self.y}}}"

class Generator:
    def __init__(self, rng):
        self.rng = rng
        self.start = None
        self.end = None
        self.main_chain = []
        self.all_rooms = []

    def layout_map(self):
        self.start.x = 0
        self.start.y = 0
        room_map = {self.start.xy: self.start}
        todo = [self.start]
        while todo:
            r = todo.pop(0)
            dirs = ["up", "down", "left", "right"]
            self.rng.shuffle(dirs)
            for c in r.connections:
                while c.direction is None:
                    if not dirs:
                        raise CaveGenFailed("Cannot layout map")
                    c.direction = dirs.pop(0)
                    c.target.x = c.source.x + DIR_X[c.direction]
                    c.target.y = c.source.y + DIR_Y[c.direction]
                    if c.target.xy in room_map:
                        c.direction = None
                    else:
                        room_map[c.target.xy] = c.target
                        todo.append(c.target)
        minx = min(xy[0] for xy in room_map)
        miny = min(xy[1] for xy in room_map)
        shiftx = -minx
        shifty = -miny
        for room in room_map.values():
            room.x += shiftx
            room.y += shifty

    def setup_connection_types(self):
        for room in self.all_rooms:
            for c in room.connections:
                c.type = self.rng.choice(["big", "small", "door", "bomb"])
                if c.type == "bomb" and room in self.main_chain and c.target in self.main_chain:
                    if self.rng.randrange(0, 100) < 70:
                        c.type = self.rng.choice(["big", "small", "door"])

    def set_room_types(self):
        # First find end side rooms and turn those potentially in reward rooms
        for room in [room for room in self.all_rooms if not room.connections and room.type == "side"]:
            if self.rng.randrange(0, 100) < 70:
                room.type = "reward"
        # Next give each other room a 10% chance of having a reward
        for room in [room for room in self.all_rooms if room.type in {"side", "normal"}]:
            if self.rng.randrange(0, 100) < 10:
                room.type = "reward"
        # Now, find rooms to put enemy hazards in.
        for room in [room for room in self.all_rooms if room.type not in {"start", "end"}]:
            if self.rng.randrange(0, 100) < (70 if room.type != "reward" else 40):
                room.hazard = "enemy"
        # potentially add a single miniboss
        if self.rng.randrange(0, 100) < 70:
            potential_miniboss_rooms = [room for room in self.all_rooms if room.hazard == "enemy" and room.connections]
            if potential_miniboss_rooms:
                room = self.rng.choice(potential_miniboss_rooms)
                room.type = "miniboss"
                room.hazard = "miniboss"
                room.event = 0x21  # Open doors on kill all
                room.source.type = "door"
                for c in room.connections:
                    c.type = "door"

        # Apply actual enemies
        for room in [room for room in self.all_rooms if room.hazard == "enemy"]:
            room.hazard = self.rng.choice(ENEMY_TYPES)
        for room in [room for room in self.all_rooms if room.hazard == "miniboss"]:
            room.hazard = self.rng.choice(MINIBOSS_TYPES)

        # Setup actual rewards
        for room in [room for room in self.all_rooms if room.type == "reward"]:
            if room.hazard and self.rng.randrange(0, 100) < 70:
                room.type = "chest" # TODO: "hidden-chest"
            else:
                room.type = "chest"

        # Setup entities for hazards
        for room in [room for room in self.all_rooms if room.hazard]:
            first = True
            for x, y, entity in HAZARD_ENTITIES[room.hazard]:
                if x < 0:
                    x = self.rng.randint(1, 8)
                    y = self.rng.randint(1, 6)
                    if not first and self.rng.randrange(0, 100) < 20:
                        continue
                    first = False
                room.entities.append((x, y, entity))

    def build_room_tiles(self, room):
        tiles = [TILE_FLOOR] * 10 * 8
        for x in range(10):
            tiles[x] = TILE_WALL_U
            tiles[10*7+x] = TILE_WALL_D
        for y in range(8):
            tiles[y*10] = TILE_WALL_L
            tiles[y*10+9] = TILE_WALL_R
        tiles[0] = TILE_WALL_UL
        tiles[9] = TILE_WALL_UR
        tiles[10*7] = TILE_WALL_DL
        tiles[10*7+9] = TILE_WALL_DR
        if room.source:
            ctype = room.source.type
            if room.event == 0x21 and ctype == "door":
                ctype = "door-closed"
            for k, v in TILE_CONNECTIONS[ctype][DIR_MIRROR[room.source.direction]].items():
                tiles[k] = v
        for c in room.connections:
            ctype = c.type
            if room.event == 0x21 and ctype == "door":
                ctype = "door-closed"
            for k, v in TILE_CONNECTIONS[ctype][c.direction].items():
                tiles[k] = v
        if room.type == "start":
            tiles[4*10+5] = 0xCB
        if room.type == "chest":
            tiles[3*10+5] = 0xA0

        room.tiles = tiles

    def get_reward_count(self) -> int:
        return sum(1 for room in self.all_rooms if room.type in {"chest", "hidden-chest"})

    def generate(self):
        for n in range(100):
            try:
                self._generate()
                return
            except CaveGenFailed:
                pass
        raise CaveGenFailed("Failed after 100 tries")

    def _generate(self):
        self.start = Room(type="start")
        self.end = self.start
        self.main_chain = [self.start]
        self.all_rooms = [self.start]
        for n in range(self.rng.randint(4, 6)):
            self.end = self.end.add_room()
            self.main_chain.append(self.end)
            self.all_rooms.append(self.end)
        side_room = None
        side_room_count = min(self.rng.randint(8, 11) - len(self.main_chain), 5)
        for n in range(side_room_count):
            if side_room is None or self.rng.randrange(0, 100) < 50:
                side_room = self.main_chain[self.rng.randint(1, len(self.main_chain) - 2)].add_room("side")
            else:
                side_room = side_room.add_room("side")
            if side_room is not None:
                self.all_rooms.append(side_room)
        self.end.type = "end"
        self.layout_map()
        self.setup_connection_types()
        self.set_room_types()
        cave_room_ids = [0x2B6, 0x2B7, 0x2B8, 0x2B9, 0x285, 0x286, 0x2F3, 0x2ED, 0x2EE, 0x2EA, 0x2EB, 0x2EC, 0x287, 0x2F1, 0x2F2, 0x2EF, 0x2BA, 0x2BB, 0x2BC, 0x28D, 0x2F9, 0x2FA, 0x280, 0x281, 0x282, 0x283, 0x284, 0x28C, 0x288, 0x28A, 0x290, 0x291, 0x292, 0x28E, 0x29A, 0x289, 0x28B]
        for room in self.all_rooms:
            room.room_id = cave_room_ids.pop()
            self.build_room_tiles(room)
        return self.start


class CaveGenFailed(Exception):
    pass


def dump(filename, *starts):
    f = open(filename, "wt")
    f.write('<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="700">')
    for start_idx, start in enumerate(starts):
        f.write(f'<g transform="scale(100 100) translate({(start_idx%4)*8} {(start_idx//4)*8})">')
        def dumpRoom(r):
            for c in r.connections:
                col = "#000"
                if c.type == "bomb":
                    col = "#F00"
                f.write(f'<line x1="{r.x+.4}" y1="{r.y+.4}" x2="{c.target.x+.4}" y2="{c.target.y+.4}" stroke="{col}" stroke-width="0.1" />')
                dumpRoom(c.target)
            col = "#FFF"
            if r.type == "start":
                col = "#F88"
            if r.type == "end":
                col = "#8F8"
            if r.type == "side":
                col = "#88F"
            if r.type in {"chest", "hidden-chest"}:
                col = "#8FF"
            f.write(f'<rect x="{r.x}" y="{r.y}" width="0.8" height="0.8" fill="{col}" stroke="#000" stroke-width="0.1" />')
            f.write(f'<text x="{r.x+.1}" y="{r.y+.1}" alignment-baseline="hanging" font-size="0.2">{r.type}</text>')
            if r.hazard:
                f.write(f'<text x="{r.x+.1}" y="{r.y+.3}" alignment-baseline="hanging" font-size="0.2">{r.hazard}</text>')
        dumpRoom(start)
        f.write("</g>")
    f.write("</svg>")
    f.close()


if __name__ == "__main__":
    import sys
    import romTables
    from roomEditor import RoomEditor
    import random
    import mapexport
    rng = random.Random()
    cave = Generator(rng).generate()
    dump("cave.svg", cave)

    rom = romTables.ROMWithTables(open(sys.argv[1], "rb"))
    for x in range(8):
        for y in range(8):
            rom.banks[0x14][0x0220 + 10 * 8*8 + x + y * 8] = 0
    cave_room_ids = [0x2B6, 0x2B7, 0x2B8, 0x2B9, 0x285, 0x286, 0x2F3, 0x2ED, 0x2EE, 0x2EA, 0x2EB, 0x2EC, 0x287, 0x2F1, 0x2F2, 0x2EF, 0x2BA, 0x2BB, 0x2BC, 0x28D, 0x2F9, 0x2FA, 0x280, 0x281, 0x282, 0x283, 0x284, 0x28C, 0x288, 0x28A, 0x290, 0x291, 0x292, 0x28E, 0x29A, 0x289, 0x28B]
    def place(room):
        room_id = cave_room_ids.pop()
        rom.banks[0x14][0x0220 + 10 * 8*8 + room.x + room.y * 8] = room_id & 0xFF
        re = RoomEditor(rom, room_id)
        re.entities = []
        re.buildObjectList(room.tiles)
        re.store(rom)
        for c in room.connections:
            place(c.target)
    place(cave)

    for ri in cave_room_ids:
        re = RoomEditor(rom, ri)
        re.entities = []
        re.objects = []
        re.store(rom)
    mapexport.MapExport(rom).export_all()
