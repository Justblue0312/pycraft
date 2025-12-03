"""Expression nodes.

This module contains nodes for various expressions:
- Call: function/method calls
- BoolOp: boolean operations (and, or)
- UnaryOp: unary operations (not, -, +)
- BinOp: binary operations (+, -, *, /, etc.)
- Compare: comparison operations (==, !=, <, >, etc.)
- Lambda: lambda expressions
- IfExp: conditional expressions (ternary)
- Starred: starred expression (*args)
- Keyword: keyword argument
"""

from dataclasses import dataclass, field

from pycraft.core.base import BaseNode


@dataclass
class Call[T: BaseNode](BaseNode):
    """Represents a function or method call.

    This corresponds to calling a function or method with arguments
    and keyword arguments.

    Example:
        func()
        func(arg1, arg2)
        func(keyword=value)

    Attributes:
        func: The function/method being called
        args: List of positional arguments
        keywords: List of keyword arguments
    """

    func: T | None = None
    args: list[T] = field(default_factory=list)
    keywords: list[T] = field(default_factory=list)


@dataclass
class Keyword[T: BaseNode](BaseNode):
    """Represents a keyword argument in a function call.

    Example:
        func(arg=value)
        func(**kwargs)

    Attributes:
        arg: The argument name (None for **kwargs)
        value: The argument value
    """

    arg: str | None = None
    value: T | None = None


@dataclass
class BoolOp[T: BaseNode](BaseNode):
    """Represents a boolean operation.

    Example:
        x and y
        a or b or c

    Attributes:
        op: The boolean operator (And, Or)
        values: List of operands
    """

    op: T | None = None
    values: list[T] = field(default_factory=list)


@dataclass
class UnaryOp[T: BaseNode](BaseNode):
    """Represents a unary operation.

    Example:
        not x
        -5
        +value

    Attributes:
        op: The unary operator (Not, USub, UAdd)
        operand: The operand
    """

    op: T | None = None
    operand: T | None = None


@dataclass
class BinOp[T: BaseNode](BaseNode):
    """Represents a binary operation.

    Example:
        x + y
        a * b
        c / d

    Attributes:
        left: Left operand
        op: The operator (Add, Sub, Mult, Div, etc.)
        right: Right operand
    """

    left: T | None = None
    op: T | None = None
    right: T | None = None


@dataclass
class Compare[T: BaseNode](BaseNode):
    """Represents a comparison operation.

    Example:
        x == y
        a < b < c
        value in container

    Attributes:
        left: Left operand
        ops: List of comparison operators
        comparators: List of comparison targets
    """

    left: T | None = None
    ops: list[T] = field(default_factory=list)
    comparators: list[T] = field(default_factory=list)


@dataclass
class Lambda[T: BaseNode](BaseNode):
    """Represents a lambda expression.

    Example:
        lambda x: x + 1
        lambda: 42

    Attributes:
        args: Arguments specification
        body: The lambda body expression
    """

    __kw__ = "lambda"
    args: T | None = None
    body: T | None = None


@dataclass
class IfExp[T: BaseNode](BaseNode):
    """Represents a conditional expression (ternary operator).

    Example:
        x if condition else y

    Attributes:
        test: The condition
        body: Expression if true
        orelse: Expression if false
    """

    test: T | None = None
    body: T | None = None
    orelse: T | None = None


@dataclass
class Starred[T: BaseNode](BaseNode):
    """Represents a starred expression.

    Example:
        *args
        [*items]

    Attributes:
        value: The expression being starred
    """

    value: T | None = None


__all__ = [
    "Call",
    "Keyword",
    "BoolOp",
    "UnaryOp",
    "BinOp",
    "Compare",
    "Lambda",
    "IfExp",
    "Starred",
]
