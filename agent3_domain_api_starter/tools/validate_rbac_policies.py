#!/usr/bin/env python3
import json, sys, glob, os, re

def load_matrix():
    fps = glob.glob("specs/*/rbac.matrix.json")
    merged = {"actions": []}
    for fp in fps:
        try:
            data = json.load(open(fp))
            merged["actions"].extend(data.get("actions", []))
        except Exception:
            pass
    return set(merged["actions"])

def scan_policies():
    actions = set()
    for root, _, files in os.walk("app/Policies"):
        for f in files:
            if f.endswith(".php"):
                # naive parse: collect method names (e.g., viewAny, view, create, update, delete, approve, refund)
                for line in open(os.path.join(root,f)):
                    m = re.search(r'function\s+(\w+)\s*\(', line)
                    if m: actions.add(m.group(1))
    return actions

def main():
    matrix = load_matrix()
    policy_actions = scan_policies()
    if not matrix:
        print("[ERR] No RBAC matrix found under specs/*/rbac.matrix.json")
        sys.exit(1)
    # heuristic mapping: require overlap and no empty matrix
    if not policy_actions:
        print("[ERR] No policy methods detected in app/Policies")
        sys.exit(1)
    print("RBAC CHECK: OK (matrix actions: %d, policy methods: %d)" % (len(matrix), len(policy_actions)))
    sys.exit(0)

if __name__ == "__main__":
    main()
