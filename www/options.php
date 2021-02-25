<?php
$gfx_options = ['' => 'Default'];
$gfx_info = ['' => ''];
foreach(scandir("LADXR/gfx") as $gfx)
{
    if (substr($gfx, -4) == ".bin")
    {
        $gfx_options[$gfx] = substr($gfx, 0, -4);
        $gfx_info[$gfx] = trim(@file_get_contents("LADXR/gfx/".$gfx.".txt"));
    }
}
$options = [
    'Main' => [
        'seed' => ['label' => 'Seed', 'type' => 'text', 'placeholder' => 'Leave empty for random seed', 'arg' => '--seed', 'multiworld' => False,
            'tooltip' => 'For multiple people to generate the same randomization result, enter the generated seed number here.|Note, not all strings are valid seeds.'],
        'logic' => ['label' => 'Logic', 'type' => ['casual' => 'Casual', '' => 'Normal', 'hard' => 'Hard', 'glitched' => 'Glitched', 'hell' => 'Hell'], 'arg' => '--logic', 'default' => '',
            'tooltip' => 'Affects where items are allowed to be placed.|[Casual] Same as normal, except that a few more complex options are removed, like removing bushes with powder and killing enemies with powder or bombs.|[Normal] playable without using any tricks or glitches. Requires nothing to be done outside of normal item usage.|[Hard] More advanced techniques may be required, but glitches are not. Examples include tricky jumps, killing enemies with only pots and skipping keys with smart routing.|[Glitched] Advanced glitches and techniques may be required, but extremely difficult or tedious tricks are not required. Examples include Bomb Triggers, Super Jumps and Jesus Jumps.|[Hell] Obscure and hard techniques may be required. Examples include featherless jumping with boots and/or hookshot, sequential pit buffers and unclipped superjumps.'],
        'accessibility' => ['label' => 'Accessibility', 'type' => ['all' => '100% Locations', 'goal' => 'Beatable'], 'arg' => '--accessibility', 'default' => 'all',
            'tooltip' => '[100% Locations] guaranteed that every single item can be reached and gained.|[Beatable] only guarantees that the game is beatable. Certain items/chests might never be reachable.'],
        'race' => ['label' => 'Race mode', 'type' => 'check', 'default' => '', 'arg' => '--race',
            'tooltip' => 'Spoiler logs can not be generated for ROMs generated with race mode enabled, and seed generation is slightly different.', 'multiworld' => False],
        'spoilerformat' => ['label' => 'Spoiler Format', 'type' => ['none' => 'None', 'text' => 'Text', 'json' => 'JSON'], 'arg' => '--spoilerformat', 'default' => 'none', 'multiworld' => False,
            'tooltip' => 'Affects how the spoiler log is generated.|[None] No spoiler log is generated. One can still be manually dumped later.|[Text] Creates a .txt file meant for a human to read.|[JSON] Creates a .json file with a little more information and meant for a computer to read.'],
    ],
    'Items' => [
        'heartpiece' => ['label' => 'Randomize heart pieces', 'type' => 'check', 'default' => 'true', 'arg' => '--heartpiece',
            'tooltip' => 'Includes heart pieces in the item pool'],
        'seashells' => ['label' => 'Randomize hidden seashells', 'type' => 'check', 'default' => 'true', 'arg' => '--seashells',
            'tooltip' => 'Randomizes the secret sea shells hiding in the ground/trees. (chest are always randomized)'],
        'heartcontainers' => ['label' => 'Randomize heart containers', 'type' => 'check', 'default' => 'true', 'arg' => '--heartcontainers',
            'tooltip' => 'Includes boss heart container drops in the item pool'],
        'instruments' => ['label' => 'Randomize instruments', 'type' => 'check', 'default' => '', 'arg' => '--instruments',
            'tooltip' => 'Instruments are placed on random locations, dungeon goal will just contain a random item.'],
        'witch' => ['label' => 'Randomize item given by the witch', 'type' => 'check', 'default' => 'true', 'arg' => '--witch',
            'tooltip' => 'Adds both the toadstool and the reward for giving the toadstool to the witch to the item pool'],
        'boomerang' => ['label' => 'Boomerang trade', 'type' => ['default' => 'Normal', 'trade' => 'Trade', 'gift' => 'Gift'], 'default' => 'gift', 'arg' => '--boomerang',
            'tooltip' => '[Normal], requires magnifier to get the boomerang.|[Trade], allows to trade an inventory item for a random other inventory item boomerang is shuffled.|[Gift], You get a random gift of any item, and the boomerang is shuffled.'],
    ],
    'Gameplay' => [
        'keysanity' => ['label' => 'Keysanity', 'type' => 'check', 'default' => '', 'arg' => '--keysanity',
            'tooltip' => 'If enabled, dungeon keys, maps and compasses can be found anywhere. Else they will only be in their respective dungeon.'],
        'randomstart' => ['label' => 'Random start location', 'type' => 'check', 'default' => '', 'arg' => '--randomstartlocation',
            'tooltip' => 'Randomize where your starting house is located'],
        'dungeonshuffle' => ['label' => 'Dungeon shuffle', 'type' => 'check', 'default' => '', 'arg' => '--dungeonshuffle',
            'tooltip' => 'Randomizes the dungeon that each dungeon entrance leads to'],
        'boss' => ['label' => 'Boss shuffle', 'type' => ['default' => 'Normal', 'shuffle' => 'Shuffle', 'random' => 'Randomize'], 'arg' => '--boss', 'default' => 'default',
            'tooltip' => 'Randomizes the dungeon bosses that each dungeon has'],
        'miniboss' => ['label' => 'Miniboss shuffle', 'type' => ['default' => 'Normal', 'shuffle' => 'Shuffle', 'random' => 'Randomize'], 'arg' => '--miniboss', 'default' => 'default',
            'tooltip' => 'Randomizes the dungeon minibosses that each dungeon has'],
        'goal' => ['label' => 'Goal', 'type' => ['8' => '8 instruments', '7' => '7 instruments', '6' => '6 instruments', '5' => '5 instruments', '4' => '4 instruments', '3' => '3 instruments', '2' => '2 instruments', '1' => '1 instrument', '0' => 'No instruments', '-1' => 'Egg already open', 'random' => 'Random instrument count', 'seashells' => 'Seashell hunt (20)'], 'default' => '8', 'arg' => '--goal',
            'tooltip' => 'Changes the goal of the game.|[1-8 instruments], number of instruments required to open the egg.|[No instruments] open the egg without instruments, still requires the ocarina with the balled of the windfish|[Egg already open] the egg is already open, just head for it once you have the items needed to defeat the boss.|[Seashell hunt] egg will open once you collected 20 seashells. Instruments are replaced by seashells and shuffled.'],
        'pool' => ['label' => 'Item pool', 'type' => ['' => 'Normal', 'casual' => 'Casual', 'pain' => 'Path of Pain', 'keyup' => 'More keys'], 'arg' => '--pool', 'default' => '',
            'tooltip' => 'Effects which items are shuffled.|[Casual] puts in more key items so the seed is easier.|[More keys] adds more small keys and extra nightmare keys so dungeons are easier.|[Path of pain]... just find out yourself.'],
        'hpmode' => ['label' => 'Health mode', 'type' => ['default' => 'Normal', 'inverted' => 'Inverted', '1' => 'Start with 1 heart'], 'arg' => '--hpmode', 'default' => 'default',
            'tooltip' => '[Normal] health works as you would expect.|[Inverted] you start with 9 heart containers, but killing a boss will take a heartcontainer instead of giving one.|[Start with 1] normal game, you just start with 1 heart instead of 3.'],
        'hardmode' => ['label' => 'Enable oracle mode', 'type' => 'check', 'default' => '', 'arg' => '--hard-mode',
            'tooltip' => 'Less iframes and heath from drops. Bombs damage yourself. Water damages you without flippers. No piece of power or acorn.'],
        'steal' => ['label' => 'Stealing from the shop', 'type' => ['always' => 'Always', 'never' => 'Never', 'default' => 'Normal'], 'default' => 'default', 'arg' => '--steal',
            'tooltip' => 'Effects when you can steal from the shop. Stealing is bad and never in logic.|[Normal] requires the sword before you can steal.|[Always] you can always steal from the shop|[Never] you can never steal from the shop.'],
    ],
    'Special' => [
        'bowwow' => ['label' => 'Good boy mode', 'type' => ['normal' => 'Disabled', 'always' => 'Enabled', 'swordless' => 'Enabled (swordless)'], 'arg' => '--bowwow', 'default' => 'normal',
            'tooltip' => 'Allows BowWow to be taken into any area, damage bosses and more enemies. If enabled you always start with bowwow. Swordless option removes the swords from the game and requires you to beat the game without a sword and just bowwow.'],
        'overworld' => ['label' => 'Overworld', 'type' => ['normal' => 'Normal', 'dungeondive' => 'Dungeon dive'], 'arg' => '--overworld', 'default' => 'normal',
            'tooltip' => 'Switching to dungeon dive will create a different overworld where all the dungeons are directly accessible and almost no chests are located in the overworld.'],
        'owlstatues' => ['label' => 'Owl statues', 'type' => ['' => 'Never', 'dungeon' => 'In dungeons', 'overworld' => 'On the overworld', 'both' => 'Dungeons and Overworld'], 'arg' => '--owlstatues', 'default' => '',
            'tooltip' => 'Replaces the hints from owl statues with additional randomized items'],
    ],
    'User options' => [
        'quickswap' => ['label' => 'Quickswap', 'type' => ['none' => 'Disabled', 'a' => 'Swap A button', 'b' => 'Swap B button'], 'arg' => '--quickswap', 'default' => 'none',
            'tooltip' => 'Adds that the select button swaps with either A or B. The item is swapped with the top inventory slot. The map is not available when quickswap is enabled.', 'aesthetic' => True],
        'textmode' => ['label' => 'Text mode', 'type' => ['fast' => 'Fast', 'default' => 'Normal', 'none' => 'No-text'], 'arg' => '--textmode', 'default' => 'fast',
            'tooltip' => 'Fast makes text appear twice as fast.|[No-Text] removes all text from the game', 'aesthetic' => True],
        'lowhpbeep' => ['label' => 'Low HP beeps', 'type' => ['none' => 'Disabled', 'slow' => 'Slow', 'default' => 'Normal'], 'arg' => '--lowhpbeep', 'default' => 'slow',
            'tooltip' => 'Slows or disables the low health beeping sound', 'aesthetic' => True],
        'no-flash' => ['label' => 'Remove flashing lights', 'type' => 'check', 'default' => '1', 'arg' => '--remove-flashing-lights',
            'tooltip' => 'Remove the flashing light effects from Mamu, shopkeeper and MadBatter. Useful for capture cards and people that are sensitive for these things.', 'aesthetic' => True],
        'nag-messages' => ['label' => 'Show nag messages', 'type' => 'check', 'default' => '', 'arg' => '--nag-messages',
            'tooltip' => 'Enables the nag messages normally shown when touching stones and crystals', 'aesthetic' => True],
        'gfxmod' => ['label' => 'Graphics', 'type' => $gfx_options, 'arg' => '--gfxmod', 'default' => '',
            'tooltip' => 'Generally affects at least Link\'s sprite, but can alter any graphics in the game', 'aesthetic' => True],
        'linkspalette' => ['label' => "Link's color", 'type' => ['' => 'Normal', '0' => 'Green', '1' => 'Yellow', '2' => 'Red', '3' => 'Blue', '4' => '?? A', '5' => '?? B', '6' => '?? C', '7' => '?? D'], 'arg' => '--linkspalette', 'default' => '', 'aesthetic' => True,
            'tooltip' => 'Allows you to force a certain color on link.|[Normal] color of link depends on the tunic.|[Green/Yellow/Red|Blue] forces link into one of these colors.|[?? A/B/C/D] colors of link are usually inverted and color depends on the area you are in.'],
        'music' => ['label' => 'Music', 'type' => ['' => 'Default', 'random' => 'Random', 'off' => 'Disable'], 'default' => '', 'arg' => '--music',
            'tooltip' => '[Random] Randomizes overworld and dungeon music|[Disable] no music in the whole game', 'aesthetic' => True],
    ]
];
?>
