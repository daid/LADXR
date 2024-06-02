from . import dungeon1
from . import dungeon2
from . import dungeon3
from . import dungeon4
from . import dungeon5
from . import dungeon6
from . import dungeon7
from . import dungeon8
from . import dungeonColor
from .location import Location
from locations.all import *
from .requirements import *
import cavegen


def construct(configuration_options, *, world_setup, world, requirements_settings):
    dungeon_constructors = {1: dungeon1.Dungeon1, 2: dungeon2.Dungeon2, 3: dungeon3.Dungeon3, 4: dungeon4.Dungeon4, 5: dungeon5.Dungeon5, 6: dungeon6.Dungeon6, 7: dungeon7.Dungeon7, 8: dungeon8.Dungeon8, 0: dungeonColor.DungeonColor}
    dungeon_constructors.update({
        "shop": Shop, "mamu": Mamu, "trendy": Trendy, "dream": DreamShrine, "chestcave": ChestCave,
    })
    for index in world_setup.dungeon_chain:
        if isinstance(index, cavegen.Generator):
            world.chain(CaveGen(configuration_options, world_setup, requirements_settings, index))
        else:
            world.chain(dungeon_constructors[index](configuration_options, world_setup, requirements_settings))


class Shop:
    def __init__(self, configuration_options, world_setup, requirements_settings):
        self.entrance = Location()
        self.final_room = self.entrance

        Location().add(ShopItem(0, price=200)).connect(self.entrance, COUNT("RUPEES", 200))
        Location().add(ShopItem(1, price=500)).connect(self.entrance, COUNT("RUPEES", 500))


class Mamu:
    def __init__(self, configuration_options, world_setup, requirements_settings):
        self.entrance = Location()
        self.final_room = self.entrance

        Location().add(Song(0x2FB)).connect(self.entrance, AND(OCARINA, COUNT("RUPEES", 300)))


class Trendy:
    def __init__(self, configuration_options, world_setup, requirements_settings):
        self.entrance = Location()
        self.final_room = self.entrance

        Location().add(TradeSequenceItem(0x2A0, TRADING_ITEM_YOSHI_DOLL)).connect(self.entrance, FOUND("RUPEES", 50))


class DreamShrine:
    def __init__(self, configuration_options, world_setup, requirements_settings):
        self.entrance = Location()
        self.final_room = self.entrance

        dream_hut_right = Location().add(Chest(0x2BF)).connect(self.entrance, SWORD)
        if configuration_options.logic != "casual":
            dream_hut_right.connect(self.entrance, OR(BOOMERANG, HOOKSHOT, FEATHER))
        Location().add(Chest(0x2BE)).connect(dream_hut_right, PEGASUS_BOOTS)


class ChestCave:
    def __init__(self, configuration_options, world_setup, requirements_settings):
        self.entrance = Location()
        self.final_room = self.entrance

        self.entrance.add(Chest(0x2CD))


class CaveGen:
    def __init__(self, configuration_options, world_setup, requirements_settings, random_cave):
        self.requirements_settings = requirements_settings
        self.entrance = Location()
        self.dungeon = random_cave.map_id + 1 if random_cave.map_id < 8 else None
        self.total_keys = 0
        self._add_room(self.entrance, random_cave.start)

    def _add_room(self, location, room):
        if room.template.logic:
            location = Location(dungeon=self.dungeon).connect(location, room.template.logic)
        if room.type == "end":
            self.final_room = location
        elif room.type == "reward":
            if room.template.type == "chest":
                location.add(Chest(room.room_id))
            elif room.template.type == "item":
                location.add(DroppedKey(room.room_id))
            else:
                raise RuntimeError(f"Reward room with no suitable template type? {room.template.type}")
        for c in room.connections:
            next_location = location
            if c.type == "bomb":
                next_location = Location(dungeon=self.dungeon).connect(location, BOMB)
            if c.type == "key":
                self.total_keys += 1
                next_location = Location(dungeon=self.dungeon).connect(location, AND(f"KEY{self.dungeon}", FOUND(F"KEY{self.dungeon}", self.total_keys)))
            self._add_room(next_location, c.target)
