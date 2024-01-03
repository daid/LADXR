"use strict";

var worker;
var spoilerContent;
var romArray;
var storedRomArray;

function ID(s) { return document.getElementById(s); }

function getShareLink(data) {
    var seedProvided = !ID("seed").value == "";
    if(!seedProvided)
        ID("seed").value = data.seed;
    var hash = '#' + generateSettingsString(function(s) { return !s.aesthetic; });
    if(!seedProvided)
        ID("seed").value = "";
    var l = document.location;
    return l.origin + l.pathname + l.search + hash;
}

function getRomArray() {
    return romArray;
}

async function seedComplete(data) {
    ID("generatingdialog").checked = false;

    if (data.success)
    {
        ID("seeddonedialog").checked = true;

        var blob = new Blob([data.rom], {type: "application/octet-stream"});
        downloadRom(data.romFilename, blob);

        if (ID("seedSpan"))
            ID("seedSpan").innerText = data.seed;
        if (ID("shareseed")) {
            ID("shareseed").value = getShareLink(data);
        }

        spoilerContent = data.spoiler

        if (ID("spoilerButton")) {
            if (spoilerContent)
                ID("spoilerButton").style.display = '';
            else
                ID("spoilerButton").style.display = 'none';
        }

        if (ID("magpieLink")) {
            ID("magpieLink").href = `https://magpietracker.us/?shortString=${encodeURIComponent(document.location.hash)}`;
        }
    }
    else
    {
        ID("errordialog").checked = true;
        if (data.message)
            ID("failureMessage").innerText = data.message;
        else if (typeof data === "string")
            ID("failureMessage").innerText = data;
        else
            ID("failureMessage").innerText = JSON.stringify(data, null, 4);
    }
}

function seedStdout(message)
{
    console.log(message);
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
    var seed = ID("seedSpan").innerText;
    var fileExtension = ID("spoilerformat").value === "text" ? ".txt" : ".json";

    var element = document.createElement('a');
    element.href = 'data:text/plain;charset=utf-8,' + encodeURIComponent(spoilerContent);
    element.download = "LADXR_" + seed + fileExtension;
    element.click();
}

function randomGenerationString()
{
    if (Math.random() < 0.8)
    {
        var items = ["Power bracelet", "Shield", "Bow", "Hookshot", "Magic Rod", "Pegasus Boots", "Ocarina", "Feather", "Shovel", "Magic Powder", "Bomb", "Sword", "Flippers", "Medicine", "Tail Key", "Angler Key", "Face Key", "Bird Key", "Slime Key", "Gold Leaf", "Rupees", "Seashell", "Message", "Gel", "Boomerang", "Heart Piece", "Bowwow", "Arrows", "Single Arrow", "Max Powder Upgrade", "Max Bombs Upgrade", "Max Arrows Upgrade", "Red Tunic", "Blue Tunic", "Heart Container", "Toadstool", "Small Key", "Nightmare Key", "Map", "Compass", "Stone Beak", "Instrument"];
        var item = items[Math.floor(Math.random() * items.length)];
        var prefixes = ["Placing", "Considering", "Shuffling", "Moving", "Randomizing", "Hiding"];
        var prefix = prefixes[Math.floor(Math.random() * prefixes.length)];
        ID("generatingtext").innerText = prefix + " " + item;
    } else {
        ID("generatingtext").innerText = "Shuffling D" + Math.floor(Math.random() * 8);
    }
    if (ID("generatingdialog").checked)
        setTimeout(randomGenerationString, 1000);
}

function updateGfxModImage() {
    if (!ID('gfxmod')) return;
    var gfxmod = ID('gfxmod').value
    if (gfxmod && gfxmod != 'custom') {
        var url = 'LADXR/gfx/' + gfxmod + '.png';
        ID('gfxmodimg').src = url;
    } else {
        ID('gfxmodimg').src = '';
    }
}

function updateSettingsString(filter_function) {
    var sss = generateSettingsString(filter_function);
    document.location.hash = sss;
    return sss;
}

