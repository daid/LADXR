from roomEditor import RoomEditor, WARP_TYPE_IDS, ObjectWarp
from utils import createTileData
from assembler import ASM
import entityData
import os
import patches.aesthetics


ALL_TILE_ATTR = [
    (0x22, 0x0000),
    (0x22, 0x0400),
    (0x22, 0x0800),
    (0x22, 0x0c00),
    (0x22, 0x1000),
    (0x22, 0x1400),
    (0x22, 0x1800),
    (0x22, 0x1c00),
    (0x22, 0x2000),
    (0x22, 0x2400),
    (0x22, 0x2800),
    (0x22, 0x2c00),
    (0x22, 0x3000),
    (0x22, 0x3400),
    (0x22, 0x3800),
    (0x22, 0x3c00),
    (0x25, 0x0000),
    (0x25, 0x0400),
    (0x25, 0x0800),
    (0x25, 0x0c00),
    (0x25, 0x1000),
    (0x25, 0x1400),
    (0x25, 0x1800),
    (0x25, 0x1c00),
    (0x25, 0x2000),
    (0x25, 0x2400),
    (0x25, 0x2800),
    (0x25, 0x2c00),
    (0x25, 0x3000),
    (0x25, 0x3400),
    (0x25, 0x3800),
    (0x25, 0x3c00),
    (0x27, 0x1220),
    (0x27, 0x1620),
    (0x27, 0x1a20),
    (0x27, 0x1e40),
    (0x27, 0x2240),
    (0x27, 0x2640),
    (0x27, 0x2a40),
    (0x27, 0x2e40),
]


def setMetaTile(rom, tile_id, physics, *args):
    assert len(args) == 4
    rom.banks[8][0x0AD4+tile_id] = physics
    rom.banks[0x1A][0x2B1D+tile_id*4:0x2B1D+tile_id*4+4] = args


def setTileAttr(rom, tile_id, *args, bank=None, addr=None):
    assert len(args) == 4
    if bank is None:
        for bank, addr in ALL_TILE_ATTR:
            rom.banks[bank][addr + tile_id * 4:addr + tile_id * 4 + 4] = args
        return
    rom.banks[bank][addr+tile_id*4:addr+tile_id*4+4] = args


