"""The `cuemodo` command."""
import argparse

from cuemodo import __version__


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="cuemodo", description="Open-source show control (early development).")
    parser.add_argument("--version", action="version", version=f"cuemodo {__version__}")
    parser.parse_args(argv)
    print(f"cuemodo {__version__}, early development. See https://github.com/cuemodo/cuemodo")
