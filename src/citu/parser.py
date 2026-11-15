"""Parser scaffold for doc/design.md section 2.2."""

from .ast_nodes import ASTNode, Type
from .tokens import Token


class Parser:
    """Parse a token list using the Citu grammar."""

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens

    def program(self) -> ASTNode:
        """Input: the parser's token list. Output: a Program node; implements section 2.2 rule `program`."""
        raise NotImplementedError("TODO")

    def declaration(self) -> ASTNode:
        """Input: the next declaration tokens. Output: a declaration node; implements section 2.2 rule `declaration`."""
        raise NotImplementedError("TODO")

    def var_decl(self) -> ASTNode:
        """Input: the next variable-declaration tokens. Output: a VarDecl node; implements section 2.2 rule `varDecl`."""
        raise NotImplementedError("TODO")

    def func_decl(self) -> ASTNode:
        """Input: the next function-declaration tokens. Output: a FuncDecl node; implements section 2.2 rule `funcDecl`."""
        raise NotImplementedError("TODO")

    def params(self) -> list[tuple[Type, str]]:
        """Input: the next parameter tokens. Output: ordered type/name pairs; implements section 2.2 rule `params`."""
        raise NotImplementedError("TODO")

    def type(self) -> Type:
        """Input: the next type token. Output: its Citu type; implements section 2.2 rule `type`."""
        raise NotImplementedError("TODO")

    def statement(self) -> ASTNode:
        """Input: the next statement tokens. Output: a statement node; implements section 2.2 rule `statement`."""
        raise NotImplementedError("TODO")

    def expr_stmt(self) -> ASTNode:
        """Input: the next expression-statement tokens. Output: an expression statement node; implements section 2.2 rule `exprStmt`."""
        raise NotImplementedError("TODO")

    def print_stmt(self) -> ASTNode:
        """Input: the next print-statement tokens. Output: a Print node; implements section 2.2 rule `printStmt`."""
        raise NotImplementedError("TODO")

    def if_stmt(self) -> ASTNode:
        """Input: the next if-statement tokens. Output: an If node; implements section 2.2 rule `ifStmt`."""
        raise NotImplementedError("TODO")

    def while_stmt(self) -> ASTNode:
        """Input: the next while-statement tokens. Output: a While node; implements section 2.2 rule `whileStmt`."""
        raise NotImplementedError("TODO")

    def return_stmt(self) -> ASTNode:
        """Input: the next return-statement tokens. Output: a Return node; implements section 2.2 rule `returnStmt`."""
        raise NotImplementedError("TODO")

    def block(self) -> ASTNode:
        """Input: the next block tokens. Output: a Block node; implements section 2.2 rule `block`."""
        raise NotImplementedError("TODO")

    def expression(self) -> ASTNode:
        """Input: the next expression tokens. Output: an expression node; implements section 2.2 rule `expression`."""
        raise NotImplementedError("TODO")

    def assignment(self) -> ASTNode:
        """Input: the next assignment tokens. Output: an assignment or logicOr node; implements section 2.2 rule `assignment`."""
        raise NotImplementedError("TODO")

    def logic_or(self) -> ASTNode:
        """Input: the next logical-OR tokens. Output: an expression node; implements section 2.2 rule `logicOr`."""
        raise NotImplementedError("TODO")

    def logic_and(self) -> ASTNode:
        """Input: the next logical-AND tokens. Output: an expression node; implements section 2.2 rule `logicAnd`."""
        raise NotImplementedError("TODO")

    def equality(self) -> ASTNode:
        """Input: the next equality tokens. Output: an expression node; implements section 2.2 rule `equality`."""
        raise NotImplementedError("TODO")

    def comparison(self) -> ASTNode:
        """Input: the next comparison tokens. Output: an expression node; implements section 2.2 rule `comparison`."""
        raise NotImplementedError("TODO")

    def term(self) -> ASTNode:
        """Input: the next additive tokens. Output: an expression node; implements section 2.2 rule `term`."""
        raise NotImplementedError("TODO")

    def factor(self) -> ASTNode:
        """Input: the next multiplicative tokens. Output: an expression node; implements section 2.2 rule `factor`."""
        raise NotImplementedError("TODO")

    def unary(self) -> ASTNode:
        """Input: the next unary-expression tokens. Output: an expression node; implements section 2.2 rule `unary`."""
        raise NotImplementedError("TODO")

    def call(self) -> ASTNode:
        """Input: the next call-expression tokens. Output: a call or primary node; implements section 2.2 rule `call`."""
        raise NotImplementedError("TODO")

    def arguments(self) -> list[ASTNode]:
        """Input: the next argument tokens. Output: ordered argument nodes; implements section 2.2 rule `arguments`."""
        raise NotImplementedError("TODO")

    def primary(self) -> ASTNode:
        """Input: the next primary-expression token(s). Output: a primary node; implements section 2.2 rule `primary`."""
        raise NotImplementedError("TODO")
