CheckIfLoadBowWow:
        ; Check has bowwow flag
        ld   a, [$DB56]
        cp   $01
        jr   nz, .noLoadBowwow

        ldh  a, [$F6] ; load map number
        cp   $22
        jr   z, .loadBowwow
        cp   $23
        jr   z, .loadBowwow
        cp   $24
        jr   z, .loadBowwow
        cp   $32
        jr   z, .loadBowwow
        cp   $33
        jr   z, .loadBowwow
        cp   $34
        jr   z, .loadBowwow

.noLoadBowwow:
        ld   e, $00
        jp   Exit

.loadBowwow:
        ld   e, $01
        jp   Exit
