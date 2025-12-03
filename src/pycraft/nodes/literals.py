"""Literal and name nodes.

This module contains nodes representing literals and identifiers:
- Constant: Literal values (numbers, strings, booleans, None)
- Name: Variable/function/class names
- Attribute: Attribute access (obj.attr)
- Subscript: Subscript access (obj[key])
- Dict: Dictionary literals
- List: List literals
- Set: Set literals
- Tuple: Tuple literals
"""

from dataclasses import dataclass, field

from pycraft.core.base import BaseNode


@dataclass
class Constant(BaseNode):
    """Represents a constant value (string, number, boolean, etc.).

    This corresponds to literal values in Python code such as numbers,
    strings, booleans, None, etc.

    Example:
        42
        "hello world"
        True
        None

    Attributes:
        value: The actual value of the constant
        kind: Optional kind specifier (e.g., 'f' for f-strings)
    """

    value: int | str | float | bool | None = None
    kind: str | None = None


@dataclass
class Name(BaseNode):
    """Represents a variable or attribute name.

    This corresponds to any identifier used in Python code to refer
    to variables, functions, classes, or other named entities.

    Example:
        variable_name
        function_name
        ClassName

    Attributes:
        id: The identifier string
    """

    id: str = ""


@dataclass
class Attribute[T: BaseNode](BaseNode):
    """Represents an attribute access (using dot notation).

    This corresponds to accessing attributes, methods, or properties
    of an object using the dot operator.

    Example:
        obj.attribute
        module.function
        instance.method()

    Attributes:
        value: The object being accessed
        attr: The attribute name
    """

    value: T | None = None
    attr: str = ""


@dataclass
class Subscript[T: BaseNode](BaseNode):
    """Represents a subscript expression (indexing or slicing).

    This corresponds to accessing elements of sequences (lists, tuples, strings)
    or mappings (dictionaries) using square brackets.

    Example:
        list[0]
        dict['key']
        sequence[1:5]

    Attributes:
        value: The object being subscripted
        slice: The index or slice
    """

    value: T | None = None
    slice: T | None = None


@dataclass
class Dict[T: BaseNode](BaseNode):
    """Represents a dictionary literal.

    Example:
        {"key": "value"}
        {x: y for x, y in items}

    Attributes:
        keys: List of key nodes
        values: List of value nodes
    """

    keys: list[T] = field(default_factory=list)
    values: list[T] = field(default_factory=list)


@dataclass
class List[T: BaseNode](BaseNode):
    """Represents a list literal.

    Example:
        [1, 2, 3]
        [x for x in range(10)]

    Attributes:
        elts: List of element nodes
    """

    elts: list[T] = field(default_factory=list)


@dataclass
class Set[T: BaseNode](BaseNode):
    """Represents a set literal.

    Example:
        {1, 2, 3}
        {x for x in range(10)}

    Attributes:
        elts: List of element nodes
    """

    elts: list[T] = field(default_factory=list)


@dataclass
class Tuple[T: BaseNode](BaseNode):
    """Represents a tuple literal.

    Example:
        (1, 2, 3)
        x, y = 1, 2

    Attributes:
        elts: List of element nodes
    """

    elts: list[T] = field(default_factory=list)


__all__ = [
    "Constant",
    "Name",
    "Attribute",
    "Subscript",
    "Dict",
    "List",
    "Set",
    "Tuple",
]
