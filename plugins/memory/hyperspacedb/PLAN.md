# EXECUTION PLAN AND HANDOFF - HYPERSPACEDB MEMORY PROVIDER

Freeze point: 2026-08-11 04:58:35 CEST
Next executor: GPT-5.6-Terra
Verification vocabulary: PATCHED -> UNIT TESTED -> INTEGRATION TESTED -> E2E TESTED

## 0. NON-NEGOTIABLE SCOPE

Only files under `PLUGIN_ROOT` may be modified.

`PLUGIN_ROOT` means the currently active Hermes memory-provider directory that
contains this PLAN.md. Never encode the operator's absolute home path in a file
that may be published.

Do not modify:

- Hermes core;
- `config.yaml`;
- HyperspaceDB source or SDK;
- any staging/public repository outside `PLUGIN_ROOT`;
- any other plugin;
- the production memory collection;
- any operator-specific secret or environment file.

Reading current Hermes/HyperspaceDB contracts outside `PLUGIN_ROOT` is allowed.
Writing outside `PLUGIN_ROOT` is not.

The operator has an external backup. Do not create another backup. Do not delete
any file, test artifact, database collection, or source fixture without a new
literal instruction naming the exact target.

The plugin is intended for public Internet release. Shipped source, manifest,
tests, and documentation must contain no operator-specific:

- path;
- name or identity;
- collection name;
- host;
- API key or token;
- profile name;
- private stack/repository reference.

Deployment values must come from explicit configuration, environment variables,
or neutral Hermes runtime-derived paths.

## 1. CURRENT TRUTH - WHAT ALREADY HAPPENED

### 1.1 Baseline

- [x] Original provider source was read and compared with current Hermes and
  HyperspaceDB contracts.
- [x] Baseline hashes and initial defect ledger were written to `AUDIT.md`.
- [x] Five increasingly strict audit prompts were written to
  `PROMPT_ITERATIONS.md`.
- [x] Red static contract suite was executed before the rewrite.
- [x] Red result recorded: 5 failed, 1 passed.

Confirmed original P0/P1 defects included:

- `remove` was ignored;
- `replace` inserted the new content-derived ID and left the old record alive;
- a 32-bit hash collision was treated as a harmless upsert;
- top-level SDK `payload` was ignored;
- the apparent RPC deadline was an unused local variable;
- SDK/backend errors collapsed to empty/no-hit behavior;
- model metadata could forge internal fields;
- client rotation ignored credential changes;
- shutdown did not close channels;
- backup included a private multi-gigabyte checkout;
- tool schemas permitted arbitrary collection overrides;
- prompt, schemas, collection, and paths contained private deployment hardcodes.

### 1.2 Current implementation state

`__init__.py` has already been rewritten. It is not merely planned.

Implemented and unit-covered:

- [x] generic public configuration with required explicit collection;
- [x] no private collection/path/name hardcode in provider source;
- [x] generic state path derived from active Hermes home;
- [x] SQLite identity ledger (`IdentityLedger`);
- [x] logical SHA-256 identity includes schema, collection, profile scope,
  target, source, and content;
- [x] deterministic uint32 probing with ownership/digest checks;
- [x] read-after-write owner/digest verification;
- [x] ordered bounded write queue;
- [x] `add` mirroring;
- [x] substring-resolved `replace` in the ledger path;
- [x] substring-resolved `remove` in the ledger path;
- [x] fail-closed zero/multiple old-text matching;
- [x] persistent mutation failure table;
- [x] `delete_pending` status when a replace cannot delete the old record;
- [x] gRPC stub deadline proxy;
- [x] client rotation fingerprint includes host, key, user ID, pool, timeout;
- [x] channel close on shutdown/rotation;
- [x] process environment has precedence over direct config secrets;
- [x] `.env` is read only when an explicit path is configured;
- [x] plaintext non-loopback endpoint rejected by default;
- [x] vectorize + search path requests `include_payload=True`;
- [x] payload-first extraction with metadata fallback;
- [x] provenance fields preserved: ID, distance, source, trust, target, time;
- [x] deduplication and explicit per-record truncation;
- [x] bounded query/content/result/graph/hierarchy/cluster parameters;
- [x] collection override denied by default and absent from model schemas;
- [x] internal metadata fields reserved;
- [x] custom metadata moved under a `user.` namespace;
- [x] prompt-injection quarantine for automatic prefetch;
- [x] prefetch explicitly labels recalled text as data, never instructions;
- [x] dynamic system prompt reports collection, scope, trust mode, and health;
- [x] startup health probe is bounded by the gRPC proxy;
- [x] `sync_turn` remains explicit curated-memory no-op;
- [x] `backup_paths()` returns only the ledger path;
- [x] eight original model-facing tools retained with bounded behavior;
- [x] read-only admin tool remains non-destructive.

### 1.3 Current docs and packaging

- [x] `plugin.yaml` updated to version 0.2.0.
- [x] manifest declares `hyperspacedb>=3.1.3,<4`.
- [x] README rewritten as neutral public documentation.
- [x] README documents configuration, threat model, mutation semantics,
  backup limits, migration, verification levels, and honest limitations.
- [x] README does not claim distributed ACID or a universal distance threshold.
- [x] public hardcode/secret scanner exists in `tests/test_public_release.py`.

### 1.4 Current tests

Created under `tests/`:

- `conftest.py`
- `test_baseline_contract.py`
- `test_mutation_semantics.py`
- `test_retrieval.py`
- `test_security.py`
- `test_lifecycle.py`
- `test_hermes_contract.py`
- `test_public_release.py`
- `run_test_collection_e2e.py`

Executed after the provider/docs rewrite, before the E2E runner was added:

- [x] Python compilation passed.
- [x] Full fake-client/contract/public suite passed: 37 passed in 0.54 s.
- [x] Current Hermes ABC subclass/signature contract passed.
- [x] No production collection was mutated by the 37-test suite.

Use a fresh `--basetemp` under `PLUGIN_ROOT/state/` for every run. Do not use
system `/tmp` and do not reuse/delete an old test directory.

## 2. TEST-COLLECTION E2E STATE - INTERRUPTED, NOT COMPLETE

The operator authorized a dedicated test collection and authorized copying a
bounded fixture sample from an existing legal-case collection into it. The
source collection name must be supplied only at runtime through
`HSDB_TEST_SOURCE_COLLECTION`; do not hardcode it in any public file.

The neutral target used by the interrupted run was:

`hermes_provider_test_20260811`

`tests/run_test_collection_e2e.py` was created. It is designed to:

1. require distinct source and target collection environment variables;
2. create the target as Lorentz 129D only if absent;
3. copy at most 24 textual fixtures;
4. store no fixture content in source code or stdout;
5. verify provider payload search;
6. add a synthetic record;
7. replace it;
8. remove it;
9. verify each transition;
10. leave the test collection in place.

Actual attempts:

- [x] Attempt 1: no API key in process environment; list returned empty after an
  SDK `UNAUTHENTICATED` error. No target write was proven.
- [x] Attempt 2: shell secret source did not expose the expected environment
  variable; same authentication failure. No target write was proven.
- [~] Attempt 3: a local database environment file supplied a 19-character key.
  The command was interrupted with exit 130 before it emitted JSON.
- [ ] Target state after attempt 3 is UNKNOWN. It may not exist, may exist empty,
  or may contain a partial/idempotent fixture copy.
- [ ] Add/replace/remove E2E is NOT verified.
- [ ] Do not delete the target collection. Inspect it read-only first.

First E2E action for Terra:

1. Load the local API key into process environment without printing it and
   without writing its path/value to any shipped file.
2. Read-only list collections and stats.
3. Determine whether the neutral target exists and record only boolean/count/
   metric/dimension, never fixture text.
4. If target exists, confirm metric `lorentz` and dimension `129` before any
   resume.
5. If target does not exist, let the runner create it.
6. Fix the runner's swallowed-SDK-error handling before rerunning it.
7. Rerun the E2E runner idempotently.
8. Record final JSON evidence in `AUDIT.md` without private fixture content.

## 3. CRITICAL DEFECTS STILL TO FIX BEFORE CLAIMING PRODUCTION READY

These are not optional polish. Terra must attack them before E2E.

### Historical-context boundary

This section preserves pre-closure defect analysis and must not be read as the
live status by itself. The current authority is section 8: a numbered tracker
row marked `[x]` records a later source/test closure; a row marked `[!]` remains
blocked. A narrative item here can identify residual real-backend uncertainty
without proving that its earlier fake-client implementation gap remains open.

### P0-A: SDK-swallowed RPC errors are still not fully solved

The current deadline proxy adds a real gRPC timeout, but the HyperspaceDB Python
SDK catches some `grpc.RpcError` exceptions and returns `[]`, `False`, or `None`.
The provider classifies exceptions that escape, but cannot currently distinguish
all swallowed failures from legitimate empty results.

This means the source claims `NO_HIT` vs failure separation more strongly than
is empirically earned.

Required fix:

- add thread-local RPC telemetry to `_DeadlineStubProxy`;
- proxy catches each RPC exception, records exception + monotonically increasing
  sequence for the calling thread, then re-raises so SDK behavior is unchanged;
- `_call()` snapshots telemetry sequence before the high-level SDK call;
- after SDK returns, if telemetry recorded an exception for this call, `_call()`
  raises the classified provider error instead of accepting the SDK fallback;
- successful later calls must not inherit stale telemetry;
- add tests for SDK methods that catch a stub timeout and return `[]`/`False`;
- apply the same check to the E2E fixture runner or use direct stub calls there.

Do not call failure semantics complete until these tests pass.

### P0-B: Legacy delete verification is too permissive

For newly owned points, delete verifies owner + full digest. For an adopted
legacy record, `_delete_verified()` currently permits deletion when
`get_points()` returns a point with no retrievable content.

That is not fail-closed. A foreign point could reuse the ID.

Required fix:

- for legacy adoption, require exact source + target + content + ID evidence;
- store an immutable adoption fingerprint in the ledger;
- immediately before delete, re-resolve the exact remote record by ID;
- if payload/content is unavailable, do not delete;
- if identity is ambiguous or changed, return `MUTATION_CONFLICT`;
- add collision/legacy-race tests.

### P0-C: First-stage legacy resolution ignores target

The vector-search branch of `_resolve_legacy_remote()` filters source and
old_text but does not currently require `item["target"]` to match the requested
Hermes target. The scroll branch does check target aliases.

Required fix:

- apply `_legacy_target_matches(item["target"], target)` in both branches;
- test identical text existing once in `memory` and once in `user`;
- replacement/removal must select only the requested target.

### P0-D: Raw string slicing can create invalid JSON

Several tool methods serialize JSON and then apply:

`serialized[:max_tool_output_chars]`

If the limit is crossed, this returns invalid JSON.

Required fix:

- never slice serialized JSON;
- trim result arrays/content structurally before serialization;
- always return valid JSON with explicit `output_truncated: true`;
- cover search, advanced search, graph, hierarchy, clusters, admin, and status;
- add a property-style test that every tool return parses as JSON at tiny output
  budgets.

### P1-A: `delete_pending` is persisted but never reconciled

Current code records `delete_pending` but has no bounded startup/background retry.

Required fix:

- add bounded reconciliation on initialize or an explicit internal routine;
- retry only records with complete verified ownership evidence;
- exponential backoff + attempt cap;
- persist attempt count and last error;
- never block startup beyond the configured total budget;
- test restart after new-write-success/old-delete-failure.

### P1-B: Mutation failures are a dead-letter ledger, not replay

`mutation_failures` makes failures visible but does not reconstruct missed
built-in writes after process crash.

Required decision and implementation:

- either implement bounded reconciliation against current built-in memory state
  using read-only Hermes APIs/files;
- or explicitly document that the mirror can require operator reconciliation;
- do not advertise complete eventual consistency without one of these.

Any built-in memory read must not modify files outside `PLUGIN_ROOT`.

### P1-C: Public setup/discovery flow is not verified

`collection` is required and `is_available()` returns false when absent. It is
unknown whether the current Hermes setup wizard still discovers an unavailable
provider sufficiently to collect its config.

Required fix/test:

- inspect the current plugin loader/setup code read-only;
- run actual provider discovery from this exact directory;
- test unconfigured -> wizard schema -> configured -> initialized flow;
- do not patch Hermes core;
- if the contract cannot support a required field, use a neutral generic default
  only if documentation and tests prove it is safe; never restore a private
  default.

### P1-D: Metric discovery needs stronger proof

The provider defaults to `lorentz` and tries to read metric from collection
stats. Some SDK/server versions may omit metric in stats.

Required fix:

