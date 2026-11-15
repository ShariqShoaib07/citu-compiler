"""Command-line pipeline for doc/design.md section 4."""

import argparse
import csv
import json
from pathlib import Path

from .ast_nodes import ASTNode
from .codegen import TACGenerator
from .interpreter import TACInterpreter
from .lexer import Lexer
from .parser import Parser
from .semantic import SemanticAnalyzer
from .symbol_table import SymbolKind, SymbolTable
from .tac import TAC
from .tokens import Token, TokenType


def _write_tokens(tokens: list[Token], path: Path) -> None:
    """Write the token format from doc/design.md section 4.1."""
    with path.open("w", encoding="utf-8", newline="") as output:
        for token in tokens:
            if token.type is TokenType.EOF:
                output.write(f"{token.line}:{token.column}\tEOF\n")
            else:
                output.write(
                    f"{token.line}:{token.column}\t{token.type.value}\t{token.lexeme}\n"
                )


def _ast_data(node: ASTNode) -> dict[str, object]:
    return {
        "kind": node.kind.value,
        "value": node.value,
        "type": node.dtype,
        "line": node.line,
        "children": [_ast_data(child) for child in node.children],
    }


def _write_ast(program: ASTNode, path: Path) -> None:
    """Write the AST JSON format from doc/design.md sections 4.2 and 4.3."""
    path.write_text(json.dumps(_ast_data(program), indent=2) + "\n", encoding="utf-8")


def _write_symbols(symbols: SymbolTable, path: Path) -> None:
    """Write the symbol-table format from doc/design.md section 4.3."""
    with path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output, lineterminator="\n")
        writer.writerow(["SCOPE", "NAME", "KIND", "TYPE", "OFFSET"])
        for scope_level, scope in enumerate(symbols.scopes):
            for symbol in scope.values():
                dtype = symbol.dtype
                if symbol.kind is SymbolKind.FUNCTION:
                    dtype = f"{dtype}({','.join(symbol.params)})"
                    offset = "-"
                else:
                    offset = str(symbol.offset)
                writer.writerow(
                    [scope_level, symbol.name, symbol.kind.value, dtype, offset]
                )


def _write_tac(program: list[TAC], path: Path) -> None:
    """Write the TAC text format from doc/design.md section 4.4."""
    path.write_text(
        "".join(
            f"{instruction.op}, {instruction.arg1}, {instruction.arg2}, "
            f"{instruction.result}\n"
            for instruction in program
        ),
        encoding="utf-8",
    )


def _run_pipeline(source_path: Path, emit: str, output_dir: Path) -> None:
    source = source_path.read_text(encoding="utf-8")
    output_dir.mkdir(parents=True, exist_ok=True)
    name = source_path.stem

    tokens = Lexer(source).tokenize()
    _write_tokens(tokens, output_dir / f"{name}.tok")
    if emit == "tok":
        return

    parsed = Parser(tokens).program()
    _write_ast(parsed, output_dir / f"{name}.ast.json")
    if emit == "ast":
        return

    annotated, symbols = SemanticAnalyzer().analyze(parsed)
    _write_ast(annotated, output_dir / f"{name}.ast.json")
    _write_symbols(symbols, output_dir / f"{name}.sym")
    if emit == "sym":
        return

    tac = TACGenerator().generate(annotated)
    _write_tac(tac, output_dir / f"{name}.tac")
    if emit == "tac":
        return

    TACInterpreter().run(tac)


def main(argv: list[str] | None = None) -> None:
    """Parse CLI arguments and run stages through the requested output."""
    argument_parser = argparse.ArgumentParser(description="Citu compiler scaffold")
    argument_parser.add_argument("file", type=Path, help="Citu source file")
    argument_parser.add_argument(
        "--emit",
        choices=("tok", "ast", "sym", "tac", "run"),
        default="run",
        help="last pipeline stage to run",
    )
    arguments = argument_parser.parse_args(argv)
    _run_pipeline(arguments.file, arguments.emit, Path("out"))


if __name__ == "__main__":
    main()
