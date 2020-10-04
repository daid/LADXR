<?php
include("options.php");

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
