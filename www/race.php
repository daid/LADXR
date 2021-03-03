<?php
include("options.php");

$now = time();
if ($now < strtotime("first sat of this month"))
    $now -= 60*60*24*15;
if (isset($_GET['next']) && $_GET['next'] == 'yes')
    $now += 60*60*24*25;
$this_month = (int)date("n", $now);
$this_year = (int)date("Y", $now);

if (isset($_FILES["rom"]))
{
    $romInputPath = $_FILES["rom"]["tmp_name"];
    $romOutputPath = @tempnam(sys_get_temp_dir(), "rom");
    $command = "/usr/bin/python3 main.py " . escapeshellarg($romInputPath) . " -o $romOutputPath";
    foreach($options as $cat => $list)
    {
        foreach($list as $key => $option)
        {
            if (isset($_POST[$key]) && $_POST[$key] != "" && isset($option['aesthetic']) && $option['aesthetic'])
            {
                if ($key == "gfxmod")
                    $_POST[$key] = "gfx/" . $_POST[$key];
                if ($option['type'] == 'check')
                    $command .= " ".$option['arg'];
                else
                    $command .= " ".$option['arg']." ".escapeshellarg($_POST[$key]);
            }
        }
    }
    $command .= " --race $this_month-$this_year";
    foreach(file(dirname(__FILE__) . "/$this_month-$this_year/options.txt") as $line)
    {
        $line = trim($line);
        if (substr($line, 0, 1) == "#")
            continue;
        $command .= " $line";
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

        $json = ['seed' => $seed, 'success' => true, 'romFilename' => 'LADXR_race.gbc', 'rom' => $romContents];

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

foreach($options as $cat => $list)
{
    $options[$cat] = array_filter($list, function($option) {
        if (!isset($option['aesthetic']) || !$option['aesthetic'])
            return false;
        return true;
    });
}
$options = array_filter($options);

$title = "LADXR: Legend Of Zelda: Links Awakening RANDOMIZER, RACE! $this_month-$this_year";
$info = <<<INFO
    <p>Join the <a href="https://discord.gg/vxufNFjg">discord</a> for details</p>
    <p>Rules:<ul>
        <li>Same rules as <a href="https://www.speedrun.com/ladx/full_game#Any_No_WWOoB">Any% (No WW/OoB)</a></li>
        <li>Glitches allowed (but not required)</li>
        <li>S&Q allowed</li>
        <li>Hard reset allowed (requires BIOS)</li>
    </ul></p>
INFO;
$action = "race.php";
include("main.template.php");
?>
