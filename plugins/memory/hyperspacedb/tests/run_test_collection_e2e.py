"""Operator-authorized E2E against a dedicated HyperspaceDB test collection.

Required environment:
- HSDB_TEST_SOURCE_COLLECTION: existing read-only fixture source
- HSDB_TEST_COLLECTION: dedicated target collection

The script never deletes a collection. It copies a bounded fixture sample, then
verifies provider add/replace/remove using synthetic records in the target only.
No fixture content is printed.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
import time
from pathlib import Path

from hyperspace import HyperspaceClient

ROOT = Path(__file__).resolve().parents[1]


def load_provider_module():
    name = "hsdb_plugin_e2e"
    spec = importlib.util.spec_from_file_location(name, ROOT / "__init__.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def content_of(raw):
    value = raw.get("payload")
    if isinstance(value, bytes):
        text = value.decode("utf-8", "replace")
        if text:
            return text
    if isinstance(value, str) and value:
        return value
    meta = raw.get("metadata") or {}
    for key in ("_content", "content", "text", "document", "body"):
        if meta.get(key):
            return str(meta[key])
    return ""


def candidate_id(material, probe):
    digest = hashlib.sha256(f"{material}:{probe}".encode("utf-8", "replace")).digest()
    return int.from_bytes(digest[:4], "big") or 1


def close_client(client):
    seen = set()
    for channel in list(getattr(client, "channels", []) or []) + [getattr(client, "channel", None)]:
        if channel is None or id(channel) in seen:
            continue
        seen.add(id(channel))
        channel.close()


def main():
    source = os.environ.get("HSDB_TEST_SOURCE_COLLECTION", "").strip()
    target = os.environ.get("HSDB_TEST_COLLECTION", "").strip()
    if not source or not target or source == target:
        raise SystemExit("Distinct HSDB_TEST_SOURCE_COLLECTION and HSDB_TEST_COLLECTION are required")
    host = os.environ.get("HYPERSPACE_HOST", "127.0.0.1:50051")
    key = os.environ.get("HYPERSPACE_API_KEY") or None
    user_id = os.environ.get("HYPERSPACE_USER_ID") or None
    client = HyperspaceClient(host=host, api_key=key, user_id=user_id, pool_size=2)
    summary = {
        "source_exists": False,
        "target_created": False,
        "fixtures_copied": 0,
        "payload_search_verified": False,
        "add_verified": False,
        "replace_verified": False,
        "remove_verified": False,
    }
    try:
        collections = client.list_collections()
        names = {str(item.get("name")) for item in collections if isinstance(item, dict)}
        summary["source_exists"] = source in names
        if source not in names:
            raise RuntimeError("Source fixture collection does not exist")
        if target not in names:
            ok = client.create_collection(target, dimension=129, metric="lorentz")
            if ok is not True:
                raise RuntimeError("Test collection creation did not return True")
            summary["target_created"] = True

        fixture_rows = client.scroll(limit=24, offset=0, collection=source)
        first_query = ""
        for raw in fixture_rows:
            if not isinstance(raw, dict):
                continue
            text = content_of(raw).strip()
            if not text:
                continue
            if not first_query:
                first_query = text[: min(180, len(text))]
            material = f"fixture:{raw.get('id')}:{text}"
            record_id = None
            for probe in range(64):
                proposed = candidate_id(material, probe)
                existing = client.get_points([proposed], collection=target)
                if not existing:
                    record_id = proposed
                    break
                meta = existing[0].get("metadata") or {}
                if meta.get("fixture_digest") == hashlib.sha256(material.encode()).hexdigest():
                    record_id = proposed
                    break
            if record_id is None:
                raise RuntimeError("Fixture uint32 allocation exhausted")
            vector = client.vectorize(text, metric="lorentz")
            ok = client.insert(
                record_id,
                vector=vector,
                document=text,
                payload=text.encode("utf-8", "replace"),
                metadata={
                    "source": "operator-authorized-test-fixture",
                    "trust": "test-fixture",
                    "fixture_digest": hashlib.sha256(material.encode()).hexdigest(),
                },
                collection=target,
                durability=3,
            )
            if ok is not True:
                raise RuntimeError("Fixture insert did not return True")
            summary["fixtures_copied"] += 1

        if not first_query or summary["fixtures_copied"] == 0:
            raise RuntimeError("No textual fixture could be copied")

        module = load_provider_module()
        provider = module.HyperspaceDBMemoryProvider({
            "host": host,
            "collection": target,
            "metric": "lorentz",
            "api_key_env": "HYPERSPACE_API_KEY",
            "user_id_env": "HYPERSPACE_USER_ID",
            "state_path": str(ROOT / "state" / "test-collection-e2e.sqlite3"),
            "profile_scope": "e2e-test-scope",
            "trust_mode": "annotate_all",
            "rpc_timeout": 4.0,
            "top_k": 5,
            "auto_store": True,
        })
        provider.initialize("e2e-test-session")
        try:
            search = json.loads(provider.handle_tool_call(
                "hyperspace_search", {"query": first_query, "limit": 5}
            ))
            summary["payload_search_verified"] = bool(
                search.get("ok") and search.get("results")
                and any(item.get("content") for item in search["results"])
            )

            nonce = hashlib.sha256(f"{time.time_ns()}".encode()).hexdigest()[:16]
            old = f"provider e2e old fact {nonce}"
            new = f"provider e2e new fact {nonce}"
            provider.on_memory_write("add", "memory", old)
            if not provider.flush_writes(timeout=10.0):
                raise RuntimeError("Add queue did not drain")
            rows = [r for r in provider._ledger.active_records("memory") if nonce in r["content"]]
            summary["add_verified"] = len(rows) == 1 and bool(
                client.get_points([rows[0]["external_id"]], collection=target)
            )

            provider.on_memory_write(
                "replace", "memory", new, {"old_text": f"old fact {nonce}"}
            )
            if not provider.flush_writes(timeout=10.0):
                raise RuntimeError("Replace queue did not drain")
            rows = [r for r in provider._ledger.active_records("memory") if nonce in r["content"]]
            summary["replace_verified"] = (
                len(rows) == 1 and rows[0]["content"] == new
                and bool(client.get_points([rows[0]["external_id"]], collection=target))
            )

            provider.on_memory_write(
                "remove", "memory", "", {"old_text": f"new fact {nonce}"}
            )
            if not provider.flush_writes(timeout=10.0):
                raise RuntimeError("Remove queue did not drain")
            rows = [r for r in provider._ledger.active_records("memory") if nonce in r["content"]]
            summary["remove_verified"] = rows == []
        finally:
            provider.shutdown()

        required = [
            "source_exists", "payload_search_verified", "add_verified",
            "replace_verified", "remove_verified",
        ]
        if not all(summary[key] for key in required):
            raise RuntimeError(f"E2E verification failed: {summary}")
        print(json.dumps({"ok": True, **summary}, sort_keys=True))
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
