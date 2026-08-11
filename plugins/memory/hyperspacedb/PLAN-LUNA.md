# LUNA READ-ONLY ADVERSARIAL AUDIT PLAN

## 1. Mission

Independently audit current HyperspaceDB Hermes memory-provider code and execution plan. Find real remaining risks, false confidence, inconsistent evidence, unsafe assumptions, or plan/code mismatches.

This is an adversarial review. It is not implementation work, remediation work, release approval, E2E execution, or a second copy of the base plan.

Current evidence boundary:

- Current local fake/static suite: 85 passed in 2.34s through PTY.
- Strict real-backend add/replace/remove E2E: not tested.
- Base gates 26, 28, and 43: blocked.
- Current verdict: not production ready.

Do not upgrade any verification level or production verdict.

## 2. Scope

Read only files under PLUGIN_ROOT. Write only one new file:

`LUNA-AUDIT-REPORT.md`

Do not write any other file, including this plan.

## 3. Forbidden Actions

Never:

- edit `__init__.py`, `PLAN.md`, `PLAN-LUNA.md`, `HANDOFF.md`, `README.md`, `plugin.yaml`, `AUDIT.md`, `PROMPT_ITERATIONS.md`, tests, or any shared implementation/documentation file;
- edit, create, delete, rename, clean, format, or restore runtime state, caches, SQLite files, fixtures, collections, branches, commits, or configuration;
- read `.env`, secret files, shell profiles, credentials, private runtime files, or external collections;
- invoke `tests/run_test_collection_e2e.py`, any real E2E path, any mutation API, any provider setup/configuration command, or any command that imports a credential or contacts a backend;
- run pytest, a build, a formatter, a compiler, a package installer, a dev server, or any command that can create cache/state outside `LUNA-AUDIT-REPORT.md`;
- start optional A1-A8 work;
- claim code is fixed, works, E2E tested, or production ready.

If an audit question needs forbidden evidence, record `BLOCKED BY READ-ONLY SCOPE` with the exact missing evidence. Do not work around it.

## 4. Required Reading Order

Read whole files in this order before audit analysis:

1. `HANDOFF.md`
2. `PLAN.md`
3. `PLAN-LUNA.md`
4. `__init__.py`
5. `tests/conftest.py`
6. `tests/test_baseline_contract.py`
7. `tests/test_mutation_semantics.py`
8. `tests/test_mutation_recovery.py`
9. `tests/test_retrieval.py`
10. `tests/test_security.py`
11. `tests/test_lifecycle.py`
12. `tests/test_hermes_contract.py`
13. `tests/test_public_release.py`
14. `tests/test_ledger_migrations.py`
15. `tests/test_p0_red_regressions.py`
16. `tests/run_test_collection_e2e.py`
17. `README.md`
18. `plugin.yaml`

Use read-only inspection only. Line-numbered evidence must come from these files or a scoped read-only Git observation.

## 5. Audit Questions

Answer each question separately. Do not merge findings.

Q1. Does any current source, test, README, or PLAN wording claim a verification level stronger than its direct evidence supports, especially around strict E2E, payload shapes, relevance calibration, and production readiness?

Q2. Does `__init__.py` preserve fail-closed behavior when an SDK response shape is missing, malformed, partial, swallowed after an RPC failure, or contains untrusted nested data? Identify exact branch-level evidence or an unproven gap.

Q3. Can authentication, HMAC ownership, signature rotation, provenance, trust, quarantine, and relevance be confused by a caller or remote record despite existing checks? Focus on a concrete bypass condition, not generic security advice.

Q4. Can client generation rotation, in-flight RPC leasing, queue shutdown, SQLite ledger use, reconciliation, or snapshot creation race in a way not covered by current tests? Identify exact state transition and missing test evidence.

Q5. Do tests prove claimed behavior, or do fake-client assumptions risk diverging from real SDK/server response shapes? Separate unit/integration evidence from live-backend evidence. Do not infer runtime behavior from a mock.

Q6. Does `tests/run_test_collection_e2e.py` fail closed before all client construction and mutation when approval/isolation inputs are absent or malformed? Audit source only. Do not execute it.

Q7. Are PLAN.md tracker state, HANDOFF.md status, README claims, plugin manifest, source behavior, and current test boundary mutually consistent? Identify contradictions with exact lines.

Q8. Is any remaining base blocker 26, 28, or 43 incorrectly framed as merely operational rather than necessary evidence for a production-ready claim?

## 6. Required Report Contract

Create only `LUNA-AUDIT-REPORT.md`. Update it live after every completed review step. A final bulk update is forbidden.

Use this exact structure:

```markdown
# LUNA READ-ONLY ADVERSARIAL AUDIT REPORT

## Scope And Evidence Boundary
- Files read: ...
- Commands run: ...
- No-write verification: ...
- Forbidden actions not run: ...

## Current Execution State
- Active step: ...
- Last updated UTC: ...
- Result status: IN_PROGRESS | COMPLETE | BLOCKED

## Live Tracker
| Step | Check | Started UTC | Updated UTC | Command or observation | Exit | Evidence or result | Next |
|---|---|---|---|---|---:|---|---|

## Findings
### Finding L-01: <short title>
- Audit question: Q<n>
- Finding: <atomic claim>
- Exact evidence: `<relative path>:<line or line range>`
- Impact: critical | high | medium | low
- Confidence: high | medium | low
- Evidence state: SUPPORTED_WITH_SCOPE | PARTIAL | INCONCLUSIVE | BLOCKED BY READ-ONLY SCOPE
- Recommended next action: <specific safe action, or explicit E2E gate>

## No-Finding Results
- Q<n>: <what was checked and why no finding was earned>

## Stop Condition And Limits
- Real backend/E2E: NOT RUN
- Production verdict: NOT ASSESSED; existing not-production-ready verdict preserved
- Unresolved evidence: ...

## Final Audit Verdict
- <one sentence, bounded by evidence>
```

Rules:

- Every finding needs exact evidence path and line range.
- Every statement about runtime behavior must distinguish source/test evidence from real-backend evidence.
- Do not cite historical test counts as fresh proof without labeling them historical; the plan's 85-pass result is current session evidence but not Luna-run evidence.
- Do not copy secret-like values, record contents, absolute private paths, collection names, or stack traces.
- Use ASCII only.
- Do not emit unsupported severity. `critical` requires a credible direct exploit, destructive path, or correctness failure supported by source evidence.
- Findings must be atomic. One finding, one failure mode.

## 7. Success Definition

Success means:

- all required files read;
- each Q1-Q8 answered separately;
- every finding has exact line evidence, impact, confidence, evidence state, and next action;
- no forbidden command/action occurred;
- only `LUNA-AUDIT-REPORT.md` changed;
- report preserves `not production ready` and does not start A1-A8.

## 8. Stop Conditions

Stop immediately and write a bounded report if:

- any requested proof needs a real backend, credential, private environment file, external collection, mutation, or E2E run;
- command would write outside `LUNA-AUDIT-REPORT.md`;
- source data is insufficient to support a finding;
- all Q1-Q8 are answered with evidence or explicit blocked status.

Do not ask for permission to extend scope. Mark the exact evidence gap instead.
