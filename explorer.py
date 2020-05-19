from logic import AND, OR, COUNT
import locations.location

class Explorer:
    def __init__(self):
        self.__inventory = {}
        self.__visited = set()

    def getAvailableLocations(self):
        return self.__visited

    def visit(self, location):
        self._visit(location)
        while self._process():
            pass

    def _visit(self, location):
        assert location not in self.__visited
        self.__visited.add(location)
        for ii in location.items:
            #print(ii, ii.item)
            self.addItem(ii.item)

    def _process(self):
        while self.__simpleExpand():
            pass

        options = []
        for loc in self.__visited:
            for target, req in loc.connections.items():
                if target not in self.__visited and self.testConsumableRequirements(req):
                    options.append((target, req))

        if len(options) > 0:
            # TODO: Test all possible variations
            assert self.consumeRequirements(options[0][1])
            self._visit(options[0][0])
            return True
        return False

    def __simpleExpand(self):
        for loc in self.__visited:
            for target, req in loc.connections.items():
                if target not in self.__visited and self.testSimpleRequirements(req):
                    self._visit(target)
                    return True
        return False

    def addItem(self, item):
        if item is None:
            return
        if item.startswith("RUPEES_"):
            self.__inventory["RUPEES"] = self.__inventory.get("RUPEES", 0) + int(item[7:])
        else:
            self.__inventory[item] = self.__inventory.get(item, 0) + 1

    def consumeItem(self, item):
        if item not in self.__inventory:
            return False
        if self.isConsumable(item):
            self.__inventory[item] -= 1
            if self.__inventory[item] <= 0:
                del self.__inventory[item]
        return True

    def testSimpleRequirements(self, req):
        for r in req:
            if self._processRequirement(r, lambda n: not self.isConsumable(n) and n in self.__inventory):
                return True
        return False

    def testConsumableRequirements(self, req):
        for r in req:
            if self._processRequirement(r, lambda n: n in self.__inventory):
                return True
        return False

    def consumeRequirements(self, req):
        for r in req:
            if self._processRequirement(r, self.consumeItem):
                return True
        return False

    def _processRequirement(self, req, func):
        if isinstance(req, str):
            return func(req)
        elif isinstance(req, AND):
            if all(map(lambda r: self._processRequirement(r, func), req)):
                return True
        elif isinstance(req, OR):
            if any(map(lambda r: self._processRequirement(r, func), req)):
                return True
        elif isinstance(req, COUNT):
            return self.__inventory.get(req.item, 0) >= req.amount
        else:
            raise RuntimeError("Unknown connection requirement: %s" % (req, ))
        return False

    def isConsumable(self, item):
        if item.startswith("RUPEES_"):
            return True
        if item.startswith("KEY") and len(item) == 4:
            return True
        return False

    def dump(self):
        failed = 0
        for loc in locations.location.Location.all:
            if loc not in self.__visited:
                failed += 1
                print(loc, hex(loc.items[0].addr - 0x560))
        for loc in self.__visited:
            for target, req in loc.connections.items():
                if target not in self.__visited:
                    print("Missing:", req)
        print(self.__inventory)
        print("Cannot reach: %d locations" % (failed))