- when stats lacks metric, inspect `list_collections()` for the configured
  collection;
- verify collection dimension/metric before vectorize/insert;
- fail closed on mismatch;
- never silently switch to cosine/L2;
- add fake-version compatibility tests.

### P1-E: Full content is duplicated in metadata

New writes include payload, document, local ledger content, and `_content`
metadata. This improves compatibility but can inflate memory and metadata size.

Required decision:

- empirically inspect what current `get_points`, `search(include_payload=True)`,
  and backup/reconciliation return;
- if payload + owner/digest + ledger are sufficient, remove full `_content` from
  new metadata or cap it to a documented preview;
- preserve legacy `_content` reading;
- do not change this on intuition alone.

### P1-F: Public release artifact hygiene is incomplete

Test execution created runtime artifacts under `state/`, `__pycache__`, and
possibly `.pytest_cache`. These are inside scope but must not ship.

Required actions:

- add a public package allowlist or `.gitignore` inside `PLUGIN_ROOT`;
- shipped allowlist should normally include source, manifest, README, license,
  audit, prompt iterations, tests, and no runtime SQLite/cache files;
- do not delete existing artifacts without a fresh literal operator instruction;
- test the release manifest rather than assuming ignore files work.

## 3A. REVIEW PASS 1 - CORRECTIONS TO THE FIRST HANDOFF

Verdict after the first adversarial reread: the first handoff was useful but too
optimistic in four places. It focused on the original bugs and missed security
and concurrency defects introduced or left unresolved by the rewrite.

The wording `implemented and unit-covered` in section 1 means PATCHED and tested
against the current fake-client suite only. It does not mean the mechanism is
safe under a malicious shared collection, concurrent client rotation, stalled
shutdown, or live backup.

### P0-E: Ownership metadata is not authenticated

Current checks treat `_hs_owner == hermes-hyperspacedb` plus a matching digest as
proof of ownership. In a shared collection, any writer can forge both strings.
The digest algorithm is public and is not a MAC.

Consequences:

- a foreign point can impersonate an owned point;
- collision probing may accept the foreign point as a deduplicated record;
- pre-delete verification may authorize deletion of attacker-controlled data;
- `owned_only` trust mode does not currently establish ownership.

Required design:

1. Add a dedicated provider signing key supplied through an environment variable
   such as a neutral `HYPERSPACE_PROVIDER_SIGNING_KEY` name.
2. Never derive the signing key from a content digest or public profile scope.
3. Sign canonical fields with HMAC-SHA256: schema, collection, profile scope,
   target, source, full content digest, and external ID.
4. Store the signature in provider metadata.
5. Verify with constant-time comparison before dedupe, replace, delete, or
   authoritative prefetch.
6. Keep legacy unsigned points in an explicit `legacy_unverified` state.
7. Legacy migration requires exact evidence and must never silently upgrade an
   unsigned record to authenticated ownership.
8. If no signing key is configured, provider may run in an explicitly degraded
   compatibility mode, but destructive reconciliation and authoritative
   prefetch must be disabled or require operator opt-in.
9. Add key-rotation semantics. Old signatures need a bounded previous-key
   allowlist or an explicit migration operation; never silently abandon them.

Acceptance tests:

- forged owner + forged digest + wrong HMAC is rejected;
- correct HMAC on a different external ID is rejected;
- correct HMAC from another profile scope is rejected;
- missing key yields explicit DEGRADED state;
- no signing key can never produce an `authenticated` trust label;
- key rotation does not delete records signed only by an unknown key.

### P0-F: Provenance and trust are conflated

Current `owned_only` allows automatic prefetch when any of these is true:

- metadata says the plugin owns the record;
- source appears in `trusted_sources`.

This is wrong for two independent reasons:

1. `hyperspace_store` creates `model-authored` content but gives it provider
   ownership. Provider ownership proves origin, not truth.
2. An external producer can forge a trusted source string.

Required trust model:

- provenance and epistemic trust must be separate fields;
- authenticated provider origin does not imply authoritative content;
- default automatic prefetch may include only authenticated `builtin-curated`
  records whose target/profile policy permits it;
- `hermes-explicit-tool` / `model-authored` records remain available to explicit
  search but are excluded from automatic authoritative prefetch by default;
- source labels from unauthenticated external writers are annotations only;
- operator allowlists must be described as operator assumptions, not
  cryptographic verification;
- unknown and legacy records remain explicit-search data, not automatic
  authoritative context.

Acceptance tests:

- model stores a plausible false fact; explicit search finds it, automatic
  prefetch does not;
- external record forges `source=builtin-curated`; prefetch rejects it;
- authenticated curated record passes;
- changing only `trust` text cannot change trust class;
- quarantine and trust gating are independent controls.

### P0-G: Client close/rotation races with in-flight RPCs

`_call()` obtains a client and invokes it outside `_client_lock`. Another thread
can rotate credentials, close that client, and replace it while the first RPC is
still in flight. Shutdown has the same race.

Worse: shutdown waits only a bounded time, then can close the ledger while the
worker thread is still running. A stalled worker may later write into a closed
SQLite connection.

Required lifecycle design:

- track client generations and in-flight references;
- never close a generation until its in-flight count reaches zero or the process
  enters a documented forced-degraded path;
- worker shutdown state machine: ACCEPTING -> DRAINING -> STOPPING -> STOPPED;
- after DRAINING, reject new events visibly;
- do not close the ledger while worker is alive;
- if shutdown budget expires, preserve ledger/client safety and report
  `SHUTDOWN_INCOMPLETE`; do not pretend completion;
- serialize rotation with generation swap, not with RPC execution itself;
- use barriers in tests to force rotation/shutdown during an active RPC.

Acceptance tests:

- key rotation during blocked search does not close the old channel early;
- shutdown during blocked mutation cannot touch a closed ledger;
- queue order remains deterministic across rotation;
- second shutdown is idempotent;
- no non-daemon resource/thread survives a successful shutdown.

### P0-H: Backup path is smaller but still not a consistent backup

Returning only `ledger.sqlite3` is better than returning a database checkout,
but SQLite runs in WAL mode. Copying only the main file while writes are active
can omit committed WAL data. Therefore the current README/plan still overstates
backup correctness.

Required fix:

- inspect the exact current Hermes `backup_paths()` contract;
- if no pre-backup hook exists, maintain an atomic provider-owned snapshot using
  SQLite's backup API;
- write snapshot to a new in-scope file, fsync, then atomic rename;
- `backup_paths()` should return the verified snapshot artifact, not a live WAL
  database;
- include schema version and snapshot timestamp in the snapshot;
- restore test must open the copied snapshot and verify active records/failures;
- never claim remote HyperspaceDB backup; that remains the database operator's
  separate responsibility.

Acceptance tests:

- commit record while snapshot is being prepared; snapshot is either old-complete
  or new-complete, never corrupt/partial;
- snapshot opens with SQLite integrity check;
- restore preserves delete_pending/failure state;
- missing state produces an explicit empty/new state, not a fake successful
  restore of nonexistent history.

### P1-G: No relevance gate means nearest-neighbor garbage can be injected

No universal distance threshold exists, but leaving `max_distance=None` means a
vector index can always return a nearest record even when the query is unrelated.
The plan correctly rejected a guessed threshold but did not replace it with a
safe default.

Required decision:

- automatic prefetch must be disabled by default unless a calibrated acceptance
  policy is configured; OR
- implement an empirically calibrated collection-specific threshold/null
  distribution with a stored evaluation receipt;
- explicit search may return low-relevance results only with distance and an
  `UNFILTERED` label;
- never use model confidence as the only relevance gate.

Acceptance evaluation:

- relevant positive queries;
- unrelated negative queries;
- short meaningful queries;
- adversarial keyword overlap;
- report precision/false-prefetch rate and calibration corpus scope.

### P1-H: Ledger contains plaintext private memory

The ledger stores full content, failed content, and old_text in plaintext. This
was not disclosed strongly enough.

Required fix/decision:

- create state directory with mode 0700 and ledger/snapshot with mode 0600;
- reject unsafe symlink targets and unexpected ownership/permissions;
- minimize duplicated content and failure payloads;
- document exactly what plaintext remains;
- consider keyed content encryption only if it can be implemented and tested
  without inventing key management;
- never market local SQLite as encrypted when it is not;
- add permission and symlink tests.

### P1-I: All tool surfaces carry untrusted data, not only search

Graph/hierarchy responses can contain metadata supplied by other producers.
Returning raw nested structures without a data-boundary wrapper creates another
prompt-injection route.

Required fix:

- apply a shared recursive sanitizer to graph, hierarchy, cluster, and advanced
  result structures;
- cap nesting depth, list length, keys, string length, and total output;
- label all record-derived values as untrusted data;
- status/admin may expose only structural server fields from an allowlist;
- malformed/recursive objects must not crash serialization.

### P1-J: Unexpected exceptions may escape tool handlers

Individual handlers mostly catch `ProviderError`. Programming errors,
serialization errors, or unexpected SDK result shapes can escape the tool
contract.

Required fix:

- dispatcher catches unexpected exceptions at the final boundary;
- log a correlation ID and redacted exception internally;
- return stable `INTERNAL_ERROR` JSON without secrets, paths, or stack traces;
- never convert a programming error to `NO_HIT`;
- tests verify every tool always returns parseable JSON.

### P2-A: Failure counters can double-count

`status_snapshot()` adds the in-memory failed count and the ledger failure count,
although the worker increments both for one failure. Decide whether the metric
means events, durable failures, or current unresolved failures, and test it.

### P2-B: Prompt-injection regex is heuristic only

The current quarantine patterns catch obvious text but are bypassable and can
false-positive on security research. Documentation and system prompt must call
this heuristic screening, not a complete injection defense. Trust gating,
provenance authentication, and core instruction/data separation remain primary.

## 4. ADVERSARIAL TESTS TERRA MUST ADD

- [ ] SDK stub raises deadline, high-level method swallows and returns `[]`;
  provider must return `BACKEND_TIMEOUT`, not `NO_HIT`.
- [ ] SDK stub raises unauthenticated, high-level list/search returns fallback;
  provider must return `AUTH_ERROR`.
- [ ] identical content in user and agent targets resolves independently.
- [ ] identical `old_text` in two records of one target fails closed.
- [ ] legacy record ID is replaced by foreign record between resolve and delete;
  delete must be refused.
- [ ] insert succeeds, delete fails, process restarts, reconciliation removes only
  the verified old owned record.
- [ ] queue fills; failure remains visible and later writes are not reordered.
- [ ] client credential rotates while worker is active.
- [ ] shutdown during queued write remains bounded and ledger stays readable.
- [ ] every tool output remains valid JSON under very small output budgets.
- [ ] payload-only, metadata-only, bytes, malformed payload, and missing content.
- [ ] large metadata key/value, control characters, nested objects, reserved-key
  variants, and Unicode normalization.
- [ ] remote plaintext endpoint rejected; loopback and explicitly allowed remote
  transport paths tested.
- [ ] collection override absent from schemas and rejected at runtime.
- [ ] no destructive admin operation can be reached by malformed operation name.
- [ ] no public text file contains private paths/names/collections/credentials.
- [ ] clean-room import with all private environment variables absent.
- [ ] actual Hermes loader discovers exactly one provider and eight unique tools.
- [ ] backup contract accepts a missing/new ledger and restores a closed ledger.
- [ ] test collection fixture search returns sidecar payload through the provider.
- [ ] full test-collection add -> replace -> remove leaves no synthetic zombie.

## 4A. REVIEW PASS 2 - EXECUTABILITY AND HANDOFF CORRECTIONS

Second-review verdict before these corrections: technically stronger than pass 1,
but still not executable enough. The architecture findings were present, while
the old execution order did not include the four new P0 gates. It also lacked a
formal evidence ledger, strict-mode production gate, migration matrix, and exact
portable commands. A future executor could have followed the old numbered list
and reached E2E without authenticating ownership or fixing backup/lifecycle.

This pass corrects those defects.

### 4A.1 Production mode vs compatibility mode

The implementation must expose two honest states:

- `strict`: signing key configured, ownership signatures verified, automatic
  prefetch limited to authenticated curated records, destructive reconciliation
  enabled only for authenticated records;
- `compatibility_degraded`: no signing key or legacy unsigned records; explicit
  search is allowed, but records are unverified, destructive reconciliation is
  disabled, and automatic prefetch is disabled by default.

Production-ready verdict requires successful E2E in `strict` mode. Passing only
compatibility mode is not enough.

HMAC contract must be versioned and deterministic:

