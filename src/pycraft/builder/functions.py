"""Builder context managers for functions and classes.

This module provides context managers for building function and class definitions.
"""

import types
from typing import TYPE_CHECKING, Any, Self

if TYPE_CHECKING:
    from pycraft.core.builder import Builder
    from pycraft.nodes import Arguments


class ClassDefBuilder:
    """Context manager for building class definitions."""

    def __init__(
        self, builder: Builder, name: str, bases: list | None = None, **kwargs: Any
    ) -> None:
        from pycraft.nodes import ClassDef

        self.builder = builder
        self.node = ClassDef(
            name=name, bases=bases or [], body=[], keywords=[], decorators=[]
        )

    def __enter__(self) -> Self:
        self.builder._push_node(self.node)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ):
        self.builder._pop_node()
        return False


class FunctionDefBuilder:
    """Context manager for building function definitions."""

    def __init__(
        self,
        builder: Builder,
        name: str,
        args: Arguments | None = None,
        returns: str | None = None,
        decorators_list: list[Any] | None = None,
        is_async: bool = False,
        **kwargs,
    ):
        from pycraft.nodes import Arguments, AsyncFunctionDef, FunctionDef, Name

        self.builder = builder
        self.is_async = is_async

        # Create Arguments if not provided
        if args is None:
            args = Arguments()

        # Handle returns as string or node
        returns_node = None
        if returns:
            if isinstance(returns, str):
                returns_node = Name(id=returns)
            else:
                returns_node = returns

        if decorators_list is None:
            decorators_list = []
        elif not isinstance(decorators_list, list):
            raise ValueError("decorators_list must be a list")

        # Extract type_params from kwargs if it exists
        type_params = kwargs.get("type_params", [])

        NodeClass = AsyncFunctionDef if is_async else FunctionDef
        self.node = NodeClass(
            name=name,
            args=args,
            body=[],
            returns=returns_node,
            decorator_list=decorators_list,
            type_params=type_params,
        )

    def __enter__(self):
        self.builder._push_node(self.node)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ):
        self.builder._pop_node()
        return False


# Convenience functions
def class_(
    builder: Builder, name: str, bases: list | None = None, **kwargs
) -> ClassDefBuilder:
    """Create a class definition builder."""
    return ClassDefBuilder(builder, name, bases, **kwargs)


def func(
    builder: Builder,
    name: str,
    args: Arguments | None = None,
    returns: str | None = None,
    decorators_list: list | None = None,
    **kwargs,
) -> FunctionDefBuilder:
    """Create a function definition builder."""
    return FunctionDefBuilder(builder, name, args, returns, decorators_list, **kwargs)


def async_func(
    builder: Builder,
    name: str,
    args: Arguments | None = None,
    returns: str | None = None,
    **kwargs,
) -> FunctionDefBuilder:
    """Create an async function definition builder."""
    return FunctionDefBuilder(builder, name, args, returns, is_async=True, **kwargs)


__all__ = [
    "ClassDefBuilder",
    "FunctionDefBuilder",
    "class_",
    "func",
    "async_func",
]
