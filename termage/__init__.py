from __future__ import annotations

from .execution import patched_stdout_recorder, execute, set_colors
from .__main__ import main

__version__ = "0.3.0"


def termage(code: str, **kwargs) -> str | None:
    """Executes CLI with the given (long-form) arguments.

    To see all arguments, check out the docs.

    Returns:
        The generated SVG if the `out` parameter is not given, else
        None, after writing output to `out`.
    """

    args = [code]
    for key, value in kwargs.items():
        args.extend([f"--{key}", str(value)])

    main(args)