- canonical UTF-8 JSON with sorted keys and fixed separators;
- schema name and signature version included;
- content represented by full SHA-256 digest, not a truncated preview;
- key identifier may be stored, never the key;
- signature compared with `hmac.compare_digest`;
- candidate uint32 ID should be derived from keyed HMAC in strict mode to reduce
  targeted collision/race attacks;
- probing remains required because uint32 collisions still exist.

### 4A.2 Required state-machine contract

For each logical record:

`ABSENT -> INSERTING -> ACTIVE -> REPLACING -> DELETE_PENDING -> ABSENT`

Allowed exceptional states:

- `CONFLICT`: ambiguous old_text, ownership mismatch, collision exhaustion;
- `RETRY_PENDING`: transient RPC outcome is unknown;
- `DEAD_LETTER`: attempt cap reached;
- `LEGACY_UNVERIFIED`: externally discovered unsigned record;
- `QUARANTINED`: content is not eligible for automatic prefetch.

Every transition must be a SQLite transaction with attempt count, last error
class, and timestamp. A process restart must resume only transitions whose remote
identity can be authenticated. Never replay a destructive transition from
content resemblance alone.

Unknown RPC outcome contract:

- after insert timeout, read back the exact signed candidate before retry;
- after delete timeout, read back the exact ID/signature before retry;
- do not allocate a second replacement merely because the first response was
  lost;
- `ERROR` must never become `NO_HIT`.

### 4A.3 Schema and migration contract

Use `PRAGMA user_version` and explicit monotonic migrations. At minimum persist:

- logical digest;
- external ID;
- collection/profile/target/source;
- content digest;
- signature version and key ID;
- state;
- attempt count;
- last error class/message (redacted and bounded);
- created/updated timestamps.

Decide empirically whether full content must remain. If retained, document the
plaintext risk and enforce permissions. Migration must be transactional and
backed by an integrity-checked snapshot. If migration fails, leave the previous
file usable and return `MIGRATION_FAILED`.

Compatibility matrix to test:

- fresh empty state;
- current pre-versioned ledger;
- signed current record;
- unsigned legacy remote record;
- current code with absent state file;
- corrupt/truncated SQLite file;
- unknown future `user_version` (fail closed; never downgrade).

### 4A.4 Actual Hermes path test

A provider-helper test is not enough. Add a contract test that exercises:

`MemoryTool/MemoryManager mutation -> on_memory_write -> queue -> fake HSDB`

Verify all three built-in actions with real current argument order:

- add content;
- replace content using an old_text fragment;
- remove using an old_text fragment.

The test must import the current Hermes classes read-only from the adjacent core.
If core behavior differs from the assumed hook contract, stop and mark BLOCKED;
do not patch core within this task.

### 4A.5 Mandatory live progress tracking in this PLAN.md

This PLAN.md is the execution source of truth, not a static handoff. Terra must
update it continuously while working. Do not reconstruct progress from memory at
the end of a session.

For every mandatory step 1-43 and optional step A1-A8:

1. BEFORE starting work, change the inline checkbox from `[ ]` to `[>]`, set the
   tracker row to `IN_PROGRESS`, and fill `Started UTC`, `Files/scope`, and the
   intended acceptance test.
2. AFTER every material patch or test, update `Updated UTC`, verification level,
   command, exit code, and evidence/result immediately.
3. Change `[>]` to `[x]` only after the step's acceptance criteria have passed
   and evidence is recorded.
4. On a blocker, change `[>]` to `[!]`, set `BLOCKED`, describe the exact blocker
   and next required decision. Do not mark blocked work as done.
5. If a step is deliberately excluded, use `[-] SKIPPED` only with an explicit
   operator decision and reason. Silence is not authorization to skip.
6. Keep failed attempts in the evidence/result field. Never erase a red test or
   failed E2E merely because a later retry passes.
7. Update both copies atomically: the inline checkbox in section 5/5A and the
   corresponding row in section 8. They must never disagree.
8. At most one mandatory step should be `[>] IN_PROGRESS` unless the plan records
   why independent steps are deliberately parallel.
9. Before context compression, session switch, or handoff, update `CURRENT
   EXECUTION STATE` in section 8. The next model must be able to resume by reading
   PLAN.md alone.

Checkbox meanings:

- `[ ]` - TODO, not started;
- `[>]` - IN_PROGRESS or PATCHED but not fully accepted;
- `[x]` - DONE with earned evidence;
- `[!]` - BLOCKED or FAILED;
- `[-]` - SKIPPED by explicit decision.

Progress statuses:

- `TODO`
- `IN_PROGRESS`
- `DONE`
- `BLOCKED`
- `SKIPPED`

Verification levels are separate from progress status:

- `UNVERIFIED`
- `STATIC_CHECKED`
- `PATCHED`
- `UNIT_TESTED`
- `CONTRACT_TESTED`
- `READ_ONLY_INTEGRATION_TESTED`
- `E2E_WRITE_TESTED`
- `USER_VERIFIED`

A passing static/compile check cannot be recorded as UNIT_TESTED. `PATCHED` is
not `DONE` when the step requires a test. An E2E test must name the isolated
target and verify final remote state without printing fixture content.

Required fields for every tracker row:

- checkbox;
- progress status;
- verification level;
- started/updated/completed UTC timestamps;
- files/scope touched;
- exact command or observation;
- exit code;
- evidence/result;
- blocker or next action.

### 4A.6 Stop conditions

Stop and mark BLOCKED instead of escaping scope when:

- a required behavior needs Hermes core or SDK modification;
- strict mode cannot be implemented without storing a secret in a shipped file;
- the configured collection is not Lorentz 129D;
- only a production collection is available for writes;
- the test collection identity/ownership is ambiguous;
- the interrupted target contains unexpected foreign data;
- real backend errors cannot be separated from no-hit;
- backup cannot produce an integrity-checked atomic snapshot under the current
  provider contract;
- a migration would require deleting or rewriting unknown state without explicit
  authorization.

### 4A.7 Release definition of done

All must be true:

- [ ] all P0-A through P0-H closed with red-then-green tests;
- [ ] all P1 decisions resolved or explicitly documented as non-production
  limitations accepted by the operator;
- [ ] current Hermes mutation path contract tested;
- [ ] loader/setup discovery tested;
- [ ] strict-mode signing/trust E2E tested;
- [ ] isolated collection add/replace/remove E2E tested;
- [ ] unrelated query false-prefetch evaluation passed against declared corpus;
- [ ] SQLite migration, permission, integrity, snapshot, and restore tested;
- [ ] full tool-output JSON/property suite passed;
- [ ] public release allowlist contains no runtime state/cache/private values;
- [ ] README matches actual behavior and does not claim more;
- [ ] final `AUDIT.md` lists residual uncertainty;
- [ ] final verdict is exactly `production ready` or `not production ready`,
  supported by the earned verification levels.

### 4A.8 Evaluation scores

Rubric: contract accuracy 25%, security/trust 25%, failure/lifecycle 20%, test
executability 20%, public-release hygiene 10%.

- Initial handoff before pass 1: 6.2/10. Strong original-bug inventory, but missed
  forged ownership, trust conflation, lifecycle races, and WAL backup consistency.
- After pass 1 but before pass 2: 8.1/10. Architecture risks were substantially
  complete, but execution order and acceptance accounting still lagged findings.
- After pass 2 corrections: 9.2/10 as an execution plan. Remaining uncertainty is
  deliberately transferred as empirical tasks, not hidden as assumptions. This
  score evaluates PLAN completeness, not provider readiness.

## 5. EXECUTION ORDER FOR GPT-5.6-TERRA

Do not reorder P0 gates for convenience. Update section 8 after every step.

### Phase A - Freeze and reproduce

1. [x] Read this PLAN.md, `AUDIT.md`, current source, tests, README, and manifest.
2. [x] Confirm only `PLUGIN_ROOT` will be written and no background E2E process
   remains.
3. [x] Inventory in-scope files and runtime artifacts without deleting them.
4. [x] Compile current Python source.
5. [x] Run the existing suite with a new in-scope basetemp; record the actual
   count rather than assuming 37 still pass after the E2E runner addition.
6. [x] Reproduced every listed P0 with a focused failing test.

### Phase B - Failure semantics and serialization

7. [x] Implemented thread-local swallowed-RPC telemetry (P0-A).
8. [ ] Make auth, timeout, unavailable, malformed response, and true no-hit
   tests green without state collapse.
9. [ ] Replace raw serialized-output slicing with structural truncation (P0-D).
10. [ ] Prove every tool output remains valid JSON under bounded/fuzzed inputs.
11. [ ] Add final dispatcher INTERNAL_ERROR boundary and recursive untrusted-data
    sanitizer for all record-derived surfaces.

### Phase C - Authenticated identity and trust

12. [ ] Implement versioned HMAC ownership and strict/degraded modes (P0-E).
13. [ ] Derive strict-mode candidate IDs from keyed material while retaining
    collision probing.
14. [ ] Separate provenance, ownership, trust, quarantine, and relevance (P0-F).
15. [ ] Make automatic prefetch reject model-authored, forged-source, legacy
    unsigned, and unrelated records by default.
16. [ ] Implement signing-key rotation contract and tests.
17. [ ] Harden legacy target resolution and pre-delete verification (P0-B/C).

### Phase D - Durable state and lifecycle

18. [ ] Add versioned transactional SQLite migrations and corruption/future-version
    fail-closed tests.
19. [ ] Enforce 0700 state directory, 0600 state/snapshot files, and safe symlink/
    ownership handling.
20. [ ] Implement explicit mutation state machine and unknown-outcome recovery.
21. [ ] Implement bounded authenticated delete_pending reconciliation.
22. [ ] Implement client-generation in-flight tracking and safe rotation/shutdown
    (P0-G).
23. [ ] Implement atomic integrity-checked SQLite snapshot backup/restore (P0-H).
24. [ ] Resolve full-content metadata/ledger duplication using read-only SDK
    evidence, then update docs/tests.

### Phase E - Current contracts

25. [ ] Test `MemoryTool/MemoryManager -> provider -> fake HSDB` add/replace/remove.
26. [ ] Test real plugin loader discovery, setup schema, save/reload, and exact
    eight-tool uniqueness without modifying Hermes core/config.
27. [ ] Verify actual installed SDK/server method shapes and collection metadata;
    implement Lorentz 129D fail-closed metric checking.
28. [ ] Run clean-room import with all private environment variables absent.

### Phase F - Isolated real backend

29. [ ] Load credentials only into process environment and inspect the interrupted
    neutral target read-only.
30. [ ] Confirm target metric/dimension and record only redacted count/state.
31. [ ] Fix E2E runner failure telemetry and strict-mode signing configuration.
32. [ ] Resume bounded idempotent fixture copy without logging fixture content.
33. [ ] Run payload retrieval read-only integration.
34. [ ] Run strict-mode synthetic add -> duplicate add -> replace -> remove.
35. [ ] Verify no synthetic zombie remains and no source collection was mutated.
36. [ ] Run timeout/unknown-outcome recovery on the isolated target if safely
    injectable; otherwise mark the exact unavailable live test.

### Phase G - Adversarial and release gates

37. [ ] Run the complete section 4 matrix plus short-query/relevance evaluation.
38. [ ] Run full unit/contract/read-only/E2E suite again after all fixes.
39. [ ] Run public hardcode, secret, absolute-path, cache/state, and package-allowlist
    scans over every shipped file, including the E2E runner.
40. [ ] Add release allowlist/ignore/license/changelog artifacts if required,
    without deleting current files.
41. [ ] Verify README/manifest/AUDIT claims against actual test evidence.
42. [ ] Update every checkbox and evidence row.
43. [ ] Emit final P0-P3 audit, residual uncertainty, earned verification levels,
    and exact production verdict.

## 5A. OPTIONAL CAPABILITY EXPANSION - ONLY AFTER THE BASE IS COMPLETE

This phase is explicitly SECONDARY. Do not start it while any P0-A through P0-H,
base Definition of Done item, isolated strict-mode E2E, loader contract, backup/
restore test, or public-release gate remains open.

The base provider must first earn:

- all mandatory tests green;
- current Hermes mutation and loader contracts verified;
- strict authenticated ownership enabled;
- automatic prefetch trust/relevance gates verified;
- isolated add/replace/remove E2E passed;
- atomic ledger snapshot/restore passed;
- final base verdict recorded.

Only then implement the following as a separate optional phase. Failure of an
optional capability must not destabilize the already-verified base.

### Design rule: operations before tool-schema proliferation

Hermes does not impose an eight-tool provider limit, but every separate tool
schema consumes model context on every turn. Prefer adding bounded operation
enums to an existing semantically correct tool when this stays clear and safe.
Do not create one schema per SDK method.

