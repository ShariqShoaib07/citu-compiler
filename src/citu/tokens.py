"""Token types and source token data."""

from dataclasses import dataclass
from enum import Enum


class TokenType(str, Enum):
    """Token categories defined by doc/design.md section 3.1."""

    KEYWORD = "KEYWORD"
    IDENT = "IDENT"
    INT_LIT = "INT_LIT"
    STRING_LIT = "STRING_LIT"
    OP = "OP"
    PUNCT = "PUNCT"
    EOF = "EOF"


@dataclass
class Token:
    """A token with its exact lexeme and source location (section 3.1)."""

    type: TokenType
    lexeme: str
    line: int
    column: int
