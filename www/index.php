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
    'bossshuffle' => ['label' => 'Boss shuffle', 'type' => 'check', 'default' => '', 'arg' => '--bossshuffle', 'tooltip' => 'Randomizes the dungeon bosses that each dungeon has'],
    'boomerang' => ['label' => 'Boomerang trade', 'type' => ['default' => 'Normal (require magnifier for boomerang)', 'trade' => 'Trade: Trade is always available, boomerang is shuffled in pool', 'gift' => 'Gift: Boomerang trade guy gives you a gift, boomerang itself is shuffled in the item pool'], 'arg' => '--boomerang'],
    'bowwow' => ['label' => 'Good boy mode', 'type' => ['normal' => 'Disabled', 'always' => 'Enabled', 'swordless' => 'Enabled (swordless)'], 'arg' => '--bowwow', 'tooltip' => 'Allows BowWow to be taken into any area, damage bosses and more enemies'],
    'logic' => ['label' => 'Logic', 'type' => ['' => 'Normal', 'hard' => 'Hard', 'glitched' => 'Glitched'], 'arg' => '--logic', 'tooltip' => 'Affects where items are allowed to be placed.  See the main site linked above for details.'],
    'goal' => ['label' => 'Instruments needed to open egg', 'type' => ['8' => '8', '7' => '7', '6' => '6', '5' => '5', '4' => '4', '3' => '3', '2' => '2', '1' => '1', '0' => '0', '-1' => 'Egg already open', 'random' => 'Random'], 'arg' => '--goal'],
    'pool' => ['label' => 'Item pool', 'type' => ['' => 'Normal', 'casual' => 'Casual', 'pain' => 'Path of Pain', 'keyup' => 'More keys'], 'arg' => '--pool', 'tooltip' => 'Effects which items are shuffled. Casual mode puts in more key items so the seed is easier. More keys adds more small keys and extra nightmare keys so dungeons are easier. Path of pain... just find out yourself.'],
    'hpmode' => ['label' => 'Health mode', 'type' => ['default' => 'Normal', 'inverted' => 'Inverted, defeating bosses reduces hearts', '1' => 'Start with 1 heart'], 'arg' => '--hpmode'],
    'hardmode' => ['label' => 'Enable oracle mode:', 'type' => 'check', 'default' => false, 'arg' => '--hard-mode', 'tooltip' => 'Less iframes and heath from drops. Also bombs damage yourself.'],
    'steal' => ['label' => 'Stealing from the shop', 'type' => ['always' => 'Always', 'never' => 'Never', 'default' => 'Normal'], 'arg' => '--steal'],
    'quickswap' => ['label' => 'Quickswap with SELECT key', 'type' => ['none' => 'Disabled', 'a' => 'Swap A button', 'b' => 'Swap B button'], 'arg' => '--quickswap', 'tooltip' => 'Adds a hidden item slot that select swaps with either A or B - think a Tetris hold piece.  The map is not available when quickswap is enabled.'],
    'textmode' => ['label' => 'Text mode', 'type' => ['fast' => 'Fast', 'default' => 'Normal', 'none' => 'No-text'], 'arg' => '--textmode', 'tooltip' => 'Fast makes text appear twice as fast, none removes all text from the game'],
    'lowhpbeep' => ['label' => 'Low HP beeps', 'type' => ['slow' => 'Slow', 'default' => 'Normal', 'none' => 'Disabled'], 'arg' => '--lowhpbeep', 'tooltip' => 'Slows or disables the low health beeping sound'],
    'nag-messages' => ['label' => 'Show nag messages', 'type' => 'check', 'default' => false, 'arg' => '--nag-messages', 'tooltip' => 'Enables the nag messages normally shown when touching stones and crystals'],
    'gfxmod' => ['label' => 'Graphics', 'type' => $gfx_options, 'arg' => '--gfxmod', 'tooltip' => 'Generally affects at least Link\'s sprite, but can alter any graphics in the game'],
    'linkspalette' => ['label' => "Link's color", 'type' => ['' => 'Normal (depending on tunic)', '0' => 'Green', '1' => 'Yellow', '2' => 'Red', '3' => 'Blue', '4' => '?? A', '5' => '?? B', '6' => '?? C', '7' => '?? D'], 'arg' => '--linkspalette'],
    'race' => ['label' => 'Race mode', 'type' => 'check', 'default' => false, 'arg' => '--race', 'tooltip' => 'Spoiler logs can not be generated for ROMs generated with race mode enabled'],
    'spoilerformat' => ['label' => 'Spoiler Format', 'type' => ['none' => 'None', 'text' => 'Text', 'json' => 'JSON'], 'arg' => '--spoilerformat'],
];

