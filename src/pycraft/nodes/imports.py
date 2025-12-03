"""Import-related AST nodes.

This module contains nodes for Python import statements:
- Import: import module
- ImportFrom: from module import names
- Alias: module as alias
"""

from dataclasses import dataclass, field

from pycraft.core.base import BaseNode


@dataclass
class Import[T: BaseNode](BaseNode):
    """Represents a Python import statement.

    This corresponds to the 'import' keyword in Python, used to import modules
    and make their contents available in the current namespace.

    Example:
        import os
        import sys, json

    Attributes:
        names: List of Alias nodes representing modules to import
    """

    __kw__ = "import"
    names: list[T] = field(default_factory=list)


@dataclass
class ImportFrom[T: BaseNode](BaseNode):
    """Represents a Python 'from katze.. import katze..' statement.

    This corresponds to the 'from' keyword in Python, used to import specific
    items from a module directly into the current namespace.

    Example:
        from os import path
        from typing import List, Dict

    Attributes:
        module: Name of the module to import from
        names: List of Alias nodes representing items to import
        level: Relative import level (0 for absolute, 1+ for relative)
    """

    __kw__ = "from"

    module: str = ""
    names: list[T] = field(default_factory=list)
    level: int | None = None


@dataclass
class Alias(BaseNode):
    """Represents an alias in import statements (using 'as' keyword).

    This corresponds to the 'as' keyword used in import statements to
    give imported modules or items a different name in the local namespace.

    Example:
        import numpy as np
        from typing import List as ListType

    Attributes:
        name: Original name of the imported item
        asname: Alias name (None if no alias)
    """

    name: str = ""
    asname: str | None = None


@dataclass
class ImportGroup[T: BaseNode](BaseNode):
    """Represents a group of import statements.

    This serves as a container for organizing multiple import statements
    in the code generation process, often used for grouping related imports.

    Example:
        import os
        import sys

        from typing import List, Dict
        from pathlib import Path

    Attributes:
        imports: List of import nodes in this group
    """

    imports: list[T] = field(default_factory=list)


__all__ = [
    "Import",
    "ImportFrom",
    "Alias",
    "ImportGroup",
]
