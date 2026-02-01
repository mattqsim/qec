import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="qec",
        description="QEC playground CLI (repetition code -> surface code).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="qec 0.0.0",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)  # --help is handled automatically here
    print("qec CLI is wired. Next: add subcommands.")
    return 0