if (isset($_FILES["rom"]))
{
    $romInputPath = $_FILES["rom"]["tmp_name"];
    $romOutputPath = @tempnam(sys_get_temp_dir(), "rom");
    $spoilerPath = @tempnam(sys_get_temp_dir(), "spoiler");
    $command = "/usr/bin/python3 main.py " . escapeshellarg($romInputPath) . " --spoilerfilename=$spoilerPath -o $romOutputPath";
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

        $romContents = base64_encode(file_get_contents($romOutputPath));
        $spoilerContents = file_get_contents($spoilerPath);

        $json = ['success' => true, 'seed' => $seed, 'romFilename' => 'LADXR_'.$seed.'.gbc', 'rom' => $romContents, 'spoiler' => $spoilerContents];

        header('Content-Type: application/json');
        print(json_encode($json));
        unlink($romOutputPath);
        unlink($spoilerPath);
        unlink($romInputPath);
        exit();
    }

    $message = "Command:\n$command\nOutput:\n" . print_r($output, true);
    $json = ['success' => false, 'message' => $message];
    header('Content-Type: application/json');
    print(json_encode($json));
    exit();
}
?><html>
<head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/mini.css/3.0.1/mini-default.min.css">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
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
        $("#seedSpinner").attr('style', '');
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

function b64toBlob(b64Data, contentType='', sliceSize=512)
{
    const byteCharacters = atob(b64Data);
    const byteArrays = [];

    for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
        const slice = byteCharacters.slice(offset, offset + sliceSize);

        const byteNumbers = new Array(slice.length);
        for (let i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
        }

        const byteArray = new Uint8Array(byteNumbers);
        byteArrays.push(byteArray);
    }

    const blob = new Blob(byteArrays, {type: contentType});
    return blob;
}

function downloadRom(filename, blob)
{
    var element = document.createElement('a');
    element.href = window.URL.createObjectURL(blob);
    element.download = filename;
    element.click();
}

function downloadSpoilers()
{
    var spoilerContent = $("#spoilerContent").html();
    var seed = $("#seedSpan").html();
    var fileExtension = $("#spoilerformat").val() === "text" ? ".txt" : ".json";

    var element = document.createElement('a');
    element.href = 'data:text/plain;charset=utf-8,' + encodeURIComponent(spoilerContent);
    element.download = "LADXR_" + seed + fileExtension;
    element.click();
}

function seedComplete(data)
{
    $('#submitbutton').attr('value', "Randomize!");
    $('#seedSpinner').attr('style', 'display: none;');

    if (data.success)
    {
        $('#errorCard').attr('style', 'display: none;');
        $('#successCard').attr('style', '');
        $('#seedSpan').html(data.seed);

        if ($("#spoilerformat").val() !== "none")
        {
            $('#spoilerBox').attr('style', '');
            $('#spoilerButton').attr('style', '');
            $('#spoilerContent').html(data.spoiler);
        }
        else
        {
            $('#spoilerBox').attr('style', 'display: none;');
            $('#spoilerButton').attr('style', 'display: none;');
        }
    }
    else
    {
        $('#successCard').attr('style', 'display: none;');
        $('#failureCard').attr('style', '');
        $('#failureMessage').html(data.message);
    }
}
</script>
<style>
div.row {
    border-style: none none solid none;
    border-color: #e0e0e0;
}
div.container {
    max-width: 1200px;
}

div.spinner {
    float: right;
    margin-top: 15px; /* Ugly attempt at centering the spinner vertically */
}

div.card {
    max-width: 100%;
}

div.success {
    background-color: #d9f0d1;
}

div.failure {
    background-color: #ffccd7;
}
</style>
</head>
<body>

<div class="container">
    <div id="successCard" class="card success" style="display: none;">
        <h2>Seed generation complete!<small>Seed: <span id="seedSpan"></span></small></h2>
        <button id="spoilerButton" class="primary large" onclick="downloadSpoilers()">Download Spoiler Log</button>
        <div id="spoilerBox" class="collapse" style="display: none;">
            <input type="checkbox" id="spoiler-collapse" aria-hidden="true">
            <label for="spoiler-collapse" aria-hidden="true">Spoilers</label>
            <div>
                <pre id="spoilerContent"></pre>
            </div>
        </div>
    </div>
    <div id="failureCard" class="card failure" style="display: none;">
        <h2>Error:</h2>
        <pre id="failureMessage"></pre>
    </div>
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
            <div id="romwarning" class="card error">No (proper) rom selected</div>
            <div id="seedSpinner" class="spinner" style="display: none;"></div>
        </div>
        <div class="col-sm-12 col-md">
            <input id="submitbutton" type="submit" value="Randomize!" disabled/> (Be patient, generation takes up to 2 minutes. Slow server)
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
    </fieldset>
    </form>
</div>

<script>
$("#form").submit(function(e) {
    e.preventDefault();

    var form = $(this);
    var url = form.attr('action');
    var formData = new FormData(form[0]);

    $.ajax({
        type: "POST",
        url: url,
        data: formData,
        contentType: false,
        processData: false,
        success: function(data)
        {
            if(data.success)
            {
                blob = b64toBlob(data.rom, "application/octet-stream");
                downloadRom(data.romFilename, blob);
            }

            seedComplete(data);
        },
        error: function(data)
        {
            var result = {success: false, message: data};
            seedComplete(result);
        }
        });
});
</script>

</body>
</html>
