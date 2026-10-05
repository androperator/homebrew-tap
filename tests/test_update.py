import base64
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tarfile
import unittest

spec = importlib.util.spec_from_file_location('update', Path(__file__).parents[1] / 'scripts/update.py')
update = importlib.util.module_from_spec(spec)
spec.loader.exec_module(update)


def fixture():
    manifest = {'name': '@androperator/cli', 'version': '1.1.0',
                'bin': {'androperator': 'dist/cli/index.js'}}
    output = io.BytesIO()
    with tarfile.open(fileobj=output, mode='w:gz') as archive:
        for name, data in [('package/package.json', json.dumps(manifest).encode()),
                           ('package/dist/cli/index.js', b'console.log("1.1.0")')]:
            entry = tarfile.TarInfo(name)
            entry.size = len(data)
            archive.addfile(entry, io.BytesIO(data))
    content = output.getvalue()
    metadata = {**manifest, 'dist': {'tarball': 'https://registry.npmjs.org/@androperator/cli/-/cli-1.1.0.tgz',
                'integrity': 'sha512-' + base64.b64encode(hashlib.sha512(content).digest()).decode()}}
    return metadata, content


class UpdateTests(unittest.TestCase):
    def test_verified_archive_produces_expected_version_and_checksum(self):
        metadata, content = fixture()
        result = update.validate('@androperator/cli', 'androperator', 'dist/cli/index.js', metadata, content)
        self.assertEqual(result, ('1.1.0', metadata['dist']['tarball'], hashlib.sha256(content).hexdigest()))

    def test_rejects_wrong_identity_prerelease_url_and_integrity(self):
        original, content = fixture()
        for field, value in [('name', '@other/cli'), ('version', '1.1.0-beta')]:
            with self.subTest(field=field), self.assertRaises(ValueError):
                update.validate('@androperator/cli', 'androperator', 'dist/cli/index.js',
                                {**original, field: value}, content)
        for field, value in [('tarball', 'https://example.com/archive.tgz'), ('integrity', 'sha512-wrong')]:
            with self.subTest(field=field), self.assertRaises(ValueError):
                update.validate('@androperator/cli', 'androperator', 'dist/cli/index.js',
                                {**original, 'dist': {**original['dist'], field: value}}, content)

    def test_rejects_wrong_executable_mapping(self):
        metadata, content = fixture()
        with self.assertRaises(ValueError):
            update.validate('@androperator/cli', 'unexpected-command', 'dist/cli/index.js', metadata, content)


    def test_existing_versions_cannot_be_downgraded_or_replaced(self):
        existing = '  version "1.1.0"\n  sha256 "' + 'a' * 64 + '"\n'
        update.check_existing(existing, '1.1.0', 'a' * 64)
        update.check_existing(existing, '1.2.0', 'b' * 64)
        for version, checksum in [('1.0.9', 'a' * 64), ('1.1.0', 'b' * 64)]:
            with self.subTest(version=version), self.assertRaises(ValueError):
                update.check_existing(existing, version, checksum)
        with self.assertRaises(ValueError):
            update.check_existing('', '1.1.0', 'a' * 64)
