#!/usr/bin/env python3
# Stub that compares counts; replace with real metadata checks later.
import json, sys, yaml
db = yaml.safe_load(open(sys.argv[1]))
rep = json.load(open(sys.argv[2]))
tables = len(db.get("tables", {}) or {})
covered = rep.get("tablesCovered", 0)
if covered < tables:
    print(f"[ERR] Tables covered {covered}/{tables}")
    sys.exit(1)
print("DB-GUARD: OK")
