"""Context manager nodes.

This module contains nodes for context managers:
- With: with statement
- WithItem: individual item in with statement
"""

from dataclasses import dataclass, field

from pycraft.core.base import BaseNode


@dataclass
class With[T: BaseNode](BaseNode):
    """Represents a with statement.

    Example:
        with open("file.txt") as f:
            content = f.read()

        with lock, open("log.txt") as log:
            log.write("message")

    Attributes:
        items: List of WithItem nodes
        body: Statements in with block
    """

    __kw__ = "with"
    items: list[T] = field(default_factory=list)
    body: list[T] = field(default_factory=list)


@dataclass
class WithItem[T: BaseNode](BaseNode):
    """Represents a single item in a with statement.

    Example:
        open("file.txt") as f

    Attributes:
        context_expr: The context manager expression
        optional_vars: Variable to bind to (as clause)
    """

    context_expr: T | None = None
    optional_vars: T | None = None


__all__ = [
    "With",
    "WithItem",
]
