"""TAC generator scaffold for doc/design.md sections 3.4 and 4.4."""

from .ast_nodes import ASTNode
from .tac import TAC


class TACGenerator:
    """Generate three-address code from a semantically annotated AST."""

    def generate(self, program: ASTNode) -> list[TAC]:
        """Input: a typed Program AST. Output: TAC instructions; implements sections 3.4 and 4.4."""
        raise NotImplementedError("TODO")