def patch(rom):
    # Make the honeycomb not use any graphics slots.
    entityData.SPRITE_DATA[0xB3] = None

    # New Ledge updates/mountain edges
    setMetaTile(rom, 0x05, 0xD2, 0x4A, 0x4A, 0x7F, 0x7F)
    setTileAttr(rom, 0x05, 0x03, 0x03, 0x00, 0x00)
    setMetaTile(rom, 0x06, 0x01, 0x4A, 0x4A, 0x45, 0x2A)
    setTileAttr(rom, 0x06, 0x03, 0x03, 0x01, 0x01)
    setMetaTile(rom, 0x07, 0x01, 0x4A, 0x4A, 0x2B, 0x45)
    setTileAttr(rom, 0x07, 0x03, 0x03, 0x01, 0x01)
    setMetaTile(rom, 0x63, 0x01, 0x7E, 0x7E, 0x55, 0x56)
    setTileAttr(rom, 0x63, 0x03, 0x03, 0x03, 0x03)

    # Fix up mountain tile attributes
    setTileAttr(rom, 234, 0x03, 0x01, 0x03, 0x01)
    for bank, addr in [(0x27, 0x2240), (0x27, 0x1e40)]:
        setTileAttr(rom, 43, 0x03, 0x03, 0x03, 0x01, bank=bank, addr=addr)
        setTileAttr(rom, 49, 0x03, 0x01, 0x01, 0x01, bank=bank, addr=addr)
        setTileAttr(rom, 53, 0x01, 0x01, 0x03, 0x03, bank=bank, addr=addr)
        setTileAttr(rom, 54, 0x01, 0x01, 0x03, 0x03, bank=bank, addr=addr)
        setTileAttr(rom, 70, 0x03, 0x01, 0x03, 0x01, bank=bank, addr=addr)
        setTileAttr(rom, 71, 0x01, 0x03, 0x01, 0x03, bank=bank, addr=addr)
        setTileAttr(rom, 240, 0x03, 0x07, 0x03, 0x07, bank=bank, addr=addr)
        setTileAttr(rom, 241, 0x03, 0x01, 0x03, 0x01, bank=bank, addr=addr)
        setTileAttr(rom, 242, 0x01, 0x03, 0x01, 0x03, bank=bank, addr=addr)
        setTileAttr(rom, 243, 0x07, 0x03, 0x07, 0x03, bank=bank, addr=addr)
        setTileAttr(rom, 244, 0x01, 0x03, 0x01, 0x03, bank=bank, addr=addr)
        setTileAttr(rom, 0x05, 0x03, 0x03, 0x07, 0x07, bank=bank, addr=addr)
        setTileAttr(rom, 212, 0x03, 0x03, 0x03, 0x03, bank=bank, addr=addr)

    setTileAttr(rom, 233, 0x04, 0x04, 0x04, 0x04, bank=0x22, addr=0x1800)  # Waterfall on swamp tileset
    setTileAttr(rom, 0xE1, 0x03, 0x23, 0x03, 0x23, bank=0x22, addr=0x1800)  # Cave entrance on swamp tileset
    setTileAttr(rom, 0x78, 0x03, 0x03, 0x03, 0x03, bank=0x22, addr=0x2400)  # Horizontal bridge
    setTileAttr(rom, 0x79, 0x03, 0x03, 0x03, 0x03, bank=0x22, addr=0x2400)  # Horizontal bridge

    setTileAttr(rom, 110, 0x01, 0x01, 0x01, 0x01, bank=0x25, addr=0x0C00)  # Donut on general tiles
    setTileAttr(rom, 11, 0x01, 0x01, 0x01, 0x01, bank=0x27, addr=0x1E40)  # Path on eagle tower
    setTileAttr(rom, 67, 0x01, 0x01, 0x03, 0x03, bank=0x27, addr=0x1E40)  # Path+ledge on eagle tower

    # Extra graphics in the desert tileset
    #patches.aesthetics.createPartialImage(rom.banks[0x2F][0x2C00:0x2E00], "patches/overworld/alttp/desert.png")
    rom.banks[0x2F][0x2C00:0x2E00] = patches.aesthetics.imageTo2bpp("patches/overworld/alttp/desert.png", tileheight=8, colormap=[0xFFFFFF, 0xAAAAAA, 0x555555, 0x000000])
    setTileAttr(rom, 205, 0x01, 0x01, 0x01, 0x01, bank=0x22, addr=0x2C00)
    setTileAttr(rom, 206, 0x01, 0x01, 0x01, 0x01, bank=0x22, addr=0x2C00)
    setTileAttr(rom,  94, 0x01, 0x01, 0x01, 0x01, bank=0x22, addr=0x2C00)
    setTileAttr(rom, 182, 0x01, 0x01, 0x01, 0x01, bank=0x22, addr=0x2C00)
    setTileAttr(rom, 176, 0x21, 0x21, 0x21, 0x21, bank=0x22, addr=0x2C00)
    setTileAttr(rom, 227, 0x01, 0x01, 0x02, 0x02, bank=0x22, addr=0x2C00)

    # Town changes
    setTileAttr(rom, 95, 0x06, 0x06, 0x06, 0x06, bank=0x22, addr=0x2800)
    setTileAttr(rom, 96, 0x06, 0x06, 0x06, 0x06, bank=0x22, addr=0x2800)

    # Load all new rooms
    instrument_rooms = [0x102, 0x12A, 0x159, 0x162, 0x182, 0x1B5, 0x22C, 0x230, 0x301]
    path = os.path.dirname(__file__)
    for n in range(0x100):
        re = RoomEditor(rom, n)
        re.entities = []
        re.objects = []
        extra_data = {}
        if os.path.exists("%s/overworld/alttp/%02X.json" % (path, n)):
            extra_data = re.loadFromJson("%s/overworld/alttp/%02X.json" % (path, n))
        entrances = list(filter(lambda obj: obj.type_id in WARP_TYPE_IDS, re.objects))
        for obj in re.getWarps():
            if f"warp_exit_{obj.room:x}" in extra_data:
                target_x, target_y = extra_data[f"warp_exit_{obj.room:02x}"]
            else:
                if not entrances:
                    print(f"Missing entrance for warp in room {n:02x} to {obj.room:02x}")
                    continue
                e = entrances.pop(0)
                target_x, target_y = e.x * 16 + 8, e.y * 16 + 16

            other = RoomEditor(rom, obj.room)
            for o in other.objects:
                if isinstance(o, ObjectWarp) and o.warp_type == 0:
                    o.room = n
                    o.target_x = target_x
                    o.target_y = target_y
            other.store(rom)

            if obj.room == 0x1F5:
                # Patch the boomerang guy exit
                other = RoomEditor(rom, "Alt1F5")
                other.getWarps()[0].room = n
                other.getWarps()[0].target_x = target_x
                other.getWarps()[0].target_y = target_y
                other.store(rom)

            if obj.warp_type == 1 and (obj.map_nr < 8 or obj.map_nr == 0xFF) and obj.room not in (0x1B0, 0x23A, 0x23D):
                other = RoomEditor(rom, instrument_rooms[min(8, obj.map_nr)])
                for o in other.objects:
                    if isinstance(o, ObjectWarp) and o.warp_type == 0:
                        o.room = n
                        o.target_x = target_x
                        o.target_y = target_y
                other.store(rom)
        re.store(rom)
    for n in range(0x100, 0x300):
        if not os.path.exists("%s/overworld/alttp/%03X.json" % (path, n)):
            continue
        re = RoomEditor(rom, n)
        re.entities = []
        re.objects = []
        re.loadFromJson("%s/overworld/alttp/%03X.json" % (path, n))
        re.store(rom)

    patchTarinBeeKeeperToFakeSword(rom)
    patchHoneycombToRock(rom)
    patchMermaidToPeg(rom)
    patchMermaidStatueToCrystalBlock(rom)
    patchWalrusToCastleEndGate(rom)
    patchTurtleRockEntrance(rom)

    rom.patch(0x00, 0x336C, ASM("cp $75"), ASM("cp $69"))  # Stairs under bush at castle
    rom.patch(0x14, 0x1745, ASM("cp $75"), ASM("cp $69"))  # Stairs under bush at castle

    # Skip the whole egg maze.
    rom.patch(0x14, 0x0453, "75", "73")

