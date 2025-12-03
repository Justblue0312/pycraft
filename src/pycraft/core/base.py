from dataclasses import dataclass
from typing import ClassVar, Protocol, runtime_checkable


@runtime_checkable
class NodeProtocol(Protocol):
    """Protocol defining the interface for all AST nodes.

    This ensures type safety and provides a contract that all nodes must follow.
    """

    def __repr__(self) -> str:
        """Return string representation of the node."""
        ...


@dataclass
class BaseNode:
    """Base class for all AST nodes in the builder system.

    This serves as the foundation for all node types in the AST representation,
    providing a common interface and structure for code generation and parsing.

    All node types should inherit from this class and define their specific
    attributes using dataclass fields.

    The __kw__ class variable can be set to associate a Python keyword with
    the node type (e.g., 'class', 'def', 'if', etc.).
    """

    __kw__: ClassVar[str | None] = None

    def __repr__(self) -> str:
        """Generate a readable representation of the node."""
        fields = []
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                fields.append(f"{key}={value!r}")
        return f"{self.__class__.__name__}({', '.join(fields)})"


# Marker for nodes that have a body (can contain other nodes)
@runtime_checkable
class BodyNode(Protocol):
    """Protocol for nodes that can contain a body of other nodes.

    This includes classes, functions, loops, conditionals, etc.
    """

    body: list[BaseNode]


# Marker for nodes that are expressions (can be used in expressions)
@runtime_checkable
class ExprNode(Protocol):
    """Protocol for nodes that represent expressions.

    Expressions can be used as values in assignments, function calls, etc.
    """

    pass


__all__ = [
    "BaseNode",
    "NodeProtocol",
    "BodyNode",
    "ExprNode",
]
