"""Generate SVGs from any Python code, even in your documentation."""

from __future__ import annotations

from . import mkdocs_plugin
from .__main__ import main
from .execution import execute, patched_stdout_recorder, set_colors, termage

__version__ = "0.5.0"
