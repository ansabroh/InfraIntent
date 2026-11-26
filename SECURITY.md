# Security model

## Trust boundaries

InfraIntent is an evidence assessment contract. It cannot authenticate a cloud environment, prevent a snapshot from omitting facts, or guarantee an LLM's judgment. A commit SHA and SHA-256 bind exact evidence bytes; they do not certify the operator's assertions. Obtain provenance/freshness through a separately authenticated exporter and audit process. Public fixture audits explicitly identify themselves as operator-supplied synthetic evidence.

A case owner fixes the repository, submitter, reviewer, baseline and policy at creation. Only the owner can lock. Owner/submitter may submit revisions; owner/reviewer may dispute once per revision. Anyone can pay to assess/adjudicate already committed inputs. There is no privileged outcome setter, token transfer, shell execution, deployment mutation or contract upgrade path.

## Defensive controls

- Fixed GitHub raw host; constructed URLs; full commit SHA; restricted paths; no caller-controlled domains or follow-up browsing.
- Exact HTTP status, byte length and SHA-256 checks before parsing; strict schemas, duplicate-key rejection, bounded strings and arrays; no float/bool coercion for integer limits.
- Resource limits, exposure and encryption checked deterministically. A detected violation dominates missing/unknown evidence and cannot be changed by the model.
- Raw artifacts separated inside JSON under an explicit untrusted-data prompt. Embedded instructions, URLs and claimed verdicts are not authority.
- Requirement coverage and quote grounding validated on both leader and validator candidates. Validators independently reason and agree on every status/coherence field.
- Two bounded prompt attempts per node; malformed responses fail closed. Disagreement rejects consensus; no forced agreement or success fallback.
- No storage access inside nondeterministic closures: only pre-copied JSON inputs are captured. State writes occur after consensus.
- Append-only event records and hash-linked receipts; one dispute and up to 16 revisions per case. The historical receipt survives a dispute.

## Limits

Response size checks occur after the SDK fetch, not as a streaming download cap; network timeouts, redirect policy, response allocation and gas are also constrained by the GenVM provider/runtime. The contract never deliberately follows a URL supplied in evidence; it cannot override provider transport implementation. Assessments are scoped to normalized bundle fields and the locked semantic requirements, not every cloud control. CPU/memory units and workload aggregation must be prepared correctly by the evidence exporter. Raw Terraform and Kubernetes are reviewed as text, not executed or deterministically interpreted. A compromised or colluding evidence producer can supply consistent false artifacts. Model prompt-injection resistance is a defense, not a proof.

Permissionless creation can grow global state subject to network transaction fees; per-case bounds do not create a global quota. There is no application dispute deadline or chain clock dependency. Repeated evidence may be assessed as a new revision; within the same revision, repeated assess/adjudicate is rejected by state transitions. A later revision intentionally permits a fresh review under the same immutable policy.

Report suspected vulnerabilities privately to the repository owner through GitHub's available private reporting channel; do not include live secrets in public issues.
