import typing
from .itemInfo import ItemInfo


class Location:
    all = []

    def __init__(self, dungeon=None):
        self.items = []  # type: typing.List[ItemInfo]
        self.dungeon = dungeon
        self.connections = {}
        Location.all.append(self)

    def add(self, *item_infos):
        for ii in item_infos:
            assert isinstance(ii, ItemInfo)
            ii.setLocation(self)
            self.items.append(ii)
        return self

    def connect(self, other, *args, one_way=False):
        assert isinstance(other, Location)

        if other not in self.connections:
            self.connections[other] = []
        self.connections[other] += list(args)
        if not one_way:
            other.connect(self, *args, one_way=True)
        return self
