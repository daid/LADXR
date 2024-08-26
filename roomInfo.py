

# Class which can read various metadata about rooms from the rom
# This is independed of the RoomEditor, which concerns itself mostly with what tiles are where.
#   this info instead is more about how the room is rendered.
class RoomInfo:
    def __init__(self, rom, room_nr: int, map_id: int, sidescroll: bool):
        self.room_nr = room_nr
        self.map_id = map_id
        self.sidescroll = sidescroll

        # Get the tileset id, which is important for which subgraphics to load
        if room_nr < 0x100:
            self.main_tileset_id = rom.banks[0x20][0x2E73 + (room_nr & 0x0F) // 2 + ((room_nr >> 5) * 8)]
            if rom.banks[0x3F][0x3F00 + room_nr]:  # If we have the the per room tileset patch, use that data
                self.main_tileset_id = rom.banks[0x3F][0x3F00 + room_nr]
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
            self.palette_addr = rom.banks[0x21][0x02B1 + self.palette_index*2] | (rom.banks[0x21][0x02B2 + self.palette_index*2] << 8)
        elif room_nr >= 0x300:
            self.palette_index = None
            self.palette_addr = 0x67D0
        else:
            if map_id < 9:
                self.palette_index = None
                self.palette_addr = rom.banks[0x21][0x03EF + map_id*2] | (rom.banks[0x21][0x03F0 + map_id*2] << 8)
            else:
                per_map_lookup_addr = rom.banks[0x21][0x0413 + (map_id - 10)*2] | (rom.banks[0x21][0x0414 + (map_id - 10)*2] << 8)
                self.palette_index = rom.banks[0x21][per_map_lookup_addr - 0x4000 + (self.room_nr & 0xFF)]
                self.palette_addr = rom.banks[0x21][0x043F + self.palette_index*2] | (rom.banks[0x21][0x0440 + self.palette_index*2] << 8)

        # 16x16 -> 8x8 metatiles info
        if room_nr < 0x100:
            self.metatile_bank = 0x1A
            self.metatile_addr = 0x6B1D
        elif room_nr < 0x200:
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
        elif self.room_nr >= 0x100:        
            self.wall_tiles_bank = 0x2D
            self.wall_tiles_ptr = rom.banks[0x20][0x05A9 + self.map_id] * 0x100 - 0x4000
            self.floor_tiles_bank = 0x2D
            self.floor_tiles_ptr = rom.banks[0x20][0x0589 + self.map_id] * 0x100 - 0x4000

    # Get a list of 8x8 graphic tile addresses for this room.
    def getTileset(self, animation_id: int):
        subtiles = [None] * 0x100
        if self.room_nr < 0x100:
            # Overworld tiles.
            for n in range(0, 0x20):
                subtiles[n] = (0x2F, self.main_tileset_id * 0x100 + n * 0x10)
            for n in range(0x20, 0x80):
                subtiles[n] = (0x2C, 0x1000 + n * 0x10)
            for n in range(0x80, 0x100):
                subtiles[n] = (0x2C, n * 0x10)
        else:
            for n in range(0x20, 0x80):
                subtiles[n] = (0x2D, (n - 0x20) * 0x10)
            if self.main_tileset_id != 0xFF:
                for n in range(0x00, 0x10):
                    subtiles[n] = (0x2D, 0x1000 + self.main_tileset_id * 0x100 + n*0x10)
            for n in range(0x10, 0x20):
                subtiles[n] = (0x2D, 0x2000 + n * 0x10)
            for n in range(0xF0, 0x100):
                subtiles[n] = (0x32, 0x3800 + (n - 0xF0) * 0x10)

            if self.sidescroll:
                # TODO: This isn't proper yet.
                for n in range(0x00, 0x80):
                    subtiles[n] = (0x2D, 0x3000 + n * 0x10)
            else:
                for n in range(0x20, 0x40):
                    subtiles[n] = (self.wall_tiles_bank, self.wall_tiles_ptr + (n - 0x20) * 0x10)
                for n in range(0x10, 0x20):
                    subtiles[n] = (self.floor_tiles_bank, self.floor_tiles_ptr + (n - 0x10) * 0x10)

        anim_addr = (0x0000, 0x0000, 0x2B00, 0x2C00, 0x2D00, 0x2E00, 0x2F00, 0x2D00, 0x3000, 0x3100, 0x3200, 0x2A00, 0x3300, 0x3500, 0x3600, 0x3400, 0x3700)[animation_id]
        if anim_addr:
            for n in range(0x6C, 0x70):
                subtiles[n] = (0x2C, anim_addr + (n - 0x6C) * 0x10)

        if False: #TODO: Switch block tiles, if indoor rooms contain tile 0xDB or 0xDC
            for n in range(4):
                tileset[4 + n] = (0x0C, 0x2800 + n * 0x10)
                tileset[8 + n] = (0x0C, 0x2880 + n * 0x10)

        return subtiles
