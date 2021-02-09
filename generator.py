import random
import binascii
from romTables import ROMWithTables
import assembler
import patches.overworld
import patches.dungeonEntrances
import patches.startLocation
import patches.enemies
import patches.titleScreen
import patches.aesthetics
import patches.core
import patches.phone
import patches.owl
import patches.bank3e
import patches.bank3f
import patches.inventory
import patches.witch
import patches.tarin
import patches.fishingMinigame
import patches.softlock
import patches.maptweaks
import patches.chest
import patches.bomb
import patches.shop
import patches.trendy
import patches.goal
import patches.hardMode
import patches.health
import patches.heartPiece
import patches.droppedKey
import patches.goldenLeaf
import patches.songs
import patches.bowwow
import patches.desert
import patches.reduceRNG
import patches.madBatter
import patches.tunicFairy
import patches.seashell
import patches.instrument
import patches.endscreen
import hints


# Function to generate a final rom, this patches the rom with all required patches
def generateRom(options, seed, logic, multiworld=None):
    print("Loading: %s" % (options.input_filename))
    rom = ROMWithTables(options.input_filename)

    if options.gfxmod:
        for gfx in options.gfxmod:
            patches.aesthetics.gfxMod(rom, gfx)

    expanded_inventory = options.witch or options.boomerang == 'gift'
    assembler.resetConsts()
    if expanded_inventory:
        assembler.const("INV_SIZE", 16)
        assembler.const("wHasFlippers", 0xDB3E)
        assembler.const("wHasMedicine", 0xDB3F)
        assembler.const("wTradeSequenceItem", 0xDB40)
        assembler.const("wSeashellsCount", 0xDB41)
    else:
        assembler.const("INV_SIZE", 12)
        assembler.const("wHasFlippers", 0xDB0C)
        assembler.const("wHasMedicine", 0xDB0D)
        assembler.const("wTradeSequenceItem", 0xDB0E)
        assembler.const("wSeashellsCount", 0xDB0F)
    assembler.const("wGoldenLeaves", 0xDB42)  # New memory location where to store the golden leaf counter
    assembler.const("wCollectedTunics", 0xDB6D)  # Memory location where to store which tunic options are available
    assembler.const("wCustomMessage", 0xC0A0)

    assembler.const("wLinkState", 0xDE10)
    # We store the link info in unused color dungeon flags, so it gets preserved in the savegame.
    assembler.const("wLinkSyncSequenceNumber", 0xDDF6)
    assembler.const("wLinkStatusBits", 0xDDF7)
    assembler.const("wLinkGiveItem", 0xDDF8)
    assembler.const("wLinkGiveItemFrom", 0xDDF9)
    assembler.const("wLinkSendItemRoomHigh", 0xDDFA)
    assembler.const("wLinkSendItemRoomLow", 0xDDFB)
    assembler.const("wLinkSendItemTarget", 0xDDFC)
    assembler.const("wLinkSendItemItem", 0xDDFD)
    assembler.const("HARD_MODE", 1 if options.hardMode else 0)

    patches.core.cleanup(rom)
    patches.phone.patchPhone(rom)
    patches.core.bugfixWrittingWrongRoomStatus(rom)
    patches.core.bugfixBossroomTopPush(rom)
    patches.core.bugfixPowderBagSprite(rom)
    patches.owl.removeOwlEvents(rom)
    patches.bank3e.addBank3E(rom, seed)
    patches.bank3f.addBank3F(rom)
    patches.core.removeGhost(rom)
    patches.core.alwaysAllowSecretBook(rom)
    patches.core.injectMainLoop(rom)
    if options.keysanity:
        patches.inventory.advancedInventorySubscreen(rom)
    if expanded_inventory:
        patches.inventory.moreSlots(rom)
    if options.witch:
        patches.witch.updateWitch(rom)
    patches.softlock.fixAll(rom)
    patches.maptweaks.tweakMap(rom)
    patches.chest.fixChests(rom)
    patches.shop.fixShop(rom)
    patches.trendy.fixTrendy(rom)
    patches.droppedKey.fixDroppedKey(rom)
    patches.madBatter.upgradeMadBatter(rom)
    patches.tunicFairy.upgradeTunicFairy(rom)
    patches.tarin.updateTarin(rom)
    patches.fishingMinigame.updateFinishingMinigame(rom)
    patches.health.upgradeHealthContainers(rom)
    if options.owlstatues in ("dungeon", "both"):
        patches.owl.upgradeDungeonOwlStatues(rom)
    if options.owlstatues in ("overworld", "both"):
        patches.owl.upgradeOverworldOwlStatues(rom)
    patches.goldenLeaf.fixGoldenLeaf(rom)
    patches.heartPiece.fixHeartPiece(rom)
    patches.seashell.fixSeashell(rom)
    patches.instrument.fixInstruments(rom)
    patches.seashell.upgradeMansion(rom)
    patches.songs.upgradeMarin(rom)
    patches.songs.upgradeManbo(rom)
    patches.songs.upgradeMamu(rom)
    patches.bowwow.fixBowwow(rom, everywhere=options.bowwow != 'normal')
    if options.bowwow != 'normal':
        patches.bowwow.bowwowMapPatches(rom)
    patches.desert.desertAccess(rom)
    if options.overworld == 'dungeondive':
        patches.overworld.patchOverworldTilesets(rom)
        patches.overworld.createDungeonOnlyOverworld(rom)
    # patches.reduceRNG.slowdownThreeOfAKind(rom)
    patches.reduceRNG.fixHorseHeads(rom)
    patches.bomb.onlyDropBombsWhenHaveBombs(rom)
    patches.aesthetics.noSwordMusic(rom)
    patches.aesthetics.reduceMessageLengths(rom)
    patches.aesthetics.allowColorDungeonSpritesEverywhere(rom)
    if options.hardMode:
        patches.hardMode.enableHardMode(rom)
    if options.textmode == 'fast':
        patches.aesthetics.fastText(rom)
    if options.textmode == 'none':
        patches.aesthetics.fastText(rom)
        patches.aesthetics.noText(rom)
    if options.removeNagMessages:
        patches.aesthetics.removeNagMessages(rom)
    if options.lowhpbeep == 'slow':
        patches.aesthetics.slowLowHPBeep(rom)
    if options.lowhpbeep == 'none':
        patches.aesthetics.removeLowHPBeep(rom)
    if options.linkspalette is not None:
        patches.aesthetics.forceLinksPalette(rom, options.linkspalette)
    if options.romdebugmode:
        # The default rom has this build in, just need to set a flag and we get this save.
        rom.patch(0, 0x0003, "00", "01")

    # Patch the sword check on the shopkeeper turning around.
    if options.steal == 'never':
        rom.patch(4, 0x36F9, "FA4EDB", "3E0000")
    elif options.steal == 'always':
        rom.patch(4, 0x36F9, "FA4EDB", "3E0100")

    if options.hpmode == 'inverted':
        patches.health.setStartHealth(rom, 9)
    elif options.hpmode == '1':
        patches.health.setStartHealth(rom, 1)

    if options.goal == "raft":
        patches.goal.setRaftGoal(rom)
    elif options.goal == "seashells":
        patches.goal.setSeashellGoal(rom, 20)
    elif options.goal != "random" and options.goal is not None:
        patches.goal.setRequiredInstrumentCount(rom, int(options.goal))

    patches.inventory.selectToSwitchSongs(rom)
    if options.quickswap == 'a':
        patches.core.quickswap(rom, 1)
    elif options.quickswap == 'b':
        patches.core.quickswap(rom, 0)

    # Monkey bridge patch, always have the bridge there.
    rom.patch(0x00, 0x333D, assembler.ASM("bit 4, e\njr Z, $05"), b"", fill_nop=True)

    if multiworld is None:
        hints.addHints(rom, random.Random(seed), logic.iteminfo_list)

        # Patch the generated logic into the rom
        patches.startLocation.setStartLocation(rom, logic.world_setup.start_house_index)
        patches.dungeonEntrances.changeEntrances(rom, logic.world_setup.dungeon_entrance_mapping)
        for spot in logic.iteminfo_list:
            spot.patch(rom, spot.item)
        patches.enemies.changeBosses(rom, logic.world_setup.boss_mapping)
        patches.enemies.changeMiniBosses(rom, logic.world_setup.miniboss_mapping)
    else:
        # Set a unique ID in the rom for multiworld
        for n in range(4):
            rom.patch(0x00, 0x0051 + n, "00", "%02x" % (seed[n]))
        rom.patch(0x00, 0x0055, "00", "%02x" % (multiworld))

        # Patch the generated logic into the rom
        patches.startLocation.setStartLocation(rom, logic.worlds[multiworld].world_setup.start_house_index)
        if logic.worlds[multiworld].world_setup.entrance_mapping:
            patches.dungeonEntrances.changeEntrances(rom, logic.worlds[multiworld].world_setup.dungeon_entrance_mapping)
        for spot in logic.iteminfo_list:
            if spot.world == multiworld:
                spot.patch(rom, spot.item)
        patches.enemies.changeBosses(rom, logic.worlds[multiworld].world_setup.boss_mapping)
        patches.enemies.changeMiniBosses(rom, logic.worlds[multiworld].world_setup.miniboss_mapping)

    patches.core.warpHome(rom)  # Needs to be done after setting the start location.
    patches.titleScreen.setRomInfo(rom, binascii.hexlify(seed).decode("ascii").upper(), options)
    patches.endscreen.updateEndScreen(rom)
    return rom
