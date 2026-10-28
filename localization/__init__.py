"""Generate a seed in the language of another Link's Awakening DX ROM.

The game stays built on the English v1.0 ROM. The dialogs, the font, the
graphics and the tilemaps with words come from a second ROM the player owns in
another language (French, ...). The texts LADXR writes itself are translated
with the <code>.json file of that language. See README.md in this folder.
"""
import re
import sys

import utils
import patches.aesthetics
from backgroundEditor import BackgroundEditor
from romTables import BackgroundTilesTable, BackgroundAttributeTable
from .langrom import LanguageRom, findTable, FONT_BANK, TEXT_BANK, TEXT_COUNT

# Graphics that contain words, as (bank, offset in bank, size). A DMG bank
# below $20 also copies its CGB twin $20 banks further. Taken from the files
# the LADX disassembly overrides for the French and German versions.
# credits_roll (bank $38) is left out: LADXR takes its letters for the
# end-of-game statistics.
GRAPHICS_WITH_WORDS = [
    (0x0C, 0x0800, 0x400),   # items_2
    (0x0C, 0x0C00, 0x100),   # inventory_overworld_items
    (0x0C, 0x0F00, 0x300),   # overworld_1 (signs)
    (0x0F, 0x0000, 0x400),   # menu
    (0x0F, 0x0400, 0x500),   # save_menu
    (0x0F, 0x0900, 0x700),   # title
    (0x0F, 0x1A00, 0x200),   # ow_camera_shop
    (0x0F, 0x2600, 0x200),   # ow_mabe_village
    (0x0F, 0x3E00, 0x200),   # ow_taramanch_middle
    (0x10, 0x2700, 0x900),   # font_large
    (0x12, 0x3D00, 0x100),   # inventory_indoor_items
    (0x12, 0x3E00, 0x200),   # minimap
    (0x13, 0x0000, 0x2800),  # ending_1
    (0x34, 0x0000, 0x4000),  # print
    (0x35, 0x0000, 0x1200),  # oam_color_dungeon
    (0x35, 0x1200, 0xE00),   # print_ui_1, print_ui_2
    (0x35, 0x2800, 0x1800),  # photo_album, ending.cgb.alt
    (0x38, 0x1800, 0x800),   # title_dx (CGB and DMG)
    (0x38, 0x2800, 0x300),   # thanks_for_playing
    (0x3A, 0x0000, 0x4000),  # photo_elements_2
]

SAVE_MENU_BG = 0x0D
SAVE_MENU_TILES_ADDR = 0x0400  # save_menu graphics in banks $0F/$2F, tile $80 first
SAVE_MENU_HOME_ROW = 0x9960

# What a localization changes in LADXR's own modules, to undo it before the
# next generation (the web UI generates several seeds in the same process).
_ORIGINAL_NAMES = dict(utils._NAMES)
_ORIGINAL_CHARACTERS = dict(utils._CHARACTERS)
_ORIGINAL_FORMAT_TEXT = utils.formatText
_ORIGINAL_MARIN_TEXT = patches.aesthetics.getMarinStartingText


def reset():
    utils._NAMES.clear()
    utils._NAMES.update(_ORIGINAL_NAMES)
    utils._CHARACTERS.clear()
    utils._CHARACTERS.update(_ORIGINAL_CHARACTERS)
    for module in list(sys.modules.values()):
        if getattr(getattr(module, "formatText", None), "localized", False):
            module.formatText = _ORIGINAL_FORMAT_TEXT
    patches.aesthetics.getMarinStartingText = _ORIGINAL_MARIN_TEXT


