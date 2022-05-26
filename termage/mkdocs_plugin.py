"""A mkdocs plugin, implementing Termage."""

import re
import sys
from pathlib import Path
from dataclasses import dataclass, fields

from mkdocs.plugins import BasePlugin

from .execution import patched_stdout_recorder, execute, set_colors

RE_BLOCK = re.compile(r"([^\n]*)\`\`\`termage(-svg)?(.*?)\n([\s\S]*?)\`\`\`")

OUTPUT_BLOCK_TEMPLATE = """
=== "{code_tab_name}"

    ```py
{code}
    ```

=== "{svg_tab_name}"
{svg}{{ align=center }}
"""

STDOUT_WRITE = sys.stdout.write
OUTPUT_SVG_TEMPLATE = "{indent}![{alt}]({path}){{ align=center }}"

DEFAULT_OPTS = {
    "width": 80,
    "height": 20,
    "tabs": ("Python", "Output"),
    "foreground": "#dddddd",
    "background": "#212121",
    "title": "",
    "include": None,
    "highlight": False,
}


@dataclass
class TermageOptions:
    """Options passed into the Termage plugin."""

    title: str
    width: int
    height: int
    include: str
    foreground: str
    background: str
    tabs: tuple[str, str]
    highlight: bool


class TermagePlugin(BasePlugin):
    """An mkdocs plugin for Termage."""

    def __init__(self) -> None:
        """Sets the initial SVG count."""

        self._svg_count = 0

    def _get_next_path(self) -> str:
        """Gets the next SVG path."""

        self._svg_count += 1

        return f"assets/termage_{self._svg_count}.svg"

    @staticmethod
    def _parse_opts(options: str) -> TermageOptions:
        """Parses the options given to a block."""

        opt_dict = DEFAULT_OPTS.copy()

        for option in re.split(r"(?<!\\) ", options):
            if len(option) == 0:
                continue

            try:
                key, value = option.split("=")
            except ValueError as error:
                raise ValueError(f"Invalid key=value pair {option!r}.") from error

            value = value.replace("\\", "")

            if key not in DEFAULT_OPTS:
                raise ValueError(
                    f"Unexpected key {key!r}. Please choose from {list(opt_dict)!r}."
                )

            original = opt_dict[key]
            if isinstance(original, bool):
                value = value.lower() in ("1", "true", "yes")

            elif isinstance(original, int):
                value = int(value)

            elif isinstance(opt_dict[key], tuple):
                value = tuple(value.split(","))

            opt_dict[key] = value

        return TermageOptions(**opt_dict)  # type: ignore

    def _replace_codeblock(self, matchobj) -> str:
        """Replaces a codeblock with Termage content."""

        indent, svg_only, options, code = matchobj.groups()

        if indent.endswith("\\"):
            indent = indent.replace("\\", "")
            return f"""\
{indent}```termage {options}
{code}```"""

        opts = self._parse_opts(options)

        if opts.include is not None:
            with open(opts.include, "r", encoding="utf-8") as include_file:
                include = ""
                for line in include_file.readlines():
                    include += f"{indent}{line}"

                code = include + code

        exec_code = ""
        display_code = []

        for line in code.splitlines():
            line = line[len(indent) :]

            if line.startswith("&"):
                line = line.replace("&", "", 1)
            else:
                display_code.append(line)

            # if line == "":
            #     continue

            exec_code += line + "\n"

        set_colors(opts.foreground, opts.background)
        with patched_stdout_recorder(opts.width, opts.height) as recorder:
            execute(module=None, code=exec_code, highlight=opts.highlight)

        path = self._get_next_path()
        recorder.save_svg(str(Path("docs") / path), title=opts.title)

        STDOUT_WRITE(f"Creating {path} with {opts.title=}.\n")

        if svg_only:
            return OUTPUT_SVG_TEMPLATE.format(indent=indent, alt=opts.title, path=path)

        # Re-indent template to match original indentation
        template = ""
        for line in OUTPUT_BLOCK_TEMPLATE.splitlines():
            if line not in ("{code}", "{svg}{{ align=center }}"):
                line = indent + line

            template += line + "\n"

        indent += 4 * " "
        return template.format(
            svg=f"{indent}![]({path})",
            code_tab_name=opts.tabs[0],
            svg_tab_name=opts.tabs[1],
            code="\n".join(indent + line for line in display_code),
        )

    def on_page_markdown(  # pylint: disable=unused-argument
        self, markdown, page, files, config
    ) -> str:
        """Replaces the termage markdown syntax."""

        return RE_BLOCK.sub(self._replace_codeblock, markdown)
