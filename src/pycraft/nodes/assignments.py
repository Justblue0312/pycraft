"""Assignment nodes.

This module contains nodes for various assignment types:
- Assign: regular assignment (x = value)
- AugAssign: augmented assignment (x += value)
- AnnAssign: annotated assignment (x: int = value)
"""

from dataclasses import dataclass, field

from pycraft.core.base import BaseNode


@dataclass
class Assign[T: BaseNode](BaseNode):
    """Represents an assignment statement.

    This corresponds to the '=' operator used to assign values to variables.

    Example:
        x = 5
        name = "John"
        a, b = 1, 2

    Attributes:
        targets: List of target nodes being assigned to
        value: The value being assigned
        comment: Optional inline comment
    """

    targets: list[T] = field(default_factory=list)
    value: T | None = None
    comment: str | None = None


@dataclass
class AugAssign[T: BaseNode](BaseNode):
    """Represents an augmented assignment statement.

    This corresponds to operators like +=, -=, *=, /=, etc. that combine
    an arithmetic operation with assignment.

    Example:
        x += 1
        y *= 2
        z -= 5

    Attributes:
        target: The target node being modified
        op: The operation node (Add, Sub, Mult, etc.)
        value: The value to apply the operation with
        comment: Optional inline comment
    """

    target: T | None = None
    op: T | None = None
    value: T | None = None
    comment: str | None = None


@dataclass
class AnnAssign[T: BaseNode](BaseNode):
    """Represents an annotated assignment statement.

    This corresponds to variable assignments with type annotations,
    using the ':' syntax to specify the variable's type.

    Example:
        name: str = "value"
        count: int
        items: list[str] = []

    Attributes:
        target: The target name being assigned
        annotation: The type annotation node
        simple: 1 if simple name, 0 if complex target
        comment: Optional inline comment
        value: Optional initial value
    """

    target: str = ""
    annotation: T | None = None
    simple: int = 1
    comment: str | None = None
    value: T | None = None


__all__ = [
    "Assign",
    "AugAssign",
    "AnnAssign",
]
