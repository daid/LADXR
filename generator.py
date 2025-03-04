import binascii
import importlib.util
import importlib.machinery
import os

from romTables import ROMWithTables
import assembler
import utils
import mapgen
import patches.overworld
import patches.dungeon
import patches.entrances
import patches.enemies
import patches.titleScreen
import patches.aesthetics
import patches.music
import patches.core
import patches.phone
import patches.photographer
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
import patches.rooster
import patches.shop
import patches.evilshop
import patches.trendy
import patches.goal
import patches.hardMode
import patches.weapons
import patches.health
import patches.heartPiece
import patches.droppedKey
import patches.goldenLeaf
import patches.songs
import patches.bowwow
import patches.follower
import patches.desert
import patches.reduceRNG
import patches.madBatter
import patches.tunicFairy
import patches.seashell
import patches.instrument
import patches.endscreen
import patches.save
import patches.bingo
import patches.maze
import patches.multiworld
import patches.tradeSequence
import patches.alttp
import patches.colorBook
import hints
import locations.keyLocation


# Function to generate a final rom, this patches the rom with all required patches
def generateRom(args, settings, seed, logic, *, rnd=None, multiworld=None):
    print("Loading: %s" % (args.input_filename))
    rom = ROMWithTables(open(args.input_filename, 'rb'))

    pymods = []
    if args.pymod:
        for pymod in args.pymod:
            spec = importlib.util.spec_from_loader(pymod, importlib.machinery.SourceFileLoader(pymod, pymod))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            pymods.append(module)
    for pymod in pymods:
        pymod.prePatch(rom)

    if settings.gfxmod:
        patches.aesthetics.gfxMod(rom, os.path.join(os.path.dirname(__file__), "gfx", settings.gfxmod))

    assembler.resetConsts()
    assembler.const("INV_SIZE", 16)

    #assembler.const("HARDWARE_LINK", 1)
    assembler.const("HARD_MODE", 1 if settings.hardmode != "none" else 0)

    patches.core.cleanup(rom)
    patches.core.fixD7exit(rom)
    if multiworld is not None:
        patches.save.singleSaveSlot(rom)
    patches.phone.patchPhone(rom)
    patches.photographer.fixPhotographer(rom)
    patches.core.bugfixWrittingWrongRoomStatus(rom)
    patches.core.bugfixBossroomTopPush(rom)
    patches.core.bugfixPowderBagSprite(rom)
    patches.core.fixEggDeathClearingItems(rom)
    patches.core.disablePhotoPrint(rom)
    patches.core.easyColorDungeonAccess(rom)
    patches.owl.removeOwlEvents(rom)
    patches.enemies.fixArmosKnightAsMiniboss(rom)
    patches.bank3e.addBank3E(rom, seed, settings)
    patches.bank3f.addBank3F(rom)
    patches.core.removeGhost(rom)
    patches.core.fixMarinFollower(rom)
    patches.core.fixWrongWarp(rom)
    patches.core.alwaysAllowSecretBook(rom)
    patches.core.injectMainLoop(rom)
    if settings.dungeon_items in ('localnightmarekey', 'keysanity', 'smallkeys', 'nightmarekeys'):
        patches.inventory.advancedInventorySubscreen(rom)
    patches.inventory.moreSlots(rom)
    if settings.witch:
        patches.witch.updateWitch(rom)
    patches.softlock.fixAll(rom)
    if not settings.rooster:
        patches.maptweaks.tweakMap(rom)
        patches.maptweaks.tweakBirdKeyRoom(rom)
    patches.chest.fixChests(rom)
    patches.shop.fixShop(rom, allow_both=settings.shopsanity != '', shopsanity=settings.shopsanity != '')
    if settings.evilshop != '':
        patches.evilshop.addEvilShop(rom)
    patches.rooster.patchRooster(rom)
    patches.trendy.fixTrendy(rom)
    patches.droppedKey.fixDroppedKey(rom)
    patches.madBatter.upgradeMadBatter(rom)
    patches.tunicFairy.upgradeTunicFairy(rom)
    patches.tarin.updateTarin(rom)
    patches.fishingMinigame.updateFinishingMinigame(rom)
    patches.health.upgradeHealthContainers(rom)
    if settings.owlstatues in ("dungeon", "both"):
        patches.owl.upgradeDungeonOwlStatues(rom)
    if settings.owlstatues in ("overworld", "both"):
        patches.owl.upgradeOverworldOwlStatues(rom)
    patches.goldenLeaf.fixGoldenLeaf(rom)
    patches.heartPiece.fixHeartPiece(rom)
    patches.seashell.fixSeashell(rom)
    patches.instrument.fixInstruments(rom)
    patches.seashell.upgradeMansion(rom)
    patches.songs.upgradeMarin(rom)
    patches.songs.upgradeManbo(rom)
    patches.songs.upgradeMamu(rom)
    if settings.tradequest:
        patches.tradeSequence.patchTradeSequence(rom, settings)
    else:
        patches.tradeSequence.unrequiredTradeSequence(rom)
    patches.bowwow.fixBowwow(rom)
    patches.follower.patchFollowerCreation(rom, bowwow_everywhere=settings.bowwow != 'normal', extra_spawn=settings.follower)
    if settings.bowwow != 'normal':
        patches.bowwow.bowwowMapPatches(rom)
    patches.desert.desertAccess(rom)
    if settings.overworld == 'dungeondive':
        patches.overworld.patchOverworldTilesets(rom)
        patches.overworld.createDungeonOnlyOverworld(rom)
    elif settings.overworld == 'dungeonchain':
        patches.shop.changeShopPrices(rom, 200, 500)
        patches.dungeon.patchDungeonChain(rom, logic.world_setup)
    elif settings.overworld == 'nodungeons':
        patches.dungeon.patchNoDungeons(rom)
    elif settings.overworld == 'alttp':
        patches.overworld.patchOverworldTilesets(rom)
        patches.alttp.patch(rom)
    elif settings.overworld == 'random':
        patches.overworld.patchOverworldTilesets(rom)
        mapgen.store_map(rom, logic.world.map)
    if settings.dungeon_items == 'keysy':
        patches.dungeon.removeKeyDoors(rom)
    # patches.reduceRNG.slowdownThreeOfAKind(rom)
    patches.reduceRNG.fixHorseHeads(rom)
    patches.bomb.onlyDropBombsWhenHaveBombs(rom)
    patches.colorBook.fixColorBook(rom)
    patches.aesthetics.noSwordMusic(rom)
    patches.aesthetics.reduceMessageLengths(rom, rnd)
    patches.aesthetics.allowColorDungeonSpritesEverywhere(rom)
    if settings.overworld == "alttp":
        # Only apply this to ALTTP right now, as it might cause issues otherwise.
        patches.aesthetics.allowOverworldBackgroundTileTransitions(rom)
    if settings.music == 'random':
        patches.music.randomizeMusic(rom, rnd)
    elif settings.music == 'off':
        patches.music.noMusic(rom)
    elif settings.music == 'shifted':
        patches.music.shiftedMusic(rom)
    if settings.noflash:
        patches.aesthetics.removeFlashingLights(rom)
    if settings.hardmode == "oracle":
        patches.hardMode.oracleMode(rom)
    elif settings.hardmode == "hero":
        patches.hardMode.heroMode(rom)
    elif settings.hardmode == "ohko":
        patches.hardMode.oneHitKO(rom)
    if settings.superweapons:
        patches.weapons.patchSuperWeapons(rom)
    if settings.textmode == 'fast':
        patches.aesthetics.fastText(rom)
    if settings.textmode == 'none':
        patches.aesthetics.fastText(rom)
        patches.aesthetics.noText(rom)
    if not settings.nagmessages:
        patches.aesthetics.removeNagMessages(rom)
    if settings.lowhpbeep == 'slow':
        patches.aesthetics.slowLowHPBeep(rom)
    if settings.lowhpbeep == 'none' or settings.hardmode == 'ohko':
        patches.aesthetics.removeLowHPBeep(rom)
    if 0 <= int(settings.linkspalette):
        patches.aesthetics.forceLinksPalette(rom, int(settings.linkspalette))
    if args.romdebugmode:
        # The default rom has this build in, just need to set a flag and we get this save.
        rom.patch(0, 0x0003, "00", "01")

    # Patch the sword check on the shopkeeper turning around.
    if settings.steal == 'never' or settings.overworld == "dungeonchain":
        rom.patch(4, 0x36F9, "FA4EDB", "3E0000")
    elif settings.steal == 'always':
        rom.patch(4, 0x36F9, "FA4EDB", "3E0100")
    elif settings.steal == 'ggs':
        rom.patch(4, 0x36F9, "FA4EDB", "3E0000")
        patches.shop.preventShopSaveAndQuitTheft(rom)

    if settings.shopsanity != '':
        patches.shop.changeShopPrices(rom, 100, 200)
        patches.shop.createShopRoom(rom, 0x2CB)
        patches.shop.createShopRoom(rom, 0x29B)
        patches.shop.createShopRoom(rom, 0x2B4)
        patches.shop.createShopRoom(rom, 0x29C)
        patches.shop.createShopRoom(rom, 0x29D)
        patches.shop.createShopRoom(rom, 0x2CC)
        patches.shop.createShopRoom(rom, 0x2E3)
        patches.shop.createShopRoom(rom, 0x299)
        rom.texts[0x030] = utils.formatText("Only %d {RUPEES}!" % (100,), ask="Buy  No Way")
        rom.texts[0x02C] = utils.formatText("Only %d {RUPEES}!" % (200,), ask="Buy  No Way")

    if settings.hpmode == 'inverted':
        patches.health.setStartHealth(rom, 9)
    elif settings.hpmode == '1':
        patches.health.setStartHealth(rom, 1)
    elif settings.hpmode == '5hit':
        if settings.hardmode == 'ohko':
            patches.health.setStartHealth(rom, 1)
        else:
            patches.health.setStartHealth(rom, 5)
        patches.health.limitHitChallange(rom)

    patches.inventory.songSelectAfterOcarinaSelect(rom)
    if settings.quickswap == 'a':
        patches.core.quickswap(rom, 1)
    elif settings.quickswap == 'b':
        patches.core.quickswap(rom, 0)

    if multiworld is None:
        hints.addHints(rom, rnd, logic.iteminfo_list)

        world_setup = logic.world_setup
        item_list = logic.iteminfo_list
    else:
        patches.multiworld.addMultiworldShop(rom, multiworld, settings.multiworld)

        # Set a unique ID in the rom for multiworld
        for n in range(4):
            rom.patch(0x00, 0x0051 + n, "00", "%02x" % (seed[n]))
        rom.patch(0x00, 0x0055, "00", "%02x" % (multiworld))
        rom.patch(0x00, 0x0056, "00", "01") # Set the Bizhawk connector version.

        world_setup = logic.worlds[multiworld].world_setup
        item_list = [spot for spot in logic.iteminfo_list if spot.world == multiworld]

    if world_setup.goal == "raft":
        patches.goal.setRaftGoal(rom)
    elif world_setup.goal in ("bingo", "bingo-double", "bingo-triple", "bingo-full"):
        patches.bingo.setBingoGoal(rom, world_setup.bingo_goals, world_setup.goal)
    elif world_setup.goal == "maze":
        patches.maze.patchMaze(rom, world_setup.sign_maze[0], world_setup.sign_maze[1])
    elif world_setup.goal == "seashells":
        patches.goal.setSeashellGoal(rom, 20)
    elif isinstance(world_setup.goal, str) and world_setup.goal.startswith("="):
        patches.goal.setSpecificInstruments(rom, [int(c) for c in world_setup.goal[1:]])
    else:
        patches.goal.setRequiredInstrumentCount(rom, world_setup.goal)

    # Patch the generated logic into the rom
    patches.chest.setMultiChest(rom, world_setup.multichest)
    if settings.overworld not in {"dungeondive", "dungeonchain", "random", "alttp"}:
        patches.entrances.changeEntrances(rom, world_setup.entrance_mapping)
    for spot in item_list:
        if spot.item and spot.item.startswith("*"):
            spot.item = spot.item[1:]
        spot.patch(rom, spot.item)
    patches.enemies.changeBosses(rom, world_setup.boss_mapping)
    patches.enemies.changeMiniBosses(rom, world_setup.miniboss_mapping)
    if settings.enemies == "overworld":
        patches.enemies.randomizeEnemies(rom, seed)

    if not args.romdebugmode:
        patches.core.addFrameCounter(rom, len([spot for spot in item_list if type(spot) != locations.keyLocation.KeyLocation]))

    patches.core.warpHome(rom, settings.overworld == "dungeonchain" or settings.entranceshuffle in ("chaos", "insane", "madness"))  # Needs to be done after setting the start location.
    patches.titleScreen.setRomInfo(rom, binascii.hexlify(seed).decode("ascii").upper(), settings)
    patches.endscreen.updateEndScreen(rom)
    patches.aesthetics.updateSpriteData(rom)
    if args.doubletrouble:
        patches.enemies.doubleTrouble(rom)
    for pymod in pymods:
        pymod.postPatch(rom)
    return rom
