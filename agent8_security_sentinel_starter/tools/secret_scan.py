#!/usr/bin/env python3
import os, re, json

patterns = [
  r'sk_live_[A-Za-z0-9]{16,}',
  r'sk_test_[A-Za-z0-9]{16,}',
  r'api[_-]?key\s*[:=]\s*[\'\"][A-Za-z0-9\-_]{16,}[\'\"]',
  r'Bearer\s+[A-Za-z0-9\-_]{20,}',
  r'-----BEGIN (?:RSA|EC) PRIVATE KEY-----'
]

hits = []
for root, _, files in os.walk('.'):
    if root.startswith('./.git') or '/vendor/' in root:
        continue
    for f in files:
        if f.endswith(('.php','.env','.yml','.yaml','.json','.md','.js','.ts')):
            try:
                txt = open(os.path.join(root,f), errors='ignore').read()
            except Exception:
                continue
            for pat in patterns:
                for m in re.finditer(pat, txt):
                    hits.append({"path": f"{root}/{f}", "line": txt[:m.start()].count('\n')+1, "pattern": pat})

print(json.dumps(hits, indent=2))
