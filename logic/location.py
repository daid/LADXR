import typing
from .requirements import hasConsumableRequirement, OR
from locations.itemInfo import ItemInfo
from collections.abc import Iterable


class Location:
    def __init__(self, name=None, dungeon=None):
        self.items = []  # type: typing.List[ItemInfo]
        self.dungeon = dungeon
        self.__connected_to = set()
        self.simple_connections = []
        self.gated_connections = []
        self.name = name

    def add(self, *item_infos):
        for ii in item_infos:
            assert isinstance(ii, ItemInfo)
            ii.setLocation(self)
            self.items.append(ii)
        return self

    def connect(self, others, req="UNSET", *, back="UNSET"):
        if not isinstance(others, Iterable):
            others = [others]

        # Assume there's no forward requirement if nothing is specified
        if req == "UNSET":
            req = None

        # Assume back requirement matches forward if nothing is specified
        if back == "UNSET":
            back = req

        for other in others:
            self.singleConnect(other, req)
            other.singleConnect(self, back)

        return self
    
    def singleConnect(self, other, req):
        assert isinstance(other, Location), type(other)

        if isinstance(req, bool):
            if req:
                self.singleConnect(other, None)
            return

        if other in self.__connected_to:
            for idx, data in enumerate(self.gated_connections):
                if data[0] == other:
                    if req is None or data[1] is None:
                        self.gated_connections[idx] = (other, None)
                    else:
                        self.gated_connections[idx] = (other, OR(req, data[1]))
                    break
            for idx, data in enumerate(self.simple_connections):
                if data[0] == other:
                    if req is None or data[1] is None:
                        self.simple_connections[idx] = (other, None)
                    else:
                        self.simple_connections[idx] = (other, OR(req, data[1]))
                    break
        else:
            self.__connected_to.add(other)

            if hasConsumableRequirement(req):
                self.gated_connections.append((other, req))
            else:
                self.simple_connections.append((other, req))
    

    def __repr__(self):
        return "<%s:%s:%d:%d:%d>" % (self.__class__.__name__, self.dungeon, len(self.items), len(self.simple_connections), len(self.gated_connections))

    def friendlyName(self, recurse=True):
        if self.name:
            return self.name

        if self.items:
            return self.items[0].nameId
        
        if recurse:
            uniqueConnections = {x[0].friendlyName(recurse=False) for x in self.simple_connections + self.gated_connections}
            
            return 'Unnamed - ' + ','.join(uniqueConnections)
        
        return 'Unnamed'