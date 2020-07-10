from .droppedKey import DroppedKey


class Song(DroppedKey):
    # Due to the patches a song acts like a dropped key, except that it does not do multiworld
    MULTIWORLD = False
