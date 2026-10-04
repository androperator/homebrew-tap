#!/usr/bin/env bash
set -euo pipefail
export HOMEBREW_NO_AUTO_UPDATE=1
root="$(cd "$(dirname "$0")/.." && pwd)"
tap_path="$(brew --repository)/Library/Taps/androperator/homebrew-tap"
if [[ -e "$tap_path" || -L "$tap_path" ]]; then
  [[ "$(cd "$tap_path" && pwd -P)" == "$root" ]] || {
    echo 'A different androperator/tap checkout is installed; refusing to replace it.' >&2
    exit 1
  }
else
  mkdir -p "$(dirname "$tap_path")"
  ln -s "$root" "$tap_path"
fi
for formula in cli emulator; do
  ruby -c "$root/Formula/$formula.rb"
  # Reinstall so tests exercise the candidate formula, even when its version is unchanged.
  if brew list --versions "androperator/tap/$formula" >/dev/null 2>&1; then
    brew reinstall --build-from-source --skip-link "androperator/tap/$formula"
  else
    brew install --build-from-source --skip-link "androperator/tap/$formula"
  fi
  brew test --force "androperator/tap/$formula"
done
