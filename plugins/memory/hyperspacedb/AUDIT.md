# AUDIT EVIDENCE LEDGER

## Scope

Only `PLUGIN_ROOT` may be modified during this hardening run. Public release is mandatory: no user-specific configuration may remain in shipped files.

## Baseline hashes (2026-08-11)

- `__init__.py` - `1fc5343a4cb8f0cb7f8997325d4e28790d7bd6e1356b86dba27dc27b466b21f1` - 27,682 bytes
- `README.md` - `08780a163d1b6615a492eda083aab68dd73f7de33a50bc75d28f850f68ecaf19` - 2,211 bytes
- `plugin.yaml` - `2bb851df52ceac3f29ff7d992409023d7a0471477b310e7343afbac36af023be` - 196 bytes
- `PLAN.md` initial - `c164b967ae20a2c959e3aac1ce4c0dd35c52b6955646303a1862e54f7babfa90` - 4,219 bytes

## Baseline source defects already confirmed

- P0: `__init__.py` begins with a raw gRPC log line before the module docstring. This is invalid Python syntax.
- P0: `remove` is ignored because `on_memory_write` accepts only `add` and `replace`.
- P0: `replace` inserts a new content-derived ID and never removes the old record.
- P0: uint32 collision is treated as a harmless upsert without ownership verification.
- P1: `_extract_content` ignores standard top-level `payload`.
- P1: `prefetch` creates a local `deadline` variable but never applies a deadline to an RPC.
- P1: network failures collapse to empty memory context.
- P1: tool metadata can override source, timestamp, and content fields.
- P1: a process-global client cache rotates on host only, not API key or user ID.
- P1: `shutdown` does not close client channels.
- P1: `backup_paths` returns a private multi-gigabyte checkout path instead of provider state.
- P1: arbitrary model-supplied collection overrides are accepted by advanced tools.
- P2: meaningful short queries are dropped by the 30-character gate.
- P2: result limits are insufficiently bounded and truncation is silent.
- P2: prompt text, schemas, paths, collection names, and trust claims are private-stack hardcodes, incompatible with public release.

## Evidence rules

Every final finding must be one of: CONFIRMED BY SOURCE, CONFIRMED BY TEST, READ-ONLY INTEGRATION, or UNVERIFIED. Empty SDK results are never proof of success. No production mutation is permitted before a separately approved E2E phase.

## Verification ledger

- Plan: APPROVED.
- Baseline source audit: CONFIRMED BY SOURCE AND RED TESTS.
- Red baseline: 5 failed, 1 passed (`test_baseline_contract.py`).
- Code: PATCHED locally; no-E2E source hardening remains subject to final scoped Git verification.
- Unit tests: TARGETED no-E2E RED/GREEN witnessed for model-authored prefetch, payload tamper, trust relabel, passed Hermes home, advanced collection override, release metadata, and uncalibrated annotate_all prefetch.
- Contract tests: TARGETED no-E2E checkpoints passed; final full suite is still required before a commit.
- Read-only integration: NOT RUN.
- E2E mutations: NOT AUTHORIZED.
- Production verdict: NOT E2E VERIFIED.
