import sys
import json
import logic.main
import explorer
import patches.witch
from settings import Settings
import worldSetup


class RaceRomException(Exception):
    pass


class SpoilerItemInfo:
    def __init__(self, ii, rom):
        self.id = ii.nameId
        self.area = ii.metadata.area
        self.locationName = ii.metadata.name
        self.sphere = ii.sphere if hasattr(ii, "sphere") else None
        self.itemName = str(ii.read(rom))

    def __repr__(self):
        itemName = self.itemName

        result = "%25s at %s - %s" % (itemName, self.area, self.locationName)

        if self.sphere is not None:
            result += " (Sphere %d)" % self.sphere

        return result


class SpoilerLog:
    def __init__(self, settings, args, rom):
        if rom.banks[0][7] == 0x01:
            raise RaceRomException()

        if args.dump or not settings:
            shortSettings = rom.readShortSettings()
            settings = Settings()
            settings.loadShortString(shortSettings)

        self.seed = rom.readHexSeed()
        self.testOnly = args.test
        self.accessibleItems = []
        self.inaccessibleItems = None
        self.outputFormat = args.spoilerformat
        self.settings = settings

        world_setup = worldSetup.WorldSetup()
        world_setup.loadFromRom(rom)

        self.logic = logic.main.Logic(self.settings, world_setup=world_setup)

        self._loadItems(self.settings, rom)

    def _loadItems(self, settings, rom):
        remainingItems = set(self.logic.iteminfo_list)

        currentSphere = 0
        lastAccessibleLocations = set()
        itemContents = {}
        for ii in self.logic.iteminfo_list:
            itemContents[ii] = ii.read(rom)

        # Feed the logic items one sphere at a time
        while remainingItems:
            e = explorer.Explorer()
            e.visit(self.logic.start)

            newLocations = e.getAccessableLocations() - lastAccessibleLocations

            if not newLocations:
                # Some locations must be inaccessible, stop counting spheres
                break

            for location in newLocations:
                for ii in location.items:
                    ii.sphere = currentSphere
                    ii.item = itemContents[ii]
                    if ii in remainingItems:
                        remainingItems.remove(ii)
            
            lastAccessibleLocations = e.getAccessableLocations()
            currentSphere += 1

        for ii in remainingItems:
            ii.item = itemContents[ii]

        for location in e.getAccessableLocations():
            for ii in location.items:
                self.accessibleItems.append(SpoilerItemInfo(ii, rom))

        if len(e.getAccessableLocations()) != len(self.logic.location_list):
            self.inaccessibleItems = []
            for loc in self.logic.location_list:
                if loc not in e.getAccessableLocations():
                    for ii in loc.items:
                        self.inaccessibleItems.append(SpoilerItemInfo(ii, rom))

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

        jsonContent = json.dumps({
            "accessibleItems": [item.__dict__ for item in self.accessibleItems],
            "inaccessibleItems": [item.__dict__ for item in self.inaccessibleItems or []],
            "options": {s.key: s.value for s in self.settings},
            "entrances":
                {entrance: target for entrance, target in self.logic.world_setup.entrance_mapping.items() if f"{entrance}:inside" != target and entrance != f"{target}:inside"}
                if isinstance(self.logic, logic.main.Logic) else [
                    {entrance: target for entrance, target in world.world_setup.entrance_mapping.items() if f"{entrance}:inside" != target and entrance != f"{target}:inside"} for world in self.logic.worlds
                ],
            "seed": self.seed
        }, indent="  ")

        if zipFile:
            zipFile.writestr(filename, jsonContent)
        else:
            with open(filename, 'w') as logFile:
                logFile.write(jsonContent)

        print("Saved: %s" % filename)

    def __repr__(self):
        lines = []
        if not self.testOnly:
            if isinstance(self.logic, logic.main.Logic):
                for entrance, target in sorted(self.logic.world_setup.entrance_mapping.items()):
                    if f"{entrance}:inside" != target and entrance != f"{target}:inside":
                        lines.append("Entrance: %s -> %s" % (entrance, target))
            lines += [str(x) for x in sorted(self.accessibleItems, key=lambda x: (x.sphere if x.sphere is not None else sys.maxsize, x.area, x.locationName))]

        if self.inaccessibleItems:
            lines.append("Logic failure! Cannot access all locations.")
            lines.append("Failed to find:")
            lines += [str(x) for x in sorted(self.inaccessibleItems, key=lambda x: (x.sphere if x.sphere is not None else sys.maxsize, x.area, x.locationName))]
        else:
            lines.append("Success!  All locations can be accessed.")
        
        return '\n'.join(lines)
