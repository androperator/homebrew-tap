class Emulator < Formula
  desc "Android emulator lifecycle command"
  homepage "https://github.com/androperator/androperator-emulator"
  url "https://registry.npmjs.org/@androperator/emulator/-/emulator-0.1.1.tgz"
  version "0.1.1"
  sha256 "e099f8eca757bf2f5b370b7fa949034cb580349a3afe68cf17749ae5f6e2c95e"
  license "Apache-2.0"

  depends_on "node"

  def install
    system "npm", "install", *std_npm_args
    (bin/"androperator-emulator").write <<~SH
      #!/bin/bash
      exec "#{Formula["node"].opt_bin}/node" "#{libexec}/lib/node_modules/@androperator/emulator/dist/cli.js" "$@"
    SH
    chmod 0755, bin/"androperator-emulator"
  end

  test do
    assert_match "0.1.1", shell_output("#{bin}/androperator-emulator --version")
    assert_match "androperator-emulator", shell_output("#{bin}/androperator-emulator --help")
  end
end
