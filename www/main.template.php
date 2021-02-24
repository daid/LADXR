<html>
<head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/mini.css/3.0.1/mini-default.min.css">
<link rel="stylesheet" href="style.css">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script>
var gfxInfoMap = <?=json_encode($gfx_info)?>
</script>
<script src="script.js"></script>
</head>
<body>
    <input type="checkbox" id="generatingdialog" class="modal">
    <div>
        <div class="card">
            <h3 class="section"><span class="spinner" style="margin: 0 10 0 0"></span>Randomizing...</h3>
            <p class="section" id="generatingtext">...</p>
        </div>
    </div>
    <input type="checkbox" id="seeddonedialog" class="modal">
    <div>
        <div class="card large">
            <label for="seeddonedialog" class="modal-close" ></label>
            <h3 class="section">Seed generation complete!</h3>
            <p class="section">Seed: <span id="seedSpan">...</span></p>
            <p class="section"><button id="spoilerButton" class="primary large" onclick="downloadSpoilers()">Download Spoiler Log</button></p>
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
        <form action="<?=$action?>?<?=http_build_query($_GET)?>" method="post" enctype="multipart/form-data" id="form">
        <div class="row">
            <div class="col-sm-12 col-md-6 tooltip bottom" aria-label="Requires 'Legend of Zelda, The - Link's Awakening DX (V1.0)' English version">
                <input type="file" id="rom" name="rom" style="display:none"/>
                <label style="width:100%; box-sizing: border-box; text-align: center" for="rom" class="button" id="romlabel">Select input ROM</label>
            </div>
            <div class="col-sm-12 col-md-6 tooltip bottom" aria-label="(Be patient, generation takes up to 2 minutes. Slow server)">
                <input style="width:100%" id="submitbutton" type="submit" value="Randomize!" disabled/>
            </div>
        </div>
        <?php if (isset($info)) { ?>
        <div class="row"><div class="col-sm-12"><?=$info?></div></div>
        <?php } ?>
<?php
foreach($options as $cat => $list)
{
    ?><div class="row"><div class="col-sm-12"><h1><?=$cat?></h1></div><?php
    foreach($list as $key => $option)
    {
        $type = $option['type'];
        if($type === "check")
            $type = ['1' => "Yes", '' => "No"];

        ?><div class="col-sm-12 col-md-6 col-lg-4 inputcontainerparent">
            <div class="inputcontainer tooltip bottom" aria-label="<?=str_replace("|", "&#10;", $option['tooltip'])?>"><?php
        ?><label for='<?=$key?>'><?=$option['label']?>:</label><?php
        if($type === "text")
        {
            ?><input type='text' id='<?=$key?>' name='<?=$key?>' placeholder='<?=$option['placeholder']?>'/><?php
        }
        if (is_array($type)) {
            $default = $option['default'];
            ?><select id='<?=$key?>' name='<?=$key?>'><?php
            foreach($type as $i=>$o) {
                if ($i === $default) {
                    ?><option value='<?=$i?>' selected><?=$o?></option><?php
                } else {
                    ?><option value='<?=$i?>'><?=$o?></option><?php
                }
            }
            ?></select><?php
        }
        ?></div></div><?php
    }
    ?></div><?php
}
?>
        </div>
    </form>
    </div>
</body>
</html>
