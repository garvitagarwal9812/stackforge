#!/usr/bin/env node

/**
 * Post-install check: Verify Python 3 is available.
 * This runs after `npm install stackforge` to warn users early.
 */

const { spawnSync } = require("child_process");

function checkPython() {
  const candidates = process.platform === "win32"
    ? ["python", "python3", "py -3"]
    : ["python3", "python"];

  for (const cmd of candidates) {
    try {
      const parts = cmd.split(" ");
      const result = spawnSync(parts[0], [...parts.slice(1), "--version"], {
        stdio: "pipe",
        timeout: 5000,
      });
      if (result.status === 0 && result.stdout.toString().includes("3.")) {
        console.log(`✅ StackForge: Found ${result.stdout.toString().trim()}`);
        return;
      }
    } catch (_) {
      // continue
    }
  }

  console.warn("");
  console.warn("⚠️  StackForge requires Python 3.9+ to run.");
  console.warn("   Install Python from: https://www.python.org/downloads/");
  console.warn("   After installing Python, run: stackforge");
  console.warn("");
}

checkPython();
