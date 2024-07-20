from assembler import ASM


def fixPhotographer(rom):
    # Allow richard photo without slime key
    rom.patch(0x36, 0x3234, ASM("jr nz, $52"), "", fill_nop=True)
    rom.patch(0x36, 0x3240, ASM("jr z, $46"), "", fill_nop=True)
    # Allow richard photo when castle is opened
    rom.patch(0x36, 0x31FF, ASM("jp nz, $7288"), "", fill_nop=True)
    # Allow photographer with bowwow saved
    rom.patch(0x36, 0x0398, ASM("or [hl]"), "", fill_nop=True)
    rom.patch(0x36, 0x3183, ASM("ret nz"), "", fill_nop=True)
    rom.patch(0x36, 0x31CB, ASM("jp nz, $7288"), "", fill_nop=True)
    rom.patch(0x36, 0x03DC, ASM("and $7F"), ASM("and $00"))
    # Allow bowwow photo with follower
    rom.patch(0x36, 0x31DA, ASM("jp nz, $7288"), "", fill_nop=True)
    # Allow bridge photo with follower
    rom.patch(0x36, 0x004D, ASM("call nz, UnloadEntity"), "", fill_nop=True)
    rom.patch(0x36, 0x006D, ASM("ret nz"), "", fill_nop=True) # Checks if any entity is alive
    # Allow Marin photos after she sang for the walrus
    rom.patch(0x36, 0x3101, ASM("ld a, [wIsMarinFollowingLink]"), ASM("call $7F10"))
    rom.patch(0x36, 0x312D, ASM("ld a, [wIsMarinFollowingLink]"), ASM("call $7F10"))
    rom.patch(0x36, 0x01F4, ASM("ld a, [wIsMarinFollowingLink]"), ASM("call $7F10"))
    rom.patch(0x36, 0x3F10, "00" * 16, ASM("""
        ld  a, [wIsMarinFollowingLink]
        and a
        ret nz
        ld  a, [$D8FD]
        and $20 ; check if walrus is gone
        ret
    """), fill_nop=True)
    # Well photo is taken as soon as Link lands if Marin isn't there
    rom.patch(0x36, 0x0236, ASM("ldh a, [hLinkAnimationState] \n cp $6A"), ASM("call $7F20"), fill_nop=True)
    rom.patch(0x36, 0x3F20, "00" * 32, ASM("""
        ld  a, [wIsMarinFollowingLink]
        and a
        jr  z, noMarinFollower
        ldh a, [hLinkAnimationState]
        cp  $6A
        ret
    noMarinFollower:
        ldh a, [hLinkPositionZ]
        and a ; check if Link landed on the ground
        ret
    """), fill_nop=True)
