from __future__ import annotations

import re
import os
import tempfile
from typing import Match
from pathlib import Path
from dataclasses import dataclass

from mkdocs.livereload import LiveReloadServer
from mkdocs.plugins import BasePlugin
from mkdocs.config.config_options import Type

from .execution import execute, format_codeblock, patched_stdout_recorder, set_colors

RE_BLOCK = re.compile(r"(([^\n]*)\`\`\`termage(-svg)?(.*?)\n([\s\S]*?)\`\`\`)")
TAB_TEMPLATE = """
=== "{code_tab}"
    ```python {extra_opts}
{code}
    ```

=== "{svg_tab}"
    {content}
"""

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


def indent(text: str, amount: int) -> str:
    """Indents the text by the given amount.

    Works multiline too!"""

    pad = amount * " "
    return "\n".join(pad + line for line in text.splitlines())


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

    config_scheme = (
        ("write_files", Type(bool, default=False)),
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

        base = self.config["path"]
        name_template = self.config["name_template"]
        name = name_template.format(
            count=self._svg_count,
            title=str(title),
        )

        return f"{base}/{name}"

    def parse_options(self, options: str) -> TermageOptions:
        """Parses the options given to a block."""

        opt_dict = {key: self.config.get(key, None) for key in OPTS}

        extra_opts = ""

        for option in re.split(r"(?<!\\) ", options):
            if len(option) == 0:
                continue

            try:
                key, value = option.split("=")
            except ValueError:
                extra_opts += " " + option
                continue

            value = value.replace("\\", "")

            if key not in opt_dict:
                extra_opts += " " + option
                continue

            original = opt_dict[key]
            if isinstance(original, bool):
                value = value.lower() in ("1", "true", "yes")

            elif isinstance(original, int):
                value = int(value)

            elif isinstance(opt_dict[key], list):
                value = value.split(",")

            opt_dict[key] = value

        return TermageOptions(**opt_dict), extra_opts  # type: ignore

    def replace(self, matchobj: Match) -> str:
        full, indentation, svg_only, options, code = matchobj.groups()
        indent_len = len(indentation)

        if indentation.endswith("\\"):
            return full

        opts, extra_opts = self.parse_options(options)
        set_colors(opts.foreground, opts.background)

        if opts.include is not None:
            with open(opts.include, "r") as includefile:
                code = includefile.read() + code

            opts.title = opts.title or opts.include

        code_disp, code_exec = format_codeblock(code)
        code_exec = "\n".join(
            line.replace(indentation, "", 1) for line in code_exec.splitlines()
        )

        with patched_stdout_recorder(opts.width, opts.height) as recording:
            glob = execute(code=code_exec)

        svg = (
            recording.export_svg(
                title=opts.title,
                chrome=opts.chrome,
                prefix=f"termage-{self._svg_count}-",
                inline_styles=True,
            )
            .replace("_", "\_")
            .replace("`", r"\`")
            .replace("*", r"\*")
        )
        self._svg_count += 1
        style = "margin-top: -1em;" if not opts.chrome else ""

        if self.config["write_files"]:
            filepath = self._get_next_path(opts.title)
            with open(Path("docs") / filepath, "w") as export:
                export.write(svg)

            img_tag = (
                f"<img alt='{opts.title}' src='/{filepath}' style='{style}'></img>"
            )

            if svg_only:
                return img_tag

            return indent(
                TAB_TEMPLATE.format(
                    code_tab=opts.tabs[0],
                    extra_opts=extra_opts,
                    svg_tab=opts.tabs[1],
                    code=indent(code_disp, amount=4),
                    content=img_tag,
                ),
                amount=indent_len,
            )

        if style != "":
            svg = svg[: len("<svg ")] + f"style='{style}' " + svg[len("<svg ") :]

        if svg_only:
            return svg

        return indent(
            TAB_TEMPLATE.format(
                code_tab=opts.tabs[0],
                extra_opts=extra_opts,
                svg_tab=opts.tabs[1],
                code=indent(code_disp, amount=4),
                content=indent(svg, amount=indent_len),
            ),
            amount=indent_len,
        )

    def on_page_markdown(  # pylint: disable=unused-argument
        self, markdown, page, files, config
    ) -> str:
        """Replaces the termage markdown syntax."""

        return RE_BLOCK.sub(self.replace, markdown)
