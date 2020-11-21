import sys
import json
import logic
import explorer
import patches.witch
import patches.startLocation
import patches.dungeonEntrances
import patches.enemies

class RaceRomException(Exception):
    pass

class SpoilerItemInfo():
    def __init__(self, ii, rom, multiworld):
        self.id = ii.nameId
        self.area = ii.metadata.area
        self.locationName = ii.metadata.name
        self.sphere = ii.metadata.sphere
        self.itemName = str(ii.read(rom))
        self.player = None

        if multiworld:
            self.player = rom.banks[0x3E][0x3300 + ii.room] + 1
    
    def __repr__(self):
        itemName = self.itemName

        if self.player:
            itemName = "P%s's %s" % (self.player, itemName)

        result = "%25s at %s - %s" % (itemName, self.area, self.locationName)

        if self.sphere != None:
            result += " (Sphere %d)" % self.sphere

        return result

class SpoilerLog():
    def __init__(self, args, rom):
        if rom.banks[0][7] == 0x01:
            raise RaceRomException()

        self.seed = rom.readHexSeed()
        self.testOnly = args.test
        self.accessibleItems = []
        self.inaccessibleItems = None
        self.start_house_index = patches.startLocation.readStartLocation(rom)
        self.dungeonOrder = patches.dungeonEntrances.readEntrances(rom)
        self.bossMapping = patches.enemies.readBossMapping(rom)
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

        self._loadItems(args, rom)
    
    def _loadItems(self, args, rom):
        my_logic = logic.Logic(args, start_house_index=self.start_house_index, entranceMapping=self.dungeonOrder, bossMapping=self.bossMapping)
        remainingItems = set(my_logic.iteminfo_list)

        currentSphere = 0
        lastAccessibleLocations = set()
        itemContents = {}
        for ii in my_logic.iteminfo_list:
            itemContents[ii] = ii.read(rom)

        # Feed the logic items one sphere at a time
        while remainingItems:
            e = explorer.Explorer()
            e.visit(my_logic.start)

            newLocations = e.getAccessableLocations() - lastAccessibleLocations

            if not newLocations:
                # Some locations must be inaccessible, stop counting spheres
                break

            for location in newLocations:
                for ii in location.items:
                    ii.metadata.sphere = currentSphere
                    ii.item = itemContents[ii]
                    remainingItems.remove(ii)
            
            lastAccessibleLocations = e.getAccessableLocations()
            currentSphere += 1

        for ii in remainingItems:
            ii.item = itemContents[ii]

        for location in e.getAccessableLocations():
            for ii in location.items:
                self.accessibleItems.append(SpoilerItemInfo(ii, rom, args.multiworld))

        if len(e.getAccessableLocations()) != len(my_logic.location_list):
            self.inaccessibleItems = []
            for loc in my_logic.location_list:
                if loc not in e.getAccessableLocations():
                    for ii in loc.items:
                        self.inaccessibleItems.append(SpoilerItemInfo(ii, rom, args.multiworld))

    def output(self, filename=None, zipFile=None):
        if self.outputFormat == "text":
            self.outputTextFile(filename, zipFile)
        elif self.outputFormat == "json":
            self.outputJson(filename, zipFile)
        elif self.outputFormat == "console":
            print(self)

    def outputTextFile(self, filename=None, zipFile=None):
        if not filename:
            filename = "LADXR_%s.txt" % self.seed

        if zipFile:
            zipFile.writestr(filename, str(self))
        else:
            with open(filename, 'w') as logFile:
                logFile.write(str(self))
        
        print("Saved: %s" % filename)
    
    def outputJson(self, filename=None, zipFile=None):
        if not filename:
            filename = "LADXR_%s.json" % self.seed

        jsonContent = json.dumps(self, default=lambda x: x.__dict__)

        if zipFile:
            zipFile.writestr(filename, jsonContent)
        else:
            with open(filename, 'w') as logFile:
                logFile.write(jsonContent)

        print("Saved: %s" % filename)

    def __repr__(self):
        if not self.testOnly:
            lines = ["Dungeon order:" + ", ".join(map(lambda n: "D%d:%d" % (n[0] + 1, n[1] + 1), enumerate(self.dungeonOrder)))]
            lines += [str(x) for x in sorted(self.accessibleItems, key=lambda x: (x.sphere if x.sphere != None else sys.maxsize, x.area, x.locationName))]

        if self.inaccessibleItems:
            lines.append("Logic failure! Cannot access all locations.")
            lines.append("Failed to find:")
            lines += [str(x) for x in sorted(self.inaccessibleItems, key=lambda x: (x.sphere if x.sphere != None else sys.maxsize, x.area, x.locationName))]
        else:
            lines.append("Success!  All locations can be accessed.")
        
        return '\n'.join(lines)
