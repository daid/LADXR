class CheckMetadata:
    def __init__(self, name, area):
        self.name = name
        self.area = area
    
    def __repr__(self):
        return "%s - %s" % (self.area, self.name)

checkMetadataTable = {
    "0x1F5": CheckMetadata("Boomerang Guy Item", "Toronbo Shores"), #http://artemis251.fobby.net/zelda/maps/underworld1/01F5.GIF
    "0x2A3": CheckMetadata("Tarin's Gift", "Mabe Villiage"), #http://artemis251.fobby.net/zelda/maps/underworld2/02A3.GIF
    "0x301-0": CheckMetadata("Tunic Fairy Item 1", "Color Dungeon"), #http://artemis251.fobby.net/zelda/maps/underworld3/0301.GIF
    "0x301-1": CheckMetadata("Tunic Fairy Item 2", "Color Dungeon"), #http://artemis251.fobby.net/zelda/maps/underworld3/0301.GIF
    "0x2A2": CheckMetadata("Witch Item", "Koholint Prairie"), #http://artemis251.fobby.net/zelda/maps/underworld2/02A2.GIF
    "0x2A1-0": CheckMetadata("Shop 200 Item", "Mabe Villiage"), #http://artemis251.fobby.net/zelda/maps/underworld2/02A1.GIF
    "0x2A1-1": CheckMetadata("Shop 980 Item", "Mabe Villiage"), #http://artemis251.fobby.net/zelda/maps/underworld2/02A1.GIF
    "0x2A1-2": CheckMetadata("Shop 10 Item", "Mabe Villiage"), #http://artemis251.fobby.net/zelda/maps/underworld2/02A1.GIF
    "0x113": CheckMetadata("Pit Button Chest", "D1, Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/0113.GIF
    "0x115": CheckMetadata("Four Zol Chest", "D1, Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/0115.GIF
    "0x10E": CheckMetadata("Spark, Mini-Moldorm Chest", "D1, Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/010E.GIF
    "0x116": CheckMetadata("Hardhat Beetles Key", "D1, Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/0116.GIF
    "0x10D": CheckMetadata("Mini-Moldorm Spawn Chest", "D1, Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/010D.GIF
    "0x114": CheckMetadata("Two Stalfos, Two Keese Chest", "D1, Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/0114.GIF
    "0x10C": CheckMetadata("Bombable Wall Seashell Chest", "D1, Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/010C.GIF
    "0x103-Owl": CheckMetadata("Spiked Beetle Owl", "D1, Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/0103.GIF
    "0x104-Owl": CheckMetadata("Movable Block Owl", "D1, Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/0104.GIF
    "0x11D": CheckMetadata("Feather Chest", "D1, Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/011D.GIF
    "0x108": CheckMetadata("Nightmare Key Chest", "D1, Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/0108.GIF
    "0x10A": CheckMetadata("Three of a Kind Chest", "D1, Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/010A.GIF
    "0x10A-Owl": CheckMetadata("Three of a Kind Owl", "D1, Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/010A.GIF
    "0x106": CheckMetadata("Moldorm Heart Container", "D1, Tail Cave"), #http://artemis251.fobby.net/zelda/maps/underworld1/0106.GIF
    "0x136": CheckMetadata("Entrance Chest", "D2, Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0136.GIF
    "0x12E": CheckMetadata("Hardhat Beetle Pit Chest", "D2, Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/012E.GIF
    "0x132": CheckMetadata("Two Stalfos Key", "D2, Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0132.GIF
    "0x137": CheckMetadata("Mask-Mimic Chest", "D2, Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0137.GIF
    "0x133-Owl": CheckMetadata("Switch Owl", "D2, Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0133.GIF
    "0x138": CheckMetadata("First Switch Locked Chest", "D2, Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0138.GIF
    "0x139": CheckMetadata("Button Spawn Chest", "D2, Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0139.GIF
    "0x134": CheckMetadata("Mask-Mimic Key", "D2, Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0134.GIF
    "0x126": CheckMetadata("Vacuum Mouth Chest", "D2, Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0126.GIF
    "0x121": CheckMetadata("Outside Boo Buddies Room Chest", "D2, Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0121.GIF
    "0x129-Owl": CheckMetadata("After Hinox Owl", "D2, Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0129.GIF
    "0x12F-Owl": CheckMetadata("Before First Staircase Owl", "D2, Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/012F.GIF
    "0x120": CheckMetadata("Boo Buddies Room Chest", "D2, Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0120.GIF
    "0x122": CheckMetadata("Second Switch Locked Chest", "D2, Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0122.GIF
    "0x127": CheckMetadata("Enemy Order Room Chest", "D2, Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/0127.GIF
    "0x12B": CheckMetadata("Genie Heart Container", "D2, Bottle Grotto"), #http://artemis251.fobby.net/zelda/maps/underworld1/012B.GIF
    "0x153": CheckMetadata("Vacuum Mouth Chest", "D3, Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0153.GIF
    "0x151": CheckMetadata("Two Bombite, Sword Stalfos, Zol Chest", "D3, Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0151.GIF
    "0x14F": CheckMetadata("Four Zol Chest", "D3, Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/014F.GIF
    "0x14E": CheckMetadata("Two Stalfos, Zol Chest", "D3, Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/014E.GIF
    "0x154": CheckMetadata("North Key Room Key", "D3, Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0154.GIF
    "0x154-Owl": CheckMetadata("North Key Room Owl", "D3, Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0154.GIF
    "0x150": CheckMetadata("Sword Stalfos, Keese Switch Chest", "D3, Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0150.GIF
    "0x14C": CheckMetadata("Zol Switch Chest", "D3, Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/014C.GIF
    "0x155": CheckMetadata("West Key Room Key", "D3, Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0155.GIF
    "0x158": CheckMetadata("South Key Room Key", "D3, Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0158.GIF
    "0x14D": CheckMetadata("After Stairs Key", "D3, Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/014D.GIF
    "0x147-Owl": CheckMetadata("Tile Arrow Owl", "D3, Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0147.GIF
    "0x147": CheckMetadata("Tile Arrow Ledge Chest", "D3, Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0147.GIF
    "0x146": CheckMetadata("Boots Chest", "D3, Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0146.GIF
    "0x142": CheckMetadata("Three Zol, Stalfos Chest", "D3, Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0142.GIF
    "0x141": CheckMetadata("Three Bombite Key", "D3, Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0141.GIF
    "0x148": CheckMetadata("Two Zol, Two Pairodd Key", "D3, Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0148.GIF
    "0x144": CheckMetadata("Two Zol, Stalfos Ledge Chest", "D3, Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0144.GIF
    "0x140-Owl": CheckMetadata("Flying Bomb Owl", "D3, Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/0140.GIF
    "0x15B": CheckMetadata("Nightmare Door Key", "D3, Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/015B.GIF
    "0x15A": CheckMetadata("Slime Eye Heart Container", "D3, Key Cavern"), #http://artemis251.fobby.net/zelda/maps/underworld1/015A.GIF
    "0x179": CheckMetadata("Watery Statue Chest", "D4, Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/0179.GIF
    "0x16A": CheckMetadata("NW of Boots Pit Ledge Chest", "D4, Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/016A.GIF
    "0x178": CheckMetadata("Two Spiked Beetle, Zol Chest", "D4, Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/0178.GIF
    "0x17B": CheckMetadata("Crystal Chest", "D4, Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/017B.GIF
    "0x171": CheckMetadata("Lower Bomb Locked Watery Chest", "D4, Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/0171.GIF
    "0x165": CheckMetadata("Upper Bomb Locked Watery Chest", "D4, Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/0165.GIF
    "0x175": CheckMetadata("Flipper Locked Before Boots Pit Chest", "D4, Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/0175.GIF
    "0x16F-Owl": CheckMetadata("Spiked Beetle Owl", "D4, Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/016F.GIF
    "0x169": CheckMetadata("Pit Key", "D4, Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/0169.GIF
    "0x16E": CheckMetadata("Flipper Locked After Boots Pit Chest", "D4, Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/016E.GIF
    "0x16D": CheckMetadata("Blob Chest", "D4, Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/016D.GIF
    "0x168": CheckMetadata("Spark Chest", "D4, Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/0168.GIF
    "0x160": CheckMetadata("Flippers Chest", "D4, Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/0160.GIF
    "0x176": CheckMetadata("Nightmare Key Ledge Chest", "D4, Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/0176.GIF
    "0x1FF": CheckMetadata("Angler Fish Heart Container", "D4, Angler's Tunnel"), #http://artemis251.fobby.net/zelda/maps/underworld1/01FF.GIF
    "0x1A0": CheckMetadata("Entrance Hookshottable Chest", "D5, Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/01A0.GIF
    "0x19E": CheckMetadata("Spark, Two Iron Mask Chest", "D5, Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/019E.GIF
    "0x181": CheckMetadata("Crystal Key", "D5, Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/0181.GIF
    "0x19A-Owl": CheckMetadata("Crystal Owl", "D5, Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/019A.GIF
    "0x19B": CheckMetadata("Flying Bomb Chest", "D5, Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/019B.GIF
    "0x197": CheckMetadata("Three Iron Mask Chest", "D5, Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/0197.GIF
    "0x196": CheckMetadata("Hookshot Note Chest", "D5, Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/0196.GIF
    "0x18A-Owl": CheckMetadata("Star Owl", "D5, Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/018A.GIF
    "0x18E": CheckMetadata("Two Stalfos, Star Pit Chest", "D5, Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/018E.GIF
    "0x188": CheckMetadata("Swort Stalfos, Star, Bridge Chest", "D5, Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/0188.GIF
    "0x18F": CheckMetadata("Flying Bomb Chest", "D5, Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/018F.GIF
    "0x180": CheckMetadata("Master Stalfos Item", "D5, Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/0180.GIF
    "0x183": CheckMetadata("Three Stalfos Chest", "D5, Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/0183.GIF
    "0x186": CheckMetadata("Nightmare Key/Torch Cross Chest", "D5, Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/0186.GIF
    "0x185": CheckMetadata("Slime Eel Heart Container", "D5, Catfish's Maw"), #http://artemis251.fobby.net/zelda/maps/underworld1/0185.GIF
    "0x1CF": CheckMetadata("Mini-Moldorm, Spark Chest", "D6, Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01CF.GIF
    "0x1C9": CheckMetadata("Flying Heart, Statue Chest", "D6, Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01C9.GIF
    "0x1BB-Owl": CheckMetadata("Corridor Owl", "D6, Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01BB.GIF
    "0x1CE": CheckMetadata("L2 Bracelet Chest", "D6, Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01CE.GIF
    "0x1C0": CheckMetadata("Three Wizzrobe, Switch Chest", "D6, Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01C0.GIF
    "0x1B9": CheckMetadata("Stairs Across Statues Chest", "D6, Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01B9.GIF
    "0x1B3": CheckMetadata("Switch, Star Above Statues Chest", "D6, Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01B3.GIF
    "0x1B4": CheckMetadata("Two Wizzrobe Key", "D6, Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01B4.GIF
    "0x1B0": CheckMetadata("Top Left Horse Heads Chest", "D6, Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01B0.GIF
    "0x06C": CheckMetadata("Raft Chest", "D6, Face Shrine"), #http://artemis251.fobby.net/zelda/maps/overworld/006C.GIF
    "0x1BE": CheckMetadata("Water Tektite Chest", "D6, Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01BE.GIF
    "0x1D1": CheckMetadata("Four Wizzrobe Ledge Chest", "D6, Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01D1.GIF
    "0x1D7-Owl": CheckMetadata("Blade Trap Owl", "D6, Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01D7.GIF
    "0x1C3": CheckMetadata("Tile Room Key", "D6, Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01C3.GIF
    "0x1B1": CheckMetadata("Top Right Horse Heads Chest", "D6, Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01B1.GIF
    "0x1B6-Owl": CheckMetadata("Pot Owl", "D6, Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01B6.GIF
    "0x1B6": CheckMetadata("Pot Locked Chest", "D6, Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01B6.GIF
    "0x1BC": CheckMetadata("Facade Heart Container", "D6, Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld1/01BC.GIF
    "0x210": CheckMetadata("Entrance Key", "D7, Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/0210.GIF
    "0x216-Owl": CheckMetadata("Ball Owl", "D7, Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/0216.GIF
    "0x212": CheckMetadata("Horse Head, Bubble Chest", "D7, Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/0212.GIF
    "0x204-Owl": CheckMetadata("Beamos Owl", "D7, Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/0204.GIF
    "0x204": CheckMetadata("Beamos Ledge Chest", "D7, Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/0204.GIF
    "0x209": CheckMetadata("Switch Wrapped Chest", "D7, Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/0209.GIF
    "0x211": CheckMetadata("Three of a Kind, No Pit Chest", "D7, Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/0211.GIF
    "0x21B": CheckMetadata("Hinox Key", "D7, Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/021B.GIF
    "0x201": CheckMetadata("Kirby Ledge Chest", "D7, Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/0201.GIF
    "0x21C-Owl": CheckMetadata("Three of a Kind, Pit Owl", "D7, Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/021C.GIF
    "0x21C": CheckMetadata("Three of a Kind, Pit Chest", "D7, Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/021C.GIF
    "0x224": CheckMetadata("Nightmare Key/After Grim Creeper Chest", "D7, Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/0224.GIF
    "0x21A": CheckMetadata("Mirror Shield Chest", "D7, Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/021A.GIF
    "0x220": CheckMetadata("Conveyor Beamos Chest", "D7, Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/0220.GIF
    "0x2E8": CheckMetadata("Evil Eagle Heart Container", "D7, Eagle's Tower"), #http://artemis251.fobby.net/zelda/maps/underworld2/02E8.GIF
    "0x24F": CheckMetadata("Push Block Chest", "D8, Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/024F.GIF
    "0x24D": CheckMetadata("Left of Hinox Zamboni Chest", "D8, Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/024D.GIF
    "0x25C": CheckMetadata("Vacuum Mouth Chest", "D8, Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/025C.GIF
    "0x24C": CheckMetadata("Left Vire Key", "D8, Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/024C.GIF
    "0x255": CheckMetadata("Spark, Pit Chest", "D8, Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0255.GIF
    "0x246": CheckMetadata("Two Torches Room Chest", "D8, Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0246.GIF
    "0x253-Owl": CheckMetadata("Beamos Owl", "D8, Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0253.GIF
    "0x259": CheckMetadata("Right Lava Chest", "D8, Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0259.GIF
    "0x25A": CheckMetadata("Zamboni, Two Zol Key", "D8, Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/025A.GIF
    "0x25F": CheckMetadata("Four Ropes Pot Chest", "D8, Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/025F.GIF
    "0x245-Owl": CheckMetadata("Bombable Blocks Owl", "D8, Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0245.GIF
    "0x23E": CheckMetadata("Gibdos on Cracked Floor Key", "D8, Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/023E.GIF
    "0x235": CheckMetadata("Lava Ledge Chest", "D8, Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0235.GIF
    "0x237": CheckMetadata("Magic Rod Chest", "D8, Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0237.GIF
    "0x240": CheckMetadata("Beamos Blocked Chest", "D8, Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0240.GIF
    "0x23D": CheckMetadata("Dodongo Chest", "D8, Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/023D.GIF
    "0x000": CheckMetadata("Outside Heart Piece", "D8, Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/overworld/0000.GIF
    "0x241": CheckMetadata("Lava Arrow Statue Key", "D8, Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0241.GIF
    "0x241-Owl": CheckMetadata("Lava Arrow Statue Owl", "D8, Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0241.GIF
    "0x23A": CheckMetadata("West of Boss Door Ledge Chest", "D8, Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/023A.GIF
    "0x232": CheckMetadata("Nightmare Key/Big Zamboni Chest", "D8, Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0232.GIF
    "0x234": CheckMetadata("Hot Head Heart Container", "D8, Turtle Rock"), #http://artemis251.fobby.net/zelda/maps/underworld2/0234.GIF
    "0x314": CheckMetadata("Lower Small Key", "Color Dungeon"), #http://artemis251.fobby.net/zelda/maps/underworld3/0314.GIF
    "0x308-Owl": CheckMetadata("Upper Key Owl", "Color Dungeon"), #http://artemis251.fobby.net/zelda/maps/underworld3/0308.GIF
    "0x308": CheckMetadata("Upper Small Key", "Color Dungeon"), #http://artemis251.fobby.net/zelda/maps/underworld3/0308.GIF
    "0x30F-Owl": CheckMetadata("Entrance Owl", "Color Dungeon"), #http://artemis251.fobby.net/zelda/maps/underworld3/030F.GIF
    "0x30F": CheckMetadata("Entrance Chest", "Color Dungeon"), #http://artemis251.fobby.net/zelda/maps/underworld3/030F.GIF
    "0x311": CheckMetadata("Two Socket Chest", "Color Dungeon"), #http://artemis251.fobby.net/zelda/maps/underworld3/0311.GIF
    "0x302": CheckMetadata("Nightmare Key Chest", "Color Dungeon"), #http://artemis251.fobby.net/zelda/maps/underworld3/0302.GIF
    "0x306": CheckMetadata("Zol Chest", "Color Dungeon"), #http://artemis251.fobby.net/zelda/maps/underworld3/0306.GIF
    "0x307": CheckMetadata("Bullshit Room", "Color Dungeon"), #http://artemis251.fobby.net/zelda/maps/underworld3/0307.GIF
    "0x30A-Owl": CheckMetadata("Puzzowl", "Color Dungeon"), #http://artemis251.fobby.net/zelda/maps/underworld3/030A.GIF
    "0x2BF": CheckMetadata("Dream Hut East", "Mabe Villiage"), #http://artemis251.fobby.net/zelda/maps/underworld2/02BF.GIF
    "0x2BE": CheckMetadata("Dream Hut West", "Mabe Villiage"), #http://artemis251.fobby.net/zelda/maps/underworld2/02BE.GIF
    "0x2A4": CheckMetadata("Well Heart Piece", "Mabe Villiage"), #http://artemis251.fobby.net/zelda/maps/underworld2/02A4.GIF
    "0x2B1": CheckMetadata("Fishing Game Heart Piece", "Mabe Villiage"), #http://artemis251.fobby.net/zelda/maps/underworld2/02B1.GIF
    "0x0A3": CheckMetadata("Bush Field", "Mabe Villiage"), #http://artemis251.fobby.net/zelda/maps/overworld/00A3.GIF
    "0x2B2": CheckMetadata("Dog House Dig", "Mabe Villiage"), #http://artemis251.fobby.net/zelda/maps/underworld2/02B2.GIF
    "0x0D2": CheckMetadata("Outside D1 Tree Bonk", "Toronbo Shores"), #http://artemis251.fobby.net/zelda/maps/overworld/00D2.GIF
    "0x0E5": CheckMetadata("West of Ghost House Chest", "Toronbo Shores"), #http://artemis251.fobby.net/zelda/maps/overworld/00E5.GIF
    "0x1E3": CheckMetadata("Ghost House Barrel", "Martha's Bay"), #http://artemis251.fobby.net/zelda/maps/underworld1/01E3.GIF
    "0x044": CheckMetadata("Heart Piece of Shame", "Koholint Prairie"), #http://artemis251.fobby.net/zelda/maps/overworld/0044.GIF
    "0x071": CheckMetadata("Two Zol, Moblin Chest", "Mysterious Woods"), #http://artemis251.fobby.net/zelda/maps/overworld/0071.GIF
    "0x1E1": CheckMetadata("Mad Batter", "Mysterious Woods"), #http://artemis251.fobby.net/zelda/maps/underworld1/01E1.GIF
    "0x034": CheckMetadata("Swampy Chest", "Goponga Swamp"), #http://artemis251.fobby.net/zelda/maps/overworld/0034.GIF
    "0x041": CheckMetadata("Tail Key Chest", "Mysterious Woods"), #http://artemis251.fobby.net/zelda/maps/overworld/0041.GIF
    "0x2BD": CheckMetadata("Cave Crystal Chest", "Mysterious Woods"), #http://artemis251.fobby.net/zelda/maps/underworld2/02BD.GIF
    "0x2AB": CheckMetadata("Cave Skull Heart Piece", "Mysterious Woods"), #http://artemis251.fobby.net/zelda/maps/underworld2/02AB.GIF
    "0x2B3": CheckMetadata("Hookshot Cave", "Mysterious Woods"), #http://artemis251.fobby.net/zelda/maps/underworld2/02B3.GIF
    "0x2AE": CheckMetadata("Write Cave West", "Goponga Swamp"), #http://artemis251.fobby.net/zelda/maps/underworld2/02AE.GIF
    "0x011-Owl": CheckMetadata("North of Write Owl", "Goponga Swamp"), #http://artemis251.fobby.net/zelda/maps/overworld/0011.GIF #might come out as "0x11
    "0x2AF": CheckMetadata("Write Cave East", "Goponga Swamp"), #http://artemis251.fobby.net/zelda/maps/underworld2/02AF.GIF
    "0x035-Owl": CheckMetadata("Moblin Cave Owl", "Tal Tal Heights"), #http://artemis251.fobby.net/zelda/maps/overworld/0035.GIF
    "0x2DF": CheckMetadata("Graveyard Connector", "Koholint Prairie"), #http://artemis251.fobby.net/zelda/maps/underworld2/02DF.GIF
    "0x074": CheckMetadata("Ghost Grave Dig", "Koholint Prairie"), #http://artemis251.fobby.net/zelda/maps/overworld/0074.GIF
    "0x2E2": CheckMetadata("Moblin Cave", "Tal Tal Heights"), #http://artemis251.fobby.net/zelda/maps/underworld2/02E2.GIF
    "0x2CD": CheckMetadata("Cave East of Mabe", "Ukuku Prairie"), #http://artemis251.fobby.net/zelda/maps/underworld2/02CD.GIF
    "0x2F4": CheckMetadata("Boots 'n' Bomb Cave Bombable Wall", "Ukuku Prairie"), #http://artemis251.fobby.net/zelda/maps/underworld2/02F4.GIF
    "0x2E5": CheckMetadata("Boots 'n' Bomb Cave Chest", "Ukuku Prairie"), #http://artemis251.fobby.net/zelda/maps/underworld2/02E5.GIF
    "0x0A5": CheckMetadata("Outside D3 Ledge Dig", "Ukuku Prairie"), #http://artemis251.fobby.net/zelda/maps/overworld/00A5.GIF
    "0x0A6": CheckMetadata("Outside D3 Island Bush", "Ukuku Prairie"), #http://artemis251.fobby.net/zelda/maps/overworld/00A6.GIF
    "0x08B": CheckMetadata("East of Seashell Mansion Bush", "Ukuku Prairie"), #http://artemis251.fobby.net/zelda/maps/overworld/008B.GIF
    "0x0A4": CheckMetadata("East of Mabe Tree Bonk", "Ukuku Prairie"), #http://artemis251.fobby.net/zelda/maps/overworld/00A4.GIF
    "0x1FD": CheckMetadata("Boots Pit", "Kanalet Castle"), #http://artemis251.fobby.net/zelda/maps/underworld1/01FD.GIF
    "0x0B9": CheckMetadata("Rock Seashell", "Donut Plains"), #http://artemis251.fobby.net/zelda/maps/overworld/00B9.GIF
    "0x0E9": CheckMetadata("Lone Bush", "Martha's Bay"), #http://artemis251.fobby.net/zelda/maps/overworld/00E9.GIF
    "0x0F8": CheckMetadata("Island Bush of Destiny", "Martha's Bay"), #http://artemis251.fobby.net/zelda/maps/overworld/00F8.GIF
    "0x0A8": CheckMetadata("Donut Plains Ledge Dig", "Donut Plains"), #http://artemis251.fobby.net/zelda/maps/overworld/00A8.GIF
    "0x0A8-Owl": CheckMetadata("Donut Plains Ledge Owl", "Donut Plains"), #http://artemis251.fobby.net/zelda/maps/overworld/00A8.GIF
    "0x1E0": CheckMetadata("Mad Batter", "Martha's Bay"), #http://artemis251.fobby.net/zelda/maps/underworld1/01E0.GIF
    "0x0C6-Owl": CheckMetadata("Slime Key Owl", "Pothole Field"), #http://artemis251.fobby.net/zelda/maps/overworld/00C6.GIF
    "0x0C6": CheckMetadata("Slime Key Dig", "Pothole Field"), #http://artemis251.fobby.net/zelda/maps/overworld/00C6.GIF
    "0x2C8": CheckMetadata("Under Richard's House", "Pothole Field"), #http://artemis251.fobby.net/zelda/maps/underworld2/02C8.GIF
    "0x078": CheckMetadata("In the Moat Heart Piece", "Kanalet Castle"), #http://artemis251.fobby.net/zelda/maps/overworld/0078.GIF
    "0x05A": CheckMetadata("Bomberman Meets Whack-a-mole Leaf", "Kanalet Castle"), #http://artemis251.fobby.net/zelda/maps/overworld/005A.GIF
    "0x058": CheckMetadata("Crow Rock Leaf", "Kanalet Castle"), #http://artemis251.fobby.net/zelda/maps/overworld/0058.GIF
    "0x2D2": CheckMetadata("Darknut, Zol, Bubble Leaf", "Kanalet Castle"), #http://artemis251.fobby.net/zelda/maps/underworld2/02D2.GIF
    "0x2C5": CheckMetadata("Bombable Darknut Leaf", "Kanalet Castle"), #http://artemis251.fobby.net/zelda/maps/underworld2/02C5.GIF
    "0x2C6": CheckMetadata("Ball and Chain Darknut Leaf", "Kanalet Castle"), #http://artemis251.fobby.net/zelda/maps/underworld2/02C6.GIF
    "0x0DA": CheckMetadata("Peninsula Dig", "Martha's Bay"), #http://artemis251.fobby.net/zelda/maps/overworld/00DA.GIF
    "0x0DA-Owl": CheckMetadata("Peninsula Owl", "Martha's Bay"), #http://artemis251.fobby.net/zelda/maps/overworld/00DA.GIF
    "0x0CF-Owl": CheckMetadata("Desert Owl", "Yarna Desert"), #http://artemis251.fobby.net/zelda/maps/overworld/00CF.GIF
    "0x2E6": CheckMetadata("Bomb Arrow Cave", "Yarna Desert"), #http://artemis251.fobby.net/zelda/maps/underworld2/02E6.GIF
    "0x1E8": CheckMetadata("Cave Under Lanmola", "Yarna Desert"), #http://artemis251.fobby.net/zelda/maps/underworld1/01E8.GIF
    "0x0FF": CheckMetadata("Rock Seashell", "Yarna Desert"), #http://artemis251.fobby.net/zelda/maps/overworld/00FF.GIF
    "0x018": CheckMetadata("Access Tunnel Exterior", "Tal Tal Mountains"), #http://artemis251.fobby.net/zelda/maps/overworld/0018.GIF
    "0x2BB": CheckMetadata("Access Tunnel Interior", "Tal Tal Mountains"), #http://artemis251.fobby.net/zelda/maps/underworld2/02BB.GIF
    "0x28A": CheckMetadata("Paphl Cave", "Tal Tal Mountains"), #http://artemis251.fobby.net/zelda/maps/underworld2/028A.GIF
    "0x1F2": CheckMetadata("Damp Cave Heart Piece", "Tal Tal Heights"), #http://artemis251.fobby.net/zelda/maps/underworld1/01F2.GIF
    "0x2FC": CheckMetadata("Under Armos Cave", "Southern Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld2/02FC.GIF
    "0x08F-Owl": CheckMetadata("Outside Owl", "Southern Face Shrine"), #http://artemis251.fobby.net/zelda/maps/overworld/008F.GIF
    "0x05C": CheckMetadata("West", "Rapids Ride"), #http://artemis251.fobby.net/zelda/maps/overworld/005C.GIF
    "0x05D": CheckMetadata("East", "Rapids Ride"), #http://artemis251.fobby.net/zelda/maps/overworld/005D.GIF
    "0x05D-Owl": CheckMetadata("Owl", "Rapids Ride"), #http://artemis251.fobby.net/zelda/maps/overworld/005D.GIF
    "0x01E-Owl": CheckMetadata("Outside D7 Owl", "Tal Tal Mountains"), #http://artemis251.fobby.net/zelda/maps/overworld/001E.GIF
    "0x00C": CheckMetadata("Bridge Rock", "Tal Tal Mountains"), #http://artemis251.fobby.net/zelda/maps/overworld/000C.GIF
    "0x2F2": CheckMetadata("Five Chest Game", "Tal Tal Mountains"), #http://artemis251.fobby.net/zelda/maps/underworld2/02F2.GIF
    "0x01D": CheckMetadata("Outside Five Chest Game", "Tal Tal Mountains"), #http://artemis251.fobby.net/zelda/maps/overworld/001D.GIF
    "0x004": CheckMetadata("Outside Mad Batter", "Tal Tal Mountains"), #http://artemis251.fobby.net/zelda/maps/overworld/0004.GIF
    "0x1E2": CheckMetadata("Mad Batter", "Tal Tal Mountains"), #http://artemis251.fobby.net/zelda/maps/underworld1/01E2.GIF
    "0x2BA": CheckMetadata("Access Tunnel Bombable Heart Piece", "Tal Tal Mountains"), #http://artemis251.fobby.net/zelda/maps/underworld2/02BA.GIF
    "0x0F2": CheckMetadata("Sword on the Beach", "Toronbo Shores"), #http://artemis251.fobby.net/zelda/maps/overworld/00F2.GIF
    "0x050": CheckMetadata("Toadstool", "Mysterious Woods"), #http://artemis251.fobby.net/zelda/maps/overworld/0050.GIF
    "0x0CE": CheckMetadata("Lanmola", "Yarna Desert"), #http://artemis251.fobby.net/zelda/maps/overworld/00CE.GIF
    "0x27F": CheckMetadata("Armos Knight", "Southern Face Shrine"), #http://artemis251.fobby.net/zelda/maps/underworld2/027F.GIF
    "0x27A": CheckMetadata("Bird Key Cave", "Tal Tal Mountains"), #http://artemis251.fobby.net/zelda/maps/underworld2/027A.GIF
}