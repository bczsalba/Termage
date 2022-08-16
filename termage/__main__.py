"""Runs Termage from the CLI.

See `termage -h` for more info.
"""

from __future__ import annotations

import sys
from pathlib import Path
from argparse import ArgumentParser, Namespace

from .execution import patched_stdout_recorder, execute, set_colors


def _process_args(argv: list[str] | None) -> Namespace:
    """Processes CLI args."""

    parser = ArgumentParser()

    parser.add_argument(
        "code",
        help="Code to execute. Uses STDIN when not given or set to '-'.",
        nargs="?",
    )

    parser.add_argument(
        "-f",
        "--file",
        help="Includes code from a path.",
        type=Path,
    )

    parser.add_argument(
        "-o",
        "--out",
        help=(
            "The file to save into."
            + " SVG content will be written to STDOUT if this is not given."
        ),
        metavar="FILE",
    )

    parser.add_argument(
        "-m",
        "--module",
        help="Executes a module, using runpy.",
    )

    parser.add_argument(
        "--width",
        type=int,
        help="Sets the width, in characters.",
    )
    parser.add_argument(
        "--height",
        type=int,
        help="Sets the height, in characters.",
    )

    parser.add_argument(
        "--title",
        type=str,
        help="Sets the title displayed at the top of the window.",
    )

    parser.add_argument(
        "--highlight",
        action="store_true",
        help="Highlights the given code, instead of running it.",
    )

    parser.add_argument(
        "--chrome",
        choices=["show", "hide"],
        default="show",
        help="Highlights the given code, instead of running it.",
    )

    parser.add_argument(
        "--run",
        metavar="FILE",
        type=Path,
        help="Emulates running a file through the MkDocs plugin.",
    )

    parser.add_argument("--fg", help="Sets the foreground color.", metavar="COLOR")
    parser.add_argument("--bg", help="Sets the background color.", metavar="COLOR")

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """Executes the project."""

    args = _process_args(argv)

    if args.run:
        with open(args.run, "r") as runfile:
            # TODO: This should be done in a central location
            code = runfile.read().replace("&", "")
            from pytermgui import highlight_python, tim

            tim.print(highlight_python(code))
            execute(code=code)
        return

    if args.code is None and not sys.stdin.isatty():
        args.code = sys.stdin.read()

    args.code = args.code or ""
    args.title = args.title or ""

    set_colors(args.fg, args.bg)

    with patched_stdout_recorder(args.width, args.height) as recorder:
        execute(args.module, args.file, args.code, args.highlight)

    if args.out is None:
        print(recorder.export_svg(title=args.title, inline_styles=True))
        return

    recorder.save_svg(
        args.out, title=args.title, chrome=args.chrome == "show", inline_styles=True
    )


if __name__ == "__main__":
    main()
