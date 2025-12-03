"""Code generator for producing formatted Python code from AST nodes"""

from pathlib import Path
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from pycraft.core.builder import Builder
    from pycraft.nodes import Arguments, BaseNode, Comprehension, WithItem


class CodeGenerator:
    """Generates formatted Python code from AST nodes"""

    def __init__(self, indent_char: str = "\t"):
        """
        Initialize code generator

        Args:
            indent_char: Character(s) to use for indentation (default: tab)
        """
        self.indent_char = indent_char
        self.indent_level = 0

    def generate(
        self,
        builder: Builder,
        mode: Literal["console", "file"] = "console",
        file_name: str | None = None,
        path: str = ".",
    ) -> str:
        """
        Generate Python code from builder's AST

        Args:
            builder: Builder instance with root nodes
            mode: Output mode - 'console' to print, 'file' to save
            file_name: Name of file to save (required if mode='file')
            path: Directory path for file (default: current directory)

        Returns:
            Generated Python code as string
        """
        code = self._generate_nodes(builder.root_nodes)

        if mode == "console":
            print(code)
        elif mode == "file":
            if not file_name:
                raise ValueError("file_name is required when mode='file'")
            output_path = Path(path) / file_name
            output_path.write_text(code)

        return code

    def _generate_nodes(self, nodes: list[BaseNode]) -> str:
        """Generate code from a list of nodes"""
        from pycraft.nodes import BaseNode

        lines = []
        for node in nodes:
            if isinstance(node, BaseNode):
                code = self._generate_node(node)
                if code:
                    lines.append(code)
        return "\n".join(lines)

    def _generate_node(self, node: BaseNode) -> str:
        """Generate code for a single node"""
        from pycraft.nodes import (
            AnnAssign,
            Assert,
            Assign,
            AsyncFor,
            AsyncFunctionDef,
            AugAssign,
            Await,
            Break,
            ClassDef,
            Comment,
            Continue,
            Delete,
            Elif,
            Else,
            Expr,
            For,
            FunctionDef,
            Global,
            If,
            Import,
            ImportFrom,
            ImportGroup,
            Match,
            MatchCase,
            Nonlocal,
            Pass,
            Raise,
            Return,
            Try,
            While,
            With,
            Yield,
        )

        indent = self.indent_char * self.indent_level

        # Import statements
        if isinstance(node, Import):
            names = ", ".join(self._generate_expr(alias) for alias in node.names)
            return f"{indent}import {names}"

        elif isinstance(node, ImportFrom):
            module = node.module or ""
            level = "." * (node.level or 0)
            names = ", ".join(self._generate_expr(alias) for alias in node.names)
            return f"{indent}from {level}{module} import {names}"

        elif isinstance(node, ImportGroup):
            return self._generate_nodes(node.imports)

        # Class definition
        elif isinstance(node, ClassDef):
            lines = []

            # Render decorators
            for decorator in node.decorators:
                decorator_str = self._generate_expr(decorator)
                lines.append(f"{indent}@{decorator_str}")

            bases_str = ""
            if node.bases:
                bases_str = f"({', '.join(self._generate_expr(b) for b in node.bases)})"

            lines.append(f"{indent}class {node.name}{bases_str}:")
            self.indent_level += 1
            body_code = self._generate_nodes(node.body)
            lines.append(body_code)
            self.indent_level -= 1
            return "\n".join(lines)

        # Function definition
        elif isinstance(node, (FunctionDef, AsyncFunctionDef)):
            lines = []

            # Render decorators
            for decorator in node.decorator_list:
                decorator_str = self._generate_expr(decorator)
                lines.append(f"{indent}@{decorator_str}")

            prefix = "async def" if isinstance(node, AsyncFunctionDef) else "def"
            args_str = self._generate_arguments(node.args) if node.args else ""
            returns_str = ""
            if node.returns:
                returns_str = f" -> {self._safe_generate_expr(node.returns)}"

            # Handle type parameters for generic functions (Python 3.12+)
            type_params_str = ""
            if node.type_params:
                type_params_parts = []
                for param in node.type_params:
                    param_str = self._generate_expr(param)
                    type_params_parts.append(param_str)
                if type_params_parts:
                    type_params_str = f"[{', '.join(type_params_parts)}]"

            lines.append(
                f"{indent}{prefix} {node.name}{type_params_str}({args_str}){returns_str}:"
            )
            self.indent_level += 1
            body_code = self._generate_nodes(node.body)
            lines.append(body_code)
            self.indent_level -= 1
            return "\n".join(lines)

        # Control flow
        elif isinstance(node, If):
            test_str = self._safe_generate_expr(node.test)
            lines = [f"{indent}if {test_str}:"]
            self.indent_level += 1
            body_code = self._generate_nodes(node.body)
            lines.append(body_code)
            self.indent_level -= 1

            # Handle elif and else
            for or_else_node in node.or_else:
                elif_code = self._generate_node(or_else_node)
                lines.append(elif_code)

            return "\n".join(lines)

        elif isinstance(node, Elif):
            test_str = self._safe_generate_expr(node.test)
            lines = [f"{indent}elif {test_str}:"]
            self.indent_level += 1
            body_code = self._generate_nodes(node.body)
            lines.append(body_code)
            self.indent_level -= 1
            return "\n".join(lines)

        elif isinstance(node, Else):
            lines = [f"{indent}else:"]
            self.indent_level += 1
            body_code = self._generate_nodes(node.body)
            lines.append(body_code)
            self.indent_level -= 1
            return "\n".join(lines)

        elif isinstance(node, For):
            target_str = self._safe_generate_expr(node.target)
            iter_str = self._safe_generate_expr(node.iter)
            lines = [f"{indent}for {target_str} in {iter_str}:"]
            self.indent_level += 1
            body_code = self._generate_nodes(node.body)
            lines.append(body_code)
            self.indent_level -= 1

            if node.or_else:
                lines.append(f"{indent}else:")
                self.indent_level += 1
                else_code = self._generate_nodes(node.or_else)
                lines.append(else_code)
                self.indent_level -= 1

            return "\n".join(lines)

        elif isinstance(node, AsyncFor):
            target_str = self._safe_generate_expr(node.target)
            iter_str = self._safe_generate_expr(node.iter)
            lines = [f"{indent}async for {target_str} in {iter_str}:"]
            self.indent_level += 1
            body_code = self._generate_nodes(node.body)
            lines.append(body_code)
            self.indent_level -= 1

            if node.or_else:
                lines.append(f"{indent}else:")
                self.indent_level += 1
                else_code = self._generate_nodes(node.or_else)
                lines.append(else_code)
                self.indent_level -= 1

            return "\n".join(lines)

        elif isinstance(node, While):
            test_str = self._safe_generate_expr(node.test)
            lines = [f"{indent}while {test_str}:"]
            self.indent_level += 1
            body_code = self._generate_nodes(node.body)
            lines.append(body_code)
            self.indent_level -= 1

            if node.or_else:
                lines.append(f"{indent}else:")
                self.indent_level += 1
                else_code = self._generate_nodes(node.or_else)
                lines.append(else_code)
                self.indent_level -= 1

            return "\n".join(lines)

        elif isinstance(node, With):
            # Generate with items
            items_str = ", ".join(
                self._safe_generate_with_item(item) for item in node.items
            )
            lines = [f"{indent}with {items_str}:"]
            self.indent_level += 1
            body_code = self._generate_nodes(node.body)
            lines.append(body_code)
            self.indent_level -= 1
            return "\n".join(lines)

        elif isinstance(node, Try):
            lines = [f"{indent}try:"]
            self.indent_level += 1
            body_code = self._generate_nodes(node.body)
            lines.append(body_code)
            self.indent_level -= 1

            # Handle except clauses
            for handler in node.handlers:
                handler_code = self._generate_node(handler)
                lines.append(handler_code)

            # Handle else clause
            if node.or_else:
                lines.append(f"{indent}else:")
                self.indent_level += 1
                else_code = self._generate_nodes(node.or_else)
                lines.append(else_code)
                self.indent_level -= 1

            # Handle finally clause
            if node.finalbody:
                lines.append(f"{indent}finally:")
                self.indent_level += 1
                finally_code = self._generate_nodes(node.finalbody)
                lines.append(finally_code)
                self.indent_level -= 1

            return "\n".join(lines)

        elif isinstance(node, Match):
            subject_str = self._safe_generate_expr(node.subject)
            lines = [f"{indent}match {subject_str}:"]
            self.indent_level += 1
            for case in node.cases:
                case_code = self._generate_node(case)
                lines.append(case_code)
            self.indent_level -= 1
            return "\n".join(lines)

        elif isinstance(node, MatchCase):
            pattern_str = self._safe_generate_expr(node.pattern)
            guard_str = ""
            if node.guard:
                guard_str = f" if {self._safe_generate_expr(node.guard)}"
            lines = [f"{indent}case {pattern_str}{guard_str}:"]
            self.indent_level += 1
            body_code = self._generate_nodes(node.body)
            lines.append(body_code)
            self.indent_level -= 1
            return "\n".join(lines)

        # Statements
        elif isinstance(node, Expr):
            value_str = self._safe_generate_expr(node.value)
            return f"{indent}{value_str}"

        elif isinstance(node, Assign):
            targets_str = " = ".join(self._generate_expr(t) for t in node.targets)
            value_str = self._safe_generate_expr(node.value)
            return f"{indent}{targets_str} = {value_str}"

        elif isinstance(node, AugAssign):
            target_str = self._safe_generate_expr(node.target)
            op_str = self._generate_comparison_op(node.op) if node.op else ""
            value_str = self._safe_generate_expr(node.value)
            return f"{indent}{target_str} {op_str}= {value_str}"

        elif isinstance(node, AnnAssign):
            target_str = str(node.target)  # Handle string target
            annotation_str = self._safe_generate_expr(node.annotation)
            value_str = ""
            if node.value:
                value_str = f" = {self._safe_generate_expr(node.value)}"
            return f"{indent}{target_str}: {annotation_str}{value_str}"

        elif isinstance(node, Return):
            if node.value:
                value_str = self._safe_generate_expr(node.value)
                return f"{indent}return {value_str}"
            return f"{indent}return"

        elif isinstance(node, Yield):
            if node.value:
                value_str = self._safe_generate_expr(node.value)
                return f"{indent}yield {value_str}"
            return f"{indent}yield"

        elif isinstance(node, Await):
            value_str = self._safe_generate_expr(node.value)
            return f"{indent}await {value_str}"

        elif isinstance(node, Delete):
            targets_str = ", ".join(self._generate_expr(t) for t in node.targets)
            return f"{indent}del {targets_str}"

        elif isinstance(node, Global):
            names_str = ", ".join(node.names)
            return f"{indent}global {names_str}"

        elif isinstance(node, Nonlocal):
            names_str = ", ".join(node.names)
            return f"{indent}nonlocal {names_str}"

        elif isinstance(node, Assert):
            test_str = self._safe_generate_expr(node.test)
            if node.msg:
                msg_str = self._safe_generate_expr(node.msg)
                return f"{indent}assert {test_str}, {msg_str}"
            return f"{indent}assert {test_str}"

        elif isinstance(node, Raise):
            if node.exc:
                exc_str = self._safe_generate_expr(node.exc)
                if node.cause:
                    cause_str = self._safe_generate_expr(node.cause)
                    return f"{indent}raise {exc_str} from {cause_str}"
                return f"{indent}raise {exc_str}"
            return f"{indent}raise"

        elif isinstance(node, Pass):
            return f"{indent}pass"

        elif isinstance(node, Break):
            return f"{indent}break"

        elif isinstance(node, Continue):
            return f"{indent}continue"

        elif isinstance(node, Comment):
            if node.text:
                return f"{indent}# {node.text}"
            return ""

        else:
            # ExceptHandler is handled within Try
            from pycraft.nodes import ExceptHandler

            if isinstance(node, ExceptHandler):
                type_str = ""
                if node.type:
                    type_str = f"{self._safe_generate_expr(node.type)}"
                    if node.name:
                        type_str += f" as {node.name}"
                elif node.name:
                    type_str = f" {node.name}"

                except_line = f"{indent}except"
                if type_str:
                    except_line += f" {type_str}"
                except_line += ":"

                lines = [except_line]
                self.indent_level += 1
                body_code = self._generate_nodes(node.body)
                lines.append(body_code)
                self.indent_level -= 1
                return "\n".join(lines)

            return f"{indent}# Unknown node: {type(node).__name__}"

    def _safe_generate_expr(self, expr: BaseNode | None) -> str:
        """Generate expression string from node, handling None."""
        if expr is None:
            return ""
        return self._generate_expr(expr)

    def _generate_expr(self, expr: BaseNode) -> str:
        """Generate expression string from node"""
        from pycraft.nodes import (
            Alias,
            And,
            Arg,
            Attribute,
            Await,
            Call,
            Compare,
            Constant,
            DictComp,
            GeneratorExp,
            In,
            Is,
            IsNot,
            Keyword,
            Lambda,
            ListComp,
            Name,
            Not,
            NotIn,
            Or,
            SetComp,
            Starred,
            Subscript,
            UnaryOp,
        )

        if isinstance(expr, Name):
            return expr.id

        elif isinstance(expr, Constant):
            if isinstance(expr.value, str):
                prefix = expr.kind if expr.kind else ""
                return f"{prefix}{repr(expr.value)}"
            elif isinstance(expr.value, bool):
                return str(expr.value)
            elif expr.value is None:
                return "None"
            return str(expr.value)

        elif isinstance(expr, Alias):
            if expr.asname:
                return f"{expr.name} as {expr.asname}"
            return expr.name

        elif isinstance(expr, Call):
            func_str = self._safe_generate_expr(expr.func)
            args_list = [self._generate_expr(arg) for arg in expr.args]

            for kw in expr.keywords:
                if isinstance(kw, Keyword):
                    kw_str = f"{kw.arg}={self._safe_generate_expr(kw.value)}"
                    args_list.append(kw_str)
                elif isinstance(kw, dict):
                    kw_str = f"{kw['arg']}={self._generate_expr(kw['value'])}"
                    args_list.append(kw_str)

            return f"{func_str}({', '.join(args_list)})"

        elif isinstance(expr, Attribute):
            value_str = self._safe_generate_expr(expr.value)
            return f"{value_str}.{expr.attr}"

        elif isinstance(expr, Subscript):
            value_str = self._safe_generate_expr(expr.value)
            slice_str = self._safe_generate_expr(expr.slice)
            return f"{value_str}[{slice_str}]"

        elif isinstance(expr, Compare):
            left_str = self._safe_generate_expr(expr.left)
            parts = [left_str]
            for op, comparator in zip(expr.ops, expr.comparators, strict=False):
                op_str = self._generate_comparison_op(op)
                comp_str = self._generate_expr(comparator)
                parts.append(f"{op_str} {comp_str}")
            return " ".join(parts)

        elif isinstance(expr, Lambda):
            args_str = ""
            if isinstance(expr.args, Arguments):
                args_str = self._generate_arguments(expr.args)
            body_str = self._safe_generate_expr(expr.body)
            return f"lambda {args_str}: {body_str}"

        elif isinstance(expr, Await):
            value_str = self._safe_generate_expr(expr.value)
            return f"await {value_str}"

        elif isinstance(expr, UnaryOp):
            op_str = getattr(expr.op, "__kw__", str(expr.op))
            operand_str = self._safe_generate_expr(expr.operand)
            return f"{op_str} {operand_str}"

        elif isinstance(expr, (And, Or, Not)):
            return getattr(expr, "__kw__", str(expr))

        elif isinstance(expr, Arg):
            result = expr.arg
            if expr.annotation:
                annotation_str = self._safe_generate_expr(expr.annotation)
                result += f": {annotation_str}"
            return result

        elif isinstance(expr, Starred):
            value_str = self._safe_generate_expr(expr.value)
            return f"*{value_str}"

        elif isinstance(expr, ListComp):
            elt_str = self._safe_generate_expr(expr.elt)
            gens_str = " ".join(
                self._generate_comprehension(c) for c in expr.generators
            )
            return f"[{elt_str} {gens_str}]"

        elif isinstance(expr, SetComp):
            elt_str = self._safe_generate_expr(expr.elt)
            gens_str = " ".join(
                self._generate_comprehension(c) for c in expr.generators
            )
            return f"{{{elt_str} {gens_str}}}"

        elif isinstance(expr, DictComp):
            key_str = self._safe_generate_expr(expr.key)
            value_str = self._safe_generate_expr(expr.value)
            gens_str = " ".join(
                self._generate_comprehension(c) for c in expr.generators
            )
            return f"{{{key_str}: {value_str} {gens_str}}}"

        elif isinstance(expr, GeneratorExp):
            elt_str = self._safe_generate_expr(expr.elt)
            gens_str = " ".join(
                self._generate_comprehension(c) for c in expr.generators
            )
            return f"({elt_str} {gens_str})"

        # Handle TypeParam node specifically
        elif hasattr(expr, "__class__") and expr.__class__.__name__ == "TypeParam":
            # We import TypeParam locally to avoid circular imports if needed,
            # or just rely on the name check but safer.
            # Better: import TypeParam at top or use isinstance if imported.
            from pycraft.nodes.functions import TypeParam

            if isinstance(expr, TypeParam):
                if expr.bound:
                    bound_str = self._safe_generate_expr(expr.bound)
                    return f"{expr.name}: {bound_str}"
                return str(expr.name)

        elif isinstance(
            expr,
            (
                Name,
                Constant,
                Attribute,
                Subscript,
                Call,
                Compare,
                Await,
                UnaryOp,
                Arg,
                Starred,
                Lambda,
                And,
                Or,
                Not,
                In,
                NotIn,
                Is,
                IsNot,
            ),
        ):
            # Handle remaining standard node types using existing logic
            pass  # This part will be handled by the next section

        return str(expr)

    def _generate_comprehension(self, comp: Comprehension) -> str:
        """Generate comprehension string."""

        target_str = self._safe_generate_expr(comp.target)
        iter_str = self._safe_generate_expr(comp.iter)

        prefix = "async for" if comp.is_async else "for"
        parts = [f"{prefix} {target_str} in {iter_str}"]

        for if_clause in comp.ifs:
            if_str = self._generate_expr(if_clause)
            parts.append(f"if {if_str}")

        return " ".join(parts)

    def _generate_comparison_op(self, op: BaseNode) -> str:
        """Generate comparison operator string"""
        from pycraft.nodes import In, Is, IsNot, Name, NotIn

        if isinstance(op, In):
            return "in"
        elif isinstance(op, NotIn):
            return "not in"
        elif isinstance(op, Is):
            return "is"
        elif isinstance(op, IsNot):
            return "is not"
        elif isinstance(op, Name):
            # Handle Name nodes used as operators (e.g., Name(id=">"))
            return op.id

        # Fallback - try to get __kw__
        return getattr(op, "__kw__", str(op))

    def _generate_arguments(self, args: Arguments) -> str:
        """Generate function arguments string"""
        from pycraft.nodes import Arguments

        if not isinstance(args, Arguments):
            return ""

        parts = []

        # Regular args
        for arg in args.args:
            parts.append(self._generate_expr(arg))

        # Keyword-only args
        if args.kwonlyargs:
            if not parts:  # No regular args, add *
                parts.append("*")
            for arg in args.kwonlyargs:
                parts.append(self._generate_expr(arg))

        return ", ".join(parts)

    def _safe_generate_with_item(self, item: BaseNode) -> str:
        """Generate with item string, handling BaseNode."""
        from pycraft.nodes import WithItem

        if isinstance(item, WithItem):
            return self._generate_with_item(item)
        return str(item)

    def _generate_with_item(self, item: WithItem) -> str:
        """Generate with item string."""

        context_str = self._safe_generate_expr(item.context_expr)
        if item.optional_vars:
            vars_str = self._generate_expr(item.optional_vars)
            return f"{context_str} as {vars_str}"
        return context_str
