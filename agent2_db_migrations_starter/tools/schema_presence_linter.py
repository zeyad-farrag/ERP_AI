#!/usr/bin/env python3
import os, sys, json, glob

# This linter checks presence patterns only (agent-generated code must exist)
missing = []

# Expect migrations & models exist when specs are present
for ctx in glob.glob("specs/*/schemas"):
    for schema_fp in glob.glob(os.path.join(ctx, "*.json")):
        name = os.path.splitext(os.path.basename(schema_fp))[0]
        model_fp = f"app/Models/{name.capitalize()}.php"
        if not os.path.exists(model_fp):
            missing.append(model_fp)

if missing:
    print("[ERR] Missing generated models/migrations for some schemas (first 10):")
    for m in missing[:10]:
        print(" -", m)
    sys.exit(1)

print("SCHEMA LINTER: OK")
