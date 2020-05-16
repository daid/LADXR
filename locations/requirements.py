from location import *

bush = OR("SWORD", "BOMB", "MAGIC_POWDER", "MAGIC_ROD", "POWER_BRACELET")
attack = OR("SWORD", "BOMB", "BOW", "MAGIC_ROD", "BOOMERANG")
attack_no_bomb = OR("SWORD", "BOW", "MAGIC_ROD", "BOOMERANG")
attack_skeleton = OR("SWORD", "BOMB", "BOW", "BOOMERANG")  # cannot kill skeletons with the fire rod
rear_attack = OR("SWORD", "BOMB")
fire = OR("MAGIC_POWDER", "MAGIC_ROD")
