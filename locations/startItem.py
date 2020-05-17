from .itemInfo import ItemInfo


class StartItem(ItemInfo):
    OPTIONS = ["SHIELD"] #, "POWER_BRACELET", "FEATHER", "BOOMERANG"]
    MAPPING = {"SWORD": "01", "BOMB": "02", "POWER_BRACELET": "03", "SHIELD": "04", "BOW": "05", "HOOKSHOT": "06",
               "MAGIC_ROD": "07", "PEGASUS_BOOTS": "08", "OCARINA": "09", "FEATHER": "0A", "SHOVEL": "0B",
               "MAGIC_POWDER": "0C", "BOOMERANG": "0D"}
    ICON = {"SWORD": "84", "BOMB": "80", "POWER_BRACELET": "82", "SHIELD": "86", "BOW": "88", "HOOKSHOT": "8A",
            "MAGIC_ROD": "8C", "PEGASUS_BOOTS": "98", "OCARINA": "90", "FEATHER": "92", "SHOVEL": "96",
            "MAGIC_POWDER": "8E", "BOOMERANG": "A4"}

    def patch(self, rom, option):
        # Change which item you get at the start.
        # (NOTE: This also sets the shield level to 1, which is fine, even if we do not get the shield)
        # Giving a sword here, gives a lvl0 sword. Which... does no damage.
        rom.patch(5, 0xCD1, "04", self.MAPPING[option])
        rom.patch(5, 0xCC6, "86", self.ICON[option]) # patch shield that icon that is shown.
        # Patch the text that Tarin uses to give your shield back.
        rom.texts[0x54] = b"#####, is it    " \
                        + b"dangerous to go " \
                        + b"alone, take this\xff"
        rom.texts[0x91] = b"Got the ...     " \
                        + b"something!\xff"

    def read(self, rom):
        value = rom.banks[5][0xCD1]
        for k, v in self.MAPPING.items():
            if int(v, 16) == value:
                return k
        raise ValueError("Could not find start item contents in ROM (0x%02x)" % (value))
