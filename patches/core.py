from assembler import ASM
from roomEditor import RoomEditor


def noSwordMusic(rom):
    # Skip no-sword music override
    # Instead of loading the sword level, we put the value 1 in the A register, indicating we have a sword.
    rom.patch(2, 0x0151, ASM("ld a, [$DB4E]"), ASM("ld a, $01\nNOP"))
    rom.patch(2, 0x3B42, ASM("ld a, [$DB4E]"), ASM("ld a, $01\nNOP"))
    rom.patch(3, 0x0994, ASM("ld a, [$DB4E]"), ASM("ld a, $01\nNOP"))

def removeGhost(rom):
    ## Ghost patch
    # Do not have the ghost follow you after dungeon 4
    rom.patch(0x03, 0x1E0A, ASM("LD [$DB79], A"), ASM("NOP\nNOP\nNOP"))

def alwaysAllowSecretBook(rom):
    rom.patch(0x15, 0x3F25, ASM("ld a, [$DB0E]\ncp $0E"), ASM("xor a\ncp $00"), fill_nop=True)

def flameThrowerShieldRequirement(rom):
    rom.patch(0x03, 0x2EAF,
        ASM("ld a, [$DB44]\ncp $02\nret nz"), # if not shield level 2
        ASM("ld a, [$DB44]\ncp $02\nret c")) # if not shield level 2 or higher

def cleanup(rom):
    # Remove unused rooms to make some space in the rom
    re = RoomEditor(rom, 0x2C4)
    re.objects = []
    re.entities = []
    re.store(rom, 0x2C4)
    re.store(rom, 0x2D4)
    re.store(rom, 0x277)
    re.store(rom, 0x278)
    re.store(rom, 0x279)
