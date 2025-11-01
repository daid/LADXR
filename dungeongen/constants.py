DIR_X = {"up": 0, "down": 0, "left": -1, "right": 1}
DIR_Y = {"up": -1, "down": 1, "left": 0, "right": 0}
DIR_MIRROR = {"up": "down", "down": "up", "left": "right", "right": "left"}

TILE_FLOOR = 0x0D
TILE_UPPER = 0x0D

TILE_WALL_L = 0x23
TILE_WALL_R = 0x24
TILE_WALL_U = 0x21
TILE_WALL_D = 0x22

TILE_CONNECTIONS = {
    "up": [x for x in range(1, 9)],
    "down": [x+70 for x in range(1, 9)],
    "left": [y*10 for y in range(1, 7)],
    "right": [9+y*10 for y in range(1, 7)],
}
WALL_TILE = {
    "up": TILE_WALL_U,
    "down": TILE_WALL_D,
    "left": TILE_WALL_L,
    "right": TILE_WALL_R,
}
OPEN_DOOR_TILES = {
    "up": [0x43, 0x44],
    "down": [0x8C, 0x08],
    "left": [0x09, 0x0A],
    "right": [0x0B, 0x0C],
}
CLOSED_DOOR_TILES = {
    "up": [0x35, 0x36],
    "down": [0x37, 0x38],
    "left": [0x39, 0x3A],
    "right": [0x3B, 0x3C],
}
KEY_DOOR_TILES = {
    "up": [0x2D, 0x2E],
    "down": [0x2F, 0x30],
    "left": [0x31, 0x32],
    "right": [0x33, 0x34],
}
BOMB_WALL_TILE = {
    "up": 0x3F,
    "down": 0x40,
    "left": 0x41,
    "right": 0x42,
}
OPENING_TILES = {
    "up": [0x29, 0x2A],
    "down": [0x2B, 0x2C],
    "left": [0x29, 0x2B],
    "right": [0x2A, 0x2C],
}
OPENING_TILES_ALT = {
    "up": [TILE_WALL_L, TILE_WALL_R],
    "down": [TILE_WALL_L, TILE_WALL_R],
    "left": [TILE_WALL_U, TILE_WALL_D],
    "right": [TILE_WALL_U, TILE_WALL_D],
}
OPENING_FLOOR_TILES = {5, 13, 15}
TILE_TILESETS = {
    0xA3: [0x03, 0x0B, 0x0E],
    0xCB: [0x05, 0x0B, 0x0C],
    0x4E: [0x0C],
    0xDD: [0x05],
}
TILE_ANIMATION_SET = {
    0x0E: [3, 10, 11, 12],
    0x1B: [3, 11, 12],
    0xAB: [4, 6, 7],
    0xAC: [4, 6, 7],
    0xC7: [4, 7, 12],
    0xC8: [4, 7, 12],
    0xC9: [4, 7, 12],
    0xCA: [4, 7, 12],
}

ALL_CAVE_ROOM_IDS = [0x2B6, 0x2B7, 0x2B8, 0x2B9, 0x285, 0x286, 0x2F3, 0x2ED, 0x2EE, 0x2EA, 0x2EB, 0x2EC, 0x287, 0x2F1, 0x2F2, 0x2EF, 0x2BA, 0x2BB, 0x2BC, 0x28D, 0x2F9, 0x2FA, 0x280, 0x281, 0x282, 0x283, 0x284, 0x28C, 0x288, 0x28A, 0x290, 0x291, 0x292, 0x28E, 0x29A, 0x289, 0x28B]
