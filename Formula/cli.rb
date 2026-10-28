class Cli < Formula
  desc "Deterministic Android control for agents"
  homepage "https://androperator.com"
  url "https://registry.npmjs.org/@androperator/cli/-/cli-1.3.0.tgz"
  version "1.3.0"
  sha256 "168c576571f9a80ce2eb99bb58137f47679b519745b63645de331c50710844da"
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
    assert_match "1.3.0", shell_output("#{bin}/androperator --version")
    assert_match "Androperator", shell_output("#{bin}/androperator --help")
  end
end
