import os
import binascii
from assembler import ASM, Assembler
from utils import formatText


def hasBank3E(rom):
    return rom.banks[0x3E][0] != 0x00

# Bank $3E is used for large chunks of custom code.
#   Mainly for new chest and dropped items handling.
def addBank3E(rom, seed, settings):
    # No default text for getting the bow, so use an unused slot.
    rom.texts[0x89] = formatText("Found the {BOW}!")
    rom.texts[0xD9] = formatText("Found the {BOOMERANG}!")  # owl text slot reuse
    rom.texts[0xBE] = rom.texts[0x111]  # owl text slot reuse to get the master skull message in the first dialog group
    rom.texts[0xC8] = formatText("Found {BOWWOW}! Which monster put him in a chest? He is a good boi, and waits for you at the Swamp.")
    rom.texts[0xC9] = 0xC0A0  # Custom message slot
    rom.texts[0xCA] = formatText("Found {ARROWS_10}!")
    rom.texts[0xCB] = formatText("Found a {SINGLE_ARROW}... joy?")

    # Create a trampoline to bank 0x3E in bank 0x00.
    # There is very little room in bank 0, so we set this up as a single trampoline for multiple possible usages.
    # the A register is preserved and can directly be used as a jumptable in page 3E.
    # Trampoline at rst 8
    # the A register is preserved and can directly be used as a jumptable in page 3E.
    rom.patch(0, 0x0008, "0000000000000000000000000000", ASM("""
        ld   h, a
        ld   a, [$DBAF]
        push af
        ld   a, $3E
        call $080C ; switch bank
        ld   a, h
        jp $4000
    """), fill_nop=True)

    # Special trampoline to jump to the damage-entity code, we use this from bowwow to damage instead of eat.
    rom.patch(0x00, 0x0018, "000000000000000000000000000000", ASM("""
        ld   a, $03
        ld   [$2100], a
        call $71C0
        ld   a, [$DBAF]
        ld   [$2100], a
        ret
    """))

    my_path = os.path.dirname(__file__)
    asm = Assembler()
    asm.processFile(os.path.join(my_path, "bank3e.asm"), "main.asm", base_address=0x4000, bank=0x3E)
    asm.link()
    for section in asm.getSections():
        assert section.bank == 0x3E
        assert section.base_address == 0x4000
        assert len(section.data) < 0x2F00
        rom.banks[section.bank][0:len(section.data)] = section.data
    # 3E:3300-3616: Multiworld flags per room (for both chests and dropped keys)
    # 3E:3800-3B16: DroppedKey item types
    # 3E:3B16-3E2C: Owl statue or trade quest items

    # Put 20 rupees in all owls by default.
    rom.patch(0x3E, 0x3B16, "00" * 0x316, "1C" * 0x316)

    shortSeed = seed[:0x20]
    rom.patch(0x3E, 0x2F00, "00" * len(shortSeed), binascii.hexlify(shortSeed))

    if not settings.race:
        shortSettings = settings.getShortString().encode('utf-8')
        rom.patch(0x3E, 0x2F20, "00", binascii.hexlify(len(shortSettings).to_bytes(1, 'little')))
        rom.patch(0x3E, 0x2F21, "00" * len(shortSettings), binascii.hexlify(shortSettings))

    # Prevent the photo album from crashing due to serial interrupts
    rom.patch(0x28, 0x00D2, ASM("ld a, $09"), ASM("ld a, $01"))
