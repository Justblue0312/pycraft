# Pycraft

**And yet, A stupid Python code generation toolkit.**

Pycraft provides a fluent and intuitive builder API to programmatically construct and generate Python code. It's designed to make code generation tasks simple, readable, and maintainable.

## Installation

With pip:
```bash
pip install https://github.com/Justblue0312/pycraft.git
```

With uv:
```bash
uv add https://github.com/Justblue0312/pycraft.git
```

## Usage

Here's a simple example of how to generate a Python class with a method:

```python
from pycraft.core.builder import Builder
from pycraft.builder import class_, func
from pycraft.nodes import Return, Constant, Import, Alias
from pycraft.generator.base import CodeGenerator

# Create a builder instance
with Builder() as builder:
    # Add an import statement
    builder.add_node(Import(names=[Alias(name="os")]))

    # Define a class 'MyClass'
    with class_(builder, "MyClass"):
        # Define a method 'my_method'
        with func(builder, "my_method"):
            # Return a constant value
            builder.add_node(Return(value=Constant(value=42)))

# Generate the code
generator = CodeGenerator()
generated_code = generator.generate(builder, mode="console")

# The output will be:
# import os
#
# class MyClass:
#     def my_method():
#         return 42
```

## Features

- **Fluent Builder API**: A clean and expressive API for building code structures.
- **Comprehensive Python Support**: Generate a wide range of Python constructs, including:
  - Functions and Classes (sync and async)
  - Control Flow (if/elif/else, match/case)
  - Loops (for, while)
  - Exception Handling (try/except/finally)
  - Context Managers (with)
  - Imports, assignments, and more.
- **AST-based**: Builds an internal Abstract Syntax Tree representation.
- **Formatted Code Generation**: Produces clean and readable Python code.
- **Extensible**: Easy to extend with custom node types and builders.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
