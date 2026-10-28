"""Read a non-English Link's Awakening DX ROM: dialogs, font and codepoint table.

Each language is described by a <code>.json file in this folder. The ROM given
by the player is recognised by its byte sum (the same check as the LADXR web
page), so the player only has to supply their own cartridge dump.

Tables are found by searching the dialog engine code instead of using fixed
addresses, because bank 0 is shifted by a few bytes between versions.
"""
import glob
import json
import os
import re
import struct

TEXT_COUNT = 0x2B0
TEXT_BANK = 0x1C
TEXT_POINTERS_ADDR = 0x0001
CODEPOINT_TABLE_SIZE = 0x100
FONT_TILE_COUNT = 0xA0  # CodepointToTileMap only points to tiles $00-$9F

LANGUAGES_DIR = os.path.dirname(os.path.abspath(__file__))
ENGLISH_CHECKSUM = "89122269"

PATTERNS = {
    # ld a,[wDialogIndexHi]; ld d,a; ld hl,DialogBankTable; add hl,de; ld a,[hl]; and $3F
    "bank_table": rb"\xFA\x12\xC1\x57\x21(..)\x19\x7E\xE6\x3F",
    # ld [rSelectROMBank],a; ld hl,CodepointToTileMap; add hl,de; ld e,[hl]; ld d,0
    "codepoint_table": rb"\xEA\x00\x21\x21(..)\x19\x5E\x16\x00",
    # call ReloadSavedBank; ld hl,FontTiles; add hl,de; ld c,l; ld b,h; pop hl; ld e,$10
    "font": rb"\xCD..\x21(..)\x19\x4D\x44\xE1\x1E\x10",
}

# The font is in bank $0F in every version.
FONT_BANK = 0x0F


def loadLanguages():
    languages = {}
    for path in sorted(glob.glob(os.path.join(LANGUAGES_DIR, "*.json"))):
        with open(path, encoding="utf-8-sig") as f:
            lang = json.load(f)
        lang["code"] = os.path.splitext(os.path.basename(path))[0]
        languages[lang["code"]] = lang
    return languages


def findTable(data, key):
    m = re.search(PATTERNS[key], data[:0x4000], re.S)
    if m is None:
        raise ValueError("%s not found in the ROM" % key)
    return struct.unpack("<H", m.group(1))[0] & 0x3FFF


class LanguageRom:
    def __init__(self, data):
        if len(data) != 1024 * 1024:
            raise ValueError("The language ROM must be 1048576 bytes (unzipped .gbc)")
        checksum = str(sum(data))
        if checksum == ENGLISH_CHECKSUM:
            raise ValueError("The language ROM is the English ROM: give your ROM in another language (French...)")
        for lang in loadLanguages().values():
            if checksum in lang.get("checksums", {}):
                self.language = lang
                self.version = lang["checksums"][checksum]
                break
        else:
            raise ValueError("Unknown Link's Awakening DX ROM (checksum %s)" % checksum)
        self.data = data
        self.bank_table_addr = findTable(data, "bank_table")
        self.codepoint_table_addr = findTable(data, "codepoint_table")
        self.font_addr = findTable(data, "font")
        self.texts = self._readTexts()

    def bank(self, n):
        return self.data[n * 0x4000:(n + 1) * 0x4000]

    def _readTexts(self):
        b = self.bank(TEXT_BANK)
        pointers = struct.unpack("<" + "H" * TEXT_COUNT, b[TEXT_POINTERS_ADDR:TEXT_POINTERS_ADDR + TEXT_COUNT * 2])
        banks = b[self.bank_table_addr:self.bank_table_addr + TEXT_COUNT]
        texts = []
        for n in range(TEXT_COUNT):
            if not (0x4000 <= pointers[n] < 0x8000):
                texts.append(None)
                continue
            data = self.bank(banks[n] & 0x3F)
            start = end = pointers[n] & 0x3FFF
            while data[end] not in (0xFE, 0xFF):
                end += 1
            texts.append(bytes(data[start:end + 1]))
        return texts

    def codepointTable(self):
        b = self.bank(TEXT_BANK)
        return b[self.codepoint_table_addr:self.codepoint_table_addr + CODEPOINT_TABLE_SIZE]

    def font(self):
        b = self.bank(FONT_BANK)
        return b[self.font_addr:self.font_addr + FONT_TILE_COUNT * 16]

    def decode(self, text):
        """Readable version of a dialog, for dumps and debugging."""
        # Capitals like "À" are written as plain "A": don't decode letters back to them.
        reverse = {}
        for char, code in self.language.get("charmap", {}).items():
            code = int(code, 16)
            if not chr(code).isalnum():
                reverse.setdefault(code, char)
        out = []
        for c in text:
            if c == 0xFF:
                break
            if c in reverse:
                out.append(reverse[c])
            elif c == 0xFE:
                out.append("<ask>")
            elif c == 0x5E:
                out.append("'")
            elif 0x20 <= c < 0x7F:
                out.append(chr(c))
            else:
                out.append("<%02X>" % c)
        return "".join(out)
