"""Comprehension nodes.

This module contains nodes for comprehensions and generator expressions:
- ListComp: list comprehension
- SetComp: set comprehension
- DictComp: dictionary comprehension
- GeneratorExp: generator expression
- Comprehension: comprehension clause (for/if)
"""

from dataclasses import dataclass, field

from pycraft.core.base import BaseNode


@dataclass
class Comprehension[T: BaseNode](BaseNode):
    """Represents a comprehension clause (for/if).

    This is used in list/set/dict comprehensions and generator expressions.

    Example:
        for x in items if x > 0

    Attributes:
        target: Loop variable
        iter: Iterable
        ifs: List of filter conditions
        is_async: Whether this is async for
    """

    target: T | None = None
    iter: T | None = None
    ifs: list[T] = field(default_factory=list)
    is_async: int = 0


@dataclass
class ListComp[T: BaseNode, C: Comprehension](BaseNode):
    """Represents a list comprehension.

    Example:
        [x * 2 for x in range(10)]
        [x for x in items if x > 0]

    Attributes:
        elt: Expression for each element
        generators: List of Comprehension clauses
    """

    elt: T | None = None
    generators: list[C] = field(default_factory=list)


@dataclass
class SetComp[T: BaseNode, C: Comprehension](BaseNode):
    """Represents a set comprehension.

    Example:
        {x * 2 for x in range(10)}
        {x for x in items if x > 0}

    Attributes:
        elt: Expression for each element
        generators: List of Comprehension clauses
    """

    elt: T | None = None
    generators: list[C] = field(default_factory=list)


@dataclass
class DictComp[T: BaseNode, C: Comprehension](BaseNode):
    """Represents a dictionary comprehension.

    Example:
        {k: v for k, v in items.items()}
        {x: x**2 for x in range(10) if x % 2 == 0}

    Attributes:
        key: Expression for each key
        value: Expression for each value
        generators: List of Comprehension clauses
    """

    key: T | None = None
    value: T | None = None
    generators: list[C] = field(default_factory=list)


@dataclass
class GeneratorExp[T: BaseNode, C: Comprehension](BaseNode):
    """Represents a generator expression.

    Example:
        (x * 2 for x in range(10))
        (x for x in items if x > 0)

    Attributes:
        elt: Expression for each element
        generators: List of Comprehension clauses
    """

    elt: T | None = None
    generators: list[C] = field(default_factory=list)


__all__ = [
    "Comprehension",
    "ListComp",
    "SetComp",
    "DictComp",
    "GeneratorExp",
]
