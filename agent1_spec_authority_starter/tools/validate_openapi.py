#!/usr/bin/env python3
import json, sys

with open(sys.argv[1]) as f:
    openapi = json.load(f)

ok = True
# Check x-sourcePath on schema properties
for name, schema in openapi.get("components", {}).get("schemas", {}).items():
    for prop, spec in schema.get("properties", {}).items():
        if "x-sourcePath" not in spec:
            print(f"[ERR] {name}.{prop} missing x-sourcePath")
            ok = False

# Check x-rbac on operations
for path, ops in openapi.get("paths", {}).items():
    for method, op in ops.items():
        if isinstance(op, dict):
            if not op.get("x-rbac"):
                print(f"[ERR] {method.upper()} {path} missing x-rbac")
                ok = False

print("VALIDATION:", "OK" if ok else "FAIL")
sys.exit(0 if ok else 1)
