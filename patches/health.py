from assembler import ASM
from utils import formatText


def setStartHealth(rom, amount):
    rom.patch(0x01, 0x0B1C, ASM("ld  [hl], $03"), ASM("ld  [hl], $%02X" % (amount)))  # max health of new save
    rom.patch(0x01, 0x0B14, ASM("ld  [hl], $18"), ASM("ld  [hl], $%02X" % (amount * 8)))  # current health of new save


def upgradeHealthContainers(rom):
    # Reuse 2 unused shop messages for the heart containers.
    rom.texts[0x2A] = formatText("You found a {HEART_CONTAINER}!")
    rom.texts[0x2B] = formatText("You lost a heart!")

    rom.patch(0x03, 0x19DC, ASM("""
        ld   de, $59D8
        call RenderActiveEntitySpritesPair
    """), ASM("""
        ld   a, $05  ; renderHeartPiece
        rst  8
    """), fill_nop=True)
    rom.patch(0x03, 0x19F0, ASM("""
        ld   hl, $DB5B
        inc  [hl]
        ld   hl, $DB93
        ld   [hl], $FF
    """), ASM("""
        ld   a, $06 ; giveItemMultiworld
        rst  8
        ld   a, $0A ; messageForItemMultiworld
        rst  8
skip:
    """), fill_nop=True)  # add heart->remove heart on heart container


def limitHitChallange(rom):
    # Every hit does exactly 8 subhearts of damage
    rom.patch(0x02, 0x2385, 0x23A2,
        ASM("""
            ld  hl, wSubtractHealthBuffer
            ld  a, [hl] 
            and a
            ret z
            xor a
            ld  [hl], a
            
            ld  hl, wHealth
            ld  a, [hl]
            sub 8
            jr  nc, noZero
            xor a
        noZero:
            ld  [hl], a
            call $6414 ; LoadHeartsCount 
        """), fill_nop=True)
    rom.patch(0x02, 0x2368, ASM("ld a, [wHealth]"), ASM("ld a, e"), fill_nop=True)  # Prevent getting health

    # Remove BigFairy
    rom.patch(0x06, 0x30B8, ASM("ld hl, wEntitiesPrivateState3Table"), ASM("jp ClearEntityStatus_06"))

    # Prevent saving
    rom.patch(0x01, 0x1DE6, 0x1E66, ASM("""
        ld   a, [wSaveSlot]
        sla  a
        ld   e, a
        ld   d, $00
        ld   hl, $49F8 ; SaveGameTable  
        add  hl, de
        ld   a, [hl+]
        ld   h, [hl]
        ld   l, a
        ld   de, wDeathCount - wOverworldRoomStatus ; +5 is for the prefix
        add  hl, de
    
        call EnableSRAM
        ld   a, [wDeathCount]
        ld   [hl+], a
        ld   a, [wDeathCount+1]
        ld   [hl+], a
        ret
    """), fill_nop=True)

    # Prevent medicine from working
    rom.patch(0x02, 0x23AD, ASM("ld a, 8"), ASM("ret"), fill_nop=True)

    # Prevent continue without saving from respawning you
    rom.patch(0x01, 0x02EB, ASM("jr z, $05"), ASM("jr $05"))

    # Prevent acorn damage reduction
    rom.patch(0x03, 0x2DA0, ASM("jr nz, $09"), ASM("jr $09"))
