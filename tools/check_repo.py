"""Content check of the public vpi-releases repository.

This repository holds only public documents and the ledger of published releases. The release files themselves
live in GitHub Releases. The check runs in CI on every push and pull request and on every published or edited
release:

    python tools/check_repo.py                         # files of this checkout
    python tools/check_repo.py --base origin/main      # also: the ledger only grows (pull requests)
    python tools/check_repo.py --release-dir DIR --tag v1.0.5 --body-file BODY.md   # a GitHub release

It never prints a value that looks like a secret, only the file and the kind of problem.
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]

# Every file this repository may hold. Anything else (source code, server files, builds, reports, data) fails.
ALLOWED = {
    'README.md', 'PRIVACY.md', 'LICENSE', 'LICENSE.uk.md', 'LICENSE.ru.md', 'COPYRIGHT.md',
    'THIRD_PARTY_NOTICES.md', 'LEGAL-SHA256.txt', '.gitignore',
    '.github/ISSUE_TEMPLATE/config.yml', '.github/ISSUE_TEMPLATE/licensing-permissions.yml',
    '.github/workflows/content.yml', 'tools/check_repo.py', 'tests/test_check_repo.py', 'releases/README.md',
}
ALLOWED_PATTERNS = (
    re.compile(r'^releases/v\d+\.\d+\.\d+\.sha256$'),          # ledger: one file per published tag
    re.compile(r'^docs/[a-z0-9][a-z0-9-]*(?:\.[a-z]{2})?\.md$'),    # public documentation
    re.compile(r'^docs/images/[a-z0-9][a-z0-9-]*\.(?:png|jpg|webp)$'),
)
# The documents that must stay byte-identical to the source repository. LEGAL-SHA256.txt pins them, and the
# source repository's release gate (--public-repo) compares them with its own copies.
LEGAL = ('LICENSE', 'LICENSE.uk.md', 'LICENSE.ru.md', 'COPYRIGHT.md', 'THIRD_PARTY_NOTICES.md', 'PRIVACY.md')
LEGAL_SUMS = 'LEGAL-SHA256.txt'
MAX_FILE = 2 * 1024 * 1024

SECRET_PATTERNS = (
    ('a private key', re.compile(rb'-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----')),
    ('a GitHub token', re.compile(rb'(?<![A-Za-z0-9_])(?:gh[pousr]_[A-Za-z0-9]{36,255}|github_pat_[A-Za-z0-9_]{60,255})')),
    ('an AWS key', re.compile(rb'(?<![A-Z0-9])(?:AKIA|ASIA)[0-9A-Z]{16}(?![A-Z0-9])')),
    ('a Slack token', re.compile(rb'(?<![A-Za-z0-9])xox[abprs]-[A-Za-z0-9-]{10,}')),
    ('a Google API key', re.compile(rb'(?<![A-Za-z0-9])AIza[0-9A-Za-z_\-]{35}(?![0-9A-Za-z_\-])')),
    ('a Wargaming application_id', re.compile(
        rb'(?i)(?:application_id|VPI_WG_APPLICATION_ID)["\']?\s*[:=]\s*["\']?[A-Za-z0-9]{32}(?![A-Za-z0-9])')),
    ('a secret in .env format', re.compile(
        rb'(?im)^[ \t]*(?:export[ \t]+)?[A-Z0-9_]*(?:SECRET|TOKEN|PASSWORD|PASSWD|API_KEY|PRIVATE_KEY|SALT)[A-Z0-9_]*'
        rb'[ \t]*=[ \t]*["\']?[^\s"\'#$]{8,}')),
    ('a password in a URL', re.compile(rb'(?i)\b[a-z][a-z0-9+.-]*://[^\s/:@"\']+:[^\s/@"\']+@[a-z0-9.-]+')),
)
WG_ADDRESS = 'a direct Wargaming API address'
# Traces of private material: local paths of the author's machines and the server, server code, research data.
PRIVATE_PATTERNS = (
    ('a local path', re.compile(rb'(?i)(?<![A-Za-z0-9])[A-Z]:[\\/][A-Za-z0-9 _.()-]{1,64}[\\/]|/home/[a-z_][a-z0-9_-]*/|'
                                rb'/mnt/(?:project-files|user-data|c|d|f)/|/opt/vpi/|/root/\.')),
    ('server code', re.compile(rb'ThreadingHTTPServer|VPI_WG_PUBLIC_APPROVED|RatingsEngine|reverse_proxy')),
    (WG_ADDRESS, re.compile(rb'api\.worldoftanks\.(?:eu|com)|api\.wotblitz')),
)
# Text files of this checker may describe the patterns; they are still checked for secrets.
SELF = {'tools/check_repo.py', 'tests/test_check_repo.py'}

# Files of a public GitHub release (tools/release_policy.py in the source repository).
RELEASE_NAMES = ('VPI-Setup-{v}-EU-Public.exe', 'VPI-{v}-EU-Public.zip', 'vpi.index_{v}.wotmod',
                 'vpi-native-ui_{v}.wotmod')
SUMS = 'SHA256SUMS.txt'
NOTES = 'RELEASE-NOTES-UK.md'
TAG = re.compile(r'^v(\d+\.\d+\.\d+)$')
SUM_LINE = re.compile(r'^([0-9a-f]{64})  ([A-Za-z0-9._-]+)$')
MARKER = re.compile(r'<!--\s*vpi-release:\s*(\{[^{}]*\})\s*-->')


class Findings(list):
    def add(self, where, message):
        self.append('{}: {}'.format(where, message))


def tracked_files(root):
    """Files git tracks, or every file of the folder outside .git when it is not a checkout."""
    result = subprocess.run(['git', '-C', str(root), 'ls-files', '-z'], capture_output=True)
    if result.returncode == 0:
        return sorted(name for name in result.stdout.decode('utf-8', 'replace').split('\0') if name)
    return sorted(path.relative_to(root).as_posix() for path in root.rglob('*')
                  if path.is_file() and '.git' not in path.relative_to(root).parts)


def allowed(name):
    return name in ALLOWED or any(pattern.match(name) for pattern in ALLOWED_PATTERNS)


def scan(findings, where, data, private=True):
    for label, pattern in SECRET_PATTERNS:
        if pattern.search(data):
            findings.add(where, 'looks like {} (value not shown)'.format(label))
    if private:
        for label, pattern in PRIVATE_PATTERNS:
            # The licence documents describe the Wargaming API by name; they are pinned and identical to the source.
            if label == WG_ADDRESS and where in LEGAL:
                continue
            if pattern.search(data):
                findings.add(where, 'contains {}'.format(label))


def read_sums(text):
    """{name: sha256} of a SHA256SUMS-style text, or None when a line is malformed or a name repeats."""
    found = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        match = SUM_LINE.match(line)
        if not match or match.group(2) in found:
            return None
        found[match.group(2)] = match.group(1)
    return found


def release_files(version):
    return {name.format(v=version) for name in RELEASE_NAMES}


def check_ledger_entry(findings, name, text):
    version = re.match(r'^releases/v(\d+\.\d+\.\d+)\.sha256$', name).group(1)
    sums = read_sums(text)
    if sums is None:
        findings.add(name, 'is not in "<sha256>  <file>" format')
        return
    if set(sums) != release_files(version) | {NOTES}:
        findings.add(name, 'must list exactly the public release files of {} (SHA256SUMS.txt of the release '
                           'folder)'.format(version))


def check_files(root, findings):
    names = tracked_files(root)
    for name in names:
        path = root / name
        if not allowed(name) or PurePosixPath(name).name.startswith('.env'):
            findings.add(name, 'is not allowed in the public repository (builds go to GitHub Releases, source and '
                               'server files stay private)')
            continue
        if path.is_symlink() or not path.is_file():
            findings.add(name, 'must be a regular file')
            continue
        data = path.read_bytes()
        if len(data) > MAX_FILE:
            findings.add(name, 'is larger than {} bytes'.format(MAX_FILE))
        scan(findings, name, data, private=name not in SELF)
        if name.startswith('releases/v'):
            check_ledger_entry(findings, name, data.decode('ascii', 'replace'))
    for name in LEGAL:
        if name not in names:
            findings.add(name, 'is missing')
    check_legal(root, findings)
    return names


def check_legal(root, findings):
    path = root / LEGAL_SUMS
    pinned = read_sums(path.read_text(encoding='ascii', errors='replace')) if path.is_file() else None
    if pinned is None or set(pinned) != set(LEGAL):
        findings.add(LEGAL_SUMS, 'must pin the SHA-256 of {}'.format(', '.join(LEGAL)))
        return
    for name in LEGAL:
        document = root / name
        if document.is_file() and hashlib.sha256(document.read_bytes()).hexdigest() != pinned[name]:
            findings.add(name, 'differs from the pinned licence text (copy it with tools/legal.py --export in the '
                               'source repository and update {})'.format(LEGAL_SUMS))


def check_history(root, base, findings):
    """The ledger is append-only: an entry of a published tag is never changed, renamed or removed."""
    result = subprocess.run(['git', '-C', str(root), 'diff', '--name-status', '--no-renames', base + '...HEAD', '--',
                             'releases/'], capture_output=True, text=True)
    if result.returncode != 0:
        findings.add(base, 'cannot compare with this git revision')
        return
    for line in result.stdout.splitlines():
        status, _, name = line.partition('\t')
        if status != 'A' and re.match(r'^releases/v\d+\.\d+\.\d+\.sha256$', name):
            findings.add(name, 'tag already published: its entry must not be changed or removed, use a new version')


def check_release(root, folder, tag, body, findings):
    """A published GitHub release: allowed asset names, SHA-256 equal to the ledger, compatibility line."""
    match = TAG.match(tag or '')
    if not match:
        findings.add(tag or 'tag', 'must be vX.Y.Z')
        return
    version = match.group(1)
    entry = root / 'releases' / '{}.sha256'.format(tag)
    ledger = read_sums(entry.read_text(encoding='ascii', errors='replace')) if entry.is_file() else None
    if ledger is None:
        findings.add(entry.relative_to(root).as_posix(), 'missing or malformed: add the ledger entry before publishing')
    assets = {path.name: path for path in Path(folder).iterdir() if path.is_file()}
    allowed_assets = release_files(version) | {SUMS, NOTES}
    for name in sorted(set(assets) - allowed_assets):
        findings.add(name, 'is not a public release file of {}'.format(tag))
    for name in sorted((release_files(version) | {SUMS}) - set(assets)):
        findings.add(name, 'is missing from the release')
    digests = {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in assets.items()}
    listed = read_sums(assets[SUMS].read_text(encoding='ascii', errors='replace')) if SUMS in assets else None
    if SUMS in assets and listed is None:
        findings.add(SUMS, 'is not in "<sha256>  <file>" format')
    if listed is not None and ledger is not None and listed != ledger:
        findings.add(SUMS, 'differs from {}: a changed file needs a new version'.format(entry.name))
    for name, digest in sorted(digests.items()):
        if name == SUMS:
            continue
        if ledger is not None and ledger.get(name) != digest:
            findings.add(name, 'differs from {}: a changed file needs a new version'.format(entry.name))
        elif listed is not None and listed.get(name) != digest:
            findings.add(name, 'does not match {}'.format(SUMS))
    target = None
    found = MARKER.search(body or '')
    if found:
        try:
            target = json.loads(found.group(1))
        except ValueError:
            target = None
    if not isinstance(target, dict) or target.get('build') != 'public' or target.get('region') != 'EU' or \
            target.get('vpi') != version or not re.match(r'^\d+(?:\.\d+){1,3}$', str(target.get('wot', ''))):
        findings.add('release description', 'needs the line <!-- vpi-release: ... --> for public EU {}'.format(version))
    scan(findings, 'release description', (body or '').encode('utf-8'))


def run(root=ROOT, base=None, release_dir=None, tag=None, body=None):
    findings = Findings()
    if release_dir is not None:
        check_release(Path(root), release_dir, tag, body, findings)
    else:
        check_files(Path(root), findings)
        if base:
            check_history(Path(root), base, findings)
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--base', help='git revision to compare the ledger with (pull requests)')
    parser.add_argument('--release-dir', type=Path, help='folder with the downloaded assets of a GitHub release')
    parser.add_argument('--tag', help='tag of that release')
    parser.add_argument('--body-file', type=Path, help='description of that release')
    args = parser.parse_args(argv)
    body = args.body_file.read_text(encoding='utf-8', errors='replace') if args.body_file else ''
    findings = run(ROOT, args.base, args.release_dir, args.tag, body)
    for finding in findings:
        print('ERROR ' + finding)
    print('{} problem(s).'.format(len(findings)) if findings else 'OK')
    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(main())
