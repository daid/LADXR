import binascii
from romTables import ROMWithTables
import shlex
import randomizer
import logic
import patches.dungeonEntrances
import explorer


def main(mainargs=None):
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Randomize!')
    parser.add_argument('input_filename', metavar='input rom', type=str,
        help="Rom file to use as input.")
    parser.add_argument('-o', '--output', dest="output_filename", metavar='output rom', type=str, required=False,
        help="Output filename to use. If not specified [seed].gbc is used.")
    parser.add_argument('--dump', dest="dump", action="store_true",
        help="Dump the logic if the given rom (spoilers!)")
    parser.add_argument('--test', dest="test", action="store_true",
        help="Test the logic if the given rom, without showing anything.")
    parser.add_argument('-s', '--seed', dest="seed", type=str, required=False,
        help="Generate the specified seed")
    parser.add_argument('--romdebugmode', dest="romdebugmode", action="store_true",
        help="Patch the rom so that debug mode is enabled, this creates a default save with most items and unlocks some debug features.")
    parser.add_argument('--exportmap', dest="exportmap", action="store_true",
        help="Export the map (many graphical mistakes)")
    parser.add_argument('--emptyplan', dest="emptyplan", type=str, required=False,
        help="Write an unfilled plan file")

    # Flags that effect gameplay
    parser.add_argument('--plan', dest="plan", metavar='plandomizer', type=str, required=False,
        help="Read an item placement plan")
    parser.add_argument('--race', dest="race", action="store_true",
        help="Enable race mode. This generates a rom from which the spoiler log cannot be dumped and the seed cannot be extracted.")
    parser.add_argument('--logic', dest="logic", choices=["normal", "hard", "glitched", "hell"],
        help="Which level of logic is required.")
    parser.add_argument('--multiworld', dest="multiworld", type=int, required=False,
        help="Generates multiple roms for a multiworld setup.")
    parser.add_argument('--multiworld-config', dest="multiworld_config", action="append", required=False,
        help="Set configuration for a multiworld player, supply multiple times for settings per player")
    parser.add_argument('--forwardfactor', dest="forwardfactor", type=float, required=False,
        help="Forward item weight adjustment factor, lower values generate more rear heavy seeds while higher values generate front heavy seeds. Default is 0.5.")
    parser.add_argument('--heartpiece', dest="heartpiece", action="store_true",
        help="Enables randomization of heart pieces.")
    parser.add_argument('--seashells', dest="seashells", action="store_true",
        help="Enables seashells mode, which randomizes the secret sea shells hiding in the ground/trees. (chest are always randomized)")
    parser.add_argument('--heartcontainers', dest="heartcontainers", action="store_true",
        help="Enables heartcontainer mode, which randomizes the heart containers dropped by bosses.")
    parser.add_argument('--owlstatues', dest="owlstatues", choices=['none', 'dungeon', 'overworld', 'both'],
        help="Give the owl statues in dungeons or on the overworld items as well, instead of showing the normal hints")
    parser.add_argument('--keysanity', dest="keysanity", action="store_true",
        help="Enables keysanity mode, which shuffles all dungeon items outside dungeons as well.")
    parser.add_argument('--dungeonshuffle', dest="dungeonshuffle", action="store_true",
        help="Enable dungeon shuffle, puts dungeons on different spots.")
    parser.add_argument('--witch', dest="witch", action="store_true",
        help="Enables witch and toadstool in the item pool.")
    parser.add_argument('--hpmode', dest="hpmode", choices=['default', 'inverted', '1'], default='default',
        help="Set the HP gamplay mode. Inverted causes health containers to take HP instead of give it and you start with more health. 1 sets your starting health to just 1 hearth.")
    parser.add_argument('--boomerang', dest="boomerang", choices=['default', 'trade', 'gift'], default='default',
        help="Put the boomerang and the trade with the boomerang in the item pool")
    parser.add_argument('--steal', dest="steal", choices=['never', 'always', 'default'], default='always',
        help="Configure when to allow stealing from the shop.")
    parser.add_argument('--goal', dest="goal", choices=['-1', '0', '1', '2', '3', '4', '5', '6', '7', '8', 'random', 'raft'],
        help="Configure the instrument goal for this rom, anything between 0 and 8.")
    parser.add_argument('--bowwow', dest="bowwow", choices=['normal', 'always', 'swordless'], default='normal',
        help="Enables 'good boy mode', where BowWow is allowed on all screens and can damage bosses and more enemies.")
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
        help="Slows or disables the low health beeping sound")
    parser.add_argument('--linkspalette', dest="linkspalette", type=int, default=None,
        help="Force the palette of link")

    args = parser.parse_args(mainargs)
    if args.multiworld is not None:
        args.multiworld_options = [args] * args.multiworld
        if args.multiworld_config is not None:
            for index, settings_string in enumerate(args.multiworld_config):
                args.multiworld_options[index] = parser.parse_args([args.input_filename] + shlex.split(settings_string))

    if args.exportmap:
        import mapexport
        print("Loading: %s" % (args.input_filename))
        rom = ROMWithTables(args.input_filename)
        mapexport.MapExport(rom)
        sys.exit(0)

    if args.emptyplan:
        import checkMetadata
        import locations.items
        f = open(args.emptyplan, "wt")
        f.write(";Plandomizer data\n;Items: %s\n" % (", ".join(map(lambda n: getattr(locations.items, n), filter(lambda n: not n.startswith("__"), dir(locations.items))))))
        for key in dir(locations.items):
            f.write("")
        for name, data in sorted(checkMetadata.checkMetadataTable.items(), key=lambda n: str(n[1])):
            if name is not "None":
                f.write(";%s\n" % (data))
                f.write("%s: \n" % (name))
        sys.exit(0)

    if args.dump or args.test:
        print("Loading: %s" % (args.input_filename))
        rom = ROMWithTables(args.input_filename)
        if rom.banks[0][7] == 0x01:
            print("Cannot read spoiler log for race rom")
            sys.exit(1)
        dungeon_order = patches.dungeonEntrances.readEntrances(rom)
        print("Dungeon order:", ", ".join(map(lambda n: "D%d:%d" % (n[0] + 1, n[1] + 1), enumerate(dungeon_order))))
        my_logic = logic.Logic(args, None, entranceMapping=dungeon_order)
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
                        print("%20s at %s (%s)" % (ii.read(rom), ii.metadata, ii))
                        if ii.MULTIWORLD:
                            if rom.banks[0x00][0x0055] != rom.banks[0x3E][0x3300 + ii.room]:
                                print("  for player %d" % (rom.banks[0x3E][0x3300 + ii.room] + 1))
            sys.exit(1)
        sys.exit(0)

    if args.seed:
        try:
            args.seed = binascii.unhexlify(args.seed)
        except binascii.Error:
            args.seed = args.seed.encode("ascii")

    retry_count = 0
    while True:
        try:
            r = randomizer.Randomizer(args, seed=args.seed)
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

    print("Seed: %s" % (seed))


if __name__ == "__main__":
    main()
