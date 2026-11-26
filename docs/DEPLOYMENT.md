# Deployment

Upload `contracts/infra_intent.py` to [GenLayer Studio](https://studio.genlayer.com/contracts). It is self-contained and needs no constructor arguments, backend, external API keys or private-key export. Select the Studio built-in wallet and deploy. Wait for successful finalization, then verify `get_count()` returns 0 and inspect the method schema.

For a full lifecycle, publish the fixture bundle files to a commit first. Run `scripts/descriptor.py` with that full commit SHA. Call `create` with repository `ansabroh/InfraIntent`, the policy JSON string, baseline descriptor JSON string, and chosen submitter/reviewer addresses. Read the returned case ID. Then call `lock`, `submit` with the observed descriptor, and `assess`. Inspect `get_case` and every `get_event`. Dispute with a replacement evidence descriptor as the owner/reviewer and call `adjudicate` to retain both assessments.

Use the synthetic fixtures for development only. For real use replace the complete baseline, inventory, raw plans/manifests and audit data with appropriately redacted, authenticated exports. Changing policy or baseline requires a new case.

## Deployment record

Live deployment verification is recorded here after execution. No contract address or successful network consensus is implied by local tests alone.
