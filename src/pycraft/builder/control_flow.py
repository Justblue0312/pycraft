"""Builder context managers for all statement types.

This module consolidates all builder context managers for efficiency.
Organized into logical groups: control flow, loops, exceptions, and context managers.
"""

import types
from typing import TYPE_CHECKING, Any, Self

if TYPE_CHECKING:
    from pycraft.core.builder import Builder
    from pycraft.nodes import BaseNode

from pycraft.core.base import BodyNode
from pycraft.nodes.control_flow import Elif, Else, If, Match, MatchCase
from pycraft.nodes.exceptions import ExceptHandler, Try
from pycraft.nodes.loops import While

# ============================================================================
# Control Flow Builders
# ============================================================================


class IfBuilder:
    """Context manager for building if statements."""

    def __init__(self, builder: Builder, test: BaseNode, **kwargs):
        self.builder = builder
        self.node = If(test=test, body=[], or_else=[])

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


class ElifBuilder:
    """Context manager for building elif statements."""

    def __init__(self, builder: Builder, test: BaseNode, **kwargs):
        self.builder = builder
        self.node = Elif(test=test, body=[])

    def __enter__(self):
        self.builder._push_node(self.node)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ):
        # Special handling for elif - add to previous if's or_else
        node = self.builder._stack.pop()

        # Ensure body has at least Pass
        from pycraft.nodes import Pass

        if isinstance(node, BodyNode) and not node.body:
            node.body.append(Pass())

        # Find the parent If/Elif node and add to its or_else
        if self.builder._stack:
            parent = self.builder._stack[-1]
            if isinstance(parent, (If, While, Try)):
                parent.or_else.append(node)
            else:
                # Fallback: add to current body
                self.builder._get_current_body().append(node)
        else:
            self.builder.root_nodes.append(node)

        return False


class ElseBuilder:
    """Context manager for building else statements."""

    def __init__(self, builder: Builder, **kwargs):
        self.builder = builder
        self.node: Else = Else(body=[])

    def __enter__(self):
        self.builder._push_node(self.node)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ):
        # Special handling for else - add to previous if/elif's or_else
        node = self.builder._stack.pop()

        # Ensure body has at least Pass
        from pycraft.nodes import Pass

        if isinstance(node, BodyNode) and not node.body:
            node.body.append(Pass())

        # Find the parent If/Elif node and extend its or_else with this else's body
        if self.builder._stack:
            parent = self.builder._stack[-1]
            if isinstance(parent, (If, While, Try)) and isinstance(node, BodyNode):
                # For else, we add its body directly to the or_else
                parent.or_else.extend(node.body)
            else:
                self.builder._get_current_body().append(node)
        else:
            self.builder.root_nodes.append(node)

        return False


class MatchBuilder:
    """Context manager for building match statements (Python 3.10+)."""

    def __init__(self, builder: Builder, subject: BaseNode, **kwargs):
        self.builder = builder
        self.node = Match(subject=subject, cases=[])

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


class CaseBuilder:
    """Context manager for building case statements (Python 3.10+)."""

    def __init__(
        self,
        builder: Builder,
        pattern: BaseNode,
        guard: BaseNode | None = None,
        **kwargs,
    ):
        self.builder = builder
        self.node = MatchCase(pattern=pattern, guard=guard, body=[])

    def __enter__(self):
        self.builder._push_node(self.node)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ):
        # Add the case to the parent Match node
        node = self.builder._stack.pop()

        # Ensure body has at least Pass
        from pycraft.nodes import Pass

        if isinstance(node, BodyNode) and not node.body:
            node.body.append(Pass())

        if self.builder._stack:
            parent = self.builder._stack[-1]
            if isinstance(parent, Match):
                parent.cases.append(node)

        return False


# ============================================================================
# Loop Builders
# ============================================================================


class ForBuilder:
    """Context manager for building for loops."""

    def __init__(
        self,
        builder: Builder,
        target: BaseNode,
        iter: BaseNode,
        is_async: bool = False,
        **kwargs,
    ):
        from pycraft.nodes import AsyncFor, For

        self.builder = builder
        NodeClass = AsyncFor if is_async else For
        self.node = NodeClass(target=target, iter=iter, body=[])

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


class WhileBuilder:
    """Context manager for building while loops."""

    def __init__(self, builder: Builder, test: BaseNode, **kwargs):
        self.builder = builder
        self.node = While(test=test, body=[], or_else=[])

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


# ============================================================================
# Exception Handling Builders
# ============================================================================


class TryBuilder:
    """Context manager for building try statements."""

    def __init__(self, builder: Builder, **kwargs):
        self.builder = builder
        self.node: Try = Try(body=[], handlers=[], or_else=[], finalbody=[])

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


