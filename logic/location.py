import typing
from .requirements import hasConsumableRequirement
from locations.itemInfo import ItemInfo


class Location:
    all = []

    def __init__(self, dungeon=None):
        self.items = []  # type: typing.List[ItemInfo]
        self.dungeon = dungeon
        self.__connected_to = set()
        self.simple_connections = []
        self.gated_connections = []
        Location.all.append(self)

    def add(self, *item_infos):
        for ii in item_infos:
            assert isinstance(ii, ItemInfo)
            ii.setLocation(self)
            self.items.append(ii)
        return self

    def connect(self, other, *args, one_way=False):
        assert isinstance(other, Location)
        assert other not in self.__connected_to

        self.__connected_to.add(other)

        if hasConsumableRequirement(args):
            self.gated_connections.append((other, args))
        else:
            self.simple_connections.append((other, args))
        if not one_way:
            other.connect(self, *args, one_way=True)
        return self
