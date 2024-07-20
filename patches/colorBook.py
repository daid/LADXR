from assembler import ASM

def fixColorBook(rom):
    # patch to repair the color book shadow/flags. Can still fire projectiles over the book.
    rom.patch(0x03, 0x004A, "F2", "A2")
    # patch hitbox flags to match 1.2
    rom.patch(0x03, 0x0145, "80", "98")
