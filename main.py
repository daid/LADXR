import binascii
from romTables import ROMWithTables
import json
import randomizer
import logic.main
import spoilerLog
import argparse
from settings import Settings
from typing import Optional, List



def main(mainargs: Optional[List[str]] = None) -> None:
    import sys

    parser = argparse.ArgumentParser(description='Randomize!')
    parser.add_argument('input_filename', metavar='input rom', type=str,
        help="Rom file to use as input.")
    parser.add_argument('-o', '--output', dest="output_filename", metavar='output rom', type=str, required=False,
        help="Output filename to use. If not specified [seed].gbc is used.")
    parser.add_argument('--dump', dest="dump", type=str, nargs="*",
        help="Dump the logic of the given rom (spoilers!)")
    parser.add_argument('--spoilerformat', dest="spoilerformat", choices=["none", "console", "text", "json"], default="none",
       help="Sets the output format for the generated seed's spoiler log")
    parser.add_argument('--spoilerfilename', dest="spoiler_filename", type=str, required=False,
        help="Output filename to use for the spoiler log.  If not specified, LADXR_[seed].txt/json is used.")
    parser.add_argument('--test', dest="test", action="store_true",
        help="Test the logic of the given rom, without showing anything.")
    parser.add_argument('--romdebugmode', dest="romdebugmode", action="store_true",
        help="Patch the rom so that debug mode is enabled, this creates a default save with most items and unlocks some debug features.")
    parser.add_argument('--exportmap', dest="exportmap", action="store_true",
        help="Export the map (many graphical mistakes)")
    parser.add_argument('--emptyplan', dest="emptyplan", type=str, required=False,
        help="Write an unfilled plan file")
    parser.add_argument('--timeout', type=float, required=False,
        help="Timeout generating the seed after the specified number of seconds")
    parser.add_argument('--logdirectory', dest="log_directory", type=str, required=False,
        help="Directory to write the JSON log file. Generated independently from the spoiler log and omitted by default.")

    parser.add_argument('-s', '--setting', dest="settings", action="append", required=False,
        help="Set a configuration setting for rom generation")
    parser.add_argument('--short', dest="shortsettings", type=str, required=False,
        help="Set a configuration setting for rom generation")
    parser.add_argument('--settingjson', dest="settingjson", action="store_true",
        help="Dump a json blob which describes all settings")

    parser.add_argument('--plan', dest="plan", metavar='plandomizer', type=str, required=False,
        help="Read an item placement plan")
    parser.add_argument('--multiworld', dest="multiworld", action="append", required=False,
        help="Set configuration for a multiworld player, supply multiple times for settings per player, requires a short setting string per player.")
    parser.add_argument('--doubletrouble', dest="doubletrouble", action="store_true",
        help="Warning, bugged in various ways")
    parser.add_argument('--pymod', dest="pymod", action='append',
        help="Load python code mods.")

    settings = Settings()
    args = parser.parse_args(mainargs)
    if args.settingjson:
        print("var options =")
        print(json.dumps(settings.toJson(), indent=1))
        return
    if args.shortsettings is not None:
        settings.loadShortString(args.shortsettings)
    if args.settings:
        for s in args.settings:
            settings.set(s)
    if args.multiworld is not None:
        for s in args.multiworld:
            player_settings = Settings(len(args.multiworld))
            player_settings.loadShortString(s)
            settings.multiworld_settings.append(player_settings)

    settings.validate()
    print(f"Short settings string: {settings.getShortString()}")

    if args.timeout is not None:
        import threading
        import time
        import os
        def timeoutFunction() -> None:
            time.sleep(args.timeout)
            print("TIMEOUT")
            sys.stdout.flush()
            os._exit(1)
        threading.Thread(target=timeoutFunction, daemon=True).start()

    if args.exportmap:
        import mapexport
        print(f"Loading: {args.input_filename}")
        rom = ROMWithTables(open(args.input_filename, 'rb'))
        mapexport.MapExport(rom).export_all()
        sys.exit(0)

    if args.emptyplan:
        import locations.items
        f = open(args.emptyplan, "wt")
        f.write(";Plandomizer data\n;Items: %s\n" % (", ".join(map(lambda n: getattr(locations.items, n), filter(lambda n: not n.startswith("__"), dir(locations.items))))))
        f.write(";Modify the item pool:\n")
        f.write(";Pool:SWORD:+5\n")
        f.write(";Pool:RUPEES_50:-5\n")
        import worldSetup
        ws = worldSetup.WorldSetup()
        ws.goal = settings.goal
        iteminfo_list = logic.main.Logic(settings, world_setup=ws).iteminfo_list
        for ii in sorted(iteminfo_list, key=lambda n: (n.location.dungeon if n.location.dungeon else -1, repr(n.metadata))):
            if len(ii.OPTIONS) > 1:
                f.write(";%r\n" % (ii.metadata))
                f.write("Location:%s: \n" % (ii.nameId))
        sys.exit(0)

    if args.dump is not None or args.test:
        print("Loading: %s" % (args.input_filename))
        roms = [ROMWithTables(open(f, 'rb')) for f in [args.input_filename] + args.dump]

        if args.spoilerformat == "none":
            args.spoilerformat = "console"

        try:
            log = spoilerLog.SpoilerLog(settings, args, roms)
            log.output(args.spoiler_filename)
            sys.exit(0)
        except spoilerLog.RaceRomException:
            print("Cannot read spoiler log for race rom")
            sys.exit(1)

    userSeed = None
    if settings.seed:
        try:
            userSeed = binascii.unhexlify(settings.seed)
        except binascii.Error:
            userSeed = settings.seed.encode("ascii")

    retry_count = 0
    while True:
        try:
            r = randomizer.Randomizer(args, settings, seed=userSeed)
            seed = binascii.hexlify(r.seed).decode("ascii").upper()
            break
        except randomizer.Error as e:
            if userSeed is not None:
                print("Specified seed does not produce a valid result.")
                sys.exit(1)
            retry_count += 1
            if retry_count > 100:
                print("Randomization keeps failing, abort!")
                sys.exit(1)
            print("Failed (%s), trying again: %d" % (e, retry_count))

    print("Seed: %s" % (seed))


if __name__ == "__main__":
    main()

