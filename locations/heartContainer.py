from .droppedKey import DroppedKey
from .items import *


class HeartContainer(DroppedKey):
    # Due to the patches a heartContainers acts like a dropped key.
    def configure(self, options):
        if options.hpmode == 'inverted':
            self.OPTIONS = [BAD_HEART_CONTAINER]
        elif options.heartcontainers:
            super().configure(options)
        else:
            self.OPTIONS = [HEART_CONTAINER]

    def read(self, rom):
        if len(self.OPTIONS) == 1:
            return self.OPTIONS[0]
        return super().read(rom)
