class Emulator < Formula
  desc "Android emulator lifecycle command"
  homepage "https://github.com/androperator/androperator-emulator"
  url "https://registry.npmjs.org/@androperator/emulator/-/emulator-0.3.0.tgz"
  version "0.3.0"
  sha256 "cb8dad376c6d3a0c9874fb48e424bb782a06d8ed8d4149b9115d9e9546481ccf"
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
    assert_match "0.3.0", shell_output("#{bin}/androperator-emulator --version")
    assert JSON.parse(shell_output("#{bin}/androperator-emulator --help"))["data"]["commands"].key?("inspect")
  end
end
