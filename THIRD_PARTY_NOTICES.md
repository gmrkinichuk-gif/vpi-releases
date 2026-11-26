# Third-party notices

This file lists materials in, or used by, Vehicle Performance Index (VPI) that belong to someone other than the VPI author. The [VPI licence](LICENSE) does not cover them, and the VPI author claims no rights in them. Each is used under its owner's terms.

Last audit: 26 November 2026, VPI source tree for game client EU 2.4.2.0.

## 1. Shipped inside VPI release artifacts

### 1.1 Wargaming game client files, in modified form

`vpi-native-ui_<version>.wotmod`, and the installer that embeds it, contain copies of these World of Tanks EU client files with VPI code added. The build reads each file from the player's or builder's installed client, checks its SHA-256 against `native/ui_patch.json`, and inserts VPI fragments at fixed points:

| Client package | File |
| --- | --- |
| `gui-part4.pkg` | `gui/gameface/_dist/production/battle/battle_page/TabView/TabView.js` |
| `gui-part3.pkg` | `gui/gameface/_dist/production/battle/battle_page/TabView/TabView.css` |
| `gui-part4.pkg` | `gui/gameface/_dist/production/mono/hangar/main/main.html` |
| `gui-part2.pkg` | `gui/gameface/_dist/production/mono/post_battle/random/bundle.js` |
| `gui-part3.pkg` | `gui/gameface/_dist/production/mono/post_battle/random/random.css` |
| `gui-part3.pkg` | `gui/gameface/_dist/production/chunks/lobby/6bcda3547d182fc3c171.js` |
| `gui-part3.pkg` | `gui/gameface/_dist/production/chunks/lobby/6bcda3547d182fc3c171.css` |
| `gui-part1.pkg` | `gui/flash/battleVehicleMarkers.swf` |
| `gui-part4.pkg` | `gui/flash/messengerControls.swf` |

