# B# (B-sharp) Programming Language

A human-centric programming language written in plain English.

## Quick Start
```bash
# Run a program
python bsharp.py examples/hello.bsharp

# Run with step-by-step trace
python bsharp.py examples/fibonacci.bsharp --trace

# Get help
python bsharp.py --help
```

## Language Reference

| Feature | Syntax |
|---|---|
| Create variable | `let x be 5` |
| Update variable | `change x to 10` |
| Typed variable | `let name be string "Alice"` |
| Print output | `say "Hello", name` |
| Read input | `ask "Your name?" and store in n` |
| Typed input | `ask "Age?" as integer and store in age` |
| Condition | `if x is greater than 5 then ... end` |
| While loop | `while x is less than 10 do ... end` |
| For loop (range) | `for each n from 1 to 10 do ... end` |
| For loop (list) | `for each item in myList do ... end` |
| Define function | `define function add with a and b do ... end` |
| Call function | `call add with 3 and 5` |
| Call + store | `let r be call add with 3 and 5` |
| Return value | `return a plus b` |
| Create list | `let nums be list of 1, 2, 3` |
| Add to list | `add 5 to nums` |
| Remove from list | `remove 5 from nums` |
| Get length | `let len be get length of nums` |
| Join list | `let s be join nums with ", "` |
| Read file | `read from "data.txt" and store in content` |
| Write file | `write content to "output.txt"` |
| Error handling | `try ... catch err ... end` |
| Describe last op | `explain` |
| Comment | `note This is a comment` |

## Comparisons

| English | Meaning |
|---|---|
| `is equal to` | == |
| `is not equal to` | != |
| `is greater than` | > |
| `is less than` | < |
| `is at least` | >= |
| `is at most` | <= |
| `does contain` | in |
| `does not contain` | not in |

## VS Code Extension

1. Copy `vscode-extension/` folder to `~/.vscode/extensions/bsharp/`
2. Restart VS Code
3. `.bsharp` files now have full syntax highlighting

## Requirements

- Python 3.8 or higher
- No external libraries needed
```

---

That's all 12 files. Here's the folder structure to recreate:
```
bsharp/
├── bsharp.py                          ← The interpreter
├── README.md
├── examples/
│   ├── hello.bsharp
│   ├── fibonacci.bsharp
│   ├── lists_and_strings.bsharp
│   ├── fizzbuzz.bsharp
│   ├── error_handling.bsharp
│   ├── dictionary_demo.bsharp
│   └── input_demo.bsharp
└── vscode-extension/
    ├── package.json
    ├── language-configuration.json
    └── syntaxes/
        └── bsharp.tmLanguage.json