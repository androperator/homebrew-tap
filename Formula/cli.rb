class Cli < Formula
  desc "Deterministic Android control for agents"
  homepage "https://androperator.com"
  url "https://registry.npmjs.org/@androperator/cli/-/cli-1.1.0.tgz"
  version "1.1.0"
  sha256 "f92e6d3bdfea0b402dc4536642c95d7e07318e608daa56f6f394b944b051ebf3"
  license "Apache-2.0"

  depends_on "node"

  def install
    system "npm", "install", *std_npm_args
    (bin/"androperator").write <<~SH
      #!/bin/bash
      exec "#{Formula["node"].opt_bin}/node" "#{libexec}/lib/node_modules/@androperator/cli/dist/cli/index.js" "$@"
    SH
    chmod 0755, bin/"androperator"
  end

  test do
    assert_match "1.1.0", shell_output("#{bin}/androperator --version")
    assert_match "Androperator", shell_output("#{bin}/androperator --help")
  end
end
