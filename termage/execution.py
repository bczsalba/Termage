"""All the code used to record code execution."""

# pylint: disable=exec-used

from __future__ import annotations

import builtins
import sys
from contextlib import contextmanager
from io import StringIO
from pathlib import Path
from typing import Any, Generator

import pytermgui as ptg

DEFAULT_WIDTH = 80
DEFAULT_HEIGHT = 24

__all__ = [
    "execute",
    "EXEC_GLOBALS",
    "format_codeblock",
    "patched_stdout_recorder",
    "set_colors",
    "termage",
]


def format_codeblock(block: str) -> tuple[str, str]:
    """Formats a codeblock into display and executed lines."""

    disp_lines, exec_lines = [], []

    lines = block.splitlines()
    indent = " " * (len(lines[0]) - len(lines[0].lstrip()))

    for line in lines:
        line = line.replace(indent, "", 1)
        if line.startswith("&"):
            exec_lines.append(line[1:])
            continue

        exec_lines.append(line)
        disp_lines.append(line)

    return "\n".join(disp_lines), "\n".join(exec_lines)


class TermageNamespace:
    """A simple namespace for exec globals, exposed as `termage`.

    You can use all below methods by referencing the `termage` object
    in termage-run code, which you don't have to import.

    You _usually_ want to hide these lines, as they are generally for
    styling purposes.
    """

    @property
    def terminal(self) -> ptg.Terminal:
        """Returns the current terminal object."""

        return ptg.get_terminal()

    def fit(self, widget: ptg.Widget) -> None:
        """Fits the output terminal around the given widget."""

        self.terminal.size = widget.width, widget.height

    def resize(self, width: int, height: int) -> None:
        """Resizes the output terminal to the given dimensions."""

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
    """Records everything written to stdout, even built is print.

    It does so by monkeypathing `sys.stdout.write` to a custom function,
    which first writes to a custom `Terminal`.

    Args:
        width: The width of the terminal used for the recording.
        height: The height of the terminal used for the recording.

    Returns:
        The recorder object, with all the data written to it.
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
    code: str | None = None,
    file: Path | None = None,
    highlight: bool = False,
    *,
    exec_globals: dict[str, Any] = EXEC_GLOBALS,
) -> None:
    """Executes the given code under a custom context.

    Args:
        code: The Python code to execute.
        file: A file that will be opened, and its contents will
            be added to the executed code *before* the `code` argument.
        highlight: If set, the combined code will only be highlighted using
            PyTermGUI's `highlight_python` function, with that result being
            written to the SVG. Great for quick code screenshots!
        exec_globals: The dictionary that will be passed to `exec`, which
            makes it the global namespace of the context.
    """

    ptg.WindowManager.autorun = False

    exec_globals = exec_globals.copy()
    code = code or ""

    # if module is not None:
    # mod_name, *args = module.split()
    # sys.argv = [*args]
    # out = runpy.run_module(mod_name, init_globals={"sys": sys})
    # print(out)

    if file is not None:
        with open(file, "r", encoding="utf-8") as source:
            code = source.read() + code

    if highlight:
        print(ptg.tim.parse(ptg.highlight_python(code)))
        return exec_globals

    exec(code, exec_globals)
    sys.argv = old_argv

    if "manager" in exec_globals:
        exec_globals["manager"].compositor.draw()

    return exec_globals


def set_colors(foreground: str | None, background: str | None) -> None:
    """Sets the colors that will be used by the terminal."""

    if foreground is not None:
        ptg.Color.default_foreground = ptg.str_to_color(foreground)

    if background is not None:
        ptg.Color.default_background = ptg.str_to_color(background)


def termage(  # pylint: disable=too-many-arguments
    code: str = "",
    include: str | Path | None = None,
    width: int | None = None,
    height: int | None = None,
    title: str = "",
    chrome: bool = True,
    foreground: str | None = None,
    background: str | None = None,
    highlight_only: bool = False,
    save_as: str | Path | None = None,
) -> str:
    """A generalized wrapper for Termage functionality.

    Args:
        code: The code that will be run to generate the file.
        include: A path to a Python file that will be included before `code`.
        width: The output terminal's width.
        height: The output terminal's height.
        title: The output terminal's window title. Has no effect when `chrome`
            is `False`.
        chrome: Shows or hides the window decorations.
        foreground: Sets the default foreground (text) style of the output. Only
            applies to unstyled text.
        background: Sets the output terminal's background color.
        highlight_only: If set, the given code is not run, rather given to the
            `ptg.highlight_python` function.
        save_as: If set, the export will be written to this filepath. The export
            will be returned regardless of this setting.

    Returns:
        The exported SVG file.
    """

    set_colors(foreground, background)
    if include is not None:
        with open(include, "r", encoding="utf-8") as includefile:
            code = includefile.read() + code

    with patched_stdout_recorder(width, height) as recording:
        execute(code=code, highlight=highlight_only)

    export = recording.export_svg(title=title, chrome=chrome)

    if save_as is not None:
        with open(save_as, "w", encoding="utf-8") as save:
            save.write(export)

    return export
