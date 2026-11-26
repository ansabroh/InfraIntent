# Validation report

Run date: 2026-11-26.

- GenVM linter 0.11.0: safety lint and pinned SDK semantic validation passed.
- ABI extraction: nine public methods, including six writes and three reads; no constructor parameters.
- 44 direct-mode tests passed using genlayer-test 0.29.2 with the actual GenVM SDK/storage, mocked web responses and mocked model reasoning.
- Covered all outcomes, role separation, permissionless assessment, duplicate assessment rejection, one-dispute rule, revision bounds, immutable policy, commit/path restrictions, unavailable/tampered evidence, quote grounding, complete semantic coverage, independent validator disagreement, decision hashes and full event-chain recomputation.

Direct-mode execution does not reproduce network scheduling, transaction finality, model quality, transport behavior or multi-node consensus. Live deployment results are recorded separately in DEPLOYMENT.md. A pinned SDK runner update advisory is informational and does not fail validation. Upgrading the runner requires rerunning tests and redeploying.
