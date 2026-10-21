"""
Prototyp: Dungeon-Raeume zwischen den Dungeons tauschen (LADXR).

Idee: Raeume mit Item-Orten bleiben, wo sie sind. Alle uebrigen Raeume der
Dungeons 1-8 werden untereinander getauscht, aber nur gegen Raeume mit derselben
"Tuer-Signatur" (gleiche Seiten, gleiche Tuerart, gleiche Wand-Vorlage).

ACHTUNG: Die Logik (logic/dungeon*.py) kennt den Tausch nicht. Seeds koennen
dadurch unfair oder unloesbar werden. Das ist ein Prototyp zum Ausprobieren.

Einbau (in generator.py, nach den anderen Dungeon-Patches):
    import patches.roomShuffle
    patches.roomShuffle.shuffleDungeonRooms(rom, rnd, verbose=True)
"""
import copy

from roomEditor import RoomEditor

# Raumnummern der Dungeons 1-8 (Color Dungeon bewusst nicht dabei)
DUNGEON_BLOCKS = [
    (0x100, 0x120), (0x120, 0x140), (0x140, 0x160), (0x160, 0x180),
    (0x180, 0x1B0), (0x1B0, 0x1E0), (0x200, 0x230), (0x230, 0x260),
]

# Raeume mit Truhe, Schluessel-Drop, Eulenstatue, Herzcontainer oder Instrument
# (aus logic/dungeon*.py). Diese Raeume werden nie bewegt.
FIXED_ROOMS = {
    0x102, 0x103, 0x104, 0x106, 0x108, 0x10A, 0x10C, 0x10D, 0x10E, 0x113,
    0x114, 0x115, 0x116, 0x11D, 0x120, 0x121, 0x122, 0x126, 0x127, 0x129,
    0x12A, 0x12B, 0x12E, 0x12F, 0x132, 0x133, 0x134, 0x136, 0x137, 0x138,
    0x139, 0x140, 0x141, 0x142, 0x144, 0x146, 0x147, 0x148, 0x14C, 0x14D,
    0x14E, 0x14F, 0x150, 0x151, 0x153, 0x154, 0x155, 0x158, 0x159, 0x15A,
    0x15B, 0x160, 0x162, 0x165, 0x166, 0x168, 0x169, 0x16A, 0x16D, 0x16E,
    0x16F, 0x171, 0x175, 0x176, 0x178, 0x179, 0x17B, 0x181, 0x182, 0x183,
    0x185, 0x186, 0x188, 0x18A, 0x18E, 0x18F, 0x196, 0x197, 0x19A, 0x19B,
    0x19E, 0x1A0, 0x1B0, 0x1B1, 0x1B3, 0x1B4, 0x1B5, 0x1B6, 0x1B9, 0x1BB,
    0x1BC, 0x1BE, 0x1C0, 0x1C3, 0x1C9, 0x1CE, 0x1CF, 0x1D1, 0x1D7, 0x201,
    0x204, 0x209, 0x210, 0x211, 0x212, 0x216, 0x21A, 0x21B, 0x21C, 0x220,
    0x223, 0x224, 0x22C, 0x230, 0x232, 0x234, 0x235, 0x237, 0x23A, 0x23D,
    0x23E, 0x240, 0x241, 0x245, 0x246, 0x24C, 0x24D, 0x24F, 0x253, 0x255,
    0x259, 0x25A, 0x25C, 0x25F, 0x302, 0x306, 0x307, 0x308, 0x30A, 0x30F,
    0x311, 0x314,
}

# Raeume mit diesen Tuer-Makros werden nie bewegt (Boss, Treppe, Flipwall,
# Einwegpfeil, Eingang).
BAD_DOOR_TYPES = {0xF8, 0xF9, 0xFA, 0xFB, 0xFC, 0xFD}

# True: auch die genaue Position der Tueren muss gleich sein (strenger).
STRICT_DOOR_POSITIONS = False
# True: nur Raeume tauschen, die im ROM gleich viele Bytes belegen (Objekte und Entities).
# Normalerweise nicht noetig: shuffleDungeonRooms prueft vorab, ob die Tabellen nach dem
# Tausch noch in die ROM passen (check_fit), und verwirft Tausche, die nicht passen.
REQUIRE_SAME_SIZE = False

# Lockerungen (mehr Tauschpartner, aber unsicherer):
MATCH_WALLS = False        # False: Wand-Vorlage (offene Seiten ohne Tuer) ignorieren
MATCH_DOOR_CLASS = True   # False: Schluessel-/Shutter-/offene Tuer gleich behandeln

