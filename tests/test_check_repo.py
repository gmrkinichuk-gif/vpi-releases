"""Tests of tools/check_repo.py. Every "secret" here is invented, built at run time and valid nowhere."""

import hashlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import check_repo  # noqa: E402

VERSION = '9.8.7'
TAG = 'v' + VERSION
# Built from parts so this file itself holds no secret-shaped text.
FAKE_TOKEN = 'gh' + 'p_' + 'Q7fakeTOKENforVPItests' + '0' * 20
FAKE_KEY = '-----BEGIN ' + 'OPENSSH PRIVATE KEY-----\nZmFrZQ==\n-----END OPENSSH PRIVATE KEY-----\n'
MARKER = '<!-- vpi-release: {"build":"public","region":"EU","vpi":"%s","wot":"2.4.2.0"} -->' % VERSION


def git(folder, *args):
    subprocess.run(['git', '-C', str(folder)] + list(args), check=True, capture_output=True)


def sums(files):
    return ''.join('{}  {}\n'.format(hashlib.sha256(data).hexdigest(), name) for name, data in sorted(files.items()))


def release_assets():
    files = {name: 'fixture {}'.format(name).encode('ascii') for name in check_repo.release_files(VERSION)}
    files[check_repo.NOTES] = ('# VPI {}\n\n{}\n'.format(VERSION, MARKER)).encode('utf-8')
    return files


class RepoTestCase(unittest.TestCase):
    def setUp(self):
        self.temp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.temp, ignore_errors=True)
        self.repo = self.temp / 'repo'
        self.repo.mkdir()
        for name in sorted(check_repo.ALLOWED - {'LEGAL-SHA256.txt'}):
            source = ROOT / name
            target = self.repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.is_file():
                shutil.copyfile(source, target)
            else:
                target.write_text('# {}\n'.format(name), encoding='ascii')
        self.pin()
        git(self.repo, 'init', '-q', '-b', 'main')
        git(self.repo, 'config', 'user.email', 'test@example.invalid')
        git(self.repo, 'config', 'user.name', 'Test')
        self.commit('base')

    def pin(self):
        text = ''.join('{}  {}\n'.format(hashlib.sha256((self.repo / name).read_bytes()).hexdigest(), name)
                       for name in check_repo.LEGAL)
        (self.repo / check_repo.LEGAL_SUMS).write_text(text, encoding='ascii')

    def commit(self, message):
        git(self.repo, 'add', '-A')
        git(self.repo, 'commit', '-q', '--allow-empty', '-m', message)

    def write(self, name, data):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data if isinstance(data, bytes) else data.encode('utf-8'))

    def findings(self, base=None):
        git(self.repo, 'add', '-A')
        return check_repo.run(self.repo, base)

    def assertFinds(self, text, findings):
        self.assertTrue(any(text in item for item in findings), findings)


class FileTests(RepoTestCase):
    def test_clean_repository_passes(self):
        self.assertEqual(self.findings(), [])

    def test_this_repository_passes(self):
        result = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', '--is-inside-work-tree'], capture_output=True)
        if result.returncode != 0:
            self.skipTest('not a git checkout')
        self.assertEqual(check_repo.run(ROOT), [])

    def test_foreign_files_are_rejected(self):
        for name in ('src/vpi/client.py', 'server/vpi_server.py', 'VPI-Server.zip', 'VPI-1.0.4-EU.zip',
                     'dist/VPI-Setup-1.0.4-EU-Public.exe', 'REPORT-UK.md', 'docs/research.csv', '.env',
                     'config.json', 'notes.txt'):
            with self.subTest(name=name):
                self.write(name, 'x')
                self.assertFinds(name + ': is not allowed', self.findings())
                (self.repo / name).unlink()

    def test_documentation_is_allowed(self):
        self.write('docs/install.md', '# Install\n')
        self.write('docs/install.uk.md', '# Встановлення\n')
        self.write('docs/images/banner.png', b'\x89PNG fixture')
        self.assertEqual(self.findings(), [])

    def test_secrets_are_found_but_never_shown(self):
        for text in ('token = ' + FAKE_TOKEN, FAKE_KEY, 'VPI_SERVER_SECRET=not-a-real-secret-123\n'):
            with self.subTest(text=text[:12]):
                self.write('docs/leak.md', text)
                findings = self.findings()
                self.assertFinds('docs/leak.md: looks like', findings)
                self.assertFalse(any(FAKE_TOKEN in item or 'ZmFrZQ' in item or 'not-a-real' in item
                                     for item in findings))

    def test_private_traces_are_rejected(self):
        for text in ('See F:\\VPI-GitHub\\dist\\', 'cd /opt/vpi/server', 'https://api.worldoftanks.eu/wot/',
                     'server = ThreadingHTTPServer'):
            with self.subTest(text=text):
                self.write('docs/notes.md', text)
                self.assertFinds('docs/notes.md: contains', self.findings())

    def test_licence_mismatch_is_rejected(self):
        self.write('LICENSE.uk.md', 'змінено')
        self.assertFinds('LICENSE.uk.md: differs from the pinned', self.findings())
        (self.repo / 'PRIVACY.md').unlink()
        self.assertFinds('PRIVACY.md: is missing', self.findings())

    def test_missing_pins_are_rejected(self):
        (self.repo / check_repo.LEGAL_SUMS).unlink()
        self.assertFinds(check_repo.LEGAL_SUMS, self.findings())

    def test_ledger_entry_format(self):
        files = release_assets()
        self.write('releases/{}.sha256'.format(TAG), sums(files))
        self.assertEqual(self.findings(), [])
        files['VPI-Server.zip'] = b'server'
        self.write('releases/{}.sha256'.format(TAG), sums(files))
        self.assertFinds('must list exactly', self.findings())
        self.write('releases/{}.sha256'.format(TAG), 'not a checksum\n')
        self.assertFinds('format', self.findings())


