"use strict";

importScripts("https://cdn.jsdelivr.net/pyodide/v0.21.3/full/pyodide.js");

var stdout = [];
function jsprint(...args)
{
    stdout.push(args.join(" "));
    self.postMessage({type: "stdout", message: args.join(" ")});
}

async function loadPyodideAndPackages() {
    self.pyodide = await loadPyodide();
    console.log("Loading ladxr.tar.gz");
    await self.pyodide.unpackArchive(await(await fetch("ladxr.tar.gz")).arrayBuffer(), "gztar");
    self.pyodide.runPython("import js;import builtins;builtins.print = js.jsprint;");
    self.pyladxr = self.pyodide.pyimport("main");
}
let pyodideReadyPromise = loadPyodideAndPackages();

self.onmessage = async (event) => {
    await pyodideReadyPromise;
    try {
        self.pyodide.FS.writeFile("/input.gbc", event.data["input.gbc"]);
        self.pyodide.FS.writeFile("/spoiler.txt", "");
        stdout = [];
        console.log("Started randomizer:", event.data.args)
        self.pyladxr.main(["/input.gbc", "--output", "/output.gbc", "--spoilerfilename", "/spoiler.txt"].concat(event.data["args"]));
        var seed = "???";
        for(var line of stdout) {
            if (line.startsWith("Seed:"))
                seed = line.substr(5).trim();
        }
        console.log(`Randomizer finished for seed: ${seed}`)
        var ext = ".gbc";
        if (event.data.args.indexOf("--multiworld") > 0)
            ext = ".zip";
        self.postMessage({type: "done", id: event.data.id, success: true, seed: seed, romFilename: "LADXR_" + seed + ext, rom: pyodide.FS.readFile("/output.gbc"), spoiler: pyodide.FS.readFile("/spoiler.txt", {"encoding": "utf8"})});
    } catch (error) {
        self.postMessage({type: "done", id: event.data.id, success: false, message: stdout + "\n" + error.message});
    }
};