function generateSettingsString(filter_function) {
    var sss = "";
    for(var s of options) {
        if (filter_function && typeof filter_function === 'function' && !filter_function(s)) continue;
        var e = ID(s.key);
        if (!e || s.short_key === undefined) continue;
        if (typeof(s.default) == 'boolean') {
            if (e.value == "true") sss += s.short_key;
        } else if (s.options) {
            if (s.default != e.value) {
                for(var o of s.options) { if (o.key == e.value) { sss += s.short_key + o.short; } }
            }
        } else if (s.default != e.value) {
            sss += s.short_key + e.value + ">";
        }
        if(s.key == 'seed' || (s.default == e.value || (s.default && e.value=='true') || (!s.default && e.value=='false'))) {
            e.style['font-weight'] = 'normal'
        } else {
            e.style['font-weight'] = 'bold'
        }
    }
    return sss;
}

function loadSettingsString() {
    var sss = decodeURI(document.location.hash);
    if (!sss.startsWith("#")) return;
    loadShortSettingsString(sss.substr(1));
}

function loadShortSettingsString(sss)
{
    console.log("Loading " + sss);
    for(var s of options) {
        var e = ID(s.key);
        if (!e) continue;
        if (typeof(s.default) == 'boolean') e.value = false;
    }

    var idx = 0;
    while(idx < sss.length) {
        var key = sss[idx];
        idx += 1;
        for(var s of options) {
            var e = ID(s.key);
            if (s.short_key != key) continue;
            if (typeof(s.default) == 'boolean') {
                if (e) e.value = true;
            } else if (s.options) {
                for(var o of s.options) {
                    if (o.key != s.default && sss.substr(idx).startsWith(o.short)) {
                        if (e) e.value = o.key;
                        idx += o.short.length;
                        break;
                    }
                }
            } else {
                var end = sss.indexOf(">", idx);
                if (e) e.value = sss.substr(idx, end - idx);
                idx = end + 1;
            }
        }
    }
}

function buildUI(filter_function) {
    var last_cat = "";
    var html = "";
    for(var s of options) {
        if (filter_function && !filter_function(s)) continue;
        if (last_cat != s.category) {
            if (last_cat != "") html += `</div>`;
            html += `<div class="row"><div class="col-sm-12"><h1>${s.category}</h1></div>`
            last_cat = s.category;
        }
        html += `<div class="col-sm-12 col-md-6 col-lg-4 inputcontainerparent">`;
        html += `<div class="inputcontainer tooltip bottom" aria-label="${s.description.trim()}">`;
        html += `<label for='${s.key}'>${s.label}:</label>`;
        var opts = s.options
        if (typeof(s.default) == 'boolean') {
            opts = [{key: true, label: "Yes"}, {key: false, label: "No"}]
        }
        if (opts) {
            if (s.key == 'gfxmod') {
                html += '<input type="file" name="customgfxfile" id="customgfxfile" style="display: none">';
                html += '<img id="gfxmodimg">';
            }
            html += `<select id='${s.key}' name='${s.key}'>`;
            for(var o of opts) {
                html += `<option value='${o.key}' ${s.default==o.key?"selected":""}>${o.label}</option>`;
            }
            if (s.key == 'gfxmod') {
                html += `<option value='custom'>Custom...</option>`;
            }
            html += `</select>`;
        } else {
            html += `<input id='${s.key}' name='${s.key}' placeholder='${s.placeholder?s.placeholder:""}'>`;
        }
        html += `</div></div>`;
    }
    html += `</div>`;
    ID("settings").innerHTML += html;
    loadSettingsString();
    for(var s of options) {
        if (ID(s.key)) {
            ID(s.key).oninput = updateSettingsString;
            if (s.key == 'gfxmod') ID(s.key).oninput = function(e) {
                if (ID('gfxmod').value == 'custom') ID('customgfxfile').click();
                updateGfxModImage();
                updateSettingsString();
            };
        }
    }
    updateGfxModImage();
    updateSettingsString();
    checkStoredRom();
    if (!storedRomArray) updateForm();

    ID("rom").onchange = updateForm

    ID("submitbutton").onclick = startRomGeneration;
}

