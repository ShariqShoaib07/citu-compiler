# Citu Compiler: Design Document

**Student:** Shariq (BSCS23180) | **Course:** Compiler Construction | **Repo:** `<https://github.com/ShariqShoaib07/citu-compiler.git>` | **Commit:** `<PASTE COMMIT HASH>`

Citu is a small, statically typed, C-like teaching language. The compiler pipeline is: **Source (.citu) → Lexer → Parser → Semantic Analyzer → TAC Generator → (VM / backend)**. Each stage writes an intermediate file (Section 4).

## 1. Example Programs

### Program 1: Variables, arithmetic, output (`examples/hello.citu`)

```
let int a = 10;
let int b = 3;
let int sum = a + b * 2;
print(sum);
print("Hello, Citu!");
```

Expected output: `16` then `Hello, Citu!`. Demonstrates declarations, operator precedence, string literals and print.

### Program 2: Control flow (`examples/factorial_loop.citu`)

```
let int n = 5;
let int result = 1;
while (n > 1) {
    result = result * n;
    n = n - 1;
}
if (result == 120) {
    print("correct");
} else {
    print("wrong");
}
```

Expected output: `correct`. Demonstrates while, if/else, comparison and assignment.

### Program 3: Functions and recursion (`examples/fib.citu`)

```
func int fib(int n) {
    if (n <= 1) {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}

let int i = 0;
while (i < 8) {
    print(fib(i));
    i = i + 1;
}
```

Expected output: `0 1 1 2 3 5 8 13`. Demonstrates functions, parameters, return values, recursion and scoping.

## 2. Citu Language Grammar

### 2.1 Lexical rules (tokens)

| Token | Pattern / lexeme |
| --- | --- |
| Keywords | `let func if else while return print int bool string true false` |
| IDENTIFIER | `[A-Za-z_][A-Za-z0-9_]*` (not a keyword) |
| INT\_LIT | `[0-9]+` |
| STRING\_LIT | `"` any chars except `"` and newline `"` |
| Arithmetic | `+ - * / %` |
| Comparison | `== != < <= > >=` |
| Logical | `&& \|\| !` |
| Assignment | `=` |
| Punctuation | `( ) { } ; ,` |
| Whitespace | space, tab, newline (ignored) |
| Comment | `//` to end of line (ignored) |
| EOF | end of input |

Rule: the lexer uses longest match (`<=` before `<`). Keywords are checked after matching an identifier. Any other character is a lexical error reported with line and column.

### 2.2 Syntax rules (EBNF)

```
program     = { declaration } EOF ;
declaration = varDecl | funcDecl | statement ;

varDecl     = "let" type IDENTIFIER [ "=" expression ] ";" ;
funcDecl    = "func" type IDENTIFIER "(" [ params ] ")" block ;
params      = type IDENTIFIER { "," type IDENTIFIER } ;
type        = "int" | "bool" | "string" ;

statement   = exprStmt | printStmt | ifStmt | whileStmt
            | returnStmt | block ;
exprStmt    = expression ";" ;
printStmt   = "print" "(" expression ")" ";" ;
ifStmt      = "if" "(" expression ")" block [ "else" block ] ;
whileStmt   = "while" "(" expression ")" block ;
returnStmt  = "return" [ expression ] ";" ;
block       = "{" { declaration } "}" ;

expression  = assignment ;
assignment  = IDENTIFIER "=" assignment | logicOr ;
logicOr     = logicAnd { "||" logicAnd } ;
logicAnd    = equality { "&&" equality } ;
equality    = comparison { ( "==" | "!=" ) comparison } ;
comparison  = term { ( "<" | "<=" | ">" | ">=" ) term } ;
term        = factor { ( "+" | "-" ) factor } ;
factor      = unary { ( "*" | "/" | "%" ) unary } ;
unary       = ( "!" | "-" ) unary | call ;
call        = primary [ "(" [ arguments ] ")" ] ;
arguments   = expression { "," expression } ;
primary     = INT_LIT | STRING_LIT | "true" | "false"
            | IDENTIFIER | "(" expression ")" ;
```

**Precedence (high to low):** unary, `* / %`, `+ -`, comparison, equality, `&&`, `||`, assignment. All binary operators are left-associative; assignment is right-associative.

**Semantic rules:** variables must be declared before use; no redeclaration in the same scope; operand types must match (`int` for arithmetic, `bool` for conditions); call argument count and types must match the function signature; `return` type must match the function type.

## 3. Data Structures

### 3.1 Token and token list

