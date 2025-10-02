#!/usr/bin/env python3
import glob, sys, os

missing = False
def must_have(glob_pat, label):
    global missing
    files = glob.glob(glob_pat, recursive=True)
    if not files:
        print(f"[ERR] Missing {label}: {glob_pat}")
        missing = True

must_have("tests/Contract/**/*.php", "contract tests (Pest)")
must_have("tests/Unit/**/*.php", "unit tests (Pest)")
must_have("tests/Feature/**/*.php", "feature tests (Pest)")
must_have("tests/E2E/**/*.spec.ts", "E2E tests (Playwright)")
if missing:
    print("TEST PRESENCE: FAIL")
    sys.exit(1)
print("TEST PRESENCE: OK")
