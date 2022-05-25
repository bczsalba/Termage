from __future__ import annotations

import re
import builtins
from io import StringIO
from pathlib import Path

from mkdocs.plugins import BasePlugin

import pytermgui as ptg

__version__ = "0.1.0"

RE_BLOCK = re.compile(r"([^\n]*)\`\`\`termage(-svg)?(.*?)\n([\s\S]*?)\`\`\`")

OUTPUT_BLOCK_TEMPLATE = """
=== "{code_tab_name}"

    ```py
{code}
    ```

=== "{svg_tab_name}"
{svg}{{ align=center }}
"""

OUTPUT_SVG_TEMPLATE = "{indent}![{alt}]({path}){{ align=center }}"


def _get_terminal_from_opts(width: int, height: int) -> ptg.Terminal:
    """Creates a terminal with the size options."""

    return ptg.Terminal(stream=StringIO(), size=(width, height))


def _find_indent(line: str) -> int:
    """Finds the indentation of the line."""

    return len(line) - len(line.lstrip())


ptg.WindowManager.autorun = False


class TermagePlugin(BasePlugin):
    """The Termage plugin class."""

    def __init__(self, *args, **kwargs) -> None:
        """Initializes the plugin."""

        super().__init__(*args, **kwargs)

        self._svg_count = 0

    @staticmethod
    def _parse_options(options: str) -> dict[str, int | str]:
        """Parses option strings.

        Each option follows the pattern `key=value`. Spaces are only allowed when escaped.
        """

        opt_dict = {
            "width": 80,
            "height": 20,
            "tabs": ("Python", "Output"),
            "foreground": "#dddddd",
            "background": "#212121",
            "title": "",
            "include": None,
        }

        for option in re.split(r"(?<!\\) ", options):
            if len(option) == 0:
                continue

            try:
                key, value = option.split("=")
            except ValueError as error:
                raise ValueError(f"Invalid key=value pair {option!r}.") from error

            value = value.replace("\\", "")

            if key not in opt_dict:
                raise ValueError(
                    f"Unexpected key {key!r}. Please choose from {list(opt_dict)!r}."
                )

            if value.isdigit():
                value = int(value)

            elif isinstance(opt_dict[key], tuple):
                value = tuple(value.split(","))

            opt_dict[key] = value

        return opt_dict

    def _handle_options(
        self, options: str, indent: str
    ) -> tuple[ptg.Terminal, str, str | None]:
        """Handles the options provided within the code block.

        Returns:
            A tuple of the custom terminal instance, and the contents of the file
            passed with the `include` option, or None if not given.
        """

        opt_dict = self._parse_options(options)

        include = None
        if opt_dict["include"] is not None:
            with open(opt_dict["include"], "r", encoding="utf-8") as include_file:
                include = ""

                for line in include_file.readlines():
                    include += f"{indent}{line}"

        terminal = _get_terminal_from_opts(opt_dict["width"], opt_dict["height"])

        ptg.set_global_terminal(terminal)
        assert terminal is ptg.get_terminal()

        ptg.Color.default_foreground = ptg.str_to_color(
            opt_dict["foreground"], is_background=True
        )
        ptg.Color.default_background = ptg.str_to_color(
            opt_dict["background"], is_background=True
        )

        return terminal, opt_dict["title"], opt_dict["tabs"], include

    def _get_next_path(self) -> str:
        """Gets the next SVG path."""

        self._svg_count += 1

        return f"assets/termage_{self._svg_count}.svg"

    def _replace_codeblock(self, matchobj) -> str:
        """Replaces a codeblock with the Termage content."""

        indent, svg_only, options, code = matchobj.groups()

        if indent.endswith("\\"):
            indent = indent.replace("\\", "")
            return f"""\
{indent}```termage {options}
{code}```"""

        terminal, title, (tab1, tab2), include = self._handle_options(options, indent)

        if include is not None:
            code = include + code

        buffer = ""
        code_filtered = []

        exec_globals = {
            "__name__": "__main__",
            "__doc__": None,
            "__package__": None,
            "__annotations__": {},
            "__builtins__": builtins,
            "print": ptg.tim.print,
        }

        lines = code.splitlines()

        with terminal.record() as recording:
            for line in lines:
                line = line[len(indent) :]

                if line.startswith("&"):
                    line = line.replace("&", "", 1)
                else:
                    code_filtered.append(line)

                if line == "":
                    continue

                buffer += line + "\n"

            code_obj = compile(buffer, "<string>", "exec")
            exec(code_obj, exec_globals)

            if "manager" in exec_globals:
                exec_globals["manager"].compositor.draw()

        path = self._get_next_path()
        recording.save_svg(str(Path("docs") / path), title=title)

        code_indent = (len(indent) + 4) * " "

        if svg_only:
            return OUTPUT_SVG_TEMPLATE.format(indent=indent, alt=title, path=path)

        template = ""
        for line in OUTPUT_BLOCK_TEMPLATE.splitlines():
            if line not in ("{code}", "{svg}{{ align=center }}"):
                line = indent + line

            template += line + "\n"

        block = template.format(
            code_tab_name=tab1,
            svg_tab_name=tab2,
            code="\n".join(code_indent + line for line in code_filtered),
            svg=f"{code_indent}![]({path})",
        )

        return block

    def on_page_markdown(self, markdown, page, files, config) -> str:
        """Replaces the termage markdown syntax."""

        subbed = RE_BLOCK.sub(self._replace_codeblock, markdown)

        return subbed
