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
