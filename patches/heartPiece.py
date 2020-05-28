from assembler import ASM


def fixHeartPiece(rom):
    # Patch all locations where the piece of heart is rendered.
    rom.patch(0x03, 0x1b52, ASM("ld de, $5A4D\ncall $3BC0"), ASM("ld a, $04\nrst 8"), fill_nop=True)  # state 0

    # TODO: This does not show the entity above link.
    rom.patch(0x03, 0x1A74, None, ASM("""
        ; Render sprite
        ld   a, $05
        rst  8
    
        call $512A ; mark room as done
        
        ; Handle item effect
        ld   a, $02
        rst  8
        
        ;Show message
        ld   a, $03
        rst  8
        
        call $3F8D ; unload entity
        ret
    """))
