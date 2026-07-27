"""CLI de assets do UIKitPR."""

from __future__ import annotations

import argparse
from pathlib import Path

from .theme import stylesheet


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="uikitpr", description="Assets e informações do UIKitPR."
    )
    parser.add_argument("--version", action="store_true", help="mostra a versão")
    subcommands = parser.add_subparsers(dest="command")
    css = subcommands.add_parser("css", help="exporta o stylesheet")
    css.add_argument("-o", "--output", default="uikitpr.css")
    css.add_argument("--minify", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.version:
        from . import __version__

        print(__version__)
        return 0
    if args.command == "css":
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(stylesheet(minified=args.minify), encoding="utf-8")
        print(f"CSS exportado para {output.resolve()}")
        return 0
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

