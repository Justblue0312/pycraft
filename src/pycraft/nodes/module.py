"""Additional module node.

This module contains the Module node which represents a Python file/module.
"""

from dataclasses import dataclass, field

from pycraft.core.base import BaseNode


@dataclass
class Module[T: BaseNode](BaseNode):
    """Represents a Python module (a file containing Python code).

    This serves as the top-level container for all code in a Python file,
    containing functions, classes, variables, and other statements.

    Attributes:
        body: List of top-level statements in the module
    """

    body: list[T] = field(default_factory=list)


__all__ = ["Module"]
