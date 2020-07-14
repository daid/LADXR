<?php
$gfx_options = ['' => 'Default'];
$gfx_info = ['' => ''];
foreach(scandir("LADXR/gfx") as $gfx)
{
    if (substr($gfx, -4) == ".bin")
    {
        $gfx_options[$gfx] = substr($gfx, 0, -4);
        $gfx_info[$gfx] = "by " . trim(file_get_contents("LADXR/gfx/".$gfx.".txt"));
    }
}
$options = [
    'seed' => ['label' => 'Seed', 'type' => 'text', 'placeholder' => 'Leave empty for random seed', 'arg' => '--seed'],
    'heartpiece' => ['label' => 'Randomize heart pieces', 'type' => 'check', 'default' => 'true', 'arg' => '--heartpiece', 'tooltip' => 'Includes heart pieces in the item pool'],
    'seashells' => ['label' => 'Randomize hidden seashells', 'type' => 'check', 'default' => 'true', 'arg' => '--seashells', 'tooltip' => 'Randomizes the secret sea shells hiding in the ground/trees. (chest are always randomized)'],
    'keysanity' => ['label' => 'Keysanity', 'type' => 'check', 'default' => '', 'arg' => '--keysanity', 'tooltip' => 'Dungeon keys, maps and compasses can be found anywhere'],
    'heartcontainers' => ['label' => 'Randomize heart containers', 'type' => 'check', 'default' => '', 'arg' => '--heartcontainers', 'tooltip' => 'Includes boss heart container drops in the item pool'],
    'witch' => ['label' => 'Randomize item given by the witch', 'type' => 'check', 'default' => 'true', 'arg' => '--witch', 'tooltip' => 'Adds both the toadstool and the reward for giving the toadstool to the witch to the item pool'],
    'owlstatues' => ['label' => 'Add items on owl statues', 'type' => ['' => 'Never', 'dungeon' => 'In dungeons', 'overworld' => 'On the overworld', 'both' => 'Dungeons and Overworld'], 'arg' => '--owlstatues', 'tooltip' => 'Replaces the hints from owl statues with additional randomized items'],
    'dungeonshuffle' => ['label' => 'Dungeon shuffle', 'type' => 'check', 'default' => '', 'arg' => '--dungeonshuffle', 'tooltip' => 'Randomizes the dungeon that each dungeon entrance leads to'],
    'boomerang' => ['label' => 'Boomerang trade', 'type' => ['default' => 'Normal (require magnifier for boomerang)', 'trade' => 'Trade: Trade is always available, boomerang is shuffled in pool', 'gift' => 'Gift: Boomerang trade guy gives you a gift, boomerang itself is shuffled in the item pool'], 'arg' => '--boomerang'],
    'bowwow' => ['label' => 'Good boy mode', 'type' => ['normal' => 'Disabled', 'always' => 'Enabled', 'swordless' => 'Enabled (swordless)'], 'arg' => '--bowwow', 'tooltip' => 'Allows BowWow to be taken into any area, damage bosses and more enemies'],
    'logic' => ['label' => 'Logic', 'type' => ['' => 'Normal', 'hard' => 'Hard', 'glitched' => 'Glitched'], 'arg' => '--logic', 'tooltip' => 'Affects where items are allowed to be placed.  See the main site linked above for details.'],
    'goal' => ['label' => 'Instruments needed to open egg', 'type' => ['8' => '8', '7' => '7', '6' => '6', '5' => '5', '4' => '4', '3' => '3', '2' => '2', '1' => '1', '0' => '0', '-1' => 'Egg already open', 'random' => 'Random'], 'arg' => '--goal'],
    'pool' => ['label' => 'Item pool', 'type' => ['' => 'Normal', 'casual' => 'Casual', 'pain' => 'Path of Pain', 'keyup' => 'More keys'], 'arg' => '--pool', 'tooltip' => 'Effects which items are shuffled. Casual mode puts in more key items so the seed is easier. More keys adds more small keys and extra nightmare keys so dungeons are easier. Path of pain... just find out yourself.'],
    'hpmode' => ['label' => 'Health mode', 'type' => ['default' => 'Normal', 'inverted' => 'Inverted, defeating bosses reduces hearts', '1' => 'Start with 1 heart'], 'arg' => '--hpmode'],
    'steal' => ['label' => 'Stealing from the shop', 'type' => ['always' => 'Always', 'never' => 'Never', 'default' => 'Normal'], 'arg' => '--steal'],
    'quickswap' => ['label' => 'Quickswap with SELECT key', 'type' => ['none' => 'Disabled', 'a' => 'Swap A button', 'b' => 'Swap B button'], 'arg' => '--quickswap', 'tooltip' => 'Adds a hidden item slot that select swaps with either A or B - think a Tetris hold piece.  The map is not available when quickswap is enabled.'],
    'textmode' => ['label' => 'Text mode', 'type' => ['fast' => 'Fast', 'default' => 'Normal', 'none' => 'No-text'], 'arg' => '--textmode', 'tooltip' => 'Fast makes text appear twice as fast, none removes all text from the game'],
    'lowhpbeep' => ['label' => 'Low HP beeps', 'type' => ['slow' => 'Slow', 'default' => 'Normal', 'none' => 'Disabled'], 'arg' => '--lowhpbeep', 'tooltip' => 'Slows or disables the low health beeping sound'],
    'nag-messages' => ['label' => 'Show nag messages', 'type' => 'check', 'default' => false, 'arg' => '--nag-messages', 'tooltip' => 'Enables the nag messages normally shown when touching stones and crystals'],
    'gfxmod' => ['label' => 'Graphics', 'type' => $gfx_options, 'arg' => '--gfxmod', 'tooltip' => 'Generally affects at least Link\'s sprite, but can alter any graphics in the game'],
    'linkspalette' => ['label' => "Link's color", 'type' => ['' => 'Normal (depending on tunic)', '0' => 'Green', '1' => 'Yellow', '2' => 'Red', '3' => 'Blue', '4' => '?? A', '5' => '?? B', '6' => '?? C', '7' => '?? D'], 'arg' => '--linkspalette'],
    'race' => ['label' => 'Race mode', 'type' => 'check', 'default' => 'false', 'arg' => '--race', 'tooltip' => 'Spoiler logs can not be generated for ROMs generated with race mode enabled'],
];

