"""Operator nodes.

This module contains nodes for various operators used in expressions:

Boolean operators:
- And, Or, Not

Comparison operators:
- Eq, NotEq, Lt, LtE, Gt, GtE, Is, IsNot, In, NotIn

Binary operators:
- Add, Sub, Mult, Div, FloorDiv, Mod, Pow, MatMult
- LShift, RShift, BitOr, BitXor, BitAnd

Unary operators:
- UAdd, USub, Invert
"""

from dataclasses import dataclass

from pycraft.core.base import BaseNode


# Boolean operators
@dataclass
class And(BaseNode):
    """Represents boolean AND operator."""

    pass


@dataclass
class Or(BaseNode):
    """Represents boolean OR operator."""

    pass


@dataclass
class Not(BaseNode):
    """Represents boolean NOT operator."""

    pass


# Comparison operators
@dataclass
class Eq(BaseNode):
    """Represents == operator."""

    pass


@dataclass
class NotEq(BaseNode):
    """Represents != operator."""

    pass


@dataclass
class Lt(BaseNode):
    """Represents < operator."""

    pass


@dataclass
class LtE(BaseNode):
    """Represents <= operator."""

    pass


@dataclass
class Gt(BaseNode):
    """Represents > operator."""

    pass


@dataclass
class GtE(BaseNode):
    """Represents >= operator."""

    pass


@dataclass
class Is(BaseNode):
    """Represents 'is' operator."""

    __kw__ = "is"


@dataclass
class IsNot(BaseNode):
    """Represents 'is not' operator."""

    __kw__ = "is not"


@dataclass
class In(BaseNode):
    """Represents 'in' operator."""

    __kw__ = "in"


@dataclass
class NotIn(BaseNode):
    """Represents 'not in' operator."""

    __kw__ = "not in"


# Binary operators
@dataclass
class Add(BaseNode):
    """Represents + operator."""

    pass


@dataclass
class Sub(BaseNode):
    """Represents - operator."""

    pass


@dataclass
class Mult(BaseNode):
    """Represents * operator."""

    pass


@dataclass
class Div(BaseNode):
    """Represents / operator."""

    pass


@dataclass
class FloorDiv(BaseNode):
    """Represents // operator."""

    pass


@dataclass
class Mod(BaseNode):
    """Represents % operator."""

    pass


@dataclass
class Pow(BaseNode):
    """Represents ** operator."""

    pass


@dataclass
class MatMult(BaseNode):
    """Represents @ operator (matrix multiplication)."""

    pass


@dataclass
class LShift(BaseNode):
    """Represents << operator (left shift)."""

    pass


@dataclass
class RShift(BaseNode):
    """Represents >> operator (right shift)."""

    pass


@dataclass
class BitOr(BaseNode):
    """Represents | operator (bitwise or)."""

    pass


@dataclass
class BitXor(BaseNode):
    """Represents ^ operator (bitwise xor)."""

    pass


@dataclass
class BitAnd(BaseNode):
    """Represents & operator (bitwise and)."""

    pass


# Unary operators
@dataclass
class UAdd(BaseNode):
    """Represents unary + operator."""

    pass


@dataclass
class USub(BaseNode):
    """Represents unary - operator."""

    pass


@dataclass
class Invert(BaseNode):
    """Represents ~ operator (bitwise not)."""

    pass


__all__ = [
    # Boolean
    "And",
    "Or",
    "Not",
    # Comparison
    "Eq",
    "NotEq",
    "Lt",
    "LtE",
    "Gt",
    "GtE",
    "Is",
    "IsNot",
    "In",
    "NotIn",
    # Binary
    "Add",
    "Sub",
    "Mult",
    "Div",
    "FloorDiv",
    "Mod",
    "Pow",
    "MatMult",
    "LShift",
    "RShift",
    "BitOr",
    "BitXor",
    "BitAnd",
    # Unary
    "UAdd",
    "USub",
    "Invert",
]
