from logic import AND, OR, COUNT
from logic.requirements import isConsumable


class Explorer:
    def __init__(self, *, verbose=False):
        self.__inventory = {}
        self.__visited = set()
        self.__todo_simple = []
        self.__todo_gated = []
        self.__verbose = verbose

    def getAccessableLocations(self):
        return self.__visited

    def getInventory(self):
        return self.__visited

    def visit(self, location):
        self._visit(location)
        while self._process():
            pass

    def _visit(self, location):
        assert location not in self.__visited
        self.__visited.add(location)
        for ii in location.items:
            if self.__verbose:
                print("%20s at %s" % (ii.item, ii))
            self.addItem(ii.item)

        for target, requirements in location.simple_connections:
            if target not in self.__visited:
                if self.testRequirements(requirements):
                    self._visit(target)
                else:
                    self.__todo_simple.append((target, requirements))
        for target, requirements in location.gated_connections:
            if target not in self.__visited:
                self.__todo_gated.append((target, requirements))

    def _process(self):
        while self.__simpleExpand():
            pass

        options = []
        self.__todo_gated = list(filter(lambda n: n[0] not in self.__visited, self.__todo_gated))
        for target, req in self.__todo_gated:
            if target not in self.__visited and self.testRequirements(req):
                options.append((target, req))

        if len(options) > 0:
            # TODO: Test all possible variations, as right now we just take the first option.
            #       this will most likely branch into many different paths.
            assert self.consumeRequirements(options[0][1])
            self._visit(options[0][0])
            return True
        return False

    def __simpleExpand(self):
        self.__todo_simple = list(filter(lambda n: n[0] not in self.__visited, self.__todo_simple))
        for target, req in self.__todo_simple:
            if target not in self.__visited and self.testRequirements(req):
                self._visit(target)
                return True
        return False

    def addItem(self, item):
        if item is None:
            return
        if item.startswith("RUPEES_"):
            self.__inventory["RUPEES"] = self.__inventory.get("RUPEES", 0) + int(item[7:])
        elif item.startswith("W0_RUPEES_"):
            self.__inventory["W0_RUPEES"] = self.__inventory.get("W0_RUPEES", 0) + int(item[10:])
        elif item.startswith("W1_RUPEES_"):
            self.__inventory["W1_RUPEES"] = self.__inventory.get("W1_RUPEES", 0) + int(item[10:])
        else:
            self.__inventory[item] = self.__inventory.get(item, 0) + 1

    def consumeItem(self, item):
        if item not in self.__inventory:
            return False
        if isConsumable(item):
            self.__inventory[item] -= 1
            if self.__inventory[item] <= 0:
                del self.__inventory[item]
        return True

    def testRequirements(self, req):
        if self._processRequirement(req, lambda n: n in self.__inventory):
            return True
        return False

    def consumeRequirements(self, req):
        if self._processRequirement(req, self.consumeItem):
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

    def dump(self, logic):
        failed = 0
        for loc in logic.location_list:
            if loc not in self.__visited:
                failed += 1
        for loc in self.__visited:
            for target, req in loc.simple_connections:
                if target not in self.__visited:
                    print("Missing:", req)
            for target, req in loc.gated_connections:
                if target not in self.__visited:
                    print("Missing:", req)
        print(self.__inventory)
        print("Cannot reach: %d locations" % (failed))
