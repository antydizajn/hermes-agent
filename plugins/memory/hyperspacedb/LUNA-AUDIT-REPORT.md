# LUNA READ-ONLY ADVERSARIAL AUDIT REPORT

## Scope And Evidence Boundary
- Files read (whole, in PLAN-LUNA order): HANDOFF.md, PLAN.md, PLAN-LUNA.md, __init__.py (all 1975 lines), tests/conftest.py, tests/test_baseline_contract.py, tests/test_mutation_semantics.py, tests/test_mutation_recovery.py, tests/test_retrieval.py, tests/test_security.py, tests/test_lifecycle.py, tests/test_hermes_contract.py, tests/test_public_release.py, tests/test_ledger_migrations.py, tests/test_p0_red_regressions.py, tests/run_test_collection_e2e.py, README.md, plugin.yaml.
- Commands run (read-only inspection only): `ls`, `wc`, `sed -n ... file | grep -v ev_poll_posix`, `python3 -c "...read() / splitlines()... print(lineno|line)"` over __init__.py, PLAN.md, tests/run_test_collection_e2e.py, `grep -nE` over PLAN.md. No mutation, no import of plugin, no client construction, no pytest, no build, no git write, no E2E.
- No-write verification: the only disk write produced by this session is this file (LUNA-AUDIT-REPORT.md). No other file was touched (read-only file descriptors only).
- Forbidden actions not run: no edit of __init__.py/PLAN*/HANDOFF/README/plugin.yaml/tests/shared docs; no state/cache/SQLite/branch/commit/collection change; no .env/secret/profile/credential read; no pytest/build/formatter/install/E2E/backend/mutation; no A1-A8; no production verdict change.
- Evidence klud: terminal stdout was polluted by an unrelated background gRPC poll-list line (ev_poll_posix). All quoted line numbers were re-derived by ground-truth `python` offset scans stripping that line, so every cited line number reflects the real file on disk.

## Current Execution State
- Active step: audit analysis + report compilation
- Last updated UTC: 2026-08-11 (session running)
- Result status: COMPLETE (all Q1-Q8 answered; report written)

## Live Tracker
| Step | Check | Started UTC | Updated UTC | Command or observation | Exit | Evidence or result | Next |
|---|---|---|---|---|---:|---|---|
| 1 | Read HANDOFF.md, PLAN.md, PLAN-LUNA.md whole | 09:14 | 09:16 | read_file | 0 | Full contents reviewed; blockers 26/28/43 confirmed | audit analysis |
| 2 | Read __init__.py (1975 lines) | 09:16 | 09:31 | python line-print (ground truth) | 0 | All classes/functions located with exact lines | Q1-Q4 analysis |
| 3 | Read all 11 test files + E2E runner + README + plugin.yaml | 09:16 | 09:28 | read_file + python | 0 | Full test surface inventoried | Q5-Q6 analysis |
| 4 | Scoped git observation (ls-files for release gate) | via test source | 09:33 | read only | 0 | test_public_release checks tracked manifest | Q7 analysis |
| 5 | Compile per-question verdicts L-01..L-08 | 09:30 | 09:40 | analysis | 0 | 8 findings, 0 forbidden commands | write report |
| 6 | Write LUNA-AUDIT-REPORT.md | - | - | write_file | 0 | only allowed write | hand back |

## Findings

### Finding L-01: README claims SDK-swallowed failure distinction that PLAN still flags as unsolved
- Audit question: Q1
- Finding: README line 120-121 says the plugin "distinguishes NO_HIT from timeout, authentication, availability, collection, and malformed-response failures." PLAN.md lines 207-229 (P0-A) state the SDK swallows some gRPC errors into `[]`/`False`/`None` and that "failed mutation semantics are not complete," and classifies NO_HIT-vs-failure separation more strongly than empirically earned. README presents this distinction as a delivered feature while the execution truth marks it open.
- Exact evidence: README.md:120-121; PLAN.md:207-229
- Impact: medium (public over-assertion on a failure-classification guarantee; could mislead an operator into trusting NO_HIT as proof of absence)
- Confidence: high
- Evidence state: SUPPORTED_WITH_SCOPE (both texts read; P0-A explicitly open in PLAN)
- Recommended next action: soften README wording to "classifies errors that escape" and link malformed/swallowed separation to an authorized isolated E2E; align after measured evidence.

### Finding L-02: Swallowed-RPC telemetry path is never exercised by the fake suite
- Audit question: Q5 (and Q2)
- Finding: `_install_deadlines` only wraps stubs when `client.stubs` is a list (__init__.py:400-409). The conftest FakeClient (tests/conftest.py:24-131) defines methods directly and has NO `stubs` attribute and no `_thread_local`. Therefore in every current unit/integration test the `_DeadlineStubProxy` is never installed, `_RpcTelemetry.record` is never called, and `_call`'s swallowed-error detection (__init__.py:994-1002) can never fire. The 85-pass suite proves the surrounding code but does not exercise the P0-A telemetry mechanism it claims to fix.
- Exact evidence: __init__.py:349-416 (telemetry/proxy), __init__.py:994-1002 (consume path); tests/conftest.py:24-131 (no stubs attribute)
- Impact: high (a whole failure-separation control is unit-unproven; real SDK `.stubs` presence is unverified)
- Confidence: high (source evidence for fake surface; real-SDK behavior is outside read-only scope)
- Evidence state: SUPPORTED_WITH_SCOPE (unit side); BLOCKED BY READ-ONLY SCOPE (real SDK `.stubs`/`.stub` attribute shape)
- Recommended next action: add a fake/fixture that models `client.stubs` as a list of raising stubs and assert `_call` re-raises on swallowed error; then verify real `HyperspaceClient.stubs` shape in the isolated E2E (step 43).

