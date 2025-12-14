"""Simple test runner that executes test functions without pytest installed.

This imports the test modules and calls their test_... functions, reporting
failures and successes. It's a lightweight fallback when pytest isn't available.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import tests.test_models as test_models
import tests.test_loader as test_loader


def run_module_tests(module):
    failures = 0
    ran = 0
    for name in dir(module):
        if name.startswith("test_"):
            func = getattr(module, name)
            if callable(func):
                ran += 1
                try:
                    func()
                    print(f"OK: {module.__name__}.{name}")
                except AssertionError as e:
                    failures += 1
                    print(f"FAIL: {module.__name__}.{name} -> {e}")
                except Exception as e:
                    failures += 1
                    print(f"ERROR: {module.__name__}.{name} -> {type(e).__name__}: {e}")
    return ran, failures


def main():
    total_ran = 0
    total_fail = 0
    for mod in (test_models, test_loader):
        ran, fail = run_module_tests(mod)
        total_ran += ran
        total_fail += fail

    print(f"\nRan {total_ran} tests, {total_fail} failures")
    sys.exit(1 if total_fail else 0)


if __name__ == "__main__":
    main()
