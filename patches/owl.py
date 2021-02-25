from roomEditor import RoomEditor
from assembler import ASM
from utils import formatText


def removeOwlEvents(rom):
    # Remove all the owl events from the entity tables.
    for room in range(0x100):
        re = RoomEditor(rom, room)
        if re.hasEntity(0x41):
            re.removeEntities(0x41)
            re.store(rom)
    # Clear texts used by the owl. Potentially reused somewhere else.
    rom.texts[0x0D9] = b'\xff'  # used by boomerang
    # 1 Used by empty chest (master stalfos message)
    # 8 unused (0x0C0-0x0C7)
    # 1 used by bowwow in chest
    # 1 used by item for other player message
    # 2 used by arrow chest messages
    # 2 used by tunics
    for idx in range(0x0BE, 0x0CE):
        rom.texts[idx] = b'\xff'


    # Patch the owl entity to allow refill of powder/bombs
    rom.texts[0xC0] = formatText("Hoot!\nHoot!\nOut of stock?", ask="Okay No")
    rom.texts[0xC1] = formatText("Hoot!\nHoot! Hoot!\nHoot!\nHere are a few things for you.")
    rom.patch(0x06, 0x27F5, 0x2A77, ASM("""
    ; Render owl
    ld de, sprite
    call $3BC0

    call $64C6 ; check if game is busy (pops this stack frame if busy)

    ldh a, [$E7] ; frame counter
    cp $F0
    jr c, eyesOpen
    ld a, $01
    jr setSpriteVariant
eyesOpen:
    xor a
setSpriteVariant:
    call $3B0C ; set entity sprite variant
    call $641A ; check collision
    ldh  a, [$F0] ;entity state
    rst 0
    dw  waitForTalk
    dw  talking

waitForTalk:
    call $645D ; check if talked to
    ret  nc
    ld   a, $C0
    call $2385 ; open dialog
    call $3B12 ; increase entity state
    ret

talking:
    ; Check if we are still talking
    ld   a, [$C19F]
    and  a
    ret  nz
    call $3B12 ; increase entity state
    ld   [hl], $00 ; set to state 0
    ld   a, [$C177] ; get which option we selected
    and  a
    ret  nz

    ; Give powder
    ld   a, [$DB4C]
    cp   $10
    jr   nc, doNotGivePowder
    ld   a, $10
    ld   [$DB4C], a
doNotGivePowder:

    ld   a, [$DB4D]
    cp   $10
    jr   nc, doNotGiveBombs
    ld   a, $10
    ld   [$DB4D], a
doNotGiveBombs:

    ld   a, $C1
    call $2385 ; open dialog
    ret

sprite:
    db   $78, $01, $78, $21, $7A, $01, $7A, $21
""", 0x67F5), fill_nop=True)


def upgradeDungeonOwlStatues(rom):
    # Call our custom handler after the check for the stone beak
    rom.patch(0x18, 0x1EA2, ASM("ldh a, [$F7]\ncp $FF\njr nz, $05"), ASM("ld a, $09\nrst 8\nret"), fill_nop=True)

def upgradeOverworldOwlStatues(rom):
    # Replace the code that handles signs/owl statues on the overworld
    # This removes a "have marin with you" special case to make some room for our custom owl handling.
    rom.patch(0x00, 0x201A, ASM("""
        cp   $6F
        jr   z, $2B
        cp   $D4
        jr   z, $27
        ld   a, [$DB73]
        and  a
        jr   z, $08
        ld   a, $78
        call $237C
        jp   $20CF
    """), ASM("""
        cp   $D4
        jr   z, $2B
        cp   $6F
        jr   nz, skip

        ld   a, $09
        rst 8
        jp   $20CF
skip:
    """), fill_nop=True)
