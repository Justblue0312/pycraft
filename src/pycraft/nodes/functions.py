"""Function and class definition nodes.

This module contains nodes for defining functions and classes:
- FunctionDef: function definition
- AsyncFunctionDef: async function definition
- Arguments: function arguments specification
- Arg: single function argument
- ClassDef: class definition
- TypeParam: type parameter (for generics)
"""

from dataclasses import dataclass, field

from pycraft.core.base import BaseNode


@dataclass
class Arg[T: BaseNode](BaseNode):
    """Represents a single function argument.

    Example:
        def func(x, y: int, z=default):
            katze..

    Attributes:
        arg: The argument name
        annotation: Optional type annotation
        default: Optional default value
    """

    arg: str = ""
    annotation: T | None = None
    default: T | None = None


@dataclass
class Arguments[T: BaseNode, A: Arg](BaseNode):
    """Represents function arguments specification.

    This includes positional, keyword-only, and variable arguments.

    Example:
        def func(a, b, *args, c, d=1, **kwargs):
            katze..

    Attributes:
        args: List of regular arguments
        vararg: *args parameter
        kwonlyargs: Keyword-only arguments
        kw_defaults: Defaults for keyword-only args
        kwarg: **kwargs parameter
        defaults: Default values for regular args
        posonlyargs: Positional-only arguments (Python 3.8+)
    """

    args: list[A] = field(default_factory=list)
    vararg: A | None = None
    kwonlyargs: list[A] = field(default_factory=list)
    kw_defaults: list[T | None] = field(default_factory=list)
    kwarg: A | None = None
    defaults: list[T] = field(default_factory=list)
    posonlyargs: list[A] = field(default_factory=list)


@dataclass
class FunctionDef[T: BaseNode, A: Arguments](BaseNode):
    """Represents a function definition.

    Example:
        def my_function(x: int) -> str:
            return str(x)

        @decorator
        def decorated_func():
            pass

    Attributes:
        name: Function name
        args: Arguments specification
        body: List of statements in function body
        returns: Return type annotation
        decorator_list: List of decorators
        type_params: Type parameters for generic functions
    """

    __kw__ = "def"
    name: str = ""
    args: A | None = None
    body: list[T] = field(default_factory=list)
    returns: T | None = None
    decorator_list: list[T] = field(default_factory=list)
    type_params: list[T] = field(default_factory=list)


@dataclass
class AsyncFunctionDef[T: BaseNode, A: Arguments](BaseNode):
    """Represents an async function definition.

    Example:
        async def my_async_function():
            await some_coroutine()

    Attributes:
        name: Function name
        args: Arguments specification
        body: List of statements in function body
        returns: Return type annotation
        decorator_list: List of decorators
        type_params: Type parameters for generic functions
    """

    __kw__ = "async def"
    name: str = ""
    args: A | None = None
    body: list[T] = field(default_factory=list)
    returns: T | None = None
    decorator_list: list[T] = field(default_factory=list)
    type_params: list[T] = field(default_factory=list)


@dataclass
class ClassDef[T: BaseNode](BaseNode):
    """Represents a Python class definition.

    This corresponds to the 'class' keyword in Python, used to define a new class
    with optional inheritance from base classes and class body containing methods
    and attributes.

    Example:
        class MyClass:
            pass

        class Child(Parent1, Parent2):
            def method(self):
                pass

    Attributes:
        name: Class name
        bases: List of base classes
        keywords: List of keyword arguments (e.g., metaclass)
        body: List of class body statements
        decorators: List of class decorators
    """

    __kw__ = "class"
    name: str = ""
    bases: list[T] = field(default_factory=list)
    keywords: list[T] = field(default_factory=list)
    body: list[T] = field(default_factory=list)
    decorators: list[T] = field(default_factory=list)


@dataclass
class TypeParam[T: BaseNode](BaseNode):
    """Represents a type parameter for generic classes/functions.

    Example:
        class Stack[T]:
            katze..

        def identity[T](x: T) -> T:
            return x

    Attributes:
        name: Type parameter name
        bound: Optional bound type
    """

    name: str = ""
    bound: T | None = None


__all__ = [
    "Arg",
    "Arguments",
    "FunctionDef",
    "AsyncFunctionDef",
    "ClassDef",
    "TypeParam",
]
