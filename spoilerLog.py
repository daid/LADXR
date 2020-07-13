import json
import logic
import explorer
import patches.dungeonEntrances
import patches.titleScreen

class RaceRomException(Exception):
    pass

class SpoilerItemInfo():
    def __init__(self, ii, rom):
        self.id = ii.nameId
        self.area = ii.metadata.area
        self.locationName = ii.metadata.name
        self.itemName = str(ii.read(rom))
    
    def __repr__(self):
        return "%20s at %s - %s" % (self.itemName, self.area, self.locationName)

class SpoilerLog():
    def __init__(self, args, rom):
        if rom.banks[0][7] == 0x01:
            raise RaceRomException()

        self.seed = patches.titleScreen.readSeed(rom)
        self.testOnly = args.test
        self.accessibleItems = []
        self.inaccessibleItems = None
        self.dungeonOrder = patches.dungeonEntrances.readEntrances(rom)
        self.outputFormat = args.spoilerformat

        # Assume the broadest settings if we're dumping a seed we didn't just create
        if args.dump:
            args.witch = True
            args.boomerang = "gift"
            args.heartpiece = True
            args.seashells = True
            args.heartcontainers = True
            args.owlstatues = "both"

        my_logic = logic.Logic(args, None, entranceMapping=self.dungeonOrder)

        for ii in my_logic.iteminfo_list:
            ii.item = ii.read(rom)

        e = explorer.Explorer()
        e.visit(my_logic.start)

        for location in e.getAccessableLocations():
            for ii in location.items:
                self.accessibleItems.append(SpoilerItemInfo(ii, rom))

        if len(e.getAccessableLocations()) != len(my_logic.location_list):
            self.inaccessibleItems = []
            for loc in my_logic.location_list:
                if loc not in e.getAccessableLocations():
                    for ii in loc.items:
                        self.inaccessibleItems.append(SpoilerItemInfo(ii, rom))
    
    def output(self, filename=None):
        if self.outputFormat == "text":
            self.outputTextFile(filename)
        elif self.outputFormat == "json":
            self.outputJson(filename)
        elif self.outputFormat == "console":
            print(self)

    def outputTextFile(self, filename=None):
        if not filename:
            filename = "LADXR_%s.txt" % self.seed

        with open(filename, 'w') as logFile:
            logFile.write(str(self))
        
        print("Saved: %s" % filename)
    
    def outputJson(self, filename=None):
        if not filename:
            filename = "LADXR_%s.json" % self.seed

        with open(filename, 'w') as logFile:
            logFile.write(json.dumps(self, default=lambda x: x.__dict__))

        print("Saved: %s" % filename)

    def __repr__(self):
        if not self.testOnly:
            lines = ["Dungeon order:" + ", ".join(map(lambda n: "D%d:%d" % (n[0] + 1, n[1] + 1), enumerate(self.dungeonOrder)))]
            lines += [str(x) for x in sorted(self.accessibleItems, key=lambda x: (x.area, x.locationName))]

        if self.inaccessibleItems:
            lines.append("Logic failure! Cannot access all locations.")
            lines.append("Failed to find:")
            lines += [str(x) for x in sorted(self.inaccessibleItems, key=lambda x: (x.area, x.locationName))]
        else:
            lines.append("Success!  All locations can be accessed.")
        
        return '\n'.join(lines)
