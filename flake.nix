{
  description = "Get data from IOTE Expo China";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = {nixpkgs, ...}: let
    pkgs = import nixpkgs {system = "x86_64-linux";};
  in {
    devShells.x86_64-linux.default = pkgs.mkShell {
      packages = with pkgs; [
        (python313.withPackages (p:
          with p; [
            selenium
            webdriver-manager
          ]))
        chromium
      ];
    };
  };
}
