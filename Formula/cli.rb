class Cli < Formula
  desc "Deterministic Android control for agents"
  homepage "https://androperator.com"
  url "https://registry.npmjs.org/@androperator/cli/-/cli-1.3.1.tgz"
  version "1.3.1"
  sha256 "8164af0929e2a1b5d883868bc426acf804c402af17e4292dcf4f2afdf8690908"
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
    assert_match "1.3.1", shell_output("#{bin}/androperator --version")
    assert_match "Androperator", shell_output("#{bin}/androperator --help")
  end
end
