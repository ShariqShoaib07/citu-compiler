"""Symbol and scoped symbol-table data structures."""

from dataclasses import dataclass, field
from enum import Enum

from .ast_nodes import Type


class SymbolKind(str, Enum):
    """Symbol categories defined in doc/design.md section 3.3."""

    VARIABLE = "VARIABLE"
    FUNCTION = "FUNCTION"
    PARAMETER = "PARAMETER"


@dataclass
class Symbol:
    """A declared name and its storage/signature data (section 3.3)."""

    name: str
    kind: SymbolKind
    dtype: Type
    scopeLevel: int
    offset: int
    params: list[Type] = field(default_factory=list)


Scope = dict[str, Symbol]


class SymbolTable:
    """A stack of scopes with outward name lookup (section 3.3)."""

    def __init__(self) -> None:
        self.scopes: list[Scope] = [{}]

    def enter_scope(self) -> None:
        """Push an empty scope."""
        self.scopes.append({})

    def exit_scope(self) -> Scope:
        """Pop and return the innermost scope, preserving the global scope."""
        if len(self.scopes) == 1:
            raise RuntimeError("Cannot exit the global scope")
        return self.scopes.pop()

    def declare(self, symbol: Symbol) -> None:
        """Declare a symbol in the current scope or raise ValueError on redeclaration."""
        scope = self.scopes[-1]
        if symbol.name in scope:
            raise ValueError(f"Symbol already declared in this scope: {symbol.name}")
        scope[symbol.name] = symbol

    def lookup(self, name: str) -> Symbol | None:
        """Find a symbol from innermost scope outward, or return None."""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
