# Pycraft

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Features](#features)
- [API Reference](#api-reference)
  - [Core Components](#core-components)
  - [Builder Context Managers](#builder-context-managers)
  - [Nodes](#nodes)
- [Code Examples](#code-examples)
- [License](#license)

## Introduction
Pycraft is a fluent and intuitive builder API for programmatically constructing and generating Python code. It abstracts the AST layer, allowing developers to create clean, readable Python source programmatically.

## Installation

### With pip
```bash
pip install https://github.com/Justblue0312/pycraft.git
```

### With uv
```bash
uv add https://github.com/Justblue0312/pycraft.git
```

## Quick Start
```python
from pycraft.core.builder import Builder
from pycraft.builder import class_, func
from pycraft.nodes import Return, Constant, Import, Alias
from pycraft.generator.base import CodeGenerator

with Builder() as builder:
    builder.add_node(Import(names=[Alias(name="os")]))
    with class_(builder, "MyClass"):
        with func(builder, "my_method"):
            builder.add_node(Return(value=Constant(value=42)))

generator = CodeGenerator()
print(generator.generate(builder, mode="console"))
```

## Features
- **Fluent Builder API** – expressive construction of Python code structures.
- **Comprehensive Python Support** – functions, classes, control flow, loops, exception handling, context managers, imports, and more.
- **AST‑based** – builds an internal abstract syntax tree.
- **Formatted Code Generation** – produces clean, readable Python code.
- **Extensible** – easy to extend with custom node types and builders.

## API Reference
### Core Components
#### `Builder`
The main entry point for constructing the AST.
```python
from pycraft.core.builder import Builder
with Builder() as builder:
    # build your code here
```
**Methods**
- `add_node(node: BaseNode)` – add a node to the current scope.
- `add_import(*modules: str)` – add `import module` statements.
- `import_from(module: str, names: list[str], level: int = 0)` – add `from module import names`.
- `add_comment(text: str)` – add a comment.

#### `CodeGenerator`
Converts the AST into Python source code.
```python
from pycraft.generator.base import CodeGenerator
generator = CodeGenerator(indent_char="    ")
code = generator.generate(builder, mode="console")
```
### Builder Context Managers
#### Functions & Classes
- `func(builder, name: str)` – define a function.
- `async_func(builder, name: str)` – define an async function.
- `class_(builder, name: str, bases: list = None)` – define a class.

#### Control Flow
- `if_(builder, condition: BaseNode)` – start an if block.
- `elif_(builder, condition: BaseNode)` – add an elif block.
- `else_(builder)` – add an else block.
- `match_(builder, subject: BaseNode)` – start a match statement.
- `case_(builder, pattern: BaseNode)` – add a case block.

#### Loops
- `for_(builder, target: BaseNode, iter: BaseNode)` – create a for loop.
- `async_for(builder, target: BaseNode, iter: BaseNode)` – create an async for loop.
- `while_(builder, test: BaseNode)` – create a while loop.

#### Exceptions
- `try_(builder)` – start a try block.
- `except_(builder, type: BaseNode = None, name: str = None)` – add an except block.
- `finally_(builder)` – add a finally block.

#### Context Managers
- `with_(builder, items: list[WithItem])` – create a with statement.

## Nodes
The `pycraft.nodes` package defines the AST node classes. Commonly used nodes include:
- **Literals**: `Constant`, `List`, `Dict`, `Set`, `Tuple`
- **Variables**: `Name`
- **Expressions**: `Call`, `Attribute`, `BinOp`, `BoolOp`, `Compare`
- **Statements**: `Return`, `Assign`, `AnnAssign`, `Raise`, `Assert`
- **Imports**: `Import`, `ImportFrom`, `Alias`

### Example Using Nodes Directly
```python
from pycraft.nodes import Return, Constant, Name, Call
# return 42
builder.add_node(Return(value=Constant(value=42)))
# print("Hello")
builder.add_node(Expr(value=Call(func=Name(id="print"), args=[Constant(value="Hello")])))
```

## Code Examples
### Defining a Class with a Method
```python
with class_(builder, "MyClass"):
    with func(builder, "my_method"):
        builder.add_node(Pass())
```
### If‑Else Block
```python
with if_(builder, Name(id="condition")):
    builder.add_node(Pass())
with else_(builder):
    builder.add_node(Pass())
```
### For Loop
```python
with for_(builder, Name(id="i"), Call(func=Name(id="range"), args=[Constant(value=10)])):
    builder.add_node(Pass())
```
### Try‑Except Block
```python
with try_(builder):
    builder.add_node(Raise(exc=Name(id="ValueError")))
with except_(builder, Name(id="ValueError"), "e"):
    builder.add_node(Pass())
```
### With Statement
```python
from pycraft.nodes import WithItem
with with_(builder, [WithItem(context_expr=Call(func=Name(id="open"), args=[Constant(value="file.txt")]))]):
    builder.add_node(Pass())
```

## License
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
