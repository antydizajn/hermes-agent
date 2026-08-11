# HyperspaceDB Memory Provider for Hermes Agent

A public Hermes Agent `MemoryProvider` backed by an existing HyperspaceDB
collection. The plugin mirrors curated built-in memory mutations, exposes eight
bounded memory tools, and keeps a local identity ledger so `add`, `replace`, and
`remove` do not silently diverge.

## Status

Version 0.2.0 is hardened at the source and unit-contract levels. A deployment
is not E2E verified until its operator runs an authorized add/replace/remove
probe against a dedicated test collection.

## Requirements

- Hermes Agent with the public `MemoryProvider` plugin interface.
- `hyperspacedb>=3.1.3,<4` in the Hermes Python environment.
- A reachable HyperspaceDB gRPC server.
- An existing collection whose metric matches the configured `metric`.

The plugin never creates or deletes collections automatically.

## Install

Copy this directory to the active Hermes profile's memory plugin directory:

```text
$HERMES_HOME/plugins/memory/hyperspacedb
```

Then configure the provider and start a new Hermes session. Do not put API keys
in this repository.

## Configuration

```yaml
memory:
  provider: hyperspacedb
  hyperspacedb:
    host: 127.0.0.1:50051
    collection: hermes_memory
    metric: lorentz
    top_k: 5
    rpc_timeout: 4.0
    auto_store: true
    trust_mode: owned_only
    api_key_env: HYPERSPACE_API_KEY
    user_id_env: HYPERSPACE_USER_ID
```

`collection` is required. There is deliberately no private or deployment-
specific collection default.

### Important options

- `host`: gRPC endpoint. Plaintext remote endpoints are rejected by default.
- `collection`: one existing physical collection used by this provider.
- `metric`: vectorization metric; `lorentz` is the default.
- `rpc_timeout`: clamped to 0.1-7.0 seconds so Hermes prefetch remains bounded.
- `state_path`: optional SQLite identity ledger path. The default is derived
  from the active Hermes home, not from a hardcoded user path.
- `auto_store`: mirrors curated built-in memory writes.
- `trust_mode`: `owned_only` or `annotate_all` for automatic prefetch.
- `trusted_sources`: additional source labels allowed by `owned_only`.
- `max_distance`: optional deployment-calibrated rejection threshold. There is
  no guessed universal threshold because distance distributions are metric and
  corpus dependent.
- `allow_collection_override`: off by default. Even when enabled, a collection
  must also appear in `allowed_collections`.
- `allow_insecure_remote`: off by default. Enable only when gRPC is already
  protected by a trusted encrypted transport.

Secrets are resolved from the process environment first. An `.env` file is read
only when its path is explicitly configured with `env_file`.

## Mutation semantics

The provider treats the built-in Hermes memory files as the source of mutation
events and HyperspaceDB as a verified mirror:

1. A logical SHA-256 identity includes provider schema, collection, profile
   scope, target, source, and full content.
2. HyperspaceDB still requires a `uint32` point ID. Every candidate is checked
   before use. Foreign ownership causes deterministic probing, never blind
   overwrite.
3. Writes are read back and verified by owner and full digest.
4. `replace` writes and verifies the new record, then deletes and verifies the
   exact old record. Failed deletion becomes `delete_pending`, not success.
5. `remove` resolves `old_text` to exactly one ledger record. Zero or multiple
   matches fail closed.
6. One bounded worker preserves mutation order.

Cross-system atomic transactions are impossible with the current Hermes and
HyperspaceDB contracts. The ledger makes divergence visible and reconcilable;
it does not pretend to provide distributed ACID semantics.

### Failed mutation boundary

The provider does not replay failed `add` or `replace` events from Hermes files.
It records the failure locally and requires an operator to reconcile the primary
Hermes memory state before intentionally reissuing the mutation. The only
automatic reconciliation is bounded `delete_pending` recovery: it runs only
when the remote point has authenticated provider ownership, honors persisted
attempt/backoff limits, and never rebuilds content from a substring match. The
plugin therefore does not claim automatic eventual consistency after a crash.

## Retrieval and trust

Automatic prefetch is dangerous because Hermes currently injects the provider's
returned string as authoritative reference context. This plugin therefore:

- retrieves standard sidecar payloads with `include_payload=True`;
- preserves ID, distance, source, trust, target, and timestamp;
- marks every item as memory data, never instructions;
- quarantines common instruction-injection patterns from automatic prefetch;
- bounds query, count, content, graph, cluster, and output sizes;
- distinguishes `NO_HIT` from timeout, authentication, availability,
  collection, and malformed-response failures.

`owned_only` is the recommended public default. `annotate_all` exists for
mixed-producer migration but expands the trust surface.

## Local ledger confidentiality

The identity ledger is a local SQLite file containing plaintext memory content needed for deterministic replace and delete operations. The provider creates its ledger directory with mode `0700` and its SQLite file with mode `0600`; these POSIX permissions reduce local-account exposure but are not encryption at rest. Deployments requiring encrypted storage must provide host or volume encryption. The plugin does not claim to encrypt the ledger and does not place API keys in it.

## Tools

The plugin exposes exactly eight bounded tools:

- `hyperspace_search`
- `hyperspace_store`
- `hyperspace_status`
- `hyperspace_graph`
- `hyperspace_hierarchy`
- `hyperspace_clusters`
- `hyperspace_search_advanced`
- `hyperspace_admin`

The admin tool is read-only. Collection creation, deletion, rebuild, vacuum, and
snapshot operations are intentionally absent.

## Backup and restore

`hermes backup` receives only the local SQLite identity ledger from
`backup_paths()`. It does not archive an arbitrary server checkout and does not
claim that copying a live database directory is a consistent snapshot.

Back up the HyperspaceDB collection with the database's own verified snapshot or
cold-backup procedure. Restore the database and ledger as one documented
recovery operation, then run reconciliation checks before trusting removals or
replacements.

## Migration from 0.1.x

The previous implementation used a content-derived `uint32` without ownership
verification and did not mirror `remove`. Existing owned legacy records can be
resolved lazily by source, target, exact substring, and content. Ambiguous
legacy matches are rejected. Keep the old database snapshot until migration and
an authorized mutation E2E test are complete.

## Test

Run from this directory with the active Hermes source on `PYTHONPATH`:

```bash
python -m pytest -q
```

The default suite uses a fake client and must not write to production. The
read-only integration suite requires explicit environment variables. Mutation
E2E requires a dedicated test collection and separate operator authorization.

## Honest limitations

- HyperspaceDB's `uint32` ID API cannot make cross-process allocation races
  impossible without a server-side conditional insert.
- Hermes exposes no per-record external-memory trust type; this plugin can gate
  and label context but cannot change the core wrapper contract.
- Distributed atomicity between local Markdown memory and the remote vector
  database does not exist.
- A universal semantic distance cutoff would be dishonest; calibrate
  `max_distance` on the target metric and corpus.
