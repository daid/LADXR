from locations.items import *
from .constants import *
from .roomtemplates import ROOM_TEMPLATES
from typing import Tuple, Optional, Set
import math


class RoomConnection:
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.direction = None
        self.type = None
        self.offset = 0
        self.size = 2

    def set_type(self, value):
        self.type = value
        if value == 'bomb':
            self.size = 1
        elif value == 'big':
            self.size = 6
            self.type = 'opening'
        elif value == 'small':
            self.size = 3
            self.type = 'opening'
        else:
            self.size = 2

    def __repr__(self):
        return f"RC<:{self.source}->{self.target}:{self.direction}:{self.type}>"


class Room:
    def __init__(self, *, rtype="normal"):
        self.connections = []
        self.type = rtype
        self.x = None
        self.y = None
        self.source = None
        self.tiles = []
        self.entities = []
        self.room_id = None
        self.template = None

    def add_room(self, rtype="normal"):
        if len(self.connections) == 3:
            return None
        r = Room(rtype=rtype)
        self.connections.append(RoomConnection(self, r))
        r.source = self.connections[-1]
        return r

    def get_connection(self, direction):
        if self.source and self.source.direction == DIR_MIRROR[direction]:
            return self.source
        for c in self.connections:
            if c.direction == direction:
                return c
        return None

    def get_tileset_id(self):
        print("get_tileset_id")
        tileset_ids: Optional[Set[int]] = None
        for tile in self.tiles:
            if tile in TILE_TILESETS:
                if tileset_ids is None:
                    tileset_ids = set(TILE_TILESETS[tile])
                else:
                    tileset_ids = tileset_ids.intersection(set(TILE_TILESETS[tile]))
        if tileset_ids:
            print(tileset_ids)
            return next(iter(tileset_ids))
        return 0xFF

    def get_animation_id(self):
        animation_ids: Optional[Set[int]] = None
        for tile in self.tiles:
            if tile in TILE_ANIMATION_SET:
                if animation_ids is None:
                    animation_ids = set(TILE_ANIMATION_SET[tile])
                else:
                    animation_ids = animation_ids.intersection(set(TILE_ANIMATION_SET[tile]))
        if animation_ids:
            return next(iter(animation_ids))
        return 0x0B

    @property
    def xy(self) -> Tuple[int, int]:
        return self.x, self.y

    def __repr__(self):
        return f"ROOM{{{self.x},{self.y}}}"


