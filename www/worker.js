"use strict";

importScripts("https://cdn.jsdelivr.net/pyodide/v0.21.3/full/pyodide.js");

async function loadPyodideAndPackages() {
    self.pyodide = await loadPyodide();
    await self.pyodide.unpackArchive(await(await fetch("ladxr.tar.gz")).arrayBuffer(), "gztar");
    self.pyladxr = self.pyodide.pyimport("main");
}
let pyodideReadyPromise = loadPyodideAndPackages();

self.onmessage = async (event) => {
    await pyodideReadyPromise;
    try {
        console.log(event.data);
        self.pyodide.FS.writeFile("/input.gbc", event.data["input.gbc"]);
        self.pyodide.FS.writeFile("/spoiler.txt", "");
        self.pyodide.runPython("import sys;import io;sys.stdout = io.StringIO();");
        self.pyladxr.main(event.data["args"]);
        var stdout = await self.pyodide.runPythonAsync("sys.stdout.getvalue()");
        var seed = "???";
        for(var line of stdout.split("\n")) {
            if (line.startsWith("Seed:"))
                seed = line.substr(5).trim();
        }

        self.postMessage({"success": true, "seed": seed, "romFilename": "LADXR_" + seed + ".gbc", "rom": pyodide.FS.readFile("/output.gbc"), "spoiler": pyodide.FS.readFile("/spoiler.txt", {"encoding": "utf8"})});
    } catch (error) {
        self.postMessage({"success": false, "message": error.message});
    }
};
