from .chest import Chest
from .items import *


# The multi chest puzzle can contain only consumable items.
class MultiChest(Chest):
    OPTIONS = [MAGIC_POWDER, BOMB, MEDICINE, RUPEES_50, RUPEES_20, RUPEES_100, RUPEES_200, RUPEES_500, SEASHELL, MESSAGE, GEL, ARROWS_10, SINGLE_ARROW]

    def __init__(self, room):
        super().__init__(room)
        self.priority = 1

    def configure(self, options):
        pass  # Do not call super, so we do not configure this chest for keysanity
