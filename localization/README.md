# Localization: play a seed in another language

LADXR needs the English v1.0 ROM. With `--language-rom`, the player also gives
their own ROM in another language, and the generated seed uses its dialogs,
font, menus and graphics. The texts LADXR writes itself (item messages, hints,
shops, Marin, bingo...) are translated by `<code>.json`.

```
python main.py "Zelda DX (USA, Europe).gbc" --language-rom "Zelda DX (France).gbc" -o seed.gbc
```

On the web page, the language ROM goes in the optional "Select language ROM"
field next to the English ROM, and is remembered like the English ROM.

Each Link's Awakening DX cartridge has a single language: USA/Europe
(English), France, Germany, Japan. There is no official Spanish or Italian.

| File | State |
| --- | --- |
| `fr.json` | France v1.0 and v1.1 (Rev A). Tested with Rev A: dialogs, menus, file select, inventory, save menu, all LADXR texts including the 140 bingo goals. |
| `de.json` | Recognized, but refused until diacritics are supported (see below). |
| `ja.json` | Same (dakuten), and the LADXR texts would need kana. |

## How it works

| Step | When | What |
| --- | --- | --- |
| Dialogs | before the patches | The ~690 dialogs of the language ROM replace the English ones. LADXR then writes its own dialogs over them, through the translations. |
| Font | before the patches | Tiles $00-$9F of the font (bank $0F, and its copy in $2F that the Game Boy Color reads, which also draws some menu words) and `CodepointToTileMap`. Codepoints the language doesn't use keep their English mapping, used by LADXR's own characters (`<eacute>`, icons...). |
| Graphics with words | before the patches | `GRAPHICS_WITH_WORDS`: menus, save menu, title, inventory, map, ending, photo album... for DMG and CGB. Not `credits_roll`, where LADXR takes the letters of its end statistics. |
| Tilemaps | before the patches | The 38 backgrounds and their attributes (file select, name entry, erase/copy, inventory...). LADXR edits them afterwards like it does on the English ones. |
| LADXR texts | during the patches | `utils.formatText` is wrapped: exact translation (`texts`), then `patterns`, then `places` and `words` (whole words). Item names: `names`, plus `dungeon_items` x `dungeons`. Yes/no choices: `asks`. Marin's wake-up lines: `marin`. Texts left in English are printed as `Language: untranslated: ...`. |
| Save menu | after the patches | LADXR adds "RETURN HOME & QUIT" with English letter tiles. `save_menu_home` gives that row in the language: existing tiles plus tiles drawn as pixel art. |

The tables of the language ROM are found by searching the dialog engine code,
not at fixed addresses: bank 0 is shifted by a few bytes between versions.
Translated dialogs don't have the English sizes, so the texts table now has
`flexible_banks`: a dialog that doesn't fit in its bank goes to another one
(`DialogBankTable` is updated). English seeds are unchanged.

`reset()` undoes the changes to `utils` and `patches.aesthetics` at the start
of every generation, because the web page generates several seeds in the same
Python process.

## Adding a language

1. Copy `fr.json` to `<code>.json` and put the byte sum of the ROM in
   `checksums` (the web page prints it in the browser console).
2. `charmap`: character to ROM codepoint, to encode the LADXR texts. The file
   `constants/charmaps/dialog.asm` of each version in the
   [LADX disassembly](https://github.com/zladx/LADX-Disassembly) (`revisions/`)
   gives them.
3. Translate `names`, `dungeons`, `dungeon_items`, `places`, `words`, `asks`,
   `texts`, `patterns`, `marin`. Generate seeds with various settings: what is
   missing is printed.
4. `save_menu_home`: the third row of the save menu (see `fr.json`). The tiles
   of that menu can be read with `BackgroundEditor(rom, 0x0D)`.
5. `"graphics": false` if the graphics of the language are not at the English
   addresses (probably Japanese).
6. Add the checksums to `LANGUAGE_ROMS` in `www/js/ui.js`.

## Diacritics (German, Japanese)

The English dialog engine still has the code that draws a diacritic tile above
a letter (umlaut, dakuten), but its table lookup is replaced by `xor a`:

```
00:263C  3E 1C     ld a, $1C
00:263E  EA 00 21  ld [rSelectROMBank], a   ; bank $1C selected
00:2641  F0 D8     ldh a, [hMultiPurpose1]  ; current character
00:2643  5F        ld e, a
00:2644  16 00     ld d, $00
00:2646  AF        xor a                    ; DE/JP: ld hl, CodepointToDiacritic / add hl, de / ld a, [hl]
00:2647  E1        pop hl
00:2648  A7        and a
00:2649  28 18     jr z, .noDiacritic       ; 1 -> tile $C9, 2 -> tile $C8
```

To do, with a German or Japanese ROM to test:

- Replace the 4 bytes at `$2643` with `call Routine` + `nop`, the routine being
  in bank $1C (already selected): `ld e,a / ld d,0 / ld hl,Table /
  add hl,de / ld a,[hl] / ret`.
- Copy the 256 bytes of `CodepointToDiacritic` of the language ROM to bank $1C,
  taking the room from the dialog storage of that bank.
- Tiles $C8/$C9 are in `inventory_overworld_items`, `inventory_indoor_items` and
  `ending_1`, already copied by `GRAPHICS_WITH_WORDS`.
- The name entry screen (`file_menus.asm`, `__DIACRITICS_SUPPORT__`) needs
  another patch to show umlauts.

The French ROM also has a (disabled) table, with an acute accent on "É" at `$CE`:
it can be used to test the patch, dialog $5E "OEUF SACRÉ" would show its accent.
