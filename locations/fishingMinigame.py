from .droppedKey import DroppedKey
from .constants import *


class FishingMinigame(DroppedKey):
    MULTIWORLD = False

    def __init__(self):
        super().__init__(0x2B1)
