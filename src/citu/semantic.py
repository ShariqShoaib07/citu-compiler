"""Semantic analyzer scaffold for doc/design.md sections 2.2 and 4.3."""

from .ast_nodes import ASTNode
from .symbol_table import SymbolTable


class SemanticAnalyzer:
    """Check semantic rules and annotate an AST."""

    def analyze(self, program: ASTNode) -> tuple[ASTNode, SymbolTable]:
        """Input: a Program AST. Output: typed AST and symbol table; implements sections 2.2 and 4.3."""
        raise NotImplementedError("TODO")
