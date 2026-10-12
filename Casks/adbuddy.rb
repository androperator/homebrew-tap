cask "adbuddy" do
  version "1.0.1"
  sha256 "8b88712e8b2ba173dbeca4552cd002f67dbba5471e2b25b96dff430178475601"

  url "https://github.com/androperator/adbuddy/releases/download/v#{version}/ADBuddy-macos-universal-#{version}.zip"
  name "ADBuddy"
  desc "Android device and emulator developer tools"
  homepage "https://github.com/androperator/adbuddy"

  depends_on macos: :sonoma

  app "ADBuddy.app"

  zap trash: "~/Library/Preferences/com.clawperator.adbuddy.plist"
end
