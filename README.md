# vpi-releases

Official releases of Vehicle Performance Index (VPI) for World of Tanks EU.

Download VPI only from the [Releases](https://github.com/gmrkinichuk-gif/vpi-releases/releases) page of this repository. Copies from other sites are not official.

## What is published here

This repository holds public documents only. The source code, the private build, the server and any research data are kept elsewhere and are never published here.

Each release contains only the files of the public build, checked before publishing:

| File | What it is |
| --- | --- |
| `VPI-Setup-<version>-EU-Public.exe` | Windows installer |
| `VPI-<version>-EU-Public.zip` | Manual installation into the game folder |
| `vpi.index_<version>.wotmod`, `vpi-native-ui_<version>.wotmod` | The two game packages, also contained in the installer and the ZIP |
| `SHA256SUMS.txt` | SHA-256 of every file of the release |

Each release is built for one World of Tanks EU client version, named in its description. The SHA-256 of every published release is recorded in [`releases/`](releases/) and never changes: a changed file always gets a new version. To check a download on Windows, run `certutil -hashfile <file> SHA256` and compare the result with `SHA256SUMS.txt`.

## Privacy

VPI has no accounts, analytics, advertising or telemetry. Ratings from the VPI service are off until you agree on the **EU data** settings page. What is processed and where: [`PRIVACY.md`](PRIVACY.md).

## Licence

© 2026 Vladyslav Kinichuk (metronom_). All rights reserved.

VPI is free of charge, closed-source software, licensed under the **VPI Proprietary Freeware License 1.0**. The same terms apply to the source code, this repository and every release file.

| File | Language |
| --- | --- |
| [`LICENSE`](LICENSE) | English, governing text |
| [`LICENSE.uk.md`](LICENSE.uk.md) | Українська, переклад для зручності |
| [`LICENSE.ru.md`](LICENSE.ru.md) | Русский, перевод для удобства |

See also [`COPYRIGHT.md`](COPYRIGHT.md) and [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md). [`LEGAL-SHA256.txt`](LEGAL-SHA256.txt) pins the SHA-256 of these documents, which are identical in every release file.

- Personal, non-commercial use is free.
- Links, reviews, videos, streams, tutorials and demonstrations need no permission and may be monetised in line with Wargaming's rules. This does not cover selling or redistributing VPI itself.
- Modpacks, mirrors, redistribution, modifications and separate or commercial licences need the author's written permission. Ask through the [Licensing & Permissions](https://github.com/gmrkinichuk-gif/vpi-releases/issues/new?template=licensing-permissions.yml) form.
- Crosshairs API is an independent third-party mod. VPI does not ship its code, and the VPI licence does not cover it.

## Not affiliated with Wargaming

VPI is an unofficial modification for World of Tanks made by a player. It is not affiliated with, endorsed, sponsored or supported by Wargaming.

> This work includes trademarks and/or copyrighted works that are the exclusive property of Wargaming. All rights reserved by Wargaming. This work is unofficial and is not endorsed by Wargaming.