class Localization:
    def __init__(self, language_rom_data):
        self.rom = LanguageRom(language_rom_data)
        self.lang = self.rom.language
        if self.lang.get("diacritics"):
            raise NotImplementedError("%s needs diacritic support in the dialog engine, which is not done yet"
                                      % self.lang["name"])
        self.missing = set()

    def prePatch(self, rom):
        print("Language: %s (%s)" % (self.lang["name"], self.rom.version))
        self._copyTexts(rom)
        self._copyFont(rom)
        if self.lang.get("graphics", True):
            self._copyGraphics(rom)
            self._copyBackgrounds(rom)
        self._installTranslations()

    def postPatch(self, rom):
        if "save_menu_home" in self.lang:
            self._patchSaveMenu(rom, self.lang["save_menu_home"])
        for text in sorted(self.missing):
            print("Language: untranslated: %s" % (text.replace("\n", "\\n")))

    def _copyTexts(self, rom):
        for n in range(TEXT_COUNT):
            text = self.rom.texts[n]
            if text is not None and not isinstance(rom.texts[n], int):
                rom.texts[n] = bytearray(text)

    def _copyFont(self, rom):
        bank0 = bytes(rom.banks[0])
        font_addr = findTable(bank0, "font")
        table_addr = findTable(bank0, "codepoint_table")
        size = len(self.rom.font())
        # Bank $2F holds a copy of the font used by the Game Boy Color, which
        # also draws menu words from it (EFFACER/COPIER in French).
        for bank in (FONT_BANK, FONT_BANK + 0x20):
            rom.banks[bank][font_addr:font_addr + size] = self.rom.bank(bank)[font_addr:font_addr + size]
        # The language's codepoints win; codepoints it doesn't use keep the
        # English mapping, which LADXR's own characters (<eacute>, icons...) use.
        table = rom.banks[TEXT_BANK]
        for n, tile in enumerate(self.rom.codepointTable()):
            if tile:
                table[table_addr + n] = tile

    def _copyGraphics(self, rom):
        for bank, addr, size in GRAPHICS_WITH_WORDS:
            for b in (bank, bank + 0x20) if bank < 0x20 else (bank,):
                rom.banks[b][addr:addr + size] = self.rom.bank(b)[addr:addr + size]

    def _copyBackgrounds(self, rom):
        # Tilemaps of the menus, inventory, file select... which place the
        # words drawn in the graphics above. LADXR edits them afterwards.
        class LanguageBanks:
            banks = [bytearray(self.rom.bank(n)) for n in range(0x40)]

        for table, rom_table in ((BackgroundTilesTable, rom.background_tiles),
                                 (BackgroundAttributeTable, rom.background_attributes)):
            lang_table = table(LanguageBanks)
            for n in range(len(lang_table)):
                rom_table[n] = lang_table[n]

    def _patchSaveMenu(self, rom, config):
        """LADXR adds a third save menu option, "RETURN HOME & QUIT", by copying
        "RETURN TO GAME" and drawing "HOME" with English letter tiles. The menu
        words are drawn in a proportional font spread over tiles, so each language
        gives the tiles of its own row, and pixel art for the tiles it draws."""
        for tile, rows in config.get("custom_tiles", {}).items():
            data = bytearray()
            for row in rows:
                lo = hi = 0
                for x, c in enumerate(row):
                    c = ".123".index(c)
                    lo |= (c & 1) << (7 - x)
                    hi |= (c >> 1) << (7 - x)
                data += bytes([lo, hi])
            addr = SAVE_MENU_TILES_ADDR + (int(tile, 16) - 0x80) * 16
            for bank in (0x0F, 0x2F):
                rom.banks[bank][addr:addr + 16] = data

        # Other screens drawn with the same tiles lose them: blank them there.
        custom = {int(tile, 16) for tile in config.get("custom_tiles", {})}
        for bg in config.get("blank_in_backgrounds", []):
            be = BackgroundEditor(rom, int(bg, 16))
            for addr, tile in list(be.tiles.items()):
                if tile in custom:
                    be.tiles[addr] = 0x7F
            be.store(rom)

        be = BackgroundEditor(rom, SAVE_MENU_BG)
        for col in range(3, 17):
            be.tiles[SAVE_MENU_HOME_ROW + col] = 0x7F
        for n, tile in enumerate(config["row"]):
            be.tiles[SAVE_MENU_HOME_ROW + config["start_col"] + n] = int(tile, 16)
        be.store(rom)

    def _installTranslations(self):
        lang = self.lang
        tokens = {}
        for char, code in lang.get("charmap", {}).items():
            token = "<lang%s>" % code
            utils._CHARACTERS[token.encode()] = bytes([int(code, 16)])
            tokens[char] = token

        def encode(s):
            return "".join(tokens.get(c, c) for c in s)

        for key, name in self._allNames().items():
            if key in utils._NAMES:
                utils._NAMES[key] = encode(name)

        # Some LADXR texts are indented triple-quoted strings: compare them
        # without the spaces around each line.
        def normalize(s):
            return "\n".join(line.strip() for line in s.strip().split("\n"))

        texts = {normalize(english): local for english, local in lang.get("texts", {}).items()}
        asks = lang.get("asks", {})
        patterns = [(re.compile(p), r) for p, r in lang.get("patterns", [])]
        # Place names and the words of LADXR's useless hints, whole words only,
        # longest first so "Yarna Desert" is replaced before "Desert".
        words = dict(lang.get("places", {}), **lang.get("words", {}))
        words = [(re.compile(r"(?<!\w)%s(?!\w)" % re.escape(english)), local)
                 for english, local in sorted(words.items(), key=lambda item: -len(item[0]))]
        missing = self.missing

        def formatText(instr, *, center=False, ask=None):
            translated = texts.get(normalize(instr))
            if translated is None:
                for pattern, replacement in patterns:
                    if pattern.fullmatch(instr):
                        translated = pattern.sub(replacement, instr)
                        break
            if translated is not None:
                for english, local in words:
                    translated = english.sub(local, translated)
                instr = encode(translated)
            elif re.search(r"[A-Za-z]", re.sub(r"\{\w+\}", "", instr)):
                # Only names, numbers or symbols need no translation.
                missing.add(instr)
            if ask is not None:
                ask = encode(asks.get(ask, ask))
            return _ORIGINAL_FORMAT_TEXT(instr, center=center, ask=ask)

        formatText.localized = True
        for module in list(sys.modules.values()):
            if getattr(module, "formatText", None) is _ORIGINAL_FORMAT_TEXT:
                module.formatText = formatText

        # Marin's wake-up jokes come from patches/marin.txt, in English. A
        # language can bring its own list instead of translating the whole file.
        marin = lang.get("marin")
        if marin:
            def getMarinStartingText(rnd):
                return _ORIGINAL_FORMAT_TEXT(encode(rnd.choice(marin)))
            patches.aesthetics.getMarinStartingText = getMarinStartingText

    def _allNames(self):
        names = dict(self.lang.get("names", {}))
        dungeons = self.lang.get("dungeons", [])
        fmt = self.lang.get("dungeon_item_format", "{item} {dungeon}")
        for prefix, item in self.lang.get("dungeon_items", {}).items():
            for n, dungeon in enumerate(dungeons):
                names["%s%d" % (prefix, n)] = fmt.format(item=item, dungeon=dungeon)
        return names
