"""Control flow nodes.

This module contains nodes for control flow statements:
- If: if statement
- Elif: elif clause
- Else: else clause
- Match: match statement (Python 3.10+)
- MatchCase: case clause in match
"""

from dataclasses import dataclass, field

from pycraft.core.base import BaseNode


@dataclass
class If[T: BaseNode](BaseNode):
    """Represents an if statement.

    Example:
        if condition:
            do_something()

        if x > 0:
            positive()
        elif x < 0:
            negative()
        else:
            zero()

    Attributes:
        test: The condition to test
        body: Statements to execute if true
        or_else: Elif/else clauses or statements
    """

    __kw__ = "if"
    test: T | None = None
    body: list[T] = field(default_factory=list)
    or_else: list[T] = field(default_factory=list)


@dataclass
class Elif[T: BaseNode](BaseNode):
    """Represents an elif clause.

    This is used within an if statement's or_else.

    Example:
        elif condition:
            do_something()

    Attributes:
        test: The condition to test
        body: Statements to execute if true
    """

    __kw__ = "elif"
    test: T | None = None
    body: list[T] = field(default_factory=list)


@dataclass
class Else[T: BaseNode](BaseNode):
    """Represents an else clause.

    This is used within an if statement's or_else.

    Example:
        else:
            do_something()

    Attributes:
        body: Statements to execute
    """

    __kw__ = "else"
    body: list[T] = field(default_factory=list)


@dataclass
class Match[T: BaseNode](BaseNode):
    """Represents a match statement (Python 3.10+).

    Example:
        match value:
            case 1:
                print("one")
            case 2:
                print("two")
            case _:
                print("other")

    Attributes:
        subject: The value to match against
        cases: List of MatchCase nodes
    """

    __kw__ = "match"
    subject: T | None = None
    cases: list[T] = field(default_factory=list)


@dataclass
class MatchCase[T: BaseNode](BaseNode):
    """Represents a case clause in a match statement.

    Example:
        case pattern:
            do_something()

        case 1 | 2 | 3:
            print("small number")

    Attributes:
        pattern: The pattern to match
        guard: Optional guard condition
        body: Statements to execute if matched
    """

    __kw__ = "case"
    pattern: T | None = None
    guard: T | None = None
    body: list[T] = field(default_factory=list)


__all__ = [
    "If",
    "Elif",
    "Else",
    "Match",
    "MatchCase",
]
