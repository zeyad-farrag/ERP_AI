#!/usr/bin/env python3
import json, os, sys, yaml

POLICY_FP = ".factory-policy.yml"

# Map summary files to agent keys and minimal checks (belt-and-suspenders; each agent's own CI already checks)
AGENTS = [
  ("spec", "specs/summary.report.json", [("status", ["OK"])]),
  ("db", "specs/db.summary.json", [("status", ["OK"])]),
  ("api", "specs/api.summary.json", [("status", ["OK"])]),
  ("workflow", "specs/workflow.summary.json", [("status", ["OK"])]),
  ("integrations", "specs/integrations.summary.json", [("status", ["OK"])]),
  ("ui", "specs/ui.summary.json", [("status", ["OK"])]),
  ("qa", "specs/qa.summary.json", [("status", ["OK"])]),
  ("security", "specs/security.summary.json", [("status", ["OK"])]),
  ("compliance", "specs/compliance.summary.json", [("status", ["OK"])]),
  ("perf", "specs/perf.summary.json", [("status", ["OK"])]),
  ("sre", "specs/sre.summary.json", [("status", ["OK","FAIL"])])  # allow FAIL if rollback path expected
]

def load_yaml(fp):
    with open(fp, 'r') as f:
        return yaml.safe_load(f)

def load_json(fp):
    with open(fp, 'r') as f:
        return json.load(f)

def main():
    reasons = []
    artifacts = []
    # load policy
    if not os.path.exists(POLICY_FP):
        print("[ERR] Missing .factory-policy.yml")
        sys.exit(2)
    policy = load_yaml(POLICY_FP)
    blockOn = policy.get("automation", {}).get("blockOn", {})
    # collect agent summaries
    summaries = {}
    for key, fp, _checks in AGENTS:
        if not os.path.exists(fp):
            reasons.append({"agent": key, "code": "missing_summary", "detail": fp})
            continue
        try:
            data = load_json(fp)
            summaries[key] = data
            artifacts.append(fp)
        except Exception as e:
            reasons.append({"agent": key, "code": "invalid_json", "detail": f"{fp}: {e}"})
    # hard checks per known summaries
    def err(agent, code, detail):
        reasons.append({"agent": agent, "code": code, "detail": detail})
    # Security
    sec = summaries.get("security")
    if sec:
        if (sec.get("rbacCoveragePct",0) != 100): err("security","rbac_coverage","<100%")
        if sec.get("unauthenticatedRoutes"): err("security","unauth_routes", str(sec["unauthenticatedRoutes"]))
        if sec.get("secretFindings"): err("security","secrets_detected", str(sec["secretFindings"]))
        if sec.get("piiLeakFindings"): err("security","pii_leaks", str(sec["piiLeakFindings"]))
        sast = sec.get("sast",{})
        if sast.get("high",0) or sast.get("critical",0): err("security","sast_high","high/critical present")
        dast = sec.get("dast",{})
        if ("high" in dast or "critical" in dast) and (dast.get("high",0) or dast.get("critical",0)):
            err("security","dast_high","high/critical present")
        if sec.get("auditCoveragePct",0) != 100: err("security","audit_coverage","<100%")

    # QA
    qa = summaries.get("qa")
    if qa:
        if qa.get("contractPassPct",0) != 100: err("qa","contract_not_100","")
        if qa.get("e2ePassPct",0) != 100: err("qa","e2e_not_100","")
        if qa.get("visualPassPct",0) != 100: err("qa","visual_not_100","")
        if qa.get("rbacCoveragePct",0) != 100: err("qa","rbac_not_100","")
        if qa.get("coverageNewCodePct",0) < 95: err("qa","coverage_low","")
        if qa.get("coverageDropPct",0) > 2: err("qa","coverage_drop","")

    # Compliance
    comp = summaries.get("compliance")
    if comp:
        if comp.get("retentionJobsImplemented",0) != comp.get("retentionJobsPlanned",0): err("compliance","retention_incomplete","")
        if not comp.get("retentionScheduled"): err("compliance","retention_unscheduled","")
        if comp.get("exportControlsCoveredPct",0) != 100: err("compliance","export_controls","<100%")
        if comp.get("auditableMoneyFlowsPct",0) != 100: err("compliance","money_flows","<100%")
        if comp.get("auditLogCoveragePct",0) != 100: err("compliance","audit_coverage","<100%")
        if not comp.get("provenanceStampPresent"): err("compliance","provenance","missing")
        if comp.get("piiRedactionCoveredPct",0) != 100: err("compliance","pii_redaction","<100%")

    # Performance
    perf = summaries.get("perf")
    if perf:
        if perf.get("p95ReadMs", 10**9) > 350: err("perf","p95_read","exceeds")
        if perf.get("p95WriteMs", 10**9) > 500: err("perf","p95_write","exceeds")
        if perf.get("errorRatePct", 100.0) > 1.0: err("perf","error_rate","exceeds")
        if perf.get("nPlusOneFindings"): err("perf","nplus1","present")
        if perf.get("unboundedFindings"): err("perf","unbounded","present")

    # SRE
    sre = summaries.get("sre")
    if sre:
        hc = sre.get("healthChecks", {})
        if hc.get("/healthz") != "200" or hc.get("/readyz") != "200":
            err("sre","healthchecks","non-200")
        if sre.get("promoted") is True:
            if sre.get("errorRateDeltaPct",100) > 10: err("sre","promote_error_rate_delta",">10%")
            if sre.get("p95LatencyDeltaPct",100) > 15: err("sre","promote_latency_delta",">15%")
        else:
            if sre.get("rolledBack") is not True:
                err("sre","rollback_missing","not promoted and no rollback true")
        br = sre.get("backupRestoreDrill",{})
        if br.get("backupOk") is not True or br.get("restoreOk") is not True:
            err("sre","backup_restore","failed")
        obs = sre.get("observability",{})
        if not (obs.get("tracing") and obs.get("correlationId")):
            err("sre","observability","tracing/correlation missing")

    # Decide PASS/FAIL
    status = "PASS" if not reasons else "FAIL"
    decision = {
        "status": status,
        "reasons": reasons,
        "artifacts": artifacts,
        "next": {
            "merge": status == "PASS",
            "deploy": status == "PASS",
            "rollback": any(r["agent"]=="sre" and r["code"].startswith("promote_") for r in reasons)
        }
    }
    os.makedirs("specs", exist_ok=True)
    with open("specs/factory.decision.json","w") as f:
        json.dump(decision, f, indent=2)
    print(json.dumps(decision, indent=2))
    sys.exit(0 if status=="PASS" else 1)

if __name__ == "__main__":
    main()
