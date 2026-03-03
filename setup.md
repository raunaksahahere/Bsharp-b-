# B# Setup Guide

Everything you need to install B# and run your first program in under 5 minutes.

---

## Requirements

- **Python 3.8 or higher** — no external packages needed
- **Windows, macOS, or Linux** — all platforms supported

Check your Python version:
```bash
python --version
```

If you see `Python 3.8.x` or higher you are good to go. If Python is not installed, download it from [python.org](https://www.python.org/downloads/).

---

## Installation

### Step 1 — Download B#

**Option A — Clone with Git:**
```bash
git clone https://github.com/your-username/bsharp.git
cd bsharp
```

**Option B — Download ZIP:**
1. Go to the repository page
2. Click **Code → Download ZIP**
3. Extract the ZIP to a folder of your choice, e.g. `C:\Users\You\bsharp` on Windows or `~/bsharp` on macOS/Linux

---

### Step 2 — Verify it works

```bash
python bsharp.py version
```

You should see:
```
B# (B-sharp) Programming Language
Version : 1.0.2-beta
Runtime : Python 3.x.x
Platform: win32 / darwin / linux
```

---

### Step 3 — Run your first program

Create a file called `hello.bsharp`:
```bsharp
say "Hello, World!"
```

Run it:
```bash
python bsharp.py run hello.bsharp
```

Output:
```
Hello, World!
```

---

## Optional — Run as `bsharp` instead of `python bsharp.py`

This lets you type `bsharp run ...` instead of `python bsharp.py run ...`.

### Windows

1. Copy `bsharp.bat` into the same folder as `bsharp.py`
2. Add that folder to your **PATH**:
   - Open the Start menu and search **"Environment Variables"**
   - Click **"Edit the system environment variables"**
   - Click **"Environment Variables..."**
   - Under **User variables**, select **Path** and click **Edit**
   - Click **New** and paste the full path to your B# folder, e.g.:
     ```
     C:\Users\Raunak\Desktop\bsharp_language
     ```
   - Click **OK** on all dialogs
3. **Restart your terminal**

Now you can run:
```
bsharp run hello.bsharp
bsharp version
bsharp help
```

---

### macOS / Linux

Create a small shell script so you can type `bsharp` anywhere.

**Step 1 — Create the script:**
```bash
sudo nano /usr/local/bin/bsharp
```

**Step 2 — Paste this content** (replace the path with your actual B# folder):
```bash
#!/bin/bash
python3 /home/yourname/bsharp/bsharp.py "$@"
```

**Step 3 — Make it executable:**
```bash
sudo chmod +x /usr/local/bin/bsharp
```

**Step 4 — Test it:**
```bash
bsharp version
```

---

## VS Code Syntax Highlighting (Optional)

B# has a VS Code extension that adds syntax highlighting for `.bsharp` files.

### Windows
```
xcopy /E /I vscode-extension "%USERPROFILE%\.vscode\extensions\bsharp"
```

### macOS / Linux
```bash
cp -r vscode-extension ~/.vscode/extensions/bsharp
```

Then **restart VS Code**. Any `.bsharp` file will now have full syntax highlighting.

---

## CLI Commands

Once installed, these commands are available:

| Command | Description |
|---|---|
| `bsharp run <file>` | Run a B# program |
| `bsharp run <file> --trace` | Run with step-by-step trace |
| `bsharp run <file> --debug` | Same as `--trace` |
| `bsharp test` | Run all tests in `tests/cases/` |
| `bsharp test <folder>` | Run tests in a custom folder |
| `bsharp version` | Show version and runtime info |
| `bsharp help` | Show help and library list |

---

## Project Structure

After installation your folder should look like this:

```
bsharp/
├── bsharp.py                    ← The interpreter (this is all you need)
├── bsharp.bat                   ← Windows launcher (for bsharp run ... shortcut)
├── README.md
├── SETUP.md                     ← This file
├── docs/
│   ├── language_tour.md         ← Full language walkthrough
│   └── standard_library_docs.md ← Library reference
├── examples/
│   ├── hello.bsharp
│   ├── fibonacci.bsharp
│   ├── lists_and_strings.bsharp
│   ├── fizzbuzz.bsharp
│   ├── error_handling.bsharp
│   ├── dictionary_demo.bsharp
│   └── input_demo.bsharp
├── tests/
│   ├── cases/                   ← Test programs (.bsharp)
│   └── expected/                ← Expected outputs (.txt)
└── vscode-extension/
    ├── package.json
    ├── language-configuration.json
    └── syntaxes/
        └── bsharp.tmLanguage.json
```

---

## Using Standard Libraries

B# comes with 12 built-in libraries. Import any of them with `use`:

```bsharp
use math
use string
use random

let words be list of "hello", "world", "bsharp"
let chosen be call random.choice with words
say call string.upper with chosen
say call math.sqrt with 144
```

No installation or `pip install` required — everything is built into `bsharp.py`.

Full library reference: see `docs/standard_library_docs.md`

---

## Running the Tests

B# has a built-in test runner. To run the full test suite:

```bash
bsharp test
```

Or with the full Python command:
```bash
python bsharp.py test
```

Expected output:
```
B# Test Runner  v1.0.2-beta
──────────────────────────────────────────────────
  PASS  dictionary
  PASS  functions
  PASS  lists
  PASS  loops
  PASS  variables
──────────────────────────────────────────────────
  Passed: 5   Failed: 0   Total: 5
──────────────────────────────────────────────────
```

---

## Troubleshooting

### `python` not found
On some systems Python 3 is installed as `python3`:
```bash
python3 bsharp.py version
```
On Windows, if `python` is not found, make sure Python was added to PATH during installation. Re-run the Python installer and check **"Add Python to PATH"**.

---

### `bsharp` command not found (Windows)
Make sure:
1. `bsharp.bat` is in the same folder as `bsharp.py`
2. That folder has been added to your system PATH
3. You restarted your terminal after editing PATH

---

### `bsharp` command not found (macOS / Linux)
Check that the shell script exists and is executable:
```bash
ls -la /usr/local/bin/bsharp
```
If it is missing, repeat the macOS/Linux setup steps above.

---

### `tkinter` not found (window library)
The `window` library requires `tkinter`, which is included with most Python installations but may be missing on Linux:
```bash
sudo apt-get install python3-tk      # Ubuntu / Debian
sudo dnf install python3-tkinter     # Fedora
sudo pacman -S tk                    # Arch Linux
```
On macOS, install Python from [python.org](https://www.python.org/downloads/) rather than Homebrew, as it includes tkinter.

---

### Syntax errors in your program
Run with `--trace` to see exactly which line is being executed when the error occurs:
```bash
bsharp run myprogram.bsharp --trace
```

---

## What's Next

- **Language Tour** — `docs/language_tour.md` — full walkthrough of every language feature with examples
- **Standard Library Docs** — `docs/standard_library_docs.md` — complete reference for all 12 libraries
- **Examples** — browse the `examples/` folder for working programs
- **README** — `README.md` — quick reference card for syntax and comparisons