
{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    pkgs.python312.pkgs.buildPythonPackage
    (pkgs.python312.pkgs.buildPythonPackage rec {
      pname = "questionnaireOCR";
      version = "0.1.0";
      
      src = ./.;
      
      buildInputs = [
        pkgs.python312.pkgs.setuptools
        pkgs.python312.pkgs.wheel
      ];
      
      propagatedBuildInputs = [ pkgs.python312.pkgs.django ];
      python = pkgs.python312;
    })
  ];
}