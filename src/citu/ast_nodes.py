"""AST node kinds and data model."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal


Type = Literal["int", "bool", "string"]


class NodeKind(str, Enum):
    """AST node kinds listed in doc/design.md section 3.2."""

    PROGRAM = "Program"
    VAR_DECL = "VarDecl"
    FUNC_DECL = "FuncDecl"
    BLOCK = "Block"
    IF = "If"
    WHILE = "While"
    RETURN = "Return"
    PRINT = "Print"
    ASSIGN = "Assign"
    BINARY_OP = "BinaryOp"
    UNARY_OP = "UnaryOp"
    CALL = "Call"
    LITERAL = "Literal"
    IDENTIFIER = "Identifier"


@dataclass
class ASTNode:
    """An AST node with ordered children and semantic type (section 3.2)."""

    kind: NodeKind
    value: str
    dtype: Type | None
    children: list["ASTNode"] = field(default_factory=list)
    line: int = 0
