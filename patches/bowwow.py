from assembler import ASM
from roomEditor import RoomEditor


def neverGetBowwow(rom):
    ### BowWow patches
    rom.patch(0x03, 0x1E0E, "EA56DB", "000000")  # Do not mark BowWow as kidnapped after we complete dungeon 1.
    rom.patch(0x15, 0x06B6, "FA56DBFE80C2", "FA56DBFE80CA")  # always load the moblin boss
    rom.patch(0x03, 0x182D, "FA56DBFE80C2", "FA56DBFE80CA")  # always load the cave moblins
    rom.patch(0x07, 0x3947, "FA56DBFE80C2", "FA56DBFE80CA")  # always load the cave moblin with sword
    # TODO: Do something at the end of the bowwow cave, maybe place a chest there?

    re = RoomEditor(rom, 0x024)
    re.removeEntities(0x7E)
    re.store(rom)

    re = RoomEditor(rom, 0x033)
    re.removeEntities(0xCC)
    re.store(rom)

    return
    # Load followers in dungeons
    rom.patch(0x01, 0x1FCA, ASM("ret c"), "", fill_nop=True);
    rom.patch(0x00, 0x2EB0, ASM("ld a, [$DB56]\ncp $01\nld a, $A4\njr z, $18"), "", fill_nop=True)
    # Patch bowwow follor sprite to be used from 2nd vram bank
    rom.patch(0x05, 0x001C,
        b"40034023"
        b"42034223"
        b"44034603"
        b"48034A03"
        b"46234423"
        b"4A234823"
        b"4C034C23",
        b"500B502B"
        b"520B522B"
        b"540B560B"
        b"580B5A0B"
        b"562B542B"
        b"5A2B582B"
        b"5C0B5C2B")
    # Patch to use the chain sprite from second vram bank
    rom.patch(0x05, 0x0282,
        ASM("ld a, $4E\njr nz, $02\nld a, $7E\nld [de], a\ninc de\nld a, $00"),
        ASM("ld a, $5E\nld [de], a\ninc de\nld a, $08"), fill_nop=True)
