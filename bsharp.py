import sys

class BSharpRuntime:
    def __init__(self):
        self.variables = {} 

    def evaluate_expression(self, expr):
        expr = expr.strip()
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]
        if expr.isdigit():
            return int(expr)
        if expr in self.variables:
            return self.variables[expr]
        if " plus " in expr:
            a, b = expr.split(" plus ")
            return self.evaluate_expression(a) + self.evaluate_expression(b)
        raise Exception(f"Unknown expression: {expr}")

    def execute_line(self, line):
        line = line.strip()
        if not line or line.startswith("note"):
            return

        if line.startswith("let "):
            parts = line.replace("let ", "").split(" be ")
            name = parts[0].strip()
            value = self.evaluate_expression(parts[1])
            self.variables[name] = value

        elif line.startswith("change "):
            parts = line.replace("change ", "").split(" to ")
            name = parts[0].strip()
            value = self.evaluate_expression(parts[1])
            if name not in self.variables:
                raise Exception(f"Variable '{name}' not defined")
            self.variables[name] = value

        elif line.startswith("say "):
            content = line.replace("say ", "")
            parts = [p.strip() for p in content.split(",")]
            output = []
            for part in parts:
                output.append(str(self.evaluate_expression(part)))
            print(" ".join(output))

        else:
            raise Exception(f"Unknown statement: {line}")

    def run(self, filename):
        with open(filename, "r") as file:
            for line in file:
                self.execute_line(line)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python bsharp.py <file.bsharp>")
        sys.exit(1)

    runtime = BSharpRuntime()
    runtime.run(sys.argv[1])