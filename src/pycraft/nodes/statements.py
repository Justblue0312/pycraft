"""Statement nodes.

This module contains nodes for various Python statements:
- Pass: pass statement
- Return: return statement
- Yield: yield statement
- Await: await expression
- Break: break statement
- Continue: continue statement
- Delete: del statement
- Global: global declaration
- Nonlocal: nonlocal declaration
- Comment: code comment
- Expr: expression statement
"""

from dataclasses import dataclass, field

from pycraft.core.base import BaseNode


@dataclass
class Pass(BaseNode):
    """Represents a pass statement.

    This is a null operation - when it is executed, nothing happens.
    Used as a placeholder where a statement is syntactically required.

    Example:
        pass
    """

    __kw__ = "pass"


@dataclass
class Return[T: BaseNode](BaseNode):
    """Represents a return statement.

    This exits a function and optionally returns a value.

    Example:
        return
        return 42
        return x + y

    Attributes:
        value: The value to return (None for bare return)
    """

    __kw__ = "return"
    value: T | None = None


@dataclass
class Yield[T: BaseNode](BaseNode):
    """Represents a yield expression.

    Used in generators to yield values.

    Example:
        yield x
        y = (yield x)

    Attributes:
        value: The value to yield
    """

    __kw__ = "yield"
    value: T | None = None


@dataclass
class Await[T: BaseNode](BaseNode):
    """Represents an await expression.

    Used in async functions to await coroutines.

    Example:
        await coroutine()
        result = await async_function()

    Attributes:
        value: The coroutine to await
    """

    __kw__ = "await"
    value: T | None = None


@dataclass
class Break(BaseNode):
    """Represents a break statement.

    Exits the nearest enclosing loop.

    Example:
        break
    """

    __kw__ = "break"


@dataclass
class Continue(BaseNode):
    """Represents a continue statement.

    Continues to the next iteration of the nearest enclosing loop.

    Example:
        continue
    """

    __kw__ = "continue"


@dataclass
class Delete[T: BaseNode](BaseNode):
    """Represents a del statement.

    Deletes a name, attribute, or subscript.

    Example:
        del x
        del obj.attr
        del list[0]

    Attributes:
        targets: List of nodes to delete
    """

    __kw__ = "del"
    targets: list[T] = field(default_factory=list)


@dataclass
class Global(BaseNode):
    """Represents a global declaration.

    Declares that names are global variables.

    Example:
        global x, y

    Attributes:
        names: List of variable names
    """

    __kw__ = "global"
    names: list[str] = field(default_factory=list)


@dataclass
class Nonlocal(BaseNode):
    """Represents a nonlocal declaration.

    Declares that names are from an enclosing scope.

    Example:
        nonlocal x, y

    Attributes:
        names: List of variable names
    """

    __kw__ = "nonlocal"
    names: list[str] = field(default_factory=list)


@dataclass
class Comment(BaseNode):
    """Represents a comment in the code.

    This corresponds to lines starting with '#' that are ignored by
    the Python interpreter but provide documentation for humans.

    Example:
        # This is a comment

    Attributes:
        text: The comment text (without the # prefix)
    """

    text: str = ""


@dataclass
class Expr[T: BaseNode](BaseNode):
    """Represents an expression statement.

    This corresponds to any expression that stands alone on a line,
    typically used for its side effects rather than its value.

    Example:
        func_call()
        "string expression"
        [1, 2, 3]

    Attributes:
        value: The expression node
    """

    value: T | None = None


__all__ = [
    "Pass",
    "Return",
    "Yield",
    "Await",
    "Break",
    "Continue",
    "Delete",
    "Global",
    "Nonlocal",
    "Comment",
    "Expr",
]
