#!/usr/bin/env python3
import json, sys, os

fp = "specs/compliance.summary.json"
if not os.path.exists(fp):
    print("[ERR] Missing specs/compliance.summary.json (Agent 9 must produce it)")
    sys.exit(1)

rep = json.load(open(fp))
ok = True
def need(cond, msg):
    global ok
    if not cond:
        print("[ERR]", msg); ok = False

need(rep.get("status") in ("OK","FAIL"), "status missing/invalid")
need(rep.get("retentionJobsImplemented",0) == rep.get("retentionJobsPlanned",0), "Retention jobs not fully implemented")
need(rep.get("retentionScheduled") is True, "Retention jobs not scheduled")
need(rep.get("exportControlsCoveredPct",0) == 100, "Export controls coverage < 100%")
need(rep.get("auditableMoneyFlowsPct",0) == 100, "Money flows not fully auditable")
need(rep.get("auditLogCoveragePct",0) == 100, "Audit log coverage < 100%")
need(rep.get("provenanceStampPresent") is True, "Provenance stamp missing")
need(rep.get("piiRedactionCoveredPct",0) == 100, "PII redaction coverage < 100%")

print("COMPLIANCE SUMMARY:", "OK" if ok else "FAIL")
sys.exit(0 if ok else 1)
