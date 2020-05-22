from assembler import ASM


def fixDroppedKey(rom):
    # Patch the rendering code to use the dropped key rendering code.
    rom.patch(0x03, 0x1C99, None, ASM("""
        ld   a, $03
        call $3FF0
        jp $5CA6
    """))

    # Patch the key pickup code to use the chest pickup code.
    rom.patch(0x03, 0x248F, None, ASM("""
        ldh  a, [$F6] ; load room nr
        cp   $7C  ; L4 Side-view room where the key drops
        jr   nz, notSpecialSideView

        ld   hl, $D969 ; status of the room above the side-view where the key drops in dungeon 4 
        set  4, [hl]
notSpecialSideView:
        call $512A ; mark room as done
        
        ld   a, $01
        call $3FF0
        ; Call the dialog or not?
        ld   a, $02
        call $3FF0
        ret
    """))
