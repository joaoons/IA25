#!/usr/bin/env python3
import subprocess
import sys
import time
from pathlib import Path

def run_test(test_input_file):
    base_dir = Path(__file__).parent
    input_path = base_dir / "sample-nuruominoboards" / test_input_file
    test_num = test_input_file.stem.replace("test", "")

    # Handle both .out and .out.txt
    possible_outputs = [
        base_dir / "sample-nuruominoboards" / f"test{test_num}.out.txt",
        base_dir / "sample-nuruominoboards" / f"test{test_num}.out"
    ]

    expected_output_file = None
    for path in possible_outputs:
        if path.exists():
            expected_output_file = path
            break

    if not input_path.exists():
        return f"{test_input_file.name}: Input file not found", 0
    if not expected_output_file:
        return f"{test_input_file.name}: Expected output file not found", 0

    with open(input_path) as f:
        input_data = f.read()
    with open(expected_output_file) as f:
        expected_output = f.read().strip()

    start = time.time()
    try:
        result = subprocess.run(
            [sys.executable, "proj2425base-nuruomino/nuruomino.py"],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=3000,
            cwd=base_dir
        )
    except subprocess.TimeoutExpired:
        return f"{test_input_file.name}: ❌ TIMEOUT (>{3000}s)", 3000.0

    end = time.time()

    elapsed = end - start
    actual_output = result.stdout.strip()

    if result.returncode != 0:
        return f"{test_input_file.name}: ❌ RUNTIME ERROR ({elapsed:.2f}s)\n  {result.stderr.strip()}", elapsed

    if actual_output == expected_output:
        return f"{test_input_file.name}: ✅ PASSED ({elapsed:.2f}s)", elapsed
    else:
        return (
            f"{test_input_file.name}: ❌ FAILED ({elapsed:.2f}s)\nExpected:\n{expected_output}\nGot:\n{actual_output}",
            elapsed,
        )

def main():
    base_dir = Path(__file__).parent
    test_dir = base_dir / "sample-nuruominoboards"
    print(f"Looking for tests in: {test_dir}")

    test_files = sorted(test_dir.glob("test*.txt"))

    print("Running Nuruomino Tests")
    print("=" * 50)

    total = passed = failed = 0
    total_time = 0
    for test_file in test_files:
        result, duration = run_test(test_file)
        total += 1
        total_time += duration
        if "✅" in result:
            passed += 1
        else:
            failed += 1
        print(result)
        print("-" * 40)

    print("\nSUMMARY")
    print("=" * 50)
    print(f"Total tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total time: {total_time:.2f}s")
    print(f"Average time: {total_time/total:.3f}s" if total else "No tests run.")

if __name__ == "__main__":
    main()
