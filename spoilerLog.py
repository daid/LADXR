import sys
import json
import logic
import explorer
import patches.witch
from worldSetup import WorldSetup


class RaceRomException(Exception):
    pass


class SpoilerItemInfo:
    def __init__(self, ii, rom, multiworld):
        self.id = ii.nameId
        self.area = ii.metadata.area
        self.locationName = ii.metadata.name
        self.sphere = ii.metadata.sphere
        self.itemName = str(ii.read(rom))
        self.player = None

        if multiworld and ii.room is not None:
            if ii.MULTIWORLD:
                self.player = rom.banks[0x3E][0x3300 + ii.room] + 1
            else:
                self.player = rom.banks[0x00][0x0055] + 1
    
    def __repr__(self):
        itemName = self.itemName

        if self.player:
            itemName = "P%s's %s" % (self.player, itemName)

        result = "%25s at %s - %s" % (itemName, self.area, self.locationName)

        if self.sphere is not None:
            result += " (Sphere %d)" % self.sphere

        return result


class SpoilerLog:
    def __init__(self, args, roms):
        for rom in roms:
            if rom.banks[0][7] == 0x01:
                raise RaceRomException()

        self.seed = roms[0].readHexSeed()
        self.testOnly = args.test
        self.accessibleItems = []
        self.inaccessibleItems = None
        self.outputFormat = args.spoilerformat
        self.args = vars(args)

        # Assume the broadest settings if we're dumping a seed we didn't just create
        if args.dump:
            # The witch flag causes trouble if we blindly turn it on
            if patches.witch.witchIsPatched(roms[0]):
                args.witch = True

            args.boomerang = "gift"
            args.heartpiece = True
            args.seashells = True
            args.heartcontainers = True
            args.owlstatues = "both"

            if len(roms) > 1:
                args.multiworld = len(roms)
                if not hasattr(args, "multiworld_options"):
                    args.multiworld_options = [args] * args.multiworld

        world_setups = []
        for rom in roms:
            world_setup = WorldSetup()
            world_setup.loadFromRom(rom)
            world_setups.append(world_setup)

        if len(world_setups) == 1:
            my_logic = logic.Logic(args, world_setup=world_setups[0])
            self.world_setup = my_logic.world_setup
        else:
            my_logic = logic.MultiworldLogic(args, world_setups=world_setups)
            self.worlds = my_logic.worlds

        self._loadItems(args, my_logic, roms)
    
    def _loadItems(self, args, my_logic, roms):
        remainingItems = set(my_logic.iteminfo_list)

        currentSphere = 0
        lastAccessibleLocations = set()
        itemContents = {}
        for ii in my_logic.iteminfo_list:
            if not hasattr(ii, "world"):
                ii.world = 0
            itemContents[ii] = ii.read(roms[ii.world])

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
                    if ii in remainingItems:
                        remainingItems.remove(ii)
            
            lastAccessibleLocations = e.getAccessableLocations()
            currentSphere += 1

        for ii in remainingItems:
            ii.item = itemContents[ii]

        for location in e.getAccessableLocations():
            for ii in location.items:
                self.accessibleItems.append(SpoilerItemInfo(ii, roms[ii.world], args.multiworld))

        if len(e.getAccessableLocations()) != len(my_logic.location_list):
            self.inaccessibleItems = []
            for loc in my_logic.location_list:
                if loc not in e.getAccessableLocations():
                    for ii in loc.items:
                        self.inaccessibleItems.append(SpoilerItemInfo(ii, roms[ii.world], args.multiworld))

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

        jsonContent = json.dumps(self, default=lambda x: x.__dict__, indent="  ")

        if zipFile:
            zipFile.writestr(filename, jsonContent)
        else:
            with open(filename, 'w') as logFile:
                logFile.write(jsonContent)

        print("Saved: %s" % filename)

    def __repr__(self):
        lines = []
        if not self.testOnly:
            # use self.world_setup and self.worlds to distinguish normal vs multiworld
            # cannot use a logic.Logic reference directly to avoid circular dependency
            if self.world_setup is not None:
                for entrance, target in sorted(self.world_setup.entrance_mapping.items()):
                    if entrance != target:
                        lines.append("Entrance: %s -> %s" % (entrance, target))
            elif self.worlds is not None:
                for index, world in enumerate(self.worlds):
                    for entrance, target in sorted(world.world_setup.entrance_mapping.items()):
                        if entrance != target:
                            lines.append("P%d Entrance: %s -> %s" % (index + 1, entrance, target))
            lines += [str(x) for x in sorted(self.accessibleItems, key=lambda x: (x.sphere if x.sphere is not None else sys.maxsize, x.area, x.locationName))]

        if self.inaccessibleItems:
            lines.append("Logic failure! Cannot access all locations.")
            lines.append("Failed to find:")
            lines += [str(x) for x in sorted(self.inaccessibleItems, key=lambda x: (x.sphere if x.sphere is not None else sys.maxsize, x.area, x.locationName))]
        else:
            lines.append("Success!  All locations can be accessed.")
        
        return '\n'.join(lines)
