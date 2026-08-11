# FIVE ITERATIONS OF THE AUDIT-AND-HARDENING PROMPT

## Iteration 1

Audit the Hermes HyperspaceDB memory provider brutally. Compare its behavior with current Hermes MemoryProvider and HyperspaceDB SDK contracts. Find correctness, safety, lifecycle, and packaging defects.

## Iteration 2

Independently audit the provider as a hostile reliability reviewer. Treat previous reviews as hypotheses. Prove every claim with source locations or executable tests. Focus on add/replace/remove semantics, uint32 identity collisions, payload extraction, real RPC deadlines, failure-vs-no-hit behavior, and client shutdown.

## Iteration 3

Audit and harden the provider as a public plugin, not a private script. Reject user-specific paths, collection names, credentials, trust assumptions, or stack references. Build red tests first. Model partial failures, retries, ambiguous old_text matching, key rotation, mixed-producer collections, prompt injection, bounded retrieval, backup consistency, and compatibility drift.

## Iteration 4

Produce a fail-closed implementation only after the evidence ledger is complete. Preserve ordered memory mutations through a persistent identity ledger. Collision-check every uint32 ID, verify writes and deletes, distinguish backend failures from empty search results, use actual gRPC deadlines, close channels, reserve metadata, quarantine automatic prefetch, and deny collection override by default. Never write to production during tests.

## Iteration 5

Execute an adversarial, contract-driven release audit of the exact public Hermes MemoryProvider plugin. Requirements: neutral configuration; no private paths or names; executable red-green tests; real Hermes loader compatibility; HyperspaceDB payload interoperability; deterministic add/replace/remove with reconciliation; strict provenance and trust boundaries; bounded tool surface; honest backup semantics; read-only live integration; secret scan; final P0-P3 ledger; and an explicit verification level. Do not call it production-ready unless unit, contract, integration, and authorized E2E mutation tests all pass.
