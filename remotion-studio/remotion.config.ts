/**
 * Note: When using the Node.JS APIs, the config file
 * doesn't apply. Instead, pass options directly to the APIs.
 *
 * All configuration options: https://remotion.dev/docs/config
 */

import fs from "node:fs";
import { Config } from "@remotion/cli/config";

Config.setRspack(true);
Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
// Cloud sandbox: use its pre-installed headless Chromium (remotion.media downloads are blocked there).
// Elsewhere (Mac/Windows) Remotion downloads its own browser.
const SANDBOX_CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell";
if (fs.existsSync(SANDBOX_CHROME)) {
  Config.setBrowserExecutable(SANDBOX_CHROME);
}