Target shape: approximately 15 useful operations exposed through no more than
10 model-facing schemas.

### OPTIONAL-A: `hyperspace_audit` - recommended first

Add one read-only diagnostic tool for provider-owned state:

- active logical records count;
- records by state (`ACTIVE`, `DELETE_PENDING`, `RETRY_PENDING`,
  `DEAD_LETTER`, `LEGACY_UNVERIFIED`, `QUARANTINED`);
- signature verification summary;
- reconciliation backlog and bounded oldest age;
- redacted recent error classes;
- ledger schema version and last snapshot integrity result.

Security constraints:

- never return memory content, old_text, secret material, signatures, private
  paths, raw exceptions, or unbounded IDs;
- return aggregate counts by default;
- any bounded record detail requires authenticated ownership and current
  profile/collection scope;
- always return structurally truncated valid JSON.

Acceptance tests:

- mixed-state ledger produces correct aggregate counts;
- foreign/forged records do not appear as authenticated;
- no content/secret/path survives output;
- corrupt state returns explicit `AUDIT_UNAVAILABLE`, not fake zeros.

### OPTIONAL-B: extend `hyperspace_graph` with bounded `points`

STATUS: COMPLETED (local commit `87d3eec2a`, integration-tested only). The current server/SDK protobuf contract stores and
retrieves backend point slots as `uint32`; this is not a durable logical identity.
The plugin's logical identity is the full SHA-256 digest plus HMAC and profile
scope, with `uint32` collision probing only as a backend allocation adapter.

Do not expose raw `uint32` backend slots as a model-facing lookup surface. A
bounded list does not solve repeated enumeration, and raw IDs are not safe
cross-session identity handles. Per the local-plugin-only continuation directive,
A3 uses opaque, short-lived, profile/session/collection-scoped capability handles
minted only from prior sanitized search/store results. The handles live only in the
provider RAM map, are bounded, are cleared at initialization, and never enter an
SDK request except after local resolution to the private backend slot.

Do not expose an unrestricted full-collection dump. If a bounded `scroll` is later
considered, require opaque cursor capabilities, ownership/profile filters, hard
page and total budgets, and no automatic fallback that walks the collection.

### OPTIONAL-C: extend `hyperspace_admin`

Add only read-only operations:

- `count` - current scoped collection, bounded filters;
- `digest` - collection integrity/sync digest with an allowlisted output shape;
- `cache_stats` - structural cache counters only.

Do not add to model-facing admin:

- create/delete collection;
- rebuild index;
- vacuum;
- trigger snapshot;
- freeze/unfreeze;
- reconsolidation;
- cache mutation/configuration;
- arbitrary payload updates.

Server output must be allowlisted field-by-field. Do not pass raw server maps to
the model.

### OPTIONAL-D: add one multiplexed `hyperspace_geometry` tool

Allowed read-only operations:

- `trust_score` for a bounded ordered trajectory ID list;
- `predict_relation` for exactly two IDs;
- `predict_momentum` for a bounded trajectory and bounded numeric step value.

Requirements:

- Lorentz 129D collection verification remains mandatory;
- hard ID/count/depth/numeric limits;
- distinguish mathematical server output from factual/epistemic truth;
- label outputs as geometric diagnostics, never as proof that a memory is true;
- test malformed vectors, missing IDs, empty trajectories, non-finite values,
  timeout, and swallowed SDK errors.

### OPTIONAL-E: event observation - defer unless there is a real use case

`subscribe_to_events()` is streaming and must not be wrapped as a naive blocking
tool call. If implemented, it requires:

- one lifecycle-managed background subscriber;
- reconnect/backoff and authentication rotation;
- bounded ring buffer;
- event type/collection/profile filtering;
- sequence/cursor handling and deduplication;
- explicit overflow/drop counters;
- bounded polling tool that returns recent sanitized events;
- shutdown tests proving no surviving subscriber thread/channel.

This is medium/high complexity. Do not implement it merely because the SDK has
the method.

### OPTIONAL-F: reconciliation control - operator-only

A mutation-capable reconciliation action is high risk. If added:

- hide it by default from model tool schemas;
- require explicit operator enablement;
- operate only on authenticated provider-owned records;
- support dry-run before apply;
- require bounded batch size and idempotency token;
- persist an auditable receipt per transition;
- never adopt/delete legacy unsigned records automatically;
- return partial-success state precisely.

Do not expose raw `delete`, `update_payload`, or collection mutation as shortcuts
around the identity ledger.

### OPTIONAL-G: batch mutation - last priority

Batch store/replace/remove is not a thin wrapper around SDK `batch_insert`.
Before exposing it, implement:

- per-item logical identity and collision probing;
- per-item HMAC ownership;
- deterministic ordering;
- partial-success ledger;
- retry/unknown-outcome recovery;
- bounded batch size/content/output;
- replace/remove reconciliation;
- E2E restart tests.

No batch operation may bypass the single-record invariants proven in the base.

### Optional-phase execution order

A1. [x] Freeze the verified base test result and record its evidence hash.
A2. [x] Implement and test `hyperspace_audit`.
A3. [ ] Add bounded `points` to `hyperspace_graph`.
A4. [ ] Add read-only `count`, `digest`, and `cache_stats` to admin.
A5. [ ] Add multiplexed read-only geometry only if required by users.
A6. [ ] Re-run the complete base suite after every optional capability.
A7. [ ] Re-run schema count/context-size and public-release scans.
A8. [ ] Treat events, reconciliation control, and batch mutation as independent
    future milestones, each requiring its own threat model and E2E gate.

Optional work cannot retroactively upgrade a base verification level. Report it
separately, for example:

- `BASE: E2E_WRITE_TESTED`
- `OPTIONAL_AUDIT: CONTRACT_TESTED`
- `OPTIONAL_EVENTS: NOT_IMPLEMENTED`

## 6. COMMAND DISCIPLINE

All commands must run with working directory `PLUGIN_ROOT`.

Use the active Hermes Python environment and expose Hermes source through
`PYTHONPATH`. Use a fresh basetemp under `PLUGIN_ROOT/state/` for each run.
Never use `/tmp` for durable or test artifacts.

For the E2E runner, pass collection names and credentials only through process
environment. Never write the operator-approved source collection name, secret
file path, key, or user identity into public source/docs/tests.

Do not print fixture content. Final E2E output may contain only booleans, counts,
metric, dimension, synthetic IDs/digests, and timing.

## 7. CURRENT VERIFICATION LEVEL

- Source: PATCHED.
- Python syntax: UNIT-LEVEL COMPILE PASS.
- Fake backend and Hermes ABC contract: UNIT TESTED, 37/37 PASS.
- Public scan: PASSED before the E2E runner was added; MUST BE RERUN.
- Actual Hermes plugin loader: NOT TESTED.
- Real backend read-only integration: NOT COMPLETED.
- Dedicated test collection: INTERRUPTED / STATE UNKNOWN.
- Real add/replace/remove: NOT E2E TESTED.
- Production ready: NO.

Brutal current verdict: the rewrite is materially better than the original and
has a real test foundation, but it still has eight P0-class proof gaps: swallowed
SDK errors, permissive legacy delete verification, missing target filtering in
one legacy path, invalid JSON truncation, unauthenticated ownership metadata,
provenance/trust conflation, in-flight client lifecycle races, and inconsistent
WAL backup semantics. No competent reviewer should call it production ready
until Terra closes those gaps and the dedicated collection E2E passes.

## 8. LIVE EXECUTION TRACKER AND EVIDENCE LEDGER

This section must be updated live. A final bulk update is forbidden.

### L6 remediation scope - approved 2026-08-11T09:56:03+02:00

Goal: make the E2E runner reject an empty, relative, or PLUGIN_ROOT-contained
`HSDB_E2E_STATE_PATH` before client construction, collection access, or mutation.

Allowed file changes, and no others:

1. `tests/run_test_collection_e2e.py`: add a pure runtime state-path validator
   and call it immediately after reading the environment value.
2. `tests/test_public_release.py`: add deterministic source/behavior tests for
   empty, relative, in-root, and external absolute state paths. Tests must not
   construct a client or contact a backend.
3. `PLAN.md`: live tracker, commands, exit codes, evidence, and append-only log.

Non-goals: no `__init__.py`, README, manifest, configuration, SDK/server,
credentials, collection, fixture, runtime-state cleanup, real E2E, A1-A8, or
other test/source file change.

Acceptance: all invalid paths fail before client construction; an external
absolute path is accepted by the pure guard; changed targeted test and fresh
full local PTY suite pass. This earns UNIT/INTEGRATION evidence only, never E2E.

### CURRENT EXECUTION STATE

- Current phase: `OPTIONAL-C READ-ONLY ADMIN ALLOWLIST`
- Active step: `A4 [>]`
- Base progress: `40/43 historical tracked steps completed; strict E2E gates 26, 28, and 43 remain blocked`
- Optional progress: `A1 [x] baseline; A2 [x] committed ca7a62de3; A3 [x] committed 87d3eec2a; A4 [>] commit gate passed source/test audit`
- Last PLAN.md update UTC: `2026-08-13T11:24:00+02:00`
- Last verified test level: `A4 complete fake-client suite GREEN: 110 passed in 14.36s with E2E runner explicitly ignored; admin AST allowlist, diff whitespace, forbidden-call scan, and staged scope pass`
- Current blocker: `No implementation, audit, or staging blocker. Six reviewed A4 files are staged under the plugin only; base E2E gates 26, 28, and 43 stay blocked.`
- Immediate next action: `Create one local A4 commit without bypass flags; verify commit manifest and post-commit scope before starting OPTIONAL-D.`

When work begins, replace these values immediately. Never leave `Active step:
NONE` while any row is `[>]`.

### ACTIVE STEP DETAIL

- Step ID: `A4 [>]`
- Goal: `Add only bounded read-only `count`, `digest`, and `cache_stats` operations to hyperspace_admin through field allowlists.`
- Why now / dependency satisfied: `A3 capability migration is locally committed and verified; source inventory confirms current SDK exposes these read-only calls.`
- Progress status: `RED_READY`
- Verification level: `STATIC_CHECKED`
- Started UTC: `2026-08-13T11:04:13+02:00`
- Last updated UTC: `2026-08-13T11:04:13+02:00`
- Files/scope: `PLUGIN_ROOT/__init__.py, tests/test_optional_admin.py, tests/conftest.py if fake read-only methods are required, README.md, PLAN.md only; no core, SDK, server, config, secrets, collection, standalone/public repository, remote, or E2E action.`
- Intended acceptance test: `Fake-client RED/GREEN proves operations are read-only, output is allowlisted, malformed/unexpected maps fail closed, and no destructive admin operation is registered; full suite excludes E2E.`
- Latest command/observation: `Read-only SDK inventory found count(), get_digest(), and get_cache_stats(); cache stats use a GET endpoint but raw shape is untrusted.`
- Exit code: `0`
- Evidence/result: `No source changed for A4 yet. No actual SDK/server call was made.`
- Blocker: `Need test-defined allowlist before adding model-facing admin operations.`
- Next action: `Write A4 contract tests, run expected RED, then minimal local handler/schema/fake-client changes.`

Replace this block whenever the active step changes. Do not append secrets,
fixture content, private collection names, or private absolute paths.

### PER-STEP TRACKER

