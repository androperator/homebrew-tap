# Androperator for Homebrew

Install the ADBuddy macOS app, Android automation CLI, or standalone emulator command:

```sh
brew install --cask androperator/tap/adbuddy
brew install androperator/tap/cli
brew install androperator/tap/emulator
```

The commands remain `androperator` and `androperator-emulator`. The CLI already
includes the emulator library; install the second formula only when you want its
standalone command. Both use the same release archives published to npm, with
Homebrew-managed Node and dependencies. Android SDK tools and device permissions
are configured separately; see https://docs.androperator.com/setup/.

If migrating an existing global npm installation, remove it before linking the
Homebrew installation:

```sh
npm uninstall -g androperator @androperator/cli
# For the standalone emulator, if installed:
npm uninstall -g @androperator/emulator
```

Upgrade with `brew upgrade androperator/tap/cli androperator/tap/emulator`.
Do not use `npm install -g` to upgrade a Homebrew installation.

## ADBuddy

[ADBuddy](https://github.com/androperator/adbuddy) is a native macOS app for Android
device and emulator tasks. The cask installs the signed and notarized universal
app from GitHub Releases on macOS 14 or newer, on Apple silicon or Intel Macs.
Android SDK tools are configured separately. Emulator creation and deletion also
require Node.js 24+, which the cask does not install automatically.

Upgrade with `brew upgrade --cask androperator/tap/adbuddy` and uninstall with
`brew uninstall --cask androperator/tap/adbuddy`. Uninstalling retains saved
preferences and captures. Adding `--zap` removes the legacy shared preferences
file, `com.clawperator.adbuddy.plist`; screenshots and recordings are retained.
The app's bundle identifier is `com.androperator.adbuddy`, while the original
preferences domain is kept so upgrades preserve settings shared with its MCP helper.

For each ADBuddy release, update `Casks/adbuddy.rb` only after its GitHub Release
ZIP is published. Set the version and SHA-256 of the universal ZIP, then validate
the cask. The npm updater below does not update the ADBuddy cask.

## Automatic updates

`update.yml` checks npm's `latest` versions hourly and on manual dispatch. It
verifies registry archive integrity, generates checksummed formulae, installs and
tests both packages on macOS, and commits only the formula changes after success.
No npm token or cross-repository GitHub token is needed. Failed checks leave the
previous versions available. The hourly schedule picks up new npm releases automatically. A release can also
request an immediate check with `gh workflow run update.yml --repo androperator/homebrew-tap`.
Homebrew may defer installation of dependencies published in the previous 24 hours;
the next scheduled check retries without bypassing that protection.

Run locally with `python3 scripts/update.py`, then `bash scripts/test-formulae.sh`.
The test script installs unlinked formulae and uses their explicit executable paths;
it does not replace the commands found on your normal PATH.
