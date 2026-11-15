"""Lexer scaffold for doc/design.md section 2.1."""

from .tokens import Token


class Lexer:
    """Convert Citu source text into a token list."""

    def __init__(self, source: str) -> None:
        self.source = source

    def tokenize(self) -> list[Token]:
        """Input: source text. Output: tokens ending with EOF; implements section 2.1."""
        raise NotImplementedError("TODO")
