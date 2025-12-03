"""Exception handling nodes.

This module contains nodes for exception handling:
- Try: try statement
- ExceptHandler: except clause
- Raise: raise statement
- Assert: assert statement
- Finally: finally clause (embedded in Try node)
"""

from dataclasses import dataclass, field

from pycraft.core.base import BaseNode


@dataclass
class Try[T: BaseNode](BaseNode):
    """Represents a try statement.

    Example:
        try:
            risky_operation()
        except ValueError as e:
            handle_error(e)
        finally:
            cleanup()

    Attributes:
        body: Statements in try block
        handlers: List of ExceptHandler nodes
        orelse: Optional else block (no exception)
        finalbody: Optional finally block
    """

    __kw__ = "try"
    body: list[T] = field(default_factory=list)
    handlers: list[T] = field(default_factory=list)
    or_else: list[T] = field(default_factory=list)
    finalbody: list[T] = field(default_factory=list)


@dataclass
class ExceptHandler[T: BaseNode](BaseNode):
    """Represents an except clause in a try statement.

    Example:
        except ValueError:
            handle()

        except (TypeError, KeyError) as e:
            handle(e)

    Attributes:
        type: Exception type to catch (None for bare except)
        name: Variable name to bind exception to
        body: Statements in except block
    """

    __kw__ = "except"
    type: T | None = None
    name: str | None = None
    body: list[T] = field(default_factory=list)


@dataclass
class Finally[T: BaseNode](BaseNode):
    """Represents a finally clause.

    This is typically embedded in a Try node's finalbody.

    Example:
        finally:
            cleanup()

    Attributes:
        body: Statements in finally block
    """

    __kw__ = "finally"
    body: list[T] = field(default_factory=list)


@dataclass
class Raise[T: BaseNode](BaseNode):
    """Represents a raise statement.

    Example:
        raise ValueError("error message")
        raise
        raise CustomError() from original_error

    Attributes:
        exc: Exception to raise
        cause: Optional cause for chained exceptions
    """

    __kw__ = "raise"
    exc: T | None = None
    cause: T | None = None


@dataclass
class Assert[T: BaseNode](BaseNode):
    """Represents an assert statement.

    Example:
        assert condition
        assert x > 0, "x must be positive"

    Attributes:
        test: Condition to assert
        msg: Optional error message
    """

    __kw__ = "assert"
    test: T | None = None
    msg: T | None = None


__all__ = [
    "Try",
    "ExceptHandler",
    "Finally",
    "Raise",
    "Assert",
]
