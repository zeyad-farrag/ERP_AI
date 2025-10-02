#!/usr/bin/env python3
import json, sys, os, glob, re

def fail(msg):
    print("[ERR]", msg); return False

if not os.path.exists("specs/integrations.summary.json"):
    print("[ERR] Missing specs/integrations.summary.json (agent must produce it)")
    sys.exit(1)

rep = json.load(open("specs/integrations.summary.json"))
ok = True

ok &= rep.get("status") in ("OK","FAIL")
if rep.get("status") != "OK":
    print("[ERR] integrations.summary.status:", rep.get("status"))
    ok = False

# presence checks
required_dirs = [
  "app/Integrations/PayHub",
  "app/Integrations/EmailSms",
  "app/Webhooks",
  "app/Messaging"
]
for d in required_dirs:
    if not os.path.exists(d):
        print("[ERR] Missing directory:", d); ok = False

# tests presence
tests = glob.glob("tests/Integrations/**/*.php", recursive=True)
if not tests:
    print("[ERR] No integration tests found under tests/Integrations"); ok = False

# quick secret scan heuristics (static)
secret_patterns = [r"sk_live_", r"sk_test_", r"api[_-]?key\s*=\s*['\"]", r"Bearer\s+[A-Za-z0-9-_]{20,}"]
for root, _, files in os.walk("app"):
    for f in files:
        if f.endswith((".php",".env",".yml",".yaml",".json")):
            txt = open(os.path.join(root,f), errors="ignore").read()
            for pat in secret_patterns:
                if re.search(pat, txt):
                    print(f"[ERR] Possible secret found in {root}/{f} pattern {pat}")
                    ok = False

print("INTEGRATIONS:", "OK" if ok else "FAIL")
sys.exit(0 if ok else 1)