def patchTarinBeeKeeperToFakeSword(rom):
    rom.patch(0x07, 0x0EB1, 0x1101, ASM("""
    jp ClearEntityStatus_07
    """, 0x4EB1), fill_nop=True)


def patchHoneycombToRock(rom):
    rom.patch(0x07, 0x0C93, 0x0E8D, ASM("""
SpriteData: ; Needs to be 4 bytes!
    db   $F0, $05, $F2, $05

LiftableStatueEntityHandler:
    ldh  a, [hActiveEntityStatus]
    cp   8 ; ENTITY_STATUS_THROWN
    jr   nz, .notThrown
    ld   a, $05
    ldh  [hActiveEntityStatus], a
.notThrown:

    ld   de, SpriteData
    call RenderActiveEntitySpritesPair 
    call $3CD9
    call $7D96 ; ReturnIfNonInteractive_07
    call $0C56 ; DecrementEntityIgnoreHitsCountdown  
    call $3B70
    ldh  a, [hActiveEntityState]
    rst  0
    dw LiftableStatueState0Handler
    dw LiftableStatueState1And2Handler
    dw LiftableStatueState1And2Handler

LiftableStatueState0Handler:
    call $3B23
    call PushLinkOutOfEntity_07
    call $7E5D ; entityLinkPositionXDifference -> func_007_7E5D  
    add  $10
    cp   $20
    jp   nc, label_019_411C

    call $7E6D ; entityLinkPositionYDifference -> func_007_7E6D 
    add  $20
    cp   $30
    jp   nc, label_019_411C

    ld   a, [wLinkAttackStepAnimationCountdown]
    and  a
    jp   nz, label_019_411C

    ld   a, [$DB00] ; wInventoryItems.BButtonSlot 
    cp   $03 ; INVENTORY_POWER_BRACELET
    jr   nz, .jr_40A0

    ldh  a, [hPressedButtonsMask] 
    and  $20 ; J_B
    jr   nz, jr_019_40AD

    jr   label_019_411C

.jr_40A0:
    ld   a, [$DB01] ; wInventoryItems.AButtonSlot  
    cp   $03 ; INVENTORY_POWER_BRACELET
    jr   nz, label_019_411C

    ldh  a, [hPressedButtonsMask]
    and  $10 ; J_A
    jr   z, label_019_411C

jr_019_40AD:
    ld   a, [$C3CF]
    and  a
    jr   nz, label_019_411C

    ld   a, $01
    ldh  [hLinkInteractiveMotionBlocked], a 
    ld   [$C3CF], a
    ldh  a, [hLinkDirection]
    ld   e, a
    ld   d, $00
    ld   hl, $1F51 ; LinkDirectionToLinkAnimationState_2  
    add  hl, de
    ld   a, [hl]
    ldh  [hLinkAnimationState], a 
    ld   hl, $1F55
    add  hl, de
    ldh  a, [hPressedButtonsMask]
    and  [hl]
    jr   z, label_019_411C

    ld   hl, $1F59
    add  hl, de
    ld   a, [hl]
    ld   [$C13C], a
    ld   hl, $1F5D
    add  hl, de
    ld   a, [hl]
    ld   [$C13B], a
    ld   hl, hLinkAnimationState
    inc  [hl]
    ld   a, [wPowerBraceletLevel]
    cp   $02
    jr   nz, label_019_411C

    ld   e, $08
    ld   a, [wActivePowerUp]
    and  a
    jr   z, .jr_40F4

    ld   e, $03

.jr_40F4:
    ld   hl, wEntitiesInertiaTable
    add  hl, bc
    inc  [hl]
    ld   a, [hl]
    cp   e
    jr   c, ret_019_4122

    call IncrementEntityState  
    ld   [hl], $02
    ld   hl, wEntitiesStatusTable
    add  hl, bc
    ld   [hl], $07
    ld   hl, wEntitiesLiftedTable 
    add  hl, bc
    ld   [hl], b
    ldh  a, [hLinkDirection]
    ld   [$C15D], a ; unnamed direction value
    call GetEntityTransitionCountdown  
    ld   [hl], $02
    ld   hl, hWaveSfx
    ld   [hl], $02 ; WAVE_SFX_LIFT_UP 

label_019_411C:
    ld   hl, wEntitiesInertiaTable
    add  hl, bc
    ld   [hl], b
    ret

ret_019_4122:
    ret

LiftableStatueState1And2Handler:
    call $7E0A ; UpdateEntityPosWithSpeed_07 
    call $7E43 ; AddEntityZSpeedToPos_07 
    call $3B23
    ld   hl, wEntitiesSpeedZTable
    add  hl, bc
    dec  [hl]
    dec  [hl]
    ld   hl, wEntitiesCollisionsTable
    add  hl, bc
    ld   a, [hl]
    and  $0F
    jr   nz, .jr_4143

    ld   hl, wEntitiesPosZTable  
    add  hl, bc
    ld   a, [hl]
    and  $80
    ret  z

.jr_4143:
    ; Create chunks
    ld   a, $00

jr_019_4185:
    ldh  [hMultiPurposeG], a
    ld   a, $9D ; ENTITY_LIFTABLE_STATUE 
    call SpawnNewEntity_trampoline
    jr   c, jr_019_41E2

    ld   hl, $C2B0 ; wEntitiesPrivateState1Table  
    add  hl, de
    inc  [hl]

.jr_4193:
    ld   hl, $C340 ; wEntitiesPhysicsFlagsTable  
    add  hl, de
    ld   [hl], $C1 ; 1 | ENTITY_PHYSICS_HARMLESS | ENTITY_PHYSICS_PROJECTILE_NOCLIP 
    push bc
    ldh  a, [hMultiPurposeG] 
    ld   c, a
    ld   hl, Data_019_4165
    add  hl, bc
    ldh  a, [hMultiPurpose0]
    add  [hl]
    ld   hl, wEntitiesPosXTable
    add  hl, de
    ld   [hl], a
    ld   hl, Data_019_416B
    add  hl, bc
    ldh  a, [hMultiPurpose1]
    add  [hl]
    ld   hl, wEntitiesPosYTable
    add  hl, de
    ld   [hl], a
    ldh  a, [$FFDA] ; hMultiPurpose3 
    ld   hl, wEntitiesPosZTable  
    add  hl, de
    ld   [hl], a
    ld   hl, Data_019_4171
    add  hl, bc
    ld   a, [hl]
    ld   hl, wEntitiesSpeedXTable
    add  hl, de
    ld   [hl], a
    ld   hl, Data_019_4177
    add  hl, bc
    ld   a, [hl]
    ld   hl, wEntitiesSpeedYTable
    add  hl, de
    ld   [hl], a
    ld   hl, Data_019_417D
    add  hl, bc
    ld   a, [hl]
    ld   hl, wEntitiesSpeedZTable
    add  hl, de
    ld   [hl], a
    pop  bc
    ldh  a, [hMultiPurposeG]
    inc  a
    cp   $04
    jr   nz, jr_019_4185

jr_019_41E2:
    ld   a, $29 ; NOISE_SFX_BREAK
    ldh  [hNoiseSfx], a
    ldh  a, [hActiveEntityPosX] 
    ldh  [hMultiPurpose0], a
    ldh  a, [hActiveEntityVisualPosY] 
    ldh  [hMultiPurpose1], a
    ld   a, $02 ; TRANSCIENT_VFX_POOF 
    call $0CC7 ; AddTranscientVfx  
    jp   ClearEntityStatus_07

Data_019_4165:
    db   $00, $08, $00, $08

Data_019_416B:
    db   $00, $00, $08, $08

Data_019_4171:
    db   $FA, $06, $FB, $04

Data_019_4177:
    db   $FE, $FF, $03, $02

Data_019_417D:
    db   $13, $16, $12, $14

    """, 0x4C93), fill_nop=True)
    rom.banks[0x03][0xB3] = 0x92  # Physics=harmless, shadow, 2 sprites slots
    rom.patch(0x20, 0x0322 + 0xB3 * 2, ASM("dw $4F83"), ASM("dw $4B56"))  # No init function
    rom.banks[0x03][0x02F1 + 0xB3] = 0x42  # OPT1 = ENTITY_OPT1_SWORD_CLINK_OFF|ENTITY_OPT1_EXCLUDED_FROM_KILL_ALL
    rom.banks[0x03][0x00FB + 0xB3] = 0xA4  # hitbox flags


