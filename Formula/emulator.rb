class Emulator < Formula
  desc "Android emulator lifecycle command"
  homepage "https://github.com/androperator/androperator-emulator"
  url "https://registry.npmjs.org/@androperator/emulator/-/emulator-0.2.0.tgz"
  version "0.2.0"
  sha256 "eaa2f002b3d658acd3ffa99ba054e8be470588eface47a1586f946e95c36f2c9"
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
    assert_match "0.2.0", shell_output("#{bin}/androperator-emulator --version")
    assert JSON.parse(shell_output("#{bin}/androperator-emulator --help"))["data"]["commands"].key?("inspect")
  end
end
