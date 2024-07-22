from backgroundEditor import BackgroundEditor
from roomEditor import RoomEditor, ObjectWarp
from assembler import ASM
from locations.constants import *
from utils import formatText

REQUIRED_ROWS = {"bingo": 1, "bingo-double": 2, "bingo-triple": 3, "bingo-full": 12}

# Few unused rooms that we can use the room status variables for to store data.
UNUSED_ROOMS = [0x15D, 0x17E, 0x17F, 0x1AD]
next_bit_flag_index = 0


def getUnusedBitFlag():
    global next_bit_flag_index
    addr = UNUSED_ROOMS[next_bit_flag_index // 8] + 0xD800
    bit_nr = next_bit_flag_index & 0x07
    mask = 1 << bit_nr
    next_bit_flag_index += 1
    check_code = checkMemoryMask("$%04x" % (addr), "$%02x" % (mask))
    set_code = "ld hl, $%04x\nset %d, [hl]" % (addr, bit_nr)
    return check_code, set_code


class Goal:
    def __init__(self, description, code, tile_info, *, kill_code=None, group=None, extra_patches=None):
        self.description = description
        self.code = code
        self.tile_info = tile_info
        self.kill_code = kill_code
        self.group = group
        self.extra_patches = extra_patches or []


class TileInfo:
    def __init__(self, index1, index2=None, index3=None, index4=None, *, shift4=False, colormap=None, flipH=False):
        self.index1 = index1
        self.index2 = index2 if index2 is not None else self.index1 + 1
        self.index3 = index3
        self.index4 = index4
        if self.index3 is None:
            self.index3 = self.index1 if flipH else self.index1 + 2
        if self.index4 is None:
            self.index4 = self.index2 if flipH else self.index1 + 3
        self.shift4 = shift4
        self.colormap = colormap
        self.flipH = flipH

    def getTile(self, rom, idx):
        return rom.banks[0x2C + idx // 0x400][(idx % 0x400) * 0x10:((idx % 0x400) + 1) * 0x10]

    def get(self, rom):
        data = self.getTile(rom, self.index1) + self.getTile(rom, self.index2) + self.getTile(rom,
                                                                                              self.index3) + self.getTile(
            rom, self.index4)
        if self.shift4:
            a = []
            b = []
            for c in data[0:32]:
                a.append(c >> 4)
                b.append((c << 4) & 0xFF)
            data = bytes(a + b)
        if self.flipH:
            a = []
            for c in data[32:64]:
                d = 0
                for bit in range(8):
                    if c & (1 << bit):
                        d |= 0x80 >> bit
                a.append(d)
            data = data[0:32] + bytes(a)
        if self.colormap:
            d = []
            for n in range(0, 64, 2):
                a = data[n]
                b = data[n + 1]
                for bit in range(8):
                    col = 0
                    if a & (1 << bit):
                        col |= 1
                    if b & (1 << bit):
                        col |= 2
                    col = self.colormap[col]
                    a &= ~(1 << bit)
                    b &= ~(1 << bit)
                    if col & 1:
                        a |= 1 << bit
                    if col & 2:
                        b |= 1 << bit
                d.append(a)
                d.append(b)
            data = bytes(d)
        return data


ITEM_TILES = {
    BOMB: TileInfo(0x80, shift4=True),
    POWER_BRACELET: TileInfo(0x82, shift4=True),
    SWORD: TileInfo(0x84, shift4=True),
    SHIELD: TileInfo(0x86, shift4=True),
    BOW: TileInfo(0x88, shift4=True),
    HOOKSHOT: TileInfo(0x8A, shift4=True),
    MAGIC_ROD: TileInfo(0x8C, shift4=True),
    MAGIC_POWDER: TileInfo(0x8E, shift4=True),
    OCARINA: TileInfo(0x4E90, shift4=True),
    FEATHER: TileInfo(0x4E92, shift4=True),
    FLIPPERS: TileInfo(0x94, shift4=True),
    SHOVEL: TileInfo(0x96, shift4=True),
    PEGASUS_BOOTS: TileInfo(0x98, shift4=True),
    SEASHELL: TileInfo(0x9E, shift4=True),
    MEDICINE: TileInfo(0xA0, shift4=True),
    BOOMERANG: TileInfo(0xA4, shift4=True),
    TOADSTOOL: TileInfo(0x28C, shift4=True),
    GOLD_LEAF: TileInfo(0xCA, shift4=True),
}


def checkMemoryEqualCode(location, value):
    return """
        ld a, [%s]
        cp %s
        ret
    """ % (location, value)


def checkMemoryNotZero(*locations):
    if len(locations) == 1:
        return """
            ld  a, [%s]
            and a
            jp   flipZ
        """ % (locations[0])
    code = ""
    for location in locations:
        code += """
            ld  a, [%s]
            and a
            jp  z, flipZ
        """ % (location)
    code += "jp flipZ"
    return code


def checkMemoryMask(location, mask):
    if isinstance(location, tuple):
        code = ""
        for loc in location:
            code += """
                ld  a, [%s]
                and %s
                jp  z, clearZ
            """ % (loc, mask)
        code += "jp setZ"
        return code
    return """
        ld  a, [%s]
        and %s
        jp   flipZ
    """ % (location, mask)


def checkCountMemoryNotZero(locations, min, max=255):
    code = "ld e, $00"
    for location in locations:
        code += """
            ld  a, [%s]
            and a
            jr  z, 1
            inc e
        """ % (location)
    code += """
        ld a, e
        cp %s
        jp c, clearZ
    """ % (min)
    if 0 <= max < 255:
        code += """
            cp %s
            jp nc, clearZ
        """ % (max + 1)
    code += "jp setZ"
    return code


def checkCountMemoryMasks(checks, min, max=255):
    code = "ld e, $00"
    for check in checks:
        (location, mask) = check
        code += """
            ld  a, [%s]
            and %s
            jr  z, 1
            inc e
        """ % (location, mask)
    code += """
        ld a, e
        cp %s
        jp c, clearZ
    """ % (min)
    if 0 <= max < 255:
        code += """
            cp %s
            jp nc, clearZ
        """ % (max + 1)
    code += "jp setZ"
    return code


def checkForSeashellsCode(count):
    return """
        ld  a, [wSeashellsCount]
        cp  $%02x
        jp  nc, setZ
        ld  a, [$DAE9]
        and $10
        jp  flipZ
    """ % (count)


def checkMemoryEqualGreater(location, count):
    return """
        ld  a, [%s]
        cp  %s
        jp  nc, setZ
        jp  clearZ
    """ % (location, count)


def InventoryGoal(item, *, memory_location=None, msg=None, group=None):
    if memory_location is not None:
        code = checkMemoryNotZero(memory_location)
    elif item in INVENTORY_MAP:
        code = """
            ld   hl, $DB00
            ld   e, INV_SIZE

        .checkLoop:
            ldi  a, [hl]
            cp   $%s
            ret  z ; item found, return with zero flag set to indicate goal done.
            dec  e
            jr   nz, .checkLoop
            rra ; clear z flag
            ret
        """ % (INVENTORY_MAP[item])
    else:
        code = """
            rra ; clear z flag
            ret
        """
    if msg is None:
        msg = "Find the {%s}" % (item)
    return Goal(msg, code, ITEM_TILES[item], group=group)


def KillGoal(description, entity_id, tile_info, extra_check=None, extra_value=0, group=None):
    check_code, set_code = getUnusedBitFlag()
    kill_code = """
        cp  $%02x
        jr  nz, skip_%02x
    """ % (entity_id, entity_id)
    if extra_check == "State1":
        kill_code += """
            ld  hl, $C2B0
            add hl, bc
            ld  a, [hl]
            and a
            jr  nz, skip_%02x
        """ % (entity_id)
    elif extra_check == "Direction":
        kill_code += """
            ld  hl, wEntitiesDirectionTable
            add hl, bc
            ld  a, [hl]
            cp  $%02x
            jr  nz, skip_%02x
        """ % (extra_value, entity_id)
    kill_code += """
        %s
        jp  done
    skip_%02x:
    """ % (set_code, entity_id)
    return Goal(description, check_code, tile_info, kill_code=kill_code, group=group)


def MonkeyGoal(description, tile_info):
    check_code, set_code = getUnusedBitFlag()
    return Goal(description, check_code, tile_info, extra_patches=[
        (0x15, 0x36EC, 0x36EF, ASM("jp $7FCE")),
        (0x15, 0x3FCE, "00" * 8, ASM("""
            ld   [hl], $FA
            %s
            ret
        """ % (set_code)))
    ])


def BuzzBlobTalkGoal(description, tile_info):
    check_code, set_code = getUnusedBitFlag()
    return Goal(description, check_code, tile_info, extra_patches=[
        (0x18, 0x37C9, ASM("call $237C"), ASM("call $7FDE")),
        (0x18, 0x3FDE, "00" * 11, ASM("""
            call $237C
            ld   [hl], $FA
            %s
            ret
        """ % (set_code)))
    ])


def KillDethlGoal(description, tile_info):
    check_code, set_code = getUnusedBitFlag()
    return Goal(description, check_code, tile_info, extra_patches=[
        (0x15, 0x0606, 0x060B, ASM(set_code)),
    ])


def FishDaPondGoal(description, tile_info, group=None):
    check_code, set_code = getUnusedBitFlag()
    return Goal(description, check_code, tile_info, group=group, extra_patches=[
        (0x04, 0x21F7, 0x21FC, ASM(set_code)),
    ])


def ClearTrendyGameGoal(description, tile_info, group=None):
    check_code, set_code = getUnusedBitFlag()
    return Goal(description, check_code, tile_info, group=group, extra_patches=[
        (0x04, 0x33AB, ASM("ld hl, wEntitiesPrivateState4Table"), ASM("jp $7B96")),
        # running low on space in bank 4, now using some NOP's from the shop patches
        (0x04, 0x3B96, "00" * 22, ASM("""
            ld  hl, wEntitiesPrivateState4Table
            inc [hl]
        ; check if we just picked up the last remaining item
            ld  a, [hl]
            ld  d, a
            ld  e, $06
            ld  hl, $C390
            ld  a, [hl]
            and a
            jr  z, dollItemAvailable
            dec e
        dollItemAvailable:
            ld  a, d
            cp  e
            ret c
            jp  $7BD6
        """)),
        (0x04, 0x3BD6, "00" * 6, ASM("""
            %s
            ret
        """ % (set_code)))
    ])


def WalrusWaterGoal(description, tile_info, group=None):
    check_code, set_code = getUnusedBitFlag()
    return Goal(description, check_code, tile_info, group=group, extra_patches=[
        (0x18, 0x190D, ASM("call GetEntityTransitionCountdown"), ASM("call $7FDE")),
        (0x18, 0x3FE9, "00" * 9, ASM("""
            call GetEntityTransitionCountdown
            %s
            ret
        """ % (set_code)))
    ])


def VacuumMouthGoal(description, tile_info, group=None):
    check_code, set_code = getUnusedBitFlag()
    return Goal(description, check_code, tile_info, group=group, extra_patches=[
        (0x04, 0x28D1, ASM("ldh [hWaveSfx], a \n ret"), ASM("jp $7A76")),
        (0x04, 0x3A76, "00" * 8, ASM("""
            ldh [hWaveSfx], a
            %s
            ret
        """ % (set_code)))
    ])


PHOTO_CHECKS = (("$DC0C", "$01"),("$DC0C", "$02"),("$DC0C", "$04"),("$DC0C", "$08"),
                ("$DC0C", "$10"),("$DC0C", "$20"),("$DC0C", "$40"),("$DC0C", "$80"),
                ("$DC0D", "$01"),("$DC0D", "$02"),("$DC0D", "$04"),("$DC0D", "$08"))
MAP_ADDRESSES = ("$DB16", "$DB1B", "$DB20", "$DB25", "$DB2A", "$DB2F", "$DB34", "$DB39", "$DDDA")
COMPASS_ADDRESSES = ("$DB17", "$DB1C", "$DB21", "$DB26", "$DB2B", "$DB30", "$DB35", "$DB3A", "$DDDB")
BEAK_ADDRESSES = ("$DB18", "$DB1D", "$DB22", "$DB27", "$DB2C", "$DB31", "$DB36", "$DB3B", "$DDDC")
OW_KEY_CHECKS = (("$D8D3", "$10"), ("$D8B5", "$10"), ("$D82B", "$10"), ("$D88C", "$10"), ("$D80E", "$10"))

BINGO_GOALS = [
    InventoryGoal(BOOMERANG),
    InventoryGoal(HOOKSHOT),
    InventoryGoal(MAGIC_ROD),
    InventoryGoal(PEGASUS_BOOTS),
    InventoryGoal(FEATHER),
    InventoryGoal(POWER_BRACELET),
    Goal("Find the L2 {POWER_BRACELET}", checkMemoryEqualCode("wPowerBraceletLevel", "2"), TileInfo(0x82, 0x83, 0x06, 0xB2)),
    InventoryGoal(FLIPPERS, memory_location="wHasFlippers"),
    InventoryGoal(OCARINA),
    InventoryGoal(MEDICINE, memory_location="wHasMedicine", msg="Have the {MEDICINE}"),
    InventoryGoal(BOW),
    InventoryGoal(SHOVEL),
    # InventoryGoal(MAGIC_POWDER),
    InventoryGoal(TOADSTOOL, msg="Have the {TOADSTOOL}", group="witch"),
    Goal("Find the L2 {SHIELD}", checkMemoryEqualCode("wShieldLevel", "2"), TileInfo(0x86, 0x87, 0x06, 0xB2)),
    Goal("Find 5 Secret Seashells", checkForSeashellsCode(0x05), ITEM_TILES[SEASHELL], group="seashells"),
    Goal("Find 10 Secret Seashells", checkForSeashellsCode(0x10), ITEM_TILES[SEASHELL], group="seashells"),
    Goal("Find 15 Secret Seashells", checkForSeashellsCode(0x15), ITEM_TILES[SEASHELL], group="seashells"),
    Goal("Find the L2 {SWORD}", checkMemoryEqualCode("wSwordLevel", "2"), TileInfo(0x84, 0x85, 0x06, 0xB2)),
    Goal("Find the {TAIL_KEY}", checkMemoryNotZero("$DB11"), TileInfo(0xC0, shift4=True)),
    Goal("Find the {SLIME_KEY}", checkMemoryNotZero("$DB15"), TileInfo(0x28E, shift4=True)),
    Goal("Find the {ANGLER_KEY}", checkMemoryNotZero("$DB12"), TileInfo(0xC2, shift4=True)),
    Goal("Find the {FACE_KEY}", checkMemoryNotZero("$DB13"), TileInfo(0xC4, shift4=True)),
    Goal("Find the {BIRD_KEY}", checkMemoryNotZero("$DB14"), TileInfo(0xC6, shift4=True)),
    # {"description": "Marin's Cucco Killing Text"},
    # {"description": "Pick up Crane Game Owner"},
    BuzzBlobTalkGoal("Talk to a buzz blob", TileInfo(0x179C, colormap=[2, 3, 1, 0])),
    # {"description": "Moblin King"},
    Goal("Turtle Rock Entrance Boss", checkMemoryMask("$D810", "$20"),
         TileInfo(0x1413, flipH=True, colormap=[2, 3, 1, 0])),
    Goal("Kill Master Stalfos", checkMemoryMask("$D980", "$10"), TileInfo(0x1622, colormap=[2, 3, 1, 0])),
    # {"description": "Gohma"},
    # {"description": "Grim Creeper"},
    # {"description": "Blaino"},
    KillDethlGoal("Kill Dethl", TileInfo(0x1B38, colormap=[2, 3, 1, 0])),
    # {"description": "Rooster"},
    # {"description": "Marin"},
    # {"description": "Bow-wow"},
    # {"description": "Return Bow-wow"},
    # {"description": "8 Heart Pieces"},
    # {"description": "12 Heart Pieces"},
    Goal("{BOMB} upgrade", checkMemoryEqualCode("$DB77", "$60"), TileInfo(0x80, 0x81, 0x06, 0xA3)),
    Goal("Arrow upgrade", checkMemoryEqualCode("$DB78", "$60"), TileInfo(0x88, 0x89, 0x06, 0xA3)),
    Goal("{MAGIC_POWDER} upgrade", checkMemoryEqualCode("$DB76", "$40"), TileInfo(0x8E, 0x8F, 0x06, 0xA3)),
    # {"description": "Steal From Shop 5 Times"},
    KillGoal("Kill the giant ghini", 0x11, TileInfo(0x08A6, colormap=[2, 3, 1, 0])),
    Goal("Got the Ballad of the Wind Fish", checkMemoryMask("$DB49", "4"),
         TileInfo(0x298, flipH=True, colormap=[2, 3, 1, 0])),
    Goal("Got the Manbo's Mambo", checkMemoryMask("$DB49", "2"), TileInfo(0x29A, flipH=True, colormap=[2, 3, 1, 0])),
    Goal("Got the Frog's Song of Soul", checkMemoryMask("$DB49", "1"),
         TileInfo(0x29C, flipH=True, colormap=[2, 3, 1, 0])),
    Goal("Map and Compass in Tail Cave", checkMemoryNotZero("$DB16", "$DB17"), TileInfo(0x1BD0, index4=0xB1)),
    Goal("Map and Compass in Bottle Grotto", checkMemoryNotZero("$DB1B", "$DB1C"), TileInfo(0x1BD0, index4=0xB2)),
    Goal("Map and Compass in Key Cavern", checkMemoryNotZero("$DB20", "$DB21"), TileInfo(0x1BD0, index4=0xB3)),
    Goal("Map and Compass in Angler's Tunnel", checkMemoryNotZero("$DB25", "$DB26"), TileInfo(0x1BD0, index4=0xB4)),
    Goal("Map and Compass in Catfish's Maw", checkMemoryNotZero("$DB2A", "$DB2B"), TileInfo(0x1BD0, index4=0xB5)),
    Goal("Map and Compass in Face Shrine", checkMemoryNotZero("$DB2F", "$DB30"), TileInfo(0x1BD0, index4=0xB6)),
    Goal("Map and Compass in Eagle's Tower", checkMemoryNotZero("$DB34", "$DB35"), TileInfo(0x1BD0, index4=0xB7)),
    Goal("Map and Compass in Turtle Rock", checkMemoryNotZero("$DB39", "$DB3A"), TileInfo(0x1BD0, index4=0xB8)),
    Goal("Map and Compass in Color Dungeon", checkMemoryNotZero("$DDDA", "$DDDB"), TileInfo(0x1BD0, index4=0xB0)),
    # {"description": "Talk to all Owl Statues in Tail Cave"},
    # {"description": "Talk to all Owl Statues in Bottle Grotto"},
    # {"description": "Talk to all Owl Statues in Key Cavern"},
    # {"description": "Talk to all Owl Statues in Angler's Tunnel"},
    # {"description": "Talk to all Owl Statues in Catfish's Maw"},
    # {"description": "Talk to all Owl Statues in Face Shrine"},
    # {"description": "Talk to all Owl Statues in Eagle's Tower"},
    # {"description": "Talk to all Owl Statues in Turtle Rock"},
    # {"description": "Talk to all Owl Statues in Color Dungeon"},
    # {"description": "Defeat 2 Sets of 3-Of-A-Kind (D1, D7)"},
    # {"description": "Stand 6 HorseHeads in D6"},
    Goal("Find 3 of the Golden Leaves", checkMemoryEqualGreater("wGoldenLeaves", "3"), ITEM_TILES[GOLD_LEAF], group="leaves"),
    Goal("Find 4 of the Golden Leaves", checkMemoryEqualGreater("wGoldenLeaves", "4"), ITEM_TILES[GOLD_LEAF], group="leaves"),
    Goal("Find the 5 Golden Leaves", checkMemoryEqualGreater("wGoldenLeaves", "5"), ITEM_TILES[GOLD_LEAF], group="leaves"),
    # {"description": "Defeat Mad Bomber (outside Kanalet Castle)"},
    # {"description": "Totaka's Song in Richard's Villa"},
    Goal("Win the Yoshi Doll item in the Trendy Game", checkMemoryMask("$DAA0", "$20"), TileInfo(0x9A), group="trendy"),
    # {"description": "Save Papahl on the mountain"},
    Goal("Give the banana to Kiki", checkMemoryMask("$D87B", "$20"), TileInfo(0x1670, colormap=[2, 3, 1, 0])),
    Goal("Have 99 or less rupees", checkMemoryEqualCode("$DB5D", "0"), TileInfo(0xA6, 0xA7, shift4=True), group="rupees"),
    Goal("Have 900 or more rupees", checkMemoryEqualGreater("$DB5D", "9"), TileInfo(0xA6, 0xA7, 0xA6, 0xA7), group="rupees"),
    MonkeyGoal("Bonk the Beach Monkey", TileInfo(0x1946, colormap=[2, 3, 1, 0])),
    # {"description": "Kill an enemy after transforming"},

    Goal("Got the Red Tunic", checkMemoryMask("wCollectedTunics", "1"),
         TileInfo(0x2400, 0x0D11, 0x2400, 0x2401, flipH=True, colormap=[2, 3, 1, 0])),
    Goal("Got the Blue Tunic", checkMemoryMask("wCollectedTunics", "2"),
         TileInfo(0x2400, 0x0D01, 0x2400, 0x2401, flipH=True, colormap=[2, 3, 1, 0])),
    Goal("Buy the first shop item", checkMemoryMask("$DAA1", "$10"), TileInfo(0x0880, colormap=[2, 3, 1, 0]), group="shop"),
    Goal("Buy the second shop item", checkMemoryMask("$DAA1", "$20"), TileInfo(0x0880, colormap=[2, 3, 1, 0]), group="shop"),
    Goal("Find the {INSTRUMENT1}", checkMemoryMask("$DB65", "2"), TileInfo(0x1500, colormap=[2, 3, 1, 0])),
    Goal("Find the {INSTRUMENT2}", checkMemoryMask("$DB66", "2"), TileInfo(0x1504, colormap=[2, 3, 1, 0])),
    Goal("Find the {INSTRUMENT3}", checkMemoryMask("$DB67", "2"), TileInfo(0x1508, colormap=[2, 3, 1, 0])),
    Goal("Find the {INSTRUMENT4}", checkMemoryMask("$DB68", "2"), TileInfo(0x150C, colormap=[2, 3, 1, 0])),
    Goal("Find the {INSTRUMENT5}", checkMemoryMask("$DB69", "2"), TileInfo(0x1510, colormap=[2, 3, 1, 0])),
    Goal("Find the {INSTRUMENT6}", checkMemoryMask("$DB6A", "2"), TileInfo(0x1514, colormap=[2, 3, 1, 0])),
    Goal("Find the {INSTRUMENT7}", checkMemoryMask("$DB6B", "2"), TileInfo(0x1518, colormap=[2, 3, 1, 0])),
    Goal("Find the {INSTRUMENT8}", checkMemoryMask("$DB6C", "2"), TileInfo(0x151C, colormap=[2, 3, 1, 0])),
    # {"description": "Moldorm", "group": "d1"},
    # {"description": "Genie in a Bottle", "group": "d2"},
    # {"description": "Slime Eyes", "group": "d3"},
    # {"description": "Angler Fish", "group": "d4"},
    # {"description": "Slime Eel", "group": "d5"},
    # {"description": "Facade", "group": "d6"},
    # {"description": "Evil Eagle", "group": "d7"},
    # {"description": "Hot Head", "group": "d8"},
    # {"description": "2 Followers at the same time", "group": "multifollower"},
    # {"description": "3 Followers at the same time", "group": "multifollower"},
    Goal("Visit the 4 Fountain Fairies", checkMemoryMask(("$D853", "$D9AC", "$D9F3", "$D9FB"), "$80"),
         TileInfo(0x20, shift4=True, colormap=[2, 3, 1, 0])),
    Goal("Have at least 8 Heart Containers", checkMemoryEqualGreater("$DB5B", "8"), TileInfo(0xAA, flipH=True), group="Health"),
    Goal("Have at least 9 Heart Containers", checkMemoryEqualGreater("$DB5B", "9"), TileInfo(0xAA, flipH=True), group="Health"),
    Goal("Have at least 10 Heart Containers", checkMemoryEqualGreater("$DB5B", "10"), TileInfo(0xAA, flipH=True), group="Health"),
    Goal("Got photo 1: Here Stands A Brave Man", checkMemoryMask("$DC0C", "$01"), TileInfo(0x3008, 0x0D0F, colormap=[2, 3, 1, 0])),
    Goal("Got photo 2: Looking over the sea with Marin", checkMemoryMask("$DC0C", "$02"), TileInfo(0x08F0, 0x0D0F, colormap=[2, 3, 1, 0])),
    Goal("Got photo 3: Heads up!", checkMemoryMask("$DC0C", "$04"), TileInfo(0x0E6A, 0x0D0F, 0x0E6B, 0x0E7B)),
    Goal("Got photo 4: Say Mushroom!", checkMemoryMask("$DC0C", "$08"), TileInfo(0x0E60, 0x0D0F, 0x0E61, 0x0E71)),
    Goal("Got photo 5: Ulrira's Secret!", checkMemoryMask("$DC0C", "$10"),
         TileInfo(0x1461, 0x1464, 0x1463, 0x0D0F, colormap=[2, 3, 1, 0])),
    Goal("Got photo 6: Playing with Bowwow!", checkMemoryMask("$DC0C", "$20"),
         TileInfo(0x1A42, 0x0D0F, 0x1A42, 0x1A43, flipH=True, colormap=[2, 3, 1, 0])),
    Goal("Got photo 7: Thief!", checkMemoryMask("$DC0C", "$40"), TileInfo(0x0880, 0x0D0F, colormap=[2, 3, 1, 0])),
    Goal("Got photo 8: Be more careful next time!", checkMemoryMask("$DC0C", "$80"), TileInfo(0x14E0, index4=0x0D0F, colormap=[2, 3, 1, 0])),
    Goal("Got photo 9: I Found Zora!", checkMemoryMask("$DC0D", "$01"),
         TileInfo(0x1906, 0x0D0F, 0x1906, 0x1907, flipH=True, colormap=[2, 3, 1, 0])),
    Goal("Got photo 10: Richard at Kanalet Castle", checkMemoryMask("$DC0D", "$02"), TileInfo(0x15B0, 0x0D0F, colormap=[2, 3, 1, 0])),
    Goal("Got photo 11: Ghost", checkMemoryMask("$DC0D", "$04"), TileInfo(0x1980, 0x0D0F, colormap=[2, 3, 1, 0])),
    Goal("Got photo 12: Close Call", checkMemoryMask("$DC0D", "$08"), TileInfo(0x0FED, 0x0D0F, 0x0FED, 0x0FFD)),
    Goal("Open the 4 Overworld Warp Holes", checkMemoryMask(("$D801", "$D82C", "$D895", "$D8EC"), "$80"),
         TileInfo(0x3E, 0x3E, 0x3E, 0x3E, colormap=[2, 1, 3, 0])),
    Goal("Finish the Raft Minigame", checkMemoryMask("$D87F", "$80"), TileInfo(0x087C, flipH=True, colormap=[2, 3, 1, 0])),
    Goal("Kill the Ball and Chain Trooper", checkMemoryMask("$DAC6", "$10"), TileInfo(0x09A4, colormap=[2, 3, 1, 0])),
    Goal("Destroy all Pillars with the Ball", checkMemoryMask(("$DA14", "$DA15", "$DA18", "$DA19"), "$20"),
         TileInfo(0x166C, flipH=True)),
    FishDaPondGoal("Fish the pond empty", TileInfo(0x0A00, colormap=[2, 3, 1, 0]), group="fishing"),
    KillGoal("Kill an Anti-Kirby", 0x91, TileInfo(0x1550, colormap=[2, 3, 1, 0])),
    KillGoal("Kill a Rolling Bones", 0x81, TileInfo(0x0AB6, colormap=[2, 3, 1, 0])),
    KillGoal("Kill a Hinox", 0x89, TileInfo(0x1542, colormap=[2, 3, 1, 0])),
    KillGoal("Kill a Stone Hinox", 0xF4, TileInfo(0x2482, colormap=[2, 3, 1, 0])),
    KillGoal("Kill a Dodongo", 0x60, TileInfo(0x0AA0, flipH=True, colormap=[2, 3, 1, 0])),
    KillGoal("Kill a Cue Ball", 0x8E, TileInfo(0x1566, flipH=True, colormap=[2, 3, 1, 0])),
    KillGoal("Kill a Smasher", 0x92, TileInfo(0x1576, colormap=[2, 3, 1, 0])),

    Goal("Save Marin on the Mountain Bridge", checkMemoryMask("$D808", "$10"), TileInfo(0x1A6C, colormap=[2, 3, 1, 0])),
    Goal("Save Raccoon Tarin", checkMemoryMask("$D851", "$10"), TileInfo(0x1888, colormap=[2, 3, 1, 0])),
    Goal("Trade the {TOADSTOOL} with the witch", checkMemoryMask("$DAA2", "$20"), TileInfo(0x0A30, colormap=[2, 3, 1, 0]), group="witch"),

    Goal("Beat the Color Dungeon", checkMemoryMask("$DDE1", "$10"), TileInfo(0x20, 0x21, 0x6, 0xB0, colormap=[2, 3, 1, 0])),
    Goal("Solve the 3 statue puzzles in Color Dungeon", checkMemoryMask(("$DDEF", "$DDE8", "$DDEA"), "$10"),
         TileInfo(0x2470, flipH=True, colormap=[2, 3, 1, 0])),
    Goal("Enter the secret rupee room in Color Dungeon ", checkMemoryMask("$DDF3", "$80"), TileInfo(0xA6, 0xA7, 0xA6, 0xB0)),
    Goal("Play the Chest Game", checkMemoryMask("$DAF2", "$10"), TileInfo(0x160, 0x170, 0x160, 0x170, flipH=True)),
    Goal("Get the item in the fishing pond", checkMemoryMask("$DAB1", "$10"),
         TileInfo(0xA00, 0xA01, 0xAC, 0xAD, flipH=True, colormap=[2, 3, 1, 0]), group="fishing"),
    ClearTrendyGameGoal("Empty out the Trendy Game", TileInfo(0x890, flipH=True, colormap=[2, 3, 1, 0]), group="trendy"),
    Goal("Open the Kanalet Castle gate", checkMemoryMask("$D879", "$10"), TileInfo(0xE8A, 0xE9A, 0xE8A, 0xE9A)),
    Goal("Read the mural in Southern Face Shrine", checkMemoryMask("$DA6F", "$40"), TileInfo(0x1950, colormap=[2, 3, 1, 0])),
    Goal("Let Marin sing for the walrus", checkMemoryMask("$D8FD", "$20"), TileInfo(0x16E1, 0x16E8, 0x16E3, 0x16EA, colormap=[2, 3, 1, 0]), group="walrus"),
    WalrusWaterGoal("Play a song for the walrus after Marin left", TileInfo(0x170A, colormap=[2, 3, 1, 0]), group="walrus"),
    Goal("Get cursed by the 3 Mad Batters", checkMemoryMask(("$D9E0", "$D9E1", "$D9E2"), "$20"), TileInfo(0x1870, colormap=[2, 3, 1, 0])),
    VacuumMouthGoal("Get sucked in by a Vacuum Mouth", TileInfo(0xA6C, flipH=True)),

    Goal("Collect 4 Maps", checkCountMemoryNotZero(MAP_ADDRESSES, 4), TileInfo(0x1BD0, shift4=True), group="total maps"),
    Goal("Collect 5 Maps", checkCountMemoryNotZero(MAP_ADDRESSES, 5), TileInfo(0x1BD0, shift4=True), group="total maps"),
    Goal("Collect 6 Maps", checkCountMemoryNotZero(MAP_ADDRESSES, 6), TileInfo(0x1BD0, shift4=True), group="total maps"),
    Goal("Collect 4 Compasses", checkCountMemoryNotZero(COMPASS_ADDRESSES, 4), TileInfo(0x1BD2, shift4=True), group="total compasses"),
    Goal("Collect 5 Compasses", checkCountMemoryNotZero(COMPASS_ADDRESSES, 5), TileInfo(0x1BD2, shift4=True), group="total compasses"),
    Goal("Collect 6 Compasses", checkCountMemoryNotZero(COMPASS_ADDRESSES, 6), TileInfo(0x1BD2, shift4=True), group="total compasses"),
    Goal("Collect 4 Stone Beaks", checkCountMemoryNotZero(BEAK_ADDRESSES, 4), TileInfo(0x1BD4, shift4=True), group="total beaks"),
    Goal("Collect 5 Stone Beaks", checkCountMemoryNotZero(BEAK_ADDRESSES, 5), TileInfo(0x1BD4, shift4=True), group="total beaks"),
    Goal("Collect 6 Stone Beaks", checkCountMemoryNotZero(BEAK_ADDRESSES, 6), TileInfo(0x1BD4, shift4=True), group="total beaks"),

    Goal("Collect 4 photos", checkCountMemoryMasks(PHOTO_CHECKS, 4), TileInfo(0x3008, colormap=[2, 3, 1, 0]), group="total photos"),
    Goal("Collect 6 photos", checkCountMemoryMasks(PHOTO_CHECKS, 6), TileInfo(0x3008, colormap=[2, 3, 1, 0]), group="total photos"),
    Goal("Collect 8 photos", checkCountMemoryMasks(PHOTO_CHECKS, 8), TileInfo(0x3008, colormap=[2, 3, 1, 0]), group="total photos"),

    Goal("Learn 2 songs", checkCountMemoryMasks((("$DB49", "$04"), ("$DB49", "$02"), ("$DB49", "$01")), 2), TileInfo(0x4E90, 0x4E91, 0x1A0E, 0x1A0F)),
    Goal("Find 3 instruments", checkCountMemoryMasks(((str(0xDB65 + i), "$02") for i in range(8)), 3),
         TileInfo(0x1500, 0x1501, 0x1504, 0x1505, colormap=[2, 3, 1, 0]), group="total instruments"),
    Goal("Find 4 instruments", checkCountMemoryMasks(((str(0xDB65 + i), "$02") for i in range(8)), 4),
         TileInfo(0x1500, 0x1501, 0x1504, 0x1505, colormap=[2, 3, 1, 0]), group="total instruments"),
    Goal("Find 5 instruments", checkCountMemoryMasks(((str(0xDB65 + i), "$02") for i in range(8)), 5),
         TileInfo(0x1500, 0x1501, 0x1504, 0x1505, colormap=[2, 3, 1, 0]), group="total instruments"),
    Goal("Activate 3 dungeon warps", checkCountMemoryMasks(((str(0xDB65 + i), "$01") for i in range(8)), 3),
         TileInfo(0x25, 0x24, 0x1E, 0x1F, colormap=[2, 3, 1, 0]), group="total minibosses"),
    Goal("Activate 4 dungeon warps", checkCountMemoryMasks(((str(0xDB65 + i), "$01") for i in range(8)), 4),
         TileInfo(0x25, 0x24, 0x1E, 0x1F, colormap=[2, 3, 1, 0]), group="total minibosses"),
    Goal("Activate 5 dungeon warps", checkCountMemoryMasks(((str(0xDB65 + i), "$01") for i in range(8)), 5),
         TileInfo(0x25, 0x24, 0x1E, 0x1F, colormap=[2, 3, 1, 0]), group="total minibosses"),
    Goal("Use 2 keys on the overworld", checkCountMemoryMasks(OW_KEY_CHECKS, 2), TileInfo(0xF08, 0xF18, 0xF09, 0xF19), group="ow keys"),
    Goal("Use 3 keys on the overworld", checkCountMemoryMasks(OW_KEY_CHECKS, 3), TileInfo(0xF08, 0xF18, 0xF09, 0xF19), group="ow keys"),
    Goal("Use 4 keys on the overworld", checkCountMemoryMasks(OW_KEY_CHECKS, 4), TileInfo(0xF08, 0xF18, 0xF09, 0xF19), group="ow keys"),

    KillGoal("Kill an Armos Statue", 0x0F, TileInfo(0xEA6, 0xEB6, 0xEA7, 0xEB7)),
    KillGoal("Kill a Pokey", 0xE3, TileInfo(0x8C4, flipH=True, colormap=[2, 3, 1, 0]), extra_check="State1"),
    KillGoal("Kill a Piranha Plant", 0xA2, TileInfo(0x1640, flipH=True, colormap=[2, 3, 1, 0])),
    KillGoal("Kill a Wizzrobe", 0x21, TileInfo(0x950, flipH=True, colormap=[2, 3, 1, 0])),
    KillGoal("Kill a group of Three-of-a-Kinds (hearts)", 0x90, TileInfo(0x1594, colormap=[2, 3, 1, 0]), extra_check="Direction", extra_value=0, group="3-of-a-kind"),
    KillGoal("Kill a group of Three-of-a-Kinds (diamonds)", 0x90, TileInfo(0x1590, colormap=[2, 3, 1, 0]), extra_check="Direction", extra_value=1, group="3-of-a-kind"),
    KillGoal("Kill a group of Three-of-a-Kinds (spades)", 0x90, TileInfo(0x1598, colormap=[2, 3, 1, 0]), extra_check="Direction", extra_value=2, group="3-of-a-kind"),
    KillGoal("Kill a group of Three-of-a-Kinds (clubs)", 0x90, TileInfo(0x159C, colormap=[2, 3, 1, 0]), extra_check="Direction", extra_value=3, group="3-of-a-kind"),
]


def randomizeGoals(rnd, options):
    goals = BINGO_GOALS.copy()
    rnd.shuffle(goals)
    has_group = set()
    for n in range(len(goals)):
        if goals[n].group:
            if goals[n].group in has_group:
                goals[n] = None
            else:
                has_group.add(goals[n].group)
    goals = [goal for goal in goals if goal is not None]
    return goals[:25]


def setBingoGoal(rom, goals, mode):
    assert len(goals) == 25

    for goal in goals:
        for bank, addr, current, target in goal.extra_patches:
            rom.patch(bank, addr, current, target)

    # Setup the bingo card visuals
    be = BackgroundEditor(rom, 0x15)
    ba = BackgroundEditor(rom, 0x15, attributes=True)
    for y in range(18):
        for x in range(20):
            be.tiles[0x9800 + x + y * 0x20] = (x + (y & 2)) % 4 | ((y % 2) * 4)
            ba.tiles[0x9800 + x + y * 0x20] = 0x01

    for y in range(5):
        for x in range(5):
            idx = x + y * 5
            be.tiles[0x9843 + x * 3 + y * 3 * 0x20] = 8 + idx * 4
            be.tiles[0x9844 + x * 3 + y * 3 * 0x20] = 10 + idx * 4
            be.tiles[0x9863 + x * 3 + y * 3 * 0x20] = 9 + idx * 4
            be.tiles[0x9864 + x * 3 + y * 3 * 0x20] = 11 + idx * 4

            ba.tiles[0x9843 + x * 3 + y * 3 * 0x20] = 0x03
            ba.tiles[0x9844 + x * 3 + y * 3 * 0x20] = 0x03
            ba.tiles[0x9863 + x * 3 + y * 3 * 0x20] = 0x03
            ba.tiles[0x9864 + x * 3 + y * 3 * 0x20] = 0x03
    be.store(rom)
    ba.store(rom)

    tiles = rom.banks[0x30][0x3000:0x3040] + rom.banks[0x30][0x3100:0x3140]
    for goal in goals:
        tiles += goal.tile_info.get(rom)
    rom.banks[0x30][0x3000:0x3000 + len(tiles)] = tiles

    # Patch the mural palette to have more useful entries for us
    rom.patch(0x21, 0x36EE, ASM("dw $7C00, $7C00, $7C00, $7C00"), ASM("dw $7FFF, $56b5, $294a, $0000"))
    rom.patch(0x21, 0x36F6, ASM("dw $7C00, $7C00, $7C00, $7C00"), ASM("dw $43f0, $32ac, $1946, $0000"))

    # Patch the face shrine mural handler stage 4, we want to jump to bank 0x0D, which normally contains
    # DMG graphics, but gives us a lot of room for our own code and graphics.
    rom.patch(0x01, 0x2B81, 0x2B99, ASM("""
        ldh  a, [hMapId]
        cp   $16
        jr   nz, notFaceShrineMural
        ld   hl, $DA6F
        set  6, [hl] ; set a flag for use in a bingo goal
    notFaceShrineMural:
        ld   a,  $0D
        ld   hl, $4000
        push hl
        jp   $080C ; switch bank
    """), fill_nop=True)
    # Fix that the mural is always centered on screen, instead offset it properly
    rom.patch(0x18, 0x1E3D, ASM("add hl, bc\nld [hl], $50"), ASM("call $7FD6"))
    rom.patch(0x18, 0x3FD6, "00" * 8, ASM("""
        add hl, bc
        ld  a, [hl]
        and $F0
        add a, $0F
        ld  [hl], a
        ret
    """))

    # In stage 5, just exit the mural without waiting for a button press.
    rom.patch(0x01, 0x2B9E, ASM("jr z, $07"), "", fill_nop=True)

    # Our custom stage 4
    rom.patch(0x0D, 0x0000, 0x3000, ASM("""
wState := $C3C4 ; Our internal state, guaranteed to be 0 on the first entry.
wCursorX := $D100
wCursorY := $D101

    call mainHandler
    ; Make sure we return with bank 1 active.
    ld   a, $01
    jp   $080C ; switch bank

mainHandler:
    ld   a, [wState]
    rst  0
    dw   init
    dw   checkGoalDone
    dw   chooseSquare
    dw   waitDialogDone
    dw   finishGame

init:
    xor  a
    ld   [wCursorX], a
    ld   [wCursorY], a
    inc  a
    ld   [wState], a
    di
    ldh  [$FF4F], a ; 2nd vram bank

    ld   hl, $9843
    ld   c, 25
    ld   b, $00
.checkDoneLoop:
    push bc
    push hl
    ld   a, b
    call goalCheck
    pop  hl
    jr   nz, .notDone
.statWait1:
    ldh  a, [$FF41] ;STAT
    and  $02
    jr   nz, .statWait1 
    ld   a, $04
    ldi  [hl], a
    ldd  [hl], a

    ld   bc, $0020
    add  hl, bc
.statWait2:
    ldh  a, [$FF41] ;STAT
    and  $02
    jr   nz, .statWait2 
    ld   a, $04
    ldi  [hl], a
    ldd  [hl], a

    ld   bc, $FFE0
    add  hl, bc
.notDone:
    inc  hl
    inc  hl
    inc  hl
    ld   a, l
    and  $1F
    cp   $12
    jr   nz, .noRowSkip
    ld   bc, $0060 - 5*3
    add  hl, bc
.noRowSkip:
    pop  bc
    inc  b
    dec  c
    jr   nz, .checkDoneLoop

    xor  a
    ldh  [$FF4F], a ; 1st vram bank
    ei

checkGoalDone:
    ld   a, $02
    ld   [wState], a
    ; Check if the egg event is already triggered
    ld   a, [$D806]
    and  $10
    ret  nz

    call checkAnyGoal
    ret  c

    ; Goal done, give a message and goto state to finish the game
    ld   a, $04
    ld   [wState], a
    ld   a, $E7 
    call $2385 ; open dialog 
    ret

chooseSquare:
    ld   hl, $C000 ; oam buffer

    ; Draw the cursor
    ld   a, [wCursorY]
    call multiA24
    add  a, $27
    ldi  [hl], a
    ld   a, [wCursorX]
    call multiA24
    add  a, $24
    ldi  [hl], a
    ld   a, $A2
    ldi  [hl], a
    ld   a, $02
    ldi  [hl], a

    ldh  a, [$FFCC] ; button presses
    bit  0, a
    jr   nz, .right
    bit  1, a
    jr   nz, .left
    bit  2, a
    jr   nz, .up
    bit  3, a
    jr   nz, .down
    bit  4, a
    jr   nz, .showText
    bit  5, a
    jr   nz, exitMural
    bit  7, a
    jr   nz, exitMural
    ret

.right:
    ld   a, [wCursorX]
    cp   $04
    ret  z
    inc  a
    ld   [wCursorX], a
    ret

.left:
    ld   a, [wCursorX]
    and  a
    ret  z
    dec  a
    ld   [wCursorX], a
    ret

.down:
    ld   a, [wCursorY]
    cp   $04
    ret  z
    inc  a
    ld   [wCursorY], a
    ret

.up:
    ld   a, [wCursorY]
    and  a
    ret  z
    dec  a
    ld   [wCursorY], a
    ret

.showText:
    ld   a, [wCursorY]
    ld   c, a
    add  a, a
    add  a, a
    add  a, c
    ld   c, a
    ld   a, [wCursorX]
    add  a, c
    add  a, a
    ld   l, a
    ld   h, $00
    ld   de, messageTable
    add  hl, de
    ldi  a, [hl]
    ld   h, [hl]
    ld   l, a
    ld   de, wCustomMessage
.copyLoop:
    ldi  a, [hl]
    ld   [de], a
    inc  de
    inc  a
    jr   nz, .copyLoop

    ld   a, $C9 
    call $2385 ; open dialog 
    ld   a, [wCursorY]
    cp   $03
    ld   a, [wDialogState]
    jr   nc, .top
    or   $80
    jr  .bottom
.top:
    and  $7F
.bottom:
    ld   [wDialogState], a ; dialog position depends on the selected row
    ld   a, $03
    ld   [wState], a
    ret

waitDialogDone:
    ld   a, [wDialogState]
    and  a
    ret  nz
    ld   a, $02 ; choose square
    ld   [wState], a
    ret

exitMural:
    ld   hl, $DB96 ;gameplay subtype 
    inc  [hl]
    ret

finishGame:
    ld   a, [wDialogState]
    and  a
    ret  nz
    
    ldh  a, [$FFCC] ; button presses
    and  a
    ret  z
    
    ; Goto "credits"
    xor  a
    ld   [$DB96], a 
    inc  a
    ld   [$DB95], a
    ret

multiA24:
    ld   c, a
    add  a, a
    add  a, c
    add  a, a
    add  a, a
    add  a, a
    ret

flipZ:
    jr   nz, setZ
clearZ: 
    rra
    ret
setZ:
    cp   a
    ret

checkAnyGoal:
    xor  a
    push af
    call checkGoalRow1
    {inc_counter}
    call checkGoalRow2
    {inc_counter}
    call checkGoalRow3
    {inc_counter}
    call checkGoalRow4
    {inc_counter}
    call checkGoalRow5
    {inc_counter}
    call checkGoalCol1
    {inc_counter}
    call checkGoalCol2
    {inc_counter}
    call checkGoalCol3
    {inc_counter}
    call checkGoalCol4
    {inc_counter}
    call checkGoalCol5
    {inc_counter}
    call checkGoalDiagonal0
    {inc_counter}
    call checkGoalDiagonal1
    {inc_counter}
    pop  af
    cp   {req_rows}
    ret

checkGoalRow1:
    call goalcheck_0
    ret  nz
    call goalcheck_1
    ret  nz
    call goalcheck_2
    ret  nz
    call goalcheck_3
    ret  nz
    call goalcheck_4
    ret

checkGoalRow2:
    call goalcheck_5
    ret  nz
    call goalcheck_6
    ret  nz
    call goalcheck_7
    ret  nz
    call goalcheck_8
    ret  nz
    call goalcheck_9
    ret

checkGoalRow3:
    call goalcheck_10
    ret  nz
    call goalcheck_11
    ret  nz
    call goalcheck_12
    ret  nz
    call goalcheck_13
    ret  nz
    call goalcheck_14
    ret

checkGoalRow4:
    call goalcheck_15
    ret  nz
    call goalcheck_16
    ret  nz
    call goalcheck_17
    ret  nz
    call goalcheck_18
    ret  nz
    call goalcheck_19
    ret

checkGoalRow5:
    call goalcheck_20
    ret  nz
    call goalcheck_21
    ret  nz
    call goalcheck_22
    ret  nz
    call goalcheck_23
    ret  nz
    call goalcheck_24
    ret

checkGoalCol1:
    call goalcheck_0
    ret  nz
    call goalcheck_5
    ret  nz
    call goalcheck_10
    ret  nz
    call goalcheck_15
    ret  nz
    call goalcheck_20
    ret

checkGoalCol2:
    call goalcheck_1
    ret  nz
    call goalcheck_6
    ret  nz
    call goalcheck_11
    ret  nz
    call goalcheck_16
    ret  nz
    call goalcheck_21
    ret

checkGoalCol3:
    call goalcheck_2
    ret  nz
    call goalcheck_7
    ret  nz
    call goalcheck_12
    ret  nz
    call goalcheck_17
    ret  nz
    call goalcheck_22
    ret

checkGoalCol4:
    call goalcheck_3
    ret  nz
    call goalcheck_8
    ret  nz
    call goalcheck_13
    ret  nz
    call goalcheck_18
    ret  nz
    call goalcheck_23
    ret

checkGoalCol5:
    call goalcheck_4
    ret  nz
    call goalcheck_9
    ret  nz
    call goalcheck_14
    ret  nz
    call goalcheck_19
    ret  nz
    call goalcheck_24
    ret

checkGoalDiagonal0:
    call goalcheck_0
    ret  nz
    call goalcheck_6
    ret  nz
    call goalcheck_12
    ret  nz
    call goalcheck_18
    ret  nz
    call goalcheck_24
    ret

checkGoalDiagonal1:
    call goalcheck_4
    ret  nz
    call goalcheck_8
    ret  nz
    call goalcheck_12
    ret  nz
    call goalcheck_16
    ret  nz
    call goalcheck_20
    ret

messageTable:
""".format(inc_counter="jr nz, 3 \n pop de \n inc d \n push de", req_rows=REQUIRED_ROWS[mode]) +
    "\n".join(["dw message_%d" % (n) for n in range(25)]) + "\n" +
    "\n".join(["message_%d:\n  db m\"%s\"" % (n, goal.description) for n, goal in
               enumerate(goals)]) + "\n" +
    """
    goalCheck:
        rst  0
    """ +
    "\n".join(["dw goalcheck_%d" % (n) for n in range(25)]) + "\n" +
    "\n".join(["goalcheck_%d:\n  %s\n" % (n, goal.code) for n, goal in
               enumerate(goals)]) + "\n", 0x4000), fill_nop=True)
    rom.texts[0xE7] = formatText("BINGO!\nPress any button to finish.")

    # Patch the game to call a bit of our code when an enemy is killed by patching into the drop item handling
    rom.patch(0x00, 0x3F50, ASM("ld a, $03\nld [$C113], a\nld [$2100], a\ncall $55CF"), ASM("""
        ld a, $0D
        ld [$C113], a
        ld [$2100], a
        call $7000
    """))
    rom.patch(0x0D, 0x3000, 0x4000, ASM("""
        ldh  a, [$FFEB] ; active entity
    """ + "\n".join([goal.kill_code for goal in goals if goal.kill_code is not None]) + """
done:   ; Return to normal item drop handler
        ld   a,  $03   ;normal drop item handler bank
        ld   hl, $55CF ;normal drop item handler address
        push hl
        jp   $080F ; switch bank
    """, 0x7000), fill_nop=True)

    # Patch Dethl to warp you outside
    rom.patch(0x15, 0x0682, 0x069B, ASM("""
        ld   a, $0B
        ld   [$DB95], a
        call $0C7D

        ld   a, $07
        ld   [$DB96], a
    """), fill_nop=True)
    re = RoomEditor(rom, 0x274)
    re.objects += [ObjectWarp(0, 0, 0x06, 0x58, 0x40)] * 4
    re.store(rom)
    # Patch the egg to be always open
    rom.patch(0x00, 0x31f5, ASM("ld a, [$D806]\nand $10\njr z, $25"), ASM(""), fill_nop=True)
    rom.patch(0x20, 0x2dea, ASM("ld a, [$D806]\nand $10\njr z, $29"), ASM(""), fill_nop=True)

    # Patch unused entity 4C into our bingo board.
    rom.patch(0x03, 0x004C, "41", "82")
    rom.patch(0x03, 0x0147, "00", "98")
    rom.patch(0x20, 0x00e4, "000000", ASM("dw $5e1b\ndb $18"))

    # Add graphics for our bingo board to 2nd WRAM bank.
    rom.banks[0x3F][0x3700:0x3780] = rom.banks[0x32][0x1500:0x1580]
    rom.banks[0x3F][0x3728:0x373A] = b'\x55\xAA\x00\xFF\x55\xAA\x00\xFF\x55\xAA\x00\xFF\x55\xAA\x00\xFF\x00\xFF'
    rom.banks[0x3F][0x3748:0x375A] = b'\x55\xAA\x00\xFF\x55\xAA\x00\xFF\x55\xAA\x00\xFF\x55\xAA\x00\xFF\x00\xFF'
    rom.patch(0x18, 0x1E0B,
              "00F85003" + "00005203" + "00085403" + "00105603",
              "00F8F00B" + "0000F20B" + "0008F40B" + "0010F60B")

    # Add the bingo board to marins house
    re = RoomEditor(rom, 0x2A3)
    re.entities.append((2, 0, 0x4C))
    re.store(rom)

    # Add the bingo board to the room before the egg
    re = RoomEditor(rom, 0x016)
    re.removeObject(4, 5)
    re.entities.append((3, 4, 0x4C))
    re.updateOverlay()
    re.store(rom)

    # Remove the egg event from the egg room (no bomb triggers for you!)
    re = RoomEditor(rom, 0x006)
    re.entities = []
    re.store(rom)

    rom.texts[0xCF] = formatText("""
        Bingo!
        Young lad, I mean... #####, the hero!
        You have bingo!
        You have proven your wisdom, courage and power!
        ... ... ... ...
        As part of the Wind Fish's spirit, I am the guardian of his dream world...
        But one day, we decided to have a bingo game.
        Then you, #####, came to win the bingo...
        Thank you, #####...
        My work is done...
        The Wind Fish will wake soon.
        Good bye...Bingo!
    """)
    rom.texts[0xCE] = rom.texts[0xCF]
