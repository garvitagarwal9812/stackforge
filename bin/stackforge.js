#!/usr/bin/env node

/**
 * StackForge CLI — npm wrapper
 * Launches the Python-based StackForge CLI via `python -m stackforge`.
 * This allows global installation via: npm install -g stackforge
 */

const { spawnSync } = require("child_process");
const path = require("path");
const fs = require("fs");

// Resolve the package root (one level up from bin/)
const packageRoot = path.resolve(__dirname, "..");

/**
 * Try to find a working Python 3 interpreter.
 * Returns the command string or null.
 */
function findPython() {
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
      if (result.status === 0) {
        const version = result.stdout.toString().trim();
        if (version.includes("3.")) {
          return cmd;
        }
      }
    } catch (_) {
      // continue
    }
  }
  return null;
}

/**
 * Check if the stackforge Python package is installed.
 */
function isStackforgeInstalled(pythonCmd) {
  const parts = pythonCmd.split(" ");
  const result = spawnSync(parts[0], [...parts.slice(1), "-m", "stackforge", "--version"], {
    stdio: "pipe",
    timeout: 10000,
  });
  return result.status === 0;
}

/**
 * Install Python dependencies from the bundled requirements.txt
 */
function installDeps(pythonCmd) {
  const requirementsPath = path.join(packageRoot, "requirements.txt");
  if (!fs.existsSync(requirementsPath)) return;

  console.log("📦 Installing StackForge Python dependencies...");
  const parts = pythonCmd.split(" ");
  const result = spawnSync(parts[0], [...parts.slice(1), "-m", "pip", "install", "-r", requirementsPath], {
    stdio: "inherit",
    timeout: 120000,
  });

  if (result.status !== 0) {
    console.error("⚠️  Failed to install Python dependencies. You may need to run:");
    console.error(`   ${pythonCmd} -m pip install -r ${requirementsPath}`);
  }
}

// ─── Main ───────────────────────────────────────────────────────────────

const pythonCmd = findPython();

if (!pythonCmd) {
  console.error("❌ Python 3.9+ is required but was not found on your system.");
  console.error("   Install Python from https://www.python.org/downloads/");
  process.exit(1);
}

// If stackforge isn't installed as a pip package, install deps from bundled requirements
if (!isStackforgeInstalled(pythonCmd)) {
  installDeps(pythonCmd);
}

// Forward all CLI arguments to the Python module
const args = process.argv.slice(2);
const parts = pythonCmd.split(" ");

const result = spawnSync(parts[0], [...parts.slice(1), "-m", "stackforge", ...args], {
  stdio: "inherit",
  cwd: process.cwd(),
  env: {
    ...process.env,
    PYTHONPATH: packageRoot + (process.env.PYTHONPATH ? path.delimiter + process.env.PYTHONPATH : ""),
  },
});

process.exit(result.status || 0);
