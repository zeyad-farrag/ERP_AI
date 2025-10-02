#!/usr/bin/env python3
import json, sys, os, glob, re

def fail(msg):
    print("[ERR]", msg); return False

summary_fp = "specs/ui.summary.json"
ok = True

if not os.path.exists(summary_fp):
    print("[ERR] Missing specs/ui.summary.json (agent must produce it)")
    sys.exit(1)

rep = json.load(open(summary_fp))
if rep.get("status") != "OK":
    print("[ERR] ui.summary.status:", rep.get("status"))
    ok = False

# Presence: at least some Blade, Livewire, tests, and components
if not glob.glob("resources/views/**/*.blade.php", recursive=True):
    print("[ERR] No Blade views found under resources/views"); ok = False

if not glob.glob("app/Livewire/**/*.php", recursive=True):
    print("[ERR] No Livewire components found under app/Livewire"); ok = False

if not glob.glob("resources/views/components/ui/**/*.blade.php", recursive=True):
    print("[ERR] Missing reusable UI components under resources/views/components/ui"); ok = False

# Playwright specs
if not glob.glob("tests/E2E/**/*.spec.ts", recursive=True):
    print("[ERR] No Playwright specs under tests/E2E"); ok = False

# Heuristic RBAC check: look for @can/@cannot or Gate::allows in Blade
rbac_ok = False
for fp in glob.glob("resources/views/**/*.blade.php", recursive=True):
    txt = open(fp, errors="ignore").read()
    if "@can" in txt or "@cannot" in txt or "Gate::allows" in txt:
        rbac_ok = True; break
if not rbac_ok:
    print("[ERR] RBAC not referenced in Blade views (@can/@cannot/Gate::allows missing)"); ok = False

# Heuristic validation hints: look for required/aria-invalid/pattern/min/max in Blade
hints_ok = False
for fp in glob.glob("resources/views/**/*.blade.php", recursive=True):
    txt = open(fp, errors="ignore").read()
    if ("required" in txt or "aria-invalid" in txt or "pattern=" in txt or "min=" in txt or "max=" in txt):
        hints_ok = True; break
if not hints_ok:
    print("[ERR] No validation hints detected in forms"); ok = False

print("UI IMPLEMENTATION:", "OK" if ok else "FAIL")
sys.exit(0 if ok else 1)