class LedgerHistoryTests(RepoTestCase):
    def test_new_entry_may_be_added(self):
        self.write('releases/{}.sha256'.format(TAG), sums(release_assets()))
        self.commit('add')
        self.assertEqual(self.findings('HEAD~1'), [])

    def test_published_entry_cannot_change(self):
        files = release_assets()
        self.write('releases/{}.sha256'.format(TAG), sums(files))
        self.commit('publish')
        files['vpi.index_{}.wotmod'.format(VERSION)] = b'changed package'
        self.write('releases/{}.sha256'.format(TAG), sums(files))
        self.commit('reuse tag')
        self.assertFinds('tag already published', self.findings('HEAD~1'))

    def test_published_entry_cannot_be_removed(self):
        self.write('releases/{}.sha256'.format(TAG), sums(release_assets()))
        self.commit('publish')
        (self.repo / 'releases/{}.sha256'.format(TAG)).unlink()
        self.commit('remove')
        self.assertFinds('tag already published', self.findings('HEAD~1'))


class ReleaseTests(RepoTestCase):
    def setUp(self):
        super(ReleaseTests, self).setUp()
        self.files = release_assets()
        self.write('releases/{}.sha256'.format(TAG), sums(self.files))
        self.assets = self.temp / 'assets'
        self.assets.mkdir()
        for name, data in self.files.items():
            (self.assets / name).write_bytes(data)
        (self.assets / check_repo.SUMS).write_text(sums(self.files), encoding='ascii')
        self.body = '# VPI {}\n\n{}\n'.format(VERSION, MARKER)

    def check(self, tag=TAG, body=None):
        return check_repo.run(self.repo, release_dir=self.assets, tag=tag, body=self.body if body is None else body)

    def test_clean_release_passes(self):
        self.assertEqual(self.check(), [])

    def test_notes_asset_is_optional(self):
        (self.assets / check_repo.NOTES).unlink()
        self.assertEqual(self.check(), [])

    def test_foreign_asset_is_rejected(self):
        for name in ('VPI-Server.zip', 'VPI-{}-EU.zip'.format(VERSION), 'VPI-Setup-{}-EU.exe'.format(VERSION),
                     'REPORT-UK.md'):
            with self.subTest(name=name):
                (self.assets / name).write_bytes(b'private')
                self.assertFinds(name + ': is not a public release file', self.check())
                (self.assets / name).unlink()

    def test_changed_file_under_used_tag_is_rejected(self):
        (self.assets / 'VPI-{}-EU-Public.zip'.format(VERSION)).write_bytes(b'rebuilt')
        self.assertFinds('a changed file needs a new version', self.check())

    def test_regenerated_sums_do_not_help(self):
        changed = dict(self.files)
        changed['VPI-{}-EU-Public.zip'.format(VERSION)] = b'rebuilt'
        (self.assets / 'VPI-{}-EU-Public.zip'.format(VERSION)).write_bytes(b'rebuilt')
        (self.assets / check_repo.SUMS).write_text(sums(changed), encoding='ascii')
        self.assertFinds('a changed file needs a new version', self.check())

    def test_missing_file_is_rejected(self):
        (self.assets / 'vpi-native-ui_{}.wotmod'.format(VERSION)).unlink()
        self.assertFinds('is missing from the release', self.check())

    def test_release_without_ledger_entry_is_rejected(self):
        (self.repo / 'releases/{}.sha256'.format(TAG)).unlink()
        self.assertFinds('add the ledger entry', self.check())

    def test_compatibility_line_is_required(self):
        for body in ('# VPI', MARKER.replace('"public"', '"private"'), MARKER.replace('"EU"', '"NA"'),
                     MARKER.replace(VERSION, '1.0.0')):
            with self.subTest(body=body[:40]):
                self.assertFinds('vpi-release', self.check(body=body))

    def test_bad_tag_is_rejected(self):
        self.assertFinds('must be vX.Y.Z', self.check(tag='latest'))


if __name__ == '__main__':
    unittest.main()
