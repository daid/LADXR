from locations.items import *


DEFAULT_ITEM_POOL = {
    SWORD: 2,
    FEATHER: 1,
    HOOKSHOT: 1,
    BOW: 1,
    BOMB: 1,
    MAGIC_POWDER: 1,
    MAGIC_ROD: 1,
    OCARINA: 1,
    PEGASUS_BOOTS: 1,
    POWER_BRACELET: 2,
    SHIELD: 2,
    SHOVEL: 1,
    ROOSTER: 1,
    TOADSTOOL: 1,

    TAIL_KEY: 1, SLIME_KEY: 1, ANGLER_KEY: 1, FACE_KEY: 1, BIRD_KEY: 1,
    GOLD_LEAF: 5,

    FLIPPERS: 1,
    BOWWOW: 1,
    SONG1: 1, SONG2: 1, SONG3: 1,

    BLUE_TUNIC: 1, RED_TUNIC: 1,
    MAX_ARROWS_UPGRADE: 1, MAX_BOMBS_UPGRADE: 1, MAX_POWDER_UPGRADE: 1,

    HEART_CONTAINER: 8,
    HEART_PIECE: 12,

    RUPEES_100: 3,
    RUPEES_20: 6,
    RUPEES_200: 3,
    RUPEES_50: 19,

    SEASHELL: 24,
    MEDICINE: 3,
    GEL: 4,
    MESSAGE: 1,

    COMPASS1: 1, COMPASS2: 1, COMPASS3: 1, COMPASS4: 1, COMPASS5: 1, COMPASS6: 1, COMPASS7: 1, COMPASS8: 1, COMPASS9: 1,
    KEY1: 3, KEY2: 5, KEY3: 9, KEY4: 5, KEY5: 3, KEY6: 3, KEY7: 3, KEY8: 7, KEY9: 3,
    MAP1: 1, MAP2: 1, MAP3: 1, MAP4: 1, MAP5: 1, MAP6: 1, MAP7: 1, MAP8: 1, MAP9: 1,
    NIGHTMARE_KEY1: 1, NIGHTMARE_KEY2: 1, NIGHTMARE_KEY3: 1, NIGHTMARE_KEY4: 1, NIGHTMARE_KEY5: 1, NIGHTMARE_KEY6: 1, NIGHTMARE_KEY7: 1, NIGHTMARE_KEY8: 1, NIGHTMARE_KEY9: 1,
    STONE_BEAK1: 1, STONE_BEAK2: 1, STONE_BEAK3: 1, STONE_BEAK4: 1, STONE_BEAK5: 1, STONE_BEAK6: 1, STONE_BEAK7: 1, STONE_BEAK8: 1, STONE_BEAK9: 1,
    
    INSTRUMENT1: 1, INSTRUMENT2: 1, INSTRUMENT3: 1, INSTRUMENT4: 1, INSTRUMENT5: 1, INSTRUMENT6: 1, INSTRUMENT7: 1, INSTRUMENT8: 1,

    TRADING_ITEM_YOSHI_DOLL: 1,
    TRADING_ITEM_RIBBON: 1,
    TRADING_ITEM_DOG_FOOD: 1,
    TRADING_ITEM_BANANAS: 1,
    TRADING_ITEM_STICK: 1,
    TRADING_ITEM_HONEYCOMB: 1,
    TRADING_ITEM_PINEAPPLE: 1,
    TRADING_ITEM_HIBISCUS: 1,
    TRADING_ITEM_LETTER: 1,
    TRADING_ITEM_BROOM: 1,
    TRADING_ITEM_FISHING_HOOK: 1,
    TRADING_ITEM_NECKLACE: 1,
    TRADING_ITEM_SCALE: 1,
    TRADING_ITEM_MAGNIFYING_GLASS: 1,

    "MEDICINE2": 1, "RAFT": 1, "ANGLER_KEYHOLE": 1, "CASTLE_BUTTON": 1
}


