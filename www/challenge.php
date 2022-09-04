<?php

if (isset($_FILES["rom"]))
{
    $romInputPath = $_FILES["rom"]["tmp_name"];
    $romOutputPath = @tempnam(sys_get_temp_dir(), "rom");
    $password = strtolower(preg_replace("/[^A-Za-z0-9]/", '', $_POST["password"]));
    $patchFile = "LADXR-Secret/challenge/" . $password;
    $command = "/usr/bin/python3 LADXR-Secret/challenge/patcher.py " . escapeshellarg($romInputPath) . " --patch --target $romOutputPath --patchfile " . escapeshellarg($patchFile);
    $command .= " 2>&1";

    chdir("LADXR");

    $output = []; $result = -1;
    exec($command, $output, $result);
    if ($result == 0)
    {
        $romContents = base64_encode(file_get_contents($romOutputPath));

        $json = ['success' => true, 'romFilename' => 'LADXR_Challenge-$password.gbc', 'rom' => $romContents];

        header('Content-Type: application/json');
        print(json_encode($json));
        unlink($romOutputPath);
        unlink($romInputPath);
        exit();
    }

    $message = "Command:\n$command\nOutput:\n" . print_r($output, true);
    $json = ['success' => false, 'message' => $message];
    header('Content-Type: application/json');
    print(json_encode($json));
    exit();
}

$title = "LADXR: Legend Of Zelda: Links Awakening CHALLENGE!";
?>
<html>
<head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/mini.css/3.0.1/mini-default.min.css">
<link rel="stylesheet" href="style.css">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script src="script.js"></script>
</head>
<body>
    <input type="checkbox" id="generatingdialog" class="modal">
    <div>
        <div class="card">
            <h3 class="section"><span class="spinner" style="margin: 0 10 0 0"></span>Building...</h3>
            <p class="section" id="generatingtext">...</p>
        </div>
    </div>
    <input type="checkbox" id="seeddonedialog" class="modal">
    <div>
        <div class="card large">
            <label for="seeddonedialog" class="modal-close" ></label>
            <h3 class="section">Generation complete!</h3>
        </div>
    </div>
    <input type="checkbox" id="errordialog" class="modal">
    <div>
        <div class="card large">
            <label for="errordialog" class="modal-close" ></label>
            <h3 class="section">Error:</h3>
            <p class="section"><pre id="failureMessage"></pre></p>
        </div>
    </div>

    <header>
        <a class="logo"><?=$title?></a>
    </header>
    <div class="container">
        <form action="challenge.php" method="post" enctype="multipart/form-data" id="form">
        <div class="row">
            <div class="col-sm-12 col-md-6 tooltip bottom" aria-label="Requires 'Legend of Zelda, The - Link's Awakening DX (V1.0)' English version">
                <input type="file" id="rom" name="rom" style="display:none"/>
                <label style="width:100%; box-sizing: border-box; text-align: center" for="rom" class="button" id="romlabel">Select input ROM</label>
            </div>
            <div class="col-sm-12 col-md-6">
                <input style="width:100%" id="submitbutton" type="submit" value="Get ROM!" disabled/>
            </div>
        </div>
        <div class="row">
            <div class="col-sm-12 col-md-6 col-lg-4 inputcontainerparent">
                <div class="inputcontainer tooltip bottom" aria-label="Password">
                    <label for='password'>Password:</label>
                    <input type='text' id='password' name='password' placeholder='Password'/>
                </div>
            </div>
        </div>
        </form>
    </div>
</body>
</html>