def patchMermaidToPeg(rom):
    rom.banks[0x03][0xB7] = 0x92  # Physics=harmless, shadow, 2 sprites slots
    rom.banks[0x03][0x02F1 + 0xB7] = 0x42  # OPT1 = ENTITY_OPT1_SWORD_CLINK_OFF|ENTITY_OPT1_EXCLUDED_FROM_KILL_ALL
    rom.banks[0x03][0x00FB + 0xB7] = 0xA4  # hitbox flags
    rom.patch(0x07, 0x06BB, 0x09EC, ASM("""
EntityEntry:
    ldh  a, [hActiveEntityState]
    rst  0
    dw   BasicPeg
    dw   HammerState1
    dw   HammerState2
    dw   PegDestroyed
BasicPeg:
    ld   de, PegSpriteData
    call RenderActiveEntitySpritesPair
    call PushLinkOutOfEntity_07
    ret
PegDestroyed:
    ld   a, $0B
    ldh  [hJingle], a
    ldh  a, [hActiveEntityPosX]
    ldh  [hMultiPurpose0], a
    ldh  a, [hActiveEntityVisualPosY] 
    ldh  [hMultiPurpose1], a
    ld   a, $02 ; TRANSCIENT_VFX_POOF 
    call $0CC7 ; AddTranscientVfx
    call ClearEntityStatus_07
    ld   a, [hMapRoom]
    cp   $0F
    ret  nz
    
.seachPegsLoop:
    ld   hl, wEntitiesStatusTable
    add  hl, de
    ld   a, [hl]
    and  a
    jr   z, .noEntity
    ld   hl, wEntitiesTypeTable
    add  hl, de
    ld   a, [hl]
    cp   $B7
    jr   nz, .noEntity
    ld   hl, wEntitiesStateTable
    add  hl, de
    ld   a, [hl]
    and  a
    jr   nz, .noEntity
    ret  ; Peg found, so entrance not opening yet
.noEntity:
    dec  e
    ld   a, e
    cp   $FF
    jr   nz, .seachPegsLoop

    ; Open D3 entrance
    ld   a, $23 ; JINGLE_DUNGEON_OPENED 
    ldh  [hJingle], a
    call $0C4B ; PlayBombExplosionSfx
    
    ld   a, $14
    ld   [wFarcallBank], a
    ld   a, $57
    ld   [wFarcallAdressHigh], a
    ld   a, $67
    ld   [wFarcallAdressLow], a
    ld   a, $07
    ld   [wFarcallReturnBank], a
    call Farcall

    ret

HammerSpriteData: ; Needs this number of bytes to align the entry point
    db   $02, $2C, $00, $2C, $00, $0C, $02, $0C, $04, $4C, $06, $0C, $06, $0C, $04, $0C

PegSpriteData:
    db   $F0, $09, $F0, $29

HammerState1:
    ld   a, $0E
    ld   [wLinkAttackStepAnimationCountdown], a
    call GetEntityTransitionCountdown
    ld   [hl], $0E
    call IncrementEntityState
    ld   a, $07
    ldh  [hNoiseSfx], a
    call HammerState2
    ld   d, b
    ld   e, $F
.seachPegsLoop:
    ld   hl, wEntitiesStatusTable
    add  hl, de
    ld   a, [hl]
    and  a
    jr   z, .noEntity
    ld   hl, wEntitiesTypeTable
    add  hl, de
    ld   a, [hl]
    cp   $B7
    jr   nz, .noEntity
    ld   hl, wEntitiesStateTable
    add  hl, de
    ld   a, [hl]
    and  a
    jr   nz, .noEntity
    ld   hl, wEntitiesPosXTable
    add  hl, de
    ldh  a, [hActiveEntityPosX]
    sub  [hl]
    add  8
    sub  16
    jr   nc, .noEntity
    ld   hl, wEntitiesPosYTable
    add  hl, de
    ldh  a, [hActiveEntityPosY]
    sub  [hl]
    add  8
    sub  16
    jr   nc, .noEntity

    ld   hl, wEntitiesStateTable
    add  hl, de
    ld   [hl], 3

.noEntity:
    dec  e
    ld   a, e
    cp   $FF
    jr   nz, .seachPegsLoop
    ret 

HammerState2:
    ldh  a, [hLinkDirection]
    ld   hl, wEntitiesSpriteVariantTable
    add  hl, bc
    ld   [hl], a
    ldh  [hActiveEntitySpriteVariant], a
    ld   d, b
    ld   e, a
    ld   hl, OffsetX
    add  hl, de
    ldh  a, [hLinkPositionX]
    add  [hl]
    ldh  [hActiveEntityPosX], a
    ld   hl, OffsetY
    add  hl, de
    ldh  a, [hLinkPositionY]
    add  [hl]
    ldh  [hActiveEntityPosY], a
    ld   hl, hLinkPositionZ
    add  [hl]
    ldh  [hActiveEntityVisualPosY], a
    ld   a, [hl]
    ld   hl, wEntitiesPosZTable
    add  hl, bc
    ld   [hl], a

    ld   de, HammerSpriteData
    call RenderActiveEntitySpritesPair
    
    call GetEntityTransitionCountdown
    jp   z, ClearEntityStatus_07
    dec  [hl]
    ret

OffsetX:
    db 14, $100-14, 0, 0
OffsetY:
    db 0, 0, $100-12, 12
    """, 0x46BB), fill_nop=True)
    rom.banks[0x3F][0x3700:0x3720] = createTileData("""    ....    
   .2222
  .22233
 .222322
 .322322
 .322322
 .332233
 ..33222
 2.33332
  ...333
22.3....
 2.33232
 2..3232
222.3332
  22....
   22222""", " .32")
    rom.banks[0x3F][0x2800:0x2880] = patches.aesthetics.imageTo2bpp("patches/overworld/alttp/hammer.png", tileheight=16, colormap=[0xFFFFFF, 0xAAAAAA, 0x555555, 0x000000])