class ItemPool:
    def __init__(self, logic, settings, rnd, plando):
        self.__pool = {}
        self.__setup(logic, settings, rnd)

        if not plando:
            self.__randomizeRupees(settings, rnd)

    def add(self, item, count=1):
        self.__pool[item] = self.__pool.get(item, 0) + count

    def remove(self, item, count=1):
        self.__pool[item] = self.__pool.get(item, 0) - count
        if self.__pool[item] == 0:
            del self.__pool[item]

    def get(self, item):
        return self.__pool.get(item, 0)

    def removeRupees(self, count):
        for n in range(count):
            self.removeRupee()

    def removeRupee(self):
        for item in (RUPEES_20, RUPEES_50, RUPEES_100, RUPEES_200, RUPEES_500):
            if self.get(item) > 0:
                self.remove(item)
                return
        raise RuntimeError("Wanted to remove more rupees from the pool then we have")

    def __setup(self, logic, settings, rnd):
        default_item_pool = DEFAULT_ITEM_POOL
        if settings.overworld == "random":
            default_item_pool = logic.world.map.get_item_pool()
        for item, count in default_item_pool.items():
            self.add(item, count)
        if settings.boomerang != 'default' and settings.overworld != "random":
            self.add(BOOMERANG)
        if settings.owlstatues == 'both':
            self.add(RUPEES_20, 9 + 24)
        elif settings.owlstatues == 'dungeon':
            self.add(RUPEES_20, 24)
        elif settings.owlstatues == 'overworld':
            self.add(RUPEES_20, 9)

        if settings.hpmode == 'inverted':
            self.add(BAD_HEART_CONTAINER, self.get(HEART_CONTAINER))
            self.remove(HEART_CONTAINER, self.get(HEART_CONTAINER))
        elif settings.hpmode == 'low':
            self.add(HEART_PIECE, self.get(HEART_CONTAINER))
            self.remove(HEART_CONTAINER, self.get(HEART_CONTAINER))
        elif settings.hpmode == 'extralow':
            self.add(RUPEES_20, self.get(HEART_CONTAINER))
            self.remove(HEART_CONTAINER, self.get(HEART_CONTAINER))

        if settings.itempool == 'casual':
            self.add(SWORD)
            self.add(FLIPPERS)
            self.add(FEATHER)
            self.add(HOOKSHOT)
            self.add(BOW)
            self.add(BOMB)
            self.add(MAGIC_POWDER)
            self.add(MAGIC_ROD)
            self.add(OCARINA)
            self.add(PEGASUS_BOOTS)
            self.add(POWER_BRACELET)
            self.add(SHOVEL)
            self.add(RUPEES_200, 2)
            self.removeRupees(14)

            for n in range(9):
                self.remove("MAP%d" % (n + 1))
                self.remove("COMPASS%d" % (n + 1))
                self.add("KEY%d" % (n + 1))
                self.add("NIGHTMARE_KEY%d" % (n +1))
        elif settings.itempool == 'pain':
            self.add(BAD_HEART_CONTAINER, 12)
            self.remove(BLUE_TUNIC)
            self.removeRupees(7-self.get(MEDICINE))
            self.remove(MEDICINE, self.get(MEDICINE))
            self.remove(HEART_PIECE, 4)
        elif settings.itempool == 'keyup':
            for n in range(9):
                self.remove("MAP%d" % (n + 1))
                self.remove("COMPASS%d" % (n + 1))
                self.add("KEY%d" % (n +1))
                self.add("NIGHTMARE_KEY%d" % (n +1))
            if settings.owlstatues in ("none", "overworld"):
                for n in range(9):
                    self.remove("STONE_BEAK%d" % (n + 1))
                    self.add("KEY%d" % (n +1))

        if settings.dungeon_items == 'keysy':
            for n in range(9):
                for amount, item_name in ((9, "KEY"), (1, "NIGHTMARE_KEY")):
                    item_name = "%s%d" % (item_name, n + 1)
                    if item_name in self.__pool:
                        self.add(RUPEES_20, self.__pool[item_name])
                        self.remove(item_name, self.__pool[item_name])
                    self.add(item_name, amount)

        if settings.overworld == "dungeondive":
            self.remove(SWORD)
            self.remove(MAX_ARROWS_UPGRADE)
            self.remove(MAX_BOMBS_UPGRADE)
            self.remove(MAX_POWDER_UPGRADE)
            self.remove(SEASHELL, 24)
            self.remove(TAIL_KEY)
            self.remove(SLIME_KEY)
            self.remove(ANGLER_KEY)
            self.remove(FACE_KEY)
            self.remove(BIRD_KEY)
            self.remove(GOLD_LEAF, 5)
            self.remove(SONG2)
            self.remove(SONG3)
            self.remove(HEART_PIECE, 8)
            self.remove(RUPEES_50, 9)
            self.removeRupees(5-self.get(MEDICINE))
            self.remove(MEDICINE, self.get(MEDICINE))
            self.remove(MESSAGE)
            self.remove(BOWWOW)
            self.remove(ROOSTER)
            self.remove(GEL, 2)
            self.remove("MEDICINE2")
            self.remove("RAFT")
            self.remove("ANGLER_KEYHOLE")
            self.remove("CASTLE_BUTTON")
            self.remove(TRADING_ITEM_YOSHI_DOLL)
            self.remove(TRADING_ITEM_RIBBON)
            self.remove(TRADING_ITEM_DOG_FOOD)
            self.remove(TRADING_ITEM_BANANAS)
            self.remove(TRADING_ITEM_STICK)
            self.remove(TRADING_ITEM_HONEYCOMB)
            self.remove(TRADING_ITEM_PINEAPPLE)
            self.remove(TRADING_ITEM_HIBISCUS)
            self.remove(TRADING_ITEM_LETTER)
            self.remove(TRADING_ITEM_BROOM)
            self.remove(TRADING_ITEM_FISHING_HOOK)
            self.remove(TRADING_ITEM_NECKLACE)
            self.remove(TRADING_ITEM_SCALE)
            self.remove(TRADING_ITEM_MAGNIFYING_GLASS)
        elif not settings.rooster:
            self.remove(ROOSTER)
            self.add(RUPEES_50)

        if settings.overworld == "nodungeons":
            for n in range(9):
                for item_name in {KEY, NIGHTMARE_KEY, MAP, COMPASS, STONE_BEAK}:
                    self.remove(f"{item_name}{n+1}", self.get(f"{item_name}{n+1}"))
            if self.get(BLUE_TUNIC) > 0:
                self.remove(BLUE_TUNIC)
            else:
                self.removeRupee()
            self.remove(RED_TUNIC)
            self.remove(SEASHELL, 3)
            self.removeRupees(29-self.get(MEDICINE))
            self.remove(MEDICINE, self.get(MEDICINE))
            self.remove(GEL, 4)
            self.remove(MESSAGE, 1)
            self.add(RUPEES_500, 3)
        if settings.overworld == "dungeonchain":
            self.__pool = {}
            required_item_count = 1  # Start item
            key_counts = [3, 5, 9, 5, 3, 3, 3, 7, 3]
            item_counts = [3, 3, 4, 4, 5, 7, 4, 7, 0]
            required_items_per_dungeon = [
                {FEATHER, SHIELD, BOMB},
                {POWER_BRACELET, FEATHER},
                {POWER_BRACELET, PEGASUS_BOOTS},
                {SHIELD, FLIPPERS, FEATHER, PEGASUS_BOOTS, BOMB},
                {HOOKSHOT, FEATHER, BOMB, POWER_BRACELET, FLIPPERS},
                {POWER_BRACELET, POWER_BRACELET+"2", BOMB, FEATHER, HOOKSHOT},
                {POWER_BRACELET, SHIELD, SHIELD+"2", BOMB, HOOKSHOT},
                {MAGIC_ROD, BOMB, FEATHER, POWER_BRACELET, HOOKSHOT},
                {POWER_BRACELET, HOOKSHOT}
            ]
            required_items = {SWORD, BOW, MAGIC_POWDER}
            for dungeon_idx in logic.world_setup.dungeon_chain:
                self.add(f"KEY{dungeon_idx+1}", key_counts[dungeon_idx])
                self.add(f"NIGHTMARE_KEY{dungeon_idx + 1}")
                self.add(f"MAP{dungeon_idx + 1}")
                self.add(f"COMPASS{dungeon_idx + 1}")
                self.add(f"STONE_BEAK{dungeon_idx + 1}")
                if dungeon_idx != 8:
                    self.add(HEART_CONTAINER)
                required_item_count += item_counts[dungeon_idx]
                required_items.update(required_items_per_dungeon[dungeon_idx])
            for item in required_items:
                if item.endswith("2"):
                    item = item[:-1]
                self.add(item)
                required_item_count -= 1
            major_additions = [SWORD, FEATHER, HOOKSHOT, BOW, BOMB, MAGIC_POWDER, MAGIC_ROD, PEGASUS_BOOTS, POWER_BRACELET, SHIELD, BOOMERANG]
            minor_additions = [BOMB, MAGIC_POWDER, BLUE_TUNIC, RED_TUNIC, MAX_ARROWS_UPGRADE, MAX_BOMBS_UPGRADE, MAX_POWDER_UPGRADE, MEDICINE]
            junk_items = [RUPEES_100, RUPEES_20, RUPEES_50, SEASHELL, GEL, MESSAGE]
            max_counts = {BLUE_TUNIC: 1, RED_TUNIC: 1, MAX_ARROWS_UPGRADE: 1, MAX_BOMBS_UPGRADE: 1, MAX_POWDER_UPGRADE: 1, MEDICINE: 1, SWORD: 2, MESSAGE: 1}
            for n in range(3):
                pick = rnd.choice(major_additions)
                if pick not in required_items and required_item_count > 0:
                    self.add(pick)
                    required_item_count -= 1
            for n in range(required_item_count // 3):
                pick = rnd.choice(minor_additions)
                if required_item_count > 0 and self.get(pick) < max_counts.get(pick, 999):
                    self.add(pick)
                    required_item_count -= 1

            assert required_item_count >= 0
            while required_item_count > 0:
                pick = rnd.choice(junk_items)
                if required_item_count > 0 and self.get(pick) < max_counts.get(pick, 999):
                    self.add(pick)
                    required_item_count -= 1

        if settings.bowwow == 'always':
            # Bowwow mode takes a sword from the pool to give as bowwow. So we need to fix that.
            self.add(SWORD)
            self.remove(BOWWOW)
        elif settings.bowwow == 'swordless':
            # Bowwow mode takes a sword from the pool to give as bowwow, we need to remove all swords and Bowwow except for 1
            self.add(RUPEES_20, self.get(BOWWOW) + self.get(SWORD) - 1)
            self.remove(SWORD, self.get(SWORD) - 1)
            self.remove(BOWWOW, self.get(BOWWOW))
            
        if settings.goal == "seashells":
            for n in range(8):
                self.remove("INSTRUMENT%d" % (n + 1))
            self.add(SEASHELL, 8)
            if self.get(SEASHELL) < 20:
                raise RuntimeError("Not enough seashells (" + str(self.get(SEASHELL)) + ") available in itempool")

        # In multiworld, put a bit more rupees in the seed, this helps with generation (2nd shop item)
        #   As we cheat and can place rupees for the wrong player.
        if settings.multiworld:
            rupees20 = self.__pool.get(RUPEES_20, 0)
            self.add(RUPEES_50, rupees20 // 2)
            self.remove(RUPEES_20, rupees20 // 2)
            rupees50 = self.__pool.get(RUPEES_50, 0)
            self.add(RUPEES_200, rupees50 // 5)
            self.remove(RUPEES_50, rupees50 // 5)

    def __randomizeRupees(self, options, rnd):
        # Remove rupees from the item pool and replace them with other items to create more variety
        rupee_item = []
        rupee_item_count = []
        for k, v in self.__pool.items():
            if k in {RUPEES_20, RUPEES_50} and v > 0:
                rupee_item.append(k)
                rupee_item_count.append(v)
        rupee_chests = sum(v for k, v in self.__pool.items() if k.startswith("RUPEES_"))
        if rupee_chests // 5 > sum(rupee_item_count):
            rupee_chests = 5*sum(rupee_item_count)
        for n in range(rupee_chests // 5):
            new_item = rnd.choices((BOMB, SINGLE_ARROW, ARROWS_10, MAGIC_POWDER, MEDICINE), (10, 5, 10, 10, 1))[0]
            while True:
                remove_item = rnd.choices(rupee_item, rupee_item_count)[0]
                if self.get(remove_item) > 0:
                    break
            self.add(new_item)
            self.remove(remove_item)

    def toDict(self):
        return self.__pool.copy()
