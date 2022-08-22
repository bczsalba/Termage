from __future__ import annotations

from .execution import patched_stdout_recorder, execute, set_colors, termage
from .__main__ import main

from . import mkdocs_plugin

__version__ = "0.5.0"