if (isset($_FILES["rom"]))
{
    $file = $_FILES["rom"]["tmp_name"];
    $command = "/usr/bin/python3 main.py " . escapeshellarg($file) . " -o " . escapeshellarg($file);
    foreach($options as $key => $option)
    {
        if (isset($_POST[$key]) && $_POST[$key] != "")
        {
            if ($key == "gfxmod")
                $_POST[$key] = "gfx/" . $_POST[$key];
            if ($option['type'] == 'check')
                $command .= " ".$option['arg'];
            else
                $command .= " ".$option['arg']." ".escapeshellarg($_POST[$key]);
        }
    }
    $command .= " 2>&1";

    if (false)
    {
        echo("<pre>"); print_r($_FILES); print_r($_POST); print_r($command);
        exit();
    }
    chdir("LADXR");
    $output = []; $result = -1;
    exec($command, $output, $result);

    if ($result == 0)
    {
        $seed = "";
        foreach($output as $line)
            if (strpos($line, "Seed:") !== false)
                $seed = trim(substr($line, 5));
        header('Content-Description: File Transfer');
        header('Content-Type: application/octet-stream');
        header('Content-Disposition: attachment; filename="LADXR_'.$seed.'.gbc"');
        header('Expires: 0');
        header('Cache-Control: must-revalidate');
        header('Pragma: public');
        header('Content-Length: ' . filesize($file));
        readfile($file);
        unlink($file);
        exit();
    }
    print("<pre>Failed:");
    print_r($command);
    print_r($output);
    print_r($result);
    exit();
}
?><html>
<head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/mini.css/3.0.1/mini-default.min.css">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>
function updateForm()
{
    var rom = document.getElementById("rom");

    if (rom.files.length < 1)
        setValidRom(false);
    else if (rom.files[0].size != 1024 * 1024)
        setValidRom(false);
    else
    {
        var reader = new FileReader();
        reader.onload = function(e)
        {
            var a = new Int8Array(e.target.result);
            if (a[0x14D] != 60) // check the header checksum, simplest check for 1.0 version
                setValidRom(false);
            else
                setValidRom(true);
        };
        reader.readAsArrayBuffer(rom.files[0]);
    }
}