function checkStoredRom()
{
    try
    {
        var storedRom = localStorage.getItem("ladx_rom");
        if (storedRom)
        {
            var bin = atob(storedRom);
            var array = new Uint8Array(bin.length);
            for (var k = 0; k < bin.length; k++)
            {
                array[k] = bin.charCodeAt(k);
            }
            if (getRomChecksum(array) == 89122269)
            {
                romArray = array;
                storedRomArray = array;
                setValidRom(true, "ROM has been loaded");
            }
            else
            {
                localStorage.removeItem("ladx_rom");
            }
        }
    }
    catch(e)
    {
        console.log("Error while loading stored ROM:")
        console.log(e);
    }
}

function updateForm()
{
    romArray = storedRomArray;

    var rom = ID("rom");

    if (rom.files.length < 1)
    {
        setValidRom(false);
    }
    else if (rom.files[0].size != 1024 * 1024)
    {
        var ext = rom.files[0].name.substr(rom.files[0].name.lastIndexOf(".")).toUpperCase();
        if (ext == ".ZIP")
            setValidRom(false, "Rom needs to be unzipped.");
        else
            setValidRom(false, "Invalid ROM size, needs to be 1048576 bytes.");
    }
    else
    {
        rom.files[0].arrayBuffer().then(function(buffer) {
            var a = new Uint8Array(buffer);
            var checksum = getRomChecksum(a);
            console.log("Checksum: " + rom.files[0].name + ": " + checksum);
            if (checksum != 89122269)
            {
                if (checksum == 89139089)
                    setValidRom(false, "Supplied English 1.1 instead of 1.0");
                else if (checksum == 89653611)
                    setValidRom(false, "Supplied English 1.2 instead of 1.0");
                else if (checksum == 89199617 || checksum == 89757956)
                    setValidRom(false, "Supplied French instead of English version");
                else if (checksum == 89992511 || checksum == 90082342)
                    setValidRom(false, "Supplied German instead of English version");
                else if (checksum == 87464316 || checksum == 87479931 || checksum == 87503721)
                    setValidRom(false, "Supplied Japanese instead of English version");
                else
                    setValidRom(false, "Invalid ROM");
            }
            else
            {
                romArray = a;
                setValidRom(true);
                try
                {
                    var s = "";
                    for(var b of a) { s += String.fromCharCode(b); }
                    localStorage.setItem("ladx_rom", btoa(s));
                }
                catch(e)
                {
                    console.log("Error while storing ROM:")
                    console.log(e);
                }
            }
        });
    }
}

function setValidRom(valid, msg)
{
    ID("submitbutton").disabled = !valid && !storedRomArray;
    if (valid)
        ID("romlabel").classList.remove("selectromwarning");
    else
        ID("romlabel").classList.add("selectromwarning");
    if (msg)
        ID("romlabel").innerHTML = msg;
    else
        ID("romlabel").innerHTML = "Select input ROM";
}

function getRomChecksum(array)
{
    var checksum = 0;
    for(var b of array) { checksum += b; }
    return checksum;
}

async function startRomGeneration()
{
    ID("generatingdialog").checked = true;
    randomGenerationString();
    var args = ["--short", updateSettingsString()];
    var data = {"input.gbc": romArray, "args": args, "id": 0};
    var e = ID("spoilerformat");
    if (e && e.value != 'none') {
        args.push("--spoilerformat");
        args.push(e.value);
    }

    e = ID("plan");
    if (e && e.value != "") {
        args.push("--plan");
        args.push('/plan.txt');
        data['plan.txt'] = new Uint8Array(await e.files[0].arrayBuffer());
    }
    e = ID("gfxmod")
    if (e.value == "custom" && ID('customgfxfile').value) {
        args.push("-s");
        args.push("gfxmod=custom.png");
        data['gfx.png'] =  new Uint8Array(await ID("customgfxfile").files[0].arrayBuffer());
    }

    await postToWorker(data);
}

async function postToWorker(data)
{
    if (!worker) {
        worker = new Worker("js/worker.js");
        worker.onmessage = function(event) {
            if (event.data.type == "done")
                seedComplete(event.data);
            else if (event.data.type == "stdout")
                seedStdout(event.data.message);
            else
                console.log(event.data);
        }
        worker.onerror = console.log;
    }
    worker.postMessage(data);
}