```
Token {
    type:   TokenType   // KEYWORD, IDENT, INT_LIT, STRING_LIT, OP, PUNCT, EOF
    lexeme: string      // exact source text
    line:   int
    column: int
}
TokenList = dynamic array (vector/list) of Token, ending with EOF
```

### 3.2 AST node

```
ASTNode {
    kind:     NodeKind   // Program, VarDecl, FuncDecl, Block, If, While, Return,
                         // Print, Assign, BinaryOp, UnaryOp, Call, Literal, Identifier
    value:    string     // operator, name or literal text
    dtype:    Type       // filled in by the semantic analyzer
    children: [ASTNode]  // ordered child nodes
    line:     int
}
```

Example: `let int x = 1 + 2;` becomes `VarDecl(x, int) -> BinaryOp(+) -> [Literal(1), Literal(2)]`.

### 3.3 Symbol and symbol table

```
Symbol {
    name:      string
    kind:      VARIABLE | FUNCTION | PARAMETER
    dtype:     Type
    scopeLevel:int
    offset:    int          // stack slot / memory index
    params:    [Type]       // functions only
}
Scope       = hash map<string, Symbol>
SymbolTable = stack of Scope
```

Operations: `enterScope()`, `exitScope()`, `declare(sym)` (error if the name already exists in the current scope), `lookup(name)` (search from innermost scope outward).

### 3.4 Three-address code (TAC) instruction

```
TAC { op: string, arg1: string, arg2: string, result: string }
TACProgram = array of TAC
```

Temporaries are named `t0, t1, ...`; labels are named `L0, L1, ...`.

## 4. Intermediate File Formats

Each stage reads the previous stage's file and writes its own, so stages can be tested independently.

### 4.1 Lexer output: `<name>.tok` (one token per line, tab-separated)

```
LINE:COL<TAB>TYPE<TAB>LEXEME
1:1     KEYWORD   let
1:5     KEYWORD   int
1:9     IDENT     a
1:11    OP        =
1:13    INT_LIT   10
1:15    PUNCT     ;
2:1     EOF
```

### 4.2 Parser output: `<name>.ast.json`

```json
{
  "kind": "Program",
  "children": [
    {
      "kind": "VarDecl", "value": "a", "type": "int", "line": 1,
      "children": [ { "kind": "Literal", "value": "10", "type": "int", "children": [] } ]
    }
  ]
}
```

### 4.3 Semantic analyzer output: `<name>.sym` and annotated `<name>.ast.json`

Symbol table dump, one symbol per line, comma-separated:

```
SCOPE,NAME,KIND,TYPE,OFFSET
0,a,VARIABLE,int,0
0,b,VARIABLE,int,1
0,fib,FUNCTION,int(int),-
1,n,PARAMETER,int,0
```

The AST is re-emitted with every node's `type` field filled in. Errors go to stderr as `file:line:col: error: message`.

### 4.4 Code generator output: `<name>.tac`

Format: `op, arg1, arg2, result`, one instruction per line. Operations: `ADD SUB MUL DIV MOD LT LE GT GE EQ NE AND OR NOT NEG ASSIGN LABEL JMP JMPF PARAM CALL RET PRINT`.

For `let int sum = a + b * 2; print(sum);`:

```
MUL,  b,   2,  t0
ADD,  a,   t0, t1
ASSIGN, t1, -, sum
PRINT, sum, -, -
```

For `while (n > 1) { n = n - 1; }`:

```
LABEL, L0, -, -
GT,    n,  1,  t0
JMPF,  t0, L1, -
SUB,   n,  1,  t1
ASSIGN,t1, -,  n
JMP,   L0, -,  -
LABEL, L1, -,  -
```

### 4.5 Final stage (backend)

The TAC is either interpreted by a small stack VM or translated to bytecode `<name>.cbc` (one instruction per line, e.g. `PUSH 10`, `STORE 0`, `LOAD 0`, `ADD`, `PRINT`, `HALT`). Pick one and keep it consistent with the TAC above.

## 5. Git Repository

- **Student ID:** BSCS23180
- **Repository URL:** `<https://github.com/ShariqShoaib07/citu-compiler.git>`
- **Commit:** `<PASTE COMMIT HASH>`
- **Instructor/TA access:** umarsuleman@gmail.com and mscs24052@itu.edu.pk added as collaborators

**Repository layout:**

```
/doc        design document (this file), examples
/examples   hello.citu, factorial_loop.citu, fib.citu
/src        lexer, parser, semantic, codegen
/tests
README.md
```