function setValidRom(valid)
{
    document.getElementById("submitbutton").disabled = !valid;
    document.getElementById("romwarning").style.display = valid ? "none" : "";
}

document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById("rom").onchange = function(event) {
        updateForm();
    }
    document.getElementById("submitbutton").onclick = function(event) {
        setTimeout(1, function() {document.getElementById("submitbutton").disabled = true;});
        document.getElementById("submitbutton").value = "Working... be patient.";
        return true;
    }
    document.getElementById("form").oninput = function() {
        var data = "";
        for(var e of document.getElementById("form").elements)
        {
            if (e.name != "" && e.name != "rom")
            {
                if (e.type == 'checkbox')
                    data += "&" + encodeURIComponent(e.name) + "=" + (e.checked ? "1" : "0");
                else
                    data += "&" + encodeURIComponent(e.name) + "=" + encodeURIComponent(e.value);
            }
        }
        document.location.hash = data;
    }
    updateForm();
    for(var kv of document.location.hash.split("&"))
    {
        var kv = kv.split("=");
        if (kv.length > 1)
        {
            var e = document.getElementById(kv[0]);
            if (e.type == 'checkbox')
                e.checked = kv[1] == "1";
            else
                e.value = kv[1];
        }
    }
    var gfxinfo = document.createElement("span");
    var gfximg = document.createElement("img");
    document.getElementById("gfxmod").parentElement.appendChild(gfximg);
    document.getElementById("gfxmod").parentElement.appendChild(gfxinfo);
    document.getElementById("gfxmod").oninput = function()
    {
        if (document.getElementById("gfxmod").value != "")
            gfximg.src = "LADXR/gfx/" + document.getElementById("gfxmod").value + ".png";
        else
            gfximg.src = "";
        gfxinfo.innerHTML = gfxInfoMap[document.getElementById("gfxmod").value];
    }
    var gfxInfoMap = {};
    <?php foreach($gfx_info as $k => $v) { ?>
        gfxInfoMap["<?=$k?>"] = "<?=$v?>";
    <?php } ?>
})
</script>
<style>
div.row {
    border-style: none none solid none;
    border-color: #e0e0e0;
}
div.container {
    max-width: 1200px;
}
</style>
</head>
<body>

<div class="container">
    <form action="?" method="post" enctype="multipart/form-data" id="form">
    <fieldset>
        <legend>LADXR: Legend Of Zelda: Links Awakening RANDOMIZER, v??</legend>
        <div class="row">
        <div class="col-sm-12 col-md-6">
            <p>See: <a href="https://daid.github.io/LADXR/">main site</a> for description/details</p>
        </div>
        </div>
        <div class="row">
        <div class="col-sm-12 col-md-3">
            <label for="file-rom">Input rom:</label>
        </div>
        <div class="col-sm-12 col-md">
            <input type="file" id="rom" name="rom" style="display:none"/>
            <label for="rom" class="button">Select input ROM</label>
            <label>Requires 'Legend of Zelda, The - Link's Awakening DX (V1.0)' English version</label>
        </div>
        </div>
<?php
foreach($options as $key => $option)
{
    echo('<div class="row"');

    if(array_key_exists('tooltip', $option))
         echo('title="'.$option['tooltip']);

    echo('"><div class="col-sm-12 col-md-3">');
    echo("<label for='$key'>".$option['label'].":</label>");
    echo("</div><div class='col-sm-12 col-md'>");
    if($option['type'] == "text")
        echo("<input type='text' id='$key' name='$key' placeholder='".$option['placeholder']."'/>");
    if($option['type'] == "check")
        echo("<input type='checkbox' id='$key' name='$key' ".($option['default']?"checked=1":"")."'/>");
    if (is_array($option['type']))
    {
        echo("<select id='$key' name='$key'>");
        foreach($option['type'] as $i=>$o)
            echo("<option value='$i'>$o</option>");
        echo("</select>");
    }
    echo("</div></div id=row>");
}
?>
        <div class="row">
        <div class="col-sm-12 col-md-3">
            <div id="romwarning" class="card error">No (proper) rom selected</div>
        </div>
        <div class="col-sm-12 col-md">
            <input id="submitbutton" type="submit" value="Randomize!" disabled/> (Be patient, generation takes up to 2 minutes. Slow server)
        </div>
        </div>
    </fieldset>
    </form>
</div>

</body>
</html>
