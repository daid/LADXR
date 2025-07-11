var options =
[
 {
  "key": "seed",
  "category": "Main",
  "short_key": "<",
  "label": "Seed",
  "description": "For multiple people to generate the same randomization result, enter the generated seed number here.\nNote, not all strings are valid seeds.",
  "multiworld": false,
  "aesthetic": false,
  "default": "",
  "placeholder": "Leave empty for random seed"
 },
 {
  "key": "logic",
  "category": "Main",
  "short_key": "L",
  "label": "Logic",
  "description": "Affects where items are allowed to be placed.\n[Casual] Same as normal, except that a few more complex options are removed, like removing bushes with powder and killing enemies with powder or bombs.\n[Normal] playable without using any tricks or glitches. Requires nothing to be done outside of normal item usage.\n[Hard] More advanced techniques may be required, but glitches are not. Examples include tricky jumps, killing enemies with only pots and skipping keys with smart routing.\n[Glitched] Advanced glitches and techniques may be required, but extremely difficult or tedious tricks are not required. Examples include Bomb Triggers, Super Jumps and Jesus Jumps.\n[Hell] Obscure and hard techniques may be required. Examples include featherless jumping with boots and/or hookshot, sequential pit buffers and unclipped superjumps. Things in here can be extremely hard to do or very time consuming. Only insane people go for this.",
  "multiworld": true,
  "aesthetic": false,
  "default": "",
  "options": [
   {
    "key": "casual",
    "short": "c",
    "label": "Casual"
   },
   {
    "key": "",
    "short": "",
    "label": "Normal"
   },
   {
    "key": "hard",
    "short": "h",
    "label": "Hard"
   },
   {
    "key": "glitched",
    "short": "g",
    "label": "Glitched"
   },
   {
    "key": "hell",
    "short": "H",
    "label": "Hell"
   }
  ]
 },
 {
  "key": "forwardfactor",
  "category": "Main",
  "short_key": "F",
  "label": "Forward Factor",
  "description": "Forward item weight adjustment factor, lower values generate more rear heavy seeds while higher values generate front heavy seeds. Default is 0.5.",
  "multiworld": true,
  "aesthetic": false,
  "default": 0.0
 },
 {
  "key": "accessibility",
  "category": "Main",
  "short_key": "A",
  "label": "Accessibility",
  "description": "\n[100% Locations] Guaranteed that every single item can be reached and gained.\n[Beatable] Only guarantees that the game is beatable. Certain items/chests might never be reachable.",
  "multiworld": true,
  "aesthetic": false,
  "default": "all",
  "options": [
   {
    "key": "all",
    "short": "a",
    "label": "100% Locations"
   },
   {
    "key": "goal",
    "short": "g",
    "label": "Beatable"
   }
  ]
 },
 {
  "key": "race",
  "category": "Main",
  "short_key": "V",
  "label": "Race mode",
  "description": "\nSpoiler logs can not be generated for ROMs generated with race mode enabled, and seed generation is slightly different.",
  "multiworld": false,
  "aesthetic": false,
  "default": false
 },
 {
  "key": "heartpiece",
  "category": "Items",
  "short_key": "h",
  "label": "Randomize heart pieces",
  "description": "Includes heart pieces in the item pool.",
  "multiworld": true,
  "aesthetic": false,
  "default": true
 },
 {
  "key": "seashells",
  "category": "Items",
  "short_key": "s",
  "label": "Randomize hidden seashells",
  "description": "Randomizes the secret sea shells hiding in the ground/trees/mansion. (Chests are always randomized.)",
  "multiworld": true,
  "aesthetic": false,
  "default": true
 },
 {
  "key": "heartcontainers",
  "category": "Items",
  "short_key": "H",
  "label": "Randomize heart containers",
  "description": "Includes boss heart container drops in the item pool.",
  "multiworld": true,
  "aesthetic": false,
  "default": true
 },
 {
  "key": "instruments",
  "category": "Items",
  "short_key": "I",
  "label": "Randomize instruments",
  "description": "Instruments are placed on random locations, dungeon goal will just contain a random item.",
  "multiworld": true,
  "aesthetic": false,
  "default": false
 },
 {
  "key": "tradequest",
  "category": "Items",
  "short_key": "T",
  "label": "Randomize trade quest",
  "description": "Trade quest items are randomized, each NPC takes its normal trade quest item, but gives a random item.",
  "multiworld": true,
  "aesthetic": false,
  "default": true
 },
 {
  "key": "witch",
  "category": "Items",
  "short_key": "W",
  "label": "Randomize item given by the witch",
  "description": "Adds both the toadstool and the reward for giving the toadstool to the witch to the item pool.",
  "multiworld": true,
  "aesthetic": false,
  "default": true
 },
 {
  "key": "rooster",
  "category": "Items",
  "short_key": "R",
  "label": "Add the rooster",
  "description": "Adds the rooster to the item pool. Without this option, the rooster spot is still a check giving an item. But you will never find the rooster. In that case, any rooster spot is accessible without rooster by other means.",
  "multiworld": true,
  "aesthetic": false,
  "default": true
 },
 {
  "key": "boomerang",
  "category": "Items",
  "short_key": "Z",
  "label": "Boomerang trade",
  "description": "\n[Normal] Requires magnifying lens to get the boomerang.\n[Trade] Allows to trade an inventory item for a random other inventory item, and the boomerang is shuffled.\n[Gift] You get a random gift of any item, and the boomerang is shuffled.",
  "multiworld": true,
  "aesthetic": false,
  "default": "gift",
  "options": [
   {
    "key": "default",
    "short": "d",
    "label": "Normal"
   },
   {
    "key": "trade",
    "short": "t",
    "label": "Trade"
   },
   {
    "key": "gift",
    "short": "g",
    "label": "Gift"
   }
  ]
 },
 {
  "key": "dungeon_items",
  "category": "Gameplay",
  "short_key": "D",
  "label": "Dungeon items",
  "description": "Sets if dungeon items can only be in their respective dungeon, or everywhere.\n[Standard] Dungeon items are only in their dungeon.\n[Maps/.../..] Specified items can be anywhere.\n[Keysanity] All dungeon items can be anywhere.\n[Keysy] No keys, key doors are already open.",
  "multiworld": true,
  "aesthetic": false,
  "default": "",
  "options": [
   {
    "key": "",
    "short": "",
    "label": "Standard"
   },
   {
    "key": "smallkeys",
    "short": "s",
    "label": "Small keys"
   },
   {
    "key": "nightmarekeys",
    "short": "n",
    "label": "Nightmare keys"
   },
   {
    "key": "localkeys",
    "short": "L",
    "label": "Map/Compass/Beaks"
   },
   {
    "key": "localnightmarekey",
    "short": "N",
    "label": "MCB + SmallKeys"
   },
   {
    "key": "keysanity",
    "short": "K",
    "label": "Keysanity"
   },
   {
    "key": "keysy",
    "short": "k",
    "label": "Keysy"
   }
  ]
 },
 {
  "key": "randomstartlocation",
  "category": "Entrances",
  "short_key": "r",
  "label": "Random start location",
  "description": "Randomize where your starting house is located.",
  "multiworld": true,
  "aesthetic": false,
  "default": false
 },
 {
  "key": "dungeonshuffle",
  "category": "Entrances",
  "short_key": "u",
  "label": "Dungeon shuffle",
  "description": "Randomizes the dungeon that each dungeon entrance leads to.",
  "multiworld": true,
  "aesthetic": false,
  "default": false
 },
 {
  "key": "entranceshuffle",
  "category": "Entrances",
  "short_key": "E",
  "label": "Entrance randomizer",
  "description": "Randomizes where overworld entrances lead to.\n[Simple] Single entrance caves that contain items are randomized.\n[Split] Connector caves are also randomized, in a separate pool from single entrance caves.\n[Mixed] Connector caves are also randomized, in the same pool as single entrance caves.\n[Wild] Connections can go from overworld to overworld, or inside to inside.\n[Chaos] Entrance and exits are decoupled.\n[Insane] Combines chaos and wild, anything goes anywhere, there is no god.\n[Madness] Even worse then insane, it makes it so multiple entrances can lead to the same location.\nIf random start location and/or dungeon shuffle is enabled, then these will be shuffled with all the entrances.",
  "multiworld": true,
  "aesthetic": false,
  "default": "none",
  "options": [
   {
    "key": "none",
    "short": "",
    "label": "Default"
   },
   {
    "key": "simple",
    "short": "s",
    "label": "Simple"
   },
   {
    "key": "split",
    "short": "S",
    "label": "Split"
   },
   {
    "key": "mixed",
    "short": "m",
    "label": "Mixed"
   },
   {
    "key": "wild",
    "short": "w",
    "label": "Wild"
   },
   {
    "key": "chaos",
    "short": "c",
    "label": "Chaos"
   },
   {
    "key": "insane",
    "short": "i",
    "label": "Insane"
   },
   {
    "key": "madness",
    "short": "M",
    "label": "Madness"
   }
  ]
 },
 {
  "key": "shufflejunk",
  "category": "Entrances",
  "short_key": "j",
  "label": "Shuffle itemless entrances",
  "description": "Caves/houses without items are also randomized when entrance randomizer is set.",
  "multiworld": true,
  "aesthetic": false,
  "default": false,
  "visible_if": [
   "entranceshuffle",
   "simple",
   "split",
   "mixed",
   "wild",
   "chaos",
   "insane",
   "madness"
  ]
 },
 {
  "key": "shuffleannoying",
  "category": "Entrances",
  "short_key": "a",
  "label": "Shuffle annoying entrances",
  "description": "A few very annoying entrances (Mamu and the Raft House) will also be randomized when entrance randomizer is set.",
  "multiworld": true,
  "aesthetic": false,
  "default": false,
  "visible_if": [
   "entranceshuffle",
   "simple",
   "split",
   "mixed",
   "wild",
   "chaos",
   "insane",
   "madness"
  ]
 },
 {
  "key": "shufflewater",
  "category": "Entrances",
  "short_key": "w",
  "label": "Shuffle water entrances",
  "description": "Entrances that lead to water (Manbo and Damp Cave) will also be randomized when entrance randomizer is set. Use the warp-to-home from the Save & Quit menu if you get stuck (hold A+B+Start+Select until it works).",
  "multiworld": true,
  "aesthetic": false,
  "default": false,
  "visible_if": [
   "entranceshuffle",
   "simple",
   "split",
   "mixed",
   "wild",
   "chaos",
   "insane",
   "madness"
  ]
 },
 {
  "key": "boss",
  "category": "Gameplay",
  "short_key": "B",
  "label": "Boss shuffle",
  "description": "Randomizes the dungeon bosses that each dungeon has.",
  "multiworld": true,
  "aesthetic": false,
  "default": "default",
  "options": [
   {
    "key": "default",
    "short": "",
    "label": "Normal"
   },
   {
    "key": "shuffle",
    "short": "s",
    "label": "Shuffle"
   },
   {
    "key": "random",
    "short": "r",
    "label": "Randomize"
   }
  ]
 },
 {
  "key": "miniboss",
  "category": "Gameplay",
  "short_key": "b",
  "label": "Miniboss shuffle",
  "description": "Randomizes the dungeon minibosses that each dungeon has.",
  "multiworld": true,
  "aesthetic": false,
  "default": "default",
  "options": [
   {
    "key": "default",
    "short": "",
    "label": "Normal"
   },
   {
    "key": "shuffle",
    "short": "s",
    "label": "Shuffle"
   },
   {
    "key": "random",
    "short": "r",
    "label": "Randomize"
   }
  ]
 },
 {
  "key": "enemies",
  "category": "Gameplay",
  "short_key": "e",
  "label": "Enemizer",
  "description": "Randomizes which enemies are placed.",
  "multiworld": true,
  "aesthetic": false,
  "default": "default",
  "options": [
   {
    "key": "default",
    "short": "",
    "label": "None"
   },
   {
    "key": "overworld",
    "short": "o",
    "label": "Overworld"
   }
  ]
 },
 {
  "key": "goal",
  "category": "Gameplay",
  "short_key": "G",
  "label": "Goal",
  "description": "Changes the goal of the game.\n[Vanilla] 8 instruments required to open the egg.\n[X instruments] A number of instruments required to open the egg.\n[X specific instruments] A number of specific instruments required to open the egg. The sign at Mt. Tamaranch will tell you what they are.\n[Egg already open] The egg is already open, just head for it once you have the items needed to defeat the boss.\n[Randomized instrument count] Random number of instruments required to open the egg, between 0 and 8.\n[Random short/long game] Random number of instruments required to open the egg, chosen between 0-4 and 5-8 respectively.\n[Seashell hunt] Egg will open once you collected 20 seashells. Instruments are replaced by seashells and shuffled.\n[Bingo] Generate a 5x5 bingo board with various goals. Complete one row/column or diagonal to win!\n[Double/Triple Bingo] Bingo, but need to complete multiple rows/columns/diagonals to win!\n[Bingo-25] Bingo, but need to fill the whole bingo card to win!\n[Sign Maze] Go on a long trip on the overworld sign maze to open the egg.",
  "multiworld": true,
  "aesthetic": false,
  "default": "vanilla",
  "options": [
   {
    "key": "vanilla",
    "short": "v",
    "label": "Vanilla"
   },
   {
    "key": "instruments",
    "short": "i",
    "label": "X instruments"
   },
   {
    "key": "specific",
    "short": "s",
    "label": "X specific instruments"
   },
   {
    "key": "open",
    "short": "O",
    "label": "Egg already open"
   },
   {
    "key": "open-4",
    "short": "<",
    "label": "Random short game (0-4)"
   },
   {
    "key": "5-8",
    "short": ">",
    "label": "Random long game (5-8)"
   },
   {
    "key": "seashells",
    "short": "S",
    "label": "Seashell hunt (20)"
   },
   {
    "key": "bingo",
    "short": "b",
    "label": "Bingo!"
   },
   {
    "key": "bingo-double",
    "short": "d",
    "label": "Double Bingo!"
   },
   {
    "key": "bingo-triple",
    "short": "t",
    "label": "Triple Bingo!"
   },
   {
    "key": "bingo-full",
    "short": "B",
    "label": "Bingo-25!"
   },
   {
    "key": "maze",
    "short": "m",
    "label": "Sign Maze"
   }
  ]
 },
 {
  "key": "goalcount",
  "category": "Gameplay",
  "short_key": "i",
  "label": "Goal count",
  "description": "Amount of instruments to find for the instruments goal.",
  "multiworld": true,
  "aesthetic": false,
  "default": "4",
  "options": [
   {
    "key": "7",
    "short": "7",
    "label": "7 instruments"
   },
   {
    "key": "6",
    "short": "6",
    "label": "6 instruments"
   },
   {
    "key": "5",
    "short": "5",
    "label": "5 instruments"
   },
   {
    "key": "4",
    "short": "4",
    "label": "4 instruments"
   },
   {
    "key": "3",
    "short": "3",
    "label": "3 instruments"
   },
   {
    "key": "2",
    "short": "2",
    "label": "2 instruments"
   },
   {
    "key": "1",
    "short": "1",
    "label": "1 instrument"
   },
   {
    "key": "0",
    "short": "0",
    "label": "No instruments"
   },
   {
    "key": "random",
    "short": "R",
    "label": "Random instrument count"
   }
  ],
  "visible_if": [
   "goal",
   "instruments"
  ]
 },
 {
  "key": "itempool",
  "category": "Gameplay",
  "short_key": "P",
  "label": "Item pool",
  "description": "Effects which items are shuffled.\n[Casual] Places more inventory and key items so the seed is easier.\n[More keys] Adds more small keys and extra nightmare keys so dungeons are easier.\n[Path of pain] ...just find out yourself.",
  "multiworld": true,
  "aesthetic": false,
  "default": "",
  "options": [
   {
    "key": "",
    "short": "",
    "label": "Normal"
   },
   {
    "key": "casual",
    "short": "c",
    "label": "Casual"
   },
   {
    "key": "pain",
    "short": "p",
    "label": "Path of Pain"
   },
   {
    "key": "keyup",
    "short": "k",
    "label": "More keys"
   }
  ]
 },
 {
  "key": "hpmode",
  "category": "Gameplay",
  "short_key": "m",
  "label": "Health mode",
  "description": "\n[Normal] Health works as you would expect.\n[Inverted] You start with 9 heart containers, but killing a boss will take a heart container instead of giving one.\n[Start with 1] Normal game, you just start with 1 heart instead of 3.\n[Low max] Replace heart containers with heart pieces.\n[5 Hit Challenge] You can take 5 hits before you die, no healing, no saving.",
  "multiworld": true,
  "aesthetic": false,
  "default": "default",
  "options": [
   {
    "key": "default",
    "short": "",
    "label": "Normal"
   },
   {
    "key": "inverted",
    "short": "i",
    "label": "Inverted"
   },
   {
    "key": "1",
    "short": "1",
    "label": "Start with 1 heart"
   },
   {
    "key": "low",
    "short": "l",
    "label": "Low max"
   },
   {
    "key": "5hit",
    "short": "5",
    "label": "5Hit Challenge"
   }
  ]
 },
 {
  "key": "hardmode",
  "category": "Gameplay",
  "short_key": "X",
  "label": "Hard mode",
  "description": "\n[Oracle] Less i-frames and heath from drops. Bombs damage yourself. Water damages you without flippers. No piece of power or guardian acorn drops.\n[Hero] Switch version hero mode, double damage, no heart/fairy drops.\n[One hit KO] You die on a single hit, always.",
  "multiworld": true,
  "aesthetic": false,
  "default": "none",
  "options": [
   {
    "key": "none",
    "short": "",
    "label": "Disabled"
   },
   {
    "key": "oracle",
    "short": "O",
    "label": "Oracle"
   },
   {
    "key": "hero",
    "short": "H",
    "label": "Hero"
   },
   {
    "key": "ohko",
    "short": "1",
    "label": "One hit KO"
   }
  ]
 },
 {
  "key": "steal",
  "category": "Gameplay",
  "short_key": "t",
  "label": "Stealing from the shop",
  "description": "Effects when you can steal from the shop. Stealing is bad and never in logic.\n[Normal] Requires the sword before you can steal.\n[Always] You can always steal from the shop.\n[Never] You can never steal from the shop.\n[GGS] Glitches get stitches, do not try to rob the shopkeeper by S&Q...",
  "multiworld": true,
  "aesthetic": false,
  "default": "default",
  "options": [
   {
    "key": "always",
    "short": "a",
    "label": "Always"
   },
   {
    "key": "never",
    "short": "n",
    "label": "Never"
   },
   {
    "key": "default",
    "short": "",
    "label": "Normal"
   },
   {
    "key": "ggs",
    "short": "g",
    "label": "GGS"
   }
  ]
 },
 {
  "key": "evilshop",
  "category": "Special",
  "short_key": "v",
  "label": "Evil shop",
  "description": "Replaces the grandpa house with an evil shop, where you can sell heart pieces.",
  "multiworld": true,
  "aesthetic": false,
  "default": "",
  "options": [
   {
    "key": "",
    "short": "",
    "label": "Disabled"
   },
   {
    "key": "enabled",
    "short": "e",
    "label": "Enabled"
   }
  ]
 },
 {
  "key": "bowwow",
  "category": "Special",
  "short_key": "g",
  "label": "Good boy mode",
  "description": "Allows BowWow to be taken into any area, damage bosses and more enemies. If enabled, you always start with BowWow. Swordless option removes the swords from the game and requires you to beat the game without a sword and just BowWow.",
  "multiworld": true,
  "aesthetic": false,
  "default": "normal",
  "options": [
   {
    "key": "normal",
    "short": "",
    "label": "Disabled"
   },
   {
    "key": "always",
    "short": "a",
    "label": "Enabled"
   },
   {
    "key": "swordless",
    "short": "s",
    "label": "Enabled (swordless)"
   }
  ]
 },
 {
  "key": "overworld",
  "category": "Special",
  "short_key": "O",
  "label": "Overworld",
  "description": "\n[Dungeon Dive] Create a different overworld where all the dungeons are directly accessible and almost no chests are located in the overworld.\n[No dungeons] All dungeons only consist of a boss fight and a instrument reward. Rest of the dungeon is removed.\n[Dungeon Chain] Overworld is fully removed and all dungeons are chained together.\n[Random] Creates a randomized overworld. WARNING: This will error out often during generation, work in progress.\n[ALttP] Overworld is replaced with one based on A Link to the Past. Also adds the Hammer to the item pool, along with stakes that require the hammer to remove. WARNING: Work in progress, please report any bugs!",
  "multiworld": true,
  "aesthetic": false,
  "default": "normal",
  "options": [
   {
    "key": "normal",
    "short": "",
    "label": "Normal"
   },
   {
    "key": "dungeondive",
    "short": "D",
    "label": "Dungeon dive"
   },
   {
    "key": "nodungeons",
    "short": "N",
    "label": "No dungeons"
   },
   {
    "key": "dungeonchain",
    "short": "C",
    "label": "Dungeon chain"
   },
   {
    "key": "random",
    "short": "R",
    "label": "Randomized"
   },
   {
    "key": "alttp",
    "short": "A",
    "label": "ALttP"
   }
  ]
 },
 {
  "key": "dungeonchainlength",
  "category": "Special",
  "short_key": "d",
  "label": "Chain length",
  "description": "Amount of dungeons in the dungeon chain.",
  "multiworld": true,
  "aesthetic": false,
  "default": "5",
  "options": [
   {
    "key": "3",
    "short": "3",
    "label": "3 Dungeons"
   },
   {
    "key": "4",
    "short": "4",
    "label": "4 Dungeons"
   },
   {
    "key": "5",
    "short": "5",
    "label": "5 Dungeons"
   },
   {
    "key": "6",
    "short": "6",
    "label": "6 Dungeons"
   },
   {
    "key": "7",
    "short": "7",
    "label": "7 Dungeons"
   },
   {
    "key": "8",
    "short": "8",
    "label": "8 Dungeons"
   }
  ],
  "visible_if": [
   "overworld",
   "dungeonchain"
  ]
 },
 {
  "key": "owlstatues",
  "category": "Special",
  "short_key": "o",
  "label": "Owl statues",
  "description": "Replaces the hints from owl statues with additional randomized items.",
  "multiworld": true,
  "aesthetic": false,
  "default": "",
  "options": [
   {
    "key": "",
    "short": "",
    "label": "Never"
   },
   {
    "key": "dungeon",
    "short": "D",
    "label": "In dungeons"
   },
   {
    "key": "overworld",
    "short": "O",
    "label": "On the overworld"
   },
   {
    "key": "both",
    "short": "B",
    "label": "Dungeons and Overworld"
   }
  ]
 },
 {
  "key": "keyholesanity",
  "category": "Special",
  "short_key": "K",
  "label": "Keyhole sanity",
  "description": "Makes the overworld keyholes give rewards and turns opening dungeons into findable items.",
  "multiworld": true,
  "aesthetic": false,
  "default": false
 },
 {
  "key": "shopsanity",
  "category": "Special",
  "short_key": "N",
  "label": "Shopsanity",
  "description": "\nTurns all the phone booths into extra shops, and lowers the prices, and allows buying the two shop items independent of each other.\n[Basic] Just extra shops.\n[Important] Shops are guaranteed to have important items.",
  "multiworld": true,
  "aesthetic": false,
  "default": "",
  "options": [
   {
    "key": "",
    "short": "",
    "label": "Disabled"
   },
   {
    "key": "basic",
    "short": "b",
    "label": "Basic"
   },
   {
    "key": "important",
    "short": "i",
    "label": "Important"
   }
  ]
 },
 {
  "key": "superweapons",
  "category": "Special",
  "short_key": "q",
  "label": "Enable super weapons",
  "description": "All items will be more powerful, faster, harder, bigger stronger. You name it.",
  "multiworld": true,
  "aesthetic": false,
  "default": false
 },
 {
  "key": "quickswap",
  "category": "User options",
  "short_key": "Q",
  "label": "Quickswap",
  "description": "Adds that the select button swaps with either A or B. The item is swapped with the top inventory slot. The map is not available when quickswap is enabled.",
  "multiworld": true,
  "aesthetic": true,
  "default": "none",
  "options": [
   {
    "key": "none",
    "short": "",
    "label": "Disabled"
   },
   {
    "key": "a",
    "short": "a",
    "label": "Swap A button"
   },
   {
    "key": "b",
    "short": "b",
    "label": "Swap B button"
   }
  ]
 },
 {
  "key": "textmode",
  "category": "User options",
  "short_key": "f",
  "label": "Text mode",
  "description": "[Fast] Makes text appear twice as fast.\n[No-Text] Removes all text from the game",
  "multiworld": true,
  "aesthetic": true,
  "default": "fast",
  "options": [
   {
    "key": "fast",
    "short": "",
    "label": "Fast"
   },
   {
    "key": "default",
    "short": "d",
    "label": "Normal"
   },
   {
    "key": "none",
    "short": "n",
    "label": "No-text"
   }
  ]
 },
 {
  "key": "lowhpbeep",
  "category": "User options",
  "short_key": "p",
  "label": "Low HP beeps",
  "description": "Slows or disables the low health beeping sound",
  "multiworld": true,
  "aesthetic": true,
  "default": "slow",
  "options": [
   {
    "key": "none",
    "short": "D",
    "label": "Disabled"
   },
   {
    "key": "slow",
    "short": "S",
    "label": "Slow"
   },
   {
    "key": "default",
    "short": "N",
    "label": "Normal"
   }
  ]
 },
 {
  "key": "noflash",
  "category": "User options",
  "short_key": "l",
  "label": "Remove flashing lights",
  "description": "Remove the flashing light effects from Mamu, shopkeeper and MadBatter. Useful for capture cards and people that are sensitive for these things.",
  "multiworld": true,
  "aesthetic": true,
  "default": true
 },
 {
  "key": "nagmessages",
  "category": "User options",
  "short_key": "S",
  "label": "Show nag messages",
  "description": "Enables the nag messages normally shown when touching stones and crystals.",
  "multiworld": true,
  "aesthetic": true,
  "default": false
 },
 {
  "key": "gfxmod",
  "category": "User options",
  "short_key": "c",
  "label": "Graphics",
  "description": "Generally affects at least Link's sprite, but can alter any graphics in the game.",
  "multiworld": true,
  "aesthetic": true,
  "default": "",
  "options": [
   {
    "key": "",
    "short": "",
    "label": "Default"
   },
   {
    "key": "AgesGirl.bin",
    "short": "AgesGirl.bin>",
    "label": "AgesGirl"
   },
   {
    "key": "Bowwow.bin",
    "short": "Bowwow.bin>",
    "label": "Bowwow"
   },
   {
    "key": "Bunny.bin",
    "short": "Bunny.bin>",
    "label": "Bunny"
   },
   {
    "key": "GrandmaUlrira.bin",
    "short": "GrandmaUlrira.bin>",
    "label": "GrandmaUlrira"
   },
   {
    "key": "Kirby.bin",
    "short": "Kirby.bin>",
    "label": "Kirby"
   },
   {
    "key": "Luigi.bin",
    "short": "Luigi.bin>",
    "label": "Luigi"
   },
   {
    "key": "Marin.bin",
    "short": "Marin.bin>",
    "label": "Marin"
   },
   {
    "key": "MarinAlpha.bin",
    "short": "MarinAlpha.bin>",
    "label": "MarinAlpha"
   },
   {
    "key": "Mario.bin",
    "short": "Mario.bin>",
    "label": "Mario"
   },
   {
    "key": "Martha.bin",
    "short": "Martha.bin>",
    "label": "Martha"
   },
   {
    "key": "Matty.bin",
    "short": "Matty.bin>",
    "label": "Matty"
   },
   {
    "key": "Matty_LA.png",
    "short": "Matty_LA.png>",
    "label": "Matty_LA"
   },
   {
    "key": "Meme.bin",
    "short": "Meme.bin>",
    "label": "Meme"
   },
   {
    "key": "NESLink.bin",
    "short": "NESLink.bin>",
    "label": "NESLink"
   },
   {
    "key": "Ninten.bin",
    "short": "Ninten.bin>",
    "label": "Ninten"
   },
   {
    "key": "Richard.bin",
    "short": "Richard.bin>",
    "label": "Richard"
   },
   {
    "key": "Ricky.bin",
    "short": "Ricky.bin>",
    "label": "Ricky"
   },
   {
    "key": "Rooster.bin",
    "short": "Rooster.bin>",
    "label": "Rooster"
   },
   {
    "key": "Rosa.bin",
    "short": "Rosa.bin>",
    "label": "Rosa"
   },
   {
    "key": "Saria.bin",
    "short": "Saria.bin>",
    "label": "Saria"
   },
   {
    "key": "Subrosian.bin",
    "short": "Subrosian.bin>",
    "label": "Subrosian"
   },
   {
    "key": "Tarin.bin",
    "short": "Tarin.bin>",
    "label": "Tarin"
   },
   {
    "key": "TealMelancholy.png",
    "short": "TealMelancholy.png>",
    "label": "TealMelancholy"
   },
   {
    "key": "Totally_Normal_LADX1.png",
    "short": "Totally_Normal_LADX1.png>",
    "label": "Totally_Normal_LADX1"
   },
   {
    "key": "Totally_Normal_LADX2.png",
    "short": "Totally_Normal_LADX2.png>",
    "label": "Totally_Normal_LADX2"
   },
   {
    "key": "X.bin",
    "short": "X.bin>",
    "label": "X"
   },
   {
    "key": "X.png",
    "short": "X.png>",
    "label": "X"
   },
   {
    "key": "ladx_graphics.png",
    "short": "ladx_graphics.png>",
    "label": "ladx_graphics"
   },
   {
    "key": "navi.png",
    "short": "navi.png>",
    "label": "navi"
   },
   {
    "key": "new_link_test.png",
    "short": "new_link_test.png>",
    "label": "new_link_test"
   },
   {
    "key": "ninja.png",
    "short": "ninja.png>",
    "label": "ninja"
   }
  ]
 },
 {
  "key": "follower",
  "category": "User options",
  "short_key": "x",
  "label": "Follower",
  "description": "Gives you a pet follower in the game.",
  "multiworld": true,
  "aesthetic": true,
  "default": "",
  "options": [
   {
    "key": "",
    "short": "",
    "label": "None"
   },
   {
    "key": "fox",
    "short": "f",
    "label": "Fox"
   },
   {
    "key": "navi",
    "short": "n",
    "label": "Navi"
   },
   {
    "key": "ghost",
    "short": "g",
    "label": "Ghost"
   },
   {
    "key": "yipyip",
    "short": "y",
    "label": "YipYip"
   }
  ]
 },
 {
  "key": "linkspalette",
  "category": "User options",
  "short_key": "C",
  "label": "Link's color",
  "description": "Allows you to force a certain color on Link.\n[Normal] Color of Link depends on the tunic.\n[Green/Yellow/Red/Blue] Forces Link into one of these colors.\n[?? C/D] Colors of Link are usually inverted and color depends on the area you are in.",
  "multiworld": true,
  "aesthetic": true,
  "default": "-1",
  "options": [
   {
    "key": "-1",
    "short": "-",
    "label": "Normal"
   },
   {
    "key": "0",
    "short": "0",
    "label": "Green"
   },
   {
    "key": "1",
    "short": "1",
    "label": "Yellow"
   },
   {
    "key": "2",
    "short": "2",
    "label": "Red"
   },
   {
    "key": "3",
    "short": "3",
    "label": "Blue"
   },
   {
    "key": "4",
    "short": "4",
    "label": "Inverted Red"
   },
   {
    "key": "5",
    "short": "5",
    "label": "Inverted Blue"
   },
   {
    "key": "6",
    "short": "6",
    "label": "?? C"
   },
   {
    "key": "7",
    "short": "7",
    "label": "?? D"
   }
  ]
 },
 {
  "key": "music",
  "category": "User options",
  "short_key": "M",
  "label": "Music",
  "description": "\n[Random] Randomizes overworld and dungeon music.\n[Disable] No music in the whole game.\n[Tone shifted] Tone shifts the musics, making it sound different.",
  "multiworld": true,
  "aesthetic": true,
  "default": "",
  "options": [
   {
    "key": "",
    "short": "",
    "label": "Default"
   },
   {
    "key": "random",
    "short": "r",
    "label": "Random"
   },
   {
    "key": "off",
    "short": "o",
    "label": "Disable"
   },
   {
    "key": "shifted",
    "short": "s",
    "label": "Tone shifted"
   }
  ]
 }
]
