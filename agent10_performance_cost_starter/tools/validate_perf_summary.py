#!/usr/bin/env python3
import json, sys, os

fp = "specs/perf.summary.json"
if not os.path.exists(fp):
    print("[ERR] Missing specs/perf.summary.json (Agent 10 must produce it)")
    sys.exit(1)

rep = json.load(open(fp))
ok = True
def need(cond, msg):
    global ok
    if not cond:
        print("[ERR]", msg); ok = False

need(rep.get("status") in ("OK","FAIL"), "status missing/invalid")
need(rep.get("p95ReadMs", 1e9) <= 350, "p95ReadMs exceeds budget")
need(rep.get("p95WriteMs", 1e9) <= 500, "p95WriteMs exceeds budget")
need(rep.get("errorRatePct", 100.0) <= 1.0, "errorRatePct exceeds budget")
need(len(rep.get("nPlusOneFindings",[]) or []) == 0, "N+1 findings present")
need(len(rep.get("unboundedFindings",[]) or []) == 0, "Unbounded query findings present")

print("PERF SUMMARY:", "OK" if ok else "FAIL")
sys.exit(0 if ok else 1)
