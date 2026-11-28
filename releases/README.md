# Release ledger

One file per published tag, `v<version>.sha256`, with the SHA-256 of every file of that public release. It is a copy of `SHA256SUMS.txt` from the release folder that passed `tools/release_gate.py` in the source repository.

- Add the entry in its own pull request before publishing the release.
- An entry is never changed, renamed or removed. A changed file needs a new version and a new tag. CI (`tools/check_repo.py --base`) rejects any other change.
- After a release is published or edited, CI downloads its files and checks their names and SHA-256 against the entry and the compatibility line `<!-- vpi-release: ... -->` in its description.
