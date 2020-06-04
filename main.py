import binascii
from romTables import ROMWithTables
from assembler import ASM
import randomizer
import patches.core
import patches.phone
import patches.bowwow
import patches.desert
import patches.owl
import patches.shop
import patches.trendy
import patches.chest
import patches.droppedKey
import patches.goldenLeaf
import patches.heartPiece
import patches.seashell
import patches.softlock
import patches.maptweaks
import patches.inventory
import patches.titleScreen
import patches.reduceRNG
import patches.bank3e
import patches.bank3f
import patches.aesthetics
import patches.health
import patches.goal
import explorer
import logic
import os
import time


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('input_filename', metavar='input rom', type=str,
        help="Rom file to use as input.")
    parser.add_argument('-o', '--output', dest="output_filename", metavar='output rom', type=str, required=False,
        help="Output filename to use. If not specified [seed].gbc is used.")
    parser.add_argument('--seedlist', dest="seedlist", metavar='seed list', type=str, required=False,
        help="Instead of generating ROMS, only generate valid seeds and append them to the specified file.")
    parser.add_argument('--dump', dest="dump", action="store_true",
        help="Dump the logic if the given rom (spoilers!)")
    parser.add_argument('--test', dest="test", action="store_true",
        help="Test the logic if the given rom, without showing anything.")
    parser.add_argument('-c', '--count', dest="count", type=int, required=False, default=1,
        help="Repeat the generation this many times.")
    parser.add_argument('-s', '--seed', dest="seed", type=str, required=False,
        help="Generate the specified seed")
    parser.add_argument('--romdebugmode', dest="romdebugmode", action="store_true",
        help="Patch the rom so that debug mode is enabled, this creates a default save with most items and unlocks some debug features.")
    parser.add_argument('--exportmap', dest="exportmap", action="store_true",
        help="Export the map (many graphical mistakes)")

    # Flags that effect gameplay
    parser.add_argument('--multiworld', dest="multiworld", action="store_true",
        help="Generates 2 roms, for link cable use.")
    parser.add_argument('--heartpiece', dest="heartpiece", action="store_true",
        help="Enables randomization of heart pieces.")
    parser.add_argument('--seashells', dest="seashells", action="store_true",
        help="Enables seashells mode, which randomizes the secret sea shells hiding in the ground/trees. (chest are always randomized)")
    parser.add_argument('--keysanity', dest="keysanity", action="store_true",
        help="Enables keysanity mode, which shuffles all dungeon items outside dungeons as well.")
    parser.add_argument('--dungeonshuffle', dest="dungeonshuffle", action="store_true",
        help="Enable dungeon shuffle, puts dungeons on different spots.")
    parser.add_argument('--hpmode', dest="hpmode", choices=['default', 'inverted', '1'], default='default',
        help="Set the HP gamplay mode. Inverted causes health containers to take HP instead of give it and you start with more health. 1 sets your starting health to just 1 hearth.")
    parser.add_argument('--boomerangtrade', dest="boomerangtrade", action="store_true",
        help="Put the boomerang and the trade with the boomerang in the item pool")
    parser.add_argument('--steal', dest="steal", choices=['never', 'always', 'default'], default='always',
        help="Configure when to allow stealing from the shop.")
    parser.add_argument('--goal', dest="goal", type=int, default=8,
        help="Configure the instrument goal for this rom, anything between 0 and 8.")
    parser.add_argument('--quickswap', dest="quickswap", choices=['none', 'a', 'b'], default='none',
        help="Configure quickswap for A or B button (select key swaps, no longer opens map)")

    # Just aestetic flags
    parser.add_argument('--gfxmod', dest="gfxmod", action='append',
        help="Load graphical mods.")
    parser.add_argument('--textmode', dest="textmode", choices=['default', 'fast', 'none'], default='default',
        help="Default just keeps text normal, fast makes text appear twice as fast, and none removes all text from the game.")
    parser.add_argument('--nag-messages', dest="removeNagMessages", action="store_false",
        help="Enable the nag messages on touching stones and crystals. By default they are removed.")
    parser.add_argument('--lowhpbeep', dest="lowhpbeep", choices=['default', 'slow', 'none'], default='slow',
        help="Force the palette of link")
    parser.add_argument('--linkspalette', dest="linkspalette", type=int, default=None,
        help="Force the palette of link")

    args = parser.parse_args()

    start_time = time.monotonic()
    total_retries = 0
    for generation_number in range(args.count):
        print("Loading: %s" % (args.input_filename))
        rom = ROMWithTables(args.input_filename)

        if args.exportmap:
            import mapexport
            mapexport.MapExport(rom)
            sys.exit(0)

        if args.dump or args.test:
            my_logic = logic.Logic(args, None)
            for ii in my_logic.iteminfo_list:
                ii.item = ii.read(rom)
            e = explorer.Explorer(verbose=args.dump)
            e.visit(my_logic.start)
            if len(e.getAccessableLocations()) != len(my_logic.location_list):
                print("Logic failure! Cannot access all locations.")
                print("Failed to find:")
                for loc in my_logic.location_list:
                    if loc not in e.getAccessableLocations():
                        for ii in loc.items:
                            print("%20s: %s" % (ii, ii.read(rom)))
                sys.exit(1)
            sys.exit(0)

        if args.gfxmod:
            for gfx in args.gfxmod:
                patches.aesthetics.gfxMod(rom, gfx)

        patches.core.cleanup(rom)
        patches.phone.patchPhone(rom)
        patches.core.bugfixWrittingWrongRoomStatus(rom)
        patches.owl.removeOwlEvents(rom)
        patches.bank3e.addBank3E(rom)
        patches.bank3f.addBank3F(rom)
        patches.core.removeGhost(rom)
        patches.core.alwaysAllowSecretBook(rom)
        patches.core.warpHome(rom)
        if args.multiworld:
            patches.core.injectMainLoop(rom)
        if args.keysanity:
            patches.inventory.advancedInventorySubscreen(rom)
        patches.softlock.fixAll(rom)
        patches.maptweaks.tweakMap(rom)
        patches.chest.fixChests(rom)
        patches.shop.fixShop(rom)
        patches.trendy.fixTrendy(rom)
        patches.droppedKey.fixDroppedKey(rom)
        patches.goldenLeaf.fixGoldenLeaf(rom)
        patches.heartPiece.fixHeartPiece(rom)
        patches.seashell.fixSeashell(rom)
        patches.bowwow.neverGetBowwow(rom)
        patches.desert.desertAccess(rom)
        # patches.reduceRNG.slowdownThreeOfAKind(rom)
        patches.aesthetics.noSwordMusic(rom)
        patches.aesthetics.reduceMessageLengths(rom)
        if args.textmode == 'fast':
            patches.aesthetics.fastText(rom)
        if args.textmode == 'none':
            patches.aesthetics.fastText(rom)
            patches.aesthetics.noText(rom)
        if args.removeNagMessages:
            patches.aesthetics.removeNagMessages(rom)
        if args.lowhpbeep == 'slow':
            patches.aesthetics.slowLowHPBeep(rom)
        if args.lowhpbeep == 'none':
            patches.aesthetics.removeLowHPBeep(rom)
        if args.linkspalette is not None:
            patches.aesthetics.forceLinksPalette(rom, args.linkspalette)
        if args.romdebugmode:
            # The default rom has this build in, just need to set a flag and we get this save.
            rom.patch(0, 0x0003, "00", "01")

        # Patch the sword check on the shopkeeper turning around.
        if args.steal == 'never':
            rom.patch(4, 0x36F9, "FA4EDB", "3E0000")
        elif args.steal == 'always':
            rom.patch(4, 0x36F9, "FA4EDB", "3E0100")

        if args.hpmode == 'inverted':
            patches.health.setStartHealth(rom, 9)
            patches.health.inverseHealthContainers(rom)
        elif args.hpmode == '1':
            patches.health.setStartHealth(rom, 1)

        patches.goal.setRequiredInstrumentCount(rom, args.goal)

        if args.quickswap == 'a':
            patches.core.quickswap(rom, 1)
        elif args.quickswap == 'b':
            patches.core.quickswap(rom, 0)

        # Show marin outside, even without a sword.
        rom.patch(0x05, 0x0E78, ASM("ld a, [$DB4E]"), ASM("ld a, $01"), fill_nop=True)
        # Make marin ignore the fact that you did not save the tarin yet, and allowing getting her song
        rom.patch(0x05, 0x0E87, ASM("ld a, [$D808]"), ASM("ld a, $10"), fill_nop=True)
        rom.patch(0x05, 0x0F73, ASM("ld a, [$D808]"), ASM("ld a, $10"), fill_nop=True)
        rom.patch(0x05, 0x0FB0, ASM("ld a, [$DB48]"), ASM("ld a, $01"), fill_nop=True)
        # Show marin in the animal village
        rom.patch(0x03, 0x0A86, ASM("ld a, [$DB74]"), ASM("ld a, $01"), fill_nop=True)

        ## Monkey bridge patch, always have the bridge there.
        rom.patch(0x00, 0x333D, ASM("bit 4, e\njr Z, $05"), b"", fill_nop=True)


        if args.seed is not None and args.seed.upper() == "DEFAULT":
            seed = "DEFAULT"
            my_logic = logic.Logic(args, None)
            for ii in my_logic.iteminfo_list:
                ii.item = ii.read(rom)
                ii.patch(rom, ii.item)
            e = explorer.Explorer()
            e.visit(my_logic.start)
            e.dump(my_logic)
            # patches.dungeonEntrances.changeEntrances(rom, [1,2,3,4,5,6,7,8,0])
            # from locations import ShopItem
            # ShopItem(0).patch(rom, "SWORD")
            # from locations import Chest
            # Chest(0x113).patch(rom, "KEY2")
            # from locations import DroppedKey
            # dk = DroppedKey(0x116)
            # dk.patch(rom, "BOW")
            # from locations import StartItem
            # StartItem().patch(rom, "POWER_BRACELET")
        else:
            if args.seed:
                args.seed = binascii.unhexlify(args.seed)
            retry_count = 0
            while True:
                try:
                    r = randomizer.Randomizer(rom, args, seed=args.seed)
                    seed = binascii.hexlify(r.seed).decode("ascii").upper()
                    break
                except randomizer.Error:
                    if args.seed is not None:
                        print("Specified seed does not produce a valid result.")
                        sys.exit(1)
                    retry_count += 1
                    if retry_count > 100:
                        print("Randomization keeps failing, abort!")
                        sys.exit(1)
                    print("Failed, trying again: %d" % (retry_count))
            total_retries += retry_count

        print("Seed: %s" % (seed))
        patches.titleScreen.setRomInfo(rom, seed)

        if args.seedlist:
            f = open(args.seedlist, "at")
            f.write("%s\n" % (seed))
            f.close()
        elif args.output_filename:
            filename = args.output_filename
            if generation_number > 0:
                filename = "%s.%d%s" % (os.path.splitext(filename)[0], generation_number, os.path.splitext(filename)[1])
            rom.save(filename, name=seed)
        else:
            rom.save("LADXR_%s.gbc" % (seed), name=seed)

    if args.count > 1:
        total_time = time.monotonic() - start_time
        print("Generated: %d roms" % (args.count))
        print("Success ratio: %g%%" % (args.count / (args.count + total_retries) * 100))
        print("Total time: %gsec (Per generation: %gsec)" % (total_time, total_time / (args.count + total_retries)))
