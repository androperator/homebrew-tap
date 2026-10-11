cask "adbuddy" do
  version "1.0.0"
  sha256 "95363f2de0e159ff71d120498c531dafa2e4663e07ad6ea51b74d4b0e5f63595"

  url "https://github.com/androperator/adbuddy/releases/download/v#{version}/ADBuddy-macos-universal-#{version}.zip"
  name "ADBuddy"
  desc "Android device and emulator developer tools"
  homepage "https://github.com/androperator/adbuddy"

  depends_on macos: :sonoma

  app "ADBuddy.app"

  zap trash: "~/Library/Preferences/com.clawperator.adbuddy.plist"
end
