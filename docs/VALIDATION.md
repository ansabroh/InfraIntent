# Validation report

Run date: 2026-11-26.

- GenVM linter 0.11.0: safety lint and pinned SDK semantic validation passed.
- ABI extraction: nine public methods, including six writes and three reads; no constructor parameters.
- 50 direct-mode tests passed using genlayer-test 0.29.2 with the actual GenVM SDK/storage, mocked web responses and mocked model reasoning.
- Covered all outcomes, role separation, permissionless assessment, duplicate assessment rejection, one-dispute rule, revision bounds, immutable policy, commit/path restrictions, unavailable/tampered evidence, quote grounding, complete semantic coverage, independent validator disagreement, decision hashes and full event-chain recomputation.

Direct-mode execution does not reproduce network scheduling, transaction finality, model quality, transport behavior or multi-node consensus. Live deployment results are recorded separately in DEPLOYMENT.md. A pinned SDK runner update advisory is informational and does not fail validation. Upgrading the runner requires rerunning tests and redeploying.

## Live network verification

Final contract `0x02acA2373A0FB3e702Ee1da864244d568C158963` completed deployment, create, lock, submit, assess, dispute and adjudicate using Studio Normal (Full Consensus), simulation disabled. All seven transactions finalized SUCCESS/Accepted. The semantic model review produced COMPLIANT with three grounded PASS rows; deterministic adjudication of replacement evidence produced DRIFT. All six exported lifecycle events and both decision hashes were recomputed and matched the on-chain head. See [deployment details](DEPLOYMENT.md) for exact transaction links and [live history](../evidence/live-events.json) for the preserved receipts.

These live checks use synthetic fixtures; they establish lifecycle execution and consensus, not compliance of an actual cloud deployment. CONDITIONAL and INCONCLUSIVE are covered by direct-mode tests, not claimed as separately executed live outcomes.