# Raeume, die im Code fest verdrahtet sind, aber nicht als Raumnummer in logic/dungeon*.py stehen:
#   0x180 = Hookshot-Drop (locations/hookshot.py, D5)
#   0x17C = Sidescroller-Raum, in den der Schluessel aus 0x169 faellt (droppedKey.py, D4)
HARDCODED_ROOMS = {0x180, 0x17C}

# Optional: weitere Raeume, die du von Hand ausschliessen willst
# (zum Beispiel Raeume, die andere Patches mit RoomEditor veraendern).
EXTRA_FIXED_ROOMS = set()

# Raeume mit diesen Entity-IDs werden nie bewegt (Namen aus entityData.py).
# "Strukturell": Dinge, die die Logik oder andere Patches an einen festen Raum binden.
BLOCKED_ENTITY_IDS = {
    0x42, 0x39,                                  # Eulenstatue, Instrument
    0x5F,                                        # Master Stalfos (nur D5)
    0x61,                                        # WARP = Miniboss-Portal
    0x66,                                        # Kristallschalter
    0x46, 0x47, 0x48, 0x49, 0x69,                # Moving Blocks (D4-Puzzle)
    0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x62, 0x63,    # Bosse
    0x5E, 0x60, 0x81, 0x82, 0x88, 0x89, 0x8E,    # Minibosse: Ghoma, Dodongo, Rolling Bones,
    0x92, 0xBC, 0xBD, 0xBE, 0xF4, 0xF8,          #   Armos Knight, Hinox, Cue Ball, Smasher, ...
}
BLOCKED_OBJECT_IDS = set()

# Streng: zusaetzlich alle Gegner sperren, die logic/dungeon*.py ueber
# enemy_requirements nennt. Sehr sicher, aber der Pool wird winzig (siehe Hinweis).
BLOCK_LOGIC_ENEMIES = False
LOGIC_ENEMY_IDS = {
    0x0B, 0x0D, 0x14, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1E, 0x1F, 0x20, 0x21,
    0x23, 0x24, 0x28, 0x29, 0x2C, 0x50, 0x55, 0x56, 0x57, 0x8F, 0x90, 0x9B, 0x9C,
    0xA0, 0xA1, 0xAA, 0xAB,
}
# Optional: Raeume mit mehr Entities als diesem Wert nie bewegen (None = egal).
MAX_ENTITIES = None


def _door_class(type_id):
    if 0xEC <= type_id <= 0xEF:
        return "K"  # Schluesseltuer
    if 0xF0 <= type_id <= 0xF3:
        return "C"  # geschlossene Tuer (Shutter)
    if 0xF4 <= type_id <= 0xF7:
        return "O"  # offene Tuer
    return None


def _signature(room_editor):
    """Gibt eine Signatur zurueck oder None, wenn der Raum nicht tauschbar ist."""
    doors = []
    for obj in room_editor.objects:
        t = obj.type_id
        if not isinstance(t, int) or not 0xEC <= t <= 0xFD:
            continue  # Warps (type_id None) und normale Tiles
        if t in BAD_DOOR_TYPES:
            return None
        cls = _door_class(t)
        if cls is None:
            return None
        if obj.y == 0:
            side = "N"
        elif obj.y == 7:
            side = "S"
        elif obj.x == 0:
            side = "W"
        elif obj.x == 9:
            side = "E"
        else:
            return None  # Tuer mitten im Raum: unbekannt, nicht anfassen
        entry = (side, cls if MATCH_DOOR_CLASS else "D")
        if STRICT_DOOR_POSITIONS:
            entry = entry + (obj.x, obj.y)
        doors.append(entry)
    if not doors:
        return None
    walls = (room_editor.floor_object & 0xF0) if MATCH_WALLS else 0
    return (walls, tuple(sorted(doors)))


def _scan(rom):
    groups = {}
    editors = {}
    for start, end in DUNGEON_BLOCKS:
        for room in range(start, end):
            if room in FIXED_ROOMS or room in HARDCODED_ROOMS or room in EXTRA_FIXED_ROOMS:
                continue
            try:
                r = RoomEditor(rom, room)
            except (AssertionError, IndexError, KeyError):
                continue
            if r.getWarps():
                continue
            if MAX_ENTITIES is not None and len(r.entities) > MAX_ENTITIES:
                continue
            blocked = BLOCKED_ENTITY_IDS | (LOGIC_ENEMY_IDS if BLOCK_LOGIC_ENEMIES else set())
            if any(e[2] in blocked for e in r.entities):
                continue
            if any(isinstance(o.type_id, int) and o.type_id in BLOCKED_OBJECT_IDS for o in r.objects):
                continue
            sig = _signature(r)
            if sig is None:
                continue
            # Das Tileset liest RoomEditor bei Innenraeumen nicht selbst aus.
            r.tileset_index = rom.banks[0x20][0x2EB3 + room - 0x100]
            if REQUIRE_SAME_SIZE:
                size = 3 + sum(len(o.export()) for o in r.objects)  # wie in RoomEditor.store
                sig = sig + (size, len(r.entities))
            groups.setdefault(sig, []).append(room)
            editors[room] = r
    return groups, editors


