from .itemInfo import ItemInfo
from .items import *


class FaceKey(ItemInfo):
    OPTIONS = [FACE_KEY]

    def patch(self, rom, option):
        pass

    def read(self, rom):
        return FACE_KEY
