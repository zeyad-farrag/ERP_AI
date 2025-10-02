#!/usr/bin/env python3
import json, sys, os

if len(sys.argv) < 2:
    print("Usage: validate_db_summary.py specs/db.summary.json")
    sys.exit(2)

with open(sys.argv[1]) as f:
    rep = json.load(f)

ok = True
def need(k, cond, msg):
    global ok
    if not cond:
        print(f"[ERR] {msg}")
        ok = False

need("status", rep.get("status") in ("OK","FAIL"), "status missing/invalid")
if rep.get("status") == "OK":
    need("tables", rep.get("tablesImplemented") == rep.get("tablesPlanned"), "tablesImplemented != tablesPlanned")
    need("fk", rep.get("fkCoveragePct",0) == 100, "FK coverage < 100%")
    need("idx", rep.get("indexCoveragePct",0) == 100, "Index coverage < 100%")
    need("casts", rep.get("castsCoveragePct",0) >= 95, "Casts coverage < 95%")
if rep.get("drift"):
    print("[ERR] Drift detected:", rep["drift"][:5])
    ok = False

print("DB SUMMARY:", "OK" if ok else "FAIL")
sys.exit(0 if ok else 1)
