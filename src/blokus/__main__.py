"""Module entry point for `python -m blokus`."""

from blokus.cli import main


if __name__ == "__main__":
    # Bubble the CLI exit code back to the shell.
    raise SystemExit(main())