def _room_table(rom, room):
    if room < 0x200:
        return rom.rooms_indoor_a, room - 0x100
    return rom.rooms_indoor_b, room - 0x200


def _table_fits(table):
    """Rechnet PointerTable.store() nach, ohne etwas zu schreiben.
    Gibt True zurueck, wenn alle Daten in den Speicher der Tabelle passen."""
    data = getattr(table, "_PointerTable__data", None)
    if data is None:
        return True  # keine echte PointerTable (zum Beispiel im Test): nichts zu pruefen
    banks = table._PointerTable__banks
    info = table._PointerTable__info
    storage = copy.deepcopy(table._PointerTable__storage)
    done = {st["bank"]: {} for st in storage}

    def place(size, bank):
        for st in storage:
            if st["end"] - st["start"] >= size and st["bank"] == bank:
                start = st["start"]
                st["start"] = start + size
                return start
        return None

    for key in info.get("alt_pointers", {}):
        s = bytes(table._PointerTable__alt_data[key])
        if place(len(s), info["data_bank"]) is None:
            return False
    for n, s in enumerate(data):
        if isinstance(s, int):
            continue
        s = bytes(s)
        bank = banks[n]
        if bank not in done:
            return False
        if s in done[bank]:
            continue
        start = place(len(s), bank)
        if start is None:
            return False
        if "data_size" not in info:
            for skip in range(len(s)):
                done[bank][s[skip:]] = start + skip
        done[bank][s] = start
    return True


def _all_fit(rom):
    return all(_table_fits(t) for t in (rom.rooms_indoor_a, rom.rooms_indoor_b, rom.entities))


def _snapshot(rom, rooms):
    snap = {}
    for room in rooms:
        table, idx = _room_table(rom, room)
        snap[room] = (bytes(table[idx]), bytes(rom.entities[room]),
                      rom.banks[0x20][0x2EB3 + room - 0x100])
    return snap


def _restore(rom, snap):
    for room, (objects_raw, entities_raw, tileset) in snap.items():
        table, idx = _room_table(rom, room)
        table[idx] = bytearray(objects_raw)
        rom.entities[room] = bytearray(entities_raw)
        rom.banks[0x20][0x2EB3 + room - 0x100] = tileset


def shuffleDungeonRooms(rom, rnd, verbose=False, check_fit=True):
    """Tauscht Raeume innerhalb von Gruppen mit gleicher Signatur.
    rnd: ein random.Random. Gibt die Liste der (Zielraum, Quellraum) zurueck.
    check_fit: Tausche verwerfen, nach denen die ROM-Tabellen nicht mehr in den
    Speicher passen (sonst scheitert rom.save mit "Not enough room in storage")."""
    if check_fit and not _all_fit(rom):
        if verbose:
            print("roomShuffle: WARNUNG: Die Tabellen passen schon vor dem Tausch nicht mehr "
                  "in den Speicher. Pruefung wird uebersprungen.")
        check_fit = False

    groups, editors = _scan(rom)
    swaps = []
    skipped = 0
    for sig in sorted(groups, key=lambda s: groups[s][0]):
        rooms = groups[sig]
        if len(rooms) < 2:
            continue
        order = rooms[:]
        rnd.shuffle(order)

        # Erst die volle Permutation versuchen, dann einzelne Paare.
        candidates = [dict(zip(rooms, order))]
        candidates += [{a: b, b: a} for a, b in zip(order[::2], order[1::2])]
        for number, mapping in enumerate(candidates):
            mapping = {slot: src for slot, src in mapping.items() if slot != src}
            if not mapping:
                continue
            snap = _snapshot(rom, mapping.keys()) if check_fit else None
            for slot, source in mapping.items():
                # Alle Editoren wurden vor dem ersten store() geladen.
                editors[source].store(rom, slot)
            if check_fit and not _all_fit(rom):
                _restore(rom, snap)
                skipped += 1
                continue
            swaps.extend(mapping.items())
            if number == 0:
                break  # volle Permutation hat gepasst, Paare nicht mehr noetig
    if verbose:
        print("roomShuffle: %d Raeume getauscht, %d Versuche passten nicht in den ROM-Speicher"
              % (len(swaps), skipped))
        for slot, source in swaps:
            print("  Platz 0x%03X <- Raum 0x%03X" % (slot, source))
    return swaps