| Step | Check | Progress | Verification | Started UTC | Updated UTC | Completed UTC | Files/scope | Command/test | Exit | Evidence/result | Blocker/next |
|---:|:---:|---|---|---|---|---|---|---|---:|---|---|
| 1 | [x] | DONE | STATIC_CHECKED | 2026-08-11T05:00:00+02:00 | 2026-08-11T05:22:04+02:00 | 2026-08-11T05:22:04+02:00 | PLAN.md, AUDIT.md, README.md, plugin.yaml, __init__.py, tests | Read all named artifacts; AST inventory | 0 | 5 root artifacts plus 9 test files read; provider has 48 methods | Step 2 |
| 2 | [x] | DONE | STATIC_CHECKED | 2026-08-11T05:22:04+02:00 | 2026-08-11T05:22:42+02:00 | 2026-08-11T05:22:42+02:00 | PLAN.md only; read-only process/scope inspection | Process inventory | 0 | Zero matching E2E processes; write scope remains PLUGIN_ROOT only | Step 3 |
| 3 | [x] | DONE | STATIC_CHECKED | 2026-08-11T05:22:42+02:00 | 2026-08-11T05:23:19+02:00 | 2026-08-11T05:23:19+02:00 | PLUGIN_ROOT; read-only file inventory | Recursive artifact inventory | 0 | 117 files, 2.95 MB; 88 SQLite test artifacts plus caches; none deleted | Step 4 |
| 4 | [x] | DONE | STATIC_CHECKED | 2026-08-11T05:23:19+02:00 | 2026-08-11T05:23:48+02:00 | 2026-08-11T05:23:48+02:00 | __init__.py; compile check only | python -m py_compile __init__.py | 0 | Syntax compile passed | Step 5 |
| 5 | [x] | DONE | UNIT_TESTED | 2026-08-11T05:23:48+02:00 | 2026-08-11T05:24:25+02:00 | 2026-08-11T05:24:25+02:00 | tests and temporary state under PLUGIN_ROOT | pytest -q with unique basetemp | 0 | 37 passed in 0.86s | Step 6 |
| 6 | [x] | COMPLETED | UNIT_TESTED | 2026-08-11T05:24:25+02:00 | 2026-08-11T05:30:22+02:00 | tests/test_p0_red_regressions.py | Eight focused P0 red tests | pytest exit 1 | 8/8 expected failures: A swallowed timeout; B target; C delete; D JSON; E forgery; F trust; G shutdown; H snapshot | - | Start P0-A |
| 7 | [x] | COMPLETED | UNIT_TESTED | 2026-08-11T05:30:22+02:00 | 2026-08-11T05:37:24+02:00 | __init__.py; tests/test_p0_red_regressions.py | P0-A swallowed timeout | py_compile + pytest P0-A exit 0 | 1 passed: proxy records swallowed RPC TimeoutError and _call raises BackendTimeout | - | Start P0-B |
| 8 | [x] | COMPLETE | UNIT_TESTED | 2026-08-11T05:37:24+02:00 | 2026-08-11T05:41:29+02:00 | __init__.py; tests/test_p0_red_regressions.py | P0-B target-aware legacy identity | py_compile plus isolated P0-B pytest | exit 0; 1 passed | - | Step 9 |
| 9 | [x] | COMPLETE | UNIT_TESTED | 2026-08-11T05:41:29+02:00 | 2026-08-11T05:42:57+02:00 | __init__.py; tests/test_p0_red_regressions.py | P0-C fail-closed legacy delete | py_compile plus isolated P0-C pytest | exit 0; 1 passed | - | Step 10 |
| 10 | [x] | COMPLETE | UNIT_TESTED | 2026-08-11T05:42:57+02:00 | 2026-08-11T05:46:13+02:00 | __init__.py; tests/test_p0_red_regressions.py | P0-D structural tool JSON truncation | py_compile plus isolated P0-D pytest | exit 0; 1 passed | - | Step 11 |
| 11 | [x] | COMPLETE | UNIT_TESTED | 2026-08-11T05:46:13+02:00 | 2026-08-11T05:48:54+02:00 | __init__.py; tests/conftest.py; tests/test_p0_red_regressions.py | P0-E HMAC ownership authentication | py_compile plus isolated P0-E pytest | exit 0; 1 passed | - | Step 12 |
| 12 | [x] | COMPLETE | UNIT_TESTED | 2026-08-11T05:48:54+02:00 | 2026-08-11T05:49:58+02:00 | __init__.py; tests/test_p0_red_regressions.py | P0-F provenance and trust boundary | py_compile plus isolated P0-F pytest | exit 0; 1 passed | - | Step 13 |
| 13 | [x] | COMPLETE | UNIT_TESTED | 2026-08-11T05:49:58+02:00 | 2026-08-11T05:52:09+02:00 | __init__.py; tests/test_p0_red_regressions.py | P0-G lifecycle and P0-H snapshot backup | py_compile plus P0-G, P0-H, then full P0 pytest | exit 0; 8 passed | - | Step 14 |
| 14 | [x] | COMPLETE | UNIT_TESTED | 2026-08-11T05:52:09+02:00 | 2026-08-11T05:53:17+02:00 | __init__.py; tests/test_lifecycle.py | Full local regression repair | complete local pytest suite | exit 0; 45 passed | - | Step 15 |
| 15 | [x] | COMPLETE | UNIT_TESTED | 2026-08-11T05:53:17+02:00 | 2026-08-11T05:55:10+02:00 | __init__.py; tests/test_p0_red_regressions.py | Strict prefetch rejects spoofed and legacy claims | isolated P0-F spoofed-source pytest | exit 0; 1 passed | - | Step 16 |
| 16 | [x] | COMPLETE | UNIT_TESTED | 2026-08-11T05:55:10+02:00 | 2026-08-11T05:56:45+02:00 | __init__.py; tests/test_p0_red_regressions.py | Ownership signing-key rotation | isolated rotation pytest | exit 0; 1 passed | - | Step 17 |
| 17 | [x] | COMPLETE | UNIT_TESTED | 2026-08-11T05:56:45+02:00 | 2026-08-11T05:57:52+02:00 | __init__.py; tests/test_p0_red_regressions.py | Harden legacy target and pre-delete verification | isolated forged pre-delete pytest | exit 0; 1 passed | - | Step 18 |
| 18 | [x] | COMPLETE | UNIT_TESTED | 2026-08-11T05:57:52+02:00 | 2026-08-11T06:00:16+02:00 | __init__.py; tests/test_ledger_migrations.py | Versioned SQLite migration and corruption gate | targeted migration pytest | exit 0; 2 passed | - | Step 19 |
| 19 | [x] | COMPLETE | UNIT_TESTED | 2026-08-11T06:00:16+02:00 | 2026-08-11T06:01:12+02:00 | __init__.py; tests/test_ledger_migrations.py | State permissions and symlink resistance | targeted permission pytest | exit 0; 4 passed | - | Step 20 |
| 20 | [x] | COMPLETE | INTEGRATION_TESTED | 2026-08-11T06:01:34+02:00 | 2026-08-11T06:14:30+02:00 | __init__.py; tests/test_mutation_recovery.py | Mutation state machine and unknown outcomes | py_compile; recovery suite; full pytest | exit 0; 6 focused, 58 full | Signed insert/deletion outcomes recover without duplicate insert or unsafe delete | Step 22 |
| 21 | [x] | COMPLETE | UNIT_TESTED | 2026-08-11T06:08:20+02:00 | 2026-08-11T06:10:18+02:00 | __init__.py; tests/test_mutation_recovery.py | Bounded authenticated delete_pending reconciliation | targeted pytest | exit 0; 4 passed | Only signed record deleted; missing confirmed by health; forged is conflict; no key is inert | Step 20 |
| 22 | [x] | COMPLETE | INTEGRATION_TESTED | 2026-08-11T06:14:30+02:00 | 2026-08-11T06:26:55+02:00 | 2026-08-11T06:26:55+02:00 | __init__.py; tests/test_lifecycle.py; tests/test_mutation_recovery.py | Client generation in-flight safety | py_compile; barrier suite; full pytest | exit 0; 10 focused, 62 full | Rotation and shutdown defer close until blocked RPC releases | Step 23 |
| 23 | [x] | COMPLETE | INTEGRATION_TESTED | 2026-08-11T06:26:55+02:00 | 2026-08-11T06:42:40+02:00 | 2026-08-11T06:42:40+02:00 | __init__.py; tests/test_ledger_migrations.py; tests/test_mutation_recovery.py | P1-A persisted bounded reconciliation | py_compile; P1-A suite; full pytest | exit 0; 16 focused, 64 full | Schema v2 persists retry count and due time; startup budget and cap prevent unbounded replay | Step 24 |
| 24 | [x] | COMPLETE | UNIT_TESTED | 2026-08-11T06:42:40+02:00 | 2026-08-11T07:08:42+02:00 | 2026-08-11T07:08:42+02:00 | README.md; tests/test_public_release.py | P1-B failed-mutation replay boundary | public docs test; full pytest | exit 0; 4 focused, 65 full | Docs state no add/replace replay and no eventual-consistency claim | Step 25 |
| 25 | [x] | COMPLETE | INTEGRATION_TESTED | 2026-08-11T06:44:05+02:00 | 2026-08-11T07:08:42+02:00 | 2026-08-11T07:08:42+02:00 | __init__.py; tests/test_hermes_contract.py | P1-C/D discovery and collection contract | real discovery probe; contract suite; full pytest | exit 0; 8 focused, 69 full | Setup discovers unconfigured provider; metric/dimension mismatch blocks reads and writes | Step 26 |
| 26 | [!] | BLOCKED | UNVERIFIED | 2026-08-11T07:08:42+02:00 | 2026-08-11T07:08:42+02:00 | - | P1-E payload duplication decision | authorized isolated E2E payload inspection | - | - | Cannot decide metadata content removal without live response shapes | Approved isolated E2E endpoint required; proceed Step 27 |
| 27 | [x] | COMPLETE | INTEGRATION_TESTED | 2026-08-11T07:08:42+02:00 | 2026-08-11T07:17:40+02:00 | 2026-08-11T07:17:40+02:00 | .gitignore; tests/test_public_release.py | P1-F release artifact hygiene | focused release suite; full pytest | exit 0; 5 focused, 70 full | Runtime state now ignored without deleting existing artifacts | Step 28 |
| 28 | [!] | BLOCKED | UNVERIFIED | 2026-08-11T07:17:40+02:00 | 2026-08-11T07:17:40+02:00 | - | P1-G relevance gate | calibrated distance distribution from authorized isolated E2E | - | - | No arbitrary Lorentz distance cutoff added | Needs actual result distances; proceed Step 29 |
| 29 | [x] | COMPLETE | INTEGRATION_TESTED | 2026-08-11T07:17:40+02:00 | 2026-08-11T07:22:52+02:00 | 2026-08-11T07:22:52+02:00 | README.md; tests/test_public_release.py | P1-H plaintext ledger disclosure | focused release suite; full pytest | exit 0; 6 focused, 71 full | README states plaintext scope, permissions, and encryption boundary | Step 30 |
| 30 | [x] | COMPLETE | INTEGRATION_TESTED | 2026-08-11T07:20:23+02:00 | 2026-08-11T07:22:52+02:00 | 2026-08-11T07:22:52+02:00 | __init__.py; tests/test_hermes_contract.py | P1-I tool trust boundary | focused tool suite; full pytest; py_compile | exit 0; 15 focused, 72 full | Search tools label retrieved content non-executable and reject unknown tool names | Step 31 |
| 31 | [x] | COMPLETE | INTEGRATION_TESTED | 2026-08-11T07:22:52+02:00 | 2026-08-11T07:28:22+02:00 | 2026-08-11T07:28:22+02:00 | __init__.py; tests/test_hermes_contract.py | error/status redaction | focused contract suite; full pytest | exit 0; 10 focused, 73 full | Secret-like strings are redacted from tool errors and status | Step 32 |
| 32 | [x] | COMPLETE | INTEGRATION_TESTED | 2026-08-11T07:27:44+02:00 | 2026-08-11T07:28:22+02:00 | 2026-08-11T07:28:22+02:00 | __init__.py; tests/test_hermes_contract.py | strict tool argument allowlist | focused contract suite; full pytest | exit 0; 11 focused, 74 full | Unknown tool arguments fail before handlers | Step 33 |
| 33 | [x] | COMPLETE | INTEGRATION_TESTED | 2026-08-11T07:28:22+02:00 | 2026-08-11T07:48:36+02:00 | 2026-08-11T07:48:36+02:00 | __init__.py; README.md; tests/ | public configuration contract | focused config suite; full pytest | exit 0; 19 focused, 76 full | Setup schema exposes metric/dimension controls; docs removed invalid trust-mode claim | Step 34 |
| 34 | [x] | COMPLETE | INTEGRATION_TESTED | 2026-08-11T07:39:42+02:00 | 2026-08-11T07:48:36+02:00 | 2026-08-11T07:48:36+02:00 | __init__.py; README.md; tests/ | HMAC environment boundary | focused credential suite; full pytest | exit 0; 22 focused, 79 full | Env HMAC overrides legacy config; authenticated writes refuse absent key without breaking read-only init | Step 35 |
| 35 | [x] | COMPLETE | INTEGRATION_TESTED | 2026-08-11T07:48:36+02:00 | 2026-08-11T08:35:42+02:00 | 2026-08-11T08:35:42+02:00 | __init__.py; tests/test_hermes_contract.py | queue overload failure accounting | focused contract suite; full pytest | exit 0; 15 focused, 80 full | Queue full is non-blocking, durable, and counted exactly once | Step 36 |
| 36 | [x] | COMPLETE | INTEGRATION_TESTED | 2026-08-11T07:50:58+02:00 | 2026-08-11T08:35:42+02:00 | 2026-08-11T08:35:42+02:00 | __init__.py; tests/test_hermes_contract.py | contract verification telemetry | focused contract suite; full pytest | exit 0; 16 focused, 81 full | Status exposes actual metric/dimension verification state | Step 37 |
| 37 | [x] | COMPLETE | INTEGRATION_TESTED | 2026-08-11T07:52:17+02:00 | 2026-08-11T08:35:42+02:00 | 2026-08-11T08:35:42+02:00 | tests/test_public_release.py | manifest/README version contract | release suite; full pytest | exit 0; 9 focused, 82 full | Manifest semver/dependency constraint matches public docs | Step 38 |
| 38 | [x] | INTEGRATION_TESTED | 2026-08-11T08:35:05+02:00 | 2026-08-11T08:35:42+02:00 | 2026-08-11T08:35:42+02:00 | tests/run_test_collection_e2e.py; tests/test_public_release.py | E2E pre-write guard | static runner gate; full pytest | exit 0; 10 focused, 83 full | E2E requires literal approval, non-prod HMAC, and hsdb_e2e_ target | Step 39 |
| 39 | [x] | INTEGRATION_TESTED | 2026-08-11T08:35:36+02:00 | 2026-08-11T08:35:42+02:00 | 2026-08-11T08:35:42+02:00 | tests/run_test_collection_e2e.py | live no-approval fail-closed probe | isolated shell invocation | exit 1 expected | Runner stopped at approval gate before client construction or collection mutation | Step 40 |
| 40 | [x] | COMPLETE | INTEGRATION_TESTED | 2026-08-11T08:35:42+02:00 | 2026-08-11T08:37:18+02:00 | 2026-08-11T08:37:18+02:00 | tests/test_public_release.py | tracked release manifest | release suite; full pytest | exit 0; 11 focused, 84 full | Git tracked manifest excludes state, SQLite, and bytecode artifacts | Step 41 |
| 41 | [x] | COMPLETE | STATIC_RELEASE_TESTED | 2026-08-11T08:37:18+02:00 | 2026-08-11T08:40:22+02:00 | 2026-08-11T08:40:22+02:00 | PLAN.md; Git state | final static release audit | diff check; tracked manifest; full pytest | exit 0; manifest 19 files, 85 full | No diff whitespace failures; tracked manifest has no runtime artifacts | Step 42 |
| 42 | [x] | COMPLETE | INTEGRATION_TESTED | 2026-08-11T08:38:34+02:00 | 2026-08-11T08:40:22+02:00 | 2026-08-11T08:40:22+02:00 | README.md; tests/run_test_collection_e2e.py; tests/ | E2E state isolation | release suite; full pytest | exit 0; 12 focused, 85 full | E2E needs external explicit ledger path; plugin state remains untouched | Step 43 |
| 43 | [!] | BLOCKED | NOT_E2E_VERIFIED | 2026-08-11T08:40:22+02:00 | 2026-08-11T08:40:22+02:00 | - | strict isolated mutation E2E + production verdict | approved target/source/HMAC/state path | - | exit 1 expected at HMAC gate | No production/shared collection was touched; static hardening cannot substitute for E2E | Await explicitly isolated E2E configuration |
| LUNA-1 | [x] | DONE | INTEGRATION_TESTED | 2026-08-11T09:05:26+02:00 | 2026-08-11T09:09:40+02:00 | 2026-08-11T09:09:40+02:00 | PLAN.md; PLAN-LUNA.md only | PTY local suite, then write PLAN-LUNA.md | 0 | 85 passed in 2.34s; PLAN-LUNA.md written and verified by write receipt. No real E2E runner, collection, or shared implementation/test/documentation file was changed. | User may launch Luna; base steps 26, 28, and 43 remain blocked. |
| LUNA-2 | [x] | DONE | STATIC_CHECKED | 2026-08-11T09:51:41+02:00 | 2026-08-11T09:54:08+02:00 | 2026-08-11T09:54:08+02:00 | PLAN.md changed; LUNA-AUDIT-REPORT.md plus cited source/tests read only | Read report and validate current cited lines | 0 | Accepted L-03, L-04, L-06 as scoped gaps; L-05 restates blocked live-SDK evidence; rejected L-01, L-02, L-07; L-08 no defect. No implementation/test/E2E action. | Await explicit isolated E2E authorization or separately approved fix scope. |
| L6-1 | [x] | DONE | INTEGRATION_TESTED | 2026-08-11T09:56:03+02:00 | 2026-08-11T10:15:02+02:00 | 2026-08-11T10:15:02+02:00 | PLAN.md; runner/test diff reviewed | Targeted guard suite, full PTY suite, scoped diff review | 0 | Guard rejects empty/relative/in-plugin paths and accepts external absolute path. 16 targeted passed in 1.51s; 89 full passed in 2.28s. RED phase not witnessed because changes pre-existed Terra's write attempt. No E2E runner invoked. | Strict E2E gates 26, 28, 43 remain blocked. |
| L4-1 | [x] | DONE | INTEGRATION_TESTED | 2026-08-11T10:28:26+02:00 | 2026-08-11T10:55:55+02:00 | 2026-08-11T10:55:55+02:00 | PLAN.md; __init__.py; tests/test_public_release.py only | RED, targeted GREEN, privacy scan, full no-E2E PTY suite, diff review | 0 | RED witnessed; trusted_sources removal passed targeted GREEN. Current full suite: 90 passed in 3.60s. No E2E/backend action. | Publication is separately tracked as PUBLISH-1. |
| PUBLISH-1 | [-] | SKIPPED | NOT_APPLICABLE | 2026-08-11T10:55:55+02:00 | 2026-08-13T08:51:38+02:00 | 2026-08-13T08:51:38+02:00 | No public or standalone repository action | User supersession instruction | - | Local-only directive cancelled every remote/subtree/push action. | LOCAL-HARDENING-1 |
| LOCAL-HARDENING-1 | [x] | DONE | INTEGRATION_TESTED | 2026-08-13T08:51:38+02:00 | 2026-08-13T09:18:31+02:00 | 2026-08-13T09:18:31+02:00 | __init__.py; tests; README; manifest; LICENSE; attributes; AUDIT; PLAN | Targeted RED/GREEN; full no-E2E PTY suite; staged archive/index review; scoped local commit | 0 | 96 passed in 14.32s before commit `1f2fcd519`; commit contains only reviewed local plugin artifacts. | Base strict E2E remains blocked; OPTIONAL-A began from this committed baseline |
| HANDOFF-2 | [x] | DONE | STATIC_CHECKED | 2026-08-11T10:22:57+02:00 | 2026-08-11T10:25:07+02:00 | 2026-08-11T10:25:07+02:00 | PLAN.md; HANDOFF-TERRA-2.md only | Current status/log plus handoff creation | 0 | Handoff write receipt verified. No source/test operation during transfer. | Next session resumes L4 RED and Git gate from handoff. |
| A1 | [x] | DONE | STATIC_CHECKED | 2026-08-13T09:18:31+02:00 | 2026-08-13T09:18:31+02:00 | 2026-08-13T09:18:31+02:00 | PLAN.md; local commit baseline | Optional baseline frozen at `1f2fcd519` before A2 | 0 | Baseline recorded before optional local changes; no E2E | A2 |
| A2 | [x] | DONE | INTEGRATION_TESTED | 2026-08-13T09:20:00+02:00 | 2026-08-13T09:36:00+02:00 | 2026-08-13T09:36:00+02:00 | __init__.py; tests/test_optional_audit.py; tests/test_ledger_migrations.py; tests/test_hermes_contract.py; PLAN.md | Aggregate-only profile-scoped local audit tool; fake-client/local-ledger tests; full no-E2E suite | 0 | 24 focused passed; 97 full passed; local commit `ca7a62de3` | A3 |
| A3 | [x] | DONE | INTEGRATION_TESTED | 2026-08-13T09:40:48+02:00 | 2026-08-13T11:04:13+02:00 | 2026-08-13T11:04:13+02:00 | __init__.py; README.md; tests/test_optional_graph_points.py; tests/test_mutation_semantics.py; tests/test_p0_red_regressions.py; tests/test_public_release.py; PLAN.md | Raw uint32 backend-slot lookup replaced locally with short-lived opaque capability handles; store/prefetch/graph/hierarchy outputs avoid slot IDs; clusters expose only safe cardinalities; docs match nine-tool capability contract | focused fake-client/README suites plus full no-E2E suite and staged scope review | final pre-commit suite: 105 passed in 14.45s; commit `87d3eec2a` has seven plugin files and zero outside-plugin files | Base strict E2E remains blocked | A4 |
| A4 | [>] | COMMIT_GATE | INTEGRATION_TESTED | 2026-08-13T11:04:13+02:00 | 2026-08-13T11:22:41+02:00 | - | __init__.py; README.md; tests/conftest.py; tests/test_optional_admin.py; tests/test_public_release.py; PLAN.md | Add only read-only admin count/digest/cache_stats; sanitize existing stats/status with field allowlists | fake-client admin/status/security plus README contracts; full no-E2E suite; AST allowlist audit | RED 3 expected failures; GREEN admin/status 32 passed; README/admin 5 passed; full 110 passed in 14.36s; AST/compile/diff-check passed | No implementation blocker; exact staged scope remains | Stage/recheck listed plugin paths, then local A4 commit only if staging gate is clean |
| A5 | [ ] | TODO | UNVERIFIED | - | - | - | - | - | - | - | - |
| A6 | [ ] | TODO | UNVERIFIED | - | - | - | - | - | - | - | - |
| A7 | [ ] | TODO | UNVERIFIED | - | - | - | - | - | - | - | - |
| A8 | [ ] | TODO | UNVERIFIED | - | - | - | - | - | - | - | - |

