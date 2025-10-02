#!/usr/bin/env python3
import json, sys, os
fp = "specs/factory.decision.json"
if not os.path.exists(fp):
    print("[ERR] Missing specs/factory.decision.json"); sys.exit(1)
dec = json.load(open(fp))
ok = True
def need(cond, msg):
    global ok
    if not cond:
        print("[ERR]", msg); ok=False
need(dec.get("status") in ("PASS","FAIL"), "status invalid")
need(isinstance(dec.get("reasons",[]), list), "reasons must be list")
nx = dec.get("next",{})
need(all(k in nx for k in ("merge","deploy","rollback")), "next keys missing")
print("ORCHESTRATOR DECISION:", "OK" if ok else "FAIL")
sys.exit(0 if ok else 1)
