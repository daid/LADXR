from assembler import ASM
from utils import formatText


def patchRooster(rom):
    # Do not give the rooster
    rom.patch(0x19, 0x0E9D, ASM("ld [$DB7B], a"), "", fill_nop=True)

    # Do not load the rooster sprites
    rom.patch(0x00, 0x2EC7, ASM("jr nz, $08"), "", fill_nop=True)

    # Draw the found item
    rom.patch(0x19, 0x0E4A, ASM("ld hl, $4E37\nld c, $03\ncall $3CE6"), ASM("ld a, $0C\nrst $08"), fill_nop=True)
    rom.patch(0x19, 0x0E7B, ASM("ld hl, $4E37\nld c, $03\ncall $3CE6"), ASM("ld a, $0C\nrst $08"), fill_nop=True)
    # Give the item and message
    rom.patch(0x19, 0x0E69, ASM("ld a, $6D\ncall $2373"), ASM("ld a, $0E\nrst $08"), fill_nop=True)

    # Reuse unused evil eagle text slot for rooster message
    rom.texts[0x0B8] = formatText("Got the {ROOSTER}, pick him up with the A button!")

    # Always allow rooster pickup with A button
    rom.patch(0x19, 0x1ABE, ASM("ret nz"), "", fill_nop=True)

    # Do not take away the rooster after D7
    rom.patch(0x03, 0x1E25, ASM("ld [$DB7B], a"), "", fill_nop=True)

    # Patch the color dungeon entrance not to check for rooster
    rom.patch(0x02, 0x3409, ASM("ld hl, $DB7B\nor [hl]"), "", fill_nop=True)
