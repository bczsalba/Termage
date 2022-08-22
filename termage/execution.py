"""All the code used to record code execution."""

# pylint: disable=exec-used

from __future__ import annotations

import sys
import builtins
from io import StringIO
from pathlib import Path
from typing import Generator, Any
from contextlib import contextmanager

import pytermgui as ptg

DEFAULT_WIDTH = 80
DEFAULT_HEIGHT = 24


def format_codeblock(block: str) -> tuple[str, str]:
    disp_lines, exec_lines = [], []

    for line in block.splitlines():
        if line.startswith("&"):
            exec_lines.append(line[1:])
            continue

        exec_lines.append(line)
        disp_lines.append(line)

    return "\n".join(disp_lines), "\n".join(exec_lines)


class TermageNamespace:
    @property
    def terminal(self) -> ptg.Terminal:
        return ptg.get_terminal()

    def fit(self, widget: ptg.Widget) -> None:
        self.terminal.size = widget.width, widget.height

    def resize(self, width: int, height: int) -> None:
        self.terminal.size = width, height


EXEC_GLOBALS: dict[str, Any] = {
    "__name__": "__main__",
    "__doc__": None,
    "__package__": None,
    "__annotations__": {},
    "__builtins__": builtins,
    "termage": TermageNamespace(),
}


@contextmanager
def patched_stdout_recorder(
    width: int | None, height: int | None
) -> Generator[ptg.Recorder, None, None]:
    """Patches sys.stdout.write to write to a new terminal.

    Returns:
        The recorder that was written to.
    """

    if width is None:
        width = DEFAULT_WIDTH

    if height is None:
        height = DEFAULT_HEIGHT

    stdout_write = sys.stdout.write

    stream = StringIO()
    terminal = ptg.Terminal(stream=stream, size=(width, height))

    ptg.set_global_terminal(terminal)

    def _write(item, **kwargs) -> None:
        """Writes something, breaks lines."""

        ends_with_linebreak = item.endswith("\n")

        lines = list(ptg.break_line(item, terminal.width))

        for i, line in enumerate(lines):
            if ends_with_linebreak or i < len(lines) - 1:
                line += "\n"

            terminal.write(line, **kwargs)

    with terminal.record() as recorder:
        try:
            sys.stdout.write = _write
            yield recorder

        finally:
            sys.stdout.write = stdout_write  # type: ignore


def execute(
    module: str | None = None,
    file: Path | None = None,
    code: str | None = None,
    highlight: bool = None,
    *,
    exec_globals: dict[str, Any] = EXEC_GLOBALS
) -> None:
    """Executes the given code."""

    ptg.WindowManager.autorun = False

    exec_globals = exec_globals.copy()
    code = code or ""

    if module is not None:
        # mod_name, *args = module.split()
        # sys.argv = [*args]
        # out = runpy.run_module(mod_name, init_globals={"sys": sys})
        # print(out)
        raise NotImplementedError("Module execution is not yet implemented.")

    if file is not None:
        with open(file, "r", encoding="utf-8") as source:
            code = source.read() + code

    if highlight:
        print(ptg.tim.parse(ptg.highlight_python(code)))
        return

    exec(code, exec_globals)

    if "manager" in exec_globals:
        exec_globals["manager"].compositor.draw()


def set_colors(foreground: str | None, background: str | None) -> None:
    """Sets the colors that will be used by the terminal."""

    if foreground is not None:
        ptg.Color.default_foreground = ptg.str_to_color(foreground)

    if background is not None:
        ptg.Color.default_background = ptg.str_to_color(background)


def termage(
    code: str = "",
    include: str | Path | None = None,
    width: int | None = None,
    height: int | None = None,
    title: str = "",
    chrome: bool = True,
    foreground: str | None = None,
    background: str | None = None,
    save_as: str | Path | None = None,
) -> str:
    """Executes CLI with the given (long-form) arguments.

    To see all arguments, check out the docs.

    Returns:
        The generated SVG if the `out` parameter is not given, else
        None, after writing output to `out`.
    """

    set_colors(foreground, background)
    if include is not None:
        with open(include, "r") as includefile:
            code = includefile.read() + code

    with patched_stdout_recorder(width, height) as recording:
        execute(code=code)

    export = recording.export_svg(title=title, chrome=chrome)

    if save_as is not None:
        with open(save_as, "w") as save:
            save.write(export)

    return export
