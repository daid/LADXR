import binascii
from romTables import ROMWithTables
from assembler import ASM
import randomizer
import patches.core
import patches.bowwow
import patches.desert
import patches.owl
import patches.chest
import patches.droppedKey
import patches.softlock
import patches.titleScreen
import patches.reduceRNG
import patches.bank3e
import patches.bank3f
import locations.itemInfo
import locations.location
import explorer
import utils
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
            for ii in locations.itemInfo.ItemInfo.all:
                ii.item = ii.read(rom)
            e = explorer.Explorer(verbose=args.dump)
            e.visit(logic.start)
            if len(e.getAccessableLocations()) != len(locations.location.Location.all):
                print("Logic failure! Cannot access all locations.")
                for loc in locations.location.Location.all:
                    if loc not in e.getAccessableLocations():
                        for ii in loc.items:
                            print(ii, ii.read(rom))
                sys.exit(1)
            sys.exit(0)

        patches.core.cleanup(rom)
        patches.bank3e.addBank3E(rom)
        patches.bank3f.addBank3F(rom)
        patches.owl.removeOwlEvents(rom)
        patches.core.noSwordMusic(rom)
        patches.core.removeGhost(rom)
        # patches.core.removeBirdKeyHoleDrop(rom)
        patches.core.alwaysAllowSecretBook(rom)
        patches.core.flameThrowerShieldRequirement(rom)
        patches.softlock.fixAll(rom)
        patches.chest.fixChests(rom)
        patches.droppedKey.fixDroppedKey(rom)
        patches.bowwow.neverGetBowwow(rom)
        patches.desert.desertAccess(rom)
        patches.reduceRNG.slowdownThreeOfAKind(rom)
        if args.romdebugmode:
            # The default rom has this build in, just need to set a flag and we get this save.
            rom.patch(0, 0x0003, "00", "01")


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

        # Remove "this object is heavy, bla bla", and other nag messages when touching an object
        rom.patch(0x02, 0x2B8A, ASM("ld a, [$C5A6]\nand a"), ASM("ld a, $01\nand a"), fill_nop=True)
        rom.patch(0x02, 0x32EC, ASM("ld a, [$C5A6]\nand a"), ASM("ld a, $01\nand a"), fill_nop=True)

        # Low health beep patches
        rom.patch(2,  0x2338, ASM("ld a, $30"), ASM("ld a, $60")) # slow slow hp beep
        #rom.patch(2,  0x233A, ASM("ld hl, $FFF3\nld [hl], $04"), b"", fill_nop=True) # Remove health beep

        # Never allow stealing (always acts as if you do not have a sword)
        #rom.patch(4, 0x36F9, "FA4EDB", "3E0000")
        # Always allow stealing (even without a sword)
        rom.patch(4, 0x36F9, "FA4EDB", "3E0100")

        # Into text from Marin. Got to go fast, so less text. (This intro text is very long)
        rom.texts[0x01] = utils.formatText(b"Let's a go!")

        # Reduce length of a bunch of common texts
        rom.texts[0xEA] = utils.formatText(b"You've got a Guardian Acorn!")
        rom.texts[0xEB] = rom.texts[0xEA]
        rom.texts[0xEC] = rom.texts[0xEA]
        rom.texts[0x08] = utils.formatText(b"You got a Piece of Power!")
        rom.texts[0xEF] = utils.formatText(b"You found a Secret Seashell!")
        rom.texts[0xA7] = utils.formatText(b"You've got the Compass!")

        if args.seed is not None and args.seed.upper() == "DEFAULT":
            seed = "DEFAULT"
            for ii in locations.itemInfo.ItemInfo.all:
                ii.item = ii.read(rom)
                ii.patch(rom, ii.item)
            e = explorer.Explorer()
            e.visit(logic.start)
            e.dump()
            #from locations import Chest
            #Chest(0x113).patch(rom, "SWORD")
            #from locations import DroppedKey
            #dk = DroppedKey(0x116)
            #dk.patch(rom, "SWORD")
            #from locations import StartItem
            #StartItem().patch(rom, "POWER_BRACELET")
        else:
            if args.seed:
                args.seed = binascii.unhexlify(args.seed)
            retry_count = 0
            while True:
                try:
                    seed = randomizer.Randomizer(rom, seed=args.seed).seed
                    seed = binascii.hexlify(seed).decode("ascii").upper()
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
        patches.titleScreen.setRomInfo(rom, seed[16:], seed[:16])

        if args.output_filename:
            filename = args.output_filename
            if generation_number > 0:
                filename = "%s.%d%s" % (os.path.splitext(filename)[0], generation_number, os.path.splitext(filename)[1])
            rom.save(filename, name=seed)
        else:
            rom.save("lozlar_%s.gbc" % (seed), name=seed)

    if args.count > 1:
        total_time = time.monotonic() - start_time
        print("Generated: %d roms" % (args.count))
        print("Success ratio: %g%%" % (args.count / (args.count + total_retries) * 100))
        print("Total time: %gsec (Per generation: %gsec)" % (total_time, total_time / (args.count + total_retries)))