- **Owner:** Wargaming Group Limited and its affiliates.
- **Terms:** [Wargaming EULA](https://legal.wargaming.net/en/user-documents/eula/end-user-license-agreement/view/) and [Player Content Policy](https://legal.wargaming.net/en/user-documents/content-policies/player-content-policy/view). The Player Content Policy (section 1.4) allows players to "create and make available modifications for our games, subject to the EULA". Wargaming keeps all rights in its files (EULA 6.3, Player Content Policy 3.1).
- Only the inserted VPI fragments (`native/*.fragment`, `native/*.css`, `native/hangar.js`, and the AVM2 bytecode from `native/*/src`) are the VPI author's work.
- VPI is distributed free of charge, in line with the Policy's ban on commercial use of Wargaming IP (section 2.1).

### 1.2 Crosshairs API: not shipped, integrated locally

Crosshairs API is an independent third-party mod. VPI does not include its code, and the [VPI licence](LICENSE) does not cover it.

- No VPI release artifact contains a file from a Crosshairs API package, original or modified. `tools/audit_release.py` checks every release ZIP and EXE for this, the build runs it automatically, and the tests cover it.
- When a supported Crosshairs API package (`meta.xml` id `crosshairs_api_1.3`) is installed, the VPI installer reads that package's hangar page on the player's computer and writes a local copy to `res_mods/<client>/gui/gameface/_dist/production/mono/hangar/main/main.html`. The copy has two added lines that load VPI's own `vpi.js` and `vpi.css`. The Crosshairs API package is not changed. Its code and notices stay as they are.
- The installer records the SHA-256 of that copy in `mods/configs/vpi-index/install-state.json`. It replaces or removes a loose hangar page only if VPI wrote it, and it never overwrites a page from another source.
- VPI releases up to 1.0.4 shipped such a page in some ZIP and EXE files. Those files are withdrawn and are not used for further public distribution.

### 1.3 Data derived from the game client

`VPI-Server.zip` contains `vehicle-roles.json`, a table of vehicle IDs and their role tags. The build reads it from `scripts/item_defs/vehicles/*/list.xml` in the client's `scripts.pkg`.

- **Owner:** Wargaming. **Terms:** Wargaming EULA.

### 1.4 Wargaming Public API data (private builds only)

Private builds made with `--catalog-seed` can include `vehicle-catalog.seed.json`, a snapshot of `encyclopedia/vehicles` from the Wargaming Public API. Public builds refuse this option.

- **Owner:** Wargaming. **Terms:** [Wargaming Public API terms](https://developers.wargaming.net/documentation/rules/agreement/). See `docs/FAIR-PLAY.md`.

### 1.5 Names and trademarks

VPI shows Wargaming names, such as "World of Tanks", "WTR", vehicle names and game terms, to describe compatibility and data. These are trademarks or materials of Wargaming, used only to refer to Wargaming's game.

## 2. Used at run time, not shipped

| Component | Owner | How VPI uses it |
| --- | --- | --- |
| World of Tanks client, its Python 2.7 runtime and game modules (`BigWorld`, `gui`, `helpers` and others) | Wargaming (Python runtime: Python Software Foundation) | The mod runs inside the game and imports its modules. Nothing is copied. |
| Game icons and images, such as `coui://gui/maps/icons/...` | Wargaming | Loaded from the installed client by reference. |
| Game fonts | Wargaming and their licensors | Used through the game UI. VPI ships no fonts. |
| Wargaming Public API (`api.worldoftanks.eu`) | Wargaming | Statistics requests, under the [API terms](https://developers.wargaming.net/documentation/rules/agreement/). |
| .NET Framework 4.x (`System.*` assemblies) | Microsoft | The installer runs on the copy that comes with Windows. No assemblies are bundled. |

## 3. Server deployment, obtained by the operator

`VPI-Server.zip` contains only VPI files and the data in section 1.3. When deployed, Docker downloads these components from their publishers. They are not part of the VPI release.

| Component | Licence |
| --- | --- |
| Docker image `python:3.12-slim-trixie` (Python 3.12 on Debian) | Python: [PSF License](https://docs.python.org/3/license.html). Debian packages: their own licences. |
| `curl`, installed in that image from Debian | [curl licence](https://curl.se/docs/copyright.html) |
| Docker image `caddy:2` | [Apache License 2.0](https://github.com/caddyserver/caddy/blob/master/LICENSE) |
| Docker Engine and Docker Compose | Apache License 2.0 |
| TLS certificates that Caddy obtains automatically (Let's Encrypt or ZeroSSL) | Terms of the certificate authority, accepted by the operator |

## 4. Build and test tools, not shipped

These tools are used to build or test VPI. Their output contains only VPI code and the materials listed in section 1. Their code is not included.

| Tool | Licence | Use |
| --- | --- | --- |
| Python 3 (build scripts) | PSF License | Runs the build. |
| `python27.dll` from the installed game client | Wargaming (Python: PSF License) | Compiles the mod's Python 2.7 bytecode. The DLL is not copied. |
| [Pillow](https://github.com/python-pillow/Pillow) | MIT-CMU (HPND) licence | Generates textures and the installer icon. |
| [Apache Royale](https://royale.apache.org/) compiler (`mxmlc.jar`) | Apache License 2.0 | Compiles `native/*/src` to AVM2 bytecode. Only VPI classes go into the `.abc` files. The stubs in `native/*/stubs` are excluded (`-externs`). |
| `playerglobal.swc` | Adobe | Compile-time API definitions, linked externally. Not included in any output. |
| Java runtime | Its distributor's licence | Runs the Royale compiler. |
| .NET Framework C# compiler (`csc.exe`) | Microsoft | Compiles the installer. |
| GitHub Actions (`actions/checkout`, `actions/setup-python`) | MIT | Runs the unit tests in CI. |

The ActionScript stubs in `native/markers/stubs` and `native/contacts/stubs` are short declarations written by the VPI author. They mirror the names of game classes so the compiler can resolve them. They contain no Wargaming code and are not compiled into the output.

## 5. Referenced only

`docs/MODEL.md` compares VPI with WN8, WNX and WTR and links to their public descriptions. VPI contains no code, expected-value tables or other material from those ratings.

## 6. Not found

No bundled third-party Python, JavaScript or .NET libraries, no fonts, and no third-party images were found in the VPI source or release artifacts. If a third-party component is added later, list it here in the same pull request and follow its licence (for example, by including its licence text in the artifact).