### Finding L-03: Malformed nested result rows are silently dropped, not flagged
- Audit question: Q2
- Finding: in `_search_records`, a non-dict element in the search result list is silently skipped (`continue`) and rows with no extractable content are skipped (__init__.py:1132-1154). A partially malformed payload therefore produces a partial/NO_HIT result with no `malformed` signal, rather than failing closed or labeling the malformed subset.
- Exact evidence: __init__.py:1149-1156 (skip non-dict/empty-content rows)
- Impact: low-medium (graceful tolerance vs. silent partial-truth; a caller could infer "no memory" from a response whose rows failed to decode)
- Confidence: high
- Evidence state: SUPPORTED_WITH_SCOPE
- Recommended next action: decide (operator + E2E) whether to count skipped rows and surface `dropped_malformed: N` in the tool envelope instead of silent omission.

### Finding L-04: `trusted_sources` branch is unreachable dead code that would be forgeable if enabled
- Audit question: Q3 (and Q7)
- Finding: `_search_records` implements a `trusted_sources` trust mode where `allowed = authenticated_owner or (source in self._trusted_sources and trusted_claim)` (__init__.py:1168-1170), reading `source`/`trust` directly from point metadata (unauthenticated strings). But `_validate_config` only accepts `owned_only`/`annotate_all` (__init__.py:886-887) and the setup schema choices likewise omit `trusted_sources` (__init__.py:1094), and README lists only the two modes (README.md:67). So the branch is currently unreachable, but it is a latent P0-F-class conflation (forgable source/trust strings) that survives in source and contradicts the plan's required "annotations only" treatment.
- Exact evidence: __init__.py:1165-1174, __init__.py:828-832, __init__.py:886-887, __init__.py:1094; PLAN.md:413-447 (P0-F required trust model)
- Impact: low today (unreachable), medium as latent defect / source-vs-design mismatch
- Confidence: high (source reachability), medium (exploitability only if mode were re-enabled)
- Evidence state: SUPPORTED_WITH_SCOPE
- Recommended next action: remove the dead `trusted_sources` branch or gate it behind the plan's authenticated-owner-only rule; add a test asserting config never accepts `trusted_sources`.

### Finding L-05: FakeClient search/model surface is invented; real-SDK kwarg/return shapes unverified
- Audit question: Q5
- Finding: conftest FakeClient.search accepts kwargs `include_payload`, `use_wasserstein`, `use_wave`, `hybrid_query`, `hybrid_alpha`, `scroll(limit, offset=...)`, etc. (tests/conftest.py:83-102). `_search_records` passes several of these (__init__.py:1130-1144). There is no test that the real `HyperspaceClient` accepts those exact kwargs or returns the expected dict/payload shape. A packaged dependency change or SDK kwarg rename would raise TypeError/KeyError only on a real backend, invisible to the current suite.
- Exact evidence: tests/conftest.py:83-102; __init__.py:1128-1146
- Impact: high (the whole add/replace/remove + payload-search path is unproven against a real SDK contract)
- Confidence: high (fake diverges by construction); real contract = BLOCKED BY READ-ONLY SCOPE
- Evidence state: BLOCKED BY READ-ONLY SCOPE (real backend); SUPPORTED_WITH_SCOPE (fake-surface evidence)
- Recommended next action: in the authorized isolated E2E (step 43) assert full SDK method signatures and response shapes once before trusting the mirror path.

### Finding L-06: E2E runner gates correctly before client construction; state-path location is doc-only
- Audit question: Q6
- Finding: the runner fail-closes on approval, HMAC key, state path, distinct source/target, and `hsdb_e2e_` prefix, all before `client = HyperspaceClient(...)` (tests/run_test_collection_e2e.py:70-88), and test_public_release asserts the ordering (test_public_release.py:96-102). This is correct. However, the "outside this plugin" requirement for `HSDB_E2E_STATE_PATH` is enforced only by wording (runner lines 76-78 check only non-empty), not by a runtime guard against PLUGIN_ROOT.
- Exact evidence: tests/run_test_collection_e2e.py:70-88, 76-78; test_public_release.py:96-102, 119-122
- Impact: low (gates pass test assertions; only a hard-coded path guard is missing)
- Confidence: high
- Evidence state: SUPPORTED_WITH_SCOPE
- Recommended next action: optionally add a runtime check that the resolved state path is not under the plugin dir (operator-facing, not mechanical change).

