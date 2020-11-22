from assembler import ASM
from roomEditor import RoomEditor


def updateFinishingMinigame(rom):
    rom.patch(0x04, 0x26BE, 0x26DF, ASM("""
        ld   a, $0B ; GiveItemAndMessageForRoom
        rst  8
        
        ; Mark selection as stopping minigame, as we are not asking a question.
        ld   a, $01
        ld   [$C177], a
    """), fill_nop=True)
