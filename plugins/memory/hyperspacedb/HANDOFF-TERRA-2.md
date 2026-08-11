# HANDOFF TERRA 2 - HYPERSPACEDB MEMORY PROVIDER

Status date: 2026-08-11
Scope token: PLUGIN_ROOT
Plan authority: PLAN.md

## 1. Read Order

Before any write, read whole files in this order:

1. HANDOFF-TERRA-2.md
2. PLAN.md
3. HANDOFF.md
4. PLAN-LUNA.md
5. LUNA-AUDIT-REPORT.md

Then inspect scoped Git state. Do not trust historical tracker counts without a fresh PTY test result.

## 2. Non-Negotiable Scope

Write only under PLUGIN_ROOT.

Never modify Hermes core, configuration, SDK/server code, other plugins, staging repositories, production data, private environment or secret files, or anything outside PLUGIN_ROOT.

Never delete files, runtime state, caches, fixtures, collections, or Git state. Never use reset, clean, checkout discard, or a broad Git add.

Do not run a real E2E, collection mutation, provider setup, or credential-loading command without a new literal `approved` plus isolated runtime-only inputs. Do not start A1-A8.

Use PTY for Python compile and pytest evidence. Keep all fresh test state under PLUGIN_ROOT/state and never reuse or delete an old test directory.

## 3. Current Verified Evidence

- Full local plugin suite, PTY: 89 passed in 2.28s.
- L6 targeted release/source-contract suite, PTY: 16 passed in 1.51s.
- L6 guard observed: rejects empty, relative, and in-plugin E2E state paths; accepts an external absolute path; guard runs before HyperspaceClient construction.
- L6 RED phase was not witnessed because runner/test changes existed before Terra encountered them. Do not claim test-first proof for L6.
- No E2E runner, backend, credential, collection, or production-data action was run in this session.
- Current verdict: not production ready.
- Strict E2E gates 26, 28, and 43 remain blocked.

## 4. Current Scoped Git State

Observed before this handoff file was created:

Tracked modified files:

- PLAN.md
- tests/run_test_collection_e2e.py
- tests/test_public_release.py

Untracked documentation files:

- PLAN-LUNA.md
- LUNA-AUDIT-REPORT.md

The L6 runner/test diff was already present when Terra attempted to start it. It was inspected and tested, but source/test authorship is not attributed to this session. Do not overwrite or blindly commit it. Review it first, retain only evidence-backed scope, then selectively stage it with the final approved plugin change.

## 5. Luna Audit Triage

Accepted:

- L-03: malformed nested search rows are silently skipped. Low-severity observability gap; no patch started.
- L-04: unreachable trusted_sources policy branch relied on forgeable metadata if ever re-enabled. Static cleanup authorized and paused before RED.
- L-06: E2E state path boundary was missing. Existing L6 diff now provides local test evidence.
- L-05 restates existing real-SDK and E2E blockers, not a new local task.

Rejected:

- L-01: plan historical section was misread as current state; tracker remains authoritative.
- L-02: test_p0_red_regressions.py exercises the swallowed-RPC stub telemetry path.
- L-07: 3.07s and 2.34s came from separate PTY runs.
- L-08 found no defect.

## 6. Active Next Task: L4 Dead Trust-Policy Removal

PLAN.md row L4-1 is PAUSED_FOR_HANDOFF, not complete.

Exact write scope for L4:

- PLAN.md
- __init__.py
- tests/test_public_release.py

No L4 source/test patch landed. A malformed patch invocation returned `patch content required`; it modified no file. The intended L4 test is absent.

### Required TDD sequence

1. Update PLAN.md first: L4-1 back to `[>] IN_PROGRESS`, with current UTC time, exact scope, and RED acceptance command.
2. In tests/test_public_release.py add one public-surface contract test:

```python
def test_provider_has_no_dead_trusted_sources_policy():
    source = (ROOT / "__init__.py").read_text(encoding="utf-8")
    assert "trusted_sources" not in source
```

3. Run only that test through PTY with bytecode and pytest cache writes disabled. It must fail because __init__.py still contains trusted_sources. Record exact exit and failure in PLAN.md immediately.
4. Make minimal source-only removal in __init__.py:
   - remove trusted_sources configuration/default state;
   - remove trusted_claim calculation;
   - remove the `elif self._trust_mode == "trusted_sources"` branch;
   - make fallback error wording match only accepted modes, owned_only and annotate_all.
   Preserve source and trust metadata fields used for result provenance.
5. Run the targeted test through PTY. It must pass.
6. Run full plugin suite through PTY with a fresh in-scope basetemp. Record actual count/time.
7. Inspect scoped diff and run `git diff --check` before closing L4-1. Do not claim E2E.

## 7. Git Gate: Mandatory, Selective

Do not forget Git. Do not commit before L4 verification and scoped diff review.

After L4 passes:

1. `git status --short -- .`
2. `git diff --check -- .`
3. `git diff --name-only -- .`
4. Review every planned file. Never stage state, cache, secret, config, SDK, core, or other-plugin content.
5. Selectively stage only approved plugin files, for example:

```text
git add -- PLAN.md __init__.py tests/run_test_collection_e2e.py tests/test_public_release.py HANDOFF-TERRA-2.md
```

Do not stage PLAN-LUNA.md or LUNA-AUDIT-REPORT.md until their public-release role is deliberately reviewed. They are currently untracked and must remain preserved.

6. Verify staged scope:

```text
git diff --cached --name-only
git diff --cached --check
```

7. Commit only if staged scope matches the reviewed plugin files. Suggested message:

```text
fix: harden hyperspacedb e2e preflight
```

A commit records a reviewed snapshot. It does not upgrade E2E or production verification.

## 8. Strict E2E Boundary

Do not run tests/run_test_collection_e2e.py unless the user newly provides literal `approved` and isolated runtime-only values for the required E2E inputs. Never print those values or read secret files. Before any real call, update step 43 to `[>]`, inspect source/target read-only, verify Lorentz 129D, and keep all fixture content out of output.

Without that authorization, retain:

```text
not production ready
```

## 9. Handoff Completion Rule

Update PLAN.md after every patch or test. Append failures and decisions; never erase prior evidence. At final response, state actual test result, committed or uncommitted Git state, active blocker, and earned verification level only.
