"""A mkdocs plugin, implementing Termage."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from dataclasses import dataclass, fields
from typing import Match

from mkdocs.plugins import BasePlugin
from mkdocs.config.config_options import Type
from mkdocs.structure.files import Files, File

from .execution import patched_stdout_recorder, execute, set_colors

RE_BLOCK = re.compile(r"([^\n]*)\`\`\`termage(-svg)?(.*?)\n([\s\S]*?)\`\`\`")

OUTPUT_BLOCK_TEMPLATE = """
=== "{code_tab_name}"

    ```py
{code}
    ```

=== "{svg_tab_name}"
{svg}
"""

STDOUT_WRITE = sys.stdout.write

OUTPUT_SVG_TEMPLATE = """\
{indent}<p align="center">
{indent}<img src="{src}" alt="{alt}" {style}>
{indent}</p>"""

OPTS = [
    "width",
    "height",
    "tabs",
    "foreground",
    "background",
    "chrome",
    "title",
    "include",
    "highlight",
]


@dataclass
class TermageOptions:
    """Options passed into the Termage plugin."""

    title: str
    width: int
    height: int
    include: str
    foreground: str
    background: str
    chrome: bool
    tabs: tuple[str, str]
    highlight: bool


class TermagePlugin(BasePlugin):
    """An mkdocs plugin for Termage."""

    """
    termage:
        path: "docs/assets"
        template: "termage_{count}.svg"
    """

    config_scheme = (
        ("path", Type(str, default="assets")),
        ("name_template", Type(str, default="termage_{count}.svg")),
        ("background", Type(str, default="#212121")),
        ("foreground", Type(str, default="#dddddd")),
        ("tabs", Type(list, default=["Python", "Output"])),
        ("chrome", Type(bool, default=True)),
        ("width", Type(int, default=80)),
        ("height", Type(int, default=24)),
    )

    def __init__(self) -> None:
        """Sets the initial SVG count."""

        self._svg_count = 0

    def _get_next_path(self, title: str | None) -> str:
        """Gets the next SVG path."""

        self._svg_count += 1

        base = self.config["path"]
        name_template = self.config["name_template"]
        name = name_template.format(
            count=self._svg_count,
            title=str(title),
        )

        return f"{base}/{name}"

    def _parse_opts(self, options: str) -> TermageOptions:
        """Parses the options given to a block."""

        opt_dict = {key: self.config.get(key, None) for key in OPTS}

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

            original = opt_dict[key]
            if isinstance(original, bool):
                value = value.lower() in ("1", "true", "yes")

            elif isinstance(original, int):
                value = int(value)

            elif isinstance(opt_dict[key], list):
                value = value.split(",")

            opt_dict[key] = value

        return TermageOptions(**opt_dict)  # type: ignore

    def _replace_codeblock(self, matchobj: Match) -> str:
        """Replaces a codeblock with Termage content."""

        indent, svg_only, options, code = matchobj.groups()

        if indent.endswith("\\"):
            indent = indent.replace("\\", "")
            return f"""\
{indent}```termage{svg_only or ''}{options}
{code}```"""

        opts = self._parse_opts(options)

        if opts.include is not None:
            with open(opts.include, "r", encoding="utf-8") as include_file:
                include = ""
                for line in include_file.readlines():
                    include += f"{indent}{line}"

                code = include + code

            if opts.title == "":
                opts.title = opts.include

        exec_code = ""
        display_code = []

        for line in code.splitlines():
            line = line[len(indent) :]

            if line.startswith("&"):
                line = line.replace("&", "", 1)
            else:
                display_code.append(line)

            exec_code += line + "\n"

        set_colors(opts.foreground, opts.background)
        with patched_stdout_recorder(opts.width, opts.height) as recorder:
            execute(module=None, code=exec_code, highlight=opts.highlight)

        name = self._get_next_path(title=opts.title)
        path = Path("docs") / name
        export = recorder.export_svg(title=opts.title, chrome=opts.chrome)

        existing = ""
        if os.path.exists(path):
            with open(path, "r") as existing_file:
                existing = existing_file.read()

        if existing != export:
            with open(path, "w") as new:
                new.write(export)

        # Point the filename back to root
        name = "/" + name

        style = 'style="margin-top: -1em;"' if not opts.chrome else ""

        if svg_only:
            return OUTPUT_SVG_TEMPLATE.format(
                indent=indent, alt=opts.title, src=name, style=style
            )

        # Re-indent template to match original indentation
        template = ""
        for line in OUTPUT_BLOCK_TEMPLATE.splitlines():
            if line not in ("{code}", "{svg}"):
                line = indent + line

            template += line + "\n"

        indent += 4 * " "

        return template.format(
            code_tab_name=opts.tabs[0],
            svg_tab_name=opts.tabs[1],
            code="\n".join(indent + line for line in display_code),
            svg=OUTPUT_SVG_TEMPLATE.format(
                indent=indent, alt=opts.title, src=name, style=style
            ),
        )

    def on_page_markdown(  # pylint: disable=unused-argument
        self, markdown, page, files, config
    ) -> str:
        """Replaces the termage markdown syntax."""

        return RE_BLOCK.sub(self._replace_codeblock, markdown)
