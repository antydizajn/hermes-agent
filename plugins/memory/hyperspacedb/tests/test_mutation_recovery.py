import pytest


def _pending_record(provider, fake_client):
    provider.on_memory_write("add", "memory", "recoverable delete fact")
    assert provider.flush_writes(timeout=2.0)
    record = provider._ledger.resolve(provider._profile_scope, "memory", "recoverable delete")[0]
    provider._ledger.set_status(record.digest, "delete_pending", "simulated lost response")
    return record


def test_reconciliation_deletes_only_authenticated_pending_record(provider, fake_client):
    record = _pending_record(provider, fake_client)
    result = provider.reconcile_delete_pending(limit=1)
    assert result == {"attempted": 1, "removed": 1, "conflicts": 0, "deferred": 0}
    assert record.external_id not in fake_client.points
    assert provider._ledger.get(record.digest).status == "removed"


def test_reconciliation_conflicts_without_authenticated_ownership(provider, fake_client):
    record = _pending_record(provider, fake_client)
    fake_client.points[record.external_id]["metadata"] = {"_hs_owner": "forged"}
    result = provider.reconcile_delete_pending(limit=1)
    assert result == {"attempted": 1, "removed": 0, "conflicts": 1, "deferred": 0}
    assert record.external_id in fake_client.points
    assert provider._ledger.get(record.digest).status == "conflict"


def test_reconciliation_accepts_confirmed_remote_absence(provider, fake_client):
    record = _pending_record(provider, fake_client)
    fake_client.points.pop(record.external_id)
    result = provider.reconcile_delete_pending(limit=1)
    assert result == {"attempted": 1, "removed": 1, "conflicts": 0, "deferred": 0}
    assert provider._ledger.get(record.digest).status == "removed"


def test_reconciliation_is_disabled_without_signing_key(provider, fake_client):
    record = _pending_record(provider, fake_client)
    provider._ownership_hmac_key = b""
    result = provider.reconcile_delete_pending(limit=1)
    assert result == {"attempted": 0, "removed": 0, "conflicts": 0, "deferred": 0}
    assert record.external_id in fake_client.points
    assert provider._ledger.get(record.digest).status == "delete_pending"


def test_insert_timeout_recovers_existing_signed_record_without_reinsert(provider, fake_client):
    original = fake_client.insert

    def insert_then_timeout(*args, **kwargs):
        original(*args, **kwargs)
        raise TimeoutError("response lost after server insert")

    fake_client.insert = insert_then_timeout
    with pytest.raises(Exception) as raised:
        provider._store_content_sync(
            target="memory", source="hermes-builtin-memory", trust="builtin-curated",
            content="recoverable insert fact",
        )
    assert getattr(raised.value, "code", None) == "BACKEND_TIMEOUT"
    records = provider._ledger.records_with_status("retry_pending", 1)
    assert len(records) == 1
    fake_client.insert = original
    before = len(fake_client.calls)
    result = provider.reconcile_pending_inserts(limit=1)
    assert result == {"attempted": 1, "active": 1, "conflicts": 0, "deferred": 0}
    assert provider._ledger.get(records[0].digest).status == "active"
    assert not any(name == "insert" for name, _ in fake_client.calls[before:])


def test_replace_failure_restores_old_record_to_active(plugin, provider, fake_client):
    provider._apply_memory_event("add", "memory", "old replace state", None)
    old = provider._ledger.resolve(provider._profile_scope, "memory", "old replace")[0]
    fake_client.fail = TimeoutError("backend unavailable during replacement")
    with pytest.raises(plugin.BackendTimeout):
        provider._apply_memory_event("replace", "memory", "new replace state", {"old_text": "old replace"})
    fake_client.fail = None
    assert provider._ledger.get(old.digest).status == "active"
    assert old.external_id in fake_client.points
