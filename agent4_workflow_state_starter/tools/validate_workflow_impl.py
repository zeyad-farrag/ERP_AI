#!/usr/bin/env python3
import json, sys, glob, os
summary_fp = "specs/workflow.summary.json"
if not os.path.exists(summary_fp):
    print("[ERR] Missing specs/workflow.summary.json"); sys.exit(1)
rep = json.load(open(summary_fp))
ok = True
if rep.get("status") != "OK": print("[ERR] status", rep.get("status")); ok=False
if rep.get("workflowsImplemented",0) < rep.get("workflowsPlanned",0): print("[ERR] not all workflows implemented"); ok=False
if rep.get("idempotentStepsPct",0) < 100: print("[ERR] steps not idempotent"); ok=False
if not rep.get("hasDLQ"): print("[ERR] no DLQ"); ok=False
if not rep.get("hasParkingLot"): print("[ERR] no parking lot"); ok=False
if rep.get("timeoutsImplementedPct",0) < 100: print("[ERR] timeouts missing"); ok=False
if rep.get("eventsValidatedPct",0) < 100: print("[ERR] events not validated"); ok=False
# presence
def any_glob(p): return bool(glob.glob(p, recursive=True))
if not any_glob("app/Workflow/**/*"): print("[ERR] no state machines"); ok=False
if not any_glob("app/Jobs/**/*"): print("[ERR] no Jobs"); ok=False
if not any_glob("app/Actions/**/*"): print("[ERR] no Actions"); ok=False
print("WORKFLOW IMPLEMENTATION:", "OK" if ok else "FAIL"); sys.exit(0 if ok else 1)