class ExceptBuilder:
    """Context manager for building except handlers."""

    def __init__(
        self,
        builder: Builder,
        exc_type: BaseNode | None = None,
        name: str | None = None,
        **kwargs,
    ):
        self.builder = builder
        self.node = ExceptHandler(type=exc_type, name=name, body=[])

    def __enter__(self):
        self.builder._push_node(self.node)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ):
        # Add the handler to the parent Try node
        node = self.builder._stack.pop()

        # Ensure body has at least Pass
        from pycraft.nodes import Pass

        if isinstance(node, BodyNode) and not node.body:
            node.body.append(Pass())

        if self.builder._stack:
            parent = self.builder._stack[-1]
            if isinstance(parent, Try):
                parent.handlers.append(node)
            else:
                self.builder._get_current_body().append(node)

        return False


class FinallyBuilder:
    """Context manager for building finally blocks."""

    def __init__(self, builder: Builder, **kwargs):
        self.builder = builder
        self.temp_body: list[BaseNode] = []

    @property
    def body(self) -> list[BaseNode]:
        """Property to make FinallyBuilder compatible with builder's _get_current_body."""
        return self.temp_body

    def __enter__(self) -> Self:
        # Push ourselves to the stack so builder.add_node works
        self.builder._stack.append(self)  # type: ignore[arg-type]
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ):
        # Pop ourselves
        self.builder._stack.pop()

        # Add Pass if empty
        from pycraft.nodes import Pass

        if not self.temp_body:
            self.temp_body.append(Pass())

        # Find the parent Try node and add to finalbody
        if self.builder._stack:
            parent = self.builder._stack[-1]
            if isinstance(parent, Try):
                parent.finalbody.extend(self.temp_body)

        return False


# ============================================================================
# Context Manager Builders
# ============================================================================


class WithBuilder:
    """Context manager for building with statements."""

    def __init__(
        self,
        builder: Builder,
        context_expr: BaseNode,
        optional_vars: BaseNode | None = None,
        **kwargs: Any,
    ):
        from pycraft.nodes import With, WithItem

        self.builder = builder
        items: list = [WithItem(context_expr=context_expr, optional_vars=optional_vars)]
        self.node = With(items=items, body=[])

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


# ============================================================================
# Convenience Functions
# ============================================================================


def if_(builder: Builder, test: BaseNode, **kwargs: Any) -> IfBuilder:
    """Create an if statement builder."""
    return IfBuilder(builder, test, **kwargs)


def elif_(builder: Builder, test: BaseNode, **kwargs: Any) -> ElifBuilder:
    """Create an elif statement builder."""
    return ElifBuilder(builder, test, **kwargs)


def else_(builder: Builder, **kwargs: Any) -> ElseBuilder:
    """Create an else statement builder."""
    return ElseBuilder(builder, **kwargs)


def match_(builder: Builder, subject: BaseNode, **kwargs: Any) -> MatchBuilder:
    """Create a match statement builder (Python 3.10+)."""
    return MatchBuilder(builder, subject, **kwargs)


def case_(
    builder: Builder, pattern: BaseNode, guard: BaseNode | None = None, **kwargs: Any
) -> CaseBuilder:
    """Create a case statement builder (Python 3.10+)."""
    return CaseBuilder(builder, pattern, guard, **kwargs)


def for_(
    builder: Builder, target: BaseNode, iter: BaseNode, **kwargs: Any
) -> ForBuilder:
    """Create a for loop builder."""
    return ForBuilder(builder, target, iter, **kwargs)


def async_for(
    builder: Builder, target: BaseNode, iter: BaseNode, **kwargs: Any
) -> ForBuilder:
    """Create an async for loop builder."""
    return ForBuilder(builder, target, iter, is_async=True, **kwargs)


def while_(builder: Builder, test: BaseNode, **kwargs: Any) -> WhileBuilder:
    """Create a while loop builder."""
    return WhileBuilder(builder, test, **kwargs)


def try_(builder: Builder, **kwargs: Any) -> TryBuilder:
    """Create a try statement builder."""
    return TryBuilder(builder, **kwargs)


def except_(
    builder: Builder,
    exc_type: BaseNode | None = None,
    name: str | None = None,
    **kwargs: Any,
) -> ExceptBuilder:
    """Create an except handler builder."""
    return ExceptBuilder(builder, exc_type, name, **kwargs)


def finally_(builder: Builder, **kwargs: Any) -> FinallyBuilder:
    """Create a finally block builder."""
    return FinallyBuilder(builder, **kwargs)


def with_(
    builder: Builder,
    context_expr: BaseNode,
    optional_vars: BaseNode | None = None,
    **kwargs: Any,
) -> WithBuilder:
    """Create a with statement builder."""
    return WithBuilder(builder, context_expr, optional_vars, **kwargs)


__all__ = [
    # Control Flow
    "IfBuilder",
    "ElifBuilder",
    "ElseBuilder",
    "MatchBuilder",
    "CaseBuilder",
    "if_",
    "elif_",
    "else_",
    "match_",
    "case_",
    # Loops
    "ForBuilder",
    "WhileBuilder",
    "for_",
    "async_for",
    "while_",
    # Exceptions
    "TryBuilder",
    "ExceptBuilder",
    "FinallyBuilder",
    "try_",
    "except_",
    "finally_",
    # Context Managers
    "WithBuilder",
    "with_",
]
