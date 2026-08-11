# HANDOFF - HyperspaceDB Hermes Memory Provider

Status date: 2026-08-11
Prepared for: next executor
Scope token: PLUGIN_ROOT

## 1. Read This First

This handoff is a compact continuation map. `PLAN.md` is the complete execution source of truth and contains the live per-step evidence ledger. Read `PLAN.md` before changing anything.

Current executor state:

- Base tracker: 40/43 completed.
- Blocked base steps: 26, 28, and 43.
- Optional A1-A8: locked.
- Current verdict: NOT PRODUCTION READY.
- Current worktree status at handoff creation: clean for PLUGIN_ROOT.
- No production or shared collection was mutated by this hardening sequence.
- No runtime `state/` artifact was deleted or committed.

The blocker is real, not a planning excuse: strict mutation E2E needs an explicitly authorized isolated backend configuration. Fake-client and static tests cannot establish payload response shape, calibrated Lorentz relevance behavior, or real add/replace/remove behavior.

## 2. Non-Negotiable Scope

Write only under PLUGIN_ROOT. Do not modify:

- Hermes core;
- Hermes config or secret files;
- HyperspaceDB SDK/server source;
- other plugins, staging repositories, or production data;
- a production/shared collection;
- any file outside PLUGIN_ROOT.

Do not delete files, test artifacts, ledgers, collections, or fixtures without a new literal instruction naming the exact target.

Public plugin files must not contain private paths, names, hosts, collection names, profile names, keys, tokens, or stack references. Do not add them to this handoff either.

## 3. Mandatory Tracker Discipline

`PLAN.md` must be updated continuously, not reconstructed at the end.

Before a numbered action:

1. Set its inline checkbox to `[>]`.
2. Set its tracker row to `IN_PROGRESS`.
3. Fill Started UTC, Files/scope, and acceptance test.

After every patch or test:

1. Update UTC, command, exit code, verification level, and evidence/result.
2. Keep the failure history. Never erase red or interrupted attempts.
3. Change to `[x]` only after the stated acceptance gate passed.
4. Use `[!] BLOCKED` for missing authorization/data; do not mark it complete.
5. Keep inline checkboxes and the live table consistent.

At handoff/compaction, update CURRENT EXECUTION STATE before replying.

## 4. What Was Hardened

The provider now has evidence-backed local behavior for:

- explicit collection configuration with no private defaults;
- Lorentz metric and optional exact dimension contract verification;
- read/write refusal when the collection contract is not verified;
- payload-first extraction and bounded structural JSON output;
- authenticated HMAC ownership, key rotation support, and strict ownership checks;
- separated origin, trust, and prefetch eligibility;
- queue-ordered mutation handling;
- persistent mutation states and bounded delete-pending reconciliation;
- SQLite ledger schema migration, permissions, symlink resistance, atomic snapshots;
- client generation and in-flight RPC lifetime safety;
- tool argument allowlisting, output data-boundary labels, redacted errors, and JSON errors;
- release hygiene: `.gitignore`, public scanner, tracked-manifest gate, and neutral docs;
- E2E pre-write gates requiring explicit approval and an isolated target.

Important behavior boundaries:

- Failed `add` and `replace` are not replayed automatically. The README documents this truthfully.
- Automatic relevance has no invented universal distance cutoff. `max_distance` remains deployment-calibrated.
- The local ledger is plaintext SQLite protected by POSIX permissions, not encryption at rest.
- The E2E runner leaves its isolated collection intact; it never deletes a collection.

## 5. Verified Evidence

Latest full local suite, run from PLUGIN_ROOT with the active Hermes source on PYTHONPATH:

```text
85 passed in 3.07s
```

This is fake-client/static/integration evidence, not real-backend E2E evidence.

Recent scoped commits:

```text
56d7531c8 test: isolate strict memory provider e2e state
ebb8f0146 test: harden release and e2e safety gates
fa780ccd1 feat: document and enforce authenticated memory writes
241480033 fix: harden provider tool boundary and error redaction
89d1e1f0a feat: harden provider contracts and release boundaries
ca4237d7d feat: bound pending memory reconciliation retries
bcb05ad92 docs: record hyperspace provider lifecycle evidence
71b9e8fd1 fix: defer hyperspace client rotation during rpc
```

Do not claim "working", "fixed", or "production ready" from these tests alone.

## 6. Known Tooling Quirk

Non-PTY terminal test runs were observed to exit 130 immediately with gRPC poll-list noise. The same test commands passed through a PTY. Use PTY for subsequent Python compilation and pytest evidence until the terminal behavior is independently diagnosed.

Do not copy gRPC diagnostic lines into source files. A prior failed patch operation prepended one such line to provider source; it was removed before the validated test run.

## 7. Remaining Base Gates

### Step 26 - BLOCKED: payload duplication decision

New records store content in several places for compatibility. Do not remove or cap `_content` based on intuition. On an authorized isolated backend, inspect only response shapes and bounded metadata behavior for:

- `get_points`;
- `search(include_payload=True)`;
- backup/reconciliation paths.

Then decide whether payload plus ledger is sufficient. Preserve legacy metadata reading regardless.

### Step 28 - BLOCKED: relevance gate

Do not invent a Lorentz threshold. The isolated E2E must measure relevant positives and unrelated negatives on a declared corpus before enabling a default relevance cutoff. Explicit search can remain labeled with raw distance; automatic prefetch must not receive a guessed policy.

### Step 43 - BLOCKED: strict isolated mutation E2E

The runner is `tests/run_test_collection_e2e.py`.

It requires all of the following at process runtime only:

```text
HSDB_E2E_WRITE_APPROVED=approved
HSDB_TEST_OWNERSHIP_HMAC_KEY=<non-production secret>
HSDB_TEST_SOURCE_COLLECTION=<approved read-only fixture source>
HSDB_TEST_COLLECTION=<dedicated target named hsdb_e2e_...>
HSDB_E2E_STATE_PATH=<temporary external ledger path, not PLUGIN_ROOT/state>
```

Never print these values or write them to any shipped file. Do not re-read private env files without new explicit permission.

The runner has been safely probed twice:

1. With approval absent: exited at the approval gate before client construction.
2. With approval present but test HMAC absent: exited at the HMAC gate before client construction.

No collection operation was reached by either probe.

When the user explicitly provides authorization and isolated values:

1. Update PLAN.md step 43 to `[>]` before any real call.
2. Inspect the source/target read-only first.
3. Verify target metric `lorentz` and dimension `129`.
4. Confirm the target is isolated and suitable for creation/resume.
5. Run the bounded runner only with runtime environment variables.
6. Do not print fixture content.
7. Record only booleans, counts, metric, dimension, synthetic record state, command, exit, and redacted failure class in PLAN.md and AUDIT.md.
8. Resolve steps 26 and 28 from measured evidence.
9. Run the full local suite again.
10. Only then issue the final production verdict.

## 8. Required Final Verdict Rules

Use exactly one evidence-calibrated verdict:

- `production ready` only after strict isolated add -> replace -> remove E2E, no synthetic zombie, payload inspection, relevance evaluation, and all stated release gates pass.
- `not production ready` if any strict E2E prerequisite or measured gate remains absent.

Current correct verdict: `not production ready`.

## 9. Suggested First Commands for a New Session

Run only after reading PLAN.md and confirming scope:

```text
1. Inspect scoped Git status and recent commits.
2. Run the current full local suite through PTY.
3. Read the live CURRENT EXECUTION STATE and tracker rows 26, 28, 43.
4. Do not run E2E without explicit isolated authorization.
```

No optional capability work is allowed until the base verdict is earned.
