import subprocess
import os
import sys

BASE_DIR = os.path.dirname(__file__)
CASES_DIR = os.path.join(BASE_DIR, "cases")
EXPECTED_DIR = os.path.join(BASE_DIR, "expected")

INTERPRETER = os.path.abspath(os.path.join(BASE_DIR, "..", "bsharp.py"))

def run_test(test_name):
    case_path = os.path.join(CASES_DIR, test_name + ".bsharp")
    expected_path = os.path.join(EXPECTED_DIR, test_name + ".txt")

    result = subprocess.run(
        ["python", INTERPRETER, case_path],
        capture_output=True,
        text=True
    )

    output = result.stdout.strip()
    error = result.stderr.strip()

    if os.path.exists(expected_path):
        with open(expected_path, "r", encoding="utf-8") as f:
            expected = f.read().strip()
    else:
        expected = ""

    if output == expected:
        print(f"PASS: {test_name}")
        return True
    else:
        print(f"FAIL: {test_name}")
        print("Expected:")
        print(expected)
        print("Got:")
        print(output)
        return False

def main():
    tests = [f.replace(".bsharp", "") for f in os.listdir(CASES_DIR) if f.endswith(".bsharp")]

    passed = 0
    failed = 0

    for test in tests:
        if run_test(test):
            passed += 1
        else:
            failed += 1

    print("\n====================")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print("====================")

    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()