#!/usr/bin/env python3
"""SportSyncAI Identity API — minimal example client.

Calls the two public endpoints only, over HTTPS, against the real hosted
service. Contains no SportSyncAI internal code — this is exactly what a
partner's own backend would do, in the simplest form possible.

Usage:
    SPORTSYNCAI_API_KEY=<your key> python3 example.py

Or via Docker (see ../README.md):
    docker run -e SPORTSYNCAI_API_KEY=<your key> sportsyncai-example
"""
import json
import os
import sys
import urllib.error
import urllib.request

BASE_URL = os.environ.get("SPORTSYNCAI_BASE_URL", "https://sportsyncai.site")
API_KEY = os.environ.get("SPORTSYNCAI_API_KEY", "")


def _get(path: str):
    with urllib.request.urlopen(f"{BASE_URL}{path}", timeout=15) as resp:
        return json.loads(resp.read())


def _post(path: str, body: dict, headers: dict):
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=json.dumps(body).encode("utf-8"),
        headers={**headers, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def main() -> int:
    if not API_KEY:
        print("Set SPORTSYNCAI_API_KEY before running. Contact SportSyncAI to get one.")
        return 1

    print(f"1. Fetching the question catalog from {BASE_URL} ...")
    catalog = _get("/api/v1/integrate/questions")
    question = catalog["questions"][0]
    print(f"   Got {len(catalog['questions'])} questions.")
    print(f"   Using: \"{question['question_en']}\"")

    answer_text = question["options"][0]["text_en"]
    print(f"   Answering: \"{answer_text}\"")
    print()

    print("2. Sending the answer to POST /api/v1/integrate/identity ...")
    status, result = _post(
        "/api/v1/integrate/identity",
        {"answers": [{"question_key": question["key"], "answer_text": answer_text}],
         "language": "en"},
        {"X-API-Key": API_KEY},
    )
    print(f"   HTTP {status}")
    print()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if status == 200 else 1


if __name__ == "__main__":
    sys.exit(main())
