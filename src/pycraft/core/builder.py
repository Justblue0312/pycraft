"""Core Builder class for constructing AST nodes.

This module contains the main Builder class that manages the context stack
and provides the primary interface for building Python code AST.
"""

import types
from typing import TYPE_CHECKING, Literal, Self

if TYPE_CHECKING:
    from pycraft.nodes import BaseNode

from .base import BodyNode


class Builder:
    """Main builder that tracks the context stack of nodes.

    The Builder maintains a stack of parent nodes to handle nested structures
    like classes containing methods, if statements with elif/else clauses, etc.

    Usage:
        with Builder() as builder:
            builder.add_node(Import(names=[Alias(name="os")]))
            with class_(builder, "MyClass"):
                with func(builder, "method"):
                    builder.add_node(Return(value=Constant(value=42)))
    """

    def __init__(self) -> None:
        """Initialize the builder with empty root nodes and stack."""
        self.root_nodes: list[BaseNode] = []
        self._stack: list[BaseNode] = []  # Stack of parent nodes

    def __enter__(self) -> Self:
        """Enter builder context."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> Literal[False]:
        """Exit builder context and ensure valid Python code."""
        # Add Pass nodes to any empty bodies at the end
        self._ensure_pass_in_empty_bodies()
        return False

    def _get_current_body(self) -> list[BaseNode]:
        """Get the body list to append to (either root or current parent's body).

        Returns:
            The body list of the current context (parent node or root)
        """
        if self._stack:
            parent = self._stack[-1]
            # Get the appropriate body attribute
            if isinstance(parent, BodyNode):
                return parent.body
        return self.root_nodes

    def _push_node(self, node: BaseNode) -> None:
        """Push a node with body to the stack.

        Args:
            node: The node to push onto the stack
        """
        self._stack.append(node)

    def _pop_node(self) -> BaseNode:
        """Pop a node from the stack and add to parent.

        Returns:
            The popped node
        """
        from pycraft.nodes import Pass

        node = self._stack.pop()

        # Add Pass to empty bodies (for valid Python code)
        if isinstance(node, BodyNode) and isinstance(node.body, list):
            if not node.body:
                node.body.append(Pass())

        # Add to parent's body
        self._get_current_body().append(node)
        return node

    def _ensure_pass_in_empty_bodies(self) -> None:
        """Ensure all empty bodies have Pass statements."""
        from pycraft.nodes import Pass

        for node in self.root_nodes:
            if (
                isinstance(node, BodyNode)
                and isinstance(node.body, list)
                and not node.body
            ):
                node.body.append(Pass())

    def add_node(self, node: BaseNode) -> None:
        """Add a node directly to the current body.

        Args:
            node: The node to add
        """
        self._get_current_body().append(node)

    # Convenience helpers
    def import_from(self, module: str, names: list[str], level: int = 0) -> None:
        """Add an 'from katze.. import katze..' statement.

        Args:
            module: Module name to import from
            names: List of names to import
            level: Relative import level (0 for absolute)
        """
        from pycraft.nodes import Alias, ImportFrom

        aliases: list[Alias] = [Alias(name=name) for name in names]
        self.add_node(ImportFrom(module=module, names=aliases, level=level))

    def add_import(self, *modules: str) -> None:
        """Add an import statement.

        Args:
            *modules: Module names to import
        """
        from pycraft.nodes import Alias, Import

        aliases: list = [Alias(name=mod) for mod in modules]
        self.add_node(Import(names=aliases))

    def add_comment(self, text: str) -> None:
        """Add a comment.

        Args:
            text: Comment text (without # prefix)
        """
        from pycraft.nodes import Comment

        self.add_node(Comment(text=text))


__all__ = ["Builder"]
