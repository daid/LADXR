from typing import Optional, List, Tuple


# Class which can read various metadata about rooms from the rom
# This is independent of the RoomEditor, which concerns itself mostly with what tiles are where.
#   this info instead is more about how the room is rendered.
class RoomInfo:
    def __init__(self, rom, room_nr: int, map_id: int, sidescroll: bool):
        self.room_nr = room_nr
        self.map_id = map_id
        self.sidescroll = sidescroll

        # Get the tileset id, which is important for which subgraphics to load
        if room_nr < 0x100:
            self.main_tileset_id = rom.banks[0x20][0x2E73 + (room_nr & 0x0F) // 2 + ((room_nr >> 5) * 8)]
            if rom.banks[0x3F][0x3F00 + room_nr]:  # If we have the per room tileset patch, use that data
                self.main_tileset_id = rom.banks[0x3F][0x3F00 + room_nr]
            elif rom.banks[0x3F][0x2F00 + room_nr]:  # Older style per-room-tileset patch
                self.main_tileset_id = rom.banks[0x3F][0x2F00 + room_nr]
        else:
            self.main_tileset_id = rom.banks[0x20][0x2EB3 + room_nr - 0x100]
        
        # Get which graphics attribute table to use, nicely overly complicated...
        if room_nr < 0x100:
            self.attribute_bank = rom.banks[0x1A][0x2476 + room_nr]
            self.attribute_addr = rom.banks[0x1A][0x1E76 + room_nr * 2]
            self.attribute_addr |= rom.banks[0x1A][0x1E76 + room_nr * 2 + 1] << 8
        elif room_nr >= 0x300:
            self.attribute_bank = 0x23
            self.attribute_addr = 0x6000
        else:
            if room_nr < 0x200:
                self.attribute_bank = 0x23
            else:
                self.attribute_bank = 0x24
            underworld_offset = (room_nr & 0xF00)
            if map_id == 6 or map_id == 7:
                self.attribute_bank = 0x23
                underworld_offset = 0x100
            self.attribute_addr = rom.banks[0x1A][0x1E76 + underworld_offset * 2 + map_id * 2]
            self.attribute_addr |= rom.banks[0x1A][0x1E76 + underworld_offset * 2 + map_id * 2 + 1] << 8
        
        # Find the palette to use, this is a bit weird, and also overly complicated (most DX related stuff is)
        if room_nr < 0x100:
            self.palette_index = rom.banks[0x21][0x02EF + room_nr]
            self._palette_addr_table = [(rom.banks[0x21][0x02B1+n*2] | (rom.banks[0x21][0x02B1+1+n*2] << 8)) for n in range(0x1F)]
            self._palette_addr = None
        elif room_nr >= 0x300:
            self.palette_index = None
            self._palette_addr_table = None
            self._palette_addr = 0x67D0
        else:
            if map_id < 9:
                self.palette_index = None
                self._palette_addr_table = None
                addr = 0x0401 if self.sidescroll else 0x03EF
                self._palette_addr = rom.banks[0x21][addr + map_id*2] | (rom.banks[0x21][addr + 1 + map_id*2] << 8)
                if room_nr in {0x264, 0x265, 0x266, 0x267, 0x26A, 0x26B}:
                    self._palette_addr = 0x2750  # Specific D8 sidescroll overrules
            else:
                per_map_lookup_addr = rom.banks[0x21][0x0413 + (map_id - 10)*2] | (rom.banks[0x21][0x0414 + (map_id - 10)*2] << 8)
                self.palette_index = rom.banks[0x21][per_map_lookup_addr - 0x4000 + (self.room_nr & 0xFF)]
                self._palette_addr_table = [(rom.banks[0x21][0x043F + n * 2] | (rom.banks[0x21][0x0440 + n * 2] << 8)) for n in range(0x23)]
                self._palette_addr = None

        # 16x16 -> 8x8 metatiles info
        if room_nr < 0x100:
            self.metatile_bank = 0x1A
            self.metatile_addr = 0x6B1D
        elif room_nr < 0x300:
            self.metatile_bank = 0x08
            self.metatile_addr = 0x43B0
        else: # color dungeon
            self.metatile_bank = 0x08
            self.metatile_addr = 0x4760

        # Physics
        self.physics_bank = 0x08
        if room_nr < 0x100: # Check if color dungeon also uses this table... (code at 00:2A12 is sus)
            self.physics_addr = 0x4AD4
        else:
            self.physics_addr = 0x4BD4

        # For underworld, we need some extra info for what floor/wall tiles to use depending on the map.
        if self.room_nr >= 0x300:
            self.wall_tiles_bank = 0x2D
            self.wall_tiles_ptr = 0x0A00
            self.floor_tiles_bank = 0x35
            self.floor_tiles_ptr = 0x2000
            #TODO: This is wrong.
            self.item_tiles_bank = 0x32
            self.item_tiles_ptr = 0x3800
        elif self.room_nr >= 0x100:        
            self.wall_tiles_bank = 0x2D
            self.wall_tiles_ptr = rom.banks[0x20][0x05A9 + self.map_id] * 0x100 - 0x4000
            self.floor_tiles_bank = 0x2D
            self.floor_tiles_ptr = rom.banks[0x20][0x0589 + self.map_id] * 0x100 - 0x4000
            self.item_tiles_bank = 0x32
            self.item_tiles_ptr = rom.banks[0x20][0x05CA + self.map_id] * 0x100 - 0x4000

    def store(self, rom):
        if self.room_nr < 0x100:
            rom.banks[0x3F][0x3F00 + self.room_nr] = self.main_tileset_id
        else:
            rom.banks[0x20][0x2EB3 + self.room_nr - 0x100] = self.main_tileset_id

        if self.room_nr < 0x100:
            rom.banks[0x1A][0x2476 + self.room_nr] = self.attribute_bank
            rom.banks[0x1A][0x1E76 + self.room_nr * 2] = self.attribute_addr & 0xFF
            rom.banks[0x1A][0x1E76 + self.room_nr * 2 + 1] = (self.attribute_addr >> 8) | 0x40

        # Find the palette to use, this is a bit weird, and also overly complicated (most DX related stuff is)
        if self.room_nr < 0x100:
            rom.banks[0x21][0x02EF + self.room_nr] = self.palette_index
        elif self.room_nr >= 0x300:
            pass
        else:
            if self.map_id < 9:
                pass
            else:
                per_map_lookup_addr = rom.banks[0x21][0x0413 + (self.map_id - 10) * 2] | (rom.banks[0x21][0x0414 + (self.map_id - 10) * 2] << 8)
                rom.banks[0x21][per_map_lookup_addr - 0x4000 + (self.room_nr & 0xFF)] = self.palette_index

    @property
    def palette_addr(self):
        if self._palette_addr is not None:
            return self._palette_addr
        return self._palette_addr_table[self.palette_index]

    # Get a list of 8x8 graphic tile addresses for this room.
    def getTileset(self, animation_id: Optional[int], switch_blocks=False):
        subtiles: List[Optional[Tuple[int, int]]] = [None] * 0x100
        if self.room_nr < 0x100:
            # Overworld tiles.
            if self.main_tileset_id is not None and self.main_tileset_id != 0x0F:
                for n in range(0, 0x20):
                    subtiles[n] = (0x2F, self.main_tileset_id * 0x100 + n * 0x10)
            for n in range(0x20, 0x80):
                subtiles[n] = (0x2C, 0x1000 + n * 0x10)
            for n in range(0x80, 0x100):
                subtiles[n] = (0x2C, n * 0x10)
        else:
            # TODO: Color dungeon is still bit messed up (It's always color dungeon...)
            for n in range(0x20, 0x80):
                subtiles[n] = (0x2D, (n - 0x20) * 0x10)
            if self.main_tileset_id is not None and self.main_tileset_id != 0xFF:
                for n in range(0x00, 0x10):
                    subtiles[n] = (0x2D, 0x1000 + self.main_tileset_id * 0x100 + n*0x10)
            for n in range(0x10, 0x20):
                subtiles[n] = (0x2D, 0x2000 + n * 0x10)
            for n in range(0x10):
                subtiles[0xF0 + n] = (self.item_tiles_bank, self.item_tiles_ptr + n * 0x10)

            if self.sidescroll:
                sidescroll_addr = 0x3800
                if (self.map_id == 6 or self.map_id >= 0x0A) and self.room_nr != 0x2E9:
                    sidescroll_addr = 0x3000
                for n in range(0x00, 0x80):
                    subtiles[n] = (0x2D, sidescroll_addr + n * 0x10)
            else:
                for n in range(0x20, 0x40):
                    subtiles[n] = (self.wall_tiles_bank, self.wall_tiles_ptr + (n - 0x20) * 0x10)
                for n in range(0x10, 0x20):
                    subtiles[n] = (self.floor_tiles_bank, self.floor_tiles_ptr + (n - 0x10) * 0x10)
            
            # Camera shop override (still looks wrong)
            if self.map_id == 0x10 and self.room_nr == 0x2B5:
                for n in range(0x20):
                    subtiles[(0xF0 + n) & 0xFF] = (0x35, 0x2600 + n * 0x10)

        if animation_id is not None:
            anim_addr = (0x0000, 0x0000, 0x2B00, 0x2C00, 0x2D00, 0x2E00, 0x2F00, 0x2D00, 0x3000, 0x3100, 0x3200, 0x2A00, 0x3300, 0x3500, 0x3600, 0x3400, 0x3700)[animation_id]
            if anim_addr:
                for n in range(0x6C, 0x70):
                    subtiles[n] = (0x2C, anim_addr + (n - 0x6C) * 0x10)
                if animation_id == 0x07:
                    for n in range(4):
                        subtiles[0x0C + n] = (0x2C, 0x07C0 + n * 0x10)

        if switch_blocks and self.room_nr >= 0x100:
            for n in range(4):
                subtiles[4 + n] = (0x2C, 0x2800 + n * 0x10)
                subtiles[8 + n] = (0x2C, 0x2880 + n * 0x10)

        return subtiles
