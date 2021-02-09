import binascii
from romTables import ROMWithTables
import shlex
import randomizer
import logic
import patches.dungeonEntrances
import explorer
import spoilerLog


def main(mainargs=None):
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Randomize!')
    parser.add_argument('input_filename', metavar='input rom', type=str,
        help="Rom file to use as input.")
    parser.add_argument('-o', '--output', dest="output_filename", metavar='output rom', type=str, required=False,
        help="Output filename to use. If not specified [seed].gbc is used.")
    parser.add_argument('--dump', dest="dump", action="store_true",
        help="Dump the logic of the given rom (spoilers!)")
    parser.add_argument('--spoilerformat', dest="spoilerformat", choices=["none", "console", "text", "json"], default="none",
        help="Sets the output format for the generated seed's spoiler log")
    parser.add_argument('--spoilerfilename', dest="spoiler_filename", type=str, required=False,
        help="Output filename to use for the spoiler log.  If not specified, LADXR_[seed].txt/json is used.")
    parser.add_argument('--test', dest="test", action="store_true",
        help="Test the logic of the given rom, without showing anything.")
    parser.add_argument('-s', '--seed', dest="seed", type=str, required=False,
        help="Generate the specified seed")
    parser.add_argument('--romdebugmode', dest="romdebugmode", action="store_true",
        help="Patch the rom so that debug mode is enabled, this creates a default save with most items and unlocks some debug features.")
    parser.add_argument('--exportmap', dest="exportmap", action="store_true",
        help="Export the map (many graphical mistakes)")
    parser.add_argument('--emptyplan', dest="emptyplan", type=str, required=False,
        help="Write an unfilled plan file")
    parser.add_argument('--timeout', type=float, required=False,
        help="Timeout generating the seed after the specified number of seconds")

    # Flags that effect gameplay
    parser.add_argument('--plan', dest="plan", metavar='plandomizer', type=str, required=False,
        help="Read an item placement plan")
    parser.add_argument('--race', dest="race", nargs="?", default=False, const=True,
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
    parser.add_argument('--instruments', dest="instruments", action="store_true",
        help="Shuffle the instruments in the item pool.")
    parser.add_argument('--owlstatues', dest="owlstatues", choices=['none', 'dungeon', 'overworld', 'both'], default='none',
        help="Give the owl statues in dungeons or on the overworld items as well, instead of showing the normal hints")
    parser.add_argument('--keysanity', dest="keysanity", action="store_true",
        help="Enables keysanity mode, which shuffles all dungeon items outside dungeons as well.")
    parser.add_argument('--randomstartlocation', dest="randomstartlocation", action="store_true",
        help="Place your starting house at a random location.")
    parser.add_argument('--dungeonshuffle', dest="dungeonshuffle", action="store_true",
        help="Enable dungeon shuffle, puts dungeons on different spots.")
    parser.add_argument('--boss', dest="boss", choices=["default", "shuffle", "random"], default="default",
        help="Enable boss shuffle, swaps around dungeon bosses.")
    parser.add_argument('--miniboss', dest="miniboss", choices=["default", "shuffle", "random"], default="default",
        help="Shuffle the minibosses or just randomize them.")
    parser.add_argument('--witch', dest="witch", action="store_true",
        help="Enables witch and toadstool in the item pool.")
    parser.add_argument('--hpmode', dest="hpmode", choices=['default', 'inverted', '1'], default='default',
        help="Set the HP gamplay mode. Inverted causes health containers to take HP instead of give it and you start with more health. 1 sets your starting health to just 1 hearth.")
    parser.add_argument('--boomerang', dest="boomerang", choices=['default', 'trade', 'gift'], default='default',
        help="Put the boomerang and the trade with the boomerang in the item pool")
    parser.add_argument('--steal', dest="steal", choices=['never', 'always', 'default'], default='always',
        help="Configure when to allow stealing from the shop.")
    parser.add_argument('--hard-mode', dest="hardMode", action="store_true",
        help="Make the game a bit harder, less health from drops, bombs damage yourself, and less iframes.")
    parser.add_argument('--goal', dest="goal", choices=['-1', '0', '1', '2', '3', '4', '5', '6', '7', '8', 'random', 'raft', 'seashells'], default='8',
        help="Configure the instrument goal for this rom, anything between 0 and 8.")
    parser.add_argument('--accessibility', dest="accessibility_rule", choices=['all', 'goal'],
        help="Switches between making sure all locations are reachable or only the goal is reachable")
    parser.add_argument('--bowwow', dest="bowwow", choices=['normal', 'always', 'swordless'], default='normal',
        help="Enables 'good boy mode', where BowWow is allowed on all screens and can damage bosses and more enemies.")
    parser.add_argument('--pool', dest="itempool", choices=['normal', 'casual', 'pain', 'keyup'], default='normal',
        help="Sets up different item pools, for easier or harder gameplay.")
    parser.add_argument('--overworld', dest="overworld", choices=['normal', 'dungeondive'], default='normal')

    # Just aestetic flags
    parser.add_argument('--gfxmod', dest="gfxmod", action='append',
        help="Load graphical mods.")
    parser.add_argument('--quickswap', dest="quickswap", choices=['none', 'a', 'b'], default='none',
        help="Configure quickswap for A or B button (select key swaps, no longer opens map)")
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

    if args.timeout is not None:
        import threading
        import time
        import os
        def timeoutFunction():
            time.sleep(args.timeout)
            print("TIMEOUT")
            sys.stdout.flush()
            os._exit(1)
        threading.Thread(target=timeoutFunction, daemon=True).start()

    if args.exportmap:
        import mapexport
        print("Loading: %s" % (args.input_filename))
        rom = ROMWithTables(args.input_filename)
        mapexport.MapExport(rom)
        sys.exit(0)

    if args.emptyplan:
        import locations.items
        import logic
        f = open(args.emptyplan, "wt")
        f.write(";Plandomizer data\n;Items: %s\n" % (", ".join(map(lambda n: getattr(locations.items, n), filter(lambda n: not n.startswith("__"), dir(locations.items))))))
        f.write(";Modify the item pool:\n")
        f.write(";Pool:SWORD:+5\n")
        f.write(";Pool:RUPEES_50:-5\n")
        iteminfo_list = logic.Logic(args, start_house_index=0, entranceMapping=list(range(9)), bossMapping=list(range(9))).iteminfo_list
        for ii in sorted(iteminfo_list, key=lambda n: (n.location.dungeon if n.location.dungeon else -1, repr(n.metadata))):
            if len(ii.OPTIONS) > 1:
                f.write(";%r\n" % (ii.metadata))
                f.write("Location:%s: \n" % (ii.nameId))
        sys.exit(0)

    if args.dump or args.test:
        print("Loading: %s" % (args.input_filename))
        rom = ROMWithTables(args.input_filename)

        if args.spoilerformat == "none":
            args.spoilerformat = "console"

        try:
            log = spoilerLog.SpoilerLog(args, rom)
            log.output(args.spoiler_filename)
            sys.exit(0)
        except spoilerLog.RaceRomException:
            print("Cannot read spoiler log for race rom")
            sys.exit(1)

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
