"""Loop nodes.

This module contains nodes for loop statements:
- For: for loop
- AsyncFor: async for loop
- While: while loop
"""

from dataclasses import dataclass, field

from pycraft.core.base import BaseNode


@dataclass
class For[T: BaseNode](BaseNode):
    """Represents a for loop.

    Example:
        for item in items:
            process(item)

        for i in range(10):
            print(i)

    Attributes:
        target: Loop variable
        iter: Iterable to loop over
        body: Statements in loop body
        orelse: Optional else clause (executed if no break)
    """

    __kw__ = "for"
    target: T | None = None
    iter: T | None = None
    body: list[T] = field(default_factory=list)
    or_else: list[T] = field(default_factory=list)


@dataclass
class AsyncFor[T: BaseNode](BaseNode):
    """Represents an async for loop.

    Example:
        async for item in async_items():
            await process(item)

    Attributes:
        target: Loop variable
        iter: Async iterable to loop over
        body: Statements in loop body
        orelse: Optional else clause
    """

    __kw__ = "async for"
    target: T | None = None
    iter: T | None = None
    body: list[T] = field(default_factory=list)
    or_else: list[T] = field(default_factory=list)


@dataclass
class While[T: BaseNode](BaseNode):
    """Represents a while loop.

    Example:
        while condition:
            do_something()

        while x > 0:
            x -= 1

    Attributes:
        test: Loop condition
        body: Statements in loop body
        orelse: Optional else clause (executed if no break)
    """

    __kw__ = "while"
    test: T | None = None
    body: list[T] = field(default_factory=list)
    or_else: list[T] = field(default_factory=list)


__all__ = [
    "For",
    "AsyncFor",
    "While",
]
