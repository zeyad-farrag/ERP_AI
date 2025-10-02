#!/usr/bin/env python3
import json, sys, os

fp = "specs/security.summary.json"
if not os.path.exists(fp):
    print("[ERR] Missing specs/security.summary.json (Agent 8 must produce it)")
    sys.exit(1)

rep = json.load(open(fp))
ok = True
def need(cond, msg):
    global ok
    if not cond:
        print("[ERR]", msg)
        ok = False

need(rep.get("status") in ("OK","FAIL"), "status missing/invalid")
need(rep.get("rbacCoveragePct",0) == 100, "RBAC coverage != 100%")
need(len(rep.get("unauthenticatedRoutes",[]) or []) == 0, "Unauthenticated protected routes found")
need(len(rep.get("secretFindings",[]) or []) == 0, "Secrets detected in repo")
need(len(rep.get("piiLeakFindings",[]) or []) == 0, "PII leaks detected in logs/exports")

sast = rep.get("sast",{})
need(sast.get("high",0) == 0 and sast.get("critical",0) == 0, "SAST high/critical findings present")

dast = rep.get("dast",{})
# If DAST section exists (i.e., preview provided), enforce zero high/critical
if "high" in dast or "critical" in dast:
    need(dast.get("high",0) == 0 and dast.get("critical",0) == 0, "DAST high/critical findings present")

need(rep.get("auditCoveragePct",0) == 100, "Audit coverage < 100% for sensitive ops")

print("SECURITY SUMMARY:", "OK" if ok else "FAIL")
sys.exit(0 if ok else 1)
