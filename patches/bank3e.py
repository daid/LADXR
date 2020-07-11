import os
from assembler import ASM
from utils import formatText


def hasBank3E(rom):
    return rom.banks[0x3E][0] != 0x00

# Bank $3E is used for large chunks of custom code.
#   Mainly for new chest and dropped items handling.
def addBank3E(rom):
    # No default text for getting the bow, so use an unused slot.
    rom.texts[0x89] = formatText(b"Found the bow!")
    rom.texts[0xD9] = formatText(b"Found the boomerang!")  # owl text slot reuse
    rom.texts[0xBE] = rom.texts[0x111]  # owl text slot reuse to get the master skull message in the first dialog group
    for idx in range(8):
        rom.texts[0xBF + idx] = b""
    rom.texts[0xC7] = b""
    rom.texts[0xC8] = formatText(b"Found BowWow! Which monster put him in a chest? He is a good boi, and waits for you at the Swamp.")
    rom.texts[0xC9] = 0xC0A0  # Custom message slot
    rom.texts[0xCA] = formatText(b"Found 10 arrows!")
    rom.texts[0xCB] = formatText(b"Found a single arrow... joy?")

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
    rom.patch(0x3E, 0x0000, 0x3000, ASM("""
        call MainJumpTable
        pop af
        jp $080C ; switch bank and return to normal code.

MainJumpTable:
        rst  0 ; JUMP TABLE
        dw   MainLoop                     ; 0
        dw   RenderChestItem              ; 1
        dw   GiveItemFromChest            ; 2
        dw   ItemMessage                  ; 3
        dw   RenderDroppedKey             ; 4
        dw   RenderHeartPiece             ; 5
        dw   GiveItemFromChestMultiworld  ; 6
        dw   CheckIfLoadBowWow            ; 7
        dw   BowwowEat                    ; 8
        dw   HandleOwlStatue              ; 9
        dw   ItemMessageMultiworld        ; A
        dw   GiveItemAndMessageForRoom    ; B
        dw   RenderItemForRoom            ; C

    """ + open(os.path.join(my_path, "bank3e.asm/link.asm"), "rt").read()
        + open(os.path.join(my_path, "bank3e.asm/chest.asm"), "rt").read()
        + open(os.path.join(my_path, "bank3e.asm/bowwow.asm"), "rt").read()
        + open(os.path.join(my_path, "bank3e.asm/message.asm"), "rt").read()
        + open(os.path.join(my_path, "bank3e.asm/owl.asm"), "rt").read(), 0x4000), fill_nop=True)
    # 3E:3300-3616: Multiworld flags per room (for both chests and dropped keys)
    # 3E:3800-3B16: DroppedKey item types
    # 3E:3B16-3E2C: Owl statue items

    # Put 20 rupees in all owls by default.
    rom.patch(0x3E, 0x3B16, "00" * 0x316, "1C" * 0x316)