### FAILURE AND DECISION LOG

Append failures and operator decisions; never overwrite earlier entries.

| UTC time | Step | Type | Observation/decision | Consequence | Next action |
|---|---:|---|---|---|---|
| - | - | - | No next-executor entries yet | - | Start step 1 |
| 2026-08-11T06:08:39+02:00 | 20 | TOOLING | A quoted terminal patch failed before writing source. | No source change from failed command. | Switched to an encoded in-scope editor. |
| 2026-08-11T06:10:18+02:00 | 21 | DECISION | User required git commits limited to this plugin. | Stage/commit only plugin paths after an evidence-backed batch. | Run full suite, inspect scoped diff, then create scoped commit. |
| 2026-08-11T06:11:50+02:00 | 20/21 | GIT | Scoped plugin-only baseline committed after full fake suite. | Commit 0775d5948 contains only 18 plugin source/docs/test files; runtime state was excluded. | Continue Step 20; stage only explicit plugin source paths for later commits. |
| 2026-08-11T06:14:30+02:00 | 20 | TEST | State transitions and recovery tested on fake backend. | 6 focused tests and 58 full tests passed; no real backend mutated. | Begin lifecycle generation safety. |
| 2026-08-11T06:24:50+02:00 | 22 | TEST | Existing lifecycle test expected immediate close after direct client acquisition. | Test failed because direct acquisition is now a lease; revised it to release before close assertion. | Barrier tests added, then full suite rerun. |
| 2026-08-11T06:26:55+02:00 | 22 | TEST | Barrier rotation/shutdown lifecycle cases passed. | 10 focused tests and 62 full tests pass; fake backend only. | Begin P1-A bounded retry persistence. |
| 2026-08-11T06:27:40+02:00 | 22 | GIT | Scoped lifecycle hardening committed. | Commit 71b9e8fd1 contains only plugin source, tests, and tracker; runtime state remains excluded. | Continue Step 23 with persisted bounded retry design. |
| 2026-08-11T06:31:20+02:00 | BASE | OPERATOR | User requires uninterrupted execution with an explicit report every 10 tracked points. | Continue silently until checkpoint 30, then 40, then base completion; keep PLAN live and commit scoped batches. | Implement Step 23. |
| 2026-08-11T06:42:40+02:00 | 23 | TEST | Persisted retry/backoff and schema upgrade tested. | 16 focused tests and 64 full tests passed on fake backend; no external endpoint invoked. | Close P1-B documentation boundary. |
| 2026-08-11T06:57:13+02:00 | 25 | TEST | Initial metric contract tests exposed missing dimension fallback and degraded rather than configuration health. | Repaired fallback and status semantics; 69 full tests pass. | Mark Step 25 complete. |
| 2026-08-11T07:08:42+02:00 | 26 | BLOCKER | Payload duplication requires actual current server responses to decide safely. | No source removal based on intuition; status remains not E2E verified. | Continue non-E2E release hygiene. |
| 2026-08-11T06:46:06+02:00 | BASE | OPERATOR | Delegate only genuinely easy missions to GPT-5.6-Luna while current context budget is constrained. | Current P1-D was a critical fail-closed code path and remained local. | Route later mechanical review only if Luna invocation is verifiably available. |
| 2026-08-11T07:17:40+02:00 | 27 | DECISION | Runtime `state/` existed but must neither be deleted nor committed. | Added ignore rules and a Git behavior test; artifacts remain untouched. | Mark Step 27 complete. |
| 2026-08-11T07:17:40+02:00 | 28 | BLOCKER | Automatic relevance depends on actual backend distance scale, which has not been empirically authorized. | Retain existing optional `max_distance`; do not invent a default cutoff. | Resume only after isolated E2E. |
| 2026-08-11T07:20:32+02:00 | 30 | TEST | Initial data-boundary test exposed an omitted advanced-search envelope. | Added the envelope; a failed external patch operation had prepended one gRPC log line to `__init__.py`, which was removed before compilation. | Keep direct py_compile in the gate. |
| 2026-08-11T07:22:52+02:00 | 30 | CHECKPOINT | Numeric steps through 30 processed: 28 completed, 2 correctly blocked on authorized E2E evidence. | Latest local suite is 72 passed. | Commit post-P1 changes and proceed Step 31. |
| 2026-08-11T07:28:22+02:00 | 31 | TEST | Initial redaction test expected a redaction marker from a generic backend error, but the classifier had already dropped the secret. | Retained generic-error safety test and added direct sanitizer test; fixed regex backreference using a lambda. | Mark Step 31 complete. |
| 2026-08-11T07:28:22+02:00 | 32 | DECISION | JSON schemas alone are not a reliable runtime validation boundary. | Added fail-closed per-tool argument allowlist in the handler. | Mark Step 32 complete. |
| 2026-08-11T07:47:32+02:00 | 34 | TEST | Eager HMAC validation blocked read-only initialization and two existing lifecycle tests. | Removed eager validation; writes remain authenticated and fail closed at mutation time. | Mark Step 34 complete. |
| 2026-08-11T08:35:36+02:00 | 39 | VERIFY | Ran the E2E runner with approval and all E2E identity variables deliberately unset. | Exit 1 at the literal approval guard; no client, collection, or write was reached. | Mark Step 39 complete. |
| 2026-08-11T08:37:18+02:00 | 40 | VERIFY | Checked the actual Git tracked manifest rather than merely `.gitignore`. | 84 full tests pass and no runtime state, SQLite, or bytecode is tracked. | Mark Step 40 complete; checkpoint report due. |
| 2026-08-11T08:40:15+02:00 | 43 | VERIFY | Ran the runner with literal approval but unset test HMAC/state/source/target variables. | Exit 1 at HMAC gate before a client, collection, or mutation operation. | Retain NOT_E2E_VERIFIED verdict. |
| 2026-08-11T08:40:22+02:00 | 43 | VERDICT | 85 fake/static tests and release gates are green, but payload-shape, relevance-distance calibration, and add/replace/remove integration are unmeasured. | Public release is not production-ready. | Stop optional work; wait for authorized isolated E2E. |
| 2026-08-11T08:44:30+02:00 | HANDOFF | HANDOFF | Created `HANDOFF.md` with the complete compact continuation state after a clean scoped Git status and PTY full suite. | Next executor has explicit scope, evidence, commits, blockers, and tracker rules. | Read HANDOFF.md and PLAN.md before any action. |
| 2026-08-11T09:05:26+02:00 | LUNA-1 | DECISION | User requested a separate GPT-5.6-Luna read-only adversarial audit plan and literal launch prompt. | Base tracker remains 40/43 with steps 26, 28, and 43 blocked; no implementation, optional capability, shared test, or E2E action is authorized. | Record a fresh PTY local-suite result, then write only PLAN-LUNA.md and update this ledger immediately. |
| 2026-08-11T09:06:42+02:00 | LUNA-1 | TEST | Current full plugin suite ran through PTY using a fresh in-scope basetemp. | Exit 0; 85 passed in 2.34s. This is current fake/static integration evidence, not real-backend E2E evidence. | Create the bounded read-only Luna audit plan; retain the not-production-ready verdict. |
| 2026-08-11T09:09:40+02:00 | LUNA-1 | HANDOFF | Created PLAN-LUNA.md under PLUGIN_ROOT only. It assigns Luna an independent read-only adversarial audit and permits writing only LUNA-AUDIT-REPORT.md. | Luna cannot alter source, PLAN.md, tests, shared docs, runtime state, configuration, collections, or E2E state. Base steps 26, 28, and 43 remain blocked. | User may start Luna with literal prompt; current production verdict remains not production ready. |
| 2026-08-11T09:51:41+02:00 | LUNA-2 | DECISION | User reported the Luna audit complete. | Terra opens a separate evidence-review step before accepting any report finding or changing implementation/test state. | Read the report and validate each cited claim against current files. |
| 2026-08-11T09:54:08+02:00 | LUNA-2 | REVIEW | Terra independently checked Luna report citations against current source/test/plan lines. | Accepted: L-03 malformed-row observability, L-04 unreachable trusted_sources branch, L-06 no runtime guard against an in-plugin E2E state path. Existing blockers: L-05. Rejected: L-01 because section 3 is historical while step 7 is closed, L-02 because test_p0_red_regressions exercises list stubs and swallowed telemetry, L-07 because 3.07s and 2.34s are distinct PTY runs. L-08 correctly found no defect. | Do not patch without a separate approved scope; strict E2E gates 26, 28, 43 remain blocked. |
| 2026-08-11T09:56:03+02:00 | L6-1 | OPERATOR | User issued go-ahead for the L-06 remediation after its evidence review. | Scope frozen to runner, release test, and PLAN.md only; no backend/configuration/collection action is authorized. | Read live runner/test headers and implement the pure fail-closed state-path boundary. |
| 2026-08-11T10:03:21+02:00 | L6-1 | CONCURRENT_STATE | Terra's PLAN patch found the L6 plan and runner/test diff already present with an earlier timestamp. | No stale overwrite occurred. Current diff was read and treated as un-attributed until directly tested. | Run targeted PTY test and record only observed evidence. |
| 2026-08-11T10:05:35+02:00 | L6-1 | TEST | Targeted release/source-contract suite executed through PTY without bytecode or pytest cache writes. | Exit 0; 16 passed in 1.51s. L6 path guard behavior passed. RED phase remains unobserved due pre-existing concurrent changes. | Run full local PTY suite; do not invoke E2E. |
| 2026-08-11T10:13:56+02:00 | L6-1 | TEST | Full local plugin suite executed through PTY with bytecode and pytest cache writes disabled and a fresh in-scope basetemp. | Exit 0; 89 passed in 2.28s. The E2E runner was not invoked; no backend, credential, collection, or runtime-state mutation occurred beyond isolated local test state. | Inspect scoped diff before marking L6 complete. |
| 2026-08-11T10:15:02+02:00 | L6-1 | REVIEW | Scoped runner/test diff and whitespace contract were reviewed after current full-suite evidence. | Diff contains only pure external-state-path validation, its pre-client invocation, and matching stubbed contract tests. `git diff --check` exit 0. No secret, client construction, backend call, or mutation path added by the guard. | Mark L6 static preflight hardening complete; strict E2E remains blocked. |
| 2026-08-11T10:17:11+02:00 | L4-1 | OPERATOR | User directed continued execution after L6 completion. | Scope frozen to PLAN.md, __init__.py, and tests/test_public_release.py for removal of unreachable trusted_sources code only. No E2E, backend, config, collection, or optional work is authorized. | TDD RED test through PTY, then minimal source removal. |
| 2026-08-11T10:22:57+02:00 | L4-1 | TOOLING | A malformed patch invocation returned `patch content required`. | Tool reported no file modification; the planned L4 test remains absent. | Preserve the failed attempt, pause L4 for user-requested handoff, and resume with RED test next session. |
| 2026-08-11T10:22:57+02:00 | HANDOFF-2 | OPERATOR | User requested a next-session handoff and reminded that Git commit discipline is required. | Do not commit un-attributed current L6 diff blindly. Next session must review scoped diff, run/retain tests, selectively stage only approved plugin files, verify staged scope, then commit. | Create handoff with exact Git gate and literal next-session prompt. |
| 2026-08-11T10:25:07+02:00 | HANDOFF-2 | HANDOFF | Created HANDOFF-TERRA-2.md under PLUGIN_ROOT only. | It records current Git state, L6 evidence, L4 exact RED-GREEN sequence, strict E2E prohibition, and selective Git commit gate. No source/test/E2E operation occurred during transfer. | User may launch next Terra session with literal prompt. |
| 2026-08-11T10:28:26+02:00 | L4-1 | DECISION | Read all mandated handoff documents and observed scoped Git status, diff names, and eight scoped commits before a write. | L4 set to IN_PROGRESS; source and test remain untouched. | Run fresh PTY local suite with a new in-scope basetemp; never invoke E2E. |
| 2026-08-11T10:30:24+02:00 | L4-1 | TEST | Current full local suite ran through PTY with bytecode and pytest cache writes disabled; E2E runner was explicitly ignored. | Exit 0; 89 passed in 3.88s. This is fake/static integration evidence only and does not test L4 behavior or real backend paths. | Add required RED source-contract test before changing __init__.py. |
| 2026-08-11T10:33:58+02:00 | L4-1 | DECISION | Exact required L4 source-contract test was already present in the uncommitted public-release diff. User confirmed no other live editor will modify PLUGIN_ROOT. | No duplicate test was added; source remains unchanged. Direct test-first authorship is unavailable. | Run only the existing L4 test through PTY and require expected RED before source edit. |
| 2026-08-11T10:34:29+02:00 | L4-1 | TEST | Targeted public-surface contract ran through PTY with bytecode and pytest cache writes disabled. | Exit 1 was expected: 1 failed in 0.45s because trusted_sources remains in __init__.py. No E2E runner or backend path was invoked. | Apply minimal source removal; do not alter result provenance metadata. |
| 2026-08-11T10:36:21+02:00 | L4-1 | PATCH | Applied a bounded source-only removal after the witnessed RED. | Removed trusted_sources config/default state, trusted_claim, unreachable branch, and obsolete fallback wording; source/trust result metadata retained. | Run targeted GREEN through PTY. |
| 2026-08-11T10:38:18+02:00 | L4-1 | TEST | Re-ran the same targeted public-surface contract through PTY after the minimal source removal. | Exit 0; 1 passed in 0.67s. This is unit evidence only; no E2E runner or backend path was invoked. | Run full local no-E2E PTY suite. |
| 2026-08-11T10:39:56+02:00 | L4-1 | TEST | Full local suite ran through PTY with bytecode and pytest cache writes disabled; E2E runner was explicitly ignored. | Exit 1: 89 passed, 1 public-release privacy-scan failure caused by PLAN.md private identifiers. | Scrub PLAN.md only, then rerun focused release scan and full suite. |
| 2026-08-11T10:41:38+02:00 | L4-1 | TEST | Focused public-release privacy scan ran through PTY after PLAN.md command evidence was neutralized. | Exit 0; 1 passed in 0.81s. No E2E runner or real backend path was invoked. | Run full local no-E2E PTY suite. |
| 2026-08-11T10:43:07+02:00 | L4-1 | TEST | Full local suite ran through PTY with bytecode and pytest cache writes disabled; E2E runner was explicitly ignored. | Exit 0; 90 passed in 3.79s. This is current fake/static integration evidence only, not real-backend E2E. | Run scoped diff check/review before selective staging. |
| 2026-08-11T10:55:55+02:00 | PUBLISH-1 | OPERATOR | User explicitly directed replacement of the public target v1 with the current plugin artifact. | Target public visibility was observed before outbound action; candidate scan across 23 selected files was clean and current no-E2E suite passed 90 in 3.60s. | Selectively stage, commit, replace target main, and verify remote readback. |
| 2026-08-13T08:51:38+02:00 | LOCAL-HARDENING-1 | OPERATOR | User superseded public-repository work: ignore every standalone/public repository and repair only the local plugin tree with local Git commits. | PUBLISH-1 is cancelled; no remote/subtree/push action is allowed. Active work is bounded local trust, payload-integrity, profile-scope, advanced-override, relevance-prefetch, packaging, docs, tests, and PLAN tracking. | Complete local fake-client gates; do not invoke E2E or any backend. |
| 2026-08-13T08:51:38+02:00 | LOCAL-HARDENING-1 | TEST | Witnessed RED/GREEN cycles for HMAC-signed model-authored prefetch, tampered returned payload, trust relabel, passed Hermes home, advanced collection override, release metadata, and uncalibrated annotate_all prefetch. | Source gates are PATCHED; targeted no-E2E suites passed at intermediate checkpoints. A fixture-only syntax error and fixture-wide max-distance overreach were detected and repaired before source acceptance. | Run final full no-E2E suite, archive/release gate, doc scan, staged-diff review, then commit only local plugin files. |
| 2026-08-13T08:51:38+02:00 | OPTIONAL-A-G | OPERATOR | After LOCAL-HARDENING-1 is verified and committed, user explicitly authorized OPTIONAL-A through OPTIONAL-G. | This later user instruction overrides the prior optional-phase ordering restriction, but does not authorize E2E, backend calls, collection mutation, secret loading, core/config/SDK changes, or work outside PLUGIN_ROOT. | Execute optional capabilities sequentially with TDD, live PLAN append entries, scoped Git commits, and no false production claim. |
| 2026-08-13T09:05:23+02:00 | LOCAL-HARDENING-1 | TOOLING | Initial final-suite command used a repository-relative path while the terminal remained in the plugin directory. | Git add failed before staging or test execution; no source/test result was produced and the pre-existing staged set was unchanged. | Re-run with explicit plugin-directory paths and retain this failed command as evidence. |
| 2026-08-13T09:07:53+02:00 | LOCAL-HARDENING-1 | VERIFY | Full fake-client local suite ran through PTY with `run_test_collection_e2e.py` explicitly ignored. Staged-index archive was built from `git write-tree`. | Exit 0; 96 passed in 14.32s. Archive contains one LICENSE, no PLAN/HANDOFF/AUDIT/LUNA/PROMPT ledgers, and staged tracked scan contains no state/SQLite/bytecode paths. No backend, credentials, collection, or E2E action occurred. | Update active state and staged PLAN, commit only the 11 reviewed plugin files, then start OPTIONAL-A. |
| 2026-08-13T09:10:16+02:00 | LOCAL-HARDENING-1 | GIT | Staged scope rechecked after tracker rewrite. | Exactly 11 plugin files staged; `AUDIT-CLEAN-20260813.md` remains preserved but untracked and outside the commit. Staged whitespace check is clean. | Run final suite after this PLAN append, then create local commit. |
| 2026-08-13T09:15:41+02:00 | LOCAL-HARDENING-1 | HARNESS | A mistakenly broad repository test command collected unrelated Hermes suites under the system Python. | Exit 2 during collection because optional unrelated dependencies (`acp`, `prompt_toolkit`, `wcwidth`) are absent. This does not invalidate the dedicated plugin suite and no provider test ran in this command. No installation or unrelated test/core modification was performed. | Re-run only `PLUGIN_ROOT/tests` via explicit `cd` with E2E runner ignored; do not claim repository-wide verification. |
| 2026-08-13T09:17:00+02:00 | LOCAL-HARDENING-1 | VERIFY | Dedicated plugin suite reran through explicit `cd` to PLUGIN_ROOT, with E2E runner ignored and a fresh in-plugin basetemp. | Exit 0; 96 passed in 11.15s. Staged scope remains exactly 11 local plugin files, with no staged path outside PLUGIN_ROOT. | Commit local hardening; then start OPTIONAL-A under the separately authorized scope. |
| 2026-08-13T09:18:31+02:00 | LOCAL-HARDENING-1 | GIT | Local commit `1f2fcd519` created from 11 reviewed plugin files. | Commit contains only local provider code/tests/docs/metadata; public/standalone repositories were not accessed or modified. `AUDIT-CLEAN-20260813.md` remains preserved and untracked. | Freeze OPTIONAL-A baseline and begin its TDD cycle. |
| 2026-08-13T09:18:31+02:00 | A1/A2 | START | Optional baseline frozen at local commit `1f2fcd519`; user authorized OPTIONAL-A through OPTIONAL-G after that commit. | A2 is active. Scope is local provider source/tests/README/PLAN only; no E2E/backend/secrets/core/SDK/config work. | Add A2 aggregate-only audit test, witness RED, then minimal implementation. |
| 2026-08-13T09:20:00+02:00 | A2 | TEST | Wrote the A2 aggregate-only audit contract and ran it with the fake client/local ledger. | Expected RED: exit 1, because `hyperspace_audit` is not yet registered. The test asserts no memory content, raw error, digest, or point ID escapes. | Add only local ledger aggregate queries, audit schema, and a read-only tool handler; no RPC path. |
| 2026-08-13T09:26:06+02:00 | A2 | TOOLING | First v3 ledger-migration patch accidentally replaced the v2 retry-table creation block. The source was corrected immediately to preserve v1->v2->v3 order. | Migration suite then failed only because its historical assertions still expected schema v2, while live source now correctly reports v3. This is a test-contract update required by the new local schema, not a backend failure. | Update migration assertions for v3 and verify v2 retry table plus v3 profile-scope column before wiring audit handler. |
| 2026-08-13T09:32:59+02:00 | A2 | TEST | First GREEN run verified code paths but audit test incorrectly expected an empty fake-client history even though provider initialization already probes health/stats. | The audit handler itself made no new RPC; assertion was narrowed to compare call history before and after the audit invocation. | Re-run the same targeted A2/migration/contract suite. |
| 2026-08-13T09:34:01+02:00 | A2 | VERIFY | Aggregate-only audit, v3 migration, and tool-contract suite reran through PTY using fake client/local ledger only. | Exit 0; 24 passed in 1.35s. Audit exposes profile-scoped state/failure aggregates and schema version only; no content, raw error, digest, ID, or new RPC call escapes. | Run complete local no-E2E suite, staged review, then commit OPTIONAL-A. |
| 2026-08-13T09:35:21+02:00 | A2 | VERIFY | Full local plugin suite reran with E2E runner ignored. | Exit 0; 97 passed in 10.53s. `hyperspace_audit` is read-only over the local ledger, profile-scoped, aggregate-only, and makes no new client RPC. | Stage exact A2 files, commit locally, then start A3. |
| 2026-08-13T09:40:48+02:00 | A3 | TEST | Wrote bounded graph-points tests and ran them against the existing graph handler. | Expected RED: exit 1 because `points` was not an accepted graph operation. Duplicate/oversized input already made no RPC, but after implementation the user-input error class was `CONFIGURATION_ERROR` instead of the required stable `INVALID_ARGUMENT`. | Add a dedicated invalid-argument provider error and rerun the same bounded graph test. |
| 2026-08-13T09:55:45+02:00 | A3 | DECISION | User challenged the `uint32` premise. Source audit confirms the current protobuf and Rust index use uint32 slots, but logical identity is full SHA-256/HMAC/profile scope. At ~39,482 records, a uniform 32-bit initial-slot allocation has a 16.60% probability of at least one collision; probing is necessary but does not make a slot an identity. | The draft accepts raw backend IDs and therefore gives the model an enumerable cross-session addressing surface. Functional tests pass, but the design is rejected. The uncommitted draft is preserved; no A3 commit or promotion occurs. | Await explicit approval of opaque, short-lived, profile-scoped result handles or a separately scoped server/SDK wider-ID migration. |
| 2026-08-13T10:32:50+02:00 | A3 | OPERATOR | User directed continuation of the entire local-plugin PLAN and required live PLAN.md appends. | A3 resumes only as a plugin-local capability-handle migration: random handles are RAM-only, profile/session/collection scoped, bounded, and never expose raw slots. No SDK/server/backend/E2E change is authorized. | Migrate legacy graph and hierarchy raw-ID inputs/outputs, then verify focused and full no-E2E suite before any commit. |
| 2026-08-13T10:32:50+02:00 | A3 | TEST | Fake-client capability-points tests reached GREEN, then a dedicated node test was added before changing legacy graph behavior. | RED exit 1 proves legacy `start_id` is still accepted and leaks a raw backend slot through the graph surface; A3 is not accepted yet. | Replace graph/hierarchy model inputs with capability handles and recursively sanitize returned slot IDs. |
| 2026-08-13T10:37:34+02:00 | A3 | TEST | Focused GREEN after graph/hierarchy migration failed one graph-node contract assertion. | The sanitizer minted a second handle for the same live slot instead of preserving the caller's capability; no raw slot leaked, but handle continuity was wrong. `py_compile` and scoped whitespace check still passed. | Canonicalize handle issuance per live profile/session/collection/slot, rerun focused GREEN, then full no-E2E suite. |
| 2026-08-13T10:40:17+02:00 | A3 | TEST | Expanded fake-client output-surface test found `hyperspace_store` returning `record_id`, a backend uint32 allocation slot. Cluster output is also structurally an ID list and must not become a raw-slot enumeration surface. | A3 remains IN_PROGRESS; the failure is a real contract defect, not an accepted test adjustment. | Replace store `record_id` with its live capability handle; reduce clusters to sanitized structural sizes rather than point identifiers, update identity test, then rerun focused GREEN. |
| 2026-08-13T10:47:24+02:00 | A3 | VERIFY | Focused fake-client capability suite executed after store/prefetch/graph/hierarchy output sanitization and lifecycle negative tests. | Exit 0; 53 passed in 2.93s. Expired and reinitialized handles failed locally before graph RPC; `py_compile` and scoped `git diff --check` both passed. No E2E runner, credential, collection, or server/SDK action occurred. | Run fresh complete plugin suite with E2E runner ignored and inspect scoped diff before local commit. |
| 2026-08-13T10:49:24+02:00 | A3 | VERIFY | Full local plugin suite ran with `run_test_collection_e2e.py` explicitly ignored. | Exit 0; 104 passed in 19.88s. Schema probe confirmed raw graph/hierarchy slot input fields are absent and handle fields are present. Scope inspection found only intended source/tests/PLAN plus the preserved untracked audit artifact. | Repair discovered README tool-count/capability-contract drift, then rerun release and complete no-E2E verification before A3 commit. |
| 2026-08-13T10:52:03+02:00 | A3 | TEST | Added a README contract test after source/schema review showed docs claim eight tools although the provider registers nine since A2. | Expected RED: exit 1 because README lacks the current tool count and capability-handle contract. No runtime/backend action. | Update README only with verified current tool list and raw-slot boundary, then rerun targeted GREEN. |
| 2026-08-13T10:53:24+02:00 | A3 | VERIFY | README nine-tool and capability-boundary contract test reran after the bounded documentation correction. | Exit 0; 1 passed in 0.91s. `py_compile` and scoped whitespace passed. This corrects documentation only and does not alter E2E status. | Run final complete local plugin suite with E2E runner ignored, then stage/review local A3 files. |
| 2026-08-13T10:56:13+02:00 | A3 | VERIFY | Final complete local plugin suite reran after README correction with `run_test_collection_e2e.py` explicitly ignored. | Exit 0; 105 passed in 18.23s. No E2E runner, credentials, collection mutation, server/SDK, core, config, standalone/public repository, or remote action occurred. | Update tracker to COMMIT_GATE; stage only reviewed local A3 files and verify index scope before commit. |
| 2026-08-13T11:04:13+02:00 | A3 | GIT | Local commit `87d3eec2a` created after staged scope review. | Commit manifest contains exactly seven files under the local plugin path and zero paths outside it; preserved audit artifact remains untracked. | Begin A4 only after source inventory and a fresh RED contract. |
| 2026-08-13T11:08:05+02:00 | A4 | INVENTORY | Read-only SDK/source audit found `count`, `get_digest`, and `get_cache_stats`; server cache endpoint is GET and cache struct has six structural fields. Existing plugin `stats` and `status` pass raw backend maps, which would violate the same allowlist rule. | A4 scope includes sanitizing existing model-facing stats/status as well as adding the three planned operations. No source, SDK/server, collection, credential, or E2E action occurred during inventory. | Write fake-client RED tests for all admin output allowlists and malformed responses. |
| 2026-08-13T11:10:11+02:00 | A4 | TEST | Added fake-client admin allowlist/malformed/schema contracts and ran them before A4 implementation. | Expected RED: exit 1; three failures showed missing operations/schema and raw stats passthrough. A source check also found the actual DigestResponse state_hash is uint64, so the initially drafted string-hash test was corrected before implementation. | Add only read-only fake stubs, schemas, strict numeric allowlists, and handler branches; do not change SDK/server. |
| 2026-08-13T11:18:14+02:00 | A4 | VERIFY | Targeted admin/status/security/Hermes-contract suite reran after implementation and an added status regression contract. | Exit 0; 32 passed in 1.53s. Admin `stats`, `count`, `digest`, `cache_stats`, and status stats use strict allowlists; malformed maps fail with MALFORMED_RESULT; no cache mutation operation was registered. Scoped whitespace is clean. | Add README contract for the verified admin operations, then rerun targeted and full no-E2E suite. |
