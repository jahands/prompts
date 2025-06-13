set shell := ["zsh", "-c"]

[private]
@help:
  just --list

fix:
  bun prettier --cache --write .
