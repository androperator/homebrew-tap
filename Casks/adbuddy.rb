cask "adbuddy" do
  version "1.0.3"
  sha256 "dc0b3f3ebf6a59f9f046fb5e0b33b485131ca23259b42669086500c59d83f3f5"

  url "https://github.com/androperator/ADBuddy/releases/download/v#{version}/ADBuddy-macos-universal-#{version}.zip"
  name "ADBuddy"
  desc "Android device and emulator developer tools"
  homepage "https://github.com/androperator/adbuddy"

  depends_on macos: :sonoma

  app "ADBuddy.app"

  zap trash: "~/Library/Preferences/com.clawperator.adbuddy.plist"
end
