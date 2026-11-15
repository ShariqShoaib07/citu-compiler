# Citu Compiler

Citu is a small, statically typed, C-like teaching language. This repository
contains the initial scaffolding for a compiler pipeline; compiler stages are
placeholders and are not implemented yet.

## Pipeline

```text
Source (.citu) -> Lexer -> Parser -> Semantic Analyzer -> TAC Generator -> TAC Interpreter
```

## Usage

The package uses a `src/` layout. In PowerShell, make it importable from the
workspace root and invoke the CLI:

```powershell
$env:PYTHONPATH = "src"
python -m citu.main examples\hello.citu --emit tok
```

Available `--emit` choices are `tok`, `ast`, `sym`, `tac`, and `run`. Generated
intermediate files are written to `out/`. Stages currently raise
`NotImplementedError("TODO")`.

Install the test dependency and run the test suite with:

```powershell
python -m pip install -r requirements.txt
python -m pytest
```

## Project layout

```text
.
|-- doc/
|   `-- design.md
|-- examples/
|   |-- hello.citu
|   |-- factorial_loop.citu
|   `-- fib.citu
|-- src/
|   `-- citu/
|       |-- __init__.py
|       |-- tokens.py
|       |-- lexer.py
|       |-- ast_nodes.py
|       |-- parser.py
|       |-- symbol_table.py
|       |-- semantic.py
|       |-- tac.py
|       |-- codegen.py
|       |-- interpreter.py
|       `-- main.py
|-- tests/
`-- out/
```

## Implementation status

- [ ] Lexer
- [ ] Parser
- [ ] Semantic analyzer
- [ ] TAC generator
- [ ] TAC interpreter

Authored by Shariq (BSCS23180), ITU.