### Finding L-07: Documented local-suite run times disagree (2.34s vs 3.07s)
- Audit question: Q7
- Finding: PLAN.md tracker row (line 1281) and PLAN-LUNA.md (line 12) record "85 passed in 2.34s", while HANDOFF.md (line 89) records "85 passed in 3.07s". Same count, different durations across documents that claim to describe the current-session PTY result. This is a minor ledger inconsistency, not a correctness contradiction.
- Exact evidence: PLAN.md:1281; PLAN-LUNA.md:12; HANDOFF.md:89
- Impact: low
- Confidence: high (all three texts read)
- Evidence state: SUPPORTED_WITH_SCOPE
- Recommended next action: record one canonical PTY result line (count + time) in both docs at the same update timestamp; do not treat either as fresh proof without labeling run time.

### Finding L-08: sh1fted line-40/43 verdict correctly labels blockers as NECESSARY evidence, not merely operational
- Audit question: Q8
- Finding: blockers 26, 28, 43 are framed as required evidence for any production-ready claim: HANDOFF.md:22-23 states fake/static tests "cannot establish payload response shape, calibrated Lorentz relevance behavior, or real add/replace/remove behavior"; HANDOFF.md:117-131 and PLAN.md:203-359 tie each to a measured gate. No document treats them as optional operational polish. No mis-framing found.
- Exact evidence: HANDOFF.md:22-23, 117-131; PLAN.md:203-359, 1161-1240 (tracker rows with BLOCKED/NOT_E2E_VERIFIED)
- Impact: n/a (no defect; compliance confirmed)
- Confidence: high
- Evidence state: SUPPORTED_WITH_SCOPE
- Recommended next action: none for correctness; keep the verdict until an isolated authorized E2E supplies the three missing evidence classes.

## No-Finding Results
- Q1: README is otherwise honest (README:11-13 does not claim E2E/production; README:96-98 disclaims ACID; README:184-193 lists honest limitations; README:107-108 and test_public_release.py:48-52 verify the "no automatic replay" disclosure). Single over-assertion captured in L-01.
- Q2: Contract checks are generally fail-closed (non-list responses raise BackendMalformed at __init__.py:1132, 1145-1146, 1300-1302, 1356-1359, 1505-1507; empty-response health raises at 1021-1023; redacted errors 1161-1167, 173-193). The two gaps are L-02 (swallowed path unexercised) and L-03 (silent row skip).
- Q3: HMAC ownership is sound where reachable: `_point_owner_matches` demands owner+digest+profile+signature (__init__.py:1275-1289); `_ownership_signature` covers canonical fields with constant-time compare (1267-1273); rotation allowlist bounded (1282-1288, 849-854); metadata reserved/`user.` namespacing (104-110, 1317-1331, 295-311); collection override denied (106/1094, 1739-1744, tool allowlist 46-55, 1922-1925). Only latent issue is dead `trusted_sources` (L-04).
- Q4: Rotation/shutdown/lease design is well-guarded: inflight refcount (859-860, 946-982, 955-967), retired-clients deferral, SHUTDOWN_TIMEOUT/SHUTDOWN_INFLIGHT preserve ledger+client (1941-1970), barrier tests cover rotation/shutdown during a blocked RPC (test_lifecycle.py:180-227), worker-alive ledger guard (test_p0_red_regressions.py:213-232). Ledger writes and snapshot_to share one RLock (438-511, 636-654) so reconcile/worker/snapshot serialize. No uncovered race found in read-only scope; cross-thread interleaving beyond these is untestable here.
- Q6: Approval/HMAC/state/source/target/prefix gates all precede client construction and are asserted by test; only doc-only state-path guard noted in L-06.
- Q7: Beyond L-04/L-07, tracker state is mutually consistent: HANDOFF (40/43, blocked 26/28/43), PLAN tracker rows (26/28/43 BLOCKED / NOT_E2E_VERIFIED), README version 0.2.0 == plugin.yaml, dependency string matches both, and E2E runner env names match README and tests.
- Q8: see L-08 (no mis-framing).

## Stop Condition And Limits
- Real backend / E2E: NOT RUN. `tests/run_test_collection_e2e.py` was audited by source only, never executed.
- Production verdict: NOT ASSESSED by this audit; the existing `not production ready` verdict is preserved (no evidence here changes it).
- Unresolved evidence (BLOCKED BY READ-ONLY SCOPE): real `HyperspaceClient` `.stubs`/`.stub` and `_thread_local` attribute shapes (L-02), real SDK search/scroll kwarg and return/payload shapes (L-05), real add/replace/remove + payload shape + relevance distance distribution (blockers 26/28/43 per plan), and whether the local 2.34 vs 3.07s discrepancy is more than timing jitter.

## Final Audit Verdict
This read-only audit found no production-ready evidence; it confirms the existing `not production ready` verdict, flags an over-asserting README claim (L-01), an unexercised swallowed-RPC telemetry path (L-02), a silent-malformed-row skip (L-03), and a latent dead `trusted_sources` trust-conflation branch (L-04), each waiting on authorized isolated E2E evidence before the mirror path can be certified.