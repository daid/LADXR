import json
import logic
import explorer
import patches.witch
import patches.dungeonEntrances

class RaceRomException(Exception):
    pass

class SpoilerItemInfo():
    def __init__(self, ii, rom, multiworld):
        self.id = ii.nameId
        self.area = ii.metadata.area
        self.locationName = ii.metadata.name
        self.itemName = str(ii.read(rom))
        self.player = None

        if multiworld:
            self.player = rom.banks[0x3E][0x3300 + ii.room] + 1
    
    def __repr__(self):
        itemName = self.itemName

        if self.player:
            itemName = "P%s's %s" % (self.player, itemName)

        return "%25s at %s - %s" % (itemName, self.area, self.locationName) 

class SpoilerLog():
    def __init__(self, args, rom):
        if rom.banks[0][7] == 0x01:
            raise RaceRomException()

        self.seed = rom.readHexSeed()
        self.testOnly = args.test
        self.accessibleItems = []
        self.inaccessibleItems = None
        self.dungeonOrder = patches.dungeonEntrances.readEntrances(rom)
        self.outputFormat = args.spoilerformat

        # Assume the broadest settings if we're dumping a seed we didn't just create
        if args.dump:
            # The witch flag causes trouble if we blindly turn it on
            if patches.witch.witchIsPatched(rom):
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
                self.accessibleItems.append(SpoilerItemInfo(ii, rom, args.multiworld))

        if len(e.getAccessableLocations()) != len(my_logic.location_list):
            self.inaccessibleItems = []
            for loc in my_logic.location_list:
                if loc not in e.getAccessableLocations():
                    for ii in loc.items:
                        self.inaccessibleItems.append(SpoilerItemInfo(ii, rom, args.multiworld))
    
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