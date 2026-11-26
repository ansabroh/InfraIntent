# Deployment

Upload `contracts/infra_intent.py` to [GenLayer Studio](https://studio.genlayer.com/contracts). It is self-contained and needs no constructor arguments, backend, external API keys or private-key export. Select the Studio built-in wallet and deploy. Wait for successful finalization, then verify `get_count()` returns 0 and inspect the method schema.

For a full lifecycle, publish the fixture bundle files to a commit first. Run `scripts/descriptor.py` with that full commit SHA. Call `create` with repository `ansabroh/InfraIntent`, the policy JSON string, baseline descriptor JSON string, and chosen submitter/reviewer addresses. Read the returned case ID. Then call `lock`, `submit` with the observed descriptor, and `assess`. Inspect `get_case` and every `get_event`. Dispute with a replacement evidence descriptor as the owner/reviewer and call `adjudicate` to retain both assessments.

Use the synthetic fixtures for development only. For real use replace the complete baseline, inventory, raw plans/manifests and audit data with appropriately redacted, authenticated exports. Changing policy or baseline requires a new case.

## Deployment record

Date: 2026-11-26. Network: GenLayer Studio. Studio built-in wallet, Normal (Full Consensus), simulation disabled.

**Current contract:** [0x02acA2373A0FB3e702Ee1da864244d568C158963](https://explorer-studio.genlayer.com/address/0x02acA2373A0FB3e702Ee1da864244d568C158963).

Source commit: `5ca4f55cd31ee53bb98444bceae4ab203598f31d`. Exact source SHA-256 is in [deployment.json](../evidence/deployment.json). Evidence fixtures are bound to the earlier immutable commit `333f382e1cf2f9bb2db794611450563e0cbca0ce`.

Deployment, create, lock and submit were executed and observed reaching consensus. Case `0` uses synthetic fixture evidence; it makes no assertion about a real cloud deployment. Submitter and reviewer are hexadecimal string addresses, normalized and validated on-chain. Use plain hex strings in Studio's typed text inputs.

[GitHub CI](https://github.com/ansabroh/InfraIntent/actions/runs/45783552866) passed lint, SDK validation, ABI extraction and 50 direct-mode tests.

The earlier instance `0x3776EF9DB271128ccF420Bf048FC8a2c83975472` is superseded. It detected deterministic exposure/encryption drift in case 0; final deployment adds explicit role-address validation/normalization so malformed calldata cannot silently create unusable roles.

## Finalized full lifecycle

All seven transactions were independently observed on the public explorer as **FINALIZED**, **SUCCESS**, consensus **Accepted**:

| Operation | Transaction |
|---|---|
| deploy | [0xff105dc757…](https://explorer-studio.genlayer.com/tx/0xff105dc757b25cd0debb1b3e2856d62989912fb7862c97e685be13413754f5aa) |
| create | [0xd3946abb57…](https://explorer-studio.genlayer.com/tx/0xd3946abb57d619c142d992cf3c3708a3872f1fda1e4b3fb22a70bcb276eff82b) |
| lock | [0xf51e07b65f…](https://explorer-studio.genlayer.com/tx/0xf51e07b65fbacc800803d32d99d998ed2d2343652d30e8e6dec7eeffc623ba71) |
| submit | [0xcb7ce05bb4…](https://explorer-studio.genlayer.com/tx/0xcb7ce05bb4014764cc5e8f650dbd10b67cf4e2b4d7b0294f1bad8e6ce025dbad) |
| assess | [0x7b8a7c535b…](https://explorer-studio.genlayer.com/tx/0x7b8a7c535bbbee22d0347a5c97933ed44a0e330117b4beb50e1990e22696d2fc) |
| dispute | [0x0bf42a1ad6…](https://explorer-studio.genlayer.com/tx/0x0bf42a1ad6584ab7943c2249daaac4ea4733da79c0130f8e77389367d9f28009) |
| adjudicate | [0xa815dcbc2e…](https://explorer-studio.genlayer.com/tx/0xa815dcbc2e15cd69fb9b4193501caaf669601670cc85ae93952b4c44320b0704) |

Initial semantic assessment: **COMPLIANT**, all three requirements PASS with observed artifact quotes and coherent inventory. A disputed follow-up snapshot then produced **DRIFT** for public exposure and disabled encryption. The previous COMPLIANT receipt remains event 3; the adjudication is event 5. Final case state is ASSESSED with six hash-linked events.

The exported [live case](../evidence/live-case.json), [full event history](../evidence/live-events.json), and [deployment manifest](../evidence/deployment.json) are committed for independent verification. `scripts/verify_history.py` successfully recomputed all six event hashes, both decision hashes and the final on-chain head.
