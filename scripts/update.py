#!/usr/bin/env python3
"""Generate formulae from verified, stable npm releases."""
import base64
import hashlib
import io
import json
from pathlib import Path
import re
import tarfile
from urllib.parse import quote, urlparse
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = {
    'cli': ('@androperator/cli', 'androperator', 'dist/cli/index.js',
            'Deterministic Android control for agents', 'https://androperator.com'),
    'emulator': ('@androperator/emulator', 'androperator-emulator', 'dist/cli.js',
                 'Android emulator lifecycle command', 'https://github.com/androperator/androperator-emulator'),
}


def download(url):
    with urlopen(url, timeout=60) as response:
        return response.read()


def validate(package, command, entrypoint, metadata, archive):
    version = metadata.get('version', '')
    if metadata.get('name') != package or not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('Expected the named package and a stable version')
    dist = metadata['dist']
    expected_url = f'https://registry.npmjs.org/{package}/-/{package.split("/")[-1]}-{version}.tgz'
    if dist['tarball'] != expected_url:
        raise ValueError('Unexpected npm archive URL')
    integrity = 'sha512-' + base64.b64encode(hashlib.sha512(archive).digest()).decode()
    if dist.get('integrity') != integrity:
        raise ValueError('npm archive integrity mismatch')
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as contents:
        manifest = json.load(contents.extractfile('package/package.json'))
        if manifest.get('name') != package or manifest.get('version') != version:
            raise ValueError('Archive manifest does not match registry metadata')
        if manifest.get('bin') != {command: entrypoint}:
            raise ValueError('Archive has an unexpected executable mapping')
        target = contents.getmember(f'package/{entrypoint}')
        if not target.isfile() or target.size == 0:
            raise ValueError('Archive executable is missing or empty')
    return version, expected_url, hashlib.sha256(archive).hexdigest()


def formula(name, package, command, entrypoint, description, homepage, version, url, checksum):
    return f'''class {name.capitalize()} < Formula
  desc "{description}"
  homepage "{homepage}"
  url "{url}"
  version "{version}"
  sha256 "{checksum}"
  license "Apache-2.0"

  depends_on "node"

  def install
    system "npm", "install", *std_npm_args
    (bin/"{command}").write <<~SH
      #!/bin/bash
      exec "#{{Formula["node"].opt_bin}}/node" "#{{libexec}}/lib/node_modules/{package}/{entrypoint}" "$@"
    SH
    chmod 0755, bin/"{command}"
  end

  test do
    assert_match "{version}", shell_output("#{{bin}}/{command} --version")
    assert_match "{command if name == 'emulator' else 'Androperator'}", shell_output("#{{bin}}/{command} --help")
  end
end
'''


def main():
    outputs = {}
    for name, (package, command, entrypoint, description, homepage) in PACKAGES.items():
        metadata = json.loads(download(f'https://registry.npmjs.org/{quote(package, safe="")}/latest'))
        # Validate URL before allowing registry metadata to select a download host.
        url = metadata['dist']['tarball']
        if urlparse(url).scheme != 'https' or urlparse(url).netloc != 'registry.npmjs.org':
            raise ValueError('Archive must be served by the npm registry over HTTPS')
        archive = download(url)
        version, url, checksum = validate(package, command, entrypoint, metadata, archive)
        outputs[name] = formula(name, package, command, entrypoint, description, homepage, version, url, checksum)
        print(f'{name}: verified {package}@{version}')
    for name, content in outputs.items():
        (ROOT / 'Formula' / f'{name}.rb').write_text(content)


if __name__ == '__main__':
    main()
