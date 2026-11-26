# InfraIntent

**Infrastructure configuration compliance verification on GenLayer.**

InfraIntent locks an approved architecture and its security requirements, verifies commit-pinned deployment evidence, and records append-only assessments. It never applies Terraform, changes Kubernetes, or controls cloud deployments.

## Outcomes

| Outcome | Exact rule |
|---|---|
| COMPLIANT | Complete deterministic facts, coherent raw artifacts, and PASS on every semantic requirement |
| CONDITIONAL | Only advisory semantic requirements fail; all hard requirements pass and evidence is complete |
| DRIFT | A deterministic violation, or independently agreed FAIL on a hard semantic requirement |
| INCONCLUSIVE | Missing/unverifiable evidence, unknown facts, incoherent normalization, UNKNOWN semantic results, or agreed model unavailability |

Known deterministic violations take precedence over unknown evidence. Consensus disagreement rejects the candidate transaction; it does not manufacture an INCONCLUSIVE receipt. A network execution failure leaves committed state unchanged.

## What makes GenLayer central

A custom `gl.vm.run_nondet_unsafe` leader/validator pair compares the locked baseline with observed Terraform, Kubernetes and audit artifacts. Each validator independently runs the review; every requirement status and the artifact-coherence decision must agree. Exact quotation grounding and complete requirement coverage are enforced in code. Validators do not accept a leader merely because it returned correctly formatted JSON.

Deterministic checks enforce private exposure policy, encryption and integer CPU/memory limits. A model cannot override these violations. Fetching uses strict equality on normalized, hash-verified evidence; open-ended model prose is never compared using strict equality.

## Lifecycle

1. `create(repository, policy_json, baseline_json, submitter, reviewer)` creates a case; the caller owns it. All addresses and requirements are immutable.
2. `lock(case_id)` is owner-only. The commit-pinned baseline must be accessible, schema-valid and satisfy deterministic constraints.
3. `submit(case_id, evidence_json)` is owner/submitter-only. A maximum of 16 revisions prevents unlimited per-case growth.
4. `assess(case_id)` is permissionless and assesses only the committed submission.
5. `dispute(case_id, evidence_json, reason)` is owner/reviewer-only, once per revision. It records replacement evidence without overwriting the original receipt.
6. `adjudicate(case_id)` is permissionless and independently reassesses the disputed evidence against the original locked policy/baseline.
7. `get_case`, `get_event`, and `get_count` expose state, receipts and hash-linked history.

A new submission after assessment creates the next revision. Dispute and protocol-level GenLayer appeals are distinct mechanisms. Locking is explicit consent to the fixed policy; there is no editing or administrator override.

## Run verification

Python 3.12+:

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
genvm-lint check contracts/infra_intent.py
genvm-lint schema contracts/infra_intent.py
python -m pytest tests -q
```

The tests execute the real GenVM Python SDK and storage in direct mode with mocked web/LLM responses. They do not establish live multi-validator network consensus. The pinned SDK runner is tested explicitly; the linter may report that a newer runner exists.

## Evidence format

See [EVIDENCE.md](docs/EVIDENCE.md). Every bundle contains raw Terraform, Kubernetes and audit text plus a bounded normalized inventory. This is a narrow evidence protocol, not a general Terraform interpreter or Kubernetes admission controller. Unknown settings must use `null`, never an invented safe default. Semantic validators must verify normalization against the raw artifacts before a clean assessment is possible.

All fixtures are synthetic examples, not authenticated cloud exports. Content hashes prove byte integrity, not the truth, freshness, provenance or completeness of an operator's snapshot. Integrations must establish those properties separately. Never publish secrets from Terraform state or Kubernetes manifests.

## Documentation

- [Deployment and Studio walkthrough](docs/DEPLOYMENT.md)
- [Evidence schema and hash verification](docs/EVIDENCE.md)
- [Security model](SECURITY.md)
- [Validation report](docs/VALIDATION.md)
- [Submission description](docs/SUBMISSION.md)

## Official references

Implementation checked against the [Equivalence Principle](https://docs.genlayer.com/developers/intelligent-contracts/equivalence-principle), [Calling LLMs](https://docs.genlayer.com/developers/intelligent-contracts/features/calling-llms), [SDK reference](https://sdk.genlayer.com/), and [direct-mode testing](https://docs.genlayer.com/api-references/genlayer-test/direct). Where prose docs differ, the pinned SDK is authoritative (its HTTP response field is `status`).