def patchMermaidStatueToCrystalBlock(rom):
    rom.banks[0x03][0xCE] = 0x92  # Physics=harmless, shadow, 2 sprites slots
    rom.banks[0x03][0x02F1 + 0xCE] = 0x42  # OPT1 = ENTITY_OPT1_SWORD_CLINK_OFF|ENTITY_OPT1_EXCLUDED_FROM_KILL_ALL
    rom.banks[0x03][0x00FB + 0xCE] = 0xA4  # hitbox flags
    rom.patch(0x18, 0x0928, 0x09C0, ASM("""
SpriteData:  ; Needs this number of bytes to align the entry point
    db   $F2, $0D, $F4, $0D, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00

EntityEntry:
    ld   de, SpriteData
    call RenderActiveEntitySpritesPair
    call PushLinkOutOfEntity_18
    ret

    """, 0x4928), fill_nop=True)
    rom.banks[0x3F][0x3720:0x3730] = rom.banks[0x2D][0x1900:0x1910]
    rom.banks[0x3F][0x3730:0x3740] = rom.banks[0x2D][0x1920:0x1930]
    rom.banks[0x3F][0x3740:0x3750] = rom.banks[0x2D][0x1910:0x1920]
    rom.banks[0x3F][0x3750:0x3760] = rom.banks[0x2D][0x1930:0x1940]

