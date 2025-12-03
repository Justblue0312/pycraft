"""Node types for pycraft.

This package contains all AST node types organized by category.
"""

# Import base node first
from pycraft.core.base import BaseNode

# Import all node types from submodules
from .assignments import AnnAssign, Assign, AugAssign
from .comprehensions import (
    Comprehension,
    DictComp,
    GeneratorExp,
    ListComp,
    SetComp,
)
from .context_managers import With, WithItem
from .control_flow import Elif, Else, If, Match, MatchCase
from .exceptions import Assert, ExceptHandler, Finally, Raise, Try
from .expressions import (
    BinOp,
    BoolOp,
    Call,
    Compare,
    IfExp,
    Keyword,
    Lambda,
    Starred,
    UnaryOp,
)
from .functions import (
    Arg,
    Arguments,
    AsyncFunctionDef,
    ClassDef,
    FunctionDef,
    TypeParam,
)
from .imports import Alias, Import, ImportFrom, ImportGroup
from .literals import Attribute, Constant, Dict, List, Name, Set, Subscript, Tuple
from .loops import AsyncFor, For, While
from .module import Module
from .operators import (
    Add,
    And,
    BitAnd,
    BitOr,
    BitXor,
    Div,
    Eq,
    FloorDiv,
    Gt,
    GtE,
    In,
    Invert,
    Is,
    IsNot,
    LShift,
    Lt,
    LtE,
    MatMult,
    Mod,
    Mult,
    Not,
    NotEq,
    NotIn,
    Or,
    Pow,
    RShift,
    Sub,
    UAdd,
    USub,
)
from .statements import (
    Await,
    Break,
    Comment,
    Continue,
    Delete,
    Expr,
    Global,
    Nonlocal,
    Pass,
    Return,
    Yield,
)

__all__ = [
    # Base
    "BaseNode",
    # Imports
    "Import",
    "ImportFrom",
    "Alias",
    "ImportGroup",
    # Literals
    "Constant",
    "Name",
    "Attribute",
    "Subscript",
    "Dict",
    "List",
    "Set",
    "Tuple",
    # Statements
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
    # Assignments
    "Assign",
    "AugAssign",
    "AnnAssign",
    # Expressions
    "Call",
    "Keyword",
    "BoolOp",
    "UnaryOp",
    "BinOp",
    "Compare",
    "Lambda",
    "IfExp",
    "Starred",
    # Functions
    "Arg",
    "Arguments",
    "FunctionDef",
    "AsyncFunctionDef",
    "ClassDef",
    "TypeParam",
    # Control Flow
    "If",
    "Elif",
    "Else",
    "Match",
    "MatchCase",
    # Loops
    "For",
    "AsyncFor",
    "While",
    # Exceptions
    "Try",
    "ExceptHandler",
    "Finally",
    "Raise",
    "Assert",
    # Context Managers
    "With",
    "WithItem",
    # Comprehensions
    "Comprehension",
    "ListComp",
    "SetComp",
    "DictComp",
    "GeneratorExp",
    # Operators - Boolean
    "And",
    "Or",
    "Not",
    # Operators - Comparison
    "Eq",
    "NotEq",
    "Lt",
    "LtE",
    "Gt",
    "GtE",
    "Is",
    "IsNot",
    "In",
    "NotIn",
    # Operators - Binary
    "Add",
    "Sub",
    "Mult",
    "Div",
    "FloorDiv",
    "Mod",
    "Pow",
    "MatMult",
    "LShift",
    "RShift",
    "BitOr",
    "BitXor",
    "BitAnd",
    # Operators - Unary
    "UAdd",
    "USub",
    "Invert",
    # Module
    "Module",
]
