# Evidence protocol

## Locked policy

`fixtures/policy.json` is a complete example. Exact keys are mandatory; unknown fields and duplicate JSON keys are rejected.

- `environment`: nonempty scope identifier, maximum 120 characters.
- `required_ids`: 1–32 unique resource IDs; each at most 120 characters.
- `allowed_public_ids`: unique subset of required IDs. Public resources outside this subset cause DRIFT.
- `require_encryption`: strict boolean.
- `max_cpu_millis`, `max_memory_mib`: positive integers, at most 1,000,000. Applied to every scoped normalized resource.
- `requirements`: 1–12 objects with unique `id` (40 characters), `text` (800 characters), and `severity` (`hard` or `advisory`).

Canonical policy encoding must fit 10,000 bytes. Policy hashes are SHA-256 over canonical ASCII JSON: sorted keys, compact separators, `ensure_ascii=True`.

## Baseline and observed bundle

Exact keys:

```json
{
  "environment": "production-eu",
  "resources": [
    {"id":"api","public":false,"encrypted":true,"cpu_millis":1000,"memory_mib":1024}
  ],
  "terraform": "Exact approved configuration / plan text",
  "kubernetes": "Exact scoped manifests and relevant policies",
  "audit": "Scoped inventory, audit findings and provenance information"
}
```

The original UTF-8 JSON must fit 24,000 bytes. The normalized fetch-result wrapper must also fit 24,000 bytes, so leave encoding overhead headroom. Raw artifact fields must each be nonempty and at most 12,000 characters. Resources must contain 1–32 unique IDs. Numeric values are strict integers (zero is allowed in evidence), at most 1 billion. Booleans and limits may be `null` to declare unknown facts.

Use public=true if **any** relevant interface, ingress, host network, address family or public service exposes a resource. Aggregate limits conservatively across all scoped workload containers. Never infer encryption from absent attributes. Extra resources are DRIFT; absent required resources are unknown, because absence in a snapshot does not prove deletion.

Baseline deterministic facts must all be known and satisfy the policy before locking. Semantic baseline compliance is reviewed during assessment; lock alone does not certify semantic approval. Raw text and audit integrity remain the operator's responsibility. The model checks that the normalized inventory agrees with raw artifacts; it cannot independently authenticate a cloud account.

## Commit descriptor

```json
{"commit":"<40 lowercase hex characters>","path":"fixtures/compliant.json","sha256":"<64 lowercase hex characters>","bytes":1234}
```

The case fixes one GitHub `owner/repository`. URLs are built only as `https://raw.githubusercontent.com/{repository}/{commit}/{path}`. Branches, tags, query strings, percent escapes, credentials, absolute paths and dot path segments are rejected. There is one HTTP GET per evidence reference per node, no recursive browsing or execution. HTTP 200, exact byte count, SHA-256, UTF-8 decoding, JSON schema and environment must all pass. A transport/provider failure or malformed evidence cannot become COMPLIANT.

To prepare a descriptor from committed file bytes:

```sh
python scripts/descriptor.py FULL_COMMIT_SHA fixtures/baseline.json
python scripts/descriptor.py FULL_COMMIT_SHA fixtures/compliant.json
```

Do not hash reformatted JSON after uploading: the descriptor hashes the exact file bytes, including its final newline. No live secret or account credentials belong in an evidence bundle.

## Review and receipt verification

Every semantic row contains a requirement ID, PASS/FAIL/UNKNOWN, baseline/observed source, and a nonempty exact quote from an artifact. PASS must cite observed evidence. Validators independently classify each requirement and coherence; quotes may differ but both candidates must pass grounding validation. A quote's presence does not prove entailment, which remains a semantic validation responsibility.

A decision hash covers the complete receipt excluding `decision_hash`. An event hash covers the complete event excluding `hash`; each event includes the prior event hash, actor, case ID and sequence. Verify from sequence 0 through `get_case(...).events - 1`, and compare the final hash with the case head. Chain integrity does not prove an assessment correct; it makes the committed history auditable.
