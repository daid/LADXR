from .constants import *
from typing import Tuple


class RoomTemplate:
    BOMB_WALL_TILES = {0x3F, 0x40, 0x41, 0x42, 0x47, 0x48, 0x49, 0x4A}

    def __init__(self, *, name, user, logic=None, entities=None, tiles, event=0):
        self.name = name
        self.user = user
        self.logic = logic
        self.type = "normal"
        self.entities = entities
        self.tiles = tiles
        self.event = event
        self.specific_doors = {}  # key: direction, if key not set, then has ?? walls, null=no entrance, else tuple of (type, position, size) for door type.
        for d in DIR_MIRROR.keys():
            if self._check_any_edge_tiles(d, {-1,}):
                continue
            for idx in range(len(TILE_CONNECTIONS[d])-1):
                if self.tiles[TILE_CONNECTIONS[d][idx]] in self.BOMB_WALL_TILES:
                    self.specific_doors[d] = ('bomb', idx, 1)
            if d not in self.specific_doors:
                for idx in range(len(TILE_CONNECTIONS[d])-1):
                    if self.tiles[TILE_CONNECTIONS[d][idx]] == OPEN_DOOR_TILES[d][0] and self.tiles[TILE_CONNECTIONS[d][idx+1]] == OPEN_DOOR_TILES[d][1]:
                        self.specific_doors[d] = ('door', idx, 2)
            if d not in self.specific_doors:
                for idx in range(len(TILE_CONNECTIONS[d])-2):
                    if self.tiles[TILE_CONNECTIONS[d][idx]] in {OPENING_TILES[d][0], OPENING_TILES_ALT[d][0]} and self.tiles[TILE_CONNECTIONS[d][idx+1]] in OPENING_FLOOR_TILES:
                        s = 2
                        while idx + s < len(TILE_CONNECTIONS[d]) - 1 and self.tiles[TILE_CONNECTIONS[d][idx+s]] in OPENING_FLOOR_TILES:
                            s += 1
                        if self.tiles[TILE_CONNECTIONS[d][idx+s]] in {OPENING_TILES[d][1], OPENING_TILES_ALT[d][1]}:
                            self.specific_doors[d] = ('opening', idx, s+1)

            if d not in self.specific_doors:
                # if self._check_any_edge_tiles(d, OPENING_FLOOR_TILES):
                #     print("What?", self.name, d)
                self.specific_doors[d] = None
        if 0xA0 in self.tiles:
            self.type = "chest"
        if 0xA3 in self.tiles or 0xBE in self.tiles or 0xCB in self.tiles:
            if self.entities:
                self.type = "stairs-danger"
            else:
                self.type = "stairs"
        if self.event == 0x61:
            self.type = "chest"
        elif self.event == 0x81:
            self.type = "item"

    def match_room_type(self, room_type):
        if room_type == "reward":
            return self.type in {"chest", "item"}
        if room_type == "start":
            return self.type == "stairs"
        if room_type == "end":
            return self.type in {"stairs", "stairs-danger"}
        return self.type == "normal"

    def has_choice(self, direction):
        return direction not in self.specific_doors

    def can_be_open(self, direction):
        return direction not in self.specific_doors or self.specific_doors[direction] is not None

    def can_be_closed(self, direction):
        return direction not in self.specific_doors or self.specific_doors[direction] is None

    def can_be_connected_to(self, target_template, direction):
        return len(self.possible_door_positions(target_template, direction)) > 0

    def can_have_connection_of_type(self, direction, connection_type):
        if direction in self.specific_doors:
            door = self.specific_doors[direction]
            if not door:
                return False
            if door[0] == 'door' and connection_type in {'door', 'key'}:
                return True
            return door[0] == connection_type
        gap_size = 0
        for idx in TILE_CONNECTIONS[direction]:
            if self.tiles[idx] == -1:
                gap_size += 1
                if gap_size >= 2:
                    return True
            else:
                gap_size = 0
        return False

    def possible_door_positions(self, target_template, direction, size=1):
        if direction in self.specific_doors:
            my_door = self.specific_doors[direction]
            if my_door is None:
                return []
            if DIR_MIRROR[direction] in target_template.specific_doors:
                other_door = target_template.specific_doors[DIR_MIRROR[direction]]
                if my_door == other_door:
                    return [my_door]
                return []
            for n in range(my_door[2]):
                if target_template.tiles[TILE_CONNECTIONS[DIR_MIRROR[direction]][n+my_door[1]]] != -1:
                    return []
            return [my_door]
        if DIR_MIRROR[direction] in target_template.specific_doors:
            other_door = target_template.specific_doors[DIR_MIRROR[direction]]
            if other_door is None:
                return []
            for n in range(other_door[2]):
                if self.tiles[TILE_CONNECTIONS[direction][n+other_door[1]]] != -1:
                    return []
            return [other_door]
        result = []
        overlap = 0
        for idx, (s, d) in enumerate(zip(TILE_CONNECTIONS[direction], TILE_CONNECTIONS[DIR_MIRROR[direction]])):
            if self.tiles[s] == -1 and target_template.tiles[d] == -1:
                overlap += 1
                if overlap == size:
                    overlap -= 1
                    result.append(idx - overlap)
            else:
                overlap = 0
        return result

    def get_stairs_position(self) -> Tuple[int, int]:
        for y in range(8):
            for x in range(10):
                if self.tiles[x+y*10] in {0xA3, 0xBE, 0xCB}:
                    return x, y
        raise RuntimeError("Stairs not found...")

    def _check_any_edge_tiles(self, direction, check_set):
        for n in TILE_CONNECTIONS[direction]:
            if self.tiles[n] in check_set:
                return True
        return False
