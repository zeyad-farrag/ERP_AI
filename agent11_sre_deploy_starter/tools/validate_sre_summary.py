#!/usr/bin/env python3
import json, sys, os

fp = "specs/sre.summary.json"
if not os.path.exists(fp):
    print("[ERR] Missing specs/sre.summary.json (Agent 11 must produce it)")
    sys.exit(1)

rep = json.load(open(fp))
ok = True
def need(cond, msg):
    global ok
    if not cond:
        print("[ERR]", msg); ok = False

need(rep.get("status") in ("OK","FAIL"), "status missing/invalid")
hc = rep.get("healthChecks", {})
need(hc.get("/healthz") == "200" and hc.get("/readyz") == "200", "health checks must be 200")

if rep.get("promoted") is True:
    need(rep.get("errorRateDeltaPct", 100) <= 10, "errorRateDeltaPct > 10 on promote")
    need(rep.get("p95LatencyDeltaPct", 100) <= 15, "p95LatencyDeltaPct > 15 on promote")
else:
    # If not promoted, require rollback to be true
    need(rep.get("rolledBack") is True, "not promoted but no rollback set")

br = rep.get("backupRestoreDrill", {})
need(br.get("backupOk") is True and br.get("restoreOk") is True, "backup/restore drill not OK")

obs = rep.get("observability", {})
need(obs.get("tracing") is True and obs.get("correlationId") is True, "observability tracing/correlation missing")

print("SRE SUMMARY:", "OK" if ok else "FAIL")
sys.exit(0 if ok else 1)
