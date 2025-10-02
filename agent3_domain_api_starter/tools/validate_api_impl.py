#!/usr/bin/env python3
import json, sys, os, glob, re

def load_openapi(fp):
    with open(fp) as f:
        return json.load(f)

def count_endpoints(spec):
    c=0
    for p, ops in spec.get("paths", {}).items():
        for m, op in ops.items():
            if isinstance(op, dict) and m.lower() in ["get","post","put","patch","delete"]:
                c+=1
    return c

def has_rfc7807(op):
    # basic heuristic: look for application/problem+json in responses
    resps = op.get("responses",{})
    for code, r in resps.items():
        content = r.get("content", {})
        if "application/problem+json" in content:
            return True
    return False

def scan_impl():
    controllers = glob.glob("app/Http/Controllers/**/*.php", recursive=True)
    requests = glob.glob("app/Http/Requests/**/*Request.php", recursive=True)
    policies = glob.glob("app/Policies/**/*.php", recursive=True)
    services = glob.glob("app/Services/**/*.php", recursive=True)
    resources = glob.glob("app/Http/Resources/**/*.php", recursive=True)
    tests = glob.glob("tests/**/*", recursive=True)
    return {
        "controllers": len(controllers),
        "requests": len(requests),
        "policies": len(policies),
        "services": len(services),
        "resources": len(resources),
        "tests": len([t for t in tests if t.endswith(".php")])
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: validate_api_impl.py specs/<context>/openapi.json")
        sys.exit(2)
    # allow multi-context check
    specs = []
    arg = sys.argv[1]
    if os.path.isdir(arg):
        specs = glob.glob(os.path.join(arg, "*/openapi.json"))
    else:
        specs = [arg]

    total_planned=0
    total_rfc7807=0
    for fp in specs:
        spec = load_openapi(fp)
        ep = count_endpoints(spec)
        total_planned += ep
        for pth, ops in spec.get("paths", {}).items():
            for m, op in ops.items():
                if isinstance(op, dict) and m.lower() in ["get","post","put","patch","delete"]:
                    if has_rfc7807(op):
                        total_rfc7807 += 1

    impl = scan_impl()

    ok = True
    if total_planned == 0:
        print("[ERR] No endpoints found in OpenAPI")
        ok = False
    else:
        # Heuristic: require at least as many Requests as write endpoints and at least some controllers
        if impl["controllers"] == 0:
            print("[ERR] No controllers implemented")
            ok = False
        if impl["services"] == 0:
            print("[ERR] No services implemented")
            ok = False
        if impl["requests"] == 0:
            print("[ERR] No FormRequest classes implemented")
            ok = False
        if impl["resources"] == 0:
            print("[ERR] No API Resource classes implemented")
            ok = False
        if impl["tests"] == 0:
            print("[ERR] No tests present")
            ok = False

    # RFC7807 coverage heuristic
    if total_planned and total_rfc7807 < total_planned:
        print(f"[ERR] RFC7807 not declared for all endpoints ({total_rfc7807}/{total_planned})")
        ok = False

    print("API IMPLEMENTATION:", "OK" if ok else "FAIL")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
