#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "docs/research/AGENT_REGISTRY.json"

SEARCHES = (
    "AI coding agent sandbox git python",
    "autonomous coding agent sandbox python",
    "software engineering agent docker",
)

ROLE_CAPABILITIES = {
    "RESEARCH_AGENT": {"agent", "local", "git"},
    "SECURITY_AGENT": {"agent", "sandbox", "docker"},
    "VALIDATION_AGENT": {"agent", "testing", "git"},
}


def github_search(query: str) -> list[dict]:
    encoded = urllib.parse.quote(query)
    url = (
        "https://api.github.com/search/repositories"
        f"?q={encoded}&sort=stars&order=desc&per_page=10"
    )

    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "AI_BRIDGE-V3-candidate-discovery",
        },
    )

    with urllib.request.urlopen(request, timeout=15) as response:
        data = json.load(response)

    return data.get("items", [])


def license_name(item: dict) -> str:
    license_data = item.get("license") or {}
    return license_data.get("spdx_id") or "UNKNOWN"


def infer_capabilities(item: dict) -> set[str]:
    text = " ".join(
        str(item.get(key, ""))
        for key in ("name", "full_name", "description", "language", "topics")
    ).lower()

    capabilities = {"agent"}

    if any(x in text for x in ("git", "github", "repository")):
        capabilities.add("git")

    if any(x in text for x in ("test", "pytest", "testing")):
        capabilities.add("testing")

    if any(x in text for x in ("docker", "container", "sandbox")):
        capabilities.update({"docker", "sandbox"})

    if any(x in text for x in ("local", "cli", "terminal")):
        capabilities.add("local")

    return capabilities


def candidate_record(item: dict) -> dict:
    return {
        "name": item["name"],
        "repository": item["clone_url"],
        "github": item["html_url"],
        "license": license_name(item),
        "capabilities": sorted(infer_capabilities(item)),
        "status": "DISCOVERED",
        "stars": item.get("stargazers_count", 0),
        "archived": bool(item.get("archived", False)),
    }


def load_registry() -> dict:
    if not REGISTRY.exists():
        return {"candidates": []}

    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def save_registry(data: dict) -> None:
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def discover() -> list[dict]:
    found: dict[str, dict] = {}

    for query in SEARCHES:
        try:
            items = github_search(query)
        except Exception as exc:
            print(f"SEARCH_ERROR:{query}:{exc}", file=sys.stderr)
            continue

        for item in items:
            if item.get("fork") or item.get("archived"):
                continue

            record = candidate_record(item)
            found[record["github"]] = record

    return sorted(
        found.values(),
        key=lambda item: (-item["stars"], item["name"].lower()),
    )


def role_matches(candidate: dict) -> list[str]:
    capabilities = set(candidate["capabilities"])

    return [
        role
        for role, required in ROLE_CAPABILITIES.items()
        if required.issubset(capabilities)
    ]


def main() -> int:
    registry = load_registry()
    existing = {
        item.get("github") or item.get("repository")
        for item in registry.get("candidates", [])
    }

    discovered = discover()
    new_candidates = [
        item
        for item in discovered
        if item["github"] not in existing
    ]

    for candidate in new_candidates:
        candidate["roles"] = role_matches(candidate)

    print("AI_BRIDGE V3 — CANDIDATE DISCOVERY")
    print(f"DISCOVERED: {len(discovered)}")
    print(f"NEW: {len(new_candidates)}")

    for candidate in new_candidates:
        print(
            f"- {candidate['name']} | "
            f"license={candidate['license']} | "
            f"stars={candidate['stars']} | "
            f"roles={','.join(candidate['roles']) or 'NONE'}"
        )

    if not new_candidates:
        print("DECISION: NO_NEW_CANDIDATES")
        return 0

    registry.setdefault("candidates", []).extend(new_candidates)
    save_registry(registry)

    print("REGISTRY: UPDATED")
    print("STATUS: DISCOVERED_ONLY")
    print("SECURITY: REQUIRED")
    print("SANDBOX: REQUIRED")
    print("CONTRACT: REQUIRED")
    print("PROMOTION: NOT_PERFORMED")

    return 0


if __name__ == "__main__":
    sys.exit(main())