class Generator:
    ROOM_IDS_PER_MAP = {
        0x00: [n for n in range(0x101, 0x120)],
        0x01: [n for n in range(0x120, 0x140)],
        0x02: [n for n in range(0x140, 0x15D)],
        0x03: [n for n in range(0x160, 0x17E)],
        0x04: [n for n in range(0x180, 0x1AC)],
        0x05: [n for n in range(0x1B0, 0x1DE)],
        0x06: [n for n in range(0x201, 0x22F)],
        0x07: [n for n in range(0x230, 0x26C)],
        0x0A: ALL_CAVE_ROOM_IDS
    }

    def __init__(self, rng, map_id=0x0A):
        self.rng = rng
        self.map_id = map_id
        self.start = None
        self.end = None
        self.main_chain = []
        self.all_rooms = []

    def layout_map(self):
        self.start.x = 0
        self.start.y = 0
        min_x, max_x = 0, 0
        min_y, max_y = 0, 0
        room_map = {self.start.xy: self.start}
        todo = [self.start]
        while todo:
            r = todo.pop(0)
            dirs = ["up", "down", "left", "right"]
            self.rng.shuffle(dirs)
            for c in r.connections:
                while c.direction is None:
                    if not dirs:
                        raise DungeonGenFailed("Cannot layout map")
                    c.direction = dirs.pop(0)
                    c.target.x = c.source.x + DIR_X[c.direction]
                    c.target.y = c.source.y + DIR_Y[c.direction]
                    if c.target.xy in room_map or abs(min_x - c.target.x) > 7 or abs(max_x - c.target.x) > 7 or abs(
                            min_y - c.target.y) > 7 or abs(max_y - c.target.y) > 7:
                        c.direction = None
                    else:
                        min_x = min(min_x, c.target.x)
                        max_x = max(max_x, c.target.x)
                        min_y = min(min_y, c.target.y)
                        max_y = max(max_y, c.target.y)
                        room_map[c.target.xy] = c.target
                        todo.append(c.target)
        minx = min(xy[0] for xy in room_map)
        miny = min(xy[1] for xy in room_map)
        shiftx = -minx
        shifty = -miny
        for room in room_map.values():
            room.x += shiftx
            room.y += shifty

    def add_key_doors(self):
        max_keys = max(0, (len(self.main_chain) - 3) // 4)
        total_keys = self.rng.randrange(max_keys // 2, max_keys)
        for n in range(total_keys):
            idx = self.rng.randrange(4, len(self.main_chain))
            self.main_chain[idx].source.type = "key"

    def set_room_types(self):
        # First find end side rooms and turn those potentially in reward rooms
        for room in [room for room in self.all_rooms if not room.connections and room.type == "side"]:
            if self.rng.randrange(0, 100) < 85:
                room.type = "reward"
        # Next give each other room a 20% chance of having a reward
        for room in [room for room in self.all_rooms if room.type in {"side", "normal"}]:
            if self.rng.randrange(0, 100) < 20:
                room.type = "reward"

        # Set a template for each room
        for room in self.all_rooms:
            possible_templates = []
            for template in ROOM_TEMPLATES:
                if not template.match_room_type(room.type):
                    continue
                allowed = True
                for d in DIR_MIRROR.keys():
                    connection = room.get_connection(d)
                    open = connection is not None
                    if open:
                        if not template.can_be_open(d):
                            allowed = False
                        if connection.target == room:
                            if not template.can_be_connected_to(connection.source.template, d):
                                allowed = False
                        if connection.type and not template.can_have_connection_of_type(d, connection.type):
                            allowed = False
                    elif not template.can_be_closed(d):
                        allowed = False

                if allowed:
                    possible_templates.append(template)
            if not possible_templates:
                print(room, room.type)
                print(room.source.source.template.name, room.source)
            room.template = self.rng.choice(possible_templates)
            if room.source:
                if room.source.type is None:
                    if room.source.source.template.event == 0x21 or room.template.event == 0x21:
                        room.source.set_type("door")
                    else:
                        room.source.set_type(self.rng.choice(["big", "small", "door", "bomb"]))
                    if room.source.type == "bomb" and room in self.main_chain and room.source.target in self.main_chain:
                        if self.rng.randrange(0, 100) < 70:
                            room.source.set_type(self.rng.choice(["big", "small", "door"]))
                options = room.template.possible_door_positions(room.source.source.template,
                                                                DIR_MIRROR[room.source.direction], room.source.size)
                while not options:
                    room.source.size -= 1
                    assert room.source.size >= 1, room.template.name
                    options = room.template.possible_door_positions(room.source.source.template,
                                                                    DIR_MIRROR[room.source.direction], room.source.size)
                if room.source.size == 2 and room.source.type not in {"door", "key"}:
                    room.source.type = "door"
                if room.source.size == 1:
                    if self.rng.randrange(0, 100) < 40:
                        room.source.type = "bomb"
                    else:
                        room.source.type = "opening"
                if len(options) == 1 and isinstance(options[0], tuple):
                    room.source.type = options[0][0]
                    room.source.offset = options[0][1]
                    room.source.size = options[0][2]
                else:
                    room.source.offset = self.rng.choice(options)

    def build_room_tiles(self, room):
        tiles = [TILE_FLOOR] * 10 * 8
        for n in range(10 * 8):
            tiles[n] = room.template.tiles[n]
        for d in DIR_MIRROR.keys():
            for n in TILE_CONNECTIONS[d]:
                if tiles[n] == -1:
                    tiles[n] = WALL_TILE[d]
            connection = room.get_connection(d)
            if connection:
                if connection.type == 'door':
                    if room.template.event == 0x21:
                        for idx in range(connection.size):
                            tiles[TILE_CONNECTIONS[d][idx + connection.offset]] = CLOSED_DOOR_TILES[d][idx]
                    else:
                        for idx in range(connection.size):
                            tiles[TILE_CONNECTIONS[d][idx + connection.offset]] = OPEN_DOOR_TILES[d][idx]
                elif connection.type == 'key':
                    for idx in range(connection.size):
                        tiles[TILE_CONNECTIONS[d][idx + connection.offset]] = KEY_DOOR_TILES[d][idx]
                elif connection.type == 'bomb':
                    for idx in range(connection.size):
                        tiles[TILE_CONNECTIONS[d][idx + connection.offset]] = BOMB_WALL_TILE[d]
                elif connection.type == 'opening':
                    for idx in range(connection.size):
                        tiles[TILE_CONNECTIONS[d][idx + connection.offset]] = TILE_FLOOR
                    if connection.size > 2:
                        tiles[TILE_CONNECTIONS[d][connection.offset]] = OPENING_TILES[d][0]
                        tiles[TILE_CONNECTIONS[d][connection.size + connection.offset - 1]] = OPENING_TILES[d][1]
                else:
                    print(connection.type)

        for n in range(10 * 8):
            if tiles[n] == -1:
                tiles[n] = 1

        room.tiles = tiles
        if room.template.entities:
            room.entities = [(x, y, e) for x, y, e in room.template.entities]

    def get_reward_count(self) -> int:
        return sum(1 for room in self.all_rooms if room.type in {"reward"})

    def get_logic_requirements(self, inventory):
        result = set()
        key_count = 0
        for room in self.all_rooms:
            if room.source:
                if room.source.type == "bomb" and BOMB not in inventory:
                    result.add(BOMB)
                if room.source.type == "key":
                    key_count += 1
            if room.template.logic is None:
                continue
            if isinstance(room.template.logic, str):
                if room.template.logic not in inventory:
                    result.add(room.template.logic)
            else:
                room.template.logic.getItems(inventory, result)
        if key_count > inventory.get(f"KEY{self.map_id + 1}", 0):
            result.add(f"KEY{self.map_id + 1}")
        return result

    def generate(self) -> Room:
        for n in range(100):
            try:
                return self._generate()
            except DungeonGenFailed:
                pass
        raise DungeonGenFailed("Failed after 100 tries")

    def _generate(self) -> Room:
        self.start = Room(rtype="start")
        self.end = self.start
        self.main_chain = [self.start]
        self.all_rooms = [self.start]
        for n in range(self.rng.randint(4, 6)):
        # for n in range(self.rng.randint(12, 18)):
            self.end = self.end.add_room()
            self.main_chain.append(self.end)
            self.all_rooms.append(self.end)
        side_room = None
        side_room_count = min(self.rng.randint(8, 11) - len(self.main_chain), 5)
        # side_room_count = min(self.rng.randint(20, 29) - len(self.main_chain), 16)
        for n in range(side_room_count):
            if side_room is None or self.rng.randrange(0, 100) < 50:
                side_room = self.all_rooms[self.rng.randint(0, len(self.all_rooms) - 1)].add_room("side")
            else:
                side_room = side_room.add_room("side")
            if side_room is not None:
                self.all_rooms.append(side_room)
        self.end.type = "end"
        self.layout_map()
        if self.map_id < 8:
            self.add_key_doors()
        self.set_room_types()
        cave_room_ids = self.ROOM_IDS_PER_MAP[self.map_id].copy()
        for room in self.all_rooms:
            room.room_id = cave_room_ids.pop()
            self.build_room_tiles(room)
        return self.start


class DungeonGenFailed(Exception):
    pass


def dump(filename, *gens):
    f = open(filename, "wt")
    scale = 40
    row_width = math.ceil(math.sqrt(len(gens)))
    rows = (len(gens) + row_width - 1) // row_width
    f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{row_width * scale * 8}" height="{rows * scale * 8}">')
    for gen_idx, gen in enumerate(gens):
        f.write(
            f'<g transform="scale({scale} {scale}) translate({(gen_idx % row_width) * 8} {(gen_idx // row_width) * 8})">')

        def dumpRoom(r):
            for c in r.connections:
                col = "#000"
                if c.type == "key":
                    col = "#00F"
                if c.type == "bomb":
                    col = "#F00"
                f.write(
                    f'<line x1="{r.x + .4}" y1="{r.y + .4}" x2="{c.target.x + .4}" y2="{c.target.y + .4}" stroke="{col}" stroke-width="0.1" />')
                dumpRoom(c.target)
            col = "#FFF"
            if r.type == "start":
                col = "#F88"
            if r.type == "end":
                col = "#8F8"
            if r.type == "side" or r not in gen.main_chain:
                col = "#88F"
            if r.type in {"chest", "item"}:
                col = "#8FF"
            f.write(
                f'<rect x="{r.x}" y="{r.y}" width="0.8" height="0.8" fill="{col}" stroke="#000" stroke-width="0.1" />')
            f.write(f'<text x="{r.x + .1}" y="{r.y + .3}" alignment-baseline="hanging" font-size="0.2">{r.type}</text>')

        dumpRoom(gen.start)
        f.write("</g>")
    f.write("</svg>")
    f.close()

