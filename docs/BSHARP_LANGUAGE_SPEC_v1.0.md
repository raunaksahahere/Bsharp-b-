# B# (B-sharp) Language Specification  
Version: 1.0.0 (Beta)  
Status: Frozen  

This document defines the complete, authoritative specification of the B# programming language as of version 1.0.0 (Beta).  
All behavior described here matches the current reference implementation exactly.  
Future versions must remain backward-compatible unless explicitly versioned otherwise.

---

## 1. Introduction

B# (spoken as “B-sharp”) is a human-centric programming language designed to be written in simple, controlled English while behaving as a real, deterministic programming language.

B# prioritizes:
- Readability and clarity over brevity
- Explicit intent over symbolic syntax
- Beginner-friendly error reporting
- Deterministic execution

B# is not a wrapper, transpiler, or syntax skin over another language.  
It defines its own syntax, grammar, semantics, and runtime behavior.

The current reference implementation is an interpreter that directly executes B# code.

---

## 2. Program Structure

### 2.1 Source Files

- B# programs are stored in files with the `.bsharp` extension.
- A program consists of a sequence of statements.
- Statements are executed sequentially from top to bottom.

### 2.2 Line Execution

- Each line represents a single logical instruction.
- Line breaks are significant.
- There is no statement terminator.

---

## 3. Comments

### 3.1 Syntax
note This is a Comment

### 3.2 Behavior

- Any line starting with `note` is treated as a comment.
- Comments are ignored entirely by the interpreter.
- Comments do not affect execution or scope.

---

## 4. Values and Types

### 4.1 Primitive Types

B# supports the following primitive types:

- integer
- float
- boolean
- string

### 4.2 Collection Types

- list
- dictionary

### 4.3 Type Literals

- Integers: `1`, `42`
- Floats: `3.14`
- Strings: `"text"`
- Booleans: `true`, `false`
- Lists: `[1, 2, 3]`
- Dictionaries: created using `dictionary with ... end`

---

## 5. Variables

### 5.1 Variable Creation
let x be 5

- Creates a new variable named `x`.
- Stores the evaluated value.

### 5.2 Typed Variables
let age be integer 21
let name be string "Alice"

- Type coercion is attempted at runtime.
- Invalid conversions raise runtime errors.

### 5.3 Variable Reassignment
change x to 10

- Updates an existing variable.
- Reassigning an undefined variable raises an error.

### 5.4 Scope Rules

- Variables are block-scoped.
- Functions introduce new scopes.
- Inner scopes may read from outer scopes.
- Reassignment affects the nearest defining scope.

---

## 6. Expressions

### 6.1 Arithmetic Operators

English-based arithmetic is used:

- plus
- minus
- times
- divided by
- modulo

Example:
let x be 5 plus 3

### 6.2 Operator Precedence

From highest to lowest:
1. Primary values
2. Arithmetic operators
3. Comparison operators
4. Logical operators

---

## 7. Comparisons and Logic

### 7.1 Comparison Operators

- is equal to
- is not equal to
- is greater than
- is less than
- is at least
- is at most

### 7.2 Logical Operators

- and
- or
- not

### 7.3 Membership

- does contain
- does not contain

---

## 8. Control Flow

### 8.1 If Statements
if condition then
statements
else if condition then
statements
else
statements
end

- Conditions are evaluated in order.
- The first matching block executes.
- `end` terminates the construct.

---

### 8.2 While Loops
while condition do
statements
end

- Condition is evaluated before each iteration.
- Infinite loops are detected and halted after a safety threshold.

---

### 8.3 For Loops (Range)
for each i from 1 to 10 do
statements
end

- Iterates inclusively from start to end.

---

### 8.4 For Each (Collections)
for each item in collection do
statements
end

- Works on lists, dictionaries (keys), and strings (characters).

---

## 9. Functions

### 9.1 Definition
define function add with a and b do
return a plus b
end

- Functions are first-class values.
- Parameters are positional.

### 9.2 Function Calls
call add with 3 and 5
or
let result be call add with 3 and 5

### 9.3 Return
return value

- Terminates function execution.
- Returns control to the caller.

### 9.4 Recursion

- Fully supported.
- Each call has its own scope.

---

## 10. Lists

### 10.1 Creation
let nums be list of 1, 2, 3

### 10.2 Modification
add 5 to nums
remove 3 from nums

### 10.3 Length
let n be get length of nums

---

## 11. Dictionaries

### 11.1 Creation
let person be dictionary with
name as "Raunak"
age as 21
end

- Keys are strings.
- Values may be any type.

---

## 12. String Operations

### 12.1 Join
let s be join words with ", "

- Joins a list of values into a string.
- Non-string values are converted automatically.

---

## 13. Input and Output

### 13.1 Output
say "Hello", name
- Prints evaluated expressions separated by spaces.

### 13.2 Input
ask "Enter age" as integer and store in age

- Input is read as text.
- Optional type conversion is applied.

---

## 14. File I/O

### 14.1 Read
read from "data.txt" and store in content

### 14.2 Write
write content to "output.txt"

- Files are read and written as UTF-8 text.
- Errors raise runtime exceptions.

---

## 15. Error Handling

### 15.1 Try / Catch
try
statements
catch err
statements
end

- Runtime errors inside `try` are intercepted.
- Error message is stored in `err`.

---

## 16. Explain Keyword
explain

- Prints a human-readable description of the most recent operation.
- If no operation has occurred, a default message is shown.

---

## 17. Trace Mode

- Enabled via command-line flag `--trace`.
- Prints each line before execution.
- Includes line numbers and source text.

---

## 18. Runtime Errors

B# errors are designed to be human-readable.

Examples:
- Variable not found
- Cannot divide by zero
- Type conversion failed
- Invalid operation on type

Errors always include line context when available.

---

## 19. Truthiness Rules

- false, 0, empty string, empty list, empty dictionary → false
- All other values → true

---

## 20. Undefined and Invalid Behavior

The following are invalid:
- Changing an undefined variable
- Calling a non-function
- Iterating over unsupported types
- Using invalid syntax

Such cases always produce runtime or syntax errors.

---

## 21. Conformance

Any implementation claiming to support **B# v1.0.0** must:
- Accept all valid syntax described here
- Reject invalid constructs
- Match runtime behavior and error semantics
- Preserve deterministic execution

---

## 22. Final Statement

This document freezes the behavior of **B# v1.0.0 (Beta)**.

All future work — native runtimes, VMs, compilers, or tooling — must conform to this specification unless a new version explicitly states otherwise.