def patchWalrusToCastleEndGate(rom):
    rom.patch(0x18, 0x1501, 0x19B7, ASM("""
EntityEntry:
    call PushLinkOutOfEntity_18
    call GetRandomByte
    and  $18
    ld   d, b
    ld   e, a
    ld   hl, SpriteData
    add  hl, de
    ld   c, $04
    jp   RenderActiveEntitySpritesRect
SpriteData:
    db   $08, $00, $70, $02
    db   $08, $08, $70, $42
    db   $08, $10, $70, $02
    db   $08, $18, $70, $42

    db   $08, $00, $70, $04
    db   $08, $08, $70, $44
    db   $08, $10, $70, $04
    db   $08, $18, $70, $44

    db   $08, $00, $70, $42
    db   $08, $08, $70, $02
    db   $08, $10, $70, $42
    db   $08, $18, $70, $02

    db   $08, $00, $70, $44
    db   $08, $08, $70, $04
    db   $08, $10, $70, $44
    db   $08, $18, $70, $04

    """, 0x5501), fill_nop=True)
    rom.banks[0x31][0x2F00:0x2F80] = patches.aesthetics.imageTo2bpp("patches/overworld/alttp/walrus.png", tileheight=16, colormap=[0xFFFFFF, 0xAAAAAA, 0x555555, 0x000000])
    rom.patch(0x19, 0x0C34, 0x0CE7, ASM("""
    ld   a, $23 ; JINGLE_DUNGEON_OPENED 
    ldh  [hJingle], a
    call $0C4B ; PlayBombExplosionSfx

    ld   d, b
    ld   e, $F
seachWalrusLoop:
    ld   hl, wEntitiesStatusTable
    add  hl, de
    ld   a, [hl]
    and  a
    jr   z, .noEntity
    ld   hl, wEntitiesTypeTable
    add  hl, de
    ld   a, [hl]
    cp   $C4
    jr   nz, .noEntity

    ld   hl, wEntitiesStatusTable
    add  hl, de
    ld   [hl], b

.noEntity:
    dec  e
    ld   a, e
    cp   $FF
    jr   nz, seachWalrusLoop

    """, 0x4C34), fill_nop=True)


def patchTurtleRockEntrance(rom):
    rom.patch(0x18, 0x3301, 0x3726, ASM("""
    ld   de, SpriteData
    call RenderActiveEntitySpritesPair
    call PushLinkOutOfEntity_18

    ld   a, [$C166] ; wLinkPlayingOcarinaCountdown 
    cp   $01
    ret  nz

    ld   a, [$DB49] ; wOcarinaSongFlags
    and  1
    ret  z

    ld   a, [wSelectedSongIndex]
    cp   $02
    ret  nz

    ld   a, $23 ; JINGLE_DUNGEON_OPENED 
    ldh  [hJingle], a
    call $0C4B ; PlayBombExplosionSfx

    ld   a, $39 ; MUSIC_TURTLE_ROCK_ENTRANCE_BOSS 
    ld   [$D368], a  ; wMusicTrackToPlay  
    ldh  [$FFB0], a  ; hDefaultMusicTrack
    ldh  [$FFBD], a  ; hDefaultMusicTrackAlt 
    ldh  [$FFBF], a  ; hNextDefaultMusicTrack 

    jp   ClearEntityStatus_18
SpriteData:
    db   $76, $01, $76, $21
    """, 0x7301) ,fill_nop=True)