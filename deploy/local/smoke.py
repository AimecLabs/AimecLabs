#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

ENDPOINTS = {
    "platform": "http://localhost:8000/health",
    "world_model": "http://localhost:8001/ready",
    "nimble": "http://localhost:8002/health",
    "timesfm": "http://localhost:8003/ready",
    "agent_computer": "http://localhost:8004/ready",
}

failed = []
for name, url in ENDPOINTS.items():
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            ok = 200 <= response.status < 300
            print(json.dumps({"service": name, "url": url, "status": response.status, "ok": ok}))
            if not ok:
                failed.append(name)
    except (urllib.error.URLError, TimeoutError) as exc:
        print(json.dumps({"service": name, "url": url, "ok": False, "error": str(exc)}))
        failed.append(name)

sys.exit(1 if failed else 0)
