#!/usr/bin/env python3
import json, sys, os

def need(cond, msg, errs):
    if not cond:
        errs.append(msg)

def main():
    fp = "specs/qa.summary.json"
    if not os.path.exists(fp):
        print("[ERR] Missing specs/qa.summary.json (Agent 7 must produce it)")
        sys.exit(1)
    rep = json.load(open(fp))
    errs = []
    need(rep.get("status") in ("OK","FAIL"), "status missing/invalid", errs)
    # Hard thresholds
    need(rep.get("contractPassPct",0) == 100, "contractPassPct != 100", errs)
    need(rep.get("e2ePassPct",0) == 100, "e2ePassPct != 100", errs)
    need(rep.get("visualPassPct",0) == 100, "visualPassPct != 100 (or not approved)", errs)
    need(rep.get("rbacCoveragePct",0) == 100, "rbacCoveragePct != 100", errs)
    need(rep.get("coverageNewCodePct",0) >= 95, "coverageNewCodePct < 95", errs)
    need(rep.get("coverageDropPct",0) <= 2, "coverageDropPct > 2", errs)

    if errs:
        for e in errs: print("[ERR]", e)
        print("QA SUMMARY: FAIL")
        sys.exit(1)
    print("QA SUMMARY: OK")
    sys.exit(0)

if __name__ == "__main__":
    main()
