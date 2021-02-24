<?php
include("options.php");

$romInputPath = $_FILES["rom"]["tmp_name"];
$romOutputPath = @tempnam(sys_get_temp_dir(), "rom");
$spoilerPath = @tempnam(sys_get_temp_dir(), "spoiler");
$command = "/usr/bin/python3 main.py " . escapeshellarg($romInputPath) . " --spoilerfilename=$spoilerPath -o $romOutputPath";
foreach($options as $sec => $list)
{
    foreach($list as $key => $option)
    {
        if (isset($_POST[$key]) && $_POST[$key] != "")
        {
            if ($key === "gfxmod")
                $_POST[$key] = "gfx/" . $_POST[$key];
            if ($option['type'] === 'check')
                $command .= " ".$option['arg'];
            else
                $command .= " ".$option['arg']." ".escapeshellarg($_POST[$key]);
        }
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

if ($result === 0)
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
