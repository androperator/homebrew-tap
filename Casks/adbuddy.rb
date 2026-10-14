cask "adbuddy" do
  version "1.0.2"
  sha256 "96f815f194442da75e13432b5ee84804da3e10cf30e492961611f8dea4140162"

  url "https://github.com/androperator/ADBuddy/releases/download/v#{version}/ADBuddy-macos-universal-#{version}.zip"
  name "ADBuddy"
  desc "Android device and emulator developer tools"
  homepage "https://github.com/androperator/adbuddy"

  depends_on macos: :sonoma

  app "ADBuddy.app"

  zap trash: "~/Library/Preferences/com.clawperator.adbuddy.plist"
end